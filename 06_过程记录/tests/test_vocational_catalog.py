import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "vocational_undergraduate_mapping"
CATALOG = ROOT / "catalogs" / "vocational_effective_2026.json"
CLASS_SKILLS = ROOT / "catalogs" / "vocational_class_skills.json"
UNDERGRADUATE = ROOT.parent / "discipline_mapping" / "catalogs" / "undergraduate_2026.json"


class VocationalCatalogTests(unittest.TestCase):
    def test_effective_catalog_has_every_current_high_vocational_major(self) -> None:
        payload = json.loads(CATALOG.read_text("utf-8"))
        rows = payload["records"]

        self.assertEqual(len(rows), 811)
        self.assertEqual(len({x["category_code"] for x in rows}), 19)
        self.assertEqual(len({x["class_code"] for x in rows}), 97)
        self.assertEqual(len({x["major_code"] for x in rows}), 811)
        self.assertTrue(all(re.fullmatch(r"[45]\d{5}K?", x["major_code"]) for x in rows))
        self.assertEqual(sum(x["major_code"].endswith("K") for x in rows), 49)
        self.assertEqual(payload["exceptions"], [])

        names_2026 = {
            "储能材料装备智能运维技术",
            "海洋智能机器人应用技术",
            "高原铁路智能建造与运维",
            "智能体通信技术",
            "车联网通信技术",
            "旅居康养运营与管理",
            "剧装戏具设计与制作",
            "婴幼儿家庭养育与指导",
            "老年教育服务与管理",
        }
        new_rows = [x for x in rows if x["enrollment_effective"] == "2027"]
        self.assertEqual({x["major_name"] for x in new_rows}, names_2026)
        self.assertEqual(
            {x["source_ids"][-1] for x in new_rows}, {"vocational_2026_release"}
        )

    def test_existing_undergraduate_catalog_remains_the_only_undergraduate_source(self) -> None:
        rows = json.loads(UNDERGRADUATE.read_text("utf-8"))["records"]
        self.assertEqual(len(rows), 883)
        self.assertEqual(len({x["category_code"] for x in rows}), 13)
        self.assertEqual(len({x["class_code"] for x in rows if x["class_code"]}), 92)
        self.assertEqual(len({x["major_code"] for x in rows}), 883)

    def test_input_professional_classes_reconcile_to_official_catalog(self) -> None:
        vocational = json.loads(CATALOG.read_text("utf-8"))["records"]
        class_skills = json.loads(CLASS_SKILLS.read_text("utf-8"))["classes"]
        official = {row["class_code"]: row["class_name"] for row in vocational}
        auxiliary = {row["class_code"]: row["class_name"] for row in class_skills}
        self.assertEqual(auxiliary, official)


if __name__ == "__main__":
    unittest.main()
