# Task 10 实施报告：中文 Word/Excel 日报与受影响专业类交付

## 交付

- `reports.py`：实现 `build_daily_docx(summary, output)`、`build_daily_xlsx(summary, output)`、`affected_scopes(before, after)` 与 `build_scope_deliveries(scopes, ledger, output_root)`。
- `daily_xlsx_builder.mjs`：唯一 artifact-tool 工作簿生成器；Python API 仅通过环境变量解析批准的 Node 和 `node_modules`，在可写临时目录建立 `node_modules` junction 后调用，不嵌入用户目录、全局缓存或仓库本地依赖路径。
- `daily_report.docx`：`standard_business_brief` + `memo_masthead` 模板；无装饰性底线。
- `daily_review.xlsx`：12 工作表可复读模板。
- `test_reports.py`：5 个报告、520 行、范围变化、专业类复用与模板复读测试。

所有 QA 报告、专业类样例和渲染图片只写入 `.superpowers/staging/task10-*`；未写正式交付目录，未建立数据库，未安装或运行候选 Skill。

## TDD：RED / GREEN

### 初始 RED

命令：

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_reports.py -v
```

结果：`FAILED (errors=1)`；测试模块因 `ModuleNotFoundError: No module named 'skill_maintainer.reports'` 无法导入，失败原因正是四个待实现接口缺失。

### 迭代 RED

1. artifact-tool 初次导出的 12 张表没有持久化 `freezeRows(1)`；`openpyxl` 只读复读得到 `freeze_panes=None`，测试要求 `A2`。
2. 逐表 PNG 检查发现 artifact-tool 渲染器把 `HYPERLINK()` 显示为 `HYPERLINK is not implemented`；测试改为要求纯 URL 单元格和真实 external hyperlink relationship 后按预期失败。
3. 逐表 PNG 检查发现无时区的 `2026-08-28T22:00:00` 被显示为 `14:00`；新增墙上时间复读断言后按预期失败。

### 最终 GREEN

- 聚焦：`python -m unittest 07_自动维护工作流/tests/test_reports.py -v` → `Ran 5 tests in 35.793s`，`OK`。
- 完整工作流：`python -m unittest discover -s 07_自动维护工作流/tests -v` → `Ran 168 tests in 54.759s`，`OK`。
- 520 行测试复读 `新增正式推荐!A521=GH-05-0520`，稳定 ID 唯一数 520；表范围到第 521 行，概览复核公式引用到第 521 行。
- 12 张表均复读到 `freeze_panes=A2`、一个动态表对象、筛选按钮、换行和指定列宽；URL 单元格是纯 URL 且存在真正的外部超链接关系；日期格式为 `yyyy-mm-dd`，运行时间复读为 `2026-08-28 22:00`。
- `affected_scopes` 覆盖新增正式项、正式版本、许可证、安全、专业任务映射和目录变化；仅增加来源别名返回空元组。跨专业共用 Skill 在每个专业类文件中只出现一次且保持同一稳定 ID。

## DOCX 设计与结构 QA

- Letter portrait；四边 1 in；页眉/页脚距离 0.492 in；Calibri 11 pt；正文 after 6 pt / 1.10。
- Heading 1：16 pt、`#2E74B5`、before 16 / after 8；Heading 2：13 pt、before 12 / after 6；Heading 3：12 pt、`#1F4D78`、before 8 / after 4。
- 13 个固定一级标题全部是 Word Heading 1，并绑定真实 decimal numbering；样例内 3 个 Skill 标题是 Heading 2，无标题层级跳跃。
- `table_geometry.py` 检查样例 10 张表：全部 `tblW=9360`、`tblInd=120`、`tblGrid=9360`、每行 `tcW` 合计 9360；单元格 margins 为 top/bottom 80、start/end 120；标签填充 `F2F4F7`。
- `section_audit.py`：1 个 section，8.50 × 11.00 in、portrait、四边 1.00 in；页眉和页脚未错误链接到前一节。
- 内容测试确认 13 节顺序、中文用途/适用人员/输入/输出/限制、英文原名、URL、许可证与“未安装、未运行”；排除项名称未进入正文或表格。

