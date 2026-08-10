# Task 7：全量视觉检查报告

日期：2026-08-09

分支：`feature/subcategory-plain-reports`

输入：完整交付树中的 66 份 DOCX 与 66 份 XLSX
结论：最终候选的 543 张原始检查图已逐张打开复核，严重问题为 0；结构验证仍为 DOCX 66/66、XLSX 66/264，交付树仍精确为 132 个文件。

## 1. 最终计数与检查口径

| 对象 | 应有 | 实际 | 逐张打开原图 | 结果 |
|---|---:|---:|---:|---|
| DOCX | 66 份 | 66 份、259 页、66 个 `rendered-pages.json` | 259/259 | 通过 |
| XLSX | 66 份 | 66 份、264 个工作表整表图 | 264/264 | 通过 |
| XLSX 长表高倍率分段图 | 5 个大分类总览 × 4 张 | 20 张 | 20/20 | 通过 |
| 逐图人工复核总计 | 543 张 | 543 张 | 543/543 | 通过 |
| 联系表 | 仅导航 | 137 张 | 不作为判断依据 | 已重建 |
| 交付文件 | 132 | 66 DOCX + 66 XLSX | — | 精确匹配 manifest |

检查时逐张以原始分辨率打开 PNG，检查文字截断、重叠、表格破裂、中文缺字、页眉页脚错位、异常空白、孤立标题或段落、列宽与行高不足、图表遮挡、网址溢出、字号过小、空白渲染和其他渲染异常。联系表只用于定位，未据此代替原图判断。

可审计文件位于：

- 初始哈希库存：`06_过程记录/visual_review/task-7-inventory.json`
- 独立逐图复核声明：`06_过程记录/visual_review/task-7-review-log.jsonl`
- 完成器核验结果：`06_过程记录/visual_review/task-7-finalized.json`

初始库存保持 `pending=543`，每条记录把 `relative_path + image_sha256 + width + height` 绑定到具体原图；整套库存的稳定摘要为 `80888dde132a1b3e0ef6069458efd3f6e1f5cde813b04f97efa895e91ca6d0f2`。独立复核日志共 563 条 JSONL：1 条 session、19 条 batch、543 条 image；完成结果为 `pass=543`、`nonpass=0`、`review_complete=true`。这是结构化人工复核声明，不是外部数字签名、录像或第三方见证。

## 2. Word canonical 渲染与最终页数

全部 Word 文件使用 documents 技能的 canonical `render_docx.py` 渲染。每份文件在重渲染前清空自己的输出目录，渲染后写入 `rendered-pages.json`；联系表/台账生成器要求标记中的预期页集合与实际 `page-N.png` 集合完全相同，因此页数减少后留下的旧 PNG 会被拒绝，而不是只检查“至少一页”。

最终 66 份文档的页数如下，总计 259 页：

| 大分类 | 文件键与页数 |
|---|---|
| 01 | `01-overview:5`；`01-01:3`；`01-02:6`；`01-03:2`；`01-04:2`；`01-05:4`；`01-06:3`；`01-07:3`；`01-08:2`；`01-09:4` |
| 02 | `02-overview:5`；`02-01:3`；`02-02:5`；`02-03:6`；`02-04:3`；`02-05:2`；`02-06:4`；`02-07:3`；`02-08:2`；`02-09:3` |
| 03 | `03-overview:5`；`03-01:6`；`03-02:8`；`03-03:2`；`03-04:3`；`03-05:4`；`03-06:2`；`03-07:3`；`03-08:6`；`03-09:4`；`03-10:2`；`03-11:2` |
| 04 | `04-overview:6`；`04-01:3`；`04-02:3`；`04-03:3`；`04-04:5`；`04-05:2`；`04-06:4`；`04-07:4`；`04-08:3`；`04-09:6`；`04-10:4`；`04-11:5`；`04-12:4` |
| 05 | `05-overview:6`；`05-01:3`；`05-02:4`；`05-03:4`；`05-04:5`；`05-05:6`；`05-06:2`；`05-07:4`；`05-08:7`；`05-09:5`；`05-10:4`；`05-11:4`；`05-12:3`；`05-13:3`；`05-14:4`；`05-15:7`；`05-16:4`；`05-17:3`；`05-18:4`；`05-19:5`；`05-20:3` |

