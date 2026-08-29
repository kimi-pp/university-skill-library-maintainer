# 高校专业 Skill 库文件化自动维护

本目录提供 Windows 上的文件化维护工作流。Excel 主台账是唯一业务基线；每轮只读发现和静态审核候选，经结构化人工审核、Microsoft Office 验证和 Word 逐页视觉复核后，才原子发布新的主台账与中文 Word/Excel 交付物。工作流不使用业务数据库，也不会安装或执行候选 Skill。

## 当前启用边界

四个平台的生产发现驱动已经接通并通过离线端到端验收。它按固定顺序检索 SkillHub、ClawHub、GitHub、Hugging Face Spaces；由已批准目录和 Excel 中的六维任务画像生成查询，执行水位增量或到期全量复核，并保存每个来源的真实请求、证据与状态。单一来源故障时继续其余来源；全部来源失败时关闭失败。全局去重后，同一上游仓库中的每个可识别 `SKILL.md` 入口分别拥有一个稳定 ID；市场条目只有绑定同一规范上游和同一入口时才合并。

生产运行仍保持人工、禁用状态：`workflow.enabled=false`、`schedule.mode="manual"`。安装、诊断和本轮验收不会创建、更新或启用自动任务；只有用户另行明确批准、全部诊断通过并由 Codex 应用更新能力回读核对后，才可改变该状态。候选 Skill 始终只做静态读取，不安装、不执行。

市场元数据只能作为候选观察材料。只有可追溯到规范上游、具体 `SKILL.md` 入口且取得完整固定包的候选才可进入固定包审查；GitHub 包必须固定到 commit SHA。根级 Skill 的审查快照包含除明确的嵌套独立 Skill 子树和仓库元数据外的全部相关文件，嵌套 Skill 只包含自身子树。不能取得完整固定包的 SkillHub、ClawHub 或 Hugging Face 条目只进入待审查或条件观察，并写明原因，不能生成受信 ReviewPacket，也不能正式纳入。

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
$ProjectRoot = (Get-Location).Path  # 请先切换到项目根目录
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
| `doctor` | 检查 Python、Word、Excel、`gh`、规则、台账、设置、renderer 和生产驱动；加 `--network` 时只读探测四个平台和教育部目录来源 |
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

`apply-settings` 绝不直接写原始自动任务，也不声称已经应用。它只返回经过验证的 schedule、渲染 prompt、TOML SHA-256、完整 doctor 结果、动作计划和“必须回读”标记。`production_ready` 同时要求 Windows、Python、`gh`、Word、Excel、五项规则、设置、台账、真实 loader-bound renderer 和可调用的生产驱动全部通过，不能只依据驱动工厂存在。随后必须由 Task 12 Skill 调用 Codex 应用的自动任务更新能力，并回读核对项目根、计划、提示词和配置哈希。默认禁用、手动设置不会自行创建自动任务。

## 手动运行与长驻三闸协议

完成安装和诊断后，Codex Skill 可在用户明确要求时调用：

```powershell
& $CliPython -I -m skill_maintainer.cli run-now --project-root $ProjectRoot --loader-output '<工作区依赖加载器的原始返回文本>'
```

该命令保持一个受信进程存活，不能跨进程从磁盘恢复 capability：

1. `prepare` 在锁内为本轮建立私有暂存，发现候选并为可固定候选创建不可变快照；随后输出 `material_review_required`，包含逐入口路径、SHA-256、快照清单和绑定标识。既有正式项、条件候选、需适配候选、已排除版本和已记录版本别名都参加版本复核；同一仓库只做一次版本查询和固定包下载，逐入口比较各自已审版本，已是最新的入口不重复进入材料审查。
2. Codex 只读固定包和规则，回传许可证、安全、规范上游等可观察事实。进程校验事实与本轮包、当前 PreparedRun 和精确候选证据的绑定后，才在内存中构建一次性受信 ReviewPacket，并输出 `review_required`。Codex 再依据专业核心任务映射、项目规则和固定证据回传 `formal`、`condition`、`adaptation` 或拒绝决定；决定候选标识必须唯一并精确覆盖本轮全部受信包，集合不全、额外或重复会在任何账本 shadow 写入和回执签发前拒绝。程序不以名称关键词替代专业判断。`display=false` 和排除 outcome 只写非展示审计，不得进入产品候选；三级展示项必须具有完整中文名称、日期、原因、使用限制和人工确认的专业任务映射。
3. 程序生成 Excel/Word，经真实 Office 打开后把 Word 转为 PDF 和逐页 PNG，输出 `page_review_required`。Codex逐页确认后，程序才执行 `finalize` 和原子发布。

