# 高校专业 Skill 库文件化自动维护 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个可部署到其他 Windows 机器、由 TOML 控制频率和启动时间、以 Excel 主台账及 Word/Excel 报告保存业务数据的 Codex 自动 Skill 调研维护工作流。

**Architecture:** Codex Skill 负责调度和需要模型判断的专业审核，Python 包负责配置、四社区只读采集、Excel 台账、规则强门、报告生成和事务发布，PowerShell 负责 Microsoft Office COM 复读与固定格式导出。系统不使用数据库；每轮先生成暂存 Excel/Word，全部结构、Office 和视觉检查通过后才原子发布。

**Tech Stack:** Windows 10/11、Python 3.12 标准库、openpyxl 3.1.5、python-docx 1.2.0、PowerShell 5.1+、Microsoft Word/Excel COM、GitHub CLI、Codex Skill 和 Codex Automations。

**Spec:** `docs/superpowers/specs/2026-08-27-高校专业Skill库文件化自动维护-design.md`

## Global Constraints

- 执行前使用 `superpowers:using-git-worktrees` 创建隔离 worktree；当前主工作区存在大量用户改动，禁止把无关文件带入提交。
- 不创建或依赖 SQLite、Access、服务端数据库、嵌入式数据库或集中式 JSON/CSV 业务数据仓。
- `workflow-settings.toml` 只保存配置；当前 Skill、来源别名、专业映射、版本历史、水位和运行记录只保存在 Excel 主台账。
- 正式交付只发布 `.docx` 和 `.xlsx`；来源快照按现行项目规则保留，运行临时文件在收尾时清理。
- 默认配置必须是 `enabled=false`、`mode="manual"`，用户应用设置前不得创建会联网的自动运行。
- 专业范围固定为现行 13 个非军事学门类及 `99 跨学科通用`；`11 军事学`和军事/武器内容禁止纳入。
- 平台顺序固定为 SkillHub、ClawHub、GitHub、Hugging Face Spaces。
- 发现和核验默认只读；不得安装、导入、执行候选代码，不得调用候选自身外部服务，不得上传真实教学或科研数据。
- 只有正式推荐项可以自动纳入；条件候选、需适配候选和疑似重复必须进入人工查验列表。
- 同一 Skill 跨平台只保存一个稳定 ID；其他平台作为来源别名，同一稳定 ID 跨专业引用不重复计算产品数。
- 外部远程 API、本地专业软件、本地脚本/插件接口必须分别记录，不能把 Abaqus、MATLAB 或本地 SDK 误写成远程 API。
- Word/Excel 使用中文说明；英文原名、URL、许可证、软件名和固定版本保持原样。
- 任一关键校验或 Office 实际打开失败时，不得覆盖旧主台账或既有专业类交付。
- 实现期间所有联网 smoke test 使用无敏感数据的只读查询；自动任务在最终验收前保持禁用。

## Target File Map

```text
07_自动维护工作流/
├─ README.md
├─ pyproject.toml
├─ requirements.txt
├─ workflow-settings.example.toml
├─ install.ps1
├─ edit-settings.ps1
├─ verify_office.ps1
├─ templates/
│  ├─ daily_report.docx
│  └─ daily_review.xlsx
├─ skill/
│  └─ university-skill-library-maintainer/
│     ├─ SKILL.md
│     ├─ assets/automation-prompt.md
│     └─ references/project-contract.md
├─ src/
│  └─ skill_maintainer/
│     ├─ __init__.py
│     ├─ cli.py
│     ├─ models.py
│     ├─ settings.py
│     ├─ scheduling.py
│     ├─ paths.py
│     ├─ locking.py
│     ├─ ledger_schema.py
│     ├─ ledger.py
│     ├─ import_existing.py
│     ├─ catalog.py
│     ├─ queries.py
│     ├─ sources/
│     │  ├─ __init__.py
│     │  ├─ base.py
│     │  ├─ skillhub.py
│     │  ├─ clawhub.py
│     │  ├─ github.py
│     │  └─ huggingface.py
│     ├─ snapshots.py
│     ├─ dedup.py
│     ├─ review.py
│     ├─ versioning.py
│     ├─ reports.py
│     ├─ office.py
│     ├─ publish.py
│     └─ runner.py
└─ tests/
   ├─ fixtures/
   ├─ test_settings.py
   ├─ test_scheduling.py
   ├─ test_ledger.py
   ├─ test_import_existing.py
   ├─ test_catalog_queries.py
   ├─ test_sources.py
   ├─ test_snapshots_review.py
   ├─ test_dedup_versioning.py
   ├─ test_reports.py
   ├─ test_publish_office.py
   ├─ test_skill_contract.py
   └─ test_end_to_end.py
```

---

### Task 1: Create the isolated package skeleton and record the no-database decision

**Files:**
- Create: `07_自动维护工作流/pyproject.toml`
- Create: `07_自动维护工作流/requirements.txt`
- Create: `07_自动维护工作流/src/skill_maintainer/__init__.py`
- Create: `07_自动维护工作流/src/skill_maintainer/cli.py`
- Create: `07_自动维护工作流/tests/test_package.py`
- Modify: `06_过程记录/DECISION_LOG.md`
- Modify: `00_索引/INDEX.md`

**Interfaces:**
- Consumes: Python 3.12 available in the Codex workspace runtime.
- Produces: importable package `skill_maintainer` and console entry `skill-maintainer`.

- [ ] **Step 1: Create an isolated worktree**

Use `superpowers:using-git-worktrees` and create a worktree named `file-based-skill-maintainer`. Confirm `git status --short` in the new worktree is empty before editing.

- [ ] **Step 2: Write the failing package test**