## 3. 逐图人工复核批次台账

以下路径均相对于仓库根目录。每个批次中的图片均按稳定排序逐张调用原图查看；“首张—末张”是该批次的闭区间。诊断期间打开过的旧候选图不计入以下最终数字。

### 3.1 Word 页面：259/259

| 批次 | 数量 | 首张—末张 | 状态 | 问题/处理 |
|---:|---:|---|---|---|
| W1 | 32 | `06_过程记录/renders/subcategorized_docx/01-01/page-1.png` — `06_过程记录/renders/subcategorized_docx/01-overview/page-3.png` | PASS | 0 |
| W2 | 32 | `06_过程记录/renders/subcategorized_docx/01-overview/page-4.png` — `06_过程记录/renders/subcategorized_docx/02-09/page-2.png` | PASS | 0 |
| W3 | 32 | `06_过程记录/renders/subcategorized_docx/02-09/page-3.png` — `06_过程记录/renders/subcategorized_docx/03-07/page-1.png` | PASS | 0 |
| W4 | 32 | `06_过程记录/renders/subcategorized_docx/03-07/page-2.png` — `06_过程记录/renders/subcategorized_docx/04-04/page-2.png` | PASS | 0 |
| W5 | 32 | `06_过程记录/renders/subcategorized_docx/04-04/page-3.png` — `06_过程记录/renders/subcategorized_docx/04-12/page-1.png` | PASS | 0 |
| W6 | 32 | `06_过程记录/renders/subcategorized_docx/04-12/page-2.png` — `06_过程记录/renders/subcategorized_docx/05-06/page-1.png` | PASS | 0 |
| W7 | 32 | `06_过程记录/renders/subcategorized_docx/05-06/page-2.png` — `06_过程记录/renders/subcategorized_docx/05-14/page-1.png` | PASS | 0 |
| W8 | 32 | `06_过程记录/renders/subcategorized_docx/05-14/page-2.png` — `06_过程记录/renders/subcategorized_docx/05-overview/page-3.png` | PASS | 0 |
| W9 | 3 | `06_过程记录/renders/subcategorized_docx/05-overview/page-4.png` — `06_过程记录/renders/subcategorized_docx/05-overview/page-6.png` | PASS | 0 |

标题规则最终修复后，66 份 DOCX 已全部重新生成、结构验证和 canonical 重渲染；人工页检也从 0 重新开始，未沿用旧候选的逐页结论。最终检查中，信息较少的末页仍同时包含读者可见的核验说明与技术追溯，不存在只剩一个追溯标题或追溯段落的空壳页。

### 3.2 Excel 工作表整表图：264/264

每个工作簿的 `1_使用说明`、`2_AI技能清单`、`3_分类统计`、`4_来源清单` 均由 artifact-tool 单独渲染并逐张查看。

| 批次 | 数量 | 首张—末张 | 状态 | 问题/处理 |
|---:|---:|---|---|---|
| X1 | 32 | `06_过程记录/renders/subcategorized_xlsx/01-01/1_使用说明.png` — `06_过程记录/renders/subcategorized_xlsx/01-08/4_来源清单.png` | PASS | 0 |
| X2 | 32 | `06_过程记录/renders/subcategorized_xlsx/01-09/1_使用说明.png` — `06_过程记录/renders/subcategorized_xlsx/02-06/4_来源清单.png` | PASS | 0 |
| X3 | 32 | `06_过程记录/renders/subcategorized_xlsx/02-07/1_使用说明.png` — `06_过程记录/renders/subcategorized_xlsx/03-04/4_来源清单.png` | PASS | 0 |
| X4 | 32 | `06_过程记录/renders/subcategorized_xlsx/03-05/1_使用说明.png` — `06_过程记录/renders/subcategorized_xlsx/03-overview/4_来源清单.png` | PASS | 0 |
| X5 | 32 | `06_过程记录/renders/subcategorized_xlsx/04-01/1_使用说明.png` — `06_过程记录/renders/subcategorized_xlsx/04-08/4_来源清单.png` | PASS | 0 |
| X6 | 32 | `06_过程记录/renders/subcategorized_xlsx/04-09/1_使用说明.png` — `06_过程记录/renders/subcategorized_xlsx/05-03/4_来源清单.png` | PASS | 0 |
| X7 | 32 | `06_过程记录/renders/subcategorized_xlsx/05-04/1_使用说明.png` — `06_过程记录/renders/subcategorized_xlsx/05-11/4_来源清单.png` | PASS | 0 |
| X8 | 32 | `06_过程记录/renders/subcategorized_xlsx/05-12/1_使用说明.png` — `06_过程记录/renders/subcategorized_xlsx/05-19/4_来源清单.png` | PASS | 0 |
| X9 | 8 | `06_过程记录/renders/subcategorized_xlsx/05-20/1_使用说明.png` — `06_过程记录/renders/subcategorized_xlsx/05-overview/4_来源清单.png` | PASS | 0 |

