---
id: GH-03-0003
category: "文献检索与学术研究"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills（兼容 Codex）"
source_form: "社区 skill、开源仓库"
compatibility: C
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# 科研证据包检索（research-lookup）

> 为科研手稿或研究简报汇集当前学术证据。

## 功能说明

默认路由到 Parallel Search/Extract，并把发现、全文证据和深度研究分层，适合为写作准备可追踪研究包。

## 适用对象与场景

- 适用角色：科研人员、研究生
- 典型场景：论文背景证据、竞争结论、研究简报
- 功能标签：证据包、来源提取、背景研究、竞争发现

## 接入判断

- 兼容等级：C
- 适配建议：需替换 Parallel 系列工具或仅保留方法框架。
- 依赖条件：Parallel Search/Extract/Research；可选 Perplexity
- 风险与边界：依赖商业外部服务，未授权材料不应上传。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/research-lookup/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/research-lookup/SKILL.md)
- 仓库：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- 仓库元数据：32822 stars；最近推送 2026-08-03；许可证 MIT（以仓库当前文件为准）