```python
import unittest

from skill_maintainer import __version__
from skill_maintainer.cli import build_parser


class PackageTest(unittest.TestCase):
    def test_package_and_commands_are_importable(self):
        self.assertEqual(__version__, "0.1.0")
        parser = build_parser()
        commands = parser._subparsers._group_actions[0].choices
        self.assertEqual(
            set(commands),
            {
                "setup", "import-existing", "doctor", "edit-settings",
                "apply-settings", "run-now", "scheduled-run", "status",
                "repair-ledger", "rebuild-report", "prepare", "apply-reviews",
                "finalize",
            },
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the test and confirm the package is absent**

Run:

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_package.py -v
```

Expected: `ModuleNotFoundError: No module named 'skill_maintainer'`.

- [ ] **Step 4: Add the minimal package and dependency contract**

Use this dependency set in `requirements.txt`:

```text
openpyxl==3.1.5
python-docx==1.2.0
```

Use this console entry in `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=75"]
build-backend = "setuptools.build_meta"

[project]
name = "university-skill-library-maintainer"
version = "0.1.0"
requires-python = ">=3.11,<3.14"
dependencies = ["openpyxl==3.1.5", "python-docx==1.2.0"]

[project.scripts]
skill-maintainer = "skill_maintainer.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
```

`build_parser()` must create the exact commands asserted by the test. Command handlers may initially return exit code `2` with the Chinese message `该命令尚未接线`.

- [ ] **Step 5: Record the approved storage deviation**

Append one dated decision to `06_过程记录/DECISION_LOG.md` stating that the user approved TOML configuration and Word/Excel business persistence, no database, and that global dedup changes from “数据库只存一次” to “Excel 主台账只存一次”. Add the new workflow entry to `00_索引/INDEX.md` without changing unrelated index text.

- [ ] **Step 6: Run the test and commit only Task 1 files**

Run the test command from Step 3. Expected: `OK`.

Commit:

```powershell
git add -- '07_自动维护工作流' '06_过程记录/DECISION_LOG.md' '00_索引/INDEX.md'
git commit -m 'feat: scaffold file-based skill maintenance workflow'
```

---

### Task 2: Implement strict TOML settings, schedule calculation, and Chinese preview

**Files:**
- Create: `07_自动维护工作流/workflow-settings.example.toml`
- Create: `07_自动维护工作流/src/skill_maintainer/models.py`
- Create: `07_自动维护工作流/src/skill_maintainer/settings.py`
- Create: `07_自动维护工作流/src/skill_maintainer/scheduling.py`
- Create: `07_自动维护工作流/tests/test_settings.py`
- Create: `07_自动维护工作流/tests/test_scheduling.py`

**Interfaces:**
- Produces: `load_settings(path: Path) -> Settings`, `settings_sha256(path: Path) -> str`, `next_run_at(settings: Settings, after: datetime, last_success_at: datetime | None = None) -> datetime | None`, and `schedule_preview(settings: Settings) -> str`.
- Consumes: standard-library `tomllib`, `zoneinfo`, `dataclasses`, and `datetime`.

- [ ] **Step 1: Write strict parsing tests**

```python
class SettingsTest(unittest.TestCase):
    def test_manual_disabled_default(self):
        settings = load_settings(self.fixture("manual.toml"))
        self.assertFalse(settings.workflow.enabled)
        self.assertEqual(settings.schedule.mode, "manual")

    def test_rejects_unknown_and_invalid_values(self):
        for text in (
            VALID.replace('[workflow]', '[workflow]\nunknown = 1'),
            VALID.replace('start_time = "22:00"', 'start_time = "25:61"'),
            VALID.replace('timezone = "Asia/Shanghai"', 'timezone = "Mars/Base"'),
            VALID.replace('interval_days = 1', 'interval_days = 0'),
            VALID.replace('day_of_month = 1', 'day_of_month = 29'),
        ):
            with self.subTest(text=text):
                with self.assertRaises(SettingsError):
                    load_settings(self.write(text))
```

- [ ] **Step 2: Write schedule tests for all five modes**

Use `2026-08-27 20:00 Asia/Shanghai` as the fixed clock. Assert exact next times for daily, weekly, interval, monthly and `None` for manual. Add a DST-independent assertion that the returned timezone is always `Asia/Shanghai`.

- [ ] **Step 3: Run both tests and verify missing symbols**

Run:

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_settings.py 07_自动维护工作流/tests/test_scheduling.py -v
```

Expected: import errors for `load_settings` and `next_run_at`.

- [ ] **Step 4: Implement immutable settings dataclasses and an exact-key validator**

Define:

```python
@dataclass(frozen=True)
class WorkflowSettings:
    enabled: bool
    timezone: str

@dataclass(frozen=True)
class ScheduleSettings:
    mode: Literal["daily", "weekly", "interval", "monthly", "manual"]
    start_time: time
    weekdays: tuple[str, ...]
    interval_days: int
    day_of_month: int

@dataclass(frozen=True)
class ResearchSettings:
    incremental_search: bool
    full_recheck_interval_days: int
    check_existing_skill_updates: bool
    include_generic_skills: bool

@dataclass(frozen=True)
class DeliverySettings:
    generate_word: bool
    generate_excel: bool
    only_refresh_affected_classes: bool
    notify_on_no_change: bool

@dataclass(frozen=True)
class Settings:
    config_version: int
    workflow: WorkflowSettings
    schedule: ScheduleSettings
    research: ResearchSettings
    delivery: DeliverySettings
```

Before constructing dataclasses, compare every TOML table key with a frozen allowlist and raise `SettingsError` for missing, extra, wrong-type or invalid values. Treat `bool` as invalid for integer fields.

- [ ] **Step 5: Implement deterministic scheduling and preview text**

`schedule_preview()` must produce examples such as:

```text
已启用；每周一、三、五 22:00（Asia/Shanghai）运行；每 7 天执行一次全量复核。
```

`next_run_at()` must use the Excel `运行记录` sheet's last successful completion for `interval` mode. It must never silently substitute a missing monthly date; `day_of_month` is already restricted to 1–28.

- [ ] **Step 6: Add a safe example configuration and run tests**

The distributed example may show every field, but active defaults must be:

```toml
[workflow]
enabled = false
timezone = "Asia/Shanghai"

