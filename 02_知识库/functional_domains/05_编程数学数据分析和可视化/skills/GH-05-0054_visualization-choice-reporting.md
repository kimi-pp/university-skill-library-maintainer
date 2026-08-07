---
id: GH-05-0054
category: "编程、数学、数据分析和可视化"
source_scope: GitHub
status: 入选
ecosystem: "Anthropic Claude Code / 可移植工作流"
source_form: "社区 skill、GitHub 公开仓库（许可证待核）"
compatibility: B
priority: "高"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# 可视化选择与结果报告（visualization-choice-reporting）

> 根据问题和数据类型选择图表，完成设计检查、叙事组织和误导风险审计。

## 功能说明

根据问题和数据类型选择图表，完成设计检查、叙事组织和误导风险审计。 本轮读取了 232 行说明，重点核对了Visualization Choice & Reporting、Workflow、Question-Data Profiling、Chart Selection Guide、Design Checklist。该结论仅反映说明与包结构，不代表依赖已安装或任务已成功运行。

## 适用对象与场景

- 适用角色：学生、教师、科研与数据分析人员
- 典型场景：实验设计、因果与贝叶斯推理、可视化选择和交互图表
- 功能标签：图表选择、数据类型、叙事、报告、误导防范

## 接入判断

- 兼容等级：B
- 适配建议：将 Claude 专用调用替换为 Codex 可用工具，并补充学科统计假设和验证门。
- 依赖条件：按任务可能需要统计软件、D3.js 或浏览器环境
- 风险与边界：仓库许可证未明确；方法模板不能代替数据诊断、因果识别条件或真实运行验证。 仓库许可证未明确或无法由 GitHub 自动识别，采用前需单独核验。
- 关联说明：同类技能按任务粒度并存；部署时优先选择覆盖需求且许可证、依赖和维护状态更合适者。

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：读取 232 行 SKILL.md；检查 skill 范围内 4 个文件，其中脚本 0 个、references/assets/templates 资源 0 个。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/lyndonkl/claude/blob/main/skills/visualization-choice-reporting/SKILL.md](https://github.com/lyndonkl/claude/blob/main/skills/visualization-choice-reporting/SKILL.md)
- 仓库：[lyndonkl/claude](https://github.com/lyndonkl/claude)
- 仓库元数据：141 stars；最近推送 2026-08-04；许可证 未明确（以仓库当前文件为准）
