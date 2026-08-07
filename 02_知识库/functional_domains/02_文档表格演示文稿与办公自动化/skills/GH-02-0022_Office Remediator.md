---
id: GH-02-0022
category: "文档、表格、演示文稿与办公自动化"
source_scope: GitHub
status: 入选
ecosystem: "Gemini CLI / Agent Skills"
source_form: "社区 skill、开源仓库"
compatibility: B
priority: "高"
validation: "说明已核验"
as_of: 2026-08-06
---

# Office 无障碍修复（Office Remediator）

> 为 Word、Excel 和 PowerPoint 生成可执行的无障碍修复方案。

## 功能说明

区分 python-docx、openpyxl、python-pptx 可自动修复的问题和必须在 Office UI 中手工处理的问题。

## 适用对象与场景

- 适用角色：教学人员、行政人员、信息化人员
- 典型场景：修复标题结构、替代文本、表格和阅读顺序问题
- 功能标签：无障碍修复、Word、Excel、PowerPoint

## 接入判断

- 兼容等级：B
- 适配建议：将 Gemini 扩展路径改造成 Codex skill，并保留人工修复清单。
- 依赖条件：python-docx、openpyxl、python-pptx；部分 Office UI
- 风险与边界：程序化修复覆盖有限，视觉和屏幕阅读器体验需人工验证。
- 关联说明：可与 GH-02-0021 组成审查—修复流程

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/Community-Access/accessibility-agents/blob/main/.gemini/extensions/a11y-agents/skills/office-remediator/SKILL.md](https://github.com/Community-Access/accessibility-agents/blob/main/.gemini/extensions/a11y-agents/skills/office-remediator/SKILL.md)
- 仓库：[Community-Access/accessibility-agents](https://github.com/Community-Access/accessibility-agents)
- 仓库元数据：382 stars；最近推送 2026-08-04；许可证 MIT（以仓库当前文件为准）
