---
id: GH-02-0007
category: "文档、表格、演示文稿与办公自动化"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills（兼容 Codex）"
source_form: "社区 skill、开源仓库"
compatibility: B
priority: "高"
validation: "说明已核验"
as_of: 2026-08-06
---

# 多格式转 Markdown（markitdown）

> 使用 Microsoft MarkItDown 将多种文档安全转换为 Markdown。

## 功能说明

覆盖 Office、PDF、数据文件、流、批处理、插件、视觉 OCR、Azure 提取和官方 MCP 路线。

## 适用对象与场景

- 适用角色：科研人员、学生、图书馆人员、行政人员
- 典型场景：资料入库、文档检索、RAG 准备和批量转换
- 功能标签：Markdown、Office、PDF、批量转换、RAG

## 接入判断

- 兼容等级：B
- 适配建议：安装对应 MarkItDown 能力或改接现有转换器。
- 依赖条件：Microsoft MarkItDown；可选 OCR、Azure 或 MCP
- 风险与边界：转换可能丢失复杂布局；外部 OCR 服务涉及数据边界。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/markitdown/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/markitdown/SKILL.md)
- 仓库：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- 仓库元数据：32822 stars；最近推送 2026-08-03；许可证 MIT（以仓库当前文件为准）
