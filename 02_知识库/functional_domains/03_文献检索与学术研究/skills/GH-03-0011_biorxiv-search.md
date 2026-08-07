---
id: GH-03-0011
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

# bioRxiv 语义检索（biorxiv-search）

> 用自然语言语义检索 bioRxiv 生命科学预印本。

## 功能说明

通过 Valyu 驱动的脚本返回与自然语言查询相关的 bioRxiv 结果，适合发现关键词难以覆盖的研究。

## 适用对象与场景

- 适用角色：科研人员、研究生
- 典型场景：生命科学前沿追踪、预印本发现
- 功能标签：bioRxiv、生命科学、预印本、语义检索

## 接入判断

- 兼容等级：C
- 适配建议：需要配置 Valyu；也可改为 bioRxiv 官方 API 关键词检索。
- 依赖条件：Valyu 服务与仓库脚本
- 风险与边界：商业语义搜索的排序和覆盖不可完全复现。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/beita6969/ScienceClaw/blob/main/skills/biorxiv-search/SKILL.md](https://github.com/beita6969/ScienceClaw/blob/main/skills/biorxiv-search/SKILL.md)
- 仓库：[beita6969/ScienceClaw](https://github.com/beita6969/ScienceClaw)
- 仓库元数据：872 stars；最近推送 2026-06-08；许可证 MIT（以仓库当前文件为准）
