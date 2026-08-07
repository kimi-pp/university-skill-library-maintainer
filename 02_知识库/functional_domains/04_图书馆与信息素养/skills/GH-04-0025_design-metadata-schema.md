---
id: GH-04-0025
category: "图书馆与信息素养"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills（通用）"
source_form: "社区 skill、GitHub 开源仓库"
compatibility: B
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# 元数据模式设计（design-metadata-schema）

> 从业务与检索需求出发定义字段、约束、验证规则和可维护的元数据模式。

## 功能说明

从业务与检索需求出发定义字段、约束、验证规则和可维护的元数据模式。 本轮读取了 60 行说明，重点核对了Design Metadata Schema Skill、Inputs、Workflow、Step 1: Requirement Analysis、Step 2: Schema Definition。该结论仅反映说明与包结构，不代表依赖已安装或任务已成功运行。

## 适用对象与场景

- 适用角色：科研人员、研究生、图书馆与科研数据管理人员
- 典型场景：个人/机构知识库、科研数据治理、元数据规范与术语控制
- 功能标签：元数据、字段约束、验证、模式文档

## 接入判断

- 兼容等级：B
- 适配建议：从只读盘点和小样本映射开始；凭据、写操作和批量变更另设审批。
- 依赖条件：对应平台或数据标准；部分功能需要 Python、API 凭据或本地索引
- 风险与边界：元数据映射可能丢失语义；凭据、未公开研究对象和批量写入必须受控。
- 关联说明：同类技能按任务粒度并存；部署时优先选择覆盖需求且许可证、依赖和维护状态更合适者。

## 功能验证

- 验证层级：说明已核验
- 验证结果：读取 60 行 SKILL.md；检查 skill 范围内 1 个文件，其中脚本 0 个、references/assets/templates 资源 0 个。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/dandye/ai-runbooks/blob/main/skills/design-metadata-schema/SKILL.md](https://github.com/dandye/ai-runbooks/blob/main/skills/design-metadata-schema/SKILL.md)
- 仓库：[dandye/ai-runbooks](https://github.com/dandye/ai-runbooks)
- 仓库元数据：120 stars；最近推送 2026-08-04；许可证 Apache-2.0（以仓库当前文件为准）
