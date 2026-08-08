"""Property 1–4 测试：issues.json 自校验与 group_id 一致性。

- P1: 合法 issues.json 通过 validate_issues_json → 空错误列表；违规输入返回非空
- P2: json 序列化往返保信
- P3: scope=document/chapter 时 excerpt 必须为 ""
- P4: 同四元组 issues 共享 group_id；不同四元组分配不同 group_id

Feature: unified-thesis-reviewer
"""
from __future__ import annotations

import sys
from pathlib import Path

# 把 tests/ 目录加入 sys.path 以便 import 本目录下的辅助模块
sys.path.insert(0, str(Path(__file__).resolve().parent))

import copy
import json
import random
import unittest

from _script_loader import load_inject_docx
from conftest import (
    DEFAULT_EXAMPLES, DEFAULT_SEED, FIXTURES_DIR,
    ENUM_SOURCE, ENUM_CATEGORY, ENUM_SEVERITY, ENUM_SCOPE,
)

ID = load_inject_docx()
validate = ID.validate_issues_json

# 读合法夹具作为基准
VALID = json.loads((FIXTURES_DIR / "issues_valid.json").read_text(encoding="utf-8"))


def random_valid_issue(rng: random.Random, idx: int) -> dict:
    """生成一条合法 issue。"""
    source = rng.choice(ENUM_SOURCE)
    category = rng.choice(ENUM_CATEGORY)
    severity = rng.choice(ENUM_SEVERITY)
    scope = rng.choice(ENUM_SCOPE)
    chapter = f"{rng.randint(1, 5)}.{rng.randint(1, 3)}.{rng.randint(1, 3)}"
    pidx = rng.randint(0, 100)
    excerpt = "" if scope in ("document", "chapter") else f"原文摘录 {idx}"[:50]

    return {
        "id": f"{source}-{category}-{idx:03d}",
        "source": source,
        "category": category,
        "severity": severity,
        "scope": scope,
        "locator": {"chapter": chapter, "paragraph_index": pidx},
        "excerpt": excerpt,
        "anchor_text": f"锚点 {idx}" if scope in ("document", "chapter") else excerpt[:20],
        "problem": f"随机生成问题 {idx}",
        "suggestion": [f"随机生成建议 {idx}"],
        "group_id": f"g-{idx:03d}",
    }


def assign_group_ids(issues: list[dict]) -> None:
    """按 rules/issues-schema.md § 4 的算法分配 group_id。"""
    key_to_gid: dict[tuple, str] = {}
    next_n = 1
    for it in issues:
        loc = it.get("locator", {})
        key = (it.get("source"), it.get("category"),
               loc.get("chapter"), loc.get("paragraph_index"))
        if key not in key_to_gid:
            key_to_gid[key] = f"g-{next_n:03d}"
            next_n += 1
        it["group_id"] = key_to_gid[key]


class TestP1ValidatorAcceptsValid(unittest.TestCase):
    """Property 1 正向：合法 issues.json 通过自校验。"""

    def test_valid_fixture_passes(self):
        errs = validate(VALID, input_is_pdf=False)
        self.assertEqual(errs, [], f"valid fixture should pass, got: {errs}")

    def test_random_valid_samples(self):
        """≥ 100 个随机合法样本都通过自校验。"""
        rng = random.Random(DEFAULT_SEED)
        for i in range(DEFAULT_EXAMPLES):
            issues = [random_valid_issue(rng, j) for j in range(rng.randint(1, 20))]
            # 确保 id 唯一
            seen = set()
            unique = []
            for it in issues:
                if it["id"] not in seen:
                    seen.add(it["id"])
                    unique.append(it)
            # 分配 group_id 保证一致
            assign_group_ids(unique)
            data = {"schema_version": "1.0", "issues": unique}
            errs = validate(data)
            self.assertEqual(errs, [], f"example {i} failed: {errs[:3]}")


class TestP1ValidatorRejectsInvalid(unittest.TestCase):
    """Property 1 反向：违规输入必返回非空错误。"""

    def _check_file(self, name: str, expected_keyword: str | None = None):
        data = json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))
        errs = validate(data)
        self.assertTrue(errs, f"{name} should have errors")
        if expected_keyword:
            blob = "\n".join(errs)
            self.assertIn(expected_keyword, blob,
                          f"expected {expected_keyword!r} in errors: {blob}")

    def test_invalid_id_pattern(self):
        self._check_file("issues_invalid_id_pattern.json", "pattern mismatch")

    def test_invalid_enum(self):
        self._check_file("issues_invalid_enum.json", "source")

    def test_invalid_duplicate_id(self):
        self._check_file("issues_invalid_duplicate_id.json", "duplicate")

    def test_invalid_length(self):
        self._check_file("issues_invalid_length.json")

    def test_invalid_scope_excerpt(self):
        self._check_file("issues_invalid_scope_excerpt.json", "scope")

    def test_invalid_table_incomplete(self):
        self._check_file("issues_invalid_table_incomplete.json", "table")

    def test_invalid_group_id(self):
        self._check_file("issues_invalid_group_id.json", "group_id")