[schedule]
mode = "manual"
start_time = "22:00"
weekdays = ["Monday"]
interval_days = 1
day_of_month = 1
```

Run both tests. Expected: all pass.

- [ ] **Step 7: Commit**

```powershell
git add -- '07_自动维护工作流/workflow-settings.example.toml' '07_自动维护工作流/src/skill_maintainer' '07_自动维护工作流/tests/test_settings.py' '07_自动维护工作流/tests/test_scheduling.py'
git commit -m 'feat: add strict TOML schedule settings'
```

---

### Task 3: Create and validate the Excel master ledger

**Files:**
- Create: `07_自动维护工作流/src/skill_maintainer/ledger_schema.py`
- Create: `07_自动维护工作流/src/skill_maintainer/ledger.py`
- Create: `07_自动维护工作流/tests/test_ledger.py`

**Interfaces:**
- Produces: `LedgerStore.create(path)`, `LedgerStore.load(path)`, `LedgerStore.validate() -> list[str]`, `LedgerStore.save_staged(path)`, `LedgerStore.append_rows(sheet, rows)`, `LedgerStore.upsert_skill(row)`, and `LedgerStore.current_snapshot() -> LedgerSnapshot`.
- Consumes: `openpyxl.Workbook`, `openpyxl.load_workbook`, and the field rules from `01_规则/DATA_DICTIONARY.md`.

- [ ] **Step 1: Write ledger schema and 520-row regression tests**

Assert the exact sheet names:

```python
EXPECTED_SHEETS = (
    "当前Skill", "来源别名", "专业任务映射", "版本历史", "候选观察",
    "目录基线", "来源水位", "运行记录", "字段说明",
)
```

Insert 520 formal rows, save, reopen, and assert all 520 rows, unique stable IDs, table range ending at row 521, filters, frozen header, hyperlinks and date cells survive.

- [ ] **Step 2: Write negative tests**

Test duplicate stable ID, duplicate canonical source assigned to two IDs, missing fixed version, a formal row with unknown license, `外部联网/API调用=是` but empty remote endpoint, and `本地专业软件=Abaqus` incorrectly copied into the remote API field. Each must produce a stable Chinese error code.

- [ ] **Step 3: Run and confirm the ledger module is absent**

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_ledger.py -v
```

Expected: import failure.

- [ ] **Step 4: Implement named-column tables, not cell-position parsing**

Create `SheetSpec(name, table_name, columns, unique_keys)` objects. `LedgerStore` must resolve columns from the header row and reject duplicate or unknown headers. Use Excel table objects for every data sheet and store URLs as actual hyperlinks.

- [ ] **Step 5: Implement validation and staged saving**

`save_staged()` writes a new `.xlsx` path, closes it, reopens with `data_only=False`, validates tables and row counts, then returns its SHA-256. It must never accept the current production ledger path as its staging path.

- [ ] **Step 6: Run the test and inspect the generated workbook manually once**

Run the test suite. Open the generated 520-row fixture with Excel read-only and confirm rows are visible; close without saving. Record this manual smoke result in the test execution note, not in the fixture workbook.

- [ ] **Step 7: Commit**

```powershell
git add -- '07_自动维护工作流/src/skill_maintainer/ledger_schema.py' '07_自动维护工作流/src/skill_maintainer/ledger.py' '07_自动维护工作流/tests/test_ledger.py'
git commit -m 'feat: add Excel master ledger'
```

---

### Task 4: Import existing Word/Excel deliveries into the initial ledger

**Files:**
- Create: `07_自动维护工作流/src/skill_maintainer/import_existing.py`
- Create: `07_自动维护工作流/tests/test_import_existing.py`
- Create: `07_自动维护工作流/tests/fixtures/import/`

**Interfaces:**
- Produces: `scan_existing_deliveries(root: Path) -> ImportInventory`, `build_initial_ledger(inventory, output: Path) -> ImportSummary`.
- Consumes: existing `.xlsx` and `.docx` under `05_交付物`, plus the latest validated structured records when their source paths can be traced.

- [ ] **Step 1: Create representative fixtures**

Include three small workbooks: current professional-class headers, a historical workbook with `API 或外部服务`, and a duplicate Skill appearing in two platform reports. Include one DOCX whose count disagrees with Excel.

- [ ] **Step 2: Write import tests**

Assert that:

- the duplicate becomes one `当前Skill` row plus two `来源别名` rows;
- the historical combined API field is not guessed and enters `候选观察` with reconciliation reason;
- a Word/Excel count mismatch is reported and blocks automatic formal import;
- the source files remain byte-for-byte unchanged;
- repeated import produces the same stable IDs and counts.

