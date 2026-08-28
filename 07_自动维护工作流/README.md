# 高校专业 Skill 库文件化自动维护

本目录提供 Windows 上的文件化维护工作流。Excel 主台账是唯一业务基线；每轮只读发现和静态审核候选，经结构化人工审核、Microsoft Office 验证和 Word 逐页视觉复核后，才原子发布新的主台账与中文 Word/Excel 交付物。工作流不使用业务数据库，也不会安装或执行候选 Skill。

## 当前启用边界

Task 13 已提供安装、诊断、设置、状态、修复、离线重建和同进程双闸运行协议。但四个平台的生产发现驱动尚未接通：市场元数据不能冒充固定版本 Skill 包，也不能绕过固定上游快照生成受信 ReviewPacket。因此，在 Task 14 完成生产驱动验收前：

- `doctor` 和 `status` 会明确显示“生产发现驱动未配置”；
- `run-now`、`scheduled-run` 会在 `prepare` 之前以操作失败退出，不联网、不创建暂存运行；
- 不得启用或创建自动任务，不能宣称自动维护已可投产。

这项限制不影响安装检查、既有交付盘点、TOML 编辑、台账备份检查或严格离线的报告重建。

## 前置条件

- Windows 10/11；生产调度只允许在 Windows 上运行。
- 64 位 Python 3.11、3.12 或 3.13，并可创建 `venv`。
- Python 环境须能取得 `requirements.txt` 固定的全部版本；完全离线安装时，这些包必须已存在于所给 Python 的系统 site-packages，或由使用者预先提供可用 wheelhouse。
- Microsoft Word 和 Excel 桌面版，且已正确注册 COM。
- GitHub CLI `gh` 可从当前 PowerShell 会话调用。
- Codex 桌面应用；涉及 Word 渲染时，必须取得当前 Codex 工作区依赖加载器的真实返回文本。
- 目标项目根目录必须包含并可完整读取以下用户维护的规则：
  1. `AGENTS.md`
  2. `01_规则/SKILL_RESEARCH_WORKFLOW.md`
  3. `01_规则/SECURITY_REVIEW_PROTOCOL.md`
  4. `01_规则/DATA_DICTIONARY.md`
  5. `01_规则/REPORTING_STANDARD.md`

安装器不会从模板、旧报告或其他机器复制或伪造这些规则。任一规则缺失、为空、不可读、是链接/重解析点，均关闭失败。

## 安装

在 PowerShell 中显式填写项目根、Python 和 Codex Skills 根目录；中文与空格路径均受支持：

```powershell
$ProjectRoot = 'D:\高校AI工作台\高校AI技能库调研'
$PythonExe = 'C:\Python312\python.exe'
$CodexSkillsRoot = Join-Path $env:USERPROFILE '.codex\skills'

powershell -NoProfile -ExecutionPolicy Bypass -File "$ProjectRoot\07_自动维护工作流\install.ps1" `
  -ProjectRoot $ProjectRoot `
  -PythonExe $PythonExe `
  -CodexSkillsRoot $CodexSkillsRoot
