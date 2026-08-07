---
id: GH-02-0016
category: "文档、表格、演示文稿与办公自动化"
source_scope: GitHub
status: 入选
ecosystem: "OpenAI Codex / Agent Skills"
source_form: "社区 skill、开源仓库"
compatibility: B
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# OfficeIMO 文档操作（officeimo-document-operator）

> 使用 OfficeIMO 检查、搜索、摘要、提取和转换本地文档。

## 功能说明

覆盖 Office、PDF、邮件、OneNote、OpenDocument、Markdown、HTML、CSV 和 EPUB，并提供 .NET CLI 回退路线。

## 适用对象与场景

- 适用角色：信息化人员、行政人员、图书馆人员
- 典型场景：本地多格式文档处理、无 COM 服务器流程
- 功能标签：OfficeIMO、DOCX、XLSX、PPTX、PDF、邮件

## 接入判断

- 兼容等级：B
- 适配建议：安装或提供 OfficeIMO CLI 后可用于 Codex；优先只读操作。
- 依赖条件：.NET 8+ 与 OfficeIMO CLI/库
- 风险与边界：格式覆盖广但特性支持不一；转换保真度需抽查。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/EvotecIT/OfficeIMO/blob/master/.agents/plugins/officeimo-document-tools/skills/officeimo-document-operator/SKILL.md](https://github.com/EvotecIT/OfficeIMO/blob/master/.agents/plugins/officeimo-document-tools/skills/officeimo-document-operator/SKILL.md)
- 仓库：[EvotecIT/OfficeIMO](https://github.com/EvotecIT/OfficeIMO)
- 仓库元数据：499 stars；最近推送 2026-08-06；许可证 MIT（以仓库当前文件为准）
