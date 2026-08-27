# Task 5 实施报告：教育部目录复核、研究范围与六维检索任务

## 范围与边界

- 目录输入证据：`06_过程记录/discipline_mapping/catalogs/undergraduate_2026.json`；未复制为新的业务 JSON/CSV。
- 教育部公开目录地址：`https://www.moe.gov.cn/srcsite/A08/moe_1034/s3882/202604/W020260427440749576927.pdf`；目录基线 SHA-256 为 `51026248004546171620678895e991a6f0ada1ebf0de6498fe8c563873b43f11`。
- 公开自动检索范围固定为 13 个非军事门类，`11 军事学`不生成 scope；另有 `99 跨学科通用`。
- 非 14 门类按专业类 scope；14 门类按专业 scope。查询任务仅在内存中生成，不创建检索任务业务仓库。
- 任务画像以 `TaskProfile` 注入 scope；后续流程须从 Excel 主台账的 `专业任务映射`/`目录基线`读取并提供该画像，不能落为新 JSON 目录。

## TDD 记录

先新增 `test_catalog_queries.py`，在不存在生产模块时运行：

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_catalog_queries.py -v
```

RED 的准确结果是 `ModuleNotFoundError: No module named 'skill_maintainer.catalog'`，`Ran 1 test`，`FAILED (errors=1)`；失败原因是所需实现尚不存在。

最小实现后，同一命令的 GREEN 输出：`Ran 5 tests in 0.005s`，`OK`。

## 实测不变量

当前 2026 fixture 的实际断言结果：

| 项目 | 实测 |
|---|---:|
| 唯一专业记录 | 883 |
| 非军事专业类 scopes | 92 |
| 14 门类专业 scopes | 15 |
| `99 跨学科通用` scope | 1 |
| `11 军事学` scope | 0 |

## 逐记录 diff 六类结果

定向构造了一次每类恰一条的目录变更，`diff_catalog` 的结果分别为：

| 类型 | 结果 |
|---|---|
| 新增 | `080006` |
| 撤销 | `080001` |
| 改名 | `080002`：保留代码新名称 |
| 专业代码变化 | `080003 → 080007` |
| 专业类调整 | `0801 → 0802` |
| 门类调整 | `07 → 08` |

这不是总数比较；六个结果保存在互斥的 `CatalogDiff` 列表中。

## 交通运输六维样例

`0818 交通运输类` 的任务画像包含专业别名、核心课程、方法、工作任务、成果/数据对象、软件/数据库/流程。SkillHub 的七条样例为：

| 稳定 query ID | 维度 | 检索词 |
|---|---|---|
| `Q-ff52d7db6ea96be6` | professional_alias | `交通运输 Skill` |
| `Q-84deec29a07721a5` | professional_alias | `transportation engineering Skill` |
| `Q-9849447ff7ede000` | core_course | `交通工程学 Skill` |
| `Q-cfb14edc135f2341` | method | `traffic flow prediction Skill` |
| `Q-5f891cb1cfc0f0ab` | work_task | `route optimisation Skill` |
| `Q-7f00beeaf701bc77` | output_or_data | `OD matrix Skill` |
| `Q-f7bd55249ba92dc5` | software_database_or_process | `SUMO traffic simulation Skill` |

每一条会按固定平台顺序 SkillHub、ClawHub、GitHub、Hugging Face Spaces 生成，且相同输入重跑后的 ID 不变。方法和工作任务查询不含“交通运输”，从而覆盖名称不含专业名称、但任务或方法相关的候选。

## 变更源阻断证据

`verify_catalog_source` 接受可注入的只读 fetch。离线测试以不同于预期 SHA 的字节返回 `CatalogSourceStatus(changed=True)`，不把测试替身表述为教育部“未变化”。当该状态存在时：

1. 未暂存新快照时 `build_scopes` 抛出 `CatalogSourceChangedError`；
2. 仅暂存快照时仍抛出同一错误；
3. 新快照和逐记录 diff 都暂存后才允许构造 scopes，之后才能调用 `build_queries`。

## 改动文件

- `07_自动维护工作流/src/skill_maintainer/catalog.py`
- `07_自动维护工作流/src/skill_maintainer/queries.py`
- `07_自动维护工作流/tests/test_catalog_queries.py`

## 验证

定向测试：`Ran 5 tests in 0.005s`，`OK`。

全工作流测试：

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest discover -s 07_自动维护工作流/tests -v
git diff --check
```

输出为 `Ran 43 tests in 3.576s`，`OK`；`git diff --check` 无输出、退出码 0。

首次全量运行因本机未安装项目锁定的 `openpyxl==3.1.5` 而在既有台账测试导入阶段失败；安装 `requirements.txt` 后以上全量结果通过。

