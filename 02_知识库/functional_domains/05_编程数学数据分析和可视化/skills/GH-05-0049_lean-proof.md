---
id: GH-05-0049
category: "编程、数学、数据分析和可视化"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills（Lean 生态）"
source_form: "社区 skill、GitHub 开源仓库"
compatibility: B
priority: "中"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# Lean 定理证明方法（lean-proof）

> 以小步验证和错误优先策略构造、调试并清理 Lean 形式化证明。

## 功能说明

以小步验证和错误优先策略构造、调试并清理 Lean 形式化证明。 本轮读取了 93 行说明，重点核对了Lean Proof Methodology、One Step at a Time、Error Priority、Work on the Hardest Case First、Across Theorems。该结论仅反映说明与包结构，不代表依赖已安装或任务已成功运行。

## 适用对象与场景

- 适用角色：数学、计算机专业学生与教师、形式化方法研究人员
- 典型场景：Lean 课程、形式化证明、mathlib 贡献与代码审查
- 功能标签：Lean、形式化证明、定理、错误定位、mathlib

## 接入判断

- 兼容等级：B
- 适配建议：对接本校 Lean/mathlib 版本和构建命令，所有证明以实际编译通过为准。
- 依赖条件：Lean 工具链、mathlib 与项目构建环境
- 风险与边界：本轮未编译证明；版本和导入差异会影响结论。
- 关联说明：同类技能按任务粒度并存；部署时优先选择覆盖需求且许可证、依赖和维护状态更合适者。

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：读取 93 行 SKILL.md；检查 skill 范围内 2 个文件，其中脚本 0 个、references/assets/templates 资源 0 个。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/leanprover/skills/blob/main/skills/lean-proof/SKILL.md](https://github.com/leanprover/skills/blob/main/skills/lean-proof/SKILL.md)
- 仓库：[leanprover/skills](https://github.com/leanprover/skills)
- 仓库元数据：61 stars；最近推送 2026-02-25；许可证 Apache-2.0（以仓库当前文件为准）