### 3.3 Excel 高倍率分段图：20/20

整表图仍保留并检查；以下分段图只用于补充检查大分类总览中缩放后不易阅读的长表。每个总览均覆盖标题/表头、最长正文、最长 URL、末行四类关键区域。

| 批次 | 数量 | 首张—末张 | 状态 | 问题/处理 |
|---:|---:|---|---|---|
| S1 | 20 | `06_过程记录/renders/subcategorized_xlsx/01-overview/2_AI技能清单_segment_last-row_A24-V24.png` — `06_过程记录/renders/subcategorized_xlsx/05-overview/2_AI技能清单_segment_title-header_A1-V5.png` | PASS | 0；覆盖五个 overview 各 4 张，实际行段仍分别为 01：A1:V5/A14:V14/A24:V24，02：A1:V5/A11:V11/A26:V26，03：A1:V5/A16:V16/A30:V30/A35:V35，04：A1:V5/A21:V21/A30:V30/A33:V33，05：A1:V5/A6:V6/A51:V51/A59:V59 |

## 4. 发现的问题、RED 证据与关闭情况

所有版式修复均落在生成器或验证器，没有手工修改单件交付物；每次修改后都重新生成并验证受影响成品。

| 编号 | 发现 | RED 证据 | 生成规则修复 | 重生成/重渲染 | 最终状态 |
|---|---|---|---|---|---|
| V-01 | 大分类总览的 `2_AI技能清单` 整表过宽，屏幕缩放下不能可靠阅读长正文和 URL；旧分段输出还可能残留 | 新增 `every overview-sized catalog receives four readable inspection segments`，修复前不能为五个总览稳定给出四类关键分段 | XLSX 渲染器对五个总览自动生成标题/表头、最长正文、最长 URL、末行四张高倍率图；每本重渲染前清空旧 PNG | 5 个总览重渲染；20/20 分段图逐张复核 | CLOSED |
| V-02 | 初始 Word 候选中，多份报告末页只剩技术追溯内容，形成低价值稀疏尾页 | `test_short_value_table_does_not_add_an_empty_spacer_paragraph`、正文 11pt 合同等在修复前暴露多余高度/尾页风险 | 技术追溯合并为一个紧凑 H3 段，保留全部字段和链接，直接字号仍精确 11pt；删除短表后的空占位段 | 61 份小分类报告重生成、结构验证、整份重渲染 | CLOSED |
| V-03 | 页数减少后可能残留旧 `page-N.png`，仅检查“至少一页”会误把旧页算入最终候选 | `test_docx_inventory_rejects_stale_pages_outside_the_renderer_expected_set`：构造 marker 期望 page-1..2、目录实际 page-1..3，修复前未拒绝 | DOCX 渲染前清空单文档目录；写 `rendered-pages.json`；台账生成器精确比较 expected set 与 actual set | 66 份 DOCX 全量重渲染后为 66 目录/259 页/66 markers，无 stale PNG | CLOSED |
| V-04 | 中间候选 `04-10/page-4.png` 仍出现追溯内容孤立到末页 | `test_technical_trace_is_anchored_to_the_last_reader_paragraph` 修复前失败：最后一个读者段落 `keep_with_next=None` | 将最后一个读者可见核验段与技术追溯绑定，避免追溯单独掉到新页；未删除字段、未缩小正文 | 受影响报告先整份重生成/结构验证/重渲染，随后 66 份全量生成与渲染 | CLOSED |
| V-05 | 中间候选 `05-08/page-1.png` 的封面标题最后一个“计”字孤立成行 | `test_cover_title_size_uses_estimated_text_width_to_avoid_orphan_characters` 首次 focused run 报 `AttributeError: ... has no attribute '_cover_title_font_size'` | 新增通用加权文本宽度估算：全角字符按 1、其他字符按 0.55、空白按 0.35；封面字号上限 27pt、下限 22pt、按 0.5pt 向下取整。只调整封面标题，正文仍精确 11pt；没有针对单个文件硬编码 | 66 份 DOCX 全量重生成、结构验证、canonical 重渲染；最终 259 页从 0 重新逐页查看 | CLOSED |

