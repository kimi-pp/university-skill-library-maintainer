---
id: GH-01-0002
category: "学术写作、引用与出版"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills（兼容 Codex）"
source_form: "社区 skill、开源仓库"
compatibility: A
priority: "高"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# 引文与 BibTeX 管理（citation-management）

> 检索论文元数据、验证引文并生成规范 BibTeX。

## 功能说明

覆盖 OpenAlex、PubMed、Google Scholar 等发现路径，提供 DOI 元数据核验、重复检查和多种引文格式流程。

## 适用对象与场景

- 适用角色：学生、科研人员、图书馆人员
- 典型场景：毕业论文参考文献、课题组文献库、投稿前引文核对
- 功能标签：引文检索、DOI、BibTeX、参考文献核验

## 接入判断

- 兼容等级：A
- 适配建议：直接使用流程；外部检索工具按可用性替换。
- 依赖条件：学术数据库或搜索工具；部分流程需要网络
- 风险与边界：数据库覆盖和速率不同；自动格式化仍需抽查。
- 关联说明：无

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：检查 skill 目录，共 21 个文件，其中 8 个脚本、12 个 references/assets 资源。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/citation-management/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/citation-management/SKILL.md)
- 仓库：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- 仓库元数据：32822 stars；最近推送 2026-08-03；许可证 MIT（以仓库当前文件为准）
