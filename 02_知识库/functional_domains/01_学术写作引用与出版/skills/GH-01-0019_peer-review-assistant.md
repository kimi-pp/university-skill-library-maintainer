---
id: GH-01-0019
category: "学术写作、引用与出版"
source_scope: GitHub
status: 入选
ecosystem: "Anthropic Claude Code / Agent Skills"
source_form: "社区 skill、开源仓库"
compatibility: C
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# 证据检索型预审助手（peer-review-assistant）

> 结合文献搜索检查手稿背景主张、遗漏引用和方法时效性。

## 功能说明

工作流先识别可检验主张，再运行定向 Consensus 搜索，区分背景证据、方法惯例和需要作者说明的问题。

## 适用对象与场景

- 适用角色：科研人员、研究生
- 典型场景：投稿前预审、背景引用补充、方法是否过时的检查
- 功能标签：同行评审、Consensus、背景主张、遗漏文献

## 接入判断

- 兼容等级：C
- 适配建议：需将 Consensus 搜索替换为可用学术数据库或 MCP。
- 依赖条件：Consensus 搜索服务
- 风险与边界：依赖外部检索结果；不能将摘要匹配等同于完整证据核验。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/stephenturner/skill-peer-review-assistant/blob/main/SKILL.md](https://github.com/stephenturner/skill-peer-review-assistant/blob/main/SKILL.md)
- 仓库：[stephenturner/skill-peer-review-assistant](https://github.com/stephenturner/skill-peer-review-assistant)
- 仓库元数据：33 stars；最近推送 2026-06-30；许可证 MIT（以仓库当前文件为准）
