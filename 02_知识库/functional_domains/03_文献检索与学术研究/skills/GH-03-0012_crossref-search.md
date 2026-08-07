---
id: GH-03-0012
category: "文献检索与学术研究"
source_scope: GitHub
status: 入选
ecosystem: "其他明确命名生态（OpenClaw）"
source_form: "社区 skill、开源仓库"
compatibility: B
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# Crossref DOI 与出版元数据（crossref-search）

> 通过 Crossref API 查询 DOI、出版物和期刊元数据。

## 功能说明

支持 DOI 解析、作品搜索和出版者信息，明确不用于全文下载。

## 适用对象与场景

- 适用角色：科研人员、学生、图书馆人员
- 典型场景：参考文献校验、DOI 补全、出版元数据核对
- 功能标签：Crossref、DOI、期刊元数据、出版社

## 接入判断

- 兼容等级：B
- 适配建议：替换为 Codex HTTP 或现有 paper-lookup 脚本。
- 依赖条件：Crossref REST API
- 风险与边界：元数据由成员提交，字段可能缺失或存在版本差异。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/beita6969/ScienceClaw/blob/main/skills/crossref-search/SKILL.md](https://github.com/beita6969/ScienceClaw/blob/main/skills/crossref-search/SKILL.md)
- 仓库：[beita6969/ScienceClaw](https://github.com/beita6969/ScienceClaw)
- 仓库元数据：872 stars；最近推送 2026-06-08；许可证 MIT（以仓库当前文件为准）
