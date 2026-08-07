---
id: GH-03-0006
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

# 全文实验数据论文检索（bgpt-paper-search）

> 通过 BGPT MCP 搜索论文并提取结构化实验字段。

## 功能说明

返回方法、结果、样本量、质量评分和结论等二十五类以上字段，面向证据综合和实验细节查找。

## 适用对象与场景

- 适用角色：科研人员、研究生
- 典型场景：系统综述数据提取、实验方法和样本量比较
- 功能标签：BGPT、全文结构化数据、方法、样本量、质量分

## 接入判断

- 兼容等级：C
- 适配建议：需要部署或连接 BGPT MCP；不可用时保留字段模板。
- 依赖条件：BGPT MCP 服务
- 风险与边界：外部抽取质量和覆盖需核验，不能直接作为原始研究证据。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/bgpt-paper-search/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/bgpt-paper-search/SKILL.md)
- 仓库：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- 仓库元数据：32822 stars；最近推送 2026-08-03；许可证 MIT（以仓库当前文件为准）