- [ ] **Step 3: Run and verify failure**

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_import_existing.py -v
```

Expected: missing `import_existing` module.

- [ ] **Step 4: Implement header aliases and conservative reconciliation**

Use a fixed mapping such as:

```python
HEADER_ALIASES = {
    "内部标识": {"内部标识", "stable_id", "skill_id"},
    "Skill名称": {"Skill名称", "原始名称", "name"},
    "来源地址": {"来源地址", "canonical_url", "GitHub仓库地址"},
    "固定版本": {"固定版本", "审查版本", "fixed_version"},
}
```

Do not infer a remote API dependency from the old combined field. Ambiguous rows remain visible in `候选观察` with `import_status=需人工对账`.

- [ ] **Step 5: Implement deterministic stable-ID allocation**

Reuse an existing stable ID when any validated delivery already contains it. Otherwise allocate from the canonical source hash plus the approved classification prefix, persist the assigned value in the ledger, and never renumber on subsequent imports.

- [ ] **Step 6: Run tests and a read-only inventory against the real `05_交付物`**

The real run must use `--inventory-only` first and print counts without writing. Review duplicate and ambiguous counts before allowing `build_initial_ledger` to write to `07_自动维护工作流/ledger/staging/`.

- [ ] **Step 7: Commit**

```powershell
git add -- '07_自动维护工作流/src/skill_maintainer/import_existing.py' '07_自动维护工作流/tests/test_import_existing.py' '07_自动维护工作流/tests/fixtures/import'
git commit -m 'feat: import existing deliveries into ledger'
```

---

### Task 5: Recheck the Ministry catalog and build the exact research scope and six-dimension queries

**Files:**
- Create: `07_自动维护工作流/src/skill_maintainer/catalog.py`
- Create: `07_自动维护工作流/src/skill_maintainer/queries.py`
- Create: `07_自动维护工作流/tests/test_catalog_queries.py`

**Interfaces:**
- Produces: `verify_catalog_source(url, expected_sha) -> CatalogSourceStatus`, `diff_catalog(old_rows, new_rows) -> CatalogDiff`, `build_scopes(catalog) -> tuple[ResearchScope, ...]`, and `build_queries(scope) -> tuple[QueryJob, ...]`.
- Consumes: `06_过程记录/discipline_mapping/catalogs/undergraduate_2026.json`, the official PDF URL recorded in `02_知识库/discipline_catalog/SOURCE_AND_METHOD.md`, and the Excel `目录基线` sheet.

- [ ] **Step 1: Write catalog invariants**

Using the current 2026 fixture, assert 883 unique major records, no category 11 scope, 92 professional-class scopes for categories with class codes, 15 category-14 major scopes, and one `99 跨学科通用` scope.

- [ ] **Step 2: Write exact diff tests**

Create fixture changes for add, remove, rename, major-code change, class move and category move. Assert each lands in a distinct `CatalogDiff` list; a total-count-only comparison must not satisfy the test.

- [ ] **Step 3: Write six-dimension query tests**

For `0818 交通运输类`, require jobs for professional aliases, core courses, methods, work tasks, outputs/data objects, and software/database/processes. Assert names without `交通运输` can still appear through method/task queries. Assert every job includes one of the four platform names and a stable query ID.

- [ ] **Step 4: Run and verify failure**

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_catalog_queries.py -v
```

- [ ] **Step 5: Implement catalog verification and scope construction**

The online check may reuse the local PDF only after confirming the public URL still returns the same content hash. If the official content changes, return `CatalogSourceStatus(changed=True)` and block query creation until the new snapshot and per-record diff are staged.

- [ ] **Step 6: Implement query generation from task profiles**

Store professional aliases and task profiles in the Excel `专业任务映射`/`目录基线` sheets, not in a new JSON catalog. Generate query jobs in memory; do not write a permanent query database.

- [ ] **Step 7: Run tests and commit**

```powershell
git add -- '07_自动维护工作流/src/skill_maintainer/catalog.py' '07_自动维护工作流/src/skill_maintainer/queries.py' '07_自动维护工作流/tests/test_catalog_queries.py'
git commit -m 'feat: add catalog and query scope gates'
```

---

### Task 6: Implement the four read-only source adapters and Excel watermarks

**Files:**
- Create: `07_自动维护工作流/src/skill_maintainer/sources/base.py`
- Create: `07_自动维护工作流/src/skill_maintainer/sources/skillhub.py`
- Create: `07_自动维护工作流/src/skill_maintainer/sources/clawhub.py`
- Create: `07_自动维护工作流/src/skill_maintainer/sources/github.py`
- Create: `07_自动维护工作流/src/skill_maintainer/sources/huggingface.py`
- Create: `07_自动维护工作流/tests/test_sources.py`

**Interfaces:**
- Produces protocol `SourceAdapter.search(job, watermark) -> SearchBatch`, `latest_version(identity) -> VersionObservation`, and `snapshot(identity, version, destination) -> SnapshotResult`.
- Produces normalized `SourceCandidate` and `SourceRequestEvent` dataclasses.
- Consumes the `来源水位` sheet and in-memory `QueryJob` values.

- [ ] **Step 1: Write adapter contract tests with fake transports**

Use fake page sequences to assert full pagination, exact request URLs, stable result ordering, response byte hashes, retry counts and last-page detection. Include GitHub's 1,000-result ceiling and a 422 query-parse failure that must be recorded as a source error rather than retried indefinitely.

- [ ] **Step 2: Write watermark tests**

Assert that a successful run advances only that platform's watermark, a failed or partial run leaves the old watermark unchanged, and the configured full-recheck interval ignores the incremental watermark for one run without deleting it.

