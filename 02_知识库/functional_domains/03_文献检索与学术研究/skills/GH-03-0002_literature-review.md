---
id: GH-03-0002
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

# 系统化文献综述（literature-review）

> 跨多个学术数据库开展系统化文献综述并生成报告。

## 功能说明

提供问题界定、数据库策略、筛选、主题综合、引用样式和 Markdown/PDF 报告模板，适用于科学与技术领域。

## 适用对象与场景

- 适用角色：学生、科研人员、图书馆人员
- 典型场景：综述论文、课题背景、系统检索与证据综合
- 功能标签：文献综述、系统检索、研究综合、引文格式

## 接入判断

- 兼容等级：A
- 适配建议：直接复用流程；数据库和 PDF 生成工具按环境配置。
- 依赖条件：学术检索 API；Python PDF 与引用工具
- 风险与边界：完整性依赖检索策略；自动摘要不能替代全文核验。
- 关联说明：无

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：检查 skill 目录，共 12 个文件，其中 5 个脚本、6 个 references/assets 资源。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/literature-review/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/literature-review/SKILL.md)
- 仓库：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- 仓库元数据：32822 stars；最近推送 2026-08-03；许可证 MIT（以仓库当前文件为准）