## 自审与顾虑

- 已确认目录变更 gate 用真实获取函数和可注入 fetch 分离；本任务未访问互联网，也未伪造教育部内容未变。
- 任务画像本身尚待 Task 3 主台账的 Excel 行提供。代码会拒绝缺少任一维度的 scope，因此后续消费者不能以仅名称关键词替代六维任务画像。
- 未修改目录证据、既有 Excel 或任何候选库；后续 Task 6 负责消费 scope/query jobs。

---

## Round 1/5 复核修复（2026-08-27）

### RED → GREEN

先添加三项复核回归测试及 Excel 520 行结构测试。RED 命令为：

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_catalog_queries.py 07_自动维护工作流/tests/test_ledger.py -v
```

RED 输出：`test_catalog_queries` 因 `ImportError: cannot import name 'TaskProfileReadError'` 失败；`专业任务映射` 因六个新字段不在 schema 中出现 `KeyError`；表头断言显示预期多出六个字段。结果为 `Ran 14 tests`、`FAILED (failures=1, errors=2)`。

GREEN 的同一命令输出：`Ran 22 tests in 3.204s`，`OK`。

### P1：不可绕过的目录变更门

- `stage_new_snapshot(rows, snapshot_sha=...)` 现在必须显式接收新解析记录，并且 `snapshot_sha` 必须等于 `CatalogSourceStatus.actual_sha`。
- `stage_record_diff(diff)` 会重新计算 `diff_catalog(old_rows, staged_new_rows)`；只有完全相等且非空的 diff 才能暂存。
- `build_scopes` 对已变更来源只使用暂存的新 rows；错误哈希、空 diff、错误 diff、缺快照或缺 diff 都会抛出 `CatalogSourceChangedError`。
- 正向测试确认 scope 的记录来自新快照（旧名称不会被用于后续查询）。

### P1：Excel 六维画像生产适配器

- `专业任务映射` 保留既有 10 列，并新增 `专业别名`、`核心课程`、`研究方法`、`工作任务`、`成果或数据对象`、`软件/数据库/流程` 六列。
- `load_task_profiles_from_ledger` 通过 `LedgerStore.rows()` 的命名列读回保存后的 Excel；按 `专业代码` 聚合。可见单元格列表按换行、顿号、中英文分号和逗号稳定拆分。
- `load_catalog_with_ledger` 是生产入口：从既有目录证据和 Excel 主台账构造内存 `Catalog`。不完整、重复或歧义画像会抛出 `TaskProfileReadError`；无画像仍会被 `build_queries` 阻断。
- 保存、重开 Excel 后的 `0818` 画像已生成完整六维 QueryJobs；未新增 JSON/CSV/profile 侧车仓库。

### P2：重复名称的代码变更

只有 unmatched old/new 中某名称两端都严格 1 条时才判定为代码变化。两个旧同名记录对一个新同名记录的对抗测试结果为 0 条代码变化、2 条撤销、1 条新增，杜绝多对一映射。

### 520 行 Excel/OOXML 核验

`专业任务映射` 写入 520 个画像后保存并重开：读取仍为 520 行，命名列 `专业代码` 正确、冻结窗格为 `A2`、命名表自动筛选范围为 `A1:P521`。OOXML 检查确认 worksheet XML 没有 worksheet-level `<autoFilter>`，`xl/tables/table3.xml` 包含 `<autoFilter ref="A1:P521"`。这只是文件结构核验；实际 Excel UI 烟测依复核方控制器安排。

### 回归与提交前核验

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest discover -s 07_自动维护工作流/tests -v
git diff --check
```

输出为 `Ran 48 tests in 4.285s`，`OK`；`git diff --check` 无差异错误、退出码 0。

### 本轮改动

- `07_自动维护工作流/src/skill_maintainer/catalog.py`
- `07_自动维护工作流/src/skill_maintainer/ledger_schema.py`
- `07_自动维护工作流/tests/test_catalog_queries.py`
- `07_自动维护工作流/tests/test_ledger.py`

### 自审/顾虑

目录 hash 绑定的是公开 PDF 内容哈希，目录 rows 的提取正确性仍由新快照的生成与 review 流程负责；本门负责防止未绑定或不精确差异绕过。Excel UI 烟测未在本任务执行，按要求留给控制器复核。

---

## Round 2/5 复核修复（2026-08-27）

### RED → GREEN

