---
id: GH-02-0020
category: "文档、表格、演示文稿与办公自动化"
source_scope: GitHub
status: 入选
ecosystem: "Anthropic Claude Code / Agent Skills"
source_form: "社区 skill、开源仓库"
compatibility: B
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# 复杂工作簿审查与编辑（spreadsheet-processing）

> 分析、调试、核对并验证复杂 Excel 或连接型表格。

## 功能说明

覆盖公式和数据流发现、跨表引用、命名范围、模板、回滚快照、Google Sheets 连接和证据/主张账本。

## 适用对象与场景

- 适用角色：行政人员、科研人员、信息化人员
- 典型场景：复杂台账审计、模板调试、跨表公式追踪
- 功能标签：工作簿审查、公式数据流、命名范围、证据包

## 接入判断

- 兼容等级：B
- 适配建议：去除 Google Sheets 特定部分也可独立用于本地 Excel。
- 依赖条件：Excel/Sheets 工具；视任务使用脚本
- 风险与边界：范围很宽，执行前需限制文件和写入边界。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/kangminlee-maker/excel-workbook-editing/blob/main/SKILL.md](https://github.com/kangminlee-maker/excel-workbook-editing/blob/main/SKILL.md)
- 仓库：[kangminlee-maker/excel-workbook-editing](https://github.com/kangminlee-maker/excel-workbook-editing)
- 仓库元数据：0 stars；最近推送 2026-06-29；许可证 MIT（以仓库当前文件为准）
