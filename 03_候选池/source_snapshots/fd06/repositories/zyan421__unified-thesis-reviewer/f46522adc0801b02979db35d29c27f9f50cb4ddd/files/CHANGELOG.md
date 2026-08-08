# Changelog

All notable changes to `unified-thesis-reviewer` documented in this file.

Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.7.0] — 2026-05-15

### 本次发布的总体定位

v2.6 在三次大规模实测（刘梓璇 22/22、胡文仲 27/27、谢佳谕 19/19）后表现良好，但在第四次硕士论文 PDF 审查中暴露了**v2.6 的盲区**——这些盲区不是工具层的，而是 Agent 判断层面的系统性偏差：

1. **严重度判定缺乏标尺**：把"同段两脚注引同一文献同一页"这种本身合规的现象定为致命级指控
2. **批注挂载位置原则缺失**：把"独创性问题"挂在文献综述、把"全文级问题"挂在不相关的具体段落
3. **PDF anchor 容错缺失**：PDF 中"第188条"实际是"第 188 条"（带空格），严格搜索失败，导致 3 条 anchor 降级为左上角便签

v2.7 针对性修复，并把 v2 系列所有暴露过的失误**案例化**为反面教材。

### Added（新增）

- **`rules/issues-schema.md` § 2.0a 严重度判定标尺**（含反向举证原则）：明确 fatal/major/minor 的判定边界。规定 fatal 必须通过"反向举证测试"——能否找到合理解释推翻这个指控？若能，不应定为 fatal
- **`rules/annotation-placement.md`**：批注挂载位置原则。三条核心原则——(1) 挂在读者最该看到的地方而非问题最早出现的地方；(2) 全文级问题挂在论文相关章节的章首段；(3) 比较性问题挂在"贡献说明"的位置
- **`rules/anchor-text-locator.md` § 7 PDF 输入的特殊建议**：明确告诉 Agent PDF 排版的"隐形空格陷阱"，并提供 anchor 选取策略
- **`rules/case-studies.md`**：实战案例库。7 个真实失误案例（脚注重复指控过严、独创性挂载错位、监察法挂载错位、PDF anchor 失败、藏民终17号编造证据、第四章自动编号误判、"幽灵引用"措辞过激），每个案例标注"指向的规则"

### Changed（变更）

- **`tools/annotate-pdf.py` 重大改造**：
  - 新增 `_generate_space_tolerant_variants()` 函数：自动生成 anchor_text 的空格容错变体（中文↔数字、中文↔字母边界）
  - 新增 `_try_search_with_variants()` 函数：依次尝试原文与所有空格变体
  - `search_near_page()` 和 `search_fulltext()` 改用容错搜索路径
  - `AUTHOR` 改为"张老师的AGENT"（v2.6 仅 docx 改了，pdf 未同步）
  - `VERSION` 升至 2.7.0
- **`SKILL.md`**：版本号升至 2.7.0，新增 v2.7 升级说明

### Fixed（修复）

| v2.6 失误 | v2.7 修复 |
|---|---|
| 同段两脚注引同一文献同一页 → 定为致命级 | 严重度标尺 + 反向举证 → 降为 minor，措辞中性 |
| 独创性问题挂在文献综述"叶汉杰指出..."旁 | 挂载位置原则三 → 挂在"本文主张..."贡献说明段 |
| 监察法缺位挂在赵作海案段落 → 兜底左上角 | 挂载位置原则二 → 挂在困境章章首段 |
| PDF anchor "该法第188条首次" 搜不到 | 空格容错 → 自动尝试"该法第 188 条 首次"等变体 |
| PDF anchor "有该法第30条明确列举" 搜不到 | 同上 |

### 实测改进数据

| 指标 | v2.6 | v2.7 |
|---|---|---|
| 硕士论文 PDF 批注命中率 | 17/20 精准 + 3 条降级为左上角 | **20/20 全部精准** |
| PDF anchor 严格搜索失败时的处理 | 降级为左上角便签（用户易错过） | 自动空格容错→精准定位 |
| 同类现象的严重度判定 | 凭印象（易升级为指控） | 标尺 + 反向举证（中性化） |

## [2.6.0] — 2026-05-14

### 本次发布的总体定位

v2.0-v2.5 在多轮实测中暴露了**两大类系统性问题**：
1. **批注定位严重错位**——v2.0 在含 `<w:sdt>` 容器（如 Word 自动生成的目录字段）的 docx 文档上，批注命中率仅 15%（如 6 条批注挤在湘大封面标题）
2. **审查过度偏向形式问题**——v2.5 实测刘梓璇论文形式问题占 60%，实质性问题（思想性硬伤、论证缺陷、自相矛盾、研究承诺失约）仅占 15%

