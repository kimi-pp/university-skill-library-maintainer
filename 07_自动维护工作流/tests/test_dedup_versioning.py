import io
import json
import tempfile
import unittest
from unittest.mock import patch
from dataclasses import replace
from datetime import date
from hashlib import sha256
from pathlib import Path

from skill_maintainer.dedup import canonical_key, deduplicate
from skill_maintainer.ledger import LedgerStore
from skill_maintainer.ledger_schema import CURRENT_SKILL_COLUMNS
from skill_maintainer.review import DerivedFields, ObservedFacts, ProjectJudgments, ReviewDecision, apply_reviews_from_stream, build_review_packet
from skill_maintainer.snapshots import SnapshotCandidate, build_snapshot
from skill_maintainer.versioning import VersionDecision, apply_approved_version, compare_version


def review_snapshot_hash(content: bytes = b"# review evidence") -> str:
    digest = sha256()
    digest.update(b"SKILL.md")
    digest.update(b"\0")
    digest.update(str(len(content)).encode("ascii"))
    digest.update(b"\0")
    digest.update(sha256(content).digest())
    return digest.hexdigest()


def formal_row(number: int = 1, **overrides):
    row = {column: "已填" for column in CURRENT_SKILL_COLUMNS}
    row.update({
        "内部标识": f"SK-{number:04d}",
        "Skill名称": f"skill-{number}",
        "规范名称": f"技能 {number}",
        "入库层级": "正式",
        "功能一级分类": "01",
        "功能二级标签": "教学设计",
        "原生生态": "Codex",
        "来源形态": "Skill",
        "来源平台": "GitHub",
        "发现地址": f"https://example.invalid/discovery/{number}",
        "收集日期": date(2026, 8, 27),
        "Canonical source": f"https://github.com/example/skill-{number}",
        "上游项目地址": f"https://github.com/example/skill-{number}",
        "Skill入口路径": "SKILL.md",
        "发布者": "example",
        "固定版本": f"v{number}.0.0",
        "固定版本内容指纹": f"{number:064x}",
        "许可证": "MIT",
        "外部联网/API 调用": "否",
        "远程服务端点": "",
        "安全等级": "SA",
        "验证状态": "全部通过（未实测）",
        "验证证据位置": f"evidence/skill-{number}",
        "质量评分": 5,
    })
    row.update(overrides)
    return row


def candidate(platform: str, source_url: str, **overrides):
    value = {
        "platform": platform,
        "source_url": source_url,
        "canonical_source": "https://github.com/acme/course-designer",
        "upstream_identity": "acme/course-designer",
        "entry_path": "skills/course/SKILL.md",
        "content_hash": "a" * 64,
        "name": "Course Designer",
        "function": "build a course outline from a syllabus",
        "observed_on": "2026-08-27",
    }
    value.update(overrides)
    return value


class DeduplicationTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.ledger = LedgerStore.create(Path(self.temporary.name) / "ledger.xlsx")

    def test_cross_platform_upstream_becomes_one_stable_skill_with_three_aliases(self):
        result = deduplicate((
            candidate("SkillHub", "https://skillhub.example/acme/course-designer"),
            candidate("ClawHub", "https://clawhub.example/acme/course-designer"),
            candidate("GitHub", "https://github.com/acme/course-designer"),
        ), self.ledger)

        self.assertEqual(result.product_count, 1)
        self.assertEqual(len(result.skills), 1)
        self.assertEqual(len(result.aliases), 3)
        self.assertEqual({alias["内部标识"] for alias in result.aliases}, {result.skills[0]["内部标识"]})
        self.assertEqual({alias["来源平台"] for alias in result.aliases}, {"SkillHub", "ClawHub", "GitHub"})
        self.assertTrue(all(alias["去重依据"] for alias in result.aliases))

    def test_same_name_with_different_function_remains_separate(self):
        result = deduplicate((
            candidate("GitHub", "https://github.com/acme/course-designer"),
            candidate(
                "Hugging Face Spaces", "https://huggingface.co/spaces/acme/course-designer",
                canonical_source="https://huggingface.co/spaces/acme/course-designer",
                upstream_identity="acme/course-designer-space",
                entry_path="app.py",
                content_hash="b" * 64,
                function="generate classroom illustrations from prompts",
            ),
        ), self.ledger)

        self.assertEqual(result.product_count, 2)
        self.assertEqual(len(result.manual_review), 0)

    def test_insufficient_name_similarity_is_manual_review_not_merge(self):
        result = deduplicate((
            candidate("GitHub", "https://github.com/acme/course-designer"),
            candidate(
                "ClawHub", "https://clawhub.example/other/course-design",
                canonical_source="",
                upstream_identity="",
                entry_path="",
                content_hash="",
                name="Course Design Assistant",
            ),
        ), self.ledger)

        self.assertEqual(result.product_count, 2)
        self.assertEqual(len(result.manual_review), 1)
        self.assertEqual(result.manual_review[0]["观察状态"], "manual_review")
        self.assertEqual(result.manual_review[0]["原因"], "possible_duplicate")

    def test_safe_canonical_url_normalization_merges_but_repo_or_entry_difference_does_not(self):
        self.assertEqual(
            canonical_key(candidate("GitHub", "https://github.com/acme/course-designer")),
            canonical_key(candidate("GitHub", "https://GITHUB.com/acme/course-designer.git/")),
        )
        merged = deduplicate((
            candidate("GitHub", "https://github.com/acme/course-designer"),
            candidate("ClawHub", "https://clawhub.example/mirror", canonical_source="https://GITHUB.com/acme/course-designer.git/"),
        ), self.ledger)
        separate = deduplicate((
            candidate("GitHub", "https://github.com/acme/course-designer"),
            candidate("GitHub", "https://github.com/acme/other", canonical_source="https://github.com/acme/other", upstream_identity="acme/other"),
            candidate("GitHub", "https://github.com/acme/course-designer/subskill", canonical_source="", entry_path="skills/other/SKILL.md"),
        ), self.ledger)

        self.assertEqual(merged.product_count, 1)
        self.assertEqual(separate.product_count, 3)

    def test_query_and_fragment_are_identity_not_tracking_noise(self):
        first = candidate("GitHub", "https://github.com/acme/course-designer?id=one", canonical_source="https://github.com/acme/course-designer?id=one")
        second = candidate("GitHub", "https://github.com/acme/course-designer?id=two#entry", canonical_source="https://github.com/acme/course-designer?id=two#entry")

        self.assertNotEqual(canonical_key(first), canonical_key(second))
        self.assertEqual(deduplicate((first, second), self.ledger).product_count, 2)

    def test_same_canonical_repository_with_different_known_entry_paths_stays_separate(self):
        first = candidate("GitHub", "https://github.com/acme/mono", canonical_source="https://github.com/acme/mono", entry_path="skills/a/SKILL.md")
        second = candidate("GitHub", "https://github.com/acme/mono", canonical_source="https://github.com/acme/mono", entry_path="skills/b/SKILL.md")

        self.assertEqual(deduplicate((first, second), self.ledger).product_count, 2)

    def test_transitive_pair_evidence_cannot_merge_across_a_strong_identity_conflict(self):
        first = candidate("GitHub", "https://github.com/acme/a", canonical_source="https://github.com/acme/a", upstream_identity="", entry_path="", content_hash="c" * 64)
        bridge = candidate("ClawHub", "https://clawhub.example/bridge", canonical_source="", upstream_identity="acme/shared", entry_path="SKILL.md", content_hash="c" * 64)
        third = candidate("GitHub", "https://github.com/acme/c", canonical_source="https://github.com/acme/c", upstream_identity="acme/shared", entry_path="SKILL.md", content_hash="d" * 64)

        result = deduplicate((first, bridge, third), self.ledger)

        self.assertEqual(result.product_count, 2)
        self.assertEqual(len({item["内部标识"] for item in result.skills}), 2)

    def test_existing_source_alias_reuses_ledger_stable_id_but_untrusted_candidate_id_cannot(self):
        current = formal_row(8, **{"内部标识": "EXISTING-8", "Canonical source": "https://github.com/acme/existing"})
        self.ledger.append_rows("当前Skill", [current])
        self.ledger.append_rows("来源别名", [{
            "别名标识": "existing-alias", "内部标识": "EXISTING-8", "来源平台": "ClawHub",
            "来源地址": "https://clawhub.example/acme/existing", "Canonical source": current["Canonical source"],
            "关系类型": "跨平台别名", "去重依据": "已验证", "记录日期": "2026-08-27",
        }])
        alias_discovery = candidate("ClawHub", "https://clawhub.example/acme/existing", canonical_source="", upstream_identity="", entry_path="", content_hash="e" * 64, **{"内部标识": "ATTACKER"})
        conflict = candidate("GitHub", "https://github.com/other/skill", canonical_source="https://github.com/other/skill", upstream_identity="other/skill", entry_path="SKILL.md", content_hash="f" * 64, **{"内部标识": "EXISTING-8"})

        reused = deduplicate((alias_discovery,), self.ledger)
        rejected = deduplicate((conflict,), self.ledger)

        self.assertEqual(reused.skills[0]["内部标识"], "EXISTING-8")
        self.assertNotEqual(rejected.skills[0]["内部标识"], "EXISTING-8")
        self.assertTrue(any(item["原因"] == "untrusted_stable_id_conflict" for item in rejected.manual_review))

    def test_conflicting_current_and_alias_ledger_id_is_manual_review_not_a_third_skill(self):
        first = formal_row(31, **{"内部标识": "EXISTING-A", "Canonical source": "https://github.com/acme/mono"})
        second = formal_row(32, **{"内部标识": "EXISTING-B", "Canonical source": "https://github.com/acme/other"})
        self.ledger.append_rows("当前Skill", [first, second])
        self.ledger.append_rows("来源别名", [{
            "别名标识": "alias-b", "内部标识": "EXISTING-B", "来源平台": "ClawHub",
            "来源地址": "https://clawhub.example/acme/mono", "Canonical source": second["Canonical source"],
            "关系类型": "跨平台别名", "去重依据": "已验证", "记录日期": "2026-08-27",
        }])
        discovery = candidate("ClawHub", "https://clawhub.example/acme/mono", canonical_source=first["Canonical source"])

        forward = deduplicate((discovery,), self.ledger)
        reverse = deduplicate(tuple(reversed((discovery,))), self.ledger)

        self.assertEqual(forward.skills, ())
        self.assertEqual(forward.aliases, ())
        self.assertEqual(forward, reverse)
        self.assertEqual(len(forward.manual_review), 1)
        self.assertEqual(forward.manual_review[0]["原因"], "inconsistent_ledger")

    def test_stable_ids_are_independent_of_candidate_input_order(self):
        candidates = (
            candidate("GitHub", "https://github.com/acme/z", canonical_source="https://github.com/acme/z", upstream_identity="acme/z", content_hash="1" * 64),
            candidate("GitHub", "https://github.com/acme/a", canonical_source="https://github.com/acme/a", upstream_identity="acme/a", content_hash="2" * 64),
        )

        forward = deduplicate(candidates, self.ledger)
        reverse = deduplicate(tuple(reversed(candidates)), self.ledger)

        forward_ids = {item["Canonical source"]: item["内部标识"] for item in forward.skills}
        reverse_ids = {item["Canonical source"]: item["内部标识"] for item in reverse.skills}
        self.assertEqual(forward_ids, reverse_ids)

    def test_malformed_hash_never_merges_and_conflicting_identity_blocks_hash_fallback_without_entry(self):
        malformed_first = candidate("GitHub", "https://github.com/acme/first", canonical_source="", upstream_identity="", entry_path="", content_hash="unknown")
        malformed_second = candidate("ClawHub", "https://clawhub.example/second", canonical_source="", upstream_identity="", entry_path="", content_hash="unknown")
        conflicting_first = candidate("GitHub", "https://github.com/acme/first", canonical_source="https://github.com/acme/first", upstream_identity="", entry_path="", content_hash="3" * 64)
        conflicting_second = candidate("GitHub", "https://github.com/acme/second", canonical_source="https://github.com/acme/second", upstream_identity="", entry_path="", content_hash="3" * 64)

        self.assertEqual(deduplicate((malformed_first, malformed_second), self.ledger).product_count, 2)
        self.assertEqual(deduplicate((conflicting_first, conflicting_second), self.ledger).product_count, 2)

    def test_rerun_is_idempotent_for_stable_ids_and_aliases(self):
        candidates = (
            candidate("SkillHub", "https://skillhub.example/acme/course-designer"),
            candidate("GitHub", "https://github.com/acme/course-designer"),
        )

        first = deduplicate(candidates, self.ledger)
        second = deduplicate(candidates, self.ledger)

        self.assertEqual(first.skills, second.skills)
        self.assertEqual(first.aliases, second.aliases)
        self.assertEqual(len({alias["别名标识"] for alias in second.aliases}), 2)


class VersionRetentionTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.ledger = LedgerStore.create(Path(self.temporary.name) / "ledger.xlsx")
        self.current = formal_row()
        self.current["固定版本内容指纹"] = review_snapshot_hash()
        self.ledger.append_rows("当前Skill", [self.current])

    def observed(self, **overrides):
        value = {
            "内部标识": self.current["内部标识"],
            "fixed_version": "v2.0.0",
            "content_hash": review_snapshot_hash(b"# changed evidence"),
            "canonical_source": self.current["Canonical source"],
            "source_url": "https://github.com/example/skill-1/releases/tag/v2.0.0",
            "evidence_paths": ("snapshots/v2/SKILL.md",),
            "license": self.current["许可证"],
            "security_grade": self.current["安全等级"],
        }
        value.update(overrides)
        return value

    def approved(self, change, *, current=None, observed=None):
        current = current or change.current
        observed = observed or change.observed
        facts = ObservedFacts(
            fixed_version=observed["fixed_version"], entry_description_complete=True,
            prerequisites_clear_and_available=True, license=observed["license"],
            canonical_source=observed["canonical_source"], evidence_paths=tuple(observed["evidence_paths"]),
            remote_api_call="否", remote_endpoints=(), local_professional_software="无",
            local_script_plugin_interface="不使用", security_grade=observed["security_grade"],
            verification_status="全部通过（未实测）",
        )
        proposed = {key: value.isoformat() if isinstance(value, date) else value for key, value in current.items()}
        proposed.update({
            "固定版本": observed["fixed_version"], "固定版本内容指纹": observed["content_hash"],
            "Canonical source": observed["canonical_source"], "许可证": observed["license"],
            "安全等级": observed["security_grade"], "质量评分": 2,
            "验证状态": facts.verification_status, "验证证据位置": "；".join(facts.evidence_paths),
            "外部联网/API 调用": facts.remote_api_call, "远程服务端点": "",
            "本地专业软件或运行时依赖": facts.local_professional_software,
            "本地脚本/插件接口": facts.local_script_plugin_interface,
        })
        review = ReviewDecision(
            facts, ProjectJudgments("正式推荐", True, True, 5, (True,)),
            DerivedFields(quality_score=2, ledger_row=proposed), current["内部标识"],
        )
        with tempfile.TemporaryDirectory(dir=self.temporary.name) as temporary:
            root = Path(temporary)
            source = root / "candidate"
            source.mkdir()
            content = b"# review evidence" if observed["content_hash"] == review_snapshot_hash() else b"# changed evidence"
            (source / "SKILL.md").write_bytes(content)
            snapshot = build_snapshot(
                SnapshotCandidate(current["内部标识"], observed["fixed_version"], source, tuple(observed["evidence_paths"])), root / "snapshot",
            )
            packet = build_review_packet(
                {"id": current["内部标识"], "canonical_source": observed["canonical_source"], "license": observed["license"], "security_grade": observed["security_grade"],
                 "upstream_repository": current["上游项目地址"], "skill_entry_path": current["Skill入口路径"]},
                snapshot,
            )
        payload = {
            "decisions": [{
                "candidate_id": review.candidate_id,
                "observed_facts": {
                    "fixed_version": facts.fixed_version,
                    "entry_description_complete": facts.entry_description_complete,
                    "prerequisites_clear_and_available": facts.prerequisites_clear_and_available,
                    "license": facts.license,
                    "canonical_source": facts.canonical_source,
                    "evidence_paths": list(facts.evidence_paths),
                    "remote_api_call": facts.remote_api_call,
                    "remote_endpoints": list(facts.remote_endpoints),
                    "local_professional_software": facts.local_professional_software,
                    "local_script_plugin_interface": facts.local_script_plugin_interface,
                    "security_grade": facts.security_grade,
                    "verification_status": facts.verification_status,
                },
                "project_judgments": {
                    "record_tier": "正式推荐", "display_in_product": True, "direct_deployable": True,
                    "relevance_score": 5, "quality_bonus_flags": [True],
                },
                "derived_fields": {"quality_score": 2, "ledger_row": proposed},
            }]
        }
        review_ledger = LedgerStore.create(Path(self.temporary.name) / f"review-{len(list(Path(self.temporary.name).glob('review-*')))}.xlsx")
        receipt, = apply_reviews_from_stream(
            io.BytesIO(json.dumps(payload).encode("utf-8")), review_ledger, {current["内部标识"]: packet},
        )
        review_ledger.workbook.close()
        return VersionDecision.accept_from_applied_review(
            change, receipt, review_date="2026-08-27", conclusion_change="完整复审通过", proposed_row=proposed,
        )

    def test_unchanged_hash_does_nothing_and_new_tag_is_alias_observation_only(self):
        unchanged = compare_version(self.current, self.observed(
            fixed_version=self.current["固定版本"], content_hash=self.current["固定版本内容指纹"],
        ))
        retagged = compare_version(self.current, self.observed(content_hash=self.current["固定版本内容指纹"]))

        self.assertEqual(unchanged.status, "unchanged")
        self.assertFalse(unchanged.requires_full_review)
        self.assertEqual(retagged.status, "alias_observation")
        self.assertFalse(retagged.requires_full_review)
        apply_approved_version(self.ledger, self.approved(retagged))
        self.assertEqual(self.ledger.rows("当前Skill"), [self.current])
        self.assertEqual(len(self.ledger.rows("版本历史")), 0)
        self.assertEqual(len(self.ledger.rows("来源别名")), 1)
        self.assertEqual(self.ledger.rows("来源别名")[0]["固定版本"], retagged.observed["fixed_version"])

    def test_changed_content_requires_full_review_and_rejection_preserves_current_snapshot(self):
        change = compare_version(self.current, self.observed())

        self.assertEqual(change.status, "full_review_required")
        self.assertTrue(change.requires_full_review)
        apply_approved_version(self.ledger, VersionDecision.from_change(change, outcome="rejected"))

        self.assertEqual(self.ledger.rows("当前Skill"), [self.current])
        self.assertEqual(self.ledger.rows("版本历史"), [])

    def test_accepted_change_appends_history_before_current_and_append_failure_preserves_current(self):
        change = compare_version(self.current, self.observed())
        decision = self.approved(change)
        original_append = LedgerStore.append_rows

        def fail_history(store, sheet, rows):
            if sheet == "版本历史":
                raise OSError("simulated append failure")
            return original_append(store, sheet, rows)

        with patch.object(LedgerStore, "append_rows", fail_history):
            with self.assertRaises(OSError):
                apply_approved_version(self.ledger, decision)
        self.assertEqual(self.ledger.rows("当前Skill"), [self.current])
        self.assertEqual(self.ledger.rows("版本历史"), [])

        apply_approved_version(self.ledger, decision)

        history = self.ledger.rows("版本历史")
        current = self.ledger.rows("当前Skill")[0]
        self.assertEqual(len(history), 1)
        self.assertIn(self.current["固定版本"], history[0]["变更摘要"])
        self.assertIn(self.observed()["fixed_version"], history[0]["变更摘要"])
        self.assertIn(self.current["固定版本内容指纹"], history[0]["变更摘要"])
        self.assertIn(self.observed()["content_hash"], history[0]["变更摘要"])
        self.assertEqual(current["固定版本"], self.observed()["fixed_version"])
        self.assertEqual(current["固定版本内容指纹"], self.observed()["content_hash"])

    def test_history_integrity_checks_and_rerun_are_idempotent(self):
        change = compare_version(self.current, self.observed())
        accepted = self.approved(change)
        with self.assertRaisesRegex(ValueError, "固定版本内容指纹"):
            compare_version(self.current, self.observed(content_hash=""))
        with self.assertRaisesRegex(ValueError, "history_fields"):
            apply_approved_version(self.ledger, replace(accepted, history_fields={"old_hash": "attacker"}))

        apply_approved_version(self.ledger, accepted)
        with self.assertRaisesRegex(ValueError, "receipt"):
            apply_approved_version(self.ledger, accepted)

        self.assertEqual(len(self.ledger.rows("版本历史")), 1)
        self.assertEqual(self.ledger.rows("当前Skill")[0]["固定版本"], self.observed()["fixed_version"])

    def test_existing_history_identity_with_old_current_is_rejected(self):
        change = compare_version(self.current, self.observed())
        accepted = self.approved(change)
        apply_approved_version(self.ledger, accepted)
        self.ledger.upsert_skill(self.current)
        fresh_receipt = self.approved(change)

        with self.assertRaisesRegex(ValueError, "版本历史"):
            apply_approved_version(self.ledger, fresh_receipt)

    def test_non_hex_hash_and_blank_observed_version_cannot_create_updates_or_aliases(self):
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            compare_version(self.current, self.observed(content_hash="not-a-sha"))
        blank_version = compare_version(self.current, self.observed(fixed_version="", content_hash=self.current["固定版本内容指纹"]))

        self.assertEqual(blank_version.status, "unchanged")
        apply_approved_version(self.ledger, VersionDecision.from_change(blank_version, outcome="accepted"))
        self.assertEqual(self.ledger.rows("来源别名"), [])

    def test_upsert_failure_rolls_back_appended_history_and_ledger_state(self):
        change = compare_version(self.current, self.observed())
        decision = self.approved(change)
        original_workbook = self.ledger.workbook
        source_bytes = self.ledger.source_path.read_bytes()
        def fail_upsert(store, row):
            raise OSError("simulated current-row failure")

        with patch.object(LedgerStore, "upsert_skill", fail_upsert):
            with self.assertRaises(OSError):
                apply_approved_version(self.ledger, decision)

        self.assertEqual(self.ledger.rows("当前Skill"), [self.current])
        self.assertEqual(self.ledger.rows("版本历史"), [])
        self.assertIs(self.ledger.workbook, original_workbook)
        self.assertEqual(self.ledger.source_path.read_bytes(), source_bytes)

    def test_accepted_change_requires_trusted_task7_review_and_binds_persisted_current_row(self):
        change = compare_version(self.current, self.observed())
        with self.assertRaisesRegex(ValueError, "receipt"):
            apply_approved_version(self.ledger, VersionDecision.from_change(change, outcome="accepted"))

        forged_current = dict(self.current, **{"许可证": "Attacker-License"})
        forged_change = replace(change, current=forged_current)
        forged = self.approved(forged_change, current=forged_current)
        with self.assertRaisesRegex(ValueError, "当前Skill"):
            apply_approved_version(self.ledger, forged)

    def test_public_self_signed_review_factory_is_not_an_approval_capability(self):
        change = compare_version(self.current, self.observed())

        self.assertFalse(hasattr(VersionDecision, "approve"))
        with self.assertRaisesRegex(ValueError, "receipt"):
            VersionDecision.accept_from_applied_review(
                change, object(), review_date="2026-08-27", conclusion_change="完整复审通过", proposed_row=self.current,
            )

    def test_tampered_or_reused_task7_receipt_cannot_accept_a_version(self):
        change = compare_version(self.current, self.observed())
        accepted = self.approved(change)
        tampered = replace(accepted.applied_review, fixed_content_hash="a" * 64)
        with self.assertRaisesRegex(ValueError, "receipt"):
            VersionDecision.accept_from_applied_review(
                change, tampered, review_date="2026-08-27", conclusion_change="完整复审通过", proposed_row=accepted.proposed_row,
            )

        apply_approved_version(self.ledger, accepted)
        with self.assertRaisesRegex(ValueError, "receipt"):
            apply_approved_version(self.ledger, accepted)

    def test_deleted_upstream_marks_attention_without_deleting_current_or_snapshot(self):
        change = compare_version(self.current, self.observed(availability="deleted"))

        self.assertEqual(change.status, "attention_required")
        self.assertFalse(change.requires_full_review)
        apply_approved_version(self.ledger, VersionDecision.from_change(change, outcome="rejected"))

        self.assertEqual(self.ledger.rows("当前Skill"), [self.current])
        self.assertEqual(self.ledger.rows("版本历史"), [])
        observations = self.ledger.rows("候选观察")
        self.assertEqual(len(observations), 1)
        self.assertEqual(observations[0]["观察状态"], "attention_required")


if __name__ == "__main__":
    unittest.main()
