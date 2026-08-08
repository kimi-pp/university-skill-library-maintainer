# Task 9 项目级最终验收报告

## 1. 结论

Task 9 的统一项目级验收已完成。正式结果为 `complete=true`，七项门禁全部通过，核心计数为：

| 项目 | 结果 |
|---|---:|
| 五类源记录 | 157 |
| 通用小分类 | 61 |
| 新交付文件 | 132 |
| Word / Excel | 66 / 66 |
| 原始版存档 | 10 |
| Word 渲染页面 | 259 |
| Excel 工作表整表图 | 264 |
| 大类概览分段图 | 20 |
| 逐图复核记录 | 543 |
| 人工复核批次 | 19 |

机器可读结果位于 `06_过程记录/verification/subcategorized_delivery_verification.json`。

## 2. 本任务新增内容

- 新增单一只读验收器 `06_过程记录/tools/verify_subcategorized_delivery.py`。
- 新增可注入临时项目根目录的负向测试 `06_过程记录/tests/test_verify_subcategorized_delivery.py`。
- 更新 `06_过程记录/RESEARCH_LOG.md`，记录最终验收计数、稳定性、范围保护和已知旧测试边界。
- 验收器只写指定的验证 JSON，不生成或修改报告、交付文件、原始报告、存档、渲染图或视觉审计证据。

## 3. TDD 与问题关闭记录

### 初始 RED

新测试先运行时，三个测试类均因计划脚本尚不存在而失败：

- `AssertionError: 缺少计划脚本: verify_subcategorized_delivery.py`
- 结果：0 tests，3 errors。

该失败只对应待实现的统一验收器，不是测试语法或环境错误。

### 实现后的负向覆盖

测试通过临时目录或小型真实 PNG fixture 验证以下变异均会失败：

- 五类源文件缺失、源记录重复；
- taxonomy 数量漂移、assignment 重复 JSON 键、跨大类错归属或键顺序重排；
- manifest 缺项、增项、噪声文件、空文件或额外空目录；
- 原始版存档 hash 漂移、0809 文件误入归档、原件与存档同步改名；
- CommonMark 裸空格目标、行内或引用式项目坏链、未跟踪项目 Markdown，以及 `.superpowers` / `.worktrees` 内部目录在递归和 Git 跟踪两条发现路径中的一致排除；
- Word marker 与页面集合不一致；
- Excel 工作表图或 `last-row` 分段图缺失；
- inventory digest、图片 hash、review log、finalized 完成声明漂移；
- TODO/FIXME/PLACEHOLDER/TEMPLATE、绝对临时路径、安装运行夸大、把本轮误述为学科分类；
- 同一行混合肯定/否定分句，以及“经验证可以正常使用”等夸大同义式；
- Word/Excel 富文本跨 run 或文本节点时，仍按完整段落和单元格复原后扫描；
- 验收输出只能原子写入唯一受控 JSON；失败结果为非零且 `complete=false`，保护文件摘要不变；
- 否定边界句不会被误报，例如“未安装、未运行”“不代表已成功运行”“不把候选写成已部署工具”。

最终新增测试 16/16 通过。

### 正式数据暴露并关闭的两类误报

1. 独立重建 manifest 时最初采用了不同的等价排列。修复后按批准顺序重建，同时继续精确比较 132 个路径、全部字段、66 对格式和实际交付树。
2. 文字扫描最初把否定句中的“已安装/成功运行”识别为夸大。先加入回归测试，再增加有限的否定语境识别；肯定式夸大仍会失败。

随后再次对照 brief，补强了统一门禁本身的导航验证：验收器现在以独立实现重算 61 个叶页、5 个大类导航块和总索引块的完整文本并逐行比较，不复用生成器私有渲染函数，也不只依赖链接存在或外部测试。

## 4. 七项正式门禁

| 门禁 | 独立核对结果 |
|---|---|
| 数据与分类 | 157 个唯一源 ID；20/22/31/29/55；61 个小分类；9/9/11/12/20；冻结归属 157；事实偏移 0；可读性问题 0 |
| Manifest 与交付树 | 132 个唯一文件；66 Word + 66 Excel；66 对；5 个概览 + 61 个小类；无缺失、额外、空文件或事务残留 |
| 原件、存档和 0809 边界 | 原位置 10 个五类原件；存档 10 个逐一大小和 SHA-256 相同；0809 一对存在且未进入存档或新交付范围 |
| 知识库与链接 | 61 个叶页、5 个大类导航、1 个总索引逐行一致；270 份项目 Markdown 的 1,261 个 CommonMark 链接已解析，670 个本地目标均存在；引用式和未跟踪项目 Markdown 同样纳入，内部计划与工作树目录不计入项目页面 |
| Office 结构 | Word 66/66；Excel 66/66、264 个工作表；成员、字段、公式、链接、样式和页面设置通过现有真实结构验证逻辑 |
| 视觉证据 | 259 个 Word 页面、264 个工作表整表图、20 个概览分段图；库存 schema v2 和 digest 重算一致；1 session + 19 batches + 543 images；543 pass、0 nonpass、完成状态为真 |
| 用户可见文字 | 229 份用户可见 Markdown（含 157 个 Skill 页）、157 条通俗数据的全部字符串及 132 份交付文件，共 518 个来源；Office 富文本按段落/单元格重建；问题为 0 |

