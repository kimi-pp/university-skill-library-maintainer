# DOCX 版式与验证记录

日期：2026-08-06

## 版式选择

- 设计 preset：`compact_reference_guide`
- 首页面板：`editorial_cover`
- 页面：US Letter 8.5 × 11 英寸；四边页边距 1 英寸；页眉页脚距离 0.492 英寸
- 正文字体：Calibri 11 pt；段后 6 pt；1.25 倍行距
- 标题：Heading 1 为 16 pt、Heading 2 为 13 pt、Heading 3 为 12 pt，使用 preset 指定蓝色和段前段后值
- 表格：总宽 9360 DXA；缩进 120 DXA；固定网格；单元格边距 top/bottom 80、start/end 120 DXA

## 命名覆盖

- 中文排版覆盖：保留 preset 的 Calibri ASCII/HAnsi，同时将 East Asia 字体统一设为 Microsoft YaHei，避免中文回退不一致。
- 候选元数据表：使用 preset 的 compact label-detail 宽度 1701/7659 DXA。
- 来源表：使用 3900/720/900/1260/2580 DXA，合计 9360 DXA；表格文字 8.8 pt，为来源清单专用紧凑覆盖。
- 风险段落：使用 `#9B1C1C`，与 preset 的 risk red 一致。

## 首轮逐页验证

- 首轮页数：分类 01 为 17 页，分类 02 为 19 页，分类 03 为 24 页，共 60 页。
- 为每份报告生成带页码 contact sheet，检查全部页面的页序、空白、分页、标题、表格和页眉页脚。
- 原尺寸抽查封面、摘要、首个候选、连续候选密集页、原跨页问题位置和来源清单页。
- 初次抽查发现个别四行元数据表跨页；已将“标题—摘要—元数据表”设为同一分页单元并重新生成、重新渲染。
- 最终检查未发现文字裁切、对象重叠、表格断裂、异常字体替换或无意空白页。

## PaperSpine 增补复核

- 分类 01 已增补 `GH-01-0020 paper-spine` 并重新生成 DOCX。
- 结构审计确认 20 个 Skill Heading 2、23 张表和 27 个 GitHub 超链接，页面、样式和表格几何 token 均通过。
- 本次环境未找到 LibreOffice，标准 DOCX 渲染器无法启动；Microsoft Word 后台导出未生成可用页面。因而首轮分类 01 的 17 页渲染只作为增补前历史记录，本次不宣称完成当前版本的逐页视觉复核。

## 结构审计结果

- DOCX 均可重新打开。
- Skill Heading 2 数量：20 / 22 / 31，与当前规范数据一致。
- 文档表格数量：23 / 25 / 34，与“摘要 + 选型指南 + 每个候选一表 + 来源表”结构一致。
- 页宽、页高、页边距、页眉页脚距离、Normal/Heading 样式、9360 DXA 表宽、120 DXA 表缩进和单元格宽度审计通过。
- GitHub 超链接数量：27 / 33 / 38，覆盖所有候选地址和仓库来源。
- 报告明确保留“未安装、未运行”的验证边界。

## 分类 04/05 复核

- 沿用 `compact_reference_guide` preset 与既有命名覆盖，新增报告不改变分类 01–03 的版式。
- 分类 04 结构审计：29 个 Skill Heading 2、32 张表、41 个 GitHub 超链接。
- 分类 05 结构审计：55 个 Skill Heading 2、58 张表、61 个 GitHub 超链接。
- 两份文档均可重新打开；Letter 页面、四边 1 英寸页边距、页眉页脚距离、Normal/Heading 样式、9360 DXA 表宽、120 DXA 表缩进与全部单元格宽度通过审计。
- 本机仍未找到 LibreOffice/soffice，标准渲染器无法生成 PNG；因此分类 04/05 仅记录结构审计通过，不宣称逐页视觉验证通过。