先新增真实 10 列旧版 `专业任务映射` 工作簿、源不可变、失败输出不改写、幂等当前 schema 复制和中文逗号解析测试。RED 命令：

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest 07_自动维护工作流/tests/test_catalog_queries.py 07_自动维护工作流/tests/test_ledger.py -v
```

RED 输出为 `Ran 10 tests`、`FAILED (failures=1, errors=1)`：生产层尚无 `ProfessionalTaskMapUpgradeError`/升级函数，且 `交通运输，transportation engineering` 未拆分。

GREEN 同一命令输出为 `Ran 24 tests in 3.721s`、`OK`。

### P1：10 列旧主台账的非破坏性暂存升级

- 新增 `upgrade_professional_task_maps(source_path, staging_path)` 及结构化 `ProfessionalTaskMapUpgradeSummary`。
- 函数只读源工作簿；源、暂存路径相同会拒绝。它读取实际 10 列 `ProfessionalTaskMaps` 命名表，原位保留既有工作表、业务值、公式、样式和表结构，并在表尾按批准顺序添加六个画像列，将表范围扩为 16 列。
- 每个旧版有专业代码的映射行在六个新字段都写为 `需补录`；不从旧字段推断别名、课程、方法、任务、成果或流程。升级摘要准确计数这些需补录行。
- 临时文件先经当前 `LedgerStore.validate()` 验证，再以原子替换发布到调用方指定暂存路径。任何输入/schema/验证失败都不创建或覆盖指定输出。
- 已是 16 列的主台账走确定性的已验证暂存复制，摘要 `upgraded_legacy_schema=False`、需补录计数 0，源与副本 SHA-256 相同。
- 旧版升级后的文件能被当前 `LedgerStore` 打开及校验；`load_task_profiles_from_ledger` 把 `需补录` 视为不可见占位并抛出 `TaskProfileReadError`，直至六维字段均被人工填入。

### P2：中文逗号解析

分隔符现覆盖换行、顿号、中文/英文分号、中文/英文逗号。保存后重开的 Excel 中 `交通运输，transportation engineering` 被精确解析为两个别名，并生成 28 条（7 个词 × 4 平台）六维 QueryJobs。

### 回归、520 行结构与依赖说明

全量命令：

```powershell
$env:PYTHONPATH = '07_自动维护工作流/src'
python -m unittest discover -s 07_自动维护工作流/tests -v
git diff --check
```

输出：`Ran 50 tests in 4.692s`、`OK`；`git diff --check` 无差异错误。当前 16 列 workbook 的 520 行 OOXML 测试仍通过：`专业任务映射` 表范围与自动筛选均为 `A1:P521`。

初始报告所记“安装 requirements.txt 后”是已发生的历史事实，不是当前未解决顾虑：实际执行的是 `C:\Program Files\Python311\python.exe -m pip install -r 07_自动维护工作流/requirements.txt`，在该解释器的 site-packages 安装锁定依赖；本轮没有卸载或新增依赖。

### 本轮改动与顾虑

- `07_自动维护工作流/src/skill_maintainer/ledger.py`
- `07_自动维护工作流/src/skill_maintainer/catalog.py`
- `07_自动维护工作流/tests/test_ledger.py`
- `07_自动维护工作流/tests/test_catalog_queries.py`

Excel UI 烟测仍由控制器在已关闭句柄的暂存副本上执行；本轮只做结构、OOXML 与重开核验。

---

## Approved 后控制器 Excel UI 烟测夹具（2026-08-27）

基于当前 HEAD `1e3bec96` 的产品 `LedgerStore` 生成；未打开 Excel，写入后用 `LedgerStore.load()` 重开核验并关闭所有句柄。

- 绝对路径：`C:\Users\34927\AppData\Local\Temp\task5-approved-ui-smoke-m2dk9pq_\professional-task-maps-520.xlsx`
- SHA-256：`abd8b9c67eb38722a3ce6f38ab8fa8b16148e509919e311f7f458e5f6101b91f`
- `专业任务映射`：520 行、16 列；`LedgerStore.validate()` 返回空列表。
- 控制器预期单元格：`专业任务映射!A521 = APPROVED-PROFILE-0520`。

---

## 最终真实 Excel UI 只读烟测（主控执行，2026-08-27）

主控对以下夹具完成了真实 Excel UI 只读烟测：

- 夹具：`C:\Users\34927\AppData\Local\Temp\task5-approved-ui-smoke-m2dk9pq_\professional-task-maps-520.xlsx`
- SHA-256：`abd8b9c67eb38722a3ce6f38ab8fa8b16148e509919e311f7f458e5f6101b91f`
- Excel 窗口标题：`professional-task-maps-520 - 只读 - Excel`；无修复提示。
- `专业任务映射` 显示 16 列。
- Go To `A521` 后，名称框为 `A521`，公式栏与单元格值均为 `APPROVED-PROFILE-0520`。
- 关闭时未保存；最终 Excel 进程状态为 `isRunning=false`、`windows=[]`。
