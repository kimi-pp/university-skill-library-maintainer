"""Property 10–11 测试：XFDF 生成。

- P10: 生成的 .xfdf 可解析 + annotation 数量匹配 + coords 8 倍数 + page 0-based + name 唯一
- P11: bbox 越界时 clip，不 skip；clip 后 coords 不超页面边界

Feature: unified-thesis-reviewer
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import json
import random
import tempfile
import unittest
import xml.etree.ElementTree as ET

from _script_loader import load_generate_xfdf
from conftest import DEFAULT_EXAMPLES, DEFAULT_SEED, FIXTURES_DIR

XF = load_generate_xfdf()

XFDF_NS = "{http://ns.adobe.com/xfdf/}"

COLOR_EXPECTED = {"fatal": "#E74C3C", "major": "#F39C12", "minor": "#F1C40F"}


def make_pdf_issues(rng: random.Random, count: int, *, with_bbox: bool = True) -> dict:
    """构造适配 minimal.pdf 的 pdf 模式 issues。"""
    issues = []
    categories = ["structure", "argumentation", "language"]
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

        loc = {
            "chapter": chapter,
            "paragraph_index": pidx,
            "page_number": rng.choice([1, 2]),
        }
        if with_bbox:
            # 在 US Letter (612×792) 范围内随机
            x0 = rng.randint(20, 500)
            y0 = rng.randint(100, 700)
            loc["bbox"] = [x0, y0, x0 + rng.randint(20, 100), y0 + rng.randint(10, 20)]

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


class PdfBaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from fixtures.build_minimal_pdf import build
        cls.src_pdf = build()


class TestP10XfdfParseableAndComplete(PdfBaseTest):
    """Property 10：XFDF 可解析、计数匹配、coords 8 倍数、page 0-based、name 唯一。"""

    def test_bulk_generation_invariants(self):
        rng = random.Random(DEFAULT_SEED + 20)
        examples = DEFAULT_EXAMPLES // 10
        with tempfile.TemporaryDirectory() as td:
            for i in range(examples):
                issues = make_pdf_issues(rng, rng.randint(1, 20), with_bbox=True)
                ij = Path(td) / f"i_{i}.json"
                xf = Path(td) / f"o_{i}.xfdf"
                ij.write_text(json.dumps(issues, ensure_ascii=False), encoding="utf-8")
                count, _ = XF.generate(self.src_pdf, ij, xf)
                self.assertEqual(count, len(issues["issues"]),
                                 f"example {i}: mounted count mismatch")

                tree = ET.parse(xf)
                root = tree.getroot()
                annots = root.find(f"{XFDF_NS}annots")
                self.assertIsNotNone(annots, f"example {i}: missing <annots>")

                highlights = annots.findall(f"{XFDF_NS}highlight")
                texts = annots.findall(f"{XFDF_NS}text")
                self.assertEqual(
                    len(highlights) + len(texts), count,
                    f"example {i}: element count mismatch"
                )

                # coords 长度为 8 的倍数
                for h in highlights:
                    coords = [float(x) for x in h.get("coords", "").split(",")]
                    self.assertEqual(len(coords) % 8, 0,
                                     f"example {i}: coords not multiple of 8: {len(coords)}")

                # page 0-based 非负整数
                for el in list(highlights) + list(texts):
                    page = int(el.get("page"))
                    self.assertGreaterEqual(page, 0, f"example {i}: page {page} < 0")

                # name 唯一
                names = [el.get("name") for el in list(highlights) + list(texts)]
                self.assertEqual(len(names), len(set(names)),
                                 f"example {i}: duplicate names")

                # color 按 severity 映射
                id_to_sev = {it["id"]: it["severity"] for it in issues["issues"]}
                for el in list(highlights) + list(texts):
                    expected = COLOR_EXPECTED[id_to_sev[el.get("name")]]
                    self.assertEqual(el.get("color"), expected,
                                     f"example {i}: wrong color for {el.get('name')}")

                # Foxit: date == creationdate
                for el in list(highlights) + list(texts):
                    self.assertEqual(el.get("date"), el.get("creationdate"))
                    self.assertNotIn("subject", el.attrib)

    def test_determinism(self):
        """同一 issues.json 生成两次，XFDF 除 date 外内容一致。"""
        import re as re_mod
        rng = random.Random(DEFAULT_SEED + 21)
        issues = make_pdf_issues(rng, 15, with_bbox=True)
        with tempfile.TemporaryDirectory() as td:
            ij = Path(td) / "i.json"
            xf1 = Path(td) / "a.xfdf"
            xf2 = Path(td) / "b.xfdf"
            ij.write_text(json.dumps(issues, ensure_ascii=False), encoding="utf-8")
            XF.generate(self.src_pdf, ij, xf1)
            XF.generate(self.src_pdf, ij, xf2)

            def scrub(b):
                return re_mod.sub(rb'date="[^"]+"', b'date="T"', b)

            self.assertEqual(scrub(xf1.read_bytes()), scrub(xf2.read_bytes()))


class TestP11BboxClipping(PdfBaseTest):
    """Property 11：bbox 越界时 clip，不 skip；clip 后 coords 不超页面边界。"""

    def test_clip_keeps_annotation_and_clamps_coords(self):
        rng = random.Random(DEFAULT_SEED + 22)
        examples = DEFAULT_EXAMPLES

        # 每个 example 随机生成一个"越界程度不同"的 bbox
        page_w, page_h = 612, 792  # minimal.pdf 的 MediaBox
        with tempfile.TemporaryDirectory() as td:
            for i in range(examples):
                # 随机在越界程度不同的档位选择
                extreme = rng.randint(0, 3)
                if extreme == 0:
                    bbox = [-10, -20, 700, 800]  # 四边都越界
                elif extreme == 1:
                    bbox = [100, 100, 10000, 200]  # 右越界
                elif extreme == 2:
                    bbox = [100, -500, 200, 200]  # 下越界
                else:
                    bbox = [100, 100, 200, 10000]  # 上越界

                issues = {
                    "schema_version": "1.0",
                    "issues": [{
                        "id": f"thesis-language-{i:03d}",
                        "source": "thesis",
                        "category": "language",
                        "severity": "minor",
                        "scope": "paragraph",
                        "locator": {
                            "chapter": "1",
                            "paragraph_index": 0,
                            "page_number": 1,
                            "bbox": bbox,
                        },
                        "excerpt": "片段",
                        "anchor_text": "片段",
                        "problem": "越界测试",
                        "suggestion": ["验证 clip"],
                        "group_id": "g-001",
                    }]
                }
                ij = Path(td) / f"i_{i}.json"
                xf = Path(td) / f"o_{i}.xfdf"
                ij.write_text(json.dumps(issues, ensure_ascii=False), encoding="utf-8")
                count, _ = XF.generate(self.src_pdf, ij, xf)
                self.assertEqual(count, 1, f"example {i}: annotation was skipped")

                # 验证 coords 都在页面内
                tree = ET.parse(xf)
                annots = tree.getroot().find(f"{XFDF_NS}annots")
                for h in annots.findall(f"{XFDF_NS}highlight"):
                    coords = [float(x) for x in h.get("coords", "").split(",")]
                    for k in range(0, len(coords), 2):
                        x, y = coords[k], coords[k + 1]
                        self.assertGreaterEqual(x, 0, f"example {i}: x={x} < 0")
                        self.assertLessEqual(x, page_w, f"example {i}: x={x} > {page_w}")
                        self.assertGreaterEqual(y, 0, f"example {i}: y={y} < 0")
                        self.assertLessEqual(y, page_h, f"example {i}: y={y} > {page_h}")


if __name__ == "__main__":
    unittest.main()
