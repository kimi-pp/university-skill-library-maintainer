import hashlib
import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from skill_maintainer.ledger import LedgerStore
from skill_maintainer.queries import QueryJob
from skill_maintainer.sources.base import (
    HttpResponse,
    EvidenceRoot,
    SourceWatermarkStore,
    Watermark,
    doctor_smoke,
)
from skill_maintainer.sources.clawhub import ClawHubAdapter
from skill_maintainer.sources.github import GitHubAdapter
from skill_maintainer.sources.huggingface import HuggingFaceAdapter
from skill_maintainer.sources.skillhub import SkillHubAdapter


def job(platform="SkillHub", query="chemistry Skill"):
    return QueryJob("Q-test", "0703", platform, "method", query)


class FakeHttp:
    def __init__(self, responses):
        self.responses = list(responses)
        self.urls = []

    def __call__(self, url, timeout):
        self.urls.append((url, timeout))
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        status, body = item
        return HttpResponse(url=url, status=status, body=json.dumps(body).encode("utf-8"))


class SourceAdapterContractTest(unittest.TestCase):
    def test_doctor_smoke_uses_a_fixed_query_and_never_follows_pagination(self):
        transport = FakeHttp([(200, {"items": [{"id": "one"}], "has_next": True})])
        result = doctor_smoke(SkillHubAdapter(transport=transport), platform="SkillHub")

        self.assertTrue(result.ok)
        self.assertEqual(result.pages_checked, 1)
        self.assertEqual([url for url, _ in transport.urls], [
            "https://api.skillhub.cn/api/skills?query=university+skill&page=1&limit=50"
        ])
    def test_skillhub_fetches_all_pages_records_hashes_and_sorts_results(self):
        transport = FakeHttp([
            (200, {"items": [{"id": "b", "name": "Beta"}, {"id": "a", "name": "Alpha"}], "has_next": True}),
            (200, {"items": [{"id": "c", "name": "Gamma"}], "has_next": False}),
        ])
        adapter = SkillHubAdapter(transport=transport, timeout=9, page_size=2)

        batch = adapter.search(job(), None)

        self.assertEqual(batch.status, "complete")
        self.assertEqual([item.native_id for item in batch.candidates], ["a", "b", "c"])
        self.assertEqual(
            [url for url, _ in transport.urls],
            [
                "https://api.skillhub.cn/api/skills?query=chemistry+Skill&page=1&limit=2",
                "https://api.skillhub.cn/api/skills?query=chemistry+Skill&page=2&limit=2",
            ],
        )
        self.assertTrue(all(timeout == 9 for _, timeout in transport.urls))
        self.assertEqual(batch.requests[0].response_sha256, hashlib.sha256(json.dumps({"items": [{"id": "b", "name": "Beta"}, {"id": "a", "name": "Alpha"}], "has_next": True}).encode("utf-8")).hexdigest())
        self.assertTrue(batch.requests[-1].last_page)

    def test_clawhub_retries_transient_error_and_is_partial_after_a_later_failure(self):
        transport = FakeHttp([
            (500, {"error": "temporary"}),
            (200, {"results": [{"slug": "one", "name": "One"}], "has_next": True}),
            (503, {"error": "unavailable"}),
            (503, {"error": "unavailable"}),
        ])
        batch = ClawHubAdapter(transport=transport, retries=1, page_size=1).search(job("ClawHub"), None)

        self.assertEqual(batch.status, "partial")
        self.assertEqual([item.native_id for item in batch.candidates], ["one"])
        self.assertEqual([event.attempts for event in batch.requests], [2, 2])
        self.assertEqual(batch.errors[0].status_code, 503)
        self.assertEqual(batch.errors[0].query_id, "Q-test")

    def test_github_stops_at_the_search_ceiling_and_does_not_retry_query_parse_errors(self):
        pages = [(200, {"total_count": 1001, "items": [{"id": index, "full_name": f"org/{index}", "html_url": f"https://github.com/org/{index}"}]}) for index in range(10)]
        transport = FakeHttp(pages)
        batch = GitHubAdapter(command_runner=None, transport=transport, page_size=100).search(job("GitHub"), None)
        self.assertEqual(batch.status, "partial")
        self.assertEqual(len(batch.candidates), 10)
        self.assertEqual(len(batch.requests), 10)
        self.assertIn("1000", batch.errors[0].message)

        parse_transport = FakeHttp([(422, {"message": "Validation Failed"})])
        failed = GitHubAdapter(command_runner=None, transport=parse_transport, retries=3).search(job("GitHub"), None)
        self.assertEqual(failed.status, "failed")
        self.assertEqual(len(parse_transport.urls), 1)
        self.assertEqual(failed.errors[0].status_code, 422)

    def test_github_command_runner_extracts_422_from_stderr_without_retrying(self):
        calls = []

        def runner(arguments):
            calls.append(arguments)
            return SimpleNamespace(returncode=1, stdout=b"", stderr=b'{"message":"Validation Failed","status":422}')

        batch = GitHubAdapter(command_runner=runner, retries=3).search(job("GitHub"), None)

        self.assertEqual(batch.status, "failed")
        self.assertEqual(batch.errors[0].status_code, 422)
        self.assertEqual(batch.errors[0].query_id, "Q-test")
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0], ["gh", "api", "--method", "GET", "/search/repositories?q=chemistry+Skill&per_page=50&page=1"])

    def test_huggingface_uses_offset_pagination_and_can_persist_immutable_evidence(self):
        transport = FakeHttp([
            (200, [{"id": "org/two", "author": "org", "lastModified": "2026-01-02T00:00:00Z"}, {"id": "org/one", "author": "org"}]),
            (200, []),
        ])
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            batch = HuggingFaceAdapter(transport=transport, page_size=2, evidence_root=EvidenceRoot(root)).search(job("Hugging Face Spaces"), None)
            self.assertEqual(batch.status, "complete")
            self.assertEqual([item.native_id for item in batch.candidates], ["org/one", "org/two"])
            self.assertEqual([url for url, _ in transport.urls], [
                "https://huggingface.co/api/spaces?search=chemistry+Skill&limit=2&offset=0&sort=lastModified&direction=-1",
                "https://huggingface.co/api/spaces?search=chemistry+Skill&limit=2&offset=2&sort=lastModified&direction=-1",
            ])
            snapshots = list(root.glob("*.json"))
            self.assertEqual(len(snapshots), 2)
            self.assertEqual(snapshots[0].read_bytes(), batch.requests[0].response_bytes)

    def test_huggingface_incremental_search_sorts_then_filters_at_the_exact_watermark(self):
        watermark = Watermark("Hugging Face Spaces", "chemistry Skill", datetime(2026, 1, 2, tzinfo=timezone.utc), "old")
        transport = FakeHttp([
            (200, [
                {"id": "org/new", "lastModified": "2026-01-03T00:00:00Z"},
                {"id": "org/boundary", "lastModified": "2026-01-02T00:00:00Z"},
            ]),
        ])
        batch = HuggingFaceAdapter(transport=transport, page_size=2).search(job("Hugging Face Spaces"), watermark)

        self.assertEqual([item.native_id for item in batch.candidates], ["org/new"])
        self.assertTrue(batch.requests[0].last_page)
        self.assertEqual([url for url, _ in transport.urls], [
            "https://huggingface.co/api/spaces?search=chemistry+Skill&limit=2&offset=0&sort=lastModified&direction=-1"
        ])

    def test_huggingface_marks_incremental_coverage_partial_when_a_timestamp_is_unknown(self):
        watermark = Watermark("Hugging Face Spaces", "chemistry Skill", datetime(2026, 1, 2, tzinfo=timezone.utc), "old")
        batch = HuggingFaceAdapter(
            transport=FakeHttp([(200, [{"id": "org/unknown"}])])
        ).search(job("Hugging Face Spaces"), watermark)
        self.assertEqual(batch.status, "partial")
        self.assertEqual(batch.errors[0].query_id, "Q-test")

    def test_version_and_snapshot_use_platform_endpoints_not_the_native_id_as_a_url(self):
        cases = (
            (SkillHubAdapter, "skill-1", "https://api.skillhub.cn/api/skills/skill-1", {"version": "v1"}),
            (ClawHubAdapter, "skill-1", "https://clawhub.ai/api/v1/skills/skill-1", {"version": "v1"}),
            (HuggingFaceAdapter, "org/space", "https://huggingface.co/api/spaces/org/space", {"sha": "abc"}),
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = EvidenceRoot(Path(temporary))
            for adapter_type, identity, endpoint, payload in cases:
                with self.subTest(platform=adapter_type.platform):
                    raw = json.dumps(payload).encode("utf-8")
                    transport = FakeHttp([(200, payload), (200, payload)])
                    adapter = adapter_type(transport=transport, evidence_root=root)
                    observation = adapter.latest_version(identity)
                    result = adapter.snapshot(identity, observation.version, Path(f"{adapter.platform}.json"))
                    self.assertEqual([url for url, _ in transport.urls], [endpoint, endpoint + "?version=" + observation.version])
                    self.assertEqual(observation.response_evidence_sha256, hashlib.sha256(raw).hexdigest())
                    self.assertEqual(result.sha256, hashlib.sha256(raw).hexdigest())
                    self.assertEqual((Path(temporary) / f"{adapter.platform}.json").read_bytes(), raw)

    def test_identity_endpoints_accept_supported_discovery_urls(self):
        self.assertEqual(
            SkillHubAdapter().identity_endpoint("https://skillhub.cn/skills/skill-1"),
            "https://api.skillhub.cn/api/skills/skill-1",
        )
        self.assertEqual(
            ClawHubAdapter().identity_endpoint("https://clawhub.ai/skills/skill-1"),
            "https://clawhub.ai/api/v1/skills/skill-1",
        )
        self.assertEqual(
            HuggingFaceAdapter().identity_endpoint("https://huggingface.co/spaces/org/space"),
            "https://huggingface.co/api/spaces/org/space",
        )

    def test_github_version_resolves_branch_to_commit_and_snapshots_the_fixed_archive(self):
        calls = []

        def runner(arguments):
            calls.append(arguments)
            bodies = (
                b'{"full_name":"org/repo","default_branch":"main"}',
                b'{"sha":"0123456789abcdef0123456789abcdef01234567"}',
                b"fixed archive bytes",
            )
            return SimpleNamespace(returncode=0, stdout=bodies[len(calls) - 1], stderr=b"")

        with tempfile.TemporaryDirectory() as temporary:
            adapter = GitHubAdapter(command_runner=runner, evidence_root=EvidenceRoot(Path(temporary)))
            observation = adapter.latest_version("https://github.com/org/repo")
            snapshot = adapter.snapshot("org/repo", observation.version, Path("repo.zip"))
            self.assertEqual(observation.version, "0123456789abcdef0123456789abcdef01234567")
            self.assertEqual(snapshot.sha256, hashlib.sha256(b"fixed archive bytes").hexdigest())
            self.assertEqual(calls, [
                ["gh", "api", "--method", "GET", "/repos/org/repo"],
                ["gh", "api", "--method", "GET", "/repos/org/repo/commits/main"],
                ["gh", "api", "--method", "GET", "/repos/org/repo/zipball/0123456789abcdef0123456789abcdef01234567"],
            ])

    def test_github_search_candidate_identity_closes_the_version_and_snapshot_loop(self):
        calls = []

        def runner(arguments):
            calls.append(arguments)
            bodies = (
                b'{"total_count":1,"items":[{"id":42,"full_name":"org/repo","html_url":"https://github.com/org/repo"}]}',
                b'{"full_name":"org/repo","default_branch":"main"}',
                b'{"sha":"0123456789abcdef0123456789abcdef01234567"}',
                b"fixed archive bytes",
            )
            return SimpleNamespace(returncode=0, stdout=bodies[len(calls) - 1], stderr=b"")

        with tempfile.TemporaryDirectory() as temporary:
            adapter = GitHubAdapter(command_runner=runner, evidence_root=EvidenceRoot(Path(temporary)))
            candidate = adapter.search(job("GitHub"), None).candidates[0]
            observation = adapter.latest_version(candidate.native_id)
            snapshot = adapter.snapshot(candidate.native_id, observation.version, Path("repo.zip"))
            self.assertEqual(candidate.native_id, "org/repo")
            self.assertEqual(candidate.popularity["repository_id"], 42)
            self.assertEqual(snapshot.sha256, hashlib.sha256(b"fixed archive bytes").hexdigest())
            self.assertEqual(calls[-3:], [
                ["gh", "api", "--method", "GET", "/repos/org/repo"],
                ["gh", "api", "--method", "GET", "/repos/org/repo/commits/main"],
                ["gh", "api", "--method", "GET", "/repos/org/repo/zipball/0123456789abcdef0123456789abcdef01234567"],
            ])

    def test_github_snapshot_rejects_non_immutable_refs_without_a_network_call(self):
        calls = []

        def runner(arguments):
            calls.append(arguments)
            return SimpleNamespace(returncode=0, stdout=b"archive", stderr=b"")

        with tempfile.TemporaryDirectory() as temporary:
            adapter = GitHubAdapter(command_runner=runner, evidence_root=EvidenceRoot(Path(temporary)))
            for version in (None, "", "main", "v1.2.3", "a" * 39, "g" * 40, "a" * 41):
                with self.subTest(version=version):
                    result = adapter.snapshot("org/repo", version, Path("repo.zip"))
                    self.assertIsNotNone(result.error)
            self.assertEqual(calls, [])

    def test_version_and_snapshot_preserve_http_errors_without_writing_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root_path = Path(temporary)
            adapter = ClawHubAdapter(
                transport=FakeHttp([(404, {"message": "missing"}), (404, {"message": "missing"})]),
                evidence_root=EvidenceRoot(root_path),
            )
            observation = adapter.latest_version("gone")
            result = adapter.snapshot("gone", "v1", Path("gone.json"))
            self.assertEqual(observation.error.status_code, 404)
            self.assertEqual(result.error.status_code, 404)
            self.assertFalse((root_path / "gone.json").exists())

    def test_snapshot_reports_directory_permission_and_content_conflict_errors(self):
        with tempfile.TemporaryDirectory() as temporary:
            root_path = Path(temporary)
            root = EvidenceRoot(root_path)
            adapter = SkillHubAdapter(
                transport=FakeHttp([(200, {"version": "v1"})] * 3), evidence_root=root
            )
            (root_path / "directory.json").mkdir()
            directory_result = adapter.snapshot("skill", "v1", Path("directory.json"))
            self.assertIsNotNone(directory_result.error)

            (root_path / "conflict.json").write_bytes(b"old")
            conflict_result = adapter.snapshot("skill", "v1", Path("conflict.json"))
            self.assertIsNotNone(conflict_result.error)

            with patch("skill_maintainer.sources.base.os.open", side_effect=PermissionError("denied")):
                denied_result = adapter.snapshot("skill", "v1", Path("denied.json"))
            self.assertIsNotNone(denied_result.error)

    def test_evidence_root_rejects_escape_and_symlink_destinations(self):
        with tempfile.TemporaryDirectory() as temporary:
            root_path = Path(temporary) / "evidence"
            root_path.mkdir()
            root = EvidenceRoot(root_path)
            with self.assertRaises(ValueError):
                root.write(Path("../escape.json"), b"data")
            link = root_path / "linked"
            try:
                link.symlink_to(Path(temporary), target_is_directory=True)
            except OSError:
                self.skipTest("当前环境不允许创建用于安全回归的符号链接")
            with self.assertRaises(ValueError):
                root.write(Path("linked/escape.json"), b"data")

    def test_evidence_root_retries_a_concurrent_same_content_exclusive_create(self):
        with tempfile.TemporaryDirectory() as temporary:
            root_path = Path(temporary)
            root = EvidenceRoot(root_path)
            original_open = os.open
            calls = []

            def concurrent_open(path, flags, mode):
                calls.append(path)
                if len(calls) == 1:
                    Path(path).write_bytes(b"stable")
                    raise FileExistsError("concurrent writer")
                return original_open(path, flags, mode)

            with patch("skill_maintainer.sources.base.os.open", side_effect=concurrent_open):
                self.assertEqual(root.write(Path("race.json"), b"stable"), root_path / "race.json")
            self.assertEqual(len(calls), 1)

    def test_search_turns_page_evidence_write_errors_into_a_query_scoped_batch_error(self):
        payload = {"items": []}
        raw = json.dumps(payload).encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            root_path = Path(temporary)
            name = f"skillhub-page-0001-{hashlib.sha256(raw).hexdigest()}.json"
            (root_path / name).mkdir()
            batch = SkillHubAdapter(
                transport=FakeHttp([(200, payload)]), evidence_root=EvidenceRoot(root_path)
            ).search(job(), None)
            self.assertEqual(batch.status, "failed")
            self.assertEqual(batch.errors[0].query_id, "Q-test")
            self.assertIn("普通文件", batch.errors[0].message)

    def test_search_keeps_already_discovered_candidates_as_partial_when_evidence_write_fails(self):
        payload = {"items": [{"id": "one", "name": "One"}]}
        raw = json.dumps(payload).encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            root_path = Path(temporary)
            name = f"skillhub-page-0001-{hashlib.sha256(raw).hexdigest()}.json"
            (root_path / name).mkdir()
            batch = SkillHubAdapter(
                transport=FakeHttp([(200, payload)]), evidence_root=EvidenceRoot(root_path)
            ).search(job(), None)
            self.assertEqual(batch.status, "partial")
            self.assertEqual([candidate.native_id for candidate in batch.candidates], ["one"])


class SourceWatermarkTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.ledger = LedgerStore.create(Path(self.temporary.name) / "ledger.xlsx")
        self.store = SourceWatermarkStore(self.ledger)
        self.old = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.store.write(Watermark("SkillHub", "chemistry Skill", self.old, "old", "baseline"))

    def test_only_complete_batch_advances_its_own_platform_watermark(self):
        completed = type("Batch", (), {"status": "complete", "platform": "SkillHub"})()
        partial = type("Batch", (), {"status": "partial", "platform": "ClawHub"})()
        failed = type("Batch", (), {"status": "failed", "platform": "SkillHub"})()
        now = self.old + timedelta(days=1)

        self.assertTrue(self.store.advance_if_complete(job(), completed, now, "new"))
        self.assertFalse(self.store.advance_if_complete(job("ClawHub"), partial, now, "ignored"))
        self.assertFalse(self.store.advance_if_complete(job(), failed, now, "ignored"))
        self.assertEqual(self.store.read("SkillHub", "chemistry Skill").identifier, "new")
        self.assertIsNone(self.store.read("ClawHub", "chemistry Skill"))

    def test_due_full_recheck_ignores_but_preserves_incremental_watermark(self):
        decision = self.store.for_run(
            "SkillHub", "chemistry Skill", self.old + timedelta(days=8), full_recheck_interval_days=7
        )
        self.assertTrue(decision.full_recheck)
        self.assertIsNone(decision.search_watermark)
        self.assertEqual(self.store.read("SkillHub", "chemistry Skill").identifier, "old")


if __name__ == "__main__":
    unittest.main()