- [ ] **Step 3: Run and verify failure**

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_sources.py -v
```

- [ ] **Step 4: Implement source endpoints without shell-string construction**

Use these current endpoint contracts:

```python
SKILLHUB = "https://api.skillhub.cn/api/skills"
CLAWHUB = "https://clawhub.ai/api/v1/search"
HUGGINGFACE = "https://huggingface.co/api/spaces"
```

Use `urllib.request` with explicit timeouts for HTTP sources. Invoke GitHub as an argument list:

```python
["gh", "api", "--method", "GET", endpoint]
```

Never construct a shell command string and never execute candidate-provided commands.

- [ ] **Step 5: Normalize candidates and capture source evidence**

Every normalized candidate must include platform, native ID, discovery URL, canonical-source hint, version hint, display name, publisher, updated time, popularity metrics, query ID and response evidence hash. Save immutable raw response snapshots only under the existing evidence area required by project rules, not in the master ledger.

- [ ] **Step 6: Add partial-coverage behavior**

Return `SearchBatch(status="partial")` when a platform fails after some completed pages. The runner continues other platforms but does not advance that platform's watermark or report four-platform completion.

- [ ] **Step 7: Run tests and one doctor-only endpoint smoke check**

The smoke check uses a harmless fixed query, fetches at most one page per platform, writes no candidate or ledger rows, and reports endpoint/authentication status only. Keep automation disabled.

- [ ] **Step 8: Commit**

```powershell
git add -- '07_自动维护工作流/src/skill_maintainer/sources' '07_自动维护工作流/tests/test_sources.py'
git commit -m 'feat: add four read-only source adapters'
```

---

### Task 7: Snapshot fixed versions and enforce static review contracts

**Files:**
- Create: `07_自动维护工作流/src/skill_maintainer/snapshots.py`
- Create: `07_自动维护工作流/src/skill_maintainer/review.py`
- Create: `07_自动维护工作流/tests/test_snapshots_review.py`

**Interfaces:**
- Produces: `build_snapshot(candidate, destination) -> SnapshotManifest`, `build_review_packet(candidate, snapshot) -> ReviewPacket`, `validate_review(decision, packet) -> tuple[str, ...]`, and `score_quality(decision) -> int`.
- Consumes: fixed-version source adapter methods and transient review decisions supplied by the Codex Skill over stdin; no review JSON file is persisted.

- [ ] **Step 1: Write snapshot safety tests**

Assert fixed version is mandatory, path traversal and symlink/reparse entries are rejected, file count/bytes are bounded, text/code/config files are hashed, and no candidate file is imported or executed. Mock `subprocess.run` and fail the test if candidate-controlled commands are invoked.

- [ ] **Step 2: Write review consistency tests**

Cover these regressions:

- pure Markdown Abaqus guidance: remote API `否`, local professional software `实操时需要`, local script/plugin interface `按需使用`;
- remote endpoint present but remote API `否`: reject;
- unknown license marked formal: reject;
- SB-A marked directly deployable: reject;
- relevance 2/5 included in product display: reject;
- `待核验` given SA/SB final grade: reject;
- formal item below `全部通过（未实测）`: reject.

- [ ] **Step 3: Write exact scoring tests**

Require all four admission conditions before base score 1. Add one point for each approved bonus and cap at 5. Assert safety, license or traceability failure produces score 0 regardless of popularity.

- [ ] **Step 4: Run and verify failure**

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_snapshots_review.py -v
```

- [ ] **Step 5: Implement snapshot and review models**

`ReviewDecision` must separately hold observed facts, project judgments and derived fields. Validation errors must identify exact fields. The review packet must embed the relevant rule version and evidence paths so the Codex Skill can review without guessing from platform cards.

- [ ] **Step 6: Implement transient review input**

`skill-maintainer apply-reviews --run <run-id> --stdin` reads UTF-8 JSON from stdin, validates it, writes accepted decisions into the staged Excel ledger, then discards the input bytes. It must not create a JSON review artifact.

- [ ] **Step 7: Run tests and commit**

```powershell
git add -- '07_自动维护工作流/src/skill_maintainer/snapshots.py' '07_自动维护工作流/src/skill_maintainer/review.py' '07_自动维护工作流/tests/test_snapshots_review.py'
git commit -m 'feat: add fixed-version static review gates'
```

---

### Task 8: Implement global deduplication and version-change decisions

**Files:**
- Create: `07_自动维护工作流/src/skill_maintainer/dedup.py`
- Create: `07_自动维护工作流/src/skill_maintainer/versioning.py`
- Create: `07_自动维护工作流/tests/test_dedup_versioning.py`

**Interfaces:**
- Produces: `canonical_key(candidate) -> str`, `deduplicate(candidates, ledger) -> DedupResult`, `compare_version(current, observed) -> VersionChange`, and `apply_approved_version(ledger, decision) -> None`.
- Consumes: normalized candidates, snapshot hashes, current Skill rows, source aliases and version history.

- [ ] **Step 1: Write cross-platform dedup tests**

Create one upstream Skill represented by SkillHub, ClawHub and GitHub. Assert one stable ID, three source aliases and one product count. Add a same-name/different-function pair and assert they remain separate. Add a possible duplicate with insufficient evidence and assert `manual_review`, not automatic merge.

- [ ] **Step 2: Write version tests**

Assert: unchanged hash does nothing; new tag with unchanged content adds an alias observation but no upgrade; changed content triggers full review; rejected new version preserves old current version; accepted new version appends history then changes current; deleted upstream marks attention without deleting the old fixed snapshot.

- [ ] **Step 3: Run and verify failure**

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_dedup_versioning.py -v
```

- [ ] **Step 4: Implement conservative keys and relationship evidence**

Use normalized canonical source first, then upstream identity, Skill entry path and fixed content hash. Name similarity alone may only create `possible_duplicate` evidence. Persist every accepted merge reason in `来源别名`.

- [ ] **Step 5: Implement version retention**

Never overwrite the `版本历史` row. A current version update must add a history row containing old/new version, old/new hash, review date, conclusion change and evidence paths before changing `当前Skill`.

- [ ] **Step 6: Run tests and commit**

```powershell
git add -- '07_自动维护工作流/src/skill_maintainer/dedup.py' '07_自动维护工作流/src/skill_maintainer/versioning.py' '07_自动维护工作流/tests/test_dedup_versioning.py'
git commit -m 'feat: add global dedup and version retention'
```

---

### Task 9: Build the single-writer staged run coordinator

**Files:**
- Create: `07_自动维护工作流/src/skill_maintainer/paths.py`
- Create: `07_自动维护工作流/src/skill_maintainer/locking.py`
- Create: `07_自动维护工作流/src/skill_maintainer/runner.py`
- Create: `07_自动维护工作流/tests/test_runner.py`

**Interfaces:**
- Produces: `ProjectPaths.from_root(root)`, `SingleWriterLock`, `RunCoordinator.prepare(request: RunRequest) -> PreparedRun`, `RunCoordinator.apply_reviews(prepared: PreparedRun, decisions: Iterable[ReviewDecision]) -> ReviewApplySummary`, and `RunCoordinator.finalize(prepared: PreparedRun, reviews: ReviewApplySummary) -> RunSummary`.
- Consumes: settings, ledger, catalog, sources, dedup, review and versioning components.

- [ ] **Step 1: Write locking and idempotency tests**

Assert a second process cannot acquire the lock, a stale lock file without an active OS lock is recoverable, repeated identical input creates no duplicate rows, and an interrupted staging directory never changes the production ledger.

- [ ] **Step 2: Write failure-atomicity tests**

Inject failures after discovery, after review application, during report generation, during Office verification and immediately before publish. In every case assert production ledger and professional-class outputs retain original hashes.

- [ ] **Step 3: Run and verify failure**

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_runner.py -v
```

