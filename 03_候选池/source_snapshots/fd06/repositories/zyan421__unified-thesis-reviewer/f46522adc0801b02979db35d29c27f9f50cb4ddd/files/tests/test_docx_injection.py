"""Property 5–9 测试：docx 批注注入。

- P5: 合法 docx + 合法 issues → .annotated.docx 所有核心 XML part 可解析
- P6: 三元计数等式 commentRangeStart=commentRangeEnd, w:comment=w:commentReference
- P7: 白名单 part 的 SHA256 保持不变
- P8: run 拆分前后段内字符序列不变
- P9: 排序稳定性 + 500 条上限 + id 唯一性

Feature: unified-thesis-reviewer
"""
from __future__ import annotations

import sys
from pathlib import Path

# 把 tests/ 目录加入 sys.path 以便 import 本目录下的辅助模块
sys.path.insert(0, str(Path(__file__).resolve().parent))

import copy
import hashlib
import json
import random
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

from _script_loader import load_inject_docx
from conftest import DEFAULT_EXAMPLES, DEFAULT_SEED, FIXTURES_DIR
from test_issues_json import random_valid_issue, assign_group_ids

ID = load_inject_docx()

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WHITELIST_PARTS = [
    "word/styles.xml",
    "word/_rels/.rels",
    "docProps/core.xml",
]


def sha256_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_issues_for_minimal_docx(rng: random.Random, count: int) -> dict:
    """构造与 minimal.docx 兼容的 issues（paragraph_index 在 0-16 范围）。"""
    issues = []
    categories = ["structure", "argumentation", "language", "policy"]
    severities = ["fatal", "major", "minor"]
    group_map = {}
    next_gid = 1
    for i in range(count):
        sev = rng.choice(severities)
        cat = rng.choice(categories)
        chapter = f"{rng.randint(1, 5)}.{rng.randint(1, 3)}"
        pidx = rng.randint(0, 16)
        key = ("thesis", cat, chapter, pidx)
        if key not in group_map:
            group_map[key] = f"g-{next_gid:03d}"
            next_gid += 1
        issues.append({
            "id": f"thesis-{cat}-{i:03d}",
            "source": "thesis",
            "category": cat,
            "severity": sev,
            "scope": "paragraph",
            "locator": {"chapter": chapter, "paragraph_index": pidx},
            "excerpt": f"片段 {i}",
            "anchor_text": f"片段 {i}",
            "problem": f"问题 {i}",
            "suggestion": [f"建议 {i}"],
            "group_id": group_map[key],
        })
    return {"schema_version": "1.0", "issues": issues}


class DocxBaseTest(unittest.TestCase):
    """所有 docx 测试的基类：确保 fixtures 存在。"""

    @classmethod
    def setUpClass(cls):
        from fixtures.build_minimal_docx import build
        cls.src_docx = build()


class TestP5OoxmlParseable(DocxBaseTest):
    """Property 5：.annotated.docx 所有核心 XML part 可被 ET 解析。"""

    def test_parseable_with_random_issues(self):
        rng = random.Random(DEFAULT_SEED + 10)
        required = [
            "[Content_Types].xml",
            "word/document.xml",
            "word/comments.xml",
            "word/commentsExtended.xml",
            "word/commentsIds.xml",
            "word/_rels/document.xml.rels",
        ]
        examples = DEFAULT_EXAMPLES // 10  # 每个 example 都生成完整 docx，减少到 10 次
        with tempfile.TemporaryDirectory() as td:
            for i in range(examples):
                issues = make_issues_for_minimal_docx(rng, rng.randint(1, 20))
                issues_path = Path(td) / f"issues_{i}.json"
                dst = Path(td) / f"out_{i}.annotated.docx"
                issues_path.write_text(
                    json.dumps(issues, ensure_ascii=False), encoding="utf-8")
                count, _ = ID.inject(self.src_docx, issues_path, dst)
                self.assertGreater(count, 0, f"example {i}: no comments mounted")

                with zipfile.ZipFile(dst) as z:
                    for p in required:
                        try:
                            ET.fromstring(z.read(p))
                        except ET.ParseError as e:
                            self.fail(f"example {i}, part {p}: parse failed: {e}")


class TestP6CommentTripleCounts(DocxBaseTest):
    """Property 6：commentRangeStart=commentRangeEnd, w:comment=w:commentReference。"""

    def test_counts_match(self):
        rng = random.Random(DEFAULT_SEED + 11)
        examples = DEFAULT_EXAMPLES // 10
        with tempfile.TemporaryDirectory() as td:
            for i in range(examples):
                issues = make_issues_for_minimal_docx(rng, rng.randint(1, 30))
                issues_path = Path(td) / f"issues_{i}.json"
                dst = Path(td) / f"out_{i}.annotated.docx"
                issues_path.write_text(
                    json.dumps(issues, ensure_ascii=False), encoding="utf-8")
                count, _ = ID.inject(self.src_docx, issues_path, dst)

                with zipfile.ZipFile(dst) as z:
                    doc = ET.fromstring(z.read("word/document.xml"))
                    cm = ET.fromstring(z.read("word/comments.xml"))
                    n_start = len(doc.findall(f".//{W_NS}commentRangeStart"))
                    n_end = len(doc.findall(f".//{W_NS}commentRangeEnd"))
                    n_comment = len(cm.findall(f".//{W_NS}comment"))
                    n_ref = len(doc.findall(f".//{W_NS}commentReference"))

                    self.assertEqual(n_start, n_end,
                                     f"example {i}: start {n_start} != end {n_end}")
                    self.assertEqual(n_comment, n_ref,
                                     f"example {i}: comment {n_comment} != ref {n_ref}")
                    self.assertEqual(n_comment, count,
                                     f"example {i}: comment count != mounted")


