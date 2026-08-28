"""Chinese Word/Excel report builders and affected-scope selection."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any, Iterable, Mapping

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


DAILY_WORD_SECTIONS = (
    "本轮执行摘要",
    "专业目录变化",
    "四平台覆盖情况",
    "新增正式推荐",
    "已有 Skill 版本更新",
    "发现新版本但未升级",
    "条件候选",
    "需适配候选",
    "全局去重和来源别名",
    "受影响专业类",
    "排除原因汇总",
    "失败、覆盖降级和人工复核事项",
    "核验边界和未运行声明",
)

DAILY_SHEETS = (
    "使用说明",
    "执行概览",
    "目录变化",
    "新增正式推荐",
    "版本更新",
    "发现更新未升级",
    "条件候选",
    "需适配候选",
    "去重与来源别名",
    "受影响专业类",
    "排除原因汇总",
    "来源请求审计",
)

_REPORT_KEYS = {
    "catalog_changes": ("catalog_changes", "目录变化"),
    "formal_additions": ("formal_additions", "新增正式推荐", "正式推荐"),
    "version_updates": ("version_updates", "版本更新"),
    "updates_not_applied": ("updates_not_applied", "发现更新未升级"),
    "conditional_candidates": ("conditional_candidates", "条件候选"),
    "adaptation_candidates": ("adaptation_candidates", "需适配候选"),
    "aliases": ("aliases", "来源别名", "去重与来源别名"),
    "affected_scopes": ("affected_scopes", "受影响专业类"),
    "exclusions": ("exclusions", "排除项", "排除原因"),
    "manual_reviews": ("manual_reviews", "人工复核事项", "失败与人工复核"),
    "source_requests": ("source_requests", "来源请求审计"),
}

_MATERIAL_SKILL_FIELDS = (
    "入库层级",
    "固定版本",
    "固定版本内容指纹",
    "许可证",
    "安全等级",
    "安全限制条件",
    "外部依赖",
    "外部联网/API 调用",
    "远程服务端点",
    "本地专业软件或运行时依赖",
    "本地脚本/插件接口",
    "维护状态",
    "推荐优先级",
    "适配建议",
)


class ReportBuildError(RuntimeError):
    """A report could not be built with the approved portable runtime."""


def _plain_mapping(value: object) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return {str(key): item for key, item in value.items()}
    if is_dataclass(value):
        return asdict(value)
    if hasattr(value, "__dict__"):
        return {str(key): item for key, item in vars(value).items() if not key.startswith("_")}
    raise TypeError("报告摘要必须是 Mapping、dataclass 或带公开属性的对象")


def _json_value(value: object) -> object:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value):
        return {key: _json_value(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_json_value(item) for item in value]
    return value


def _rows(summary: Mapping[str, Any], canonical: str) -> list[dict[str, Any]]:
    for key in _REPORT_KEYS[canonical]:
        if key not in summary:
            continue
        value = summary[key]
        if value is None:
            return []
        if isinstance(value, Mapping):
            return [dict(value)]
        if isinstance(value, (str, Path)):
            return [{"名称": str(value)}]
        result = []
        for item in value:
            result.append(_plain_mapping(item) if not isinstance(item, str) else {"名称": item})
        return result
    return []


def _summary_payload(summary: object) -> dict[str, Any]:
    raw = _plain_mapping(summary)
    payload = {key: _rows(raw, key) for key in _REPORT_KEYS}
    scopes = []
    for item in payload["affected_scopes"]:
        scopes.append(str(item.get("专业类") or item.get("名称") or item.get("scope") or "").strip())
    payload["affected_scopes"] = [item for item in scopes if item]
    payload.update({
        "run_id": str(raw.get("run_id") or raw.get("运行标识") or "未提供"),
        "generated_at": _json_value(raw.get("generated_at") or raw.get("生成时间") or datetime.now()),
        "blocked": bool(raw.get("blocked", False)),
        "warnings": list(raw.get("warnings") or ()),
        "source_statuses": dict(raw.get("source_statuses") or raw.get("来源状态") or {}),
    })
    # Exclusion candidate names are deliberately never serialized into a deliverable.
    payload["exclusions"] = [
        {"原因": str(row.get("原因") or row.get("reason") or "未分类原因").strip() or "未分类原因"}
        for row in payload["exclusions"]
    ]
    return _json_value(payload)  # type: ignore[return-value]


def _set_run_font(run, *, size: float = 11, bold: bool | None = None, color: str | None = None) -> None:
    run.font.name = "Calibri"
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), "Calibri")
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), "Calibri")
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "Calibri")
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color.lstrip("#"))


def _configure_styles(document: Document) -> None:
    normal = document.styles["Normal"]
    normal.font.name = "Calibri"
    normal._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), "Calibri")
    normal._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), "Calibri")
    normal._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "Calibri")
    normal.font.size = Pt(11)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.10
    for name, size, color, before, after in (
        ("Heading 1", 16, "2E74B5", 16, 8),
        ("Heading 2", 13, "2E74B5", 12, 6),
        ("Heading 3", 12, "1F4D78", 8, 4),
    ):
        style = document.styles[name]
        style.font.name = "Calibri"
        style._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), "Calibri")
        style._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), "Calibri")
        style._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "Calibri")
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor.from_string(color)
        style.font.bold = True
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True


def _add_heading_numbering(document: Document) -> int:
    numbering = document.part.numbering_part.element
    abstract_ids = [int(item.get(qn("w:abstractNumId"))) for item in numbering.findall(qn("w:abstractNum"))]
    num_ids = [int(item.get(qn("w:numId"))) for item in numbering.findall(qn("w:num"))]
    abstract_id = max(abstract_ids, default=-1) + 1
    num_id = max(num_ids, default=0) + 1
    abstract = OxmlElement("w:abstractNum")
    abstract.set(qn("w:abstractNumId"), str(abstract_id))
    multi = OxmlElement("w:multiLevelType")
    multi.set(qn("w:val"), "singleLevel")
    abstract.append(multi)
    level = OxmlElement("w:lvl")
    level.set(qn("w:ilvl"), "0")
    start = OxmlElement("w:start")
    start.set(qn("w:val"), "1")
    num_fmt = OxmlElement("w:numFmt")
    num_fmt.set(qn("w:val"), "decimal")
    lvl_text = OxmlElement("w:lvlText")
    lvl_text.set(qn("w:val"), "%1.")
    suffix = OxmlElement("w:suff")
    suffix.set(qn("w:val"), "space")
    paragraph_props = OxmlElement("w:pPr")
    tabs = OxmlElement("w:tabs")
    tab = OxmlElement("w:tab")
    tab.set(qn("w:val"), "num")
    tab.set(qn("w:pos"), "360")
    tabs.append(tab)
    indent = OxmlElement("w:ind")
    indent.set(qn("w:left"), "360")
    indent.set(qn("w:hanging"), "360")
    paragraph_props.extend((tabs, indent))
    level.extend((start, num_fmt, lvl_text, suffix, paragraph_props))
    abstract.append(level)
    numbering.append(abstract)
    num = OxmlElement("w:num")
    num.set(qn("w:numId"), str(num_id))
    abstract_ref = OxmlElement("w:abstractNumId")
    abstract_ref.set(qn("w:val"), str(abstract_id))
    num.append(abstract_ref)
    numbering.append(num)
    return num_id


def _number_heading(paragraph, num_id: int) -> None:
    ppr = paragraph._p.get_or_add_pPr()
    num_pr = ppr.find(qn("w:numPr"))
    if num_pr is None:
        num_pr = OxmlElement("w:numPr")
        ppr.append(num_pr)
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    num_ref = OxmlElement("w:numId")
    num_ref.set(qn("w:val"), str(num_id))
    num_pr.extend((ilvl, num_ref))


def _set_cell_margins(cell) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    margins = tc_pr.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        tc_pr.append(margins)
    for edge, value in (("top", 80), ("bottom", 80), ("start", 120), ("end", 120)):
        node = margins.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            margins.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def _set_table_geometry(table, widths: tuple[int, ...]) -> None:
    if sum(widths) != 9360:
        raise ValueError("Word 表格列宽必须合计 9360 DXA")
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl_pr = table._tbl.tblPr
    width = tbl_pr.first_child_found_in("w:tblW")
    if width is None:
        width = OxmlElement("w:tblW")
        tbl_pr.append(width)
    width.set(qn("w:w"), "9360")
    width.set(qn("w:type"), "dxa")
    indent = tbl_pr.first_child_found_in("w:tblInd")
    if indent is None:
        indent = OxmlElement("w:tblInd")
        tbl_pr.append(indent)
    indent.set(qn("w:w"), "120")
    indent.set(qn("w:type"), "dxa")
    layout = tbl_pr.first_child_found_in("w:tblLayout")
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tbl_pr.append(layout)
    layout.set(qn("w:type"), "fixed")
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for item in widths:
        column = OxmlElement("w:gridCol")
        column.set(qn("w:w"), str(item))
        grid.append(column)
    for row in table.rows:
        for index, cell in enumerate(row.cells):
            cell.width = Inches(widths[index] / 1440)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tc_width = cell._tc.get_or_add_tcPr().first_child_found_in("w:tcW")
            tc_width.set(qn("w:w"), str(widths[index]))
            tc_width.set(qn("w:type"), "dxa")
            _set_cell_margins(cell)
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_before = Pt(0)
                paragraph.paragraph_format.space_after = Pt(0)
                paragraph.paragraph_format.line_spacing = 1.10
                for run in paragraph.runs:
                    _set_run_font(run)


def _shade(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shading = tc_pr.first_child_found_in("w:shd")
    if shading is None:
        shading = OxmlElement("w:shd")
        tc_pr.append(shading)
    shading.set(qn("w:fill"), fill)


def _add_field(paragraph, instruction: str, placeholder: str) -> None:
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    text = OxmlElement("w:instrText")
    text.set(qn("xml:space"), "preserve")
    text.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    run_text = OxmlElement("w:t")
    run_text.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run = paragraph.add_run()._r
    run.extend((begin, text, separate, run_text, end))


def _metadata_table(document: Document, payload: Mapping[str, Any]) -> None:
    table = document.add_table(rows=4, cols=2)
    rows = (
        ("运行标识", str(payload["run_id"])),
        ("生成时间", str(payload["generated_at"])),
        ("报告口径", "正式推荐、条件候选、需适配候选分别统计"),
        ("核验方式", "静态证据审阅；候选未安装、未运行"),
    )
    for row, (label, value) in zip(table.rows, rows):
        row.cells[0].text = label
        row.cells[1].text = value
        _shade(row.cells[0], "F2F4F7")
        for run in row.cells[0].paragraphs[0].runs:
            _set_run_font(run, bold=True)
    _set_table_geometry(table, (2700, 6660))


def _add_detail_table(document: Document, rows: Iterable[tuple[str, object]]) -> None:
    values = tuple(rows)
    table = document.add_table(rows=max(1, len(values)), cols=2)
    for row, (label, value) in zip(table.rows, values):
        row.cells[0].text = str(label)
        row.cells[1].text = str(value or "未提供")
        _shade(row.cells[0], "F2F4F7")
        for run in row.cells[0].paragraphs[0].runs:
            _set_run_font(run, bold=True)
    _set_table_geometry(table, (2700, 6660))


def _display_name(row: Mapping[str, Any]) -> str:
    return str(row.get("规范名称") or row.get("Skill名称") or row.get("候选名称") or row.get("内部标识") or "未命名项")


def _add_skill_items(document: Document, rows: list[dict[str, Any]]) -> None:
    if not rows:
        document.add_paragraph("本轮无相关记录。")
        return
    for row in rows:
        heading = document.add_paragraph(style="Heading 2")
        heading.add_run(_display_name(row))
        _add_detail_table(document, (
            ("稳定 ID", row.get("内部标识") or "未分配"),
            ("英文原名", row.get("规范名称") or row.get("Skill名称") or "未提供"),
            ("用途", row.get("用途") or row.get("简要功能") or row.get("详细功能摘要") or "未提供"),
            ("适用人员", row.get("适用人员") or row.get("适用用户角色") or "未提供"),
            ("输入", row.get("输入") or "未提供"),
            ("输出", row.get("输出") or "未提供"),
            ("限制", row.get("使用限制") or row.get("安全限制条件") or row.get("适配建议") or "未提供"),
            ("固定版本", row.get("固定版本") or row.get("新版本") or row.get("发现版本") or "未提供"),
            ("许可证", row.get("许可证") or "未提供"),
            ("URL", row.get("Canonical source") or row.get("来源地址") or row.get("发现地址") or "未提供"),
        ))


def build_daily_docx(summary: object, output: str | Path) -> Path:
    """Build the fixed-order Chinese daily Word report with deterministic geometry."""

    payload = _summary_payload(summary)
    destination = Path(output).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    document = Document()
    section = document.sections[0]
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = section.right_margin = section.bottom_margin = section.left_margin = Inches(1)
    section.header_distance = section.footer_distance = Inches(0.492)
    _configure_styles(document)
    heading_num_id = _add_heading_numbering(document)

    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.LEFT
    header.paragraph_format.space_after = Pt(0)
    _set_run_font(header.add_run("高校专业 Skill 库｜自动维护日报"), size=9, color="667085")
    _set_run_font(header.add_run(f"    {payload['run_id']}"), size=9, color="667085")
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _set_run_font(footer.add_run("第 "), size=9, color="667085")
    _add_field(footer, " PAGE ", "1")
    _set_run_font(footer.add_run(" 页"), size=9, color="667085")

    title = document.add_paragraph()
    title.paragraph_format.space_before = Pt(16)
    title.paragraph_format.space_after = Pt(4)
    _set_run_font(title.add_run("高校专业 Skill 库自动查验报告"), size=23, bold=True)
    subtitle = document.add_paragraph()
    subtitle.paragraph_format.space_after = Pt(16)
    _set_run_font(subtitle.add_run("每日维护摘要与人工复核边界"), size=14, color="373737")
    _metadata_table(document, payload)

    formal = payload["formal_additions"]
    conditional = payload["conditional_candidates"]
    adaptation = payload["adaptation_candidates"]
    sections: dict[str, Any] = {
        "本轮执行摘要": lambda: _add_detail_table(document, (
            ("运行状态", "阻断" if payload["blocked"] else "完成"),
            ("新增正式推荐", len(formal)),
            ("条件候选", len(conditional)),
            ("需适配候选", len(adaptation)),
            ("受影响专业类", len(payload["affected_scopes"])),
        )),
        "专业目录变化": lambda: _add_generic_rows(document, payload["catalog_changes"]),
        "四平台覆盖情况": lambda: _add_source_statuses(document, payload["source_statuses"]),
        "新增正式推荐": lambda: _add_skill_items(document, formal),
        "已有 Skill 版本更新": lambda: _add_skill_items(document, payload["version_updates"]),
        "发现新版本但未升级": lambda: _add_skill_items(document, payload["updates_not_applied"]),
        "条件候选": lambda: _add_skill_items(document, conditional),
        "需适配候选": lambda: _add_skill_items(document, adaptation),
        "全局去重和来源别名": lambda: _add_generic_rows(document, payload["aliases"]),
        "受影响专业类": lambda: _add_scope_rows(document, payload["affected_scopes"]),
        "排除原因汇总": lambda: _add_exclusion_summary(document, payload["exclusions"]),
        "失败、覆盖降级和人工复核事项": lambda: _add_manual_items(document, payload),
        "核验边界和未运行声明": lambda: document.add_paragraph(
            "本报告仅依据固定版本、来源快照、许可证与静态安全证据进行查验。候选 Skill 未安装、未运行；"
            "未调用候选自身外部服务，也未上传真实教学或科研数据。正式采用前仍须由责任人复核许可证、依赖和数据边界。"
        ),
    }
    for name in DAILY_WORD_SECTIONS:
        heading = document.add_paragraph(name, style="Heading 1")
        _number_heading(heading, heading_num_id)
        sections[name]()
    document.save(destination)
    return destination


def _add_generic_rows(document: Document, rows: list[dict[str, Any]]) -> None:
    if not rows:
        document.add_paragraph("本轮无相关记录。")
        return
    for row in rows:
        fields = [(key, value) for key, value in row.items() if value not in (None, "")]
        _add_detail_table(document, fields or (("说明", "已记录"),))


def _add_source_statuses(document: Document, statuses: Mapping[str, Any]) -> None:
    ordered = ("SkillHub", "ClawHub", "GitHub", "Hugging Face Spaces")
    _add_detail_table(document, ((platform, statuses.get(platform, "未请求")) for platform in ordered))


def _add_scope_rows(document: Document, scopes: list[str]) -> None:
    if scopes:
        _add_detail_table(document, (("专业类", scope) for scope in scopes))
    else:
        document.add_paragraph("本轮无受影响专业类；既有专业类交付不重写。")


def _add_exclusion_summary(document: Document, exclusions: list[dict[str, Any]]) -> None:
    counts = Counter(str(row.get("原因") or "未分类原因") for row in exclusions)
    if counts:
        _add_detail_table(document, ((reason, count) for reason, count in sorted(counts.items())))
    else:
        document.add_paragraph("本轮无排除原因记录。为保护审查边界，本节只汇总原因和数量，不列排除项名称。")


def _add_manual_items(document: Document, payload: Mapping[str, Any]) -> None:
    items = list(payload["manual_reviews"])
    items.extend({"事项": warning} for warning in payload.get("warnings", ()))
    for platform, status in payload["source_statuses"].items():
        if str(status).lower() not in {"complete", "success", "ok", "成功", "完整"}:
            items.append({"事项": f"{platform} 覆盖状态为 {status}，需保留降级说明。"})
    _add_generic_rows(document, items)


def _require_runtime_path(variable: str, *, directory: bool) -> Path:
    raw = os.environ.get(variable, "").strip()
    if not raw:
        raise ReportBuildError(f"缺少环境变量 {variable}；无法使用批准的可移植 Node 运行时")
    path = Path(raw)
    valid = path.is_dir() if directory else path.is_file()
    if not valid:
        kind = "目录" if directory else "文件"
        raise ReportBuildError(f"环境变量 {variable} 指向的{kind}不存在：{path}")
    return path


def _make_node_modules_link(link: Path, target: Path) -> None:
    if os.name == "nt":
        result = subprocess.run(
            ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode:
            raise ReportBuildError(f"无法创建临时 node_modules junction：{result.stderr or result.stdout}")
    else:
        link.symlink_to(target, target_is_directory=True)


def _remove_node_modules_link(link: Path) -> None:
    if not link.exists() and not link.is_symlink():
        return
    if os.name == "nt":
        os.rmdir(link)
    else:
        link.unlink()


def _run_xlsx_builder(payload: Mapping[str, Any], destination: Path, *, verify_dir: Path | None = None) -> None:
    node = _require_runtime_path("SKILL_MAINTAINER_NODE", directory=False)
    modules = _require_runtime_path("SKILL_MAINTAINER_NODE_MODULES", directory=True)
    if not (modules / "@oai" / "artifact-tool").is_dir():
        raise ReportBuildError("SKILL_MAINTAINER_NODE_MODULES 中缺少 @oai/artifact-tool")
    source_builder = Path(__file__).with_name("daily_xlsx_builder.mjs")
    if not source_builder.is_file():
        raise ReportBuildError(f"缺少 Excel 生成器：{source_builder.name}")
    with tempfile.TemporaryDirectory(prefix="skill-maintainer-report-") as raw_temp:
        work = Path(raw_temp)
        link = work / "node_modules"
        _make_node_modules_link(link, modules)
        try:
            builder = work / source_builder.name
            request = work / "report-input.json"
            shutil.copyfile(source_builder, builder)
            request.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            command = [str(node), str(builder), str(request), str(destination)]
            if verify_dir is not None:
                command.extend(("--verify-dir", str(verify_dir)))
            result = subprocess.run(
                command,
                cwd=work,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            if result.returncode:
                detail = (result.stderr or result.stdout or "无错误输出").strip()
                raise ReportBuildError(f"artifact-tool Excel 生成失败（退出码 {result.returncode}）：{detail}")
        finally:
            _remove_node_modules_link(link)


def build_daily_xlsx(summary: object, output: str | Path) -> Path:
    """Build the 12-sheet daily workbook exclusively through artifact-tool."""

    destination = Path(output).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    _run_xlsx_builder(_summary_payload(summary), destination)
    return destination


def _ledger_rows(ledger: object, sheet: str) -> list[dict[str, Any]]:
    if hasattr(ledger, "rows") and callable(getattr(ledger, "rows")):
        return [dict(row) for row in ledger.rows(sheet)]
    mapping = _plain_mapping(ledger)
    value = mapping.get(sheet, ())
    return [_plain_mapping(row) for row in value]


def _scope_name(row: Mapping[str, Any]) -> str:
    direct = str(row.get("专业类") or row.get("scope") or "").strip()
    if direct:
        return direct
    code = str(row.get("专业代码") or "").strip()
    name = str(row.get("专业名称") or "").strip()
    return " ".join(item for item in (code, name) if item)


def _scope_index(snapshot: object) -> tuple[dict[str, set[str]], dict[str, dict[str, Any]], dict[str, tuple[tuple[str, str], ...]]]:
    skills = {
        str(row.get("内部标识") or "").strip(): row
        for row in _ledger_rows(snapshot, "当前Skill")
        if str(row.get("内部标识") or "").strip()
    }
    scopes: dict[str, set[str]] = {}
    mapping_fingerprints: dict[str, list[tuple[str, str]]] = {}
    for row in _ledger_rows(snapshot, "专业任务映射"):
        stable_id = str(row.get("内部标识") or "").strip()
        scope = _scope_name(row)
        if not stable_id or not scope:
            continue
        scopes.setdefault(stable_id, set()).add(scope)
        material = tuple(sorted(
            (str(key), str(value)) for key, value in row.items()
            if key not in {"映射标识", "mapping_id"} and value not in (None, "")
        ))
        mapping_fingerprints.setdefault(stable_id, []).append((scope, repr(material)))
    for stable_id, row in skills.items():
        scope = _scope_name(row)
        if scope:
            scopes.setdefault(stable_id, set()).add(scope)
    frozen = {key: tuple(sorted(value)) for key, value in mapping_fingerprints.items()}
    return scopes, skills, frozen


def affected_scopes(before: object, after: object) -> tuple[str, ...]:
    """Return only scopes whose formal content or catalog boundary materially changed."""

    before_scopes, before_skills, before_maps = _scope_index(before)
    after_scopes, after_skills, after_maps = _scope_index(after)
    affected: set[str] = set()
    for stable_id in sorted(set(before_skills) | set(after_skills)):
        old = before_skills.get(stable_id)
        new = after_skills.get(stable_id)
        old_scopes = before_scopes.get(stable_id, set())
        new_scopes = after_scopes.get(stable_id, set())
        if old is None or new is None:
            affected.update(old_scopes | new_scopes)
            continue
        old_material = tuple(str(old.get(field) or "") for field in _MATERIAL_SKILL_FIELDS)
        new_material = tuple(str(new.get(field) or "") for field in _MATERIAL_SKILL_FIELDS)
        if old_material != new_material or before_maps.get(stable_id, ()) != after_maps.get(stable_id, ()):
            affected.update(old_scopes | new_scopes)
    before_catalog = _ledger_rows(before, "目录基线")
    after_catalog = _ledger_rows(after, "目录基线")
    if before_catalog != after_catalog:
        catalog_scopes = {_scope_name(row) for row in before_catalog + after_catalog if _scope_name(row)}
        affected.update(catalog_scopes or {scope for values in before_scopes.values() for scope in values} | {scope for values in after_scopes.values() for scope in values})
    return tuple(sorted(scope for scope in affected if scope))


def _safe_scope_name(scope: str) -> str:
    value = re.sub(r"[<>:\"/\\|?*\x00-\x1f]", "_", scope).strip(" .")
    if not value or value in {".", ".."}:
        raise ValueError("专业类名称不能安全地用作交付目录")
    return value


def build_scope_deliveries(
    scopes: Iterable[str],
    ledger: object,
    output_root: str | Path,
) -> tuple[Path, ...]:
    """Build one Word and one Excel copy for each materially affected scope."""

    master_rows = _ledger_rows(ledger, "当前Skill")
    mappings = _ledger_rows(ledger, "专业任务映射")
    by_id = {str(row.get("内部标识") or "").strip(): row for row in master_rows if str(row.get("内部标识") or "").strip()}
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    seen_scopes: set[str] = set()
    for raw_scope in scopes:
        scope = str(raw_scope).strip()
        if not scope or scope in seen_scopes:
            continue
        seen_scopes.add(scope)
        scope_maps = [row for row in mappings if _scope_name(row) == scope]
        ids = sorted({str(row.get("内部标识") or "").strip() for row in scope_maps if str(row.get("内部标识") or "").strip()})
        formal: list[dict[str, Any]] = []
        for stable_id in ids:
            if stable_id not in by_id:
                continue
            row = dict(by_id[stable_id])
            mapping = next(item for item in scope_maps if str(item.get("内部标识") or "").strip() == stable_id)
            row.update({
                "专业类": scope,
                "用途": mapping.get("专业任务") or row.get("简要功能"),
                "输入": mapping.get("输入") or row.get("输入"),
                "输出": mapping.get("输出") or row.get("输出"),
                "使用限制": mapping.get("使用限制") or row.get("安全限制条件"),
            })
            formal.append(row)
        payload = {
            "run_id": f"scope-{_safe_scope_name(scope)}",
            "generated_at": datetime.now(),
            "formal_additions": formal,
            "affected_scopes": [scope],
            "source_statuses": {},
        }
        directory = root / _safe_scope_name(scope)
        directory.mkdir(parents=True, exist_ok=True)
        docx_path = directory / "专业类Skill清单.docx"
        xlsx_path = directory / "专业类Skill清单.xlsx"
        build_daily_docx(payload, docx_path)
        build_daily_xlsx(payload, xlsx_path)
        outputs.extend((docx_path, xlsx_path))
    return tuple(outputs)
