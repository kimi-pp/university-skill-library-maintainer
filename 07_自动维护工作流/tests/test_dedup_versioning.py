import tempfile
import unittest
from dataclasses import replace
from datetime import date
from pathlib import Path

from skill_maintainer.dedup import canonical_key, deduplicate
from skill_maintainer.ledger import LedgerStore
from skill_maintainer.ledger_schema import CURRENT_SKILL_COLUMNS
from skill_maintainer.versioning import VersionDecision, apply_approved_version, compare_version


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
        "固定版本内容指纹": f"sha256:{number:064x}",
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
        "content_hash": "sha256:" + "a" * 64,
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
                content_hash="sha256:" + "b" * 64,
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
        self.ledger.append_rows("当前Skill", [self.current])

    def observed(self, **overrides):
        value = {
            "内部标识": self.current["内部标识"],
            "fixed_version": "v2.0.0",
            "content_hash": "sha256:" + "f" * 64,
            "canonical_source": self.current["Canonical source"],
            "source_url": "https://github.com/example/skill-1/releases/tag/v2.0.0",
            "evidence_paths": ("snapshots/v2/SKILL.md",),
        }
        value.update(overrides)
        return value

    def test_unchanged_hash_does_nothing_and_new_tag_is_alias_observation_only(self):
        unchanged = compare_version(self.current, self.observed(
            fixed_version=self.current["固定版本"], content_hash=self.current["固定版本内容指纹"],
        ))
        retagged = compare_version(self.current, self.observed(content_hash=self.current["固定版本内容指纹"]))

        self.assertEqual(unchanged.status, "unchanged")
        self.assertFalse(unchanged.requires_full_review)
        self.assertEqual(retagged.status, "alias_observation")
        self.assertFalse(retagged.requires_full_review)
        apply_approved_version(self.ledger, VersionDecision.from_change(retagged, outcome="accepted"))
        self.assertEqual(self.ledger.rows("当前Skill"), [self.current])
        self.assertEqual(len(self.ledger.rows("版本历史")), 0)
        self.assertEqual(len(self.ledger.rows("来源别名")), 1)

    def test_changed_content_requires_full_review_and_rejection_preserves_current_snapshot(self):
        change = compare_version(self.current, self.observed())

        self.assertEqual(change.status, "full_review_required")
        self.assertTrue(change.requires_full_review)
        apply_approved_version(self.ledger, VersionDecision.from_change(change, outcome="rejected"))

        self.assertEqual(self.ledger.rows("当前Skill"), [self.current])
        self.assertEqual(self.ledger.rows("版本历史"), [])

    def test_accepted_change_appends_history_before_current_and_append_failure_preserves_current(self):
        change = compare_version(self.current, self.observed())
        decision = VersionDecision.from_change(
            change,
            outcome="accepted",
            review_date="2026-08-27",
            conclusion_change="安全、许可证和专业映射已完整复审",
        )
        original_append = self.ledger.append_rows

        def fail_history(sheet, rows):
            if sheet == "版本历史":
                raise OSError("simulated append failure")
            return original_append(sheet, rows)

        self.ledger.append_rows = fail_history
        with self.assertRaises(OSError):
            apply_approved_version(self.ledger, decision)
        self.assertEqual(self.ledger.rows("当前Skill"), [self.current])
        self.assertEqual(self.ledger.rows("版本历史"), [])
        self.ledger.append_rows = original_append

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
        accepted = VersionDecision.from_change(change, outcome="accepted")
        with self.assertRaisesRegex(ValueError, "固定版本内容指纹"):
            compare_version(self.current, self.observed(content_hash=""))
        with self.assertRaisesRegex(ValueError, "history_fields"):
            apply_approved_version(self.ledger, replace(accepted, history_fields={"old_hash": "attacker"}))

        apply_approved_version(self.ledger, accepted)
        apply_approved_version(self.ledger, accepted)

        self.assertEqual(len(self.ledger.rows("版本历史")), 1)
        self.assertEqual(self.ledger.rows("当前Skill")[0]["固定版本"], self.observed()["fixed_version"])

    def test_existing_history_identity_with_old_current_is_rejected(self):
        change = compare_version(self.current, self.observed())
        accepted = VersionDecision.from_change(change, outcome="accepted")
        apply_approved_version(self.ledger, accepted)
        self.ledger.upsert_skill(self.current)

        with self.assertRaisesRegex(ValueError, "版本历史"):
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
