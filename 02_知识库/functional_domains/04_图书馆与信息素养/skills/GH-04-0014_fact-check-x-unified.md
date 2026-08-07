---
id: GH-04-0014
category: "图书馆与信息素养"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills（跨生态）"
source_form: "社区 skill、GitHub 开源仓库"
compatibility: B
priority: "高"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# 可复现事实核查统一入口（fact-check-x-unified）

> 编排证据优先的主张拆解、并行取证、答案比较、裁决与可复现报告流程。

## 功能说明

编排证据优先的主张拆解、并行取证、答案比较、裁决与可复现报告流程。 本轮读取了 141 行说明，重点核对了Fact-Check-X 统一入口、依赖定位、完整流程、跳过知识点对比、执行边界。该结论仅反映说明与包结构，不代表依赖已安装或任务已成功运行。

## 适用对象与场景

- 适用角色：学生、教师、科研人员、图书馆与宣传人员
- 典型场景：课程信息辨识、新闻与网络主张核验、来源教育
- 功能标签：事实核查、证据优先、答案比较、交付门禁

## 接入判断

- 兼容等级：B
- 适配建议：保留证据分级和人工裁决，把搜索工具替换为本项目可用的浏览与数据库接口。
- 依赖条件：网络检索；必要时使用网页归档或反向图像检索
- 风险与边界：检索不到不等于主张为假；恶意网页内容、时效性和来源偏差需单独处理。
- 关联说明：同类技能按任务粒度并存；部署时优先选择覆盖需求且许可证、依赖和维护状态更合适者。

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：读取 141 行 SKILL.md；检查 skill 范围内 10 个文件，其中脚本 3 个、references/assets/templates 资源 2 个。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/ASI2030/Fact-Check-X/blob/main/skills/fact-check-x-unified/SKILL.md](https://github.com/ASI2030/Fact-Check-X/blob/main/skills/fact-check-x-unified/SKILL.md)
- 仓库：[ASI2030/Fact-Check-X](https://github.com/ASI2030/Fact-Check-X)
- 仓库元数据：0 stars；最近推送 2026-07-30；许可证 Apache-2.0（以仓库当前文件为准）
