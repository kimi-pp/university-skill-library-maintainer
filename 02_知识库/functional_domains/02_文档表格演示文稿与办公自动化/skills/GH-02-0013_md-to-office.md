---
id: GH-02-0013
category: "文档、表格、演示文稿与办公自动化"
source_scope: GitHub
status: 入选
ecosystem: "Anthropic Claude Code"
source_form: "社区 skill、开源仓库"
compatibility: B
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# Markdown 转 Office（md-to-office）

> 把 Markdown 内容转换为常见 Office 文件。

## 功能说明

定义标题、列表、表格、代码块和媒体向 DOCX/PPTX 等目标格式的映射与转换路线。

## 适用对象与场景

- 适用角色：学生、教学人员、科研人员、行政人员
- 典型场景：笔记转报告、Markdown 方案转 Word、提纲转演示
- 功能标签：Markdown、DOCX、PPTX、XLSX、转换

## 接入判断

- 兼容等级：B
- 适配建议：选择本地转换工具并为目标模板增加样式映射。
- 依赖条件：Pandoc 或 Python/Node.js Office 库
- 风险与边界：跨格式转换可能丢失版式与语义，需要目标文件检查。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/claude-office-skills/skills/blob/main/md-to-office/SKILL.md](https://github.com/claude-office-skills/skills/blob/main/md-to-office/SKILL.md)
- 仓库：[claude-office-skills/skills](https://github.com/claude-office-skills/skills)
- 仓库元数据：362 stars；最近推送 2026-01-31；许可证 MIT（以仓库当前文件为准）
