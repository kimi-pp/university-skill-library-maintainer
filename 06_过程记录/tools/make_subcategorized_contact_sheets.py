"""Validate Task 7 inputs, inventory original renders, and build navigation sheets."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "subcategory_manifest.json"
CATALOG_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "plain_language_catalog.json"
DELIVERY_ROOT = PROJECT_ROOT / "05_交付物" / "通俗细分版_2026-08-07"
DOCX_RENDER_ROOT = PROJECT_ROOT / "06_过程记录" / "renders" / "subcategorized_docx"
XLSX_RENDER_ROOT = PROJECT_ROOT / "06_过程记录" / "renders" / "subcategorized_xlsx"
CONTACT_ROOT = PROJECT_ROOT / "06_过程记录" / "renders" / "subcategorized_contact_sheets"
INVENTORY_FILE = CONTACT_ROOT / "visual_review_inventory.json"
DOCX_RENDER_MANIFEST_NAME = "rendered-pages.json"

WORKSHEET_RENDER_NAMES = (
    "1_使用说明.png",
    "2_AI技能清单.png",
    "3_分类统计.png",
    "4_来源清单.png",
)
SEGMENT_LABELS = ("title-header", "longest-text", "longest-url", "last-row")


def _safe_resolve(root: Path, relative: str) -> Path:
    root = root.resolve()
    candidate = (root / Path(relative)).resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"不安全的 manifest 路径: {relative}")
    return candidate


def validate_delivery_tree(project_root: Path, manifest: list[dict]) -> list[Path]:
    """Require the delivery tree to contain exactly the non-empty manifest files."""
    root = project_root.resolve()
    expected: set[Path] = set()
    for item in manifest:
        if item.get("format") not in {"docx", "xlsx"}:
            raise ValueError(f"manifest 存在非目标格式: {item}")
        path = _safe_resolve(root, item["path"])
        if path in expected:
            raise ValueError(f"manifest 重复路径: {item['path']}")
        expected.add(path)
    if not expected:
        raise ValueError("manifest 为空")

    delivery_root = root / "05_交付物" / "通俗细分版_2026-08-07"
    actual = {path.resolve() for path in delivery_root.rglob("*") if path.is_file()}
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise ValueError(f"交付文件缺失: {[path.name for path in missing]}")
    if extra:
        raise ValueError(f"发现额外或非 manifest 文件: {[path.name for path in extra]}")
    empty = sorted(path for path in expected if path.stat().st_size == 0)
    if empty:
        raise ValueError(f"交付中存在空文件: {[path.name for path in empty]}")
    return sorted(expected)


def _validate_png(path: Path) -> tuple[int, int]:
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"渲染图缺失或为空: {path}")
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            width, height = image.size
    except Exception as exc:  # Pillow provides format-specific exception types.
        raise ValueError(f"渲染图无效: {path}") from exc
    if width < 1 or height < 1:
        raise ValueError(f"渲染尺寸无效: {path}")
    return width, height


def _page_number(path: Path) -> int:
    try:
        return int(path.stem.rsplit("-", 1)[1])
    except (IndexError, ValueError) as exc:
        raise ValueError(f"无法解析页码: {path.name}") from exc


def _item_key(item: dict) -> str:
    if item.get("key"):
        return str(item["key"])
    if item.get("scope") == "overview" and item.get("big_category_code"):
        return f"{item['big_category_code']}-overview"
    if item.get("scope") == "subcategory" and item.get("subcategory_code"):
        return str(item["subcategory_code"])
    raise ValueError(f"无法从 manifest 推导渲染键: {item}")


def collect_docx_render_inventory(render_root: Path, manifest: list[dict]) -> list[dict]:
    """Inventory every canonical DOCX page and reject gaps or stale original pages."""
    root = render_root.resolve()
    inventory: list[dict] = []
    items = [item for item in manifest if item.get("format") == "docx"]
    expected_keys = {_item_key(item) for item in items}
    actual_keys = {path.name for path in root.iterdir() if path.is_dir()} if root.exists() else set()
    unexpected = sorted(actual_keys - expected_keys)
    if unexpected:
        raise ValueError(f"DOCX 渲染目录存在非 manifest 项: {unexpected}")
    for item in items:
        key = _item_key(item)
        directory = root / key
        pages = sorted(directory.glob("page-*.png"), key=_page_number)
        render_manifest_path = directory / DOCX_RENDER_MANIFEST_NAME
        if not render_manifest_path.is_file():
            raise ValueError(f"{key}: 缺少 DOCX 渲染预期集合")
        try:
            render_manifest = json.loads(render_manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"{key}: DOCX 渲染预期集合无效") from exc
        expected_names = render_manifest.get("pages") if isinstance(render_manifest, dict) else None
        if (
            not isinstance(expected_names, list)
            or not expected_names
            or any(not isinstance(name, str) for name in expected_names)
            or len(expected_names) != len(set(expected_names))
        ):
            raise ValueError(f"{key}: DOCX 渲染预期集合无效")
        actual_names = [path.name for path in pages]
        if actual_names != expected_names:
            raise ValueError(
                f"{key}: DOCX 页面与渲染预期集合不一致，可能存在残留 PNG: "
                f"expected={expected_names} actual={actual_names}"
            )
        numbers = [_page_number(path) for path in pages]
        if not pages:
            raise ValueError(f"{key}: 没有 DOCX 页面")
        if numbers != list(range(1, len(pages) + 1)):
            raise ValueError(f"{key}: DOCX 页码不连续: {numbers}")
        for path, page_number in zip(pages, numbers):
            width, height = _validate_png(path)
            inventory.append(
                {
                    "artifact_key": key,
                    "artifact_path": item["path"],
                    "render_kind": "docx_page",
                    "page_number": page_number,
                    "relative_path": path.relative_to(PROJECT_ROOT).as_posix()
                    if PROJECT_ROOT in path.parents
                    else path.as_posix(),
                    "width": width,
                    "height": height,
                    "review_status": "pending",
                }
            )
    return inventory


def collect_xlsx_render_inventory(
    render_root: Path,
    manifest: list[dict],
    *,
    required_segment_keys: set[str],
) -> list[dict]:
    """Inventory four full-sheet images per workbook plus required key-range segments."""
    root = render_root.resolve()
    inventory: list[dict] = []
    items = [item for item in manifest if item.get("format") == "xlsx"]
    expected_keys = {_item_key(item) for item in items}
    actual_keys = {path.name for path in root.iterdir() if path.is_dir()} if root.exists() else set()
    unexpected = sorted(actual_keys - expected_keys)
    if unexpected:
        raise ValueError(f"XLSX 渲染目录存在非 manifest 项: {unexpected}")
    for item in items:
        key = _item_key(item)
        directory = root / key
        for worksheet_number, file_name in enumerate(WORKSHEET_RENDER_NAMES, 1):
            path = directory / file_name
            width, height = _validate_png(path)
            inventory.append(
                {
                    "artifact_key": key,
                    "artifact_path": item["path"],
                    "render_kind": "worksheet",
                    "worksheet_number": worksheet_number,
                    "worksheet_name": file_name.split("_", 1)[1].removesuffix(".png"),
                    "relative_path": path.relative_to(PROJECT_ROOT).as_posix()
                    if PROJECT_ROOT in path.parents
                    else path.as_posix(),
                    "width": width,
                    "height": height,
                    "review_status": "pending",
                }
            )
        segment_paths = sorted(directory.glob("2_AI技能清单_segment_*.png"))
        if key in required_segment_keys:
            names = [path.name for path in segment_paths]
            for label in SEGMENT_LABELS:
                if not any(f"_segment_{label}_" in name for name in names):
                    raise ValueError(f"{key}: 缺少 {label} 高倍率分段图")
        for path in segment_paths:
            width, height = _validate_png(path)
            if width < 2400:
                raise ValueError(f"{key}: 高倍率分段图宽度不足: {path.name}")
            inventory.append(
                {
                    "artifact_key": key,
                    "artifact_path": item["path"],
                    "render_kind": "segment",
                    "worksheet_number": 2,
                    "worksheet_name": "AI技能清单",
                    "relative_path": path.relative_to(PROJECT_ROOT).as_posix()
                    if PROJECT_ROOT in path.parents
                    else path.as_posix(),
                    "width": width,
                    "height": height,
                    "review_status": "pending",
                }
            )
    return inventory


def _contact_sheet(paths: list[Path], output_path: Path) -> None:
    thumb_width = 360
    label_height = 32
    margin = 20
    columns = 3
    prepared: list[tuple[Path, Image.Image]] = []
    for path in paths:
        with Image.open(path) as source:
            image = source.convert("RGB")
            height = max(1, round(image.height * thumb_width / image.width))
            prepared.append((path, image.resize((thumb_width, height), Image.Resampling.LANCZOS)))
    cell_height = max(image.height for _, image in prepared) + label_height
    rows = (len(prepared) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (margin + columns * (thumb_width + margin), margin + rows * (cell_height + margin)),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    for index, (path, image) in enumerate(prepared):
        row, column = divmod(index, columns)
        x = margin + column * (thumb_width + margin)
        y = margin + row * (cell_height + margin)
        draw.text((x, y + 7), path.name, fill="#243447")
        sheet.paste(image, (x, y + label_height))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)


def make_navigation_contact_sheets(
    project_root: Path,
    inventory: list[dict],
    output_root: Path,
) -> list[Path]:
    """Build navigation images without changing the pending original-image ledger."""
    grouped: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for row in inventory:
        relative = row["relative_path"]
        path = _safe_resolve(project_root, relative)
        grouped[(row["render_kind"], row["artifact_key"])].append(path)
    outputs: list[Path] = []
    for (kind, key), paths in sorted(grouped.items()):
        output_path = output_root / kind / f"{key}.png"
        _contact_sheet(paths, output_path)
        outputs.append(output_path)
    return outputs


def finalize_review_inventory(
    inventory: list[dict], reviewed_paths: list[str], attestation: str
) -> list[dict]:
    """Mark only an exact, manually supplied set of original images as reviewed."""
    expected = {row["relative_path"] for row in inventory}
    reviewed = set(reviewed_paths)
    missing = sorted(expected - reviewed)
    extra = sorted(reviewed - expected)
    if missing or extra:
        raise ValueError(f"缺少人工复核或路径不匹配: missing={missing}, extra={extra}")
    if not attestation.strip():
        raise ValueError("人工复核说明不能为空")
    return [
        {
            **row,
            "review_status": "pass",
            "inspection_method": attestation.strip(),
            "issues": [],
        }
        for row in inventory
    ]


def required_segment_keys(catalog: list[dict]) -> set[str]:
    """All five overview catalogs exceed ten data rows and need readable segments."""
    counts: dict[str, int] = defaultdict(int)
    for record in catalog:
        counts[str(record["cat"])] += 1
    return {f"{category}-overview" for category, count in counts.items() if count > 10}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--finalize", action="store_true", help="在逐张人工查看完成后标记全部原图通过")
    args = parser.parse_args(argv)
    if args.finalize:
        inventory = json.loads(INVENTORY_FILE.read_text(encoding="utf-8"))
        finalized = finalize_review_inventory(
            inventory,
            [row["relative_path"] for row in inventory],
            "逐张打开原始 PNG，并检查截断、重叠、表格破裂、中文缺字、页眉页脚、空白、列宽、行高、网址溢出和渲染异常。",
        )
        INVENTORY_FILE.write_text(json.dumps(finalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"reviewed={len(finalized)}")
        return 0

    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
    validated = validate_delivery_tree(PROJECT_ROOT, manifest)
    docx = collect_docx_render_inventory(DOCX_RENDER_ROOT, manifest)
    xlsx = collect_xlsx_render_inventory(
        XLSX_RENDER_ROOT,
        manifest,
        required_segment_keys=required_segment_keys(catalog),
    )
    inventory = docx + xlsx
    CONTACT_ROOT.mkdir(parents=True, exist_ok=True)
    contacts = make_navigation_contact_sheets(PROJECT_ROOT, inventory, CONTACT_ROOT)
    INVENTORY_FILE.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"delivery={len(validated)} docx_pages={len(docx)} "
        f"xlsx_originals={sum(row['render_kind'] == 'worksheet' for row in xlsx)} "
        f"xlsx_segments={sum(row['render_kind'] == 'segment' for row in xlsx)} "
        f"contacts={len(contacts)} pending={len(inventory)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
