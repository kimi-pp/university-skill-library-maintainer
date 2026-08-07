---
id: GH-05-0032
category: "编程、数学、数据分析和可视化"
source_scope: GitHub
status: 入选
ecosystem: "多智能体生态（Codex、Claude Code、Cursor、Gemini CLI 等）"
source_form: "社区 skill、GitHub 开源仓库"
compatibility: B
priority: "高"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# 数据叙事与洞察表达（data-storytelling）

> 把分析结论组织为面向特定受众的背景、冲突、洞察和行动建议。

## 功能说明

把分析结论组织为面向特定受众的背景、冲突、洞察和行动建议。 本轮读取了 70 行说明，重点核对了Data Storytelling、When to Use This Skill、Core Concepts、1. Story Structure、2. Narrative Arc。该结论仅反映说明与包结构，不代表依赖已安装或任务已成功运行。

## 适用对象与场景

- 适用角色：学生、教师、数据工程与开发人员
- 典型场景：教学项目、数据平台、数据库、Python/JavaScript 工程和 MLOps
- 功能标签：数据故事、受众、叙事结构、图表、建议

## 接入判断

- 兼容等级：B
- 适配建议：抽取单一 skill 并替换 Claude 插件路由；保留与现有工具链相匹配的章节。
- 依赖条件：对应语言、数据库或数据平台；部分流程需要云服务或测试框架
- 风险与边界：技术栈与版本差异较大；性能、安全和数据质量结论必须由实际环境验证。
- 关联说明：同类技能按任务粒度并存；部署时优先选择覆盖需求且许可证、依赖和维护状态更合适者。

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：读取 70 行 SKILL.md；检查 skill 范围内 2 个文件，其中脚本 0 个、references/assets/templates 资源 1 个。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/wshobson/agents/blob/main/plugins/business-analytics/skills/data-storytelling/SKILL.md](https://github.com/wshobson/agents/blob/main/plugins/business-analytics/skills/data-storytelling/SKILL.md)
- 仓库：[wshobson/agents](https://github.com/wshobson/agents)
- 仓库元数据：38534 stars；最近推送 2026-08-05；许可证 MIT（以仓库当前文件为准）
