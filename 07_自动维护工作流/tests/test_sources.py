import hashlib
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from skill_maintainer.ledger import LedgerStore
from skill_maintainer.queries import QueryJob
from skill_maintainer.sources.base import (
    HttpResponse,
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

    def test_huggingface_uses_offset_pagination_and_can_persist_immutable_evidence(self):
        transport = FakeHttp([
            (200, [{"id": "org/two", "author": "org", "lastModified": "2026-01-02T00:00:00Z"}, {"id": "org/one", "author": "org"}]),
            (200, []),
        ])
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            batch = HuggingFaceAdapter(transport=transport, page_size=2, evidence_directory=root).search(job("Hugging Face Spaces"), None)
            self.assertEqual(batch.status, "complete")
            self.assertEqual([item.native_id for item in batch.candidates], ["org/one", "org/two"])
            self.assertEqual([url for url, _ in transport.urls], [
                "https://huggingface.co/api/spaces?search=chemistry+Skill&limit=2&offset=0",
                "https://huggingface.co/api/spaces?search=chemistry+Skill&limit=2&offset=2",
            ])
            snapshots = list(root.glob("*.json"))
            self.assertEqual(len(snapshots), 2)
            self.assertEqual(snapshots[0].read_bytes(), batch.requests[0].response_bytes)


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
