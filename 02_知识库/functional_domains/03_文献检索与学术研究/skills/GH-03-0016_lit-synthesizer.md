---
id: GH-03-0016
category: "文献检索与学术研究"
source_scope: GitHub
status: 入选
ecosystem: "其他明确命名生态（OpenClaw）"
source_form: "社区 skill、开源仓库"
compatibility: C
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# 文献搜索与引用图综合（lit-synthesizer）

> 搜索 PubMed 和 bioRxiv，生成摘要、引用图和综述段落。

## 功能说明

把检索、LLM 摘要、引用图构建和写作串成一条紧凑流水线。

## 适用对象与场景

- 适用角色：科研人员、研究生
- 典型场景：快速主题扫描、综述草稿和引用关系探索
- 功能标签：PubMed、bioRxiv、摘要、引用图、综述段落

## 接入判断

- 兼容等级：C
- 适配建议：需要确认仓库列出的脚本和模型依赖；可拆分成独立阶段。
- 依赖条件：Python、学术 API、LLM
- 风险与边界：端到端自动化容易把摘要错误传播到综述文本。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/beita6969/ScienceClaw/blob/main/skills/lit-synthesizer/SKILL.md](https://github.com/beita6969/ScienceClaw/blob/main/skills/lit-synthesizer/SKILL.md)
- 仓库：[beita6969/ScienceClaw](https://github.com/beita6969/ScienceClaw)
- 仓库元数据：872 stars；最近推送 2026-06-08；许可证 MIT（以仓库当前文件为准）