- [ ] **Step 4: Implement Windows single-writer locking**

Use a project-local lock file with `msvcrt.locking` held for the process lifetime. Store PID and start time for diagnostics, but determine ownership from the OS lock rather than file existence.

- [ ] **Step 5: Implement the three-stage coordinator**

`prepare` creates a run directory and staged ledger, checks catalog, discovers candidates and builds review packets. `apply_reviews` only validates and writes review decisions to the staged ledger. `finalize` runs dedup/version updates, generates reports, verifies Office artifacts and publishes. No stage writes the production ledger early.

- [ ] **Step 6: Implement partial-source semantics**

Continue other sources when one fails. Record source status in the staged ledger and report; only completed source watermarks advance. If all four fail, block finalize and produce a failure report in staging without publishing business changes.

- [ ] **Step 7: Run tests and commit**

```powershell
git add -- '07_自动维护工作流/src/skill_maintainer/paths.py' '07_自动维护工作流/src/skill_maintainer/locking.py' '07_自动维护工作流/src/skill_maintainer/runner.py' '07_自动维护工作流/tests/test_runner.py'
git commit -m 'feat: add staged single-writer coordinator'
```

---

### Task 10: Generate Chinese Word and Excel reports and affected-class deliveries

**Files:**
- Create: `07_自动维护工作流/src/skill_maintainer/reports.py`
- Create: `07_自动维护工作流/templates/daily_report.docx`
- Create: `07_自动维护工作流/templates/daily_review.xlsx`
- Create: `07_自动维护工作流/tests/test_reports.py`

**Interfaces:**
- Produces: `build_daily_docx(summary, output)`, `build_daily_xlsx(summary, output)`, `affected_scopes(before, after)`, and `build_scope_deliveries(scopes, ledger, output_root)`.
- Consumes: `RunSummary`, staged ledger rows and existing report standards.

- [ ] **Step 1: Write report-content tests**

Assert the Word contains all 13 required sections from the spec, Chinese purpose/inputs/outputs/limits, original English name and URLs, and the explicit `未安装、未运行` boundary. Assert exclusion names do not appear.

- [ ] **Step 2: Write Excel structure and scale tests**

Assert the 12 required sheet names, exact stable-ID counts, actual hyperlinks, filters, frozen rows, wrap text and formulas covering 520 rows. Reopen the saved workbook and assert a known last-row value is non-empty.

- [ ] **Step 3: Write affected-scope tests**

Assert a new formal item, accepted version change, license/safety/task-mapping change or catalog change refreshes the scope; adding only a source alias does not refresh unrelated scopes.

- [ ] **Step 4: Run and verify failure**

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_reports.py -v
```

- [ ] **Step 5: Implement Excel generation with dynamic table ranges**

Generate table formulas from `max_row`, never a fixed row limit. Use the current report vocabulary: `正式推荐`, `条件候选`, `需适配候选`, and keep their counts separate.

- [ ] **Step 6: Implement Word generation and scope refresh**

Use 11 pt body/table text, Chinese headings and deterministic section order. Scope Word/Excel must reference the same stable IDs as the ledger and reuse one Skill across scopes without duplicating the master row.

- [ ] **Step 7: Run tests and commit**

```powershell
git add -- '07_自动维护工作流/src/skill_maintainer/reports.py' '07_自动维护工作流/templates' '07_自动维护工作流/tests/test_reports.py'
git commit -m 'feat: generate Chinese Word and Excel reports'
```

---

### Task 11: Add Microsoft Office verification and atomic publication

**Files:**
- Create: `07_自动维护工作流/verify_office.ps1`
- Create: `07_自动维护工作流/src/skill_maintainer/office.py`
- Create: `07_自动维护工作流/src/skill_maintainer/publish.py`
- Create: `07_自动维护工作流/tests/test_publish_office.py`

**Interfaces:**
- Produces: `verify_excel(path) -> OfficeCheck`, `verify_word(path, render_dir) -> OfficeCheck`, `build_publish_plan(staging, production) -> PublishPlan`, and `publish_atomically(plan) -> PublishReceipt`.
- Consumes: Microsoft Excel/Word COM, staged ledger/reports and immutable pre-publish hashes.

- [ ] **Step 1: Write COM verification tests**

Create a valid workbook, an empty-data workbook, a structurally valid but unreadable workbook and a valid DOCX. Assert Excel opens read-only, key sheet and last data cell are non-empty, Word opens and exports PDF, and every COM object is released even on failure.

- [ ] **Step 2: Write publication rollback tests**

Inject a failure for each destination file. Assert no production file is partly replaced, backups remain available and the publish receipt is absent on failure.

- [ ] **Step 3: Run deterministic Python tests first**

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_publish_office.py -v
```

Expected initially: missing modules.

- [ ] **Step 4: Implement Office COM verification**

