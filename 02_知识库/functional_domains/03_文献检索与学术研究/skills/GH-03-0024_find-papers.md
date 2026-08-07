---
id: GH-03-0024
category: "文献检索与学术研究"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills"
source_form: "社区 skill、开源仓库"
compatibility: B
priority: "高"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# 免密钥多源论文检索（find-papers）

> 无需 API 密钥跨四个来源搜索论文、作者、会场和引文。

## 功能说明

附带缓存、限流友好脚本和会场别名表，可查论文集、DOI、引用数与近期预印本。

## 适用对象与场景

- 适用角色：学生、科研人员、图书馆人员
- 典型场景：CS 与跨学科检索、会议论文集、种子论文扩展
- 功能标签：DBLP、Crossref、Semantic Scholar、arXiv、会场别名

## 接入判断

- 兼容等级：B
- 适配建议：引入仓库脚本并按 Codex 路径调整。
- 依赖条件：Python 标准库脚本；公开学术 API
- 风险与边界：公共 API 可能限流，引用数跨平台不可直接比较。
- 关联说明：无

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：检查 skill 目录，共 12 个文件，其中 8 个脚本、3 个 references/assets 资源。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills/blob/main/skills/find-papers/SKILL.md](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills/blob/main/skills/find-papers/SKILL.md)
- 仓库：[ShaishavMaisuria/research-paper-lifecycle-skills](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills)
- 仓库元数据：21 stars；最近推送 2026-06-27；许可证 Apache-2.0（以仓库当前文件为准）
