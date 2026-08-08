#!/usr/bin/env python3
"""
annotate-pdf.py —— v2.0.0 主力 pdf 批注脚本

特性：
- 把批注直接嵌入原 pdf 副本（不生成 XFDF 旁路文件）
- 任何 pdf 阅读器（WPS / Chrome / 浏览器 / Adobe / Foxit / Preview）打开即见
- 自动定位：anchor_text 跨页搜索 → excerpt 搜索 → bbox 坐标 → 章节首段便签
- 回读验证：批注数 = 输入 issue 数（允许 bbox 失败降级为便签，不丢问题）

用法：
    python3 annotate-pdf.py <原.pdf> <issues.json> <输出.annotated.pdf>

依赖：
    PyMuPDF (pip install PyMuPDF)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError as e:
    print("error: PyMuPDF is required. Install with:", file=sys.stderr)
    print("  pip install --user PyMuPDF", file=sys.stderr)
    sys.exit(10)

# --------------------------------------------------------------------------- #
# 常量
# --------------------------------------------------------------------------- #

# 颜色：RGB 元组（PyMuPDF 使用 0-1 范围）
COLOR_MAP = {
    "fatal": (0.902, 0.298, 0.235),   # #E74C3C 红
    "major": (0.953, 0.612, 0.071),   # #F39C12 橙
    "minor": (0.945, 0.769, 0.059),   # #F1C40F 黄
}

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

AUTHOR = "张老师的AGENT"
VERSION = "2.7.0"

ENUM_SOURCE = {"thesis", "citation"}
ENUM_CATEGORY = set(CATEGORY_CN.keys())
ENUM_SEVERITY = set(SEVERITY_CN.keys())
ENUM_SCOPE = {"document", "chapter", "paragraph", "sentence", "span"}


def validate_issues_basic(data: dict) -> list[str]:
    """基本 schema 校验（v2 含 anchor_text 必填）。"""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top-level must be JSON object"]
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    issues = data.get("issues")
    if not isinstance(issues, list):
        return errors + ["issues must be an array"]

    for idx, it in enumerate(issues):
        if not isinstance(it, dict):
            errors.append(f"issues[{idx}]: must be object")
            continue
        for field in ("id", "source", "category", "severity", "scope",
                      "locator", "excerpt", "problem", "suggestion",
                      "group_id", "anchor_text"):
            if field not in it:
                errors.append(f"issues[{idx}]: missing '{field}'")
        if it.get("source") and it["source"] not in ENUM_SOURCE:
            errors.append(f"issues[{idx}].source: invalid")
        if it.get("category") and it["category"] not in ENUM_CATEGORY:
            errors.append(f"issues[{idx}].category: invalid")
        if it.get("severity") and it["severity"] not in ENUM_SEVERITY:
            errors.append(f"issues[{idx}].severity: invalid")
        if it.get("scope") and it["scope"] not in ENUM_SCOPE:
            errors.append(f"issues[{idx}].scope: invalid")
    return errors


# --------------------------------------------------------------------------- #
# 核心：批注正文渲染
# --------------------------------------------------------------------------- #

def render_annotation_body(issue: dict) -> str:
    """渲染批注正文（与 templates/annotation-body-template.md 一致）。"""
    cat_cn = CATEGORY_CN.get(issue.get("category", ""), issue.get("category", ""))
    sev_cn = SEVERITY_CN.get(issue.get("severity", ""), issue.get("severity", ""))
    problem = issue.get("problem", "")
    sugg = issue.get("suggestion", []) or [""]
    issue_id = issue.get("id", "")

    lines = [f"【{cat_cn}】【{sev_cn}】{problem}"]
    lines.append(f"→ {sugg[0]}")
    if len(sugg) > 1:
        lines.append("其他建议：")
        for s in sugg[1:]:
            lines.append(f"  · {s}")
    lines.append(f"[id: {issue_id}]")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# 定位：三级策略
# --------------------------------------------------------------------------- #

def _generate_space_tolerant_variants(text: str) -> list[str]:
    """v2.7: 为 anchor_text 生成空格容错变体。

    PDF 排版（特别是 LaTeX/Word 导出的 PDF）常在以下边界插入空格：
    - 中文与数字之间："第188条" → "第 188 条"
    - 中文与英文之间："法官Judge" → "法官 Judge"
    - 数字与单位之间："2017年" → "2017 年"

    PyMuPDF 的 search_for 是字符级严格匹配，遇到这类排版会搜不到。
    本函数生成在中文↔数字/字母边界插入空格的所有可能变体。
    """
    import re as _re
    if not text:
        return []
    # 用 sentinel 标出中文与数字/字母的边界
    # 模式 1: 中文后跟数字/字母 → 中文 + 空格 + 数字/字母
    pattern1 = _re.compile(r'([\u4e00-\u9fa5])([0-9A-Za-z])')
    # 模式 2: 数字/字母后跟中文 → 数字/字母 + 空格 + 中文
    pattern2 = _re.compile(r'([0-9A-Za-z])([\u4e00-\u9fa5])')

    variants = [text]
    v1 = pattern1.sub(r'\1 \2', text)
    if v1 != text:
        variants.append(v1)
    v2 = pattern2.sub(r'\1 \2', text)
    if v2 != text:
        variants.append(v2)
    v3 = pattern2.sub(r'\1 \2', pattern1.sub(r'\1 \2', text))
    if v3 != text and v3 not in variants:
        variants.append(v3)
    return variants


def _try_search_with_variants(page, text: str) -> list:
    """v2.7: 在指定页面搜索 text，依次尝试原文与空格容错变体。"""
    for variant in _generate_space_tolerant_variants(text):
        rects = page.search_for(variant)
        if rects:
            return rects
    return []


def search_near_page(
    doc, text: str, start_page: int, radius: int = 3
) -> tuple[int, object] | None:
    """在 start_page 附近 radius 页范围内搜索（v2.7 加空格容错）。"""
    if not text:
        return None
    query = text[:30]
    # 起始页优先
    if 0 <= start_page < doc.page_count:
        rects = _try_search_with_variants(doc[start_page], query)
        if rects:
            return (start_page, rects[0])
    # 向外扩散
    for offset in range(1, radius + 1):
        for p_idx in (start_page + offset, start_page - offset):
            if 0 <= p_idx < doc.page_count:
                rects = _try_search_with_variants(doc[p_idx], query)
                if rects:
                    return (p_idx, rects[0])
    return None


def search_fulltext(doc, text: str) -> tuple[int, object] | None:
    """在整本 pdf 搜索 text（v2.7 加空格容错），命中第一个返回 (page_idx, rect)。"""
    if not text:
        return None

    lengths_to_try = [len(text)]
    if len(text) > 20:
        lengths_to_try.append(20)
    if len(text) > 10:
        lengths_to_try.append(10)

    for L in lengths_to_try:
        query = text[:L]
        for page_idx in range(doc.page_count):
            rects = _try_search_with_variants(doc[page_idx], query)
            if rects:
                return (page_idx, rects[0])
    return None


def resolve_annotation_location(
    doc, issue: dict
) -> tuple[int, object, str]:
    """
    决定一条 issue 最终批注的 (page_idx, rect, strategy)。

    策略优先级：
    1. anchor_text 在起始页附近搜（最准）
    2. anchor_text 全文搜（页码不准时兜底）
    3. excerpt 全文搜
    4. bbox 坐标（issues.json 如有）
    5. 起始页左上便签（最终兜底）
    """
    loc = issue.get("locator", {})
    page_number = loc.get("page_number")
    n_pages = doc.page_count

    start_idx = (page_number - 1) if isinstance(page_number, int) and 1 <= page_number <= n_pages else 0

    anchor_text = issue.get("anchor_text", "") or ""
    excerpt = issue.get("excerpt", "") or ""

    # 策略 1/2: anchor_text
    if anchor_text and len(anchor_text.strip()) >= 2:
        hit = search_near_page(doc, anchor_text, start_idx, radius=3)
        if hit:
            return (hit[0], hit[1], "anchor-near")
        hit = search_fulltext(doc, anchor_text)
        if hit:
            return (hit[0], hit[1], "anchor-fulltext")

    # 策略 3: excerpt
    if excerpt and excerpt != anchor_text and len(excerpt.strip()) >= 2:
        hit = search_fulltext(doc, excerpt)
        if hit:
            return (hit[0], hit[1], "excerpt-fulltext")

    # 策略 4: bbox
    bbox = loc.get("bbox")
    if isinstance(bbox, list) and len(bbox) == 4:
        page = doc[start_idx]
        x0, y0, x1, y1 = bbox
        x0 = max(0.0, min(x0, page.rect.width))
        x1 = max(0.0, min(x1, page.rect.width))
        y0 = max(0.0, min(y0, page.rect.height))
        y1 = max(0.0, min(y1, page.rect.height))
        # bbox 约定 y 向上，转换到 PyMuPDF 的 y 向下
        rect = fitz.Rect(
            x0,
            page.rect.height - max(y0, y1),
            x1,
            page.rect.height - min(y0, y1),
        )
        return (start_idx, rect, "bbox")

    # 策略 5: 便签兜底
    return (start_idx, fitz.Rect(36, 36, 56, 56), "top-left-note")


# --------------------------------------------------------------------------- #
# 批注注入
# --------------------------------------------------------------------------- #

def annotate_pdf(
    src_pdf: Path,
    issues_json: Path,
    dst_pdf: Path,
    verbose: bool = False,
) -> tuple[int, list[str]]:
    data = json.loads(issues_json.read_text(encoding="utf-8"))

    # v2 校验
    errs = validate_issues_basic(data)
    if errs:
        raise ValueError("issues.json validation failed:\n" + "\n".join(errs[:10]))

    log: list[str] = []

    doc = fitz.open(src_pdf)
    mounted = 0
    strategy_count: dict[str, int] = {}

    for issue in data.get("issues", []):
        page_idx, rect, strategy = resolve_annotation_location(doc, issue)
        strategy_count[strategy] = strategy_count.get(strategy, 0) + 1
        page = doc[page_idx]
        severity = issue.get("severity", "minor")
        color = COLOR_MAP.get(severity, COLOR_MAP["minor"])
        body = render_annotation_body(issue)

        if strategy in ("anchor-near", "anchor-fulltext", "excerpt-fulltext", "bbox"):
            annot = page.add_highlight_annot(rect)
            annot.set_colors(stroke=color)
            annot.set_opacity(0.45)
        else:
            annot = page.add_text_annot(rect.tl, body, icon="Comment")
            annot.set_colors(stroke=color)

        info = annot.info
        info["title"] = AUTHOR
        info["content"] = body
        try:
            info["creationDate"] = fitz.get_pdf_now()
        except AttributeError:
            pass
        annot.set_info(info)
        annot.update()

        mounted += 1
        log.append(f"mounted: {issue.get('id', '?')} page={page_idx + 1} strategy={strategy}")

    doc.save(str(dst_pdf), garbage=4, deflate=True, clean=True)
    doc.close()

    log.append("---strategy-distribution---")
    for s, n in sorted(strategy_count.items()):
        log.append(f"  {s}: {n}")

    return mounted, log


def readback_verify(
    annotated_pdf: Path, expected_count: int
) -> tuple[bool, list[str]]:
    """回读验证：PyMuPDF 重新打开后批注数 == expected_count。"""
    errors: list[str] = []
    try:
        doc = fitz.open(annotated_pdf)
        total_annots = 0
        for page in doc:
            total_annots += len(list(page.annots()))
        doc.close()
    except Exception as e:
        return (False, [f"readback failed to open: {e}"])

    if total_annots != expected_count:
        errors.append(f"annotation count mismatch: expected {expected_count}, got {total_annots}")
    return (len(errors) == 0, errors)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        prog="annotate-pdf",
        description="Embed annotations directly into a pdf copy (v2.0.0).",
    )
    ap.add_argument("src_pdf", type=Path, help="source .pdf file (unmodified)")
    ap.add_argument("issues_json", type=Path, help="issues.json path")
    ap.add_argument("dst_pdf", type=Path, help="output .annotated.pdf path")
    ap.add_argument("-v", "--verbose", action="store_true", help="verbose log per issue")
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
        count, log = annotate_pdf(args.src_pdf, args.issues_json, args.dst_pdf, verbose=args.verbose)
    except ValueError as e:
        print(f"[annotate-pdf] validation error: {e}", file=sys.stderr)
        return 3
    except Exception as e:
        print(f"[annotate-pdf] error: {e}", file=sys.stderr)
        return 5

    print(f"[annotate-pdf] mounted {count} annotations -> {args.dst_pdf}")
    if args.verbose:
        for entry in log:
            print(f"  {entry}")
    else:
        # 只打印策略分布
        for entry in log[-10:]:
            if "---" in entry or entry.strip().startswith(("anchor-", "excerpt-", "bbox", "top-")):
                print(f"  {entry}")

    # 回读验证
    ok, errors = readback_verify(args.dst_pdf, count)
    if not ok:
        for e in errors:
            print(f"[annotate-pdf] readback error: {e}", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
