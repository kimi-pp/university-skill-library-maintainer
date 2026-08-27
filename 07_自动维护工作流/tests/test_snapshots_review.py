import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from skill_maintainer.ledger import LedgerStore
from skill_maintainer.snapshots import SnapshotCandidate, SnapshotLimits, build_snapshot
from skill_maintainer.review import (
    DerivedFields,
    ObservedFacts,
    ProjectJudgments,
    ReviewDecision,
    apply_reviews_from_stream,
    build_review_packet,
    score_quality,
    validate_review,
)


class SnapshotContractTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def _candidate(self, source, version="0123456789abcdef0123456789abcdef01234567"):
        return SnapshotCandidate("org/example", version, Path(source), ("https://evidence.example/commit",))

    def test_fixed_version_is_required_before_snapshotting(self):
        source = self.root / "candidate"
        source.mkdir()
        (source / "SKILL.md").write_text("# skill", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "固定版本"):
            build_snapshot(self._candidate(source, ""), self.root / "snapshot")

    def test_archive_path_traversal_is_rejected_without_writing_outside_destination(self):
        archive = self.root / "candidate.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("../escape.py", "raise RuntimeError")

        with self.assertRaisesRegex(ValueError, "路径穿越"):
            build_snapshot(self._candidate(archive), self.root / "snapshot")
        self.assertFalse((self.root / "escape.py").exists())

    def test_safe_nested_archive_file_is_snapshotted_inside_destination(self):
        archive = self.root / "candidate.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("instructions/SKILL.md", "# static instruction")

        manifest = build_snapshot(self._candidate(archive), self.root / "snapshot")

        self.assertEqual([entry.path for entry in manifest.files], ["instructions/SKILL.md"])
        self.assertTrue((self.root / "snapshot" / "instructions" / "SKILL.md").is_file())

    def test_linked_candidate_entries_are_rejected(self):
        source = self.root / "candidate"
        source.mkdir()
        (source / "SKILL.md").write_text("# skill", encoding="utf-8")
        linked = source / "outside"
        try:
            linked.symlink_to(self.root, target_is_directory=True)
        except OSError:
            self.skipTest("当前环境不允许创建符号链接安全回归夹具")

        with self.assertRaisesRegex(ValueError, "链接|重解析"):
            build_snapshot(self._candidate(source), self.root / "snapshot")

    def test_snapshot_enforces_file_count_total_and_single_file_bounds(self):
        source = self.root / "candidate"
        source.mkdir()
        (source / "one.md").write_text("one", encoding="utf-8")
        (source / "two.md").write_text("two", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "文件数量"):
            build_snapshot(self._candidate(source), self.root / "count", SnapshotLimits(max_files=1, max_total_bytes=10, max_file_bytes=10))
        with self.assertRaisesRegex(ValueError, "总字节"):
            build_snapshot(self._candidate(source), self.root / "total", SnapshotLimits(max_files=3, max_total_bytes=5, max_file_bytes=10))
        with self.assertRaisesRegex(ValueError, "单文件"):
            build_snapshot(self._candidate(source), self.root / "single", SnapshotLimits(max_files=3, max_total_bytes=10, max_file_bytes=2))

    def test_oversized_archive_member_is_rejected_before_its_content_is_read(self):
        archive = self.root / "candidate.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("payload.md", "too large")
        with patch.object(zipfile.ZipFile, "read", side_effect=AssertionError("oversized candidate must not be read")):
            with self.assertRaisesRegex(ValueError, "单文件"):
                build_snapshot(self._candidate(archive), self.root / "snapshot", SnapshotLimits(max_files=1, max_total_bytes=100, max_file_bytes=2))

    def test_static_snapshot_hashes_only_text_code_and_config_without_running_candidate(self):
        source = self.root / "candidate"
        source.mkdir()
        (source / "SKILL.md").write_text("# static only", encoding="utf-8")
        (source / "plugin.py").write_text("raise RuntimeError('must not run')", encoding="utf-8")
        (source / "settings.toml").write_text("enabled = false", encoding="utf-8")
        (source / "payload.bin").write_bytes(b"\x00\x01")

        with patch("subprocess.run", side_effect=AssertionError("candidate command must never run")):
            manifest = build_snapshot(self._candidate(source), self.root / "snapshot")

        entries = {entry.path: entry for entry in manifest.files}
        self.assertIsNotNone(entries["SKILL.md"].sha256)
        self.assertIsNotNone(entries["plugin.py"].sha256)
        self.assertIsNotNone(entries["settings.toml"].sha256)
        self.assertIsNone(entries["payload.bin"].sha256)
        self.assertFalse((self.root / "candidate-ran").exists())


