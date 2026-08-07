---
id: GH-03-0001
category: "文献检索与学术研究"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills（兼容 Codex）"
source_form: "社区 skill、开源仓库"
compatibility: A
priority: "高"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# 多数据库论文检索（paper-lookup）

> 通过十一种学术 API 检索论文、预印本、引文和开放全文。

## 功能说明

按任务路由到 PubMed、Europe PMC、bioRxiv、medRxiv、arXiv、OpenAlex、Crossref、Semantic Scholar、CORE 和 Unpaywall，并保留可复现来源。

## 适用对象与场景

- 适用角色：学生、科研人员、图书馆人员
- 典型场景：查 DOI/PMID、找开放全文、引文网络和主题文献检索
- 功能标签：PubMed、PMC、arXiv、OpenAlex、Crossref、Semantic Scholar

## 接入判断

- 兼容等级：A
- 适配建议：可直接用于 Codex；按 API 可用性启用相应脚本。
- 依赖条件：Python；多个公开学术 API
- 风险与边界：API 覆盖和速率不同，检索结果不等同于质量判断。
- 关联说明：无

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：检查 skill 目录，共 17 个文件，其中 5 个脚本、11 个 references/assets 资源。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/paper-lookup/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/paper-lookup/SKILL.md)
- 仓库：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- 仓库元数据：32822 stars；最近推送 2026-08-03；许可证 MIT（以仓库当前文件为准）
