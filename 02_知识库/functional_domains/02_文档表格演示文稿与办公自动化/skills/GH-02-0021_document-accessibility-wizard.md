---
id: GH-02-0021
category: "文档、表格、演示文稿与办公自动化"
source_scope: GitHub
status: 入选
ecosystem: "OpenAI Codex"
source_form: "社区 skill、开源仓库"
compatibility: B
priority: "高"
validation: "说明已核验"
as_of: 2026-08-06
---

# 文档无障碍审查向导（document-accessibility-wizard）

> 引导式审查 Office 文档和 PDF 的无障碍问题。

## 功能说明

支持单文件、批量和递归目录，编排 Word、Excel、PowerPoint、PDF 专项检查并生成综合 Markdown 报告。

## 适用对象与场景

- 适用角色：教学人员、行政人员、学生支持人员、信息化人员
- 典型场景：课程材料、网站附件、行政通知和报告的无障碍审查
- 功能标签：无障碍、DOCX、XLSX、PPTX、PDF、批量扫描

## 接入判断

- 兼容等级：B
- 适配建议：需要将子代理调用映射到当前 Codex 能力；规则可直接复用。
- 依赖条件：多个专项无障碍 skill 和文档解析工具
- 风险与边界：自动审查不能替代辅助技术用户测试；扫描目录需严格限界。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/Community-Access/accessibility-agents/blob/main/codex-skills/document-accessibility-wizard/SKILL.md](https://github.com/Community-Access/accessibility-agents/blob/main/codex-skills/document-accessibility-wizard/SKILL.md)
- 仓库：[Community-Access/accessibility-agents](https://github.com/Community-Access/accessibility-agents)
- 仓库元数据：382 stars；最近推送 2026-08-04；许可证 MIT（以仓库当前文件为准）