### DOCX 页数与逐页检查

| 文件 | 页数 | PNG | 逐页结论 |
|---|---:|---:|---|
| `.superpowers/staging/task10-qa/daily-report-qa.docx` | 不可得 | 0 | 未完成视觉检查；只完成上述结构 QA。 |
| `07_自动维护工作流/templates/daily_report.docx` | 不可得 | 0 | 未完成视觉检查；模板结构由同一生成器和聚焦测试覆盖。 |

精确阻断：批准的 Python 调用技能 `render_docx.py ... --emit_pdf` 时，在 `convert_to_pdf → subprocess.run` 抛出 `FileNotFoundError: [WinError 2]`；当前环境没有可调用的 LibreOffice/`soffice`。因此本报告不宣称 DOCX 视觉门通过，Task 11 的 Microsoft Word 实际打开/渲染仍是正式发布前的强制门。

## Excel artifact-tool 验证

artifact-tool 在新建工作簿和导出后重导入两个阶段均运行：

```text
searchTerm: #REF!|#DIV/0!|#VALUE!|#NAME\?|#N/A
result: Cell search matched 0 entries.
```

模板 `daily_review.xlsx` 通过 artifact-tool 重新导入，返回恰好 12 张规定工作表；`使用说明!A1:B7` 可复读且公式错误扫描为 0。520 行 QA 工作簿重导入时，`新增正式推荐` used range 为 `A1:N521`。

### 12-sheet 渲染清单

最终 520 行 QA 工作簿通过 artifact-tool 重导入后渲染；全部 PNG 已实际打开检查。超链接修复后再次渲染，URL 显示为纯地址而非公式实现提示；时间修复后“执行概览”显示 `2026-08-28 22:00`。

| # | 工作表 | PNG 字节 | 视觉检查 |
|---:|---|---:|---|
| 01 | 使用说明 | 45,487 | 通过 |
| 02 | 执行概览 | 24,892 | 通过；520 行复核=520，时间=22:00 |
| 03 | 目录变化 | 3,687 | 通过；空数据时保留清晰表头 |
| 04 | 新增正式推荐 | 11,636,045 | 通过；完整渲染 520 行 |
| 05 | 版本更新 | 39,174 | 通过 |
| 06 | 发现更新未升级 | 39,193 | 通过 |
| 07 | 条件候选 | 39,317 | 通过 |
| 08 | 需适配候选 | 39,276 | 通过 |
| 09 | 去重与来源别名 | 15,559 | 通过；纯 URL 显示 |
| 10 | 受影响专业类 | 9,530 | 通过 |
| 11 | 排除原因汇总 | 5,307 | 通过；只含原因和数量 |
| 12 | 来源请求审计 | 10,927 | 通过；纯 URL 显示 |

## artifact-tool 兼容补丁与已知顾虑

- artifact-tool 2.8.6 暴露 `freezePanes.freezeRows(1)`，但导出的 XLSX 丢失 `<pane>`；其渲染器还把帮助文档列出的 `HYPERLINK()` 公式显示为实现提示。控制器明确允许后，唯一 JS builder 在 artifact-tool 完成全部值、公式、样式、表格和 XLSX 导出后，只对 12 个 worksheet 的 `sheetView` 和 URL 的 external hyperlink relationships 做确定性 ZIP/OOXML 后处理。没有使用 `openpyxl`、`xlsxwriter` 或 `pandas.ExcelWriter` 写报告；测试通过保存后复读锁定补丁结果。
- DOCX 因缺少 `soffice` 没有页数、PDF 或逐页 PNG 证据，不能视为视觉发布通过；已完成结构 QA，并保留 Task 11 Office 门。
- 520 行全表渲染产生约 11.6 MB 的纵向 PNG，生成和打开均成功，但正式使用时仍应由 Task 11 在 Microsoft Excel 中实际打开关键表和末行单元格。
