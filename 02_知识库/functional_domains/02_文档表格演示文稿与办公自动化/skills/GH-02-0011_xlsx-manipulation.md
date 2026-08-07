---
id: GH-02-0011
category: "文档、表格、演示文稿与办公自动化"
source_scope: GitHub
status: 入选
ecosystem: "Anthropic Claude Code"
source_form: "社区 skill、开源仓库"
compatibility: B
priority: "中"
validation: "说明已核验"
as_of: 2026-08-06
---

# openpyxl 表格操作（xlsx-manipulation）

> 使用 openpyxl 程序化创建和编辑 Excel 工作簿。

## 功能说明

覆盖单元格、样式、公式、图表和多表处理，适合将重复表格任务转成脚本化流程。

## 适用对象与场景

- 适用角色：行政人员、科研人员、学生
- 典型场景：台账、调查数据、批量工作簿和报表生成
- 功能标签：openpyxl、Excel、公式、样式

## 接入判断

- 兼容等级：B
- 适配建议：改写工具调用并增加公式重算与渲染门。
- 依赖条件：openpyxl
- 风险与边界：openpyxl 不计算公式，复杂 Excel 对象可能丢失。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/claude-office-skills/skills/blob/main/xlsx-manipulation/SKILL.md](https://github.com/claude-office-skills/skills/blob/main/xlsx-manipulation/SKILL.md)
- 仓库：[claude-office-skills/skills](https://github.com/claude-office-skills/skills)
- 仓库元数据：362 stars；最近推送 2026-01-31；许可证 MIT（以仓库当前文件为准）