V-05 的合同样例：短中文标题 `05-05` 保持 27pt，含 ASCII 的 `02-06` 保持 27pt，长标题 `05-08` 不高于 25pt，极长标题 `04-09` 不低于 22pt。实际字号变化的交付物只有 5 份：`02-08=26.5pt`、`04-09=22pt`、`04-12=26pt`、`05-08=24.5pt`、`05-19=26pt`。

相对本任务基线提交的 Git blob 变化为：

| 文件键 | 旧 blob | 新 blob | 最终 SHA-256 |
|---|---|---|---|
| `02-08` | `ad4831f7c5d0` | `7cc08f641fb0` | `9259cb9a1fb646c4b130bc03ef69d5c82fde1c2e83b8fbf4a213d7e630976709` |
| `04-09` | `7574a161fcad` | `296d70612258` | `d1105483c3be1db680879aee74dcdccf17dfa306d1233bcf182c93d05c2a780a` |
| `04-12` | `4008fd2887a3` | `5d54ad7c9b08` | `ecfb64f98d220349ca1ad394ccd31bd5b3be14f6f98120114e5b7312c6e9e7c0` |
| `05-08` | `c44a03006862` | `6a3b80622539` | `16ab1dd2be4e0a6214bc340a5ae3930ac5eb31d5c1b5698b827950604375db5c` |
| `05-19` | `6c9a212a8117` | `00fc2dd1a9c2` | `b4f1a97ecd9bf5fd39717937270f72b28d95f2d5f89b362710fa379ce50d0f99` |

本任务生成规则最终造成 62 份 DOCX 相对基线字节变化：全部 61 份小分类报告以及 `02-overview`。其他 4 份 overview 字节不变。无论字节是否变化，最终标题修复后仍重新生成并重渲染全部 66 份，人工复核也从 0 重计，因此没有把旧候选台账冒充最终结果。

## 5. 最终自动门禁证据

最终候选上运行并得到以下结果：

| 门禁 | 结果 |
|---|---|
| `python -m unittest 06_过程记录/tests/test_subcategorized_documents.py -v` | 28 tests，OK |
| `python -m unittest 06_过程记录/tests/test_subcategorized_visual_qa.py -v` | 15 tests，OK |
| `node --test 06_过程记录/tests/test_subcategorized_spreadsheets.mjs` | 29 tests，29 pass，0 fail |
| `python 06_过程记录/tools/verify_subcategorized_documents.py` | `verified=66 overview=5 subcategory=61 preset=OK content=OK hyperlinks=OK` |
| `node 06_过程记录/tools/verify_subcategorized_spreadsheets.mjs` | `xlsx=66 sheets=264 formulas=OK structure=OK` |
| `python 06_过程记录/tools/make_subcategorized_contact_sheets.py` | `delivery=132 docx_pages=259 xlsx_originals=264 xlsx_segments=20 contacts=137 pending=543 inventory_digest=80888dde...d0f2` |
| `python 06_过程记录/tools/make_subcategorized_contact_sheets.py --finalize` | 拒绝：必须显式提供 `--review-log <jsonl>` |
| `python 06_过程记录/tools/make_subcategorized_contact_sheets.py --finalize --review-log 06_过程记录/visual_review/task-7-review-log.jsonl` | `reviewed=543 batches=19 inventory_digest=80888dde...d0f2 complete=true` |

视觉合同还验证：

