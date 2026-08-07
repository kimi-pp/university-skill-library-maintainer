---
id: GH-02-0014
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

# Office 转 Markdown（office-to-md）

> 从 DOCX、XLSX、PPTX 等 Office 文件提取结构化 Markdown。

## 功能说明

面向后续检索、摘要和知识库处理，描述不同文件类型的文本、表格和元数据提取方式。

## 适用对象与场景

- 适用角色：图书馆人员、科研人员、行政人员、学生
- 典型场景：档案入库、课程材料检索、文档摘要与迁移
- 功能标签：Office、Markdown、提取、知识库

## 接入判断

- 兼容等级：B
- 适配建议：接入 MarkItDown 或本地 Office 解析器；保留源文件链接。
- 依赖条件：Office 解析库或转换器
- 风险与边界：复杂图形、批注和版式信息可能无法完整保留。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/claude-office-skills/skills/blob/main/office-to-md/SKILL.md](https://github.com/claude-office-skills/skills/blob/main/office-to-md/SKILL.md)
- 仓库：[claude-office-skills/skills](https://github.com/claude-office-skills/skills)
- 仓库元数据：362 stars；最近推送 2026-01-31；许可证 MIT（以仓库当前文件为准）
