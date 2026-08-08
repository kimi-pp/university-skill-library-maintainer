# 任务 1 实施报告：157 项唯一小分类归属

## 实现内容

- 新建 `03_候选池/derived/subcategory_assignments.json`，逐项记录 157 个 Skill ID 到 61 个批准小分类的唯一映射；taxonomy 保留批准设计的代码、名称和收录重点。
- 对 9 个边界条目记录“主要产出优先”的 `decision_notes`，不改变任何原始候选文件。
- 新建 `06_过程记录/tools/subcategory_pipeline.py`，提供源数据加载、底账加载、完整性/大分类一致性校验和带小分类名称的派生记录。
- 新建独立 `06_过程记录/tests/test_subcategory_pipeline.py`，不依赖既有历史测试或验证脚本。

## RED 证据

命令：

```powershell
& 'C:\Users\34927\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest '06_过程记录/tests/test_subcategory_pipeline.py' -v
```

预期且实际失败：`ModuleNotFoundError: No module named 'subcategory_pipeline'`；测试在生产模块和底账文件创建前失败，原因符合预期。

## GREEN 证据与测试结果

同一命令在实现后通过：`Ran 3 tests ... OK`。

覆盖并确认：157 个源 ID 与 157 项底账完全相同；61 个 taxonomy 小分类；批准的小分类逐项计数；五个大分类总数为 20、22、31、29、55。

## 变更文件

- `03_候选池/derived/subcategory_assignments.json`
- `06_过程记录/tools/subcategory_pipeline.py`
- `06_过程记录/tests/test_subcategory_pipeline.py`
- `.superpowers/sdd/2026-08-08-五类通用小分类与报告通俗化实施计划/task-1-report.md`

## 提交

本任务提交标题：`feat: add approved subcategory assignment ledger`。

## 问题与顾虑

- 无实现阻塞。
- 已按任务说明避开既有旧测试、旧验证脚本及其已知历史问题；未修改昨天的原始报告或原始候选 JSON。

## 修复第 1 轮：拒绝规则与映射完整性

### 修复内容

- 为缺失 ID、多余 ID、重复源 ID、未知小分类、跨大分类及重复 taxonomy 代码添加最小负例和 `assertRaisesRegex`；每项直接压力测试 `validate_assignments` 的对应拒绝分支。
- `load_assignment_file` 改用 `object_pairs_hook`，在 JSON 加载期拒绝任意重复键，避免重复 assignment 键被静默覆盖。
- 添加 157 项批准 ID→小分类映射的规范化 SHA-256 断言；交换两个 ID 的分类即使保持计数不变，也会失败。

### 本轮 RED 证据

命令：

```powershell
& 'C:\Users\34927\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest '06_过程记录/tests/test_subcategory_pipeline.py' -v
```

实际失败：`test_load_rejects_duplicate_assignment_key_in_json` 以 `AssertionError: ValueError not raised` 失败；说明旧 `json.load()` 静默覆盖了重复键，失败原因符合预期。

### 本轮 GREEN 证据与覆盖结果

同一命令在加载期重复键检测实现后通过：`Ran 11 tests ... OK`。输出无警告或测试噪声。

覆盖范围：合法 157 项底账、批准逐项映射摘要、各小分类/大分类计数，以及 7 类核心非法输入（其中重复 JSON assignment 键在加载期拒绝）。

### 本轮变更与提交

- `06_过程记录/tools/subcategory_pipeline.py`
- `06_过程记录/tests/test_subcategory_pipeline.py`
- `.superpowers/sdd/2026-08-08-五类通用小分类与报告通俗化实施计划/task-1-report.md`

本轮提交标题：`test: enforce subcategory ledger rejection rules`。