无固定包的候选仍记录来源覆盖与条件观察，但不能进入正式层。上游仓库或既有 Skill 入口删除时保留旧正式版本或旧观察，并写入带版本、入口和候选精确证据的关注项。既有正式条目的条件、需适配、排除和删除关注结论都进入日报及每个已映射专业类的“发现新版本但未升级”，旧正式行继续保留且不重复列为新候选。任一事实或决定缺失、重复、哈希不绑定、页面拒绝、标准输入 EOF、`KeyboardInterrupt`、`SystemExit` 或其他失败，都终态清理该 run 的未提交快照能力、ReviewPacket、暂存和锁；即使失败发生在 PreparedRun 注册之前，也按本轮暂存身份精确撤销已创建的 manifest，不影响其他 run。清理诊断只附注原异常，不会掩盖它。发布线性化已经成功时不会误删已提交主台账或 generation。

发布时，本轮实际采用的来源请求证据、固定归档、逐入口快照及快照清单随 Word/Excel 一起进入 `output/generations/<run-id>/authority`，台账只保存可从 generation 解析的相对路径及内容哈希。长期 generation manifest 只记录相对路径、SHA-256、字节数和逻辑角色，不保存设备号、inode 或 mtime；每次复验在当前机器重新建立普通文件句柄身份并检查读取前后稳定性，因此复制到另一台机器后仍可验证。暂存目录删除后，当前项、候选观察和版本历史中的每条证据仍须存在且哈希匹配；每次启动在联网和建立 run 暂存前复核最新成功代次以及所有仍被业务表引用的前代 generation，未被引用的旧代按保留策略不阻断运行。

CLI 本身从不执行候选。Codex 只可静态读取固定版本快照、证据和已批准的规则字段。

## 状态、诊断、备份与重建

```powershell
& $CliPython -I -m skill_maintainer.cli doctor --project-root $ProjectRoot
& $CliPython -I -m skill_maintainer.cli doctor --project-root $ProjectRoot --network
& $CliPython -I -m skill_maintainer.cli status --project-root $ProjectRoot --loader-output '<工作区依赖加载器的原始返回文本>'
& $CliPython -I -m skill_maintainer.cli repair-ledger --project-root $ProjectRoot
& $CliPython -I -m skill_maintainer.cli rebuild-report --project-root $ProjectRoot
```

`doctor --network` 严格只读，每个来源最多访问一个搜索页或探测端点，并另访问一次 Excel 目录基线中唯一的教育部 HTTPS 地址；它不下载 Skill 快照、不生成 ReviewPacket、不写台账或候选。真实端点失败会如实返回 `PARTIAL`，不会伪报通过，也不会改变离线验收结果。

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
5. 保持默认禁用和手动模式；只有用户另行明确批准且全部诊断通过后，才由 Codex 应用更新并回读自动任务。

文件本身就是可迁移状态；没有需要搬迁的数据库。

## 停用与卸载

停用时把 `workflow.enabled` 设为 `false`、`schedule.mode` 设为 `manual`，运行 `apply-settings`，再由 Codex 应用删除本项目自动任务并回读确认不存在。

卸载前保留 `ledger\Skills主台账.xlsx`、`ledger\archive` 和需要的 `output`。确认没有进程持有工作流后，可由用户删除项目内 `.venv`，以及 Codex Skills 根目录中的 `university-skill-library-maintainer`。不要删除规则、主台账、归档或既有交付；installer 与 CLI 均不会自动执行这些删除操作。