v2.6 针对性修复，并补足了多项实战暴露的盲区。三次实测全部命中率 100%，实质性问题占比 44-64%。

### Added（新增）

- **`rules/substantive-review.md`**：实质性维度强制审查清单（七维度）。从"Agent 可选"升级为"Agent 必选"。规定实质性问题占比阈值（本科 ≥ 50%、硕士 ≥ 60%、博士 ≥ 65%），不达标触发"再审一轮"
- **`rules/ooxml-style-check.md`**：OOXML 样式层核查指引。修复 v2.5 三个 bug——刘梓璇论文"第四章遗漏章号"误报（实际是 `<w:numPr>` 自动编号）、胡文仲论文"一二章 pStyle=TOC1 错用作正文样式"未发现、谢佳谕论文"七章 pStyle=none"未发现
- **`rules/table-audit.md`**：表格审查规则。基于"藏民终17号事件"教训——审查表格必须先读表格内容、提及脚注号必须先 verify 实际内容
- **`rules/anchor-text-locator.md`**：anchor_text 主路径定位机制详解。包括 sdt 容器递归收集、目录条目识别、字级精确高亮
- **主工作流新增 §4.5**：实质性维度专章审查（含 §4.5.1 OOXML 样式核查 + §4.5.2 表格审查）

### Changed（变更）

- **`tools/inject-docx-comments.py` 重大改造**：
  - 段索引算法：从只读 body 直属 `<w:p>` 改为递归收集（含 `<w:sdt>` 等容器内段）。新增 `_collect_body_paragraphs()` 函数
  - 主定位手段：从 `paragraph_index` 数字索引改为 `anchor_text` 全文搜索（schema 早已要求但 v2.0 未消费此字段）。新增 `locate_by_anchor_text()`、`locate_anchor_offset_in_paragraph()`、`_is_toc_entry()` 函数
  - 目录条目识别：v2.6 增强 `_is_toc_entry()` 正则识别"中文紧贴数字"形态（如"...制度构造31"），避免 anchor 误命中目录区段
  - 字级精确高亮：anchor_text 命中段后，再在段内字符级定位 anchor 位置（而非高亮整段）
  - anchor 未命中时不再退回数字索引：改为直接返回 None 走章节降级，避免用已知不可靠的 paragraph_index 误导用户
  - `write_annotated_docx` 改用 ZipInfo 透传保留压缩元数据
- **批注作者署名**：`AUTHOR` 从 `"unified-thesis-reviewer"` 改为 `"张老师的agent"`（缩写 ZA）。与真人导师 Word 账户名（如"张庆霖"）形成视觉区分

### Removed / Deprecated（取消）

- **"幽灵引用"概念**：参考文献列出但未脚注引用的条目不再视为问题。原因：参考文献本质是"阅读/参考过的文献清单"，并不要求每条都在脚注中显式调用——作者完全可能真读过、参考过，但行文中未必用到引注
  - `tools/citation-crossref.py` 保留 `in_refs_not_in_text` 输出（仅作为信息提示），但 issues.json 不再生成对应 issue
  - `rules/orchestration-flow.md` §5、`rules/report-merging.md` §4.3、`templates/unified-report-template.md` §⑩ 同步更新
- **术语风格**：禁用"幽灵""造假""涉嫌"等高刺激词，鼓励"疑需核实""建议核对""未匹配"等中性表述

### Fixed（修复）

- **批注定位错位**：v2.0 实测命中率 15%（17/20 错位），v2.6 实测命中率 100%（22/22、27/27、19/19）
- **第四章自动编号误判为漏字**：v2.5 把"四、"由 `<w:numPr>` 注入的情况误判为"作者漏写章号"。v2.6 改诊断为"章节编号混用：第 X 章用自动编号、其余章手写"
- **藏民终17号事件**：v2.5 Agent 看到表标题里某案号，凭印象脑补"省份代字笔误"，并编造了不存在的脚注号作为证据。v2.6 强制要求审查表格先读表内容、提及脚注号先 verify

### 实测改进数据

| 论文 | v2.5 实质性问题占比 | v2.6 实质性问题占比 | v2.6 批注命中率 |
|---|---|---|---|
| 刘梓璇《证券虚假陈述》 | 15% (3/20) | **64% (14/22)** | 22/22 |
| 胡文仲《生成式 AI 著作权》 | — | **44% (12/27)** | 27/27 |
| 谢佳谕《政府采购电子化平台》 | — | **63% (12/19)** | 19/19 |

