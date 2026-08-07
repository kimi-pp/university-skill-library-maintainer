---
id: GH-01-0006
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

# 相关工作章节写作（draft-related-work）

> 基于实际检索论文起草或重写 Related Work。

## 功能说明

从论文主张推导应覆盖的研究簇，逐簇说明差异并设置引文下限；空缺主题会返回检索流程。

## 适用对象与场景

- 适用角色：科研人员、研究生
- 典型场景：论文相关工作重构、补齐研究脉络和差异定位
- 功能标签：相关工作、主题聚类、研究差异、引文覆盖

## 接入判断

- 兼容等级：B
- 适配建议：与检索和引文验证技能配套；替换目标学科的章节惯例。
- 依赖条件：find-papers 或现有 BibTeX 文献库
- 风险与边界：检索不足会导致主题失衡；不应生成未核验引文。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills/blob/main/skills/draft-related-work/SKILL.md](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills/blob/main/skills/draft-related-work/SKILL.md)
- 仓库：[ShaishavMaisuria/research-paper-lifecycle-skills](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills)
- 仓库元数据：21 stars；最近推送 2026-06-27；许可证 Apache-2.0（以仓库当前文件为准）
