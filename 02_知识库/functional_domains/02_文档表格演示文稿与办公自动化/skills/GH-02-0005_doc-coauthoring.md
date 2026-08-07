---
id: GH-02-0005
category: "文档、表格、演示文稿与办公自动化"
source_scope: GitHub
status: 入选
ecosystem: "Anthropic Claude Code / Agent Skills"
source_form: "官方发布、开源仓库、可移植工作流"
compatibility: B
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# 结构化文档共创（doc-coauthoring）

> 引导用户共同撰写提案、规范、决策文档和说明材料。

## 功能说明

通过背景收集、结构设计、分段迭代和读者测试减少上下文遗漏，重点是写作流程而非文件格式。

## 适用对象与场景

- 适用角色：教学人员、科研人员、行政人员、学生
- 典型场景：项目方案、课程规范、制度草案和决策记录
- 功能标签：文档共创、需求澄清、迭代、读者验证

## 接入判断

- 兼容等级：B
- 适配建议：把对话阶段直接转成 Codex 任务步骤；可与 docx skill 联用。
- 依赖条件：无明确外部依赖
- 风险与边界：需要用户持续提供上下文，不适合无人监督生成正式制度。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md)
- 仓库：[anthropics/skills](https://github.com/anthropics/skills)
- 仓库元数据：166590 stars；最近推送 2026-07-24；许可证 各技能目录独立许可证（以仓库当前文件为准）
