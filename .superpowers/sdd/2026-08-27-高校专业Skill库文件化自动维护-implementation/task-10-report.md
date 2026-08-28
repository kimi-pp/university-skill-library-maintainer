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

## Fix round 1：真实运行接线、安全边界与脱敏

### 复审核实与 TDD RED

复审意见与代码现状一致：`RunSummary` 不含报告所需的台账明细，Task 9 回调实际接收的是 `PreparedRun` 和本轮 staging root；旧实现没有可供 `RunCoordinator` 注入的真实适配器。其余问题也由现有实现直接复现：安全结论字段未进入 scope 指纹、目录访问日期制造噪声、文件名清洗碰撞、父链 reparse 未拒绝、多任务映射只取首条、测试写死用户缓存、`cmd.exe /c mklink` 经过 shell、排除原因自由文本原样输出。

先只修改 `test_reports.py` 和 `test_runner.py`，使用调用环境提供的 Node/runtime，运行：

```powershell
$env:PYTHONPATH = (Resolve-Path 'src')
$env:SKILL_MAINTAINER_NODE = 'C:\Users\34927\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
$env:SKILL_MAINTAINER_NODE_MODULES = 'C:\Users\34927\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules'
python -m unittest -v tests.test_reports tests.test_runner.RunnerTestCase.test_real_report_adapter_uses_prepared_catalog_sources_and_both_ledgers_in_staging
```

首轮 RED 的首错是 `验证状态` 变化时 `affected_scopes` 实际返回 `()`、期望 `('0801 力学类',)`；同一测试的 `风险提示` 子用例也失败。后续同轮输出还确认：仅 `访问日期` 变化误刷新、`affected_scopes` 不接受 `catalog_snapshot`、未知排除自由文本泄漏、runtime reparse/错误 executable 未归一化拒绝、真实 report-builder adapter 缺失。每一项均因待实现行为缺失而失败。

强化真实集成 fixture 时曾观察到 `新增正式推荐!A2=None`；核查 Task 7 契约后确认测试决定未提供 `DerivedFields.ledger_row`，因此它本来就不会向 staged ledger 写正式项。fixture 改为完整、内容绑定的真实审查决定后，适配器测试同时证明 production/staged ledger 差异进入日报；没有为错误 fixture 修改生产行为。

### 最小实现

- `PreparedRun` 保存 prepare 阶段已经取摘要并受 digest 约束的 `catalog_snapshot`。新增 `make_project_report_builder(root)`，绑定 `ProjectPaths`；它读取正式台账与 `prepared.staging_ledger`，使用 `prepared.source_runs` 和真实 `Catalog.staged_diff` 构造日报输入，只在 `prepared.staging_dir/deliveries` 写日报和受影响专业类交付。
- `affected_scopes` 纳入验证级别/状态、风险提示、可执行/网络数据/凭据/文件行为、质量评分和实施准备度；`访问日期` 从目录基线实质指纹排除；真实 catalog 逐记录 added/removed/renamed/code/move 差异精确映射到专业类。
- 专业类目录名使用“安全可读前缀 + 原 scope SHA-256 前 10 位”，避免 `A/B` 与 `A:B` 覆盖。写入前检查 output root 全父链及子目录均为 ordinary path，拒绝 symlink/junction/reparse；真实 adapter 只传 staging 内根目录。
- 同一稳定 ID 的多条专业任务映射在用途、输入、输出和使用限制四个维度稳定去重、排序并聚合；Master Skill 仍只输出一行。
- Node 与 `node_modules` 完全取自调用环境；测试不再覆盖调用者已有配置。生产验证普通路径/reparse、`node.exe` 名称及真实 `--version` 身份、artifact-tool 包形状；临时 `node_modules` 改用参数化 `Path.symlink_to`，不再调用 `cmd.exe` 或拼接 shell 命令，`&` 路径测试通过。
- 排除原因只接受标准化代码/类别；未知自由文本统一输出“其他合规原因”，候选名称或夹带名称的原因文本不会进入 Word/Excel。

Catalog 的最小可审计契约是：真实 `Catalog.staged_diff` 为主，逐记录变化同时考虑旧、新专业类；显式 mapping 的 `affected_scopes`/`changed_scopes` 仅作为兼容输入。没有从目录访问时间推断业务变化。

### GREEN 与回归证据