Task 7 库存摘要为 `80888dde132a1b3e0ef6069458efd3f6e1f5cde813b04f97efa895e91ca6d0f2`。

## 5. 测试与命令行验收证据

- Task 1–9 相关 Python 测试：120/120 通过。
- Node Excel 测试：29/29 通过。
- 正式 Word 验证：`verified=66 overview=5 subcategory=61 preset=OK content=OK hyperlinks=OK`。
- 正式 Excel 验证：`xlsx=66 sheets=264 formulas=OK structure=OK`。
- Task 7 视觉库存：`delivery=132 docx_pages=259 xlsx_originals=264 xlsx_segments=20 ... pending=543`。
- Task 7 完成复核：`reviewed=543 batches=19 ... complete=true`。
- 全仓 Python discover：125 项中只有以下两项失败，其余 123 项通过：
  - `test_artifact_generator.ArtifactGeneratorTests.test_catalog_is_valid_and_has_expected_category_counts`
  - `test_artifact_generator.ArtifactGeneratorTests.test_manifest_contains_six_independent_deliverables`

这两项正是计划批准保留的历史期望：旧测试仍期待前三类和六份交付；没有新增失败，也未修改旧断言。

## 6. 稳定性与不改写证明

统一验收器正式连续运行两次，两个 `checked_at` 不同，但内容语义摘要相同：

`32fb874d7a61e3fc59b87429655425536cd3641c3d25750a43f43442a71cb186`

两次运行前后以下文件集合的数量和聚合 SHA-256 均不变：

| 保护范围 | 文件数 | 聚合 SHA-256 |
|---|---:|---|
| 新交付树 | 132 | `20f16d28665e2493355e4fa26c0a1a2cf2782ce8594e8f4ee28206347c3b5618` |
| 根目录报告（10 个五类原件 + 0809 一对） | 12 | `cfb60f70487711e337e7bada1e82a60ba807b5d06bfe6d8abf3bcd97c0f673bc` |
| 原始版存档 | 10 | `9be12aebdd2ed8b08b75eac3531d56a9f277b4a84a32acdb2b93d74788f12f98` |
| Word 渲染目录全部文件 | 391 | `fa084842a6983a860267d005fcfe9d16fefa73fc54f7c26becd6c47cd6f01f8a` |
| Excel 渲染目录全部文件 | 284 | `79d51db155766835a91e0743ce5f1b89b3119084014a82129a20f941d7a929d3` |
| Task 7 审计文件 | 3 | `e13cd369e2b3ae29a407abf8a04d316bd6048e59e99cb4c39438f21d316eaf54` |

## 7. 人工复核边界与顾虑

- 自动验收能核对结构、冻结事实、已管理术语说明和明确风险句式，但不能合理证明每个专业术语对所有高等教育读者都同样自然。验收 JSON 因此保留抽查 ID 与人工判断边界，没有把自动扫描写成全面语言理解证明。
- 人工清单覆盖每个大类的首尾代表项、9 个归属边界项，以及 API、CLI、JSON、DOI、GPU、SQL、UMAP、PRISMA、BibTeX、LaTeX 10 个术语及其具体来源 ID。
- 视觉完成记录是结构化人工复核声明并以图片 hash 绑定，不是外部电子签名或视频证据。
- Word 页数绑定当前规范渲染环境；换用不同 Office 或字体环境后仍应重新渲染并运行同一 exact-page-set 门禁。
- Task 6 编排器仍含指向本机打包运行时的固定 Node 路径；本机验证可用，但换用其他账号或运行环境时可能需要适配。该项是整分支复审登记的非阻塞可移植性顾虑，本轮只修 Task 9 的验收自引用，不越界修改 Task 6。
- 本任务没有修改学科分类、五类原始事实、原始报告、132 份交付或原始渲染图，也没有推送远程。

## 8. 独立复审

统一验收器完成三轮独立只读复审。前两轮发现的文字范围、混合分句、Office 富文本、归属顺序、引用式链接、导航独立性、输出保护、工作树排除和证据同步等问题均先加入失败回归再修复。第三轮结论为 `APPROVED`，未发现 Critical、Important 或 Minor 问题。

整分支最终复审随后发现一项 Task 9 自引用漂移：递归发现已排除 `.superpowers`，Git 跟踪发现却只排除 `.worktrees`，导致新提交的内部进度和报告页改变验收计数与摘要。修复先以临时 Git 仓库同时覆盖两条发现路径并取得有效 RED，再统一使用同一内部目录排除集合；普通已跟踪和未跟踪项目 Markdown 仍会纳入。严格 CommonMark 独立复算结果为 270 份项目 Markdown、1,261 个链接、670 个本地目标。
