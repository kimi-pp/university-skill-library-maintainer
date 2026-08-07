---
id: GH-05-0024
category: "编程、数学、数据分析和可视化"
source_scope: GitHub
status: 入选
ecosystem: "Agent Skills（兼容 Codex、Claude Code、Cursor 等）"
source_form: "社区 skill、GitHub 开源仓库"
compatibility: A
priority: "中"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# Python GPU 性能优化（optimize-for-gpu）

> 先分析性能瓶颈和数据搬运成本，再选择 GPU 库并分阶段优化 Python 工作负载。

## 功能说明

先分析性能瓶颈和数据搬运成本，再选择 GPU 库并分阶段优化 Python 工作负载。 本轮读取了 137 行说明，重点核对了GPU Optimization for Python with NVIDIA、When This Skill Applies、Choosing a Library、Optimization Workflow、1. Profile First。该结论仅反映说明与包结构，不代表依赖已安装或任务已成功运行。

## 适用对象与场景

- 适用角色：学生、教师、科研人员、数据与技术支持人员
- 典型场景：课程作业、科研数据处理、统计建模、机器学习和科学图表
- 功能标签：GPU、性能分析、CUDA、向量化、优化

## 接入判断

- 兼容等级：A
- 适配建议：按 Codex skill 结构接入；固定依赖版本，并为本校数据与算力环境补充预检。
- 依赖条件：Python 及相应科学计算包；部分技能需要 GPU、网络、许可证或较大内存
- 风险与边界：必须先核对数据授权、版本、计算资源和方法假设；示例代码不等同于已验证结果。
- 关联说明：同类技能按任务粒度并存；部署时优先选择覆盖需求且许可证、依赖和维护状态更合适者。

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：读取 137 行 SKILL.md；检查 skill 范围内 16 个文件，其中脚本 0 个、references/assets/templates 资源 15 个。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/optimize-for-gpu/SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/optimize-for-gpu/SKILL.md)
- 仓库：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- 仓库元数据：32822 stars；最近推送 2026-08-03；许可证 MIT（以仓库当前文件为准）
