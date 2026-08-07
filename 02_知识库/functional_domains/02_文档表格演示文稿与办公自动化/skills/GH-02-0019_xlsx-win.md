---
id: GH-02-0019
category: "文档、表格、演示文稿与办公自动化"
source_scope: GitHub
status: 入选
ecosystem: "OpenAI Codex、Anthropic Claude Code"
source_form: "社区 skill、开源仓库"
compatibility: A
priority: "高"
validation: "说明已核验"
as_of: 2026-08-06
---

# Windows 原生 Excel 自动化（xlsx-win）

> 在 Windows 上通过 Microsoft Excel COM 刷新、重算和验证工作簿。

## 功能说明

面向已有连接、缓存值、数据透视、数据模型和计算正确性，强调用真实 Excel 作为最终重算引擎。

## 适用对象与场景

- 适用角色：行政人员、科研人员、信息化人员
- 典型场景：复杂公式重算、现有连接刷新、Excel 环境自检
- 功能标签：Windows、Excel COM、刷新、重算、数据透视

## 接入判断

- 兼容等级：A
- 适配建议：Windows 且安装桌面 Excel 时可直接使用；限制为指定工作簿。
- 依赖条件：Windows、Microsoft 365 Excel、COM
- 风险与边界：会操作真实 Excel 会话；宏执行和 Power Query M 编辑不在支持范围。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/dachent/skills/blob/main/xlsx-win/SKILL.md](https://github.com/dachent/skills/blob/main/xlsx-win/SKILL.md)
- 仓库：[dachent/skills](https://github.com/dachent/skills)
- 仓库元数据：18 stars；最近推送 2026-08-03；许可证 MIT（以仓库当前文件为准）