```

参数严格为 `-ProjectRoot -PythonExe [-CodexSkillsRoot]`。省略 `-CodexSkillsRoot` 时，安装器只使用 `CODEX_HOME\skills`；若未设置 `CODEX_HOME`，使用当前 Windows 用户配置目录下的 `.codex\skills`，不猜测用户名或缓存布局。

安装器执行以下幂等操作：

- 在本目录创建或复用 `.venv`；
- 安装调用链临时清空并在 `finally` 恢复 `PYTHONPATH`、`PYTHONHOME`、`PYTHONUSERBASE`，所有 Python 业务调用均使用隔离模式 `-I`；按 `requirements.txt` 的精确版本安装依赖。若目标 venv 已提供 `wheel`，执行 `pip -e --no-build-isolation --no-deps`；没有 `wheel` 时，在该 venv 内原子写入指向本项目 `src` 的 ASCII `.pth`，形成不复制源码的等价 editable 链接；两种路径都只交付并验证调用 `python.exe -I -m skill_maintainer.cli` 的 installer-owned `Scripts\skill-maintainer.cmd`；
- 将完整 Skill 包复制到同级私有暂存树，逐文件校验哈希和普通路径后再目录级切换；切换完成即为新版本提交点；提交前失败时，仅在目标仍为空且旧目录身份精确匹配本次切换记录时原子恢复旧版，若目标被占用则保留目标、旧版和暂存路径并明确报错，绝不为回滚删除未知内容；成功提交后完整新版本保持生效，旧版 `.previous` 保留并在结果中报告待人工处理；后续安装也只报告精确命名的遗留路径及其普通目录/重解析点状态，不读取其内容，不自动删除、移动或覆盖；用户应在确认无人使用并自行备份后手工处理；
- 仅补齐缺失的 `workflow-settings.toml`、`ledger`、`ledger/archive` 和 `output`；
- 配置首次创建时保持 `enabled=false`、`mode="manual"`，既有配置绝不覆盖；
- 最后运行 `doctor`；不创建、不更新、不启用任何自动任务。

安装器会在任何 venv、设置或 Skill 写入前检查项目根、脚本根、Python、Codex Skills 根及全部既存祖先，任一 symlink/junction/重解析点都会关闭失败。安装器不会覆盖并非由它创建的同名 `.pth` 或 `.cmd`；安装后还会在清洁环境中验证 `skill_maintainer.__file__` 确实位于当前目标项目的 `07_自动维护工作流\src`，并实际执行 CLI `--help` 和 `doctor`。安装完成后重新打开 Codex 任务，使 Skill 加载器读取更新后的包。项目自带的 `workspace_renderer.py`、`pdf_renderer.py` 和依赖定义必须随工作流一起保留。

## 命令与退出码

以下示例使用安装后的项目 Python，且所有命令都要求显式 `--project-root`：

```powershell
$CliPython = "$ProjectRoot\07_自动维护工作流\.venv\Scripts\python.exe"
& $CliPython -I -m skill_maintainer.cli status --project-root $ProjectRoot
```

公开命令固定为：

| 命令 | 作用 |
|---|---|
| `setup` | 仅补齐缺失结构和默认禁用/手动配置；可用 `--codex-skills-root` 更新 Skill |
| `import-existing` | 保守盘点既有交付，或在指定暂存路径生成首次导入候选 |
| `doctor` | 检查 Python、Word、Excel、`gh`、规则、台账、设置、renderer 和生产驱动 |
| `edit-settings` | 打开中文 TOML 设置编辑器 |
| `apply-settings` | 只校验设置并输出 schedule、prompt、配置 SHA-256 和自动任务动作计划 |
| `run-now` | 同一受信进程内执行 prepare → 人工审核 → Office/逐页审核 → finalize |
| `scheduled-run` | 供已绑定配置哈希的自动任务调用同一完整协议 |
| `status` | 查看计划预览、最近运行、最新交付与生产驱动状态 |
| `repair-ledger` | 只列有效备份；明确选择后生成恢复候选，不覆盖主台账 |
| `rebuild-report` | 只读当前主台账、零网络重建 Word/Excel 报告 |

退出码含义固定：`0` 成功，`1` 操作失败，`2` 输入或配置无效，`3` 安全无操作。内部 `prepare`、`apply-reviews`、`finalize` 不能跨进程单独调用；CLI 会拒绝重建运行时 capability。

## 首次导入既有交付

先只做盘点，不写台账：

```powershell
& $CliPython -I -m skill_maintainer.cli import-existing --project-root $ProjectRoot --inventory-only
```

确认文件数、重复组、Word 不确定项和 Word/Excel 数量差异后，才可显式输出到 `ledger\staging` 下的全新文件：

```powershell
$Candidate = "$ProjectRoot\07_自动维护工作流\ledger\staging\首次导入候选.xlsx"
& $CliPython -I -m skill_maintainer.cli import-existing --project-root $ProjectRoot --output $Candidate
```

默认不带 `--inventory-only` 或 `--output` 时返回安全无操作。输出已存在、路径不在暂存区或解析存在不确定性时，不得自动覆盖正式主台账；必须由用户核查后决定后续处理。CLI 在创建缺失的嵌套目录前逐段验证项目内包含关系和链接/重解析点，拒绝经 junction 写到项目外。

## 编辑并应用运行设置

```powershell
& $CliPython -I -m skill_maintainer.cli edit-settings --project-root $ProjectRoot
& $CliPython -I -m skill_maintainer.cli apply-settings --project-root $ProjectRoot --loader-output '<工作区依赖加载器的原始返回文本>'
```

可修改 `workflow.enabled`、`schedule.mode` 和 `schedule.start_time`，以及周、月或间隔参数。运行频率与启动时间都在 `workflow-settings.toml` 中设置，不使用 `.xlsx` 作为配置文件。

`apply-settings` 绝不直接写原始自动任务，也不声称已经应用。它只返回经过验证的 schedule、渲染 prompt、TOML SHA-256、完整 doctor 结果、动作计划和“必须回读”标记。`production_ready` 同时要求 Windows、Python、`gh`、Word、Excel、五项规则、设置、台账、真实 loader-bound renderer 和可调用的生产驱动全部通过，不能只依据驱动工厂存在。随后必须由 Task 12 Skill 调用 Codex 应用的自动任务更新能力，并回读核对项目根、计划、提示词和配置哈希。当前生产发现驱动未就绪，动作计划为启用时会失败；不要创建自动任务。

## 手动运行与长驻双闸协议

生产驱动接通后，Codex Skill 才可调用：

```powershell
& $CliPython -I -m skill_maintainer.cli run-now --project-root $ProjectRoot --loader-output '<工作区依赖加载器的原始返回文本>'
```

该命令保持一个进程存活：`prepare` 后输出一行 JSON 并等待逐候选结构化决定；`apply_reviews` 后完成报告和 Office 验证，在 Word 页面 PNG 就绪后再次输出一行 JSON 并等待每页决定；最后才 `finalize`。任一决定缺失、重复、哈希不绑定、页面拒绝、标准输入 EOF、`KeyboardInterrupt`、`SystemExit` 或其他失败，都终态清理未提交暂存和锁；清理诊断只附注原异常，不会掩盖它。发布线性化已经成功时不会误删已提交主台账或 generation。

CLI 本身从不执行候选。Codex 只可静态读取固定版本快照、证据和已批准的规则字段。

## 状态、诊断、备份与重建

```powershell
& $CliPython -I -m skill_maintainer.cli doctor --project-root $ProjectRoot
& $CliPython -I -m skill_maintainer.cli status --project-root $ProjectRoot --loader-output '<工作区依赖加载器的原始返回文本>'
& $CliPython -I -m skill_maintainer.cli repair-ledger --project-root $ProjectRoot
& $CliPython -I -m skill_maintainer.cli rebuild-report --project-root $ProjectRoot
```

`doctor`、`status` 和 `apply-settings` 不从 PATH、固定用户名或 Codex 缓存布局猜测 renderer。只有在当前 Codex 环境取得工作区依赖加载器真实文本后，才可传入 `--loader-output` 验证 loader-bound renderer 前置条件。`status` 的“最新交付”只取最后一条成功运行记录绑定的 generation，并重新验证项目内包含关系、普通文件树、manifest SHA-256、delivery SHA-256 和 authority 文件集合；任意目录或篡改 generation 只会得到明确错误和 `latest_output=null`。

`repair-ledger` 首次调用只列出具备独立发布绑定的归档备份，并返回安全无操作。主台账可读时，备份 SHA-256 必须精确匹配成功运行记录中的“快照SHA-256”，且对应 generation/manifest/delivery 复验通过；主台账已损坏或不可解析时，只允许备份自身结构有效、最后一条运行记录为成功、且该记录对应发布代次复验通过的旧 authority。仅有有效 Excel schema 而没有成功发布证据的文件不会放行。用户明确选定其中一个后再运行：

```powershell
& $CliPython -I -m skill_maintainer.cli repair-ledger --project-root $ProjectRoot --backup 'D:\...\ledger\archive\Skills主台账_20260829_010203.xlsx'
```

扫描备份时，命令从单一文件句柄一次取得不可变字节快照，绑定句柄身份、路径身份和 SHA-256，并仅从同一份内存字节完成 schema、运行记录和 generation authority 复验；选择后的恢复候选也只写这份初始快照。路径替换、原地改写或发布证据不匹配均拒绝。恢复候选先写同目录私有暂存文件、复读后再切换到 `ledger\recovery`，不会自动替换 `ledger\Skills主台账.xlsx`。`rebuild-report` 严格只读当前主台账、零网络，不重新发现候选；Word/Excel 先在同级私有目录完整生成后再目录级切换，可用 `--output` 指定项目内全新输出目录，已有目标拒绝覆盖。失败时只逆序清理本次创建、身份未变化且仍为空的嵌套祖先，既有目录不会删除。

## 迁移到另一台机器

1. 停用并回读确认旧机器上的项目自动任务不存在。
2. 关闭写入进程，复制完整项目目录，包括规则、工作流、主台账、归档和交付；不要复制正在运行的锁或自行拼接零散文件。
3. 在新机器用新绝对路径再次运行 `install.ps1`。editable 链接绑定当前机器的项目路径，不能沿用旧机器链接；`.venv` 应由新机器重新建立。如复制包中含旧 `.venv`，先由用户确认并安全移除后再安装。
4. 运行 `doctor`、`status`，重新取得该机器的真实 loader 输出，并执行 `apply-settings` 生成新路径绑定和配置 SHA-256。
5. 只有 Task 14 生产驱动验收通过且全部诊断通过后，才由 Codex 应用更新并回读自动任务。

文件本身就是可迁移状态；没有需要搬迁的数据库。

## 停用与卸载

停用时把 `workflow.enabled` 设为 `false`、`schedule.mode` 设为 `manual`，运行 `apply-settings`，再由 Codex 应用删除本项目自动任务并回读确认不存在。

卸载前保留 `ledger\Skills主台账.xlsx`、`ledger\archive` 和需要的 `output`。确认没有进程持有工作流后，可由用户删除项目内 `.venv`，以及 Codex Skills 根目录中的 `university-skill-library-maintainer`。不要删除规则、主台账、归档或既有交付；installer 与 CLI 均不会自动执行这些删除操作。