- 交付树会拒绝缺件、空文件、额外件和 manifest 外文件；
- 每份 DOCX 页码必须从 1 连续、非空，并与 marker 的精确预期集合相同；
- 每份 XLSX 必须恰好有 4 张整表原图；五个 overview 必须各有四类高倍率分段图；
- 完成器必须显式读取独立 review log；无日志、缺失、重复、额外、错误 hash、复核后图片替换、inventory digest 漂移、状态与 issues 冲突、批次元数据缺失或时间倒退均拒绝；
- review log 必须精确覆盖 543 个唯一相对路径，且当前图片 hash、库存 hash、复核声明 hash 三者相同；
- XLSX 和 DOCX 重渲染都会清理各自目录中的旧图。

## 6. 范围保护、顾虑与未做事项

- 没有修改学科分类；本任务只检查五个通用大分类的交付版式。
- 没有修改原始五类事实源、没有删除或覆盖原始报告、没有把候选 Skill 写成已运行。
- 没有通过缩小正文规避分页；正文、表格、链接和技术追溯的直接字号仍由测试锁定为精确 11pt。封面标题的 22–27pt 自适应不属于正文。
- 整表图在屏幕“适合窗口”显示时可能显得很小，这是 22 列长表的自然结果；原图仍保留完整分辨率，五个大分类总览另有 20 张高倍率关键区域图。最终未发现文字被裁切或渲染为空白。
- Word 页数与本机 canonical 渲染链一致；不同 Office/字体版本可能产生轻微再分页，因此交付后若换环境批量转 PDF，应复用本任务的 exact-page-set 门禁重新渲染检查。
- `.superpowers/tmp/libreoffice-portable/`、下载包、缓存和依赖目录均被忽略，未纳入提交。
- `06_过程记录/renders/` 按仓库规则为本地可重复生成的忽略目录；初始哈希库存、独立复核日志和完成结果单独保存在可版本化的 `06_过程记录/visual_review/`，生成脚本和测试也进入版本控制。
- 未推送远程。

最终遗留严重问题：**0**。

## 7. Task 7 复审修复轮 1

复审确认旧版 `--finalize` 存在自证通道：它不接收逐图复核输入，直接从库存枚举全部路径并回填 `pass`。实测旧入口输出 `reviewed=543`、退出码 0；旧 `_validate_png` 对纯白 900×500 PNG 也只因尺寸有效而放行。这两项是本轮根因，不涉及 132 个交付文件的内容。

本轮先新增失败合同并观察到 15 项视觉测试中的 10 项失败、2 项报错，失败原因分别指向缺少 image hash、缺少稳定 inventory digest、CLI 不认识 review-log/独立路径、纯白图未拒绝。最小实现后 15/15 通过：

- 初始 inventory 使用 schema v2，保持所有 543 条为 pending；每条绑定路径、SHA-256、宽、高，并对按路径排序后的绑定集合计算稳定摘要；
- review log 由先前真实人工检查的 9 个 Word 批次、9 个 Excel 批次和 1 个分段图批次确定性整理，共 19 批；reviewer 为 `codex-task7-full-visual`，session 为 `task7-final-candidate-2026-08-09`；
- review log 不是由 finalizer 生成。finalizer 只读取 inventory 与显式 `--review-log`，逐项复算当前图片 hash/尺寸/非空白指标，核验覆盖、批次、时间、状态和问题说明，再输出完成结果；
- batch 的 start/end 是依据原工具调用先后重建的序位标记，日志中已写明 `not signed wall-clock telemetry`，不宣称精确的外部时间戳；
- PNG 空白门禁以缩略灰度直方图判定：低于 0.2% 的明显非背景像素，或灰度方差低于 1.0，均视为空白/近空白。该阈值相对 543 张实际图片约 2.24% 的最低非白比例保留十倍以上余量；纯白和均匀近白测试为 RED→GREEN，浅色背景配浅灰有效内容的测试继续通过；
- 完成结果绑定 review log SHA-256 `1bf30a57d69c0da4847ac02d4ed22e3b3b7ca4ee41813678ce2a7d756b0ec642`，最终为 543 个唯一路径、543 个路径/hash 唯一绑定、19 个非空批次、543 pass、0 nonpass。

本轮没有重新渲染，因为 543 张图片未变化；也没有修改任何 DOCX/XLSX。修复前锁定的交付聚合摘要为 `b59fa8641378e71279c1de6c38ff8f7acfa1c15df3b145a6f14a1b5ddd7e21c2`，提交前将再次复算比对。
