---
id: GH-01-0004
category: "学术写作、引用与出版"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills（兼容 Codex）"
source_form: "社区 skill、开源仓库"
compatibility: B
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# Zotero 程序化管理（pyzotero）

> 通过 pyzotero 操作 Zotero 文献库、集合、标签和附件。

## 功能说明

面向 Zotero Web API v3，提供查询、创建、更新、导出和附件管理示例，适合构建课题组文献自动化。

## 适用对象与场景

- 适用角色：科研人员、学生、图书馆人员
- 典型场景：共享文献库维护、参考文献批量导出、标签整理
- 功能标签：Zotero、文献库、标签、附件、API

## 接入判断

- 兼容等级：B
- 适配建议：配置 Zotero API 凭据并限制写操作；先以只读查询接入。
- 依赖条件：pyzotero、Zotero Web API、用户或群组密钥
- 风险与边界：写入和删除会改变文献库；凭据与附件权限需单独管理。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/pyzotero/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/pyzotero/SKILL.md)
- 仓库：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- 仓库元数据：32822 stars；最近推送 2026-08-03；许可证 MIT（以仓库当前文件为准）
