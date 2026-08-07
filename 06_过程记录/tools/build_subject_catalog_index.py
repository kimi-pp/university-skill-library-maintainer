"""从本地本科专业目录读取快照生成分层 Markdown 索引，不进行外部调研。"""

from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = PROJECT_ROOT / "06_过程记录" / "2026-08-07-本科专业目录工作簿读取.json"
OUTPUT_ROOT = PROJECT_ROOT / "02_知识库" / "discipline_catalog"
CATEGORY_DIR = OUTPUT_ROOT / "categories"


data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
sheets = {sheet["name"]: sheet for sheet in data["sheets"]}
source_rows = sheets["本科专业目录"]["values"]
stats_rows = sheets["分类统计"]["values"]

expected_header = [
    "门类",
    "门类代码",
    "一级学科（学科大类）",
    "一级学科代码",
    "二级学科（专业名称）",
    "二级学科代码",
]
assert source_rows[0] == expected_header, "源表表头与预期不一致"

catalog: OrderedDict[str, dict] = OrderedDict()
current_category = None
current_category_code = None
current_group = None
current_group_code = None

for excel_row, row in enumerate(source_rows[1:], start=2):
    category, category_code, group, group_code, major, major_code = row
    if category:
        current_category = str(category).strip()
        current_category_code = str(category_code).strip()
        catalog.setdefault(
            current_category_code,
            {"name": current_category, "groups": OrderedDict()},
        )
    if group:
        current_group = str(group).strip()
        current_group_code = str(group_code).strip()
        assert current_category_code, f"第 {excel_row} 行一级学科缺少门类"
        catalog[current_category_code]["groups"].setdefault(
            current_group_code,
            {"name": current_group, "majors": []},
        )
    if major:
        assert current_category_code and current_group_code, f"第 {excel_row} 行专业缺少上级分类"
        catalog[current_category_code]["groups"][current_group_code]["majors"].append(
            {
                "name": str(major).strip(),
                "code": "" if major_code is None else str(major_code).strip(),
                "row": excel_row,
            }
        )


stats = OrderedDict()
for row in stats_rows[1:-1]:
    name, group_count, major_count = row
    stats[str(name)] = (int(group_count), int(major_count))

all_group_codes = []
all_major_codes = []
for category in catalog.values():
    all_group_codes.extend(category["groups"])
    for group in category["groups"].values():
        all_major_codes.extend(major["code"] for major in group["majors"])

assert len(catalog) == 13, f"明细表门类数异常：{len(catalog)}"
assert len(all_group_codes) == 103, f"明细表一级学科数异常：{len(all_group_codes)}"
assert len(all_major_codes) == 512, f"明细表专业数异常：{len(all_major_codes)}"
assert len(all_group_codes) == len(set(all_group_codes)), "一级学科代码重复"
nonempty_major_codes = [code for code in all_major_codes if code]
assert len(nonempty_major_codes) == len(set(nonempty_major_codes)), "非空专业代码重复"

reconciliation = []
for category_code, category in catalog.items():
    group_count = len(category["groups"])
    major_count = sum(len(group["majors"]) for group in category["groups"].values())
    stats_count = stats.get(category["name"])
    reconciliation.append(
        {
            "code": category_code,
            "name": category["name"],
            "detail_groups": group_count,
            "detail_majors": major_count,
            "stats_groups": stats_count[0] if stats_count else None,
            "stats_majors": stats_count[1] if stats_count else None,
        }
    )


CATEGORY_DIR.mkdir(parents=True, exist_ok=True)

index_lines = [
    "# 国内大学本科专业目录：学科分类索引",
    "",
    "> 本索引只结构化 `国内大学本科专业目录.xlsx` 内已有内容；未联网、未补充、未校订，也未启动任何 skill 调研。",
    "",
    "## 总览",
    "",
    "- 来源工作表：`本科专业目录`（A1:F513）、`分类统计`（A1:C14）",
    "- 层级：门类 → 一级学科（学科大类）→ 二级学科（专业名称）",
    "- 明细表实际数量：13 个门类、103 个一级学科、512 个专业",
    "- `分类统计` 页汇总口径：12 个门类、89 个一级学科、483 个专业",
    "- 差异：统计页未列军事学；教育学、理学的汇总数也少于明细表，详见下方核对表",
    "- 编码：按源文件原样保留，包括专业代码中的 `T`、`K` 等后缀",
    "- 空值：军事学 24 个专业在源表中的专业代码为空，索引以 `—` 表示",
    "",
    "## 门类入口",
    "",
    "| 门类代码 | 门类 | 明细一级学科数 | 明细专业数 | 详细索引 |",
    "|---|---|---:|---:|---|",
]

for category_code, category in catalog.items():
    group_count = len(category["groups"])
    major_count = sum(len(group["majors"]) for group in category["groups"].values())
    filename = f"{category_code}_{category['name']}.md"
    index_lines.append(
        f"| {category_code} | {category['name']} | {group_count} | {major_count} | [查看](categories/{filename}) |"
    )

