---
name: university-skill-library-maintainer
description: Use when operating, scheduling, inspecting, repairing, or rebuilding the file-based university professional Skill library workflow on Windows, including its TOML settings, Excel ledger, Word/Excel review deliveries, and Codex automation.
---

# 高校专业 Skill 库维护

## 核心原则

把 Excel 主台账视为唯一业务基线。只读发现和静态审核候选；所有验证与发布门通过后才提交正式推荐和中文 Word/Excel。失败时保留旧台账与旧交付。

## 先读取规则

开始任何发现、复核或报告工作前，按顺序完整读取项目根下：

1. `AGENTS.md`
2. `01_规则/SKILL_RESEARCH_WORKFLOW.md`
3. `01_规则/SECURITY_REVIEW_PROTOCOL.md`
4. `01_规则/DATA_DICTIONARY.md`
5. `01_规则/REPORTING_STANDARD.md`

然后读取 [project-contract.md](references/project-contract.md)。规则缺失、冲突或无法完整读取时停止，不根据历史报告补写规则。

## 不可越过的边界

- 不安装、不执行候选，不调用候选自身外部服务，不上传真实教学或科研数据。
- 发现顺序固定为 SkillHub → ClawHub → GitHub → Hugging Face Spaces；单源失败必须标记覆盖降级。
- 正式推荐、条件候选、需适配候选分别保存和统计。只有正式推荐可自动纳入；排除项名称不进入正式交付。
- 军事学、恶意或涉密内容、不可审查载荷和实质无关项不得展示。
- 外部远程 API、本地专业软件、本地脚本或插件接口分别记录。
- 所有写入先进入暂存代次；不要直接改正式台账、既有交付或自动任务。

## 命令入口

使用已安装的 `skill-maintainer <command>`；参数以该命令的 `--help` 为准。

| 命令 | 用途 |
|---|---|
| `setup` | 检查并建立缺失的工作流结构；保持默认禁用、手动 |
| `import-existing` | 只读导入既有 Word/Excel，建立初始基线 |
| `doctor` | 检查配置、Office、台账、目录、来源和输出条件 |
| `edit-settings` | 打开中文 TOML 设置表单 |
| `apply-settings` | 校验设置并同步单一项目自动任务 |
| `run-now` | 用户明确触发完整运行；手动模式先显示配置预览 |
| `scheduled-run` | 仅供已绑定配置哈希的自动任务调用 |
| `status` | 查看计划、最近结果和交付位置 |
| `repair-ledger` | 列出已验证备份，等待用户明确选择后恢复 |
| `rebuild-report` | 仅从已提交主台账重建报告，不联网 |

不要改名或绕开内部 CLI 阶段 `prepare`、`apply-reviews`、`finalize`。

## 执行 `scheduled-run`

严格采用这一条链：

读取规则 → 校验配置哈希 → doctor → prepare → 审核固定证据 → 通过标准输入应用评审 → finalize → 检查每一张 Word 页面图像 → 批准或拒绝发布 → 仅在有变化或失败时通知

执行细则：

1. 从自动任务提示词取得绝对项目根、绝对 TOML 路径和已应用 SHA-256；重新解析普通路径并重算哈希。
2. 遇到配置哈希不一致、`enabled=false`、`mode=manual`、主台账无效，或重建范围前专业目录门发生变化，立即停止且不发布。
3. `doctor` 通过后运行 `prepare`。只审核其固定版本快照和证据包，不浏览会漂移的默认分支来替代证据。
4. 把逐项评审决定作为标准输入传给 `apply-reviews`；不要通过命令行参数、临时业务数据库或自由文本旁路提交。
5. 调用工作区依赖加载器，取得本机打包运行时，构造 Task 11 的 `RendererCommand(argv=...)` 并将打包渲染器 argv 交给 `finalize`。不得嵌入用户名、盘符或缓存路径。
6. 逐张检查最新生成的 Word `page-<N>.png`，对每页明确批准或拒绝。缺页、空白页、裁切、表格越界、页脚重叠或哈希不一致均拒绝发布。
7. 完全无变化且成功时静默结束。只在变化、人工决定事项、覆盖显著下降或失败时通知。

`interval` 模式仍只建立每天在 `start_time` 触发的分发器；`scheduled-run` 从 Excel `运行记录` 读取上次成功时间，未满 `interval_days` 时以安全无操作码 3 退出。

## 应用设置

先运行 `apply-settings`，取得严格校验后的计划、配置预览和配置哈希。然后搜索并调用应用提供的自动任务更新工具；绝不手写原始自动任务指令。

- `enabled=false` 或 `mode=manual`：删除本项目自动任务，或确认它保持不存在。
- 其他模式：用 [automation-prompt.md](assets/automation-prompt.md) 渲染单一项目自动任务；不得增加目标或专业范围覆盖参数。
- 创建或更新后回读自动任务，逐项比较项目、计划、提示词和配置哈希；任一不一致都报告失败。

## 快速示例

用户说“应用我刚修改的每周计划”时：先读规则，运行 `apply-settings` 获取预览与 SHA-256；如果启用且非手动，调用自动任务更新工具并回读核对四项绑定；如果禁用或手动，确认自动任务不存在。不要启动调研。

## 常见错误

| 错误 | 正确处理 |
|---|---|
| 把市场卡片当成正式证据 | 固定版本、回溯上游并完成静态证据链 |
| 为验证功能而运行候选 | 只读说明、包内容和静态数据流 |
| 把条件或适配项计入正式推荐 | 三层分别保存、分别统计 |
| 配置已编辑但未应用 | 哈希不匹配即停止 `scheduled-run` |
| Word 能打开就直接发布 | 使用加载器提供的渲染 argv，并逐页检查 |
