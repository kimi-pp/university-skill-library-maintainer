"""Render each selected DOCX to isolated page PNGs and a QA contact sheet."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from build_subcategorized_documents import (  # noqa: E402
    MANIFEST_FILE,
    _parse_only,
    select_manifest_items,
)


RENDER_SCRIPT_ENV = "DOCUMENTS_RENDER_DOCX"
DEFAULT_RENDER_ROOT = PROJECT_ROOT / "06_过程记录" / "renders" / "subcategorized_docx"
RENDER_MANIFEST_NAME = "rendered-pages.json"


def resolve_render_script(
    explicit: Path | None = None,
    *,
    environ: dict[str, str] | None = None,
) -> Path:
    """Resolve the canonical documents-skill renderer without version/user hard-coding."""
    environment = os.environ if environ is None else environ
    candidate: Path | None = explicit
    source = "--render-script"
    if candidate is None and environment.get(RENDER_SCRIPT_ENV):
        candidate = Path(environment[RENDER_SCRIPT_ENV])
        source = RENDER_SCRIPT_ENV
    if candidate is not None:
        resolved = candidate.expanduser().resolve()
        if resolved.is_file():
            return resolved
        raise FileNotFoundError(
            f"找不到 documents 技能渲染器（来源 {source}）: {resolved}；"
            f"请使用 --render-script 或 {RENDER_SCRIPT_ENV} 指定 canonical render_docx.py"
        )

    codex_root = Path(environment.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    search_root = codex_root / "plugins" / "cache" / "openai-primary-runtime" / "documents"
    matches = sorted(
        search_root.glob("*/skills/documents/render_docx.py"),
        key=lambda path: path.parent.parent.parent.name,
        reverse=True,
    )
    if matches:
        return matches[0].resolve()
    raise FileNotFoundError(
        f"找不到 documents 技能渲染器；默认搜索 {search_root}。"
        f"请使用 --render-script 或 {RENDER_SCRIPT_ENV} 指定 canonical render_docx.py"
    )


def build_render_plan(items: list[dict], project_root: Path, output_root: Path) -> list[dict]:
    """Return one collision-free render directory per selected DOCX."""
    root = project_root.resolve()
    renders = output_root.resolve()
    plan: list[dict] = []
    seen_outputs: set[Path] = set()
    for item in select_manifest_items(items, None):
        document_path = (root / Path(item["path"])).resolve()
        if root not in document_path.parents:
            raise ValueError(f"不安全的 DOCX 路径: {item['path']}")
        output_dir = (renders / item["key"]).resolve()
        if renders != output_dir and renders not in output_dir.parents:
            raise ValueError(f"不安全的渲染目录: {output_dir}")
        if output_dir in seen_outputs:
            raise ValueError(f"重复渲染目录: {output_dir}")
        seen_outputs.add(output_dir)
        plan.append({"key": item["key"], "docx_path": document_path, "output_dir": output_dir})
    return plan


def _page_number(path: Path) -> int:
    try:
        return int(path.stem.rsplit("-", 1)[1])
    except (IndexError, ValueError) as exc:
        raise ValueError(f"无法解析页码: {path.name}") from exc


def _make_contact_sheet(page_paths: list[Path], output_path: Path) -> None:
    """Create a navigation-only sheet; original PNGs remain the inspection authority."""
    if not page_paths:
        raise ValueError("没有页面 PNG，无法生成联系表")
    thumb_width = 360
    margin = 24
    label_height = 34
    columns = 3
    prepared: list[Image.Image] = []
    for path in page_paths:
        with Image.open(path) as image:
            preview = image.convert("RGB")
            height = max(1, round(preview.height * thumb_width / preview.width))
            prepared.append(preview.resize((thumb_width, height), Image.Resampling.LANCZOS))
    cell_height = max(image.height for image in prepared) + label_height
    rows = (len(prepared) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (margin + columns * (thumb_width + margin), margin + rows * (cell_height + margin)),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    for index, (path, image) in enumerate(zip(page_paths, prepared)):
        row, column = divmod(index, columns)
        x = margin + column * (thumb_width + margin)
        y = margin + row * (cell_height + margin)
        sheet.paste(image, (x, y + label_height))
        draw.text((x, y + 8), f"Page {_page_number(path)}", fill="#243447")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)


def render_plan(plan: list[dict], *, render_script: Path | None = None) -> dict[str, list[Path]]:
    """Render selected documents with the packaged renderer and return all page PNGs."""
    render_script = resolve_render_script(render_script)
    results: dict[str, list[Path]] = {}
    for item in plan:
        document_path = Path(item["docx_path"])
        output_dir = Path(item["output_dir"])
        if not document_path.exists():
            raise FileNotFoundError(f"待渲染 DOCX 不存在: {document_path}")
        output_dir.mkdir(parents=True, exist_ok=True)
        for stale in [
            *output_dir.glob("page-*.png"),
            output_dir / "contact-sheet.png",
            output_dir / RENDER_MANIFEST_NAME,
        ]:
            if stale.exists():
                stale.unlink()
        subprocess.run(
            [sys.executable, str(render_script), str(document_path), "--output_dir", str(output_dir)],
            check=True,
        )
        pages = sorted(output_dir.glob("page-*.png"), key=_page_number)
        if not pages or any(path.stat().st_size == 0 for path in pages):
            raise RuntimeError(f"{item['key']} 未生成有效页面 PNG")
        (output_dir / RENDER_MANIFEST_NAME).write_text(
            json.dumps({"pages": [path.name for path in pages]}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        _make_contact_sheet(pages, output_dir / "contact-sheet.png")
        results[item["key"]] = pages
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="*", help="仅渲染键，如 05-overview 05-05")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_RENDER_ROOT)
    parser.add_argument("--render-script", type=Path, help="canonical documents 技能 render_docx.py 路径")
    args = parser.parse_args(argv)
    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    if not isinstance(manifest, list):
        raise ValueError("manifest 格式错误")
    selected = select_manifest_items(manifest, _parse_only(args.only))
    results = render_plan(
        build_render_plan(selected, PROJECT_ROOT, args.output_root),
        render_script=args.render_script,
    )
    total_pages = sum(len(pages) for pages in results.values())
    details = ",".join(f"{key}:{len(pages)}" for key, pages in results.items())
    print(f"rendered={len(results)} pages={total_pages} details={details}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