class TestP2JsonRoundtrip(unittest.TestCase):
    """Property 2：通过自校验的数据 → json.dumps → json.loads → 再次自校验仍通过。"""

    def test_valid_roundtrip(self):
        rng = random.Random(DEFAULT_SEED + 1)
        for i in range(DEFAULT_EXAMPLES):
            issues = [random_valid_issue(rng, j) for j in range(rng.randint(1, 10))]
            seen = set()
            unique = [it for it in issues if it["id"] not in seen and not seen.add(it["id"])]
            assign_group_ids(unique)
            data = {"schema_version": "1.0", "issues": unique}

            # roundtrip
            serialized = json.dumps(data, ensure_ascii=False)
            data2 = json.loads(serialized)
            self.assertEqual(data, data2, f"example {i}: roundtrip mismatch")
            errs = validate(data2)
            self.assertEqual(errs, [], f"example {i}: re-validation failed: {errs[:3]}")


class TestP3ScopeExcerptDependency(unittest.TestCase):
    """Property 3：scope ∈ {document, chapter} → excerpt 必须为空字符串。"""

    def test_document_scope_requires_empty_excerpt(self):
        rng = random.Random(DEFAULT_SEED + 2)
        for i in range(DEFAULT_EXAMPLES):
            it = random_valid_issue(rng, i)
            it["scope"] = "document"
            it["excerpt"] = ""
            data = {"schema_version": "1.0", "issues": [it]}
            self.assertEqual(validate(data), [], f"example {i}: valid doc scope failed")

            # 反向：放入非空 excerpt 应失败
            it["excerpt"] = "不该有的内容"
            data = {"schema_version": "1.0", "issues": [it]}
            errs = validate(data)
            self.assertTrue(errs, f"example {i}: non-empty excerpt for scope=document should fail")

    def test_chapter_scope_requires_empty_excerpt(self):
        rng = random.Random(DEFAULT_SEED + 3)
        for i in range(DEFAULT_EXAMPLES):
            it = random_valid_issue(rng, i)
            it["scope"] = "chapter"
            it["excerpt"] = ""
            data = {"schema_version": "1.0", "issues": [it]}
            self.assertEqual(validate(data), [], f"example {i}: valid chapter scope failed")


class TestP4GroupIdConsistency(unittest.TestCase):
    """Property 4：同四元组 issues 共享 group_id；不同四元组分配不同 group_id。"""

    def test_same_key_shares_group_id(self):
        rng = random.Random(DEFAULT_SEED + 4)
        for i in range(DEFAULT_EXAMPLES):
            # 构造两条"四元组相同"的 issues
            base = random_valid_issue(rng, i * 2)
            clone = copy.deepcopy(base)
            clone["id"] = base["id"].replace(f"-{(i * 2):03d}", f"-{(i * 2 + 1):03d}")
            clone["severity"] = rng.choice(ENUM_SEVERITY)  # severity 不参与四元组
            clone["scope"] = rng.choice(ENUM_SCOPE)
            if clone["scope"] in ("document", "chapter"):
                clone["excerpt"] = ""
            # 四元组：source / category / chapter / paragraph_index 相同
            clone["locator"] = copy.deepcopy(base["locator"])
            # 重要：group_id 必须一致
            clone["group_id"] = base["group_id"]

            data = {"schema_version": "1.0", "issues": [base, clone]}
            errs = validate(data)
            self.assertEqual(errs, [], f"example {i}: same-key consistent group_id failed: {errs[:3]}")

    def test_different_key_requires_different_group_id(self):
        """反向：同一 group_id 下出现两种不同的四元组 → 应失败。"""
        rng = random.Random(DEFAULT_SEED + 5)
        for i in range(DEFAULT_EXAMPLES):
            a = random_valid_issue(rng, i * 2)
            b = random_valid_issue(rng, i * 2 + 1)
            # 让 b 的四元组与 a 不同（只要 source/category/chapter/paragraph_index 至少一项不同）
            # 强制设置 paragraph_index 不同
            b["locator"]["paragraph_index"] = a["locator"]["paragraph_index"] + 1
            # 但给相同 group_id
            b["group_id"] = a["group_id"]

            data = {"schema_version": "1.0", "issues": [a, b]}
            errs = validate(data)
            self.assertTrue(errs, f"example {i}: group_id reuse should fail")


if __name__ == "__main__":
    unittest.main()
