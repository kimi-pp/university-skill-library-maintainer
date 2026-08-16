import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1] / "discipline_mapping"
manifest = json.loads((ROOT / "source_manifest.json").read_text("utf-8"))
required = {
    "undergraduate_2026_pdf",
    "graduate_2022_pdf",
    "graduate_2025_correspondence",
}
by_id = {row["id"]: row for row in manifest["sources"]}

assert required <= set(by_id)
assert len(by_id) == len(manifest["sources"])

for row in manifest["sources"]:
    assert urlparse(row["url"]).hostname.endswith("moe.gov.cn")
    target = ROOT / row["local_path"]
    assert target.is_file() and target.stat().st_size > 1000
    assert hashlib.sha256(target.read_bytes()).hexdigest() == row["sha256"]
    assert row["accessed_at"] == "2026-08-16"
