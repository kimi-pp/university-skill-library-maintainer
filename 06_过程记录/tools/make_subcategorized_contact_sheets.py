"""Validate Task 7 inputs, inventory original renders, and build navigation sheets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "subcategory_manifest.json"
CATALOG_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "plain_language_catalog.json"
DELIVERY_ROOT = PROJECT_ROOT / "05_交付物" / "通俗细分版_2026-08-07"
DOCX_RENDER_ROOT = PROJECT_ROOT / "06_过程记录" / "renders" / "subcategorized_docx"
XLSX_RENDER_ROOT = PROJECT_ROOT / "06_过程记录" / "renders" / "subcategorized_xlsx"
CONTACT_ROOT = PROJECT_ROOT / "06_过程记录" / "renders" / "subcategorized_contact_sheets"
AUDIT_ROOT = PROJECT_ROOT / "06_过程记录" / "visual_review"
INVENTORY_FILE = AUDIT_ROOT / "task-7-inventory.json"
FINAL_REVIEW_FILE = AUDIT_ROOT / "task-7-finalized.json"
DOCX_RENDER_MANIFEST_NAME = "rendered-pages.json"

INVENTORY_SCHEMA_VERSION = 2
REVIEW_LOG_SCHEMA_VERSION = 1
MIN_NON_BACKGROUND_RATIO = 0.002
MIN_GRAYSCALE_VARIANCE = 1.0
INVENTORY_BINDING_FIELDS = ("relative_path", "image_sha256", "width", "height")

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
            grayscale = image.convert("L")
            grayscale.thumbnail((512, 512), Image.Resampling.LANCZOS)
            histogram = grayscale.histogram()
    except Exception as exc:  # Pillow provides format-specific exception types.
        raise ValueError(f"渲染图无效: {path}") from exc
    if width < 1 or height < 1:
        raise ValueError(f"渲染尺寸无效: {path}")
    total = sum(histogram)
    non_background_ratio = sum(histogram[:248]) / total
    mean = sum(value * count for value, count in enumerate(histogram)) / total
    variance = sum(
        ((value - mean) ** 2) * count for value, count in enumerate(histogram)
    ) / total
    if (
        non_background_ratio < MIN_NON_BACKGROUND_RATIO
        or variance < MIN_GRAYSCALE_VARIANCE
    ):
        raise ValueError(
            f"渲染图为空白或近空白: {path}; "
            f"non_background_ratio={non_background_ratio:.6f} variance={variance:.6f}"
        )
    return width, height


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _inventory_digest(images: list[dict]) -> str:
    bindings: list[dict] = []
    seen: set[str] = set()
    for row in sorted(images, key=lambda item: item.get("relative_path", "")):
        missing = [field for field in INVENTORY_BINDING_FIELDS if field not in row]
        if missing:
            raise ValueError(f"库存记录缺少绑定字段: {missing}")
        relative_path = row["relative_path"]
        if not isinstance(relative_path, str) or not relative_path:
            raise ValueError("库存 relative_path 无效")
        if relative_path in seen:
            raise ValueError(f"库存路径重复: {relative_path}")
        seen.add(relative_path)
        image_hash = row["image_sha256"]
        if not isinstance(image_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", image_hash):
            raise ValueError(f"库存 image_sha256 无效: {relative_path}")
        if not isinstance(row["width"], int) or row["width"] < 1:
            raise ValueError(f"库存 width 无效: {relative_path}")
        if not isinstance(row["height"], int) or row["height"] < 1:
            raise ValueError(f"库存 height 无效: {relative_path}")
        bindings.append({field: row[field] for field in INVENTORY_BINDING_FIELDS})
    encoded = json.dumps(
        bindings,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_inventory_document(images: list[dict]) -> dict:
    """Create a stable, hash-bound initial inventory without review conclusions."""
    ordered = sorted((dict(row) for row in images), key=lambda item: item["relative_path"])
    digest = _inventory_digest(ordered)
    return {
        "schema_version": INVENTORY_SCHEMA_VERSION,
        "inventory_digest": digest,
        "images": ordered,
    }


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
                    "image_sha256": _sha256_file(path),
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
                    "image_sha256": _sha256_file(path),
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
                    "image_sha256": _sha256_file(path),
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


def _parse_timestamp(value: object, *, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(f"批次元数据缺少 {label}")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"批次时间无效: {label}={value}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"批次时间缺少时区: {label}={value}")
    return parsed


def _validate_inventory_document(inventory: object) -> tuple[list[dict], str]:
    if not isinstance(inventory, dict) or inventory.get("schema_version") != INVENTORY_SCHEMA_VERSION:
        raise ValueError("库存 schema_version 无效")
    images = inventory.get("images")
    if not isinstance(images, list) or not images:
        raise ValueError("库存 images 为空或无效")
    computed = _inventory_digest(images)
    recorded = inventory.get("inventory_digest")
    if recorded != computed:
        raise ValueError(
            f"inventory_digest 不一致: recorded={recorded} computed={computed}"
        )
    return images, computed


def load_review_log(path: Path) -> list[dict]:
    """Load an independently prepared JSONL review declaration."""
    records: list[dict] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line.strip():
            continue
        try:
            record = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"review log 第 {line_number} 行不是有效 JSON") from exc
        if not isinstance(record, dict):
            raise ValueError(f"review log 第 {line_number} 行必须为对象")
        records.append(record)
    if not records:
        raise ValueError("review log 为空")
    return records


def finalize_review_inventory(
    project_root: Path,
    inventory: dict,
    review_records: list[dict],
    *,
    review_log_sha256: str,
) -> dict:
    """Validate an external structured review declaration against current image bytes."""
    images, digest = _validate_inventory_document(inventory)
    inventory_by_path = {row["relative_path"]: row for row in images}

    for relative_path, row in inventory_by_path.items():
        image_path = _safe_resolve(project_root, relative_path)
        width, height = _validate_png(image_path)
        if (width, height) != (row["width"], row["height"]):
            raise ValueError(f"复核后图片尺寸变化: {relative_path}")
        current_hash = _sha256_file(image_path)
        if current_hash != row["image_sha256"]:
            raise ValueError(f"复核后图片替换或 hash 变化: {relative_path}")

    unknown_types = sorted(
        {
            str(record.get("record_type"))
            for record in review_records
            if record.get("record_type") not in {"session", "batch", "image"}
        }
    )
    if unknown_types:
        raise ValueError(f"review log 存在未知记录类型: {unknown_types}")
    sessions = [record for record in review_records if record.get("record_type") == "session"]
    batches = [record for record in review_records if record.get("record_type") == "batch"]
    reviewed_images = [record for record in review_records if record.get("record_type") == "image"]
    if len(sessions) != 1:
        raise ValueError("review log 必须恰好包含一个 session 记录")
    session = sessions[0]
    if session.get("schema_version") != REVIEW_LOG_SCHEMA_VERSION:
        raise ValueError("review log session schema_version 无效")
    session_id = session.get("session_id")
    if not isinstance(session_id, str) or not session_id.strip():
        raise ValueError("review log session_id 无效")
    if session.get("inventory_digest") != digest:
        raise ValueError("review log inventory_digest 与库存不一致")
    if not isinstance(session.get("time_basis"), str) or not session["time_basis"].strip():
        raise ValueError("review log session 缺少 time_basis")

    if len(batches) < 2:
        raise ValueError("完成声明必须包含多个人工复核批次")
    batch_ids = [record.get("batch_id") for record in batches]
    if any(not isinstance(batch_id, str) or not batch_id for batch_id in batch_ids):
        raise ValueError("批次元数据缺少 batch_id")
    duplicate_batch_ids = sorted(
        batch_id for batch_id, count in Counter(batch_ids).items() if count > 1
    )
    if duplicate_batch_ids:
        raise ValueError(f"批次 ID 重复: {duplicate_batch_ids}")
    ordered_batches = sorted(batches, key=lambda record: record.get("sequence", -1))
    if [record.get("sequence") for record in ordered_batches] != list(
        range(1, len(ordered_batches) + 1)
    ):
        raise ValueError("批次 sequence 必须从 1 连续递增")
    previous_end: datetime | None = None
    for batch in ordered_batches:
        for field in ("reviewer_id", "session_id", "started_at", "ended_at", "inspection_criteria"):
            if field not in batch:
                raise ValueError(f"批次元数据缺少 {field}: {batch.get('batch_id')}")
        if not isinstance(batch["reviewer_id"], str) or not batch["reviewer_id"].strip():
            raise ValueError(f"批次 reviewer_id 无效: {batch['batch_id']}")
        if batch["session_id"] != session_id:
            raise ValueError(f"批次 session_id 不一致: {batch['batch_id']}")
        criteria = batch["inspection_criteria"]
        if (
            not isinstance(criteria, list)
            or not criteria
            or any(not isinstance(item, str) or not item.strip() for item in criteria)
        ):
            raise ValueError(f"批次 inspection_criteria 无效: {batch['batch_id']}")
        started = _parse_timestamp(batch["started_at"], label="started_at")
        ended = _parse_timestamp(batch["ended_at"], label="ended_at")
        if ended < started:
            raise ValueError(f"批次结束时间早于开始时间: {batch['batch_id']}")
        if previous_end is not None and started < previous_end:
            raise ValueError(f"批次时间顺序重叠或倒退: {batch['batch_id']}")
        previous_end = ended

    reviewed_paths = [record.get("relative_path") for record in reviewed_images]
    invalid_paths = [path for path in reviewed_paths if not isinstance(path, str) or not path]
    if invalid_paths:
        raise ValueError("review log image relative_path 无效")
    duplicate_paths = sorted(
        path for path, count in Counter(reviewed_paths).items() if count > 1
    )
    if duplicate_paths:
        raise ValueError(f"review log 图片路径重复: {duplicate_paths}")
    expected_paths = set(inventory_by_path)
    actual_paths = set(reviewed_paths)
    missing = sorted(expected_paths - actual_paths)
    extra = sorted(actual_paths - expected_paths)
    if missing or extra:
        raise ValueError(f"review log 未精确覆盖库存: 缺失={missing} 额外={extra}")

    batch_by_id = {record["batch_id"]: record for record in batches}
    batch_counts: Counter[str] = Counter()
    finalized_images: list[dict] = []
    for record in reviewed_images:
        relative_path = record["relative_path"]
        inventory_row = inventory_by_path[relative_path]
        batch_id = record.get("batch_id")
        if batch_id not in batch_by_id:
            raise ValueError(f"图片引用未知 batch_id: {relative_path}")
        batch_counts[batch_id] += 1
        if record.get("image_sha256") != inventory_row["image_sha256"]:
            raise ValueError(f"review log image hash 与库存不一致: {relative_path}")
        status = record.get("status")
        if status not in {"pass", "fail", "needs_fix", "blocked"}:
            raise ValueError(f"review log status 无效: {relative_path}")
        issues = record.get("issues")
        if not isinstance(issues, list) or any(not isinstance(issue, str) or not issue.strip() for issue in issues):
            raise ValueError(f"review log issues 无效: {relative_path}")
        if status == "pass" and issues:
            raise ValueError(f"pass 记录不得包含问题 issues: {relative_path}")
        if status != "pass" and not issues:
            raise ValueError(f"非 pass 记录必须包含问题说明 issues: {relative_path}")
        finalized_images.append(
            {
                **inventory_row,
                "batch_id": batch_id,
                "status": status,
                "issues": issues,
            }
        )
    empty_batches = sorted(set(batch_by_id) - set(batch_counts))
    if empty_batches:
        raise ValueError(f"批次没有逐图记录: {empty_batches}")

    pass_count = sum(row["status"] == "pass" for row in finalized_images)
    nonpass_count = len(finalized_images) - pass_count
    return {
        "schema_version": 1,
        "evidence_scope": "structured human review declaration; not an external signature or video record",
        "inventory_digest": digest,
        "review_log_sha256": review_log_sha256,
        "session": session,
        "batches": ordered_batches,
        "summary": {
            "images": len(finalized_images),
            "batches": len(ordered_batches),
            "pass": pass_count,
            "nonpass": nonpass_count,
        },
        "review_complete": nonpass_count == 0,
        "images": sorted(finalized_images, key=lambda row: row["relative_path"]),
    }


def required_segment_keys(catalog: list[dict]) -> set[str]:
    """All five overview catalogs exceed ten data rows and need readable segments."""
    counts: dict[str, int] = defaultdict(int)
    for record in catalog:
        counts[str(record["cat"])] += 1
    return {f"{category}-overview" for category, count in counts.items() if count > 10}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--finalize", action="store_true", help="验证独立逐图复核日志并生成完成结果")
    parser.add_argument("--review-log", type=Path, help="独立准备的 JSONL 逐图人工复核声明")
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_FILE)
    parser.add_argument("--result", type=Path, default=FINAL_REVIEW_FILE)
    args = parser.parse_args(argv)
    if args.finalize:
        if args.review_log is None:
            parser.error("--finalize 必须显式提供 --review-log <jsonl>")
        inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
        review_records = load_review_log(args.review_log)
        finalized = finalize_review_inventory(
            args.project_root,
            inventory,
            review_records,
            review_log_sha256=_sha256_file(args.review_log),
        )
        args.result.parent.mkdir(parents=True, exist_ok=True)
        args.result.write_text(
            json.dumps(finalized, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(
            f"reviewed={finalized['summary']['images']} "
            f"batches={finalized['summary']['batches']} "
            f"inventory_digest={finalized['inventory_digest']} "
            f"complete={str(finalized['review_complete']).lower()}"
        )
        return 0 if finalized["review_complete"] else 1

    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
    validated = validate_delivery_tree(PROJECT_ROOT, manifest)
    docx = collect_docx_render_inventory(DOCX_RENDER_ROOT, manifest)
    xlsx = collect_xlsx_render_inventory(
        XLSX_RENDER_ROOT,
        manifest,
        required_segment_keys=required_segment_keys(catalog),
    )
    inventory = build_inventory_document(docx + xlsx)
    CONTACT_ROOT.mkdir(parents=True, exist_ok=True)
    contacts = make_navigation_contact_sheets(PROJECT_ROOT, inventory["images"], CONTACT_ROOT)
    args.inventory.parent.mkdir(parents=True, exist_ok=True)
    args.inventory.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"delivery={len(validated)} docx_pages={len(docx)} "
        f"xlsx_originals={sum(row['render_kind'] == 'worksheet' for row in xlsx)} "
        f"xlsx_segments={sum(row['render_kind'] == 'segment' for row in xlsx)} "
        f"contacts={len(contacts)} pending={len(inventory['images'])} "
        f"inventory_digest={inventory['inventory_digest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
