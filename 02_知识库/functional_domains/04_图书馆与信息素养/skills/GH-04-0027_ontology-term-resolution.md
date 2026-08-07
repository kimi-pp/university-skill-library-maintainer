---
id: GH-04-0027
category: "图书馆与信息素养"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills（兼容 Codex、Claude Code、Cursor 等）"
source_form: "社区 skill、GitHub 开源仓库"
compatibility: B
priority: "高"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# 本体术语规范化与解析（ontology-term-resolution）

> 在指定本体范围内把自由文本解析为规范术语，并显式报告未匹配或模糊结果。

## 功能说明

在指定本体范围内把自由文本解析为规范术语，并显式报告未匹配或模糊结果。 本轮读取了 147 行说明，重点核对了Ontology Term Resolution、When to use、The rule、Two directions、Resolve text to terms。该结论仅反映说明与包结构，不代表依赖已安装或任务已成功运行。

## 适用对象与场景

- 适用角色：科研人员、研究生、图书馆与科研数据管理人员
- 典型场景：个人/机构知识库、科研数据治理、元数据规范与术语控制
- 功能标签：本体、受控词表、术语映射、数据规范

## 接入判断

- 兼容等级：B
- 适配建议：从只读盘点和小样本映射开始；凭据、写操作和批量变更另设审批。
- 依赖条件：对应平台或数据标准；部分功能需要 Python、API 凭据或本地索引
- 风险与边界：元数据映射可能丢失语义；凭据、未公开研究对象和批量写入必须受控。
- 关联说明：同类技能按任务粒度并存；部署时优先选择覆盖需求且许可证、依赖和维护状态更合适者。

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：读取 147 行 SKILL.md；检查 skill 范围内 7 个文件，其中脚本 3 个、references/assets/templates 资源 3 个。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/ontology-term-resolution/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/ontology-term-resolution/SKILL.md)
- 仓库：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- 仓库元数据：32822 stars；最近推送 2026-08-03；许可证 MIT（以仓库当前文件为准）
