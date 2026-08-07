---
id: GH-04-0026
category: "图书馆与信息素养"
source_scope: GitHub
status: 入选
ecosystem: "nanobot / 可适配 Agent Skill"
source_form: "社区 skill、GitHub 公开仓库（许可证待核）"
compatibility: B
priority: "高"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# Zotero 本地知识库桥接（zotero-bridge）

> 把 Zotero 馆藏分层同步到本地 FTS5 与 RAG 索引，支持基于个人文献库的可引用检索。

## 功能说明

把 Zotero 馆藏分层同步到本地 FTS5 与 RAG 索引，支持基于个人文献库的可引用检索。 本轮读取了 147 行说明，重点核对了Zotero Bridge、Setup、Usage、Sync Library、Quick sync (metadata + abstracts)。该结论仅反映说明与包结构，不代表依赖已安装或任务已成功运行。

## 适用对象与场景

- 适用角色：科研人员、研究生、图书馆与科研数据管理人员
- 典型场景：个人/机构知识库、科研数据治理、元数据规范与术语控制
- 功能标签：Zotero、全文索引、RAG、混合检索

## 接入判断

- 兼容等级：B
- 适配建议：从只读盘点和小样本映射开始；凭据、写操作和批量变更另设审批。
- 依赖条件：对应平台或数据标准；部分功能需要 Python、API 凭据或本地索引
- 风险与边界：元数据映射可能丢失语义；凭据、未公开研究对象和批量写入必须受控。 仓库许可证未明确或无法由 GitHub 自动识别，采用前需单独核验。
- 关联说明：同类技能按任务粒度并存；部署时优先选择覆盖需求且许可证、依赖和维护状态更合适者。

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：读取 147 行 SKILL.md；检查 skill 范围内 15 个文件，其中脚本 10 个、references/assets/templates 资源 1 个。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/Albert-Libra/nanobot-zotero-bridge/blob/master/SKILL.md](https://github.com/Albert-Libra/nanobot-zotero-bridge/blob/master/SKILL.md)
- 仓库：[Albert-Libra/nanobot-zotero-bridge](https://github.com/Albert-Libra/nanobot-zotero-bridge)
- 仓库元数据：3 stars；最近推送 2026-06-01；许可证 未明确（以仓库当前文件为准）