- `python -m unittest -v tests.test_reports` → `Ran 14 tests in 106.752s`，`OK`。
- 强化后的真实 `PreparedRun` + `RunCoordinator` + `ProjectPaths` adapter 集成 → `Ran 1 test in 24.511s`，`OK`；保存后复读日报 `新增正式推荐!A2=REPORT-NEW-1`，来源审计含 `SkillHub/partial`，且唯一受影响专业类工作簿复读到既有稳定 ID。
- `python -m unittest -v tests.test_runner`（强化 fixture 前的同一生产实现）→ `Ran 34 tests in 36.881s`，`OK`。
- `python -m unittest discover -s tests -v`（强化 fixture 前的同一生产实现）→ `Ran 178 tests in 149.964s`，`OK`。
- 提交前最终全套：`python -m unittest discover -s tests -v` → `Ran 178 tests in 150.526s`，`OK`。
- `python -m compileall -q 07_自动维护工作流/src 07_自动维护工作流/tests`、`node --check daily_xlsx_builder.mjs`、`git diff --check` 均以 0 退出；针对生产 `reports.py` 与 `test_reports.py` 搜索 `cmd.exe`、`mklink` 和硬编码用户路径均无匹配。

### 保留顾虑

- Task 11 仍须处理既有 9360 DXA grid 加 120 DXA indent 的实际 Word 视觉门；本轮不改变该已裁决的 minor。
- 当前环境仍无 `soffice`，所以没有新增 DOCX 页数/逐页 PNG 证据；不能宣称 Word 视觉门通过。原 Task 10 的结构 QA 和 12-sheet artifact-tool 渲染证据不因本轮数据接线修复失效。

## Fix round 2：新增正式映射门、候选 schema 与真实请求审计

### TDD RED

先只修改 `test_reports.py` / `test_runner.py`，运行 7 项针对性测试。结果：`Ran 7 tests in 60.015s`，`FAILED (failures=6, errors=1)`。

首错为真实 catalog snapshot 同时增加 08、11、15 门类时，`affected_scopes` 实际返回 `0809 计算机类 / 1101 军事类 / 1501 未批准类`，期望只返回批准的 `0809 计算机类`。其余 RED 分别证明：

- 条件候选与需适配候选使用真实 `观察标识/候选名称` 后，候选表 `A2` 为空；
- 没有 request event 时仍把 `SourceRun.query` 和报告生成时间伪装成请求地址/请求时间；
- 非 URL 检索词仍被建立 external hyperlink；
- 未映射以及只有军事学映射的新增正式项均未阻断，且开始产出 delivery；
- `SourceRun` 尚不接受 `request_events`，真实事件 fixture 抛出 `TypeError`。

随后为“层级/原因/限制”可见性增加独立断言，候选表 `O2` 实际为空、期望“条件候选”，得到符合预期的 RED。模板复读也先得到 `条件候选!O1=None`、期望“层级”的 RED。

### 最小实现

- 定义批准门类代码 `01–10、12–14`；军事学 11 和未知/越界代码不进入 catalog affected scopes。交叉学科 14 继续按专业逐项，`99 跨学科通用`映射继续允许。
- report adapter 在创建 `deliveries` 或任何文件前，比较 production/staged `当前Skill`，逐个验证新增正式 ID 至少存在一条批准范围内、非军事学专业任务映射；否则抛出含稳定 ID 的 `ReportBuildError`。已映射新增正式项只刷新其精确 scope。
- 条件/适配 `候选观察`在内存报告边界规范化：`观察标识→内部标识`、`候选名称→Skill名称/规范名称`，并保留 Canonical URL、许可证、候选层级、原因和限制；不修改 ledger truth。Word 增加“层级”“原因/结论”，Excel 候选/Skill 表追加同名两列。
- `SourceRun` 兼容性新增默认空元组 `request_events: tuple[SourceRequestEvent, ...]`。adapter 只展开真实事件的 platform、url、query_id、page、status_code、attempts、response SHA、evidence path、completed；事件无时间字段时明确写“未记录”。默认 query 不再制造审计行。
- Excel 来源请求审计扩为 10 列精确事件字段；唯一 JS builder 只对 `http://` / `https://` 建 external hyperlink。模板 `daily_review.xlsx` 通过同一 artifact-tool 主路径重新生成，未使用 openpyxl 写入；artifact-tool 新建/导出/重导入 inspect 与公式错误扫描完成，12 张表保持不变，来源请求审计复读为 `A1:J1`。

### GREEN 与回归证据

- 新增 7 项定向合同：`Ran 7 tests in 48.608s`，`OK`。
- 候选层级/原因强化与 mapped-formal exact-scope：`Ran 2 tests in 11.945s`，`OK`。
- 更新模板复读：`Ran 1 test in 0.011s`，`OK`。
- focused reports：`Ran 18 tests in 130.401s`，`OK`（随后增加 exact-scope/template 强化，最终数量见提交前验证）。
- 最终 focused reports：`Ran 19 tests in 130.348s`，`OK`。
- affected runner：`Ran 36 tests in 37.859s`，`OK`。
- 最终全套：`python -m unittest discover -s tests -v` → `Ran 185 tests in 174.287s`，`OK`。
- `python -m compileall -q 07_自动维护工作流/src 07_自动维护工作流/tests`、`node --check daily_xlsx_builder.mjs` 与 `git diff --check` 均以 0 退出。

