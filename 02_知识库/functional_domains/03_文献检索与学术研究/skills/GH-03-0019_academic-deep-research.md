---
id: GH-03-0019
category: "文献检索与学术研究"
source_scope: GitHub
status: 入选
ecosystem: "其他明确命名生态（OpenClaw）"
source_form: "社区 skill、开源仓库、可移植工作流"
compatibility: C
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# 可复现深度学术调研（academic-deep-research）

> 以公开方法和多轮检索开展深度研究。

## 功能说明

要求每个主题至少两轮研究、APA 引用、证据层级和三个用户检查点，强调不是黑箱 API 包装。

## 适用对象与场景

- 适用角色：科研人员、学生、行政研究人员
- 典型场景：背景调研、政策简报、复杂主题综述
- 功能标签：深度调研、双循环检索、证据层级、用户检查点

## 接入判断

- 兼容等级：C
- 适配建议：将 OpenClaw 原生工具替换为 Codex 搜索与读取工具。
- 依赖条件：web_search、web_fetch、会话并行工具
- 风险与边界：范围较宽，若问题界定不清会产生大量低价值材料。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/beita6969/ScienceClaw/blob/main/skills/academic-deep-research/SKILL.md](https://github.com/beita6969/ScienceClaw/blob/main/skills/academic-deep-research/SKILL.md)
- 仓库：[beita6969/ScienceClaw](https://github.com/beita6969/ScienceClaw)
- 仓库元数据：872 stars；最近推送 2026-06-08；许可证 MIT（以仓库当前文件为准）