index_lines.extend(
    [
        "",
        "## 与分类统计页核对",
        "",
        "| 门类 | 明细一级学科 | 统计页一级学科 | 明细专业 | 统计页专业 | 状态 |",
        "|---|---:|---:|---:|---:|---|",
    ]
)
for item in reconciliation:
    stats_groups = "未列入" if item["stats_groups"] is None else str(item["stats_groups"])
    stats_majors = "未列入" if item["stats_majors"] is None else str(item["stats_majors"])
    matched = (
        item["stats_groups"] == item["detail_groups"]
        and item["stats_majors"] == item["detail_majors"]
    )
    status = "一致" if matched else "存在差异"
    index_lines.append(
        f"| {item['name']} | {item['detail_groups']} | {stats_groups} | "
        f"{item['detail_majors']} | {stats_majors} | {status} |"
    )

index_lines.extend(
    [
        "",
        "## 使用说明",
        "",
        "- 需要按宽门类限定后续任务时，从上表进入对应门类文件。",
        "- 门类文件按源表顺序列出全部一级学科和专业，不做外部合并或重分类。",
        "- 每个专业保留源表 Excel 行号，便于回到原始文件核对。",
        "- [来源与处理方法](SOURCE_AND_METHOD.md)",
        "- [返回项目总索引](../../00_索引/INDEX.md)",
        "",
    ]
)
(OUTPUT_ROOT / "INDEX.md").write_text("\n".join(index_lines), encoding="utf-8")


for category_code, category in catalog.items():
    group_count = len(category["groups"])
    major_count = sum(len(group["majors"]) for group in category["groups"].values())
    stats_count = stats.get(category["name"])
    stats_note = (
        "未列入该门类"
        if stats_count is None
        else f"{stats_count[0]} 个一级学科、{stats_count[1]} 个专业"
    )
    lines = [
        f"# {category_code} {category['name']}",
        "",
        f"- 一级学科（学科大类）：{group_count} 个",
        f"- 二级学科（专业名称）：{major_count} 个",
        "- 来源：`国内大学本科专业目录.xlsx` → `本科专业目录` 工作表",
        "- 处理边界：原样索引，不进行外部调研或内容校订",
        f"- `分类统计` 页口径：{stats_note}",
        "",
    ]
    for group_code, group in category["groups"].items():
        lines.extend(
            [
                f"## {group_code} {group['name']}",
                "",
                f"专业数：{len(group['majors'])}",
                "",
                "| 专业代码 | 专业名称 | 源表位置 |",
                "|---|---|---|",
            ]
        )
        for major in group["majors"]:
            display_code = major["code"] or "—"
            lines.append(
                f"| {display_code} | {major['name']} | 本科专业目录!E{major['row']}:F{major['row']} |"
            )
        lines.append("")
    lines.extend(["[返回学科分类总索引](../INDEX.md)", ""])
    (CATEGORY_DIR / f"{category_code}_{category['name']}.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


method_lines = [
    "# 来源与处理方法",
    "",
    "## 来源",
    "",
    "- 文件：`D:\\高校AI工作台\\国内大学本科专业目录.xlsx`",
    "- 工作表 `本科专业目录`：A1:F513",
    "- 工作表 `分类统计`：A1:C14",
    "- 读取日期：2026-08-07",
    "",
    "## 处理方法",
    "",
    "1. 读取工作簿有效区域，不修改或重新导出源文件。",
    "2. 对源表因合并单元格产生的空白门类/一级学科值按最近非空上级值向下关联。",
    "3. 只在存在专业名称的行生成专业索引；空白分隔行不计入。",
    "4. 按源表顺序保留名称、代码和 Excel 行号。",
    "5. 将解析结果与 `分类统计` 工作表逐门类核对；差异原样记录，不用外部信息修正。",
    "",
    "## 完整性检查",
    "",
    "- 明细表：13 个门类、103 个一级学科、512 个专业。",
    "- 一级学科代码 103 个，均唯一。",
    "- 专业记录 512 个：488 个非空专业代码均唯一；军事学 24 个专业的代码单元格为空。",
    "- `分类统计` 页：12 个门类、89 个一级学科、483 个专业。",
    "- 差异集中在军事学（统计页未列）、教育学和理学（统计页数量少于明细）。",
    "",
    "## 边界",
    "",
    "本次工作不是政策或学科目录调研；未核实该文件的发布机构、版本年份、现行有效性或与其他目录的差异。",
    "",
    "[返回学科分类总索引](INDEX.md)",
    "",
]
(OUTPUT_ROOT / "SOURCE_AND_METHOD.md").write_text("\n".join(method_lines), encoding="utf-8")

print(
    f"categories={len(catalog)} groups={len(all_group_codes)} majors={len(all_major_codes)} "
    f"output={OUTPUT_ROOT}"
)
