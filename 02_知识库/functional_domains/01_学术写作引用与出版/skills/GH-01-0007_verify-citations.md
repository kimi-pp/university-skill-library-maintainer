---
id: GH-01-0007
category: "学术写作、引用与出版"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills"
source_form: "社区 skill、开源仓库"
compatibility: B
priority: "高"
validation: "说明已核验"
as_of: 2026-08-06
---

# 参考文献真实性核验（verify-citations）

> 逐条验证 BibTeX 文献并发现虚构、错误和重复条目。

## 功能说明

交叉使用多个学术来源检查 DOI、作者、年份、期刊会议、重复和撤稿信号，并输出修正入口。

## 适用对象与场景

- 适用角色：科研人员、研究生、编辑支持人员
- 典型场景：毕业论文与投稿稿件参考文献审计
- 功能标签：BibTeX、Crossref、DBLP、Semantic Scholar、arXiv

## 接入判断

- 兼容等级：B
- 适配建议：映射到 Codex 可用的检索工具；保留人工打开原始记录步骤。
- 依赖条件：外部学术 API；仓库脚本
- 风险与边界：API 未解析不等于论文不存在，撤稿状态需人工复核。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills/blob/main/skills/verify-citations/SKILL.md](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills/blob/main/skills/verify-citations/SKILL.md)
- 仓库：[ShaishavMaisuria/research-paper-lifecycle-skills](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills)
- 仓库元数据：21 stars；最近推送 2026-06-27；许可证 Apache-2.0（以仓库当前文件为准）
