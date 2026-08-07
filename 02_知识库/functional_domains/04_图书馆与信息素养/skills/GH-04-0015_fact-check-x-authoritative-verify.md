---
id: GH-04-0015
category: "图书馆与信息素养"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills（跨生态）"
source_form: "社区 skill、GitHub 开源仓库"
compatibility: B
priority: "中"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# 权威来源证据核验（fact-check-x-authoritative-verify）

> 针对单一知识点从权威来源取证，由当前智能体裁决并形成可审计报告。

## 功能说明

针对单一知识点从权威来源取证，由当前智能体裁决并形成可审计报告。 本轮读取了 122 行说明，重点核对了权威证据核验、单知识点取证、并行取证、当前智能体裁决、报告交付。该结论仅反映说明与包结构，不代表依赖已安装或任务已成功运行。

## 适用对象与场景

- 适用角色：学生、教师、科研人员、图书馆与宣传人员
- 典型场景：课程信息辨识、新闻与网络主张核验、来源教育
- 功能标签：权威证据、并行取证、主张裁决、审计

## 接入判断

- 兼容等级：B
- 适配建议：保留证据分级和人工裁决，把搜索工具替换为本项目可用的浏览与数据库接口。
- 依赖条件：网络检索；必要时使用网页归档或反向图像检索
- 风险与边界：检索不到不等于主张为假；恶意网页内容、时效性和来源偏差需单独处理。
- 关联说明：同类技能按任务粒度并存；部署时优先选择覆盖需求且许可证、依赖和维护状态更合适者。

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：读取 122 行 SKILL.md；检查 skill 范围内 18 个文件，其中脚本 7 个、references/assets/templates 资源 3 个。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/ASI2030/Fact-Check-X/blob/main/skills/fact-check-x-authoritative-verify/SKILL.md](https://github.com/ASI2030/Fact-Check-X/blob/main/skills/fact-check-x-authoritative-verify/SKILL.md)
- 仓库：[ASI2030/Fact-Check-X](https://github.com/ASI2030/Fact-Check-X)
- 仓库元数据：0 stars；最近推送 2026-07-30；许可证 Apache-2.0（以仓库当前文件为准）
