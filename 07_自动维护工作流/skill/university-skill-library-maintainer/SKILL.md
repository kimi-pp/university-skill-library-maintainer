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
- 正式推荐、条件候选、需适配候选分别保存和统计。只有正式推荐可自动纳入；`display=false` 或排除 outcome 只能进入非展示审计汇总，排除项名称不进入正式交付。
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

读取规则 → 校验配置哈希 → doctor → 同一长驻进程 prepare → 材料事实观察 → 项目评审决定 → finalize → 逐页视觉决定 → 原子发布 → 仅在有变化或失败时通知

执行细则：

1. 从自动任务提示词取得绝对项目根、绝对 TOML 路径和已应用 SHA-256；重新解析普通路径并重算哈希。
2. 遇到配置哈希不一致、`enabled=false`、`mode=manual`、主台账无效，或重建范围前专业目录门发生变化，立即停止且不发布。
3. `doctor` 通过后启动一次 `run-now` 或 `scheduled-run`，并保持同一长驻进程直到终态。不得跨进程执行或把 `prepare`、`apply-reviews`、`finalize` 拆成独立命令，也不得从磁盘恢复审查 capability。
4. 收到 `material_review_required` 后，只读检查其中逐个 `SKILL.md` 入口列出的固定包路径、固定版本、内容哈希、快照清单、候选精确来源证据和静态文件；市场元数据、搜索响应 JSON 和未固定默认分支不是 Skill 内容。根级 Skill 须覆盖除明确嵌套独立 Skill 子树和仓库元数据外的全部相关文件，嵌套 Skill 只审自身子树。按当前 run ID 精确回传 `material_observations`，逐项给出许可证与安全事实。无完整固定包或无可识别入口的候选只保留观察，不构造事实或 ReviewPacket。
5. 程序用仍存活的快照 capability 构建、绑定当前 PreparedRun 并一次性消费可信 ReviewPacket 后，才会发出 `review_required`。依据项目规则、固定证据和六维专业任务画像回传专业相关性、层级、分数、完整 ledger row，以及每个批准范围的人工任务映射（候选 ID、专业代码/名称、任务、输入、输出、理由、限制、相关度）。名称关键词不能替代专业任务判断。正式、条件、需适配都必须绑定同一候选身份和映射；三级展示项的名称、日期、原因和限制须完整。实质不相关、相关度低于 3、禁止风险或明确不展示的项目应返回 `outcome=exclude`、`display=false`、`direct=false` 及结构化中文排除原因，不得伪装成三级展示项。
6. 把材料事实与项目判断分别保存在上述两个结构化标准输入帧中；不要通过命令行参数、临时业务数据库或自由文本旁路提交。
7. 调用工作区依赖加载器，把其原始返回文本和绝对项目根传给 `build_workspace_renderer_command(loader_output, project_root)`。该接口只读取加载器明确返回的 Python、Python packages、override binaries 和 fallback binaries，验证普通路径并解析其中固定的 Poppler 包装入口，再用项目自带 `pdf_renderer.py` 构造 Task 11 的 `RendererCommand.argv`。把该命令交给 `finalize`；不得从 PATH、用户名或缓存布局猜测路径。
8. 收到 `word_visual_review_required` 后逐张检查最新生成的 Word `page-<N>.png`，对每页明确批准或拒绝。缺页、空白页、裁切、表格越界、页脚重叠或哈希不一致均拒绝发布。
9. EOF、异常或任一闸失败时让同一进程只清理该 run 的快照 capability、ReviewPacket、暂存和锁。发布时确认来源请求证据、固定归档、逐入口快照和清单已进入 generation authority，台账相对路径在暂存删除后仍可解析且哈希匹配；后续运行保留仍被引用的前代 generation。完全无变化且成功时静默结束；只在变化、人工决定事项、覆盖显著下降或失败时通知。

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
| Word 能打开就直接发布 | 用加载器返回字段构造项目渲染命令，并逐页检查 |
