---
id: GH-02-0015
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

# 多格式批量转换（batch-convert）

> 通过统一流程批量转换多种办公文档格式。

## 功能说明

提供输入扫描、格式选择、错误隔离、结果汇总和质量检查思路，适合大量材料迁移。

## 适用对象与场景

- 适用角色：行政人员、图书馆人员、教学人员
- 典型场景：历史材料迁移、课程文件统一格式、档案批处理
- 功能标签：批量转换、格式路由、文件队列

## 接入判断

- 兼容等级：B
- 适配建议：需要绑定实际转换工具；先对副本运行并保存失败清单。
- 依赖条件：LibreOffice、Pandoc 或相应格式库
- 风险与边界：转换可能造成样式或嵌入对象损失；仓库未附专用脚本。
- 关联说明：无

## 功能验证

- 验证层级：说明已核验
- 验证结果：已读取 SKILL.md 或仓库说明，确认功能定位、输入输出、依赖与边界。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/claude-office-skills/skills/blob/main/batch-convert/SKILL.md](https://github.com/claude-office-skills/skills/blob/main/batch-convert/SKILL.md)
- 仓库：[claude-office-skills/skills](https://github.com/claude-office-skills/skills)
- 仓库元数据：362 stars；最近推送 2026-01-31；许可证 MIT（以仓库当前文件为准）