## [2.0.0] — 2026-05-14

### 重大变更：基于 v1 实战反思的 10 项系统性升级

#### Added（新增）

- **`tools/annotate-pdf.py`**：v2 主力 pdf 批注脚本。使用 PyMuPDF 把批注**直接嵌入原 pdf 副本**，任何 pdf 阅读器（WPS / Chrome / Preview / Adobe / Foxit）打开即见，无需手工导入
- **`tools/extract-pdf-text.py`**：pdf 文本 + 坐标预提取工具。Agent 生成 issues.json 时可参考，以生成高质量的 anchor_text
- **`tools/citation-crossref.py`**：引用交叉对比工具。自动生成"脱钩作者表""幽灵引用表""匹配成功表"，替代 Agent 主观判断
- **`rules/pdf-annotation.md`**：v2 主路径规则文档，取代 v1 的 `rules/xfdf-annotation.md`
- **`rules/academic-integrity-guard.md`**：假阳性守门条款。致命指控必须证据链闭环，自动推进模式下 fatal 自动降级 major（除非联网确证）
- **交互节点 E**：是否匿名化报告（在 `templates/interaction-prompts.md` §E）
- **issues.json schema `anchor_text` 字段**：v2 必填，供 pdf 批注定位精确文本锚点
- **报告章节 ⑩ 交叉引用对比表**（`templates/unified-report-template.md`）
- **报告章节 ⑦ 分维度评分表**：替代 v1 "整体评价 + 总评分档"，避免 skill 越权下总评
- **"时效性自检" 小节**：每份报告开头对照 current_date 做时间线自检
- **主工作流 §0 时间基准**：强制获取 current_date，避免时间判断错误
- **联网核实 §2.1 高优先级 15 项强制核实清单**：每条 ≥ 2 次尝试
- **v2 新增测试**：`tests/test_annotate_pdf.py`（6 条新 property）

#### Changed（变更）

- **pdf 批注主路径**：从 v1 的 XFDF 旁路文件（`tools/generate-xfdf.py`）切换到嵌入式 pdf（`tools/annotate-pdf.py`）。generate-xfdf.py 保留作备用，用户明确要 XFDF 时才启用
- **依赖声明**：v2 接受 `PyMuPDF` 作为软依赖（pdf 路径用），v1 的"纯 stdlib"约束仅对 docx 路径保持
- **联网核实**：从 v1 "降级为先"改为"强制执行为先"。之前允许"工具返回噪声大 → 整章降级"，v2 改为"每条高优先级事项至少 2 次搜索；失败才降级单条"
- **引注方案推断**（节点 B）：v1 默认《法学引注手册》；v2 基于 `citation-crossref.py` 样本**先推断**作者实际方案，不明时默认"双方案对比"
- **致命指控要求**：v2 严格要求证据链闭环（`rules/academic-integrity-guard.md` §2.1–§2.4），缺证据的 fatal 自动降级 major
- **SKILL.md keywords**：新增"严格审查"等触发词
- **报告模板**：每条 issue 强制带"证据来源"标签（[联网核实] / [原文核对] / [文本分析] / [规则依据]）
- **annotation-body-template.md**：三条批注路径（docx / annotate-pdf / xfdf）共用的统一模板说明更新

#### Fixed（修复）

- **时间线误判**：v1 有把已发生日期误判为"未来日期"的 bug，v2 通过 §0 时间基准 + `current_date` 对照修复
- **假阳性"脚注编号重复"**：v1 依赖 pdftotext 提取文本流的 grep 结果做判断，v2 要求回到原 pdf 核对
- **"参考文献脱钩"武断指控**：v1 仅用 grep 少量学者名，v2 通过 `citation-crossref.py` 机械对比替代
- **WPS / Chrome 等阅读器打不开 XFDF**：v2 嵌入式 pdf 路径根治此问题

#### Deprecated（弃用但保留）

- `tools/generate-xfdf.py` 降级为"备用路径"。用户明确要 XFDF 时仍可使用
- `rules/xfdf-annotation.md` 保留。`rules/pdf-annotation.md` 为新默认

---

## [1.0.0] — 2026-05-13

### Initial release

- 一站式编排 legal-thesis-reviewer + legal-citation-checker
- 统一 Markdown 报告 + issues.json
- docx 批注注入（Word comments）
- pdf XFDF 旁路文件生成
- 12 条 correctness properties
- 跨 6 平台可移植性设计
- 60 个开发任务完成
