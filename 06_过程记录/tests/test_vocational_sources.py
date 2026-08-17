import hashlib
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1] / "vocational_undergraduate_mapping"


class VocationalSourceTests(unittest.TestCase):
    def test_official_snapshots_and_external_input_are_hash_locked(self) -> None:
        manifest = json.loads((ROOT / "source_manifest.json").read_text("utf-8-sig"))
        required = {
            "vocational_2021_base",
            "vocational_2025_supplement",
            "vocational_effective_2026_07",
        }
        by_id = {row["id"]: row for row in manifest["sources"]}

        self.assertTrue(required <= set(by_id))
        self.assertEqual(len(by_id), len(manifest["sources"]))
        self.assertEqual(manifest["accessed_at"], "2026-08-17")

        for row in manifest["sources"]:
            source_id = row["id"]
            host = urlparse(row["url"]).hostname or ""
            self.assertTrue(host == "moe.gov.cn" or host.endswith(".moe.gov.cn"))
            target = ROOT / row["local_path"]
            self.assertTrue(target.is_file(), source_id)
            self.assertGreater(target.stat().st_size, 1000, source_id)
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            self.assertEqual(digest, row["sha256"], source_id)
            self.assertEqual(target.stat().st_size, row["size_bytes"], source_id)

        input_row = json.loads((ROOT / "input_manifest.json").read_text("utf-8-sig"))
        input_path = Path(input_row["absolute_path"])
        self.assertEqual(input_path.name, "高职高专Skills领域分类表.xlsx")
        self.assertTrue(input_path.is_file())
        self.assertEqual(
            hashlib.sha256(input_path.read_bytes()).hexdigest(), input_row["sha256"]
        )
        self.assertEqual(input_row["accessed_at"], "2026-08-17")
        self.assertEqual(
            input_row["sheets"],
            {
                "Skills领域分类总表": "A1:E61",
                "领域分类-专业反向索引": "A1:F15",
                "专业大类-领域分类矩阵": "A1:R20",
                "专业类-领域分类明细": "A1:F389",
            },
        )


if __name__ == "__main__":
    unittest.main()
