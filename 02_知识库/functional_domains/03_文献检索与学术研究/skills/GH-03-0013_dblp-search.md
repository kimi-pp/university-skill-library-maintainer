---
id: GH-03-0013
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

# DBLP 计算机文献检索（dblp-search）

> 通过 DBLP API 查询计算机科学出版物、作者和会场。

## 功能说明

适合作者成果列表、会议论文集和 CS 书目信息，明确不提供跨学科覆盖和完整引文数。

## 适用对象与场景

- 适用角色：计算机类学生、科研人员、图书馆人员
- 典型场景：CS 文献检索、作者消歧、会议论文集核对
- 功能标签：DBLP、计算机科学、作者、会议、期刊

## 接入判断

- 兼容等级：B
- 适配建议：映射到 Codex HTTP 请求或 find-papers 脚本。
- 依赖条件：DBLP API
- 风险与边界：作者同名和会场别名需要进一步处理。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/beita6969/ScienceClaw/blob/main/skills/dblp-search/SKILL.md](https://github.com/beita6969/ScienceClaw/blob/main/skills/dblp-search/SKILL.md)
- 仓库：[beita6969/ScienceClaw](https://github.com/beita6969/ScienceClaw)
- 仓库元数据：872 stars；最近推送 2026-06-08；许可证 MIT（以仓库当前文件为准）