`verify_office.ps1` accepts `-Excel`, `-Word`, and `-RenderDirectory` arguments. It prints one compact UTF-8 JSON result to stdout but does not persist a JSON artifact. Excel uses `Workbooks.Open(path, 0, $true)` and Word calls `Documents.Open` with the absolute filename and `ReadOnly=$true`, followed by PDF export.

- [ ] **Step 5: Bind Word render verification**

After PDF export, the Codex Skill must use the bundled documents renderer to create page PNGs and visually inspect every page. The finalizer receives a pass/fail decision plus DOCX/PDF/page-image hashes; it refuses publication if any page is missing, blank or visually rejected.

- [ ] **Step 6: Implement backup and atomic replace**

Copy the current ledger to `ledger/archive/Skills主台账_YYYYMMDD_HHMMSS.xlsx`, fsync staged files, verify expected old hashes immediately before replace, then replace ledger and output directory. If Windows cannot make the multi-file tree atomic, publish to a versioned run directory first and update one small pointer file last; professional-class replacements occur only after the complete run directory is accepted.

- [ ] **Step 7: Run Office tests on the installed Office instance**

Confirm Excel and Word processes return to their pre-test count, all test artifacts open after a second reopen, and the 520-row workbook's final row remains populated.

- [ ] **Step 8: Commit**

```powershell
git add -- '07_自动维护工作流/verify_office.ps1' '07_自动维护工作流/src/skill_maintainer/office.py' '07_自动维护工作流/src/skill_maintainer/publish.py' '07_自动维护工作流/tests/test_publish_office.py'
git commit -m 'feat: verify Office artifacts before publish'
```

---

### Task 12: Build the reusable Codex Skill, settings editor, and automation contract

**Files:**
- Create: `07_自动维护工作流/skill/university-skill-library-maintainer/SKILL.md`
- Create: `07_自动维护工作流/skill/university-skill-library-maintainer/assets/automation-prompt.md`
- Create: `07_自动维护工作流/skill/university-skill-library-maintainer/references/project-contract.md`
- Create: `07_自动维护工作流/edit-settings.ps1`
- Create: `07_自动维护工作流/src/skill_maintainer/settings_editor.py`
- Create: `07_自动维护工作流/tests/test_skill_contract.py`

**Interfaces:**
- Produces Skill commands `setup`, `import-existing`, `doctor`, `edit-settings`, `apply-settings`, `run-now`, `scheduled-run`, `status`, `repair-ledger`, and `rebuild-report`.
- Consumes: local settings path, settings SHA, Codex automation tool, and all CLI stage commands.

- [ ] **Step 1: Read the current `skill-creator` and `writing-skills` instructions before editing the Skill**

Do this at implementation time. Validate the final Skill against both instruction sets; do not copy a historical Skill template from memory.

- [ ] **Step 2: Write static Skill contract tests**

Assert `SKILL.md` requires reading `AGENTS.md` and the four project rule files, forbids candidate execution, includes the four source order, separates formal/conditional/adaptation, and never writes raw automation directives. Assert every documented command maps to a CLI command from Task 1.

- [ ] **Step 3: Write settings editor tests**

Call pure form-to-settings functions without opening a window. Assert Chinese labels round-trip all modes, a cancelled edit leaves the file unchanged, invalid values cannot save, and saving uses a same-directory temporary file plus atomic replace.

- [ ] **Step 4: Run and verify failure**

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_skill_contract.py -v
```

- [ ] **Step 5: Implement the Skill execution sequence**

`scheduled-run` must perform this exact sequence:

```text
read rules → validate config hash → doctor → prepare → review fixed evidence
→ apply-reviews through stdin → finalize → inspect Word page images
→ approve or reject publication → notify only changes/failure
```

The Skill must stop if config hash differs from the automation prompt, settings are disabled/manual, the ledger is invalid, or the professional catalog gate changes before scope reconstruction.

- [ ] **Step 6: Implement the automation prompt**

The prompt template must contain the absolute project root, absolute TOML path, applied TOML SHA-256, fixed Skill command `scheduled-run`, no target/scope override, and the instruction to finish silently on a successful no-change run.

- [ ] **Step 7: Implement `apply-settings` as an agent-owned operation**

The Python CLI validates and prints the normalized schedule plus config hash. The Codex Skill then searches for and calls the app's automation update tool to create or update the single project automation. It must never hand-write a raw automation directive. Re-read the created automation and compare project, schedule, prompt and config hash before reporting success.

For `interval` mode, create a daily dispatcher at `start_time`; `scheduled-run` reads the last successful time from the Excel `运行记录` sheet and exits with safe no-op code `3` until `interval_days` has elapsed. For `manual` or `enabled=false`, remove or leave absent the project automation. `run-now` is an explicit user action and is allowed in manual mode after displaying the configuration preview; `scheduled-run` is not.

- [ ] **Step 8: Implement the Chinese Tk settings editor**

`edit-settings.ps1` locates the project Python command passed by the installer and opens `settings_editor.py`. The editor exposes enable, mode, start time, weekdays, interval, monthly date and full-recheck interval; it displays the exact `schedule_preview()` before save.

- [ ] **Step 9: Run tests and commit**

```powershell
git add -- '07_自动维护工作流/skill' '07_自动维护工作流/edit-settings.ps1' '07_自动维护工作流/src/skill_maintainer/settings_editor.py' '07_自动维护工作流/tests/test_skill_contract.py'
git commit -m 'feat: add deployable Codex automation skill'
```

---

### Task 13: Add installer, doctor, status, repair, and rebuild commands

**Files:**
- Create: `07_自动维护工作流/install.ps1`
- Create: `07_自动维护工作流/README.md`
- Modify: `07_自动维护工作流/src/skill_maintainer/cli.py`
- Create: `07_自动维护工作流/tests/test_cli_operations.py`

**Interfaces:**
- Produces fully working setup/import/doctor/edit/apply/run/status/repair/rebuild CLI operations.
- Consumes package modules from Tasks 2–12 and a user-supplied project root.

- [ ] **Step 1: Write CLI operation tests**

Assert setup is idempotent, uses an explicit project path, refuses a non-Windows system for production scheduling, checks Word/Excel/gh/Python, creates a disabled manual TOML, never overwrites an existing settings file, and installs the Skill into a supplied test Codex skills directory.

- [ ] **Step 2: Write repair and rebuild tests**

Assert repair lists valid backups and requires an explicit backup choice; it never auto-overwrites. Assert rebuild-report performs no network calls and reads only the current ledger to regenerate Word/Excel.

- [ ] **Step 3: Run and verify failure**

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_cli_operations.py -v
```

