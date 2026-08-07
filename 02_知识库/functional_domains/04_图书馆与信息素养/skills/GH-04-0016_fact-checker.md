---
id: GH-04-0016
category: "图书馆与信息素养"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills（跨生态）"
source_form: "社区 skill、GitHub 公开仓库（许可证待核）"
compatibility: B
priority: "中"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# 系统化事实核查与提示注入防护（fact-checker）

> 按专业核查协议完成主张拆分、证据搜索、来源分级和结论表达，并处理恶意网页指令。

## 功能说明

按专业核查协议完成主张拆分、证据搜索、来源分级和结论表达，并处理恶意网页指令。 本轮读取了 284 行说明，重点核对了Fact Checker、Critical Requirement、UNTRUSTED CONTENT PRINCIPLE、INJECTION DETECTION、USER NOTIFICATION AND CHOICE。该结论仅反映说明与包结构，不代表依赖已安装或任务已成功运行。

## 适用对象与场景

- 适用角色：学生、教师、科研人员、图书馆与宣传人员
- 典型场景：课程信息辨识、新闻与网络主张核验、来源教育
- 功能标签：事实核查、来源分级、提示注入、安全边界

## 接入判断

- 兼容等级：B
- 适配建议：保留证据分级和人工裁决，把搜索工具替换为本项目可用的浏览与数据库接口。
- 依赖条件：网络检索；必要时使用网页归档或反向图像检索
- 风险与边界：检索不到不等于主张为假；恶意网页内容、时效性和来源偏差需单独处理。 仓库许可证未明确或无法由 GitHub 自动识别，采用前需单独核验。
- 关联说明：同类技能按任务粒度并存；部署时优先选择覆盖需求且许可证、依赖和维护状态更合适者。

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：读取 284 行 SKILL.md；检查 skill 范围内 7 个文件，其中脚本 0 个、references/assets/templates 资源 3 个。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/SamaritanOC/fact-checker/blob/main/SKILL.md](https://github.com/SamaritanOC/fact-checker/blob/main/SKILL.md)
- 仓库：[SamaritanOC/fact-checker](https://github.com/SamaritanOC/fact-checker)
- 仓库元数据：0 stars；最近推送 2026-05-18；许可证 未明确（以仓库当前文件为准）
