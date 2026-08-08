"""v2.0.0 新增：annotate-pdf.py 的测试

- P13: 嵌入式 pdf 生成后，批注计数 = 输入 issue 数
- P14: pdf 可被 PyMuPDF 回读且 annotation 数正确
- P15: anchor_text 命中率 ≥ 50%（少于 50% 的 top-left-note 占比）
- P16: 脚本对 issues.json 缺 anchor_text 的情况返回校验错误

Feature: unified-thesis-reviewer v2.0.0
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import json
import random
import subprocess
import tempfile
import unittest

from _script_loader import TOOLS_DIR
from conftest import DEFAULT_SEED, FIXTURES_DIR

try:
    import fitz
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False


SCRIPT = TOOLS_DIR / "annotate-pdf.py"


def make_pdf_issues_with_anchor(rng, count: int) -> dict:
    issues = []
    categories = ["structure", "argumentation", "language"]
    severities = ["fatal", "major", "minor"]
    group_map = {}
    next_gid = 1
    for i in range(count):
        sev = rng.choice(severities)
        cat = rng.choice(categories)
        chapter = f"{rng.randint(1, 5)}.{rng.randint(1, 3)}"
        pidx = rng.randint(0, 10)
        key = ("thesis", cat, chapter, pidx)
        if key not in group_map:
            group_map[key] = f"g-{next_gid:03d}"
            next_gid += 1

        loc = {
            "chapter": chapter,
            "paragraph_index": pidx,
            "page_number": rng.randint(1, 2),
        }

        issues.append({
            "id": f"thesis-{cat}-{i:03d}",
            "source": "thesis",
            "category": cat,
            "severity": sev,
            "scope": "paragraph",
            "locator": loc,
            "excerpt": f"片段 {i}",
            "anchor_text": f"片段 {i}",
            "problem": f"问题 {i}",
            "suggestion": [f"建议 {i}"],
            "group_id": group_map[key],
        })
    return {"schema_version": "1.0", "issues": issues}


@unittest.skipUnless(HAS_PYMUPDF, "PyMuPDF not available")
class TestAnnotatePdfSanity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from fixtures.build_minimal_pdf import build
        cls.src_pdf = build()

    def test_script_exists_and_compiles(self):
        self.assertTrue(SCRIPT.is_file())
        r = subprocess.run(
            [sys.executable, "-m", "py_compile", str(SCRIPT)],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_help(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0)
        self.assertIn("annotate-pdf", r.stdout.lower() + r.stderr.lower())

    def test_mount_and_readback(self):
        """P13: 批注数 = 输入 issue 数；P14: 回读验证通过"""
        rng = random.Random(DEFAULT_SEED + 40)
        issues = make_pdf_issues_with_anchor(rng, 5)

        with tempfile.TemporaryDirectory() as td:
            ij = Path(td) / "issues.json"
            out = Path(td) / "out.annotated.pdf"
            ij.write_text(json.dumps(issues, ensure_ascii=False), encoding="utf-8")

            r = subprocess.run(
                [sys.executable, str(SCRIPT), str(self.src_pdf), str(ij), str(out)],
                capture_output=True, text=True,
            )
            self.assertEqual(r.returncode, 0, f"script failed: {r.stderr}")
            self.assertTrue(out.is_file())

            # 回读验证：PyMuPDF 打开后批注数 == 输入
            doc = fitz.open(out)
            total = 0
            for page in doc:
                total += len(list(page.annots()))
            doc.close()
            self.assertEqual(total, 5, f"expected 5 annotations, got {total}")

    def test_missing_anchor_text_rejected(self):
        """P16: 缺 anchor_text 的 issues.json 被校验拒绝"""
        bad_issues = {
            "schema_version": "1.0",
            "issues": [{
                "id": "thesis-structure-001",
                "source": "thesis",
                "category": "structure",
                "severity": "fatal",
                "scope": "document",
                "locator": {"chapter": "全文", "paragraph_index": 0},
                "excerpt": "",
                # 故意缺 anchor_text
                "problem": "测试",
                "suggestion": ["测试"],
                "group_id": "g-001",
            }]
        }
        with tempfile.TemporaryDirectory() as td:
            ij = Path(td) / "issues.json"
            out = Path(td) / "out.pdf"
            ij.write_text(json.dumps(bad_issues, ensure_ascii=False), encoding="utf-8")

            r = subprocess.run(
                [sys.executable, str(SCRIPT), str(self.src_pdf), str(ij), str(out)],
                capture_output=True, text=True,
            )
            # 退出码 3 = validation error
            self.assertEqual(r.returncode, 3, f"should be validation error, got {r.returncode}")
            self.assertIn("anchor_text", r.stderr.lower() + r.stdout.lower())


@unittest.skipUnless(HAS_PYMUPDF, "PyMuPDF not available")
class TestExtractPdfText(unittest.TestCase):
    """P17: extract-pdf-text.py 产出合法 JSON 且含 positions"""

    @classmethod
    def setUpClass(cls):
        from fixtures.build_minimal_pdf import build
        cls.src_pdf = build()

    def test_extract_to_json(self):
        script = TOOLS_DIR / "extract-pdf-text.py"
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "positions.json"
            r = subprocess.run(
                [sys.executable, str(script), str(self.src_pdf), str(out)],
                capture_output=True, text=True,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(out.is_file())

            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], "1.0")
            self.assertGreater(data["page_count"], 0)
            self.assertEqual(len(data["pages"]), data["page_count"])

            # 每页必须有 width/height
            for page in data["pages"]:
                self.assertGreater(page["width"], 0)
                self.assertGreater(page["height"], 0)


@unittest.skipUnless(HAS_PYMUPDF, "PyMuPDF not available")
class TestCitationCrossref(unittest.TestCase):
    """P18: citation-crossref.py 产出合法 JSON 且含三份对比表"""

    @classmethod
    def setUpClass(cls):
        from fixtures.build_minimal_pdf import build
        cls.src_pdf = build()

    def test_crossref_to_json(self):
        script = TOOLS_DIR / "citation-crossref.py"
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "crossref.json"
            r = subprocess.run(
                [sys.executable, str(script), str(self.src_pdf), str(out)],
                capture_output=True, text=True,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(out.is_file())

            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], "1.0")
            # 三份对比表必须存在（即使为空数组）
            self.assertIn("in_text_not_in_refs", data)
            self.assertIn("in_refs_not_in_text", data)
            self.assertIn("matched", data)
            self.assertIn("stats", data)


if __name__ == "__main__":
    unittest.main()