- [ ] **Step 4: Implement `install.ps1`**

Parameters must be `-ProjectRoot`, `-PythonExe`, and optional `-CodexSkillsRoot`. The script creates `.venv`, installs the exact `requirements.txt`, installs the package editable, copies the Skill, creates only missing workflow directories and settings, and runs `doctor`. It does not create or enable an automation.

- [ ] **Step 5: Wire every CLI command**

Commands return `0` for success, `1` for operational failure, `2` for invalid input/config and `3` for a safe no-op such as lock contention or no change. Output is concise Chinese; machine-readable details may be emitted to stdout for the current Codex process but are not persisted as a business data file.

- [ ] **Step 6: Write the deployment README**

Include: prerequisites, installation, first import, editing TOML, applying schedule, manual run, status, backup recovery, moving to another machine, disabling/uninstalling the automation, and the explicit boundary that candidate Skills are not installed or executed.

- [ ] **Step 7: Run tests and commit**

```powershell
git add -- '07_自动维护工作流/install.ps1' '07_自动维护工作流/README.md' '07_自动维护工作流/src/skill_maintainer/cli.py' '07_自动维护工作流/tests/test_cli_operations.py'
git commit -m 'feat: add workflow installer and operations'
```

---

### Task 14: Run end-to-end dry runs, portability checks, and final verification

**Files:**
- Create: `07_自动维护工作流/tests/test_end_to_end.py`
- Create: `07_自动维护工作流/tests/fixtures/e2e/`
- Modify: `07_自动维护工作流/README.md`
- Modify: `00_索引/INDEX.md`

**Interfaces:**
- Consumes the complete workflow.
- Produces a verified release package, disabled/manual default settings, initial ledger import instructions and an acceptance record.

- [ ] **Step 1: Build an offline four-source fixture**

Include: one new formal candidate, one condition candidate, one adaptation candidate, one cross-platform duplicate, one accepted version upgrade, one rejected new version, one deleted upstream and one changed catalog record. Include 520 report rows to retain the Excel regression.

- [ ] **Step 2: Write end-to-end assertions**

Run setup → import → prepare → apply-reviews → finalize twice. Assert the second run is idempotent, the master ledger has one canonical duplicate entry, only affected scopes regenerate, no database file exists anywhere under the workflow root, and published Word/Excel hashes remain unchanged on injected failure.

- [ ] **Step 3: Run the complete unit suite serially**

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest discover -s '07_自动维护工作流/tests' -p 'test_*.py' -v
```

Expected: all tests pass with no unexpected network call.

- [ ] **Step 4: Run compilation and source hygiene checks**

```powershell
python -m compileall -q '07_自动维护工作流/src' '07_自动维护工作流/tests'
rg -n 'C:\\Users\\|\.cache/codex-runtimes|sqlite|duckdb|sqlalchemy|CREATE TABLE' '07_自动维护工作流'
```

Expected: compilation succeeds; the search returns only test assertions that forbid hard-coded paths/database dependencies, not production matches.

- [ ] **Step 5: Run Office acceptance**

Generate the E2E Word, Excel and 520-row master ledger; open every file through Office COM, export Word to PDF, render every page with the bundled documents renderer, inspect every page, close Office, and assert no new WINWORD/EXCEL process remains.

- [ ] **Step 6: Run one read-only network smoke pass**

With automation still disabled, run `doctor --network` against all four platforms and the Ministry URL. Fetch at most one page per source; do not snapshot or review candidates. Record the timestamp and coverage result in the acceptance Word/Excel, not a JSON database.

- [ ] **Step 7: Perform a clean-machine portability rehearsal**

Copy only `07_自动维护工作流` plus a read-only project fixture to a new temporary directory whose path contains Chinese characters and spaces. Run install, doctor, offline E2E and Office verification with no source edits. Confirm no original-machine absolute path appears in generated files.

- [ ] **Step 8: Inspect the final Git diff and update the index**

Confirm only planned files changed. Update `00_索引/INDEX.md` with the workflow location, settings file, ledger location and operational commands. Do not stage unrelated pre-existing user changes.

- [ ] **Step 9: Commit the acceptance suite**

```powershell
git add -- '07_自动维护工作流/tests/test_end_to_end.py' '07_自动维护工作流/tests/fixtures/e2e' '07_自动维护工作流/README.md' '00_索引/INDEX.md'
git commit -m 'test: verify file-based maintenance workflow end to end'
```

- [ ] **Step 10: Request code review before enabling automation**

Use `superpowers:requesting-code-review`. The reviewer must verify the no-database constraint, candidate non-execution boundary, four-source coverage, global dedup, API/local-interface separation, Office reopen checks, atomic publish and clean-machine rehearsal. Fix any findings and rerun the complete suite.

- [ ] **Step 11: Leave production scheduling disabled for handoff**

Deliver `workflow-settings.toml` with `enabled=false` and `mode="manual"`. The user selects the actual frequency/time, then explicitly invokes `apply-settings`; only that operation may create or enable the Codex automatic task.
