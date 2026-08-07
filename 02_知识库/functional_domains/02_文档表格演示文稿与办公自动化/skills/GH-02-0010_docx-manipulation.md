---
id: GH-02-0010
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

# python-docx 文档操作（docx-manipulation）

> 使用 python-docx 程序化创建和编辑 Word 文档。

## 功能说明

提供段落、表格、样式、图片、页眉页脚等常见操作的任务路由和代码范式。

## 适用对象与场景

- 适用角色：行政人员、教学人员、科研人员
- 典型场景：批量报告、公文模板、课程材料自动生成
- 功能标签：python-docx、Word、文档操作

## 接入判断

- 兼容等级：B
- 适配建议：将 Claude 特定元数据改为 Codex skill；复用 python-docx 范式。
- 依赖条件：python-docx
- 风险与边界：复杂 Word 特性支持有限，输出仍需版式检查。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/claude-office-skills/skills/blob/main/docx-manipulation/SKILL.md](https://github.com/claude-office-skills/skills/blob/main/docx-manipulation/SKILL.md)
- 仓库：[claude-office-skills/skills](https://github.com/claude-office-skills/skills)
- 仓库元数据：362 stars；最近推送 2026-01-31；许可证 MIT（以仓库当前文件为准）