### 保留顾虑

- `SourceRequestEvent` 当前没有请求发生时间字段，因此本轮严格写“未记录”，不从报告时间推断；若未来来源层增加可信时间戳，可在不改变现有事实边界的前提下扩列取值。
- Word 9360 DXA grid + 120 DXA indent minor 仍按裁决留 Task 11；当前环境仍无 `soffice`，不宣称 DOCX 视觉门通过。

## Fix round 3：专业范围精确绑定当前目录快照

### TDD RED

先只改 `test_reports.py` / `test_runner.py`，用独立矩阵覆盖 `08evil`、伪四位交叉学科 `1401`、空代码加军事自由文本、目录外但格式正确的 `0808`、军事学 `1101`、合法 `0809`、合法六位交叉学科专业 `140101` 和精确 `99`；另以真实 `RunCoordinator` / `PreparedRun` / `LedgerStore` adapter 验证无效新增正式映射必须在创建 `deliveries` 前失败。

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_reports.ReportContentTestCase.test_scope_mappings_must_match_exact_codes_in_the_captured_catalog tests.test_runner.RunnerTestCase.test_report_adapter_rejects_malformed_prefix_mapping_before_any_output -v
```

结果为 `Ran 2 tests in 24.016s`，`FAILED (failures=5)`。首错：`08evil` 实际返回为受影响 scope、期望空；同批还证明 `1401`、空代码军事文本、目录外 `0808` 被误纳入，且真实 adapter 对 `08evil` 未抛 `ReportBuildError` 并走到了文件生成路径。合法 `0809`、合法 `140101`、精确 `99` 和 `1101` 的预期在该矩阵中没有失败。

随后补强 catalog staged diff 的同一边界，加入 malformed `08evil` class 与 `1401` major。RED 为 `Ran 1 test in 0.002s`，`FAILED (failures=1)`；实际错误地返回了 `0809 / 08evil / 1401`，期望仅合法 `0809`。

### 最小实现

- 从本轮捕获的 `Catalog` 构建批准代码集合；若存在 `staged_snapshot`，使用其 rows 作为当前有效目录，否则使用捕获 catalog 的 rows。没有维护全局专业代码白名单。
- `01–10、12–13` 只接受当前目录中与门类一致的精确四位专业类代码；`14` 只接受当前目录中精确六位、以 `14` 开头的专业代码；`99` 仅精确值允许并规范为 `99 跨学科通用`。
- `11`、其它门类、空代码、格式错误、目录中不存在的代码均被拒绝；同一代码出现冲突目录名称时也不建立批准 scope。输出 scope 名称取目录规范名称，不信任映射自由文本。
- `_scope_index` 只从通过上述绑定的专业任务映射建立 scope，不再从 `当前Skill` 的非正式附加字段绕过映射门；目录基线变化也使用同一批准规则。
- `_validate_new_formal_mappings` 接收 `prepared.catalog_snapshot`，并继续在 `deliveries` 目录创建前 fail-closed。catalog diff scope 同步增加四位/六位形状与门类前缀校验，避免 malformed staged row 进入交付范围。

### GREEN 与最终验证

- 首批定向 GREEN：`Ran 2 tests in 0.344s`，`OK`；真实无效 adapter 在生成前快速退出。
- catalog staged diff 强化 GREEN：`Ran 1 test in 0.002s`，`OK`。
- 最终 focused reports：`Ran 20 tests in 138.282s`，`OK`。
- 最终 affected runner：`Ran 37 tests in 39.612s`，`OK`。
- 最终全套：`python -m unittest discover -s tests -q` → `Ran 187 tests in 176.705s`，`OK`。
- bundled Python `compileall -q src tests`、bundled Node `--check src/skill_maintainer/daily_xlsx_builder.mjs`、`git diff --check` 均以 0 退出。`git diff --check` 仅输出仓库既有 LF→CRLF 工作树提示，没有 whitespace error。

### 保留顾虑

- 本轮没有触碰 Task 11 的 Word 9360 DXA grid + 120 DXA indent 视觉项；当前环境仍无 `soffice`，不新增或伪称 DOCX 视觉通过证据。
- 本轮只改变 scope 选择与 fail-closed 校验，没有重新生成报告模板或改变 artifact-tool Excel authoring/OOXML 兼容补丁；原 Task 10 的 12-sheet 渲染和公式扫描证据保持有效。
