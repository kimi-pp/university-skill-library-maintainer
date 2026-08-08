#!/usr/bin/env python3
"""
generate-xfdf.py —— 把 issues.json 转换为 PDF 批注旁路 XFDF 文件

用法:
    python3 generate-xfdf.py <原.pdf> <issues.json> <输出.xfdf>

特性:
    - 纯 Python 3.8+ 标准库（xml.etree.ElementTree / re / json / sys / os /
      datetime / pathlib / argparse / hashlib）
    - 不修改原 pdf；输出同目录的 `.xfdf` 旁路文件
    - 用 MediaBox 正则解析获得每页尺寸，无需 pypdf / pdfplumber
    - 退化链路：page+bbox → highlight / page-only → text / no-page → skip
    - 跨阅读器兼容：Adobe Reader DC、Adobe Acrobat Pro、Foxit PhantomPDF/Reader

参见:
    rules/xfdf-annotation.md —— XFDF 结构契约与算法
    rules/issues-schema.md   —— issues.json 数据契约
    templates/readme-section-import-xfdf.md —— 导入指引
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------- #
# 常量与命名空间
# --------------------------------------------------------------------------- #

XFDF_NS = "http://ns.adobe.com/xfdf/"
XFDF_TAG = f"{{{XFDF_NS}}}"

# 颜色映射（rules/xfdf-annotation.md §7）
COLOR_MAP = {
    "fatal": "#E74C3C",  # 红
    "major": "#F39C12",  # 橙
    "minor": "#F1C40F",  # 黄
}

# category / severity 中文映射
CATEGORY_CN = {
    "structure": "结构",
    "argumentation": "论证深度",
    "literature-review": "文献综述",
    "empirical": "实证",
    "legal-norms": "规范适用",
    "language": "语言",
    "policy": "对策",
    "academic-integrity": "学术不端线索",
    "citation-format": "引注格式",
    "citation-missing-info": "引注信息",
}
SEVERITY_CN = {"fatal": "致命", "major": "重要", "minor": "轻微"}

# issues.json 枚举
ENUM_SOURCE = {"thesis", "citation"}
ENUM_CATEGORY = set(CATEGORY_CN.keys())
ENUM_SEVERITY = set(SEVERITY_CN.keys())
ENUM_SCOPE = {"document", "chapter", "paragraph", "sentence", "span"}
ID_PATTERN = re.compile(
    r"^(thesis|citation)-"
    r"(structure|argumentation|literature-review|empirical|legal-norms|"
    r"language|policy|academic-integrity|citation-format|citation-missing-info)"
    r"-\d{3}$"
)
GROUP_ID_PATTERN = re.compile(r"^g-\d{3,}$")
CELL_KEYS = {"table_index", "row", "col", "paragraph_index_in_cell"}

# 默认页面尺寸（A4，MediaBox 解析失败时兜底）
DEFAULT_PAGE_W = 595.28
DEFAULT_PAGE_H = 841.89

# 作者与批注常量
AUTHOR = "unified-thesis-reviewer"

# 退化便签区域（页面左上 20×20 points）
TEXT_NOTE_SIZE = 20.0


# --------------------------------------------------------------------------- #
# issues.json 自校验（与 rules/issues-schema.md §6 双轨一致）
# --------------------------------------------------------------------------- #

def validate_issues_json(data: Any, *, input_is_pdf: bool = True) -> list[str]:
    """校验 issues.json，返回错误消息列表（空表示合规）。

    pdf 模式（input_is_pdf=True）下 locator.page_number 必填。
    """
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top-level must be JSON object"]
    if data.get("schema_version") != "1.0":
        errors.append(f"schema_version must be '1.0', got {data.get('schema_version')!r}")
    issues = data.get("issues")
    if not isinstance(issues, list):
        errors.append("issues must be an array")
        return errors

    seen_ids: set[str] = set()
    group_key_to_gid: dict[tuple, str] = {}
    gid_to_group_key: dict[str, tuple] = {}

    for idx, it in enumerate(issues):
        ctx = f"issues[{idx}]"
        if not isinstance(it, dict):
            errors.append(f"{ctx}: must be object")
            continue

        for field in (
            "id", "source", "category", "severity", "scope",
            "locator", "excerpt", "problem", "suggestion", "group_id",
            "anchor_text",  # v2 新增必填
        ):
            if field not in it:
                errors.append(f"{ctx}: missing required field '{field}'")

        if it.get("source") is not None and it["source"] not in ENUM_SOURCE:
            errors.append(f"{ctx}.source: {it['source']!r} not in {sorted(ENUM_SOURCE)}")
        if it.get("category") is not None and it["category"] not in ENUM_CATEGORY:
            errors.append(f"{ctx}.category: {it['category']!r} not in enum")
        if it.get("severity") is not None and it["severity"] not in ENUM_SEVERITY:
            errors.append(f"{ctx}.severity: {it['severity']!r} not in {sorted(ENUM_SEVERITY)}")
        if it.get("scope") is not None and it["scope"] not in ENUM_SCOPE:
            errors.append(f"{ctx}.scope: {it['scope']!r} not in {sorted(ENUM_SCOPE)}")

        if isinstance(it.get("id"), str):
            if not ID_PATTERN.match(it["id"]):
                errors.append(f"{ctx}.id: pattern mismatch, got {it['id']!r}")
            else:
                id_src = it["id"].split("-", 1)[0]
                id_cat = it["id"].rsplit("-", 1)[0].split("-", 1)[1]
                if it.get("source") and id_src != it["source"]:
                    errors.append(f"{ctx}.id: prefix {id_src!r} mismatches source")
                if it.get("category") and id_cat != it["category"]:
                    errors.append(f"{ctx}.id: middle {id_cat!r} mismatches category")

        if isinstance(it.get("id"), str):
            if it["id"] in seen_ids:
                errors.append(f"{ctx}.id: duplicate {it['id']!r}")
            seen_ids.add(it["id"])

        if it.get("scope") in ("document", "chapter"):
            if it.get("excerpt", "") != "":
                errors.append(f"{ctx}.excerpt: scope={it['scope']!r} requires empty string")

        if isinstance(it.get("excerpt"), str) and len(it["excerpt"]) > 60:
            errors.append(f"{ctx}.excerpt: length {len(it['excerpt'])} > 60")
        if isinstance(it.get("anchor_text"), str) and len(it["anchor_text"]) > 60:
            errors.append(f"{ctx}.anchor_text: length {len(it['anchor_text'])} > 60")
        if isinstance(it.get("problem"), str):
            if len(it["problem"]) == 0:
                errors.append(f"{ctx}.problem: must be non-empty")
            if len(it["problem"]) > 200:
                errors.append(f"{ctx}.problem: length > 200")

        sug = it.get("suggestion")
        if sug is not None:
            if not isinstance(sug, list):
                errors.append(f"{ctx}.suggestion: must be array")
            else:
                if not (1 <= len(sug) <= 5):
                    errors.append(f"{ctx}.suggestion: array length {len(sug)} not in [1,5]")
                for j, s in enumerate(sug):
                    if not isinstance(s, str):
                        errors.append(f"{ctx}.suggestion[{j}]: must be string")
                    elif len(s) > 500:
                        errors.append(f"{ctx}.suggestion[{j}]: length > 500")
                    elif len(s) == 0:
                        errors.append(f"{ctx}.suggestion[{j}]: must be non-empty")

        loc = it.get("locator")
        if not isinstance(loc, dict):
            errors.append(f"{ctx}.locator: must be object")
            continue

        chapter = loc.get("chapter")
        if not isinstance(chapter, str) or not chapter:
            errors.append(f"{ctx}.locator.chapter: must be non-empty string")
        pidx = loc.get("paragraph_index")
        if not isinstance(pidx, int) or isinstance(pidx, bool):
            errors.append(f"{ctx}.locator.paragraph_index: must be integer")
        elif pidx < -1:
            errors.append(f"{ctx}.locator.paragraph_index: {pidx} < -1")

        present_cell = CELL_KEYS & set(loc.keys())
        if present_cell and present_cell != CELL_KEYS:
            missing = CELL_KEYS - present_cell
            errors.append(f"{ctx}.locator: table-cell keys incomplete; missing {sorted(missing)}")
        if present_cell == CELL_KEYS:
            if loc.get("paragraph_index") != -1:
                errors.append(f"{ctx}.locator: table-cell requires paragraph_index == -1")

        if input_is_pdf and "page_number" not in loc:
            errors.append(f"{ctx}.locator.page_number: required for pdf input")
        if "page_number" in loc:
            pn = loc["page_number"]
            if not isinstance(pn, int) or isinstance(pn, bool) or pn < 1:
                errors.append(f"{ctx}.locator.page_number: must be integer >= 1")

        if "bbox" in loc:
            bb = loc["bbox"]
            if not isinstance(bb, list) or len(bb) != 4:
                errors.append(f"{ctx}.locator.bbox: must be array of length 4")
            else:
                for k, v in enumerate(bb):
                    if isinstance(v, bool) or not isinstance(v, (int, float)):
                        errors.append(f"{ctx}.locator.bbox[{k}]: must be number")

        gid = it.get("group_id")
        if isinstance(gid, str):
            if not GROUP_ID_PATTERN.match(gid):
                errors.append(f"{ctx}.group_id: pattern mismatch")
            gkey = (it.get("source"), it.get("category"),
                    loc.get("chapter"), loc.get("paragraph_index"))
            if gkey in group_key_to_gid and group_key_to_gid[gkey] != gid:
                errors.append(f"{ctx}.group_id: inconsistent with key {gkey}")
            elif gid in gid_to_group_key and gid_to_group_key[gid] != gkey:
                errors.append(f"{ctx}.group_id: {gid!r} reused across different keys")
            else:
                group_key_to_gid[gkey] = gid
                gid_to_group_key[gid] = gkey

    return errors


# --------------------------------------------------------------------------- #
# pdf 页面尺寸的 stdlib 解析（MediaBox 正则扫描）
# --------------------------------------------------------------------------- #

_MEDIABOX_PATTERN = re.compile(
    rb"/MediaBox\s*\[\s*(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s*\]"
)


def load_pdf_page_sizes(pdf_path: Path) -> dict[int, tuple[float, float]]:
    """手工解析 pdf 字节内容扫描 /MediaBox，返回 {page_index (0-based): (width, height)}。

    实现不依赖第三方库：读 pdf 原始字节 → 正则匹配 MediaBox → 按出现顺序赋予 page_index。
    注意：加密 pdf / xref 压缩流 / 对象流会影响扫描精度，但可接受——失败时回退 A4 尺寸。
    """
    sizes: dict[int, tuple[float, float]] = {}
    try:
        raw = pdf_path.read_bytes()
    except OSError:
        return sizes

    if not raw.startswith(b"%PDF-"):
        # 不是合法 pdf
        return sizes

    for i, m in enumerate(_MEDIABOX_PATTERN.finditer(raw)):
        try:
            x0, y0, x1, y1 = (float(m.group(k)) for k in range(1, 5))
        except (TypeError, ValueError):
            continue
        w = abs(x1 - x0)
        h = abs(y1 - y0)
        if w > 0 and h > 0:
            sizes[i] = (w, h)

    return sizes


def page_size(page_sizes: dict[int, tuple[float, float]], page_index: int) -> tuple[float, float]:
    """返回 page_index 对应页尺寸，缺失时回退 A4。"""
    if page_index in page_sizes:
        return page_sizes[page_index]
    # 若 page 0 有尺寸则用它（多页文档通常一致）
    if 0 in page_sizes:
        return page_sizes[0]
    return (DEFAULT_PAGE_W, DEFAULT_PAGE_H)


# --------------------------------------------------------------------------- #
# 坐标与颜色的辅助函数
# --------------------------------------------------------------------------- #

def bbox_to_coords(x0: float, y0: float, x1: float, y1: float) -> list[float]:
    """bbox[x0,y0,x1,y1]（左下+右上）转 XFDF coords 8 浮点数（左上/右上/左下/右下）。"""
    return [
        x0, y1,  # 左上
        x1, y1,  # 右上
        x0, y0,  # 左下
        x1, y0,  # 右下
    ]


def clip_bbox(
    bbox: list[float], page_w: float, page_h: float
) -> tuple[list[float], bool]:
    """把越界顶点 clip 到页面边界。返回 (clipped_bbox, was_clipped)。"""
    x0, y0, x1, y1 = bbox
    cx0 = max(0.0, min(x0, page_w))
    cy0 = max(0.0, min(y0, page_h))
    cx1 = max(0.0, min(x1, page_w))
    cy1 = max(0.0, min(y1, page_h))
    was_clipped = (cx0, cy0, cx1, cy1) != (x0, y0, x1, y1)
    return ([cx0, cy0, cx1, cy1], was_clipped)


def severity_to_color(severity: str) -> str:
    """严重程度 → hex 颜色字符串。"""
    return COLOR_MAP.get(severity, "#F1C40F")  # 默认黄色


def _now_iso() -> str:
    """当前 UTC 时间 ISO 8601（秒精度，带 Z）。"""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _format_number(n: float) -> str:
    """浮点数格式化为 XFDF 友好的字符串（去掉不必要的尾零）。"""
    if n == int(n):
        return str(int(n))
    return f"{n:.4f}".rstrip("0").rstrip(".")


def _coords_to_str(coords: list[float]) -> str:
    return ",".join(_format_number(c) for c in coords)


# --------------------------------------------------------------------------- #
# 批注正文渲染（与 inject-docx-comments.py 的 render_annotation_body 同源）
# --------------------------------------------------------------------------- #

def render_annotation_body(issue: dict) -> str:
    """按 templates/annotation-body-template.md 的格式渲染 XFDF 批注正文。

    换行用字符 '\n'（XFDF contents 是普通 XML 文本节点）。
    """
    cat_cn = CATEGORY_CN.get(issue.get("category", ""), issue.get("category", ""))
    sev_cn = SEVERITY_CN.get(issue.get("severity", ""), issue.get("severity", ""))
    problem = issue.get("problem", "")
    sugg = issue.get("suggestion", []) or [""]
    issue_id = issue.get("id", "")

    lines = [f"【{cat_cn}】【{sev_cn}】{problem} → {sugg[0]}"]
    if len(sugg) > 1:
        lines.append("其他建议：")
        for s in sugg[1:]:
            lines.append(f"  · {s}")
    lines.append(f"[id: {issue_id}]")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# XFDF 元素构造
# --------------------------------------------------------------------------- #

def build_xfdf_root(pdf_filename: str) -> ET.Element:
    """构造 XFDF 根节点：<xfdf><f href="{basename}"/><annots/></xfdf>"""
    ET.register_namespace("", XFDF_NS)
    root = ET.Element(f"{XFDF_TAG}xfdf")
    f_el = ET.SubElement(root, f"{XFDF_TAG}f")
    # href 只用纯文件名，确保 xfdf 与 pdf 同目录搬迁时仍然关联
    f_el.set("href", os.path.basename(pdf_filename))
    ET.SubElement(root, f"{XFDF_TAG}annots")
    return root


def build_highlight(
    issue: dict,
    bbox_clipped: list[float],
    page_0based: int,
    now_iso: str,
) -> ET.Element:
    """构造 <highlight> 元素（bbox 已 clip 后输入）。"""
    el = ET.Element(f"{XFDF_TAG}highlight")
    el.set("page", str(page_0based))
    el.set("name", issue["id"])
    el.set("title", AUTHOR)
    el.set("date", now_iso)
    el.set("creationdate", now_iso)  # Foxit 兼容：双写
    el.set("color", severity_to_color(issue.get("severity", "")))
    coords = bbox_to_coords(*bbox_clipped)
    el.set("coords", _coords_to_str(coords))

    contents = ET.SubElement(el, f"{XFDF_TAG}contents")
    contents.text = render_annotation_body(issue)
    return el


def build_text(
    issue: dict,
    page_0based: int,
    page_h: float,
    now_iso: str,
) -> ET.Element:
    """构造 <text> 便签元素（页面左上 20×20 points）。"""
    el = ET.Element(f"{XFDF_TAG}text")
    el.set("page", str(page_0based))
    el.set("name", issue["id"])
    el.set("title", AUTHOR)
    el.set("date", now_iso)
    el.set("creationdate", now_iso)
    el.set("color", severity_to_color(issue.get("severity", "")))

    # rect = [0, H-20, 20, H]（PDF 坐标系：y 轴向上，左上角）
    rect = [0.0, page_h - TEXT_NOTE_SIZE, TEXT_NOTE_SIZE, page_h]
    el.set("rect", ",".join(_format_number(c) for c in rect))

    contents = ET.SubElement(el, f"{XFDF_TAG}contents")
    contents.text = render_annotation_body(issue)
    return el


# --------------------------------------------------------------------------- #
# 退化链路分派
# --------------------------------------------------------------------------- #

def dispatch_annotation(
    issue: dict,
    page_sizes: dict[int, tuple[float, float]],
    now_iso: str,
    log: list[str],
) -> ET.Element | None:
    """根据 issue.locator 的 page_number / bbox 状态返回 annotation 元素，或 None（skip）。

    log：脚本运行日志条目列表，用于记录 skipped / clipped 事件。
    """
    loc = issue.get("locator", {})
    pn = loc.get("page_number")
    bbox = loc.get("bbox")

    if not isinstance(pn, int) or pn < 1:
        log.append(f"skipped: {issue['id']} reason=no-page-number")
        return None

    page_0based = pn - 1
    page_w, page_h = page_size(page_sizes, page_0based)

    if isinstance(bbox, list) and len(bbox) == 4:
        clipped, was_clipped = clip_bbox(bbox, page_w, page_h)
        if was_clipped:
            log.append(f"clipped: {issue['id']} reason=bbox-out-of-bounds")
        # R7B.6：跨页 issue 单条生成——只取 locator.bbox（首个），不拆分
        return build_highlight(issue, clipped, page_0based, now_iso)

    # 有 page 但无 bbox → 退化为浮动便签（R7B.4 第 2 行）
    return build_text(issue, page_0based, page_h, now_iso)


# --------------------------------------------------------------------------- #
# 回读自校验
# --------------------------------------------------------------------------- #

class XfdfReadbackError(RuntimeError):
    """XFDF 回读校验失败，副本已被删除。"""


def readback_verify_xfdf(
    xfdf_path: Path, expected_count: int
) -> tuple[bool, list[str]]:
    """回读校验，返回 (ok, errors)。

    两不变式（R7A.12）：
    1. ET.parse 可解析
    2. <annots> 下 highlight + text 元素总数 == expected_count
    """
    errors: list[str] = []
    try:
        tree = ET.parse(xfdf_path)
    except ET.ParseError as e:
        errors.append(f"parse failed: {e}")
        return (False, errors)

    root = tree.getroot()
    annots = root.find(f".//{XFDF_TAG}annots")
    if annots is None:
        errors.append("missing <annots> element")
        return (False, errors)

    actual = 0
    for child in annots:
        if child.tag in (f"{XFDF_TAG}highlight", f"{XFDF_TAG}text"):
            actual += 1

    if actual != expected_count:
        errors.append(
            f"annotation count mismatch: expected {expected_count}, got {actual}"
        )

    return (len(errors) == 0, errors)


# --------------------------------------------------------------------------- #
# 主流程
# --------------------------------------------------------------------------- #

def generate(
    src_pdf: Path,
    issues_json: Path,
    dst_xfdf: Path,
) -> tuple[int, list[str]]:
    """主入口：生成 XFDF，返回 (成功 annotation 数, 日志列表)。"""
    # 1) 读 issues.json + 校验（pdf 模式：page_number 必填）
    data = json.loads(issues_json.read_text(encoding="utf-8"))
    errs = validate_issues_json(data, input_is_pdf=True)
    if errs:
        raise ValueError("issues.json validation failed:\n" + "\n".join(errs[:10]))

    # 2) 读 pdf 页面尺寸
    page_sizes = load_pdf_page_sizes(src_pdf)
    log: list[str] = []
    if not page_sizes:
        log.append(f"warn: no MediaBox parsed from {src_pdf}, using default A4")

    # 3) 构造 XFDF 根结构
    root = build_xfdf_root(src_pdf.name)
    annots = root.find(f"{XFDF_TAG}annots")
    assert annots is not None

    # 4) 分派每条 issue → highlight / text / skip
    now = _now_iso()
    mounted_count = 0
    for issue in data["issues"]:
        el = dispatch_annotation(issue, page_sizes, now, log)
        if el is not None:
            annots.append(el)
            mounted_count += 1

    # 5) 序列化到 UTF-8 字节（无 BOM）
    # 用 ET.tostring 确保无 BOM；手工加 XML 声明保证 standalone 属性
    xml_bytes = ET.tostring(root, encoding="utf-8", xml_declaration=False)
    decl = b'<?xml version="1.0" encoding="UTF-8"?>\n'
    dst_xfdf.write_bytes(decl + xml_bytes + b"\n")

    # 6) 回读两不变式
    ok, verify_errors = readback_verify_xfdf(dst_xfdf, mounted_count)
    if not ok:
        try:
            os.remove(dst_xfdf)
        except OSError:
            pass
        raise XfdfReadbackError(
            "readback verification failed:\n" + "\n".join(verify_errors)
        )

    return (mounted_count, log)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        prog="generate-xfdf",
        description="Generate an XFDF sidecar file from issues.json for a given PDF.",
    )
    ap.add_argument("src_pdf", type=Path, help="source .pdf file (unmodified)")
    ap.add_argument("issues_json", type=Path, help="issues.json path")
    ap.add_argument("dst_xfdf", type=Path, help="output .xfdf path")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    if not args.src_pdf.is_file():
        print(f"error: source pdf not found: {args.src_pdf}", file=sys.stderr)
        return 2
    if not args.issues_json.is_file():
        print(f"error: issues.json not found: {args.issues_json}", file=sys.stderr)
        return 2

    try:
        count, log = generate(args.src_pdf, args.issues_json, args.dst_xfdf)
    except ValueError as e:
        print(f"validation error: {e}", file=sys.stderr)
        return 3
    except XfdfReadbackError as e:
        print(f"readback error: {e}", file=sys.stderr)
        return 4
    except OSError as e:
        print(f"I/O error: {e}", file=sys.stderr)
        return 5

    print(f"[generate-xfdf] generated {count} annotations -> {args.dst_xfdf}")
    if log:
        for entry in log[:10]:
            print(f"  {entry}")
        if len(log) > 10:
            print(f"  ... ({len(log) - 10} more log entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
