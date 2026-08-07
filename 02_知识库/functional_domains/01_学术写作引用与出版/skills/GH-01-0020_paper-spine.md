---
id: GH-01-0020
category: "学术写作、引用与出版"
source_scope: GitHub
status: 入选
ecosystem: "OpenAI Codex、Anthropic Claude Code、其他明确命名生态（OpenClaw、Hermes CLI）"
source_form: "社区 skill、开源仓库、跨生态可移植工作流"
compatibility: A
priority: "高"
validation: "二级包内容验证"
as_of: 2026-08-06
---

# 贡献主线驱动的论文构建与重写（paper-spine）

> 围绕已确认的核心贡献和研究动机构建、重写并审计论文或研究报告。

## 功能说明

提供已有稿件重写和基于材料从头构建两条主流程；先建立本地材料清单、引用支持库、贡献与动机主线，再生成章节蓝图、写作理由矩阵和正文，并通过结果验证、完整性、审稿风险、LaTeX、Word 与最终产物检查门。

## 适用对象与场景

- 适用角色：学生、科研人员、教学与科研支持人员
- 典型场景：论文从材料到初稿、重大结构重写、投稿前证据与审稿风险审计
- 功能标签：论文主线、贡献确认、证据库、章节蓝图、审稿审计

## 接入判断

- 兼容等级：A
- 适配建议：Codex 入口可直接采用；高校部署宜固定提交版本，按本地工具调整外部终端配置界面，并默认停用跟随 main 的自动更新。
- 依赖条件：Python；网络检索；按输出选择 LaTeX/PDF 或 Pandoc/Word 工具链
- 风险与边界：流程较重且会生成较多中间产物；无固定 GitHub Release；macOS 配置界面存在公开问题；不得把 humanize 用作检测规避，也不得虚构证据或绕过付费墙。
- 关联说明：与 GH-01-0005 都覆盖论文编排，但本项更强调贡献—动机主线、证据支持库和可审计的硬检查门。

## 功能验证

- 验证层级：二级包内容验证
- 验证结果：读取 V4 主入口并检查仓库目录：src/skill 共 55 个文件，其中 references 47 个；src/scripts 共 28 个脚本；仓库递归目录共 468 个文件。
- 运行状态：未安装、未运行；如需最小运行验证，须另行取得用户指令。

## 来源

- Skill 地址：[https://github.com/WUBING2023/PaperSpine/blob/main/src/skill/SKILL.md](https://github.com/WUBING2023/PaperSpine/blob/main/src/skill/SKILL.md)
- 仓库：[WUBING2023/PaperSpine](https://github.com/WUBING2023/PaperSpine)
- 仓库元数据：4663 stars；最近推送 2026-07-28；许可证 MIT（以仓库当前文件为准）