class TestP7WhitelistPartsPreserved(DocxBaseTest):
    """Property 7：白名单 part（styles.xml、_rels/.rels、docProps/core.xml）SHA256 不变。"""

    def test_whitelist_parts_unchanged(self):
        rng = random.Random(DEFAULT_SEED + 12)

        # 先算原 docx 中白名单 part 的 SHA256
        with zipfile.ZipFile(self.src_docx) as z:
            src_hashes = {p: sha256_of(z.read(p)) for p in WHITELIST_PARTS
                          if p in z.namelist()}

        examples = DEFAULT_EXAMPLES // 10
        with tempfile.TemporaryDirectory() as td:
            for i in range(examples):
                issues = make_issues_for_minimal_docx(rng, rng.randint(1, 15))
                issues_path = Path(td) / f"issues_{i}.json"
                dst = Path(td) / f"out_{i}.annotated.docx"
                issues_path.write_text(
                    json.dumps(issues, ensure_ascii=False), encoding="utf-8")
                ID.inject(self.src_docx, issues_path, dst)

                with zipfile.ZipFile(dst) as z:
                    for p, src_hash in src_hashes.items():
                        dst_hash = sha256_of(z.read(p))
                        self.assertEqual(
                            dst_hash, src_hash,
                            f"example {i}, part {p}: hash differs "
                            f"(src={src_hash[:8]} dst={dst_hash[:8]})"
                        )


class TestP8RunSplitPreservesCharSequence(DocxBaseTest):
    """Property 8：run 拆分前后段内字符序列不变。"""

    def test_char_sequence_preserved(self):
        """对 minimal.docx 的每个段落尝试不同 char_offset 拆分，验证字符序列不变。"""
        with zipfile.ZipFile(self.src_docx) as z:
            doc_bytes = z.read("word/document.xml")
        root = ET.fromstring(doc_bytes)
        body = root.find(f"{W_NS}body")
        paragraphs = [p for p in body if p.tag == f"{W_NS}p"]

        examples_tested = 0
        rng = random.Random(DEFAULT_SEED + 14)
        for para in paragraphs:
            # 深拷贝，避免后续迭代被影响
            # 固定 + 随机 offset 组合，确保 ≥ DEFAULT_EXAMPLES
            offsets = [0, 1, 2, 3, 5, 10] + [rng.randint(0, 30) for _ in range(10)]
            for offset in offsets:
                p_copy = copy.deepcopy(para)
                original_chars = "".join(c[0] for c in ID.flatten_runs(p_copy))
                ID.split_run_at(p_copy, offset)
                after_chars = "".join(c[0] for c in ID.flatten_runs(p_copy))
                self.assertEqual(
                    original_chars, after_chars,
                    f"offset {offset}: chars changed "
                    f"{original_chars!r} -> {after_chars!r}"
                )
                examples_tested += 1

        self.assertGreaterEqual(examples_tested, DEFAULT_EXAMPLES,
                                f"only {examples_tested} examples; need >= {DEFAULT_EXAMPLES}")


class TestP9IdUniquenessCapAndSortStability(unittest.TestCase):
    """Property 9：排序稳定性 + 500 条上限 + id 唯一性。"""

    def test_sort_stability_and_cap(self):
        # 使用 600 条夹具
        data = json.loads((FIXTURES_DIR / "issues_boundary_600.json").read_text("utf-8"))
        # 第一次
        selected1, overflowed1 = ID.select_top_n(data["issues"])
        # 第二次
        selected2, overflowed2 = ID.select_top_n(data["issues"])
        # 稳定性：两次结果完全一致
        self.assertEqual([i["id"] for i in selected1], [i["id"] for i in selected2])
        self.assertEqual([i["id"] for i in overflowed1], [i["id"] for i in overflowed2])
        # 上限
        self.assertEqual(len(selected1), 500)
        self.assertEqual(len(overflowed1), 100)
        # 顺序正确：首条 severity 必为 fatal
        self.assertEqual(selected1[0]["severity"], "fatal")

    def test_id_uniqueness_in_output(self):
        """注入后 w:comment 的 id 属性全清单唯一。"""
        from fixtures.build_minimal_docx import build
        src = build()
        rng = random.Random(DEFAULT_SEED + 13)
        issues = make_issues_for_minimal_docx(rng, 50)
        with tempfile.TemporaryDirectory() as td:
            issues_path = Path(td) / "issues.json"
            dst = Path(td) / "out.annotated.docx"
            issues_path.write_text(json.dumps(issues, ensure_ascii=False), encoding="utf-8")
            ID.inject(src, issues_path, dst)

            with zipfile.ZipFile(dst) as z:
                cm = ET.fromstring(z.read("word/comments.xml"))
                ids = [c.get(f"{W_NS}id") for c in cm.findall(f".//{W_NS}comment")]
                self.assertEqual(len(ids), len(set(ids)),
                                 f"duplicate w:id in w:comment: {ids}")


if __name__ == "__main__":
    unittest.main()