class ReviewContractTest(unittest.TestCase):
    def _decision(self, **observed_overrides):
        facts = {
            "fixed_version": "0123456789abcdef0123456789abcdef01234567",
            "entry_description_complete": True,
            "prerequisites_clear_and_available": True,
            "license": "MIT",
            "canonical_source": "https://github.com/org/example",
            "evidence_paths": ("evidence/SKILL.md",),
            "remote_api_call": "否",
            "remote_endpoints": (),
            "local_professional_software": "Abaqus，实操时需要",
            "local_script_plugin_interface": "按需使用",
            "security_grade": "SA",
            "verification_status": "全部通过（未实测）",
        }
        facts.update(observed_overrides)
        observed = ObservedFacts(**facts)
        judgments = ProjectJudgments(
            record_tier="正式",
            display_in_product=True,
            direct_deployable=True,
            relevance_score=4,
            quality_bonus_flags=(True, True, True, True, True),
        )
        return ReviewDecision(observed, judgments, DerivedFields())

    def test_packet_carries_rule_versions_and_snapshot_evidence_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "candidate"
            source.mkdir()
            (source / "SKILL.md").write_text("# example", encoding="utf-8")
            snapshot = build_snapshot(SnapshotCandidate("org/example", "a" * 40, source, ("https://source.example/a",)), Path(temporary) / "snapshot")
            packet = build_review_packet({"id": "org/example"}, snapshot)

        self.assertIn("SKILL_RESEARCH_WORKFLOW", packet.rule_versions)
        self.assertIn("VALIDATION_PROTOCOL", packet.rule_versions)
        self.assertIn("snapshot/SKILL.md", packet.evidence_paths)

    def test_abaqus_markdown_is_local_boundary_not_remote_api(self):
        self.assertEqual(validate_review(self._decision()), ())

    def test_remote_endpoint_and_remote_api_flag_must_not_conflict(self):
        errors = validate_review(self._decision(remote_endpoints=("https://api.example",)))
        self.assertIn("observed_facts.remote_endpoints: remote API 标记为否时不得填写远程端点", errors)

    def test_unknown_license_cannot_be_formal(self):
        errors = validate_review(self._decision(license="unknown"))
        self.assertIn("observed_facts.license: 正式条目许可证未明确", errors)

    def test_sb_a_cannot_be_directly_deployed(self):
        errors = validate_review(self._decision(security_grade="SB-A"))
        self.assertIn("project_judgments.direct_deployable: SB-A 原包不得直接部署", errors)

    def test_relevance_two_is_not_product_displayable(self):
        decision = self._decision()
        decision = ReviewDecision(decision.observed_facts, ProjectJudgments("正式", True, True, 2, ()), decision.derived_fields)
        errors = validate_review(decision)
        self.assertIn("project_judgments.display_in_product: 相关度低于 3/5 不得展示", errors)

    def test_pending_verification_cannot_receive_sa_or_sb(self):
        errors = validate_review(self._decision(verification_status="待核验", security_grade="SA"))
        self.assertIn("observed_facts.security_grade: 待核验不得给出 SA/SB 正式等级", errors)

    def test_formal_requires_at_least_all_passed_not_tested(self):
        errors = validate_review(self._decision(verification_status="前两步通过"))
        self.assertIn("observed_facts.verification_status: 正式条目最低为全部通过（未实测）", errors)

    def test_quality_score_needs_exactly_all_four_admission_conditions_then_caps_bonuses_at_five(self):
        complete = self._decision()
        self.assertEqual(score_quality(complete), 5)
        missing = self._decision(entry_description_complete=False)
        self.assertEqual(score_quality(missing), 0)

    def test_derived_quality_score_cannot_override_observed_facts_or_project_judgments(self):
        decision = self._decision()
        decision = ReviewDecision(decision.observed_facts, decision.project_judgments, DerivedFields(quality_score=4))
        self.assertIn(
            "derived_fields.quality_score: 必须由事实和项目判断重新计算",
            validate_review(decision),
        )

    def test_quality_score_is_zero_when_safety_license_or_traceability_fails_regardless_of_popularity(self):
        for decision in (
            self._decision(security_grade="SC"),
            self._decision(license="unknown"),
            self._decision(canonical_source="", evidence_paths=()),
        ):
            with self.subTest(decision=decision):
                self.assertEqual(score_quality(decision), 0)

    def test_review_stdin_is_decoded_in_memory_validated_and_applied_to_staged_ledger(self):
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            stream = io.BytesIO(json.dumps({"decisions": []}, ensure_ascii=False).encode("utf-8"))
            self.assertEqual(apply_reviews_from_stream(stream, store), ())
            self.assertEqual(store.rows("当前Skill"), [])
            self.assertEqual(list(Path(temporary).glob("*.json")), [])

    def test_review_stdin_rejects_string_booleans_instead_of_treating_them_as_true(self):
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            payload = {
                "decisions": [{
                    "observed_facts": {
                        "fixed_version": "a" * 40,
                        "entry_description_complete": "false",
                        "prerequisites_clear_and_available": True,
                        "license": "MIT",
                        "canonical_source": "https://github.com/org/example",
                        "evidence_paths": ["evidence/SKILL.md"],
                        "remote_api_call": "否",
                        "remote_endpoints": [],
                        "local_professional_software": "无",
                        "local_script_plugin_interface": "不使用",
                        "security_grade": "SA",
                        "verification_status": "全部通过（未实测）",
                    },
                    "project_judgments": {
                        "record_tier": "正式", "display_in_product": True, "direct_deployable": True,
                        "relevance_score": 4, "quality_bonus_flags": [],
                    },
                    "derived_fields": {},
                }]
            }
            with self.assertRaisesRegex(ValueError, "布尔"):
                apply_reviews_from_stream(io.BytesIO(json.dumps(payload).encode("utf-8")), store)


if __name__ == "__main__":
    unittest.main()
