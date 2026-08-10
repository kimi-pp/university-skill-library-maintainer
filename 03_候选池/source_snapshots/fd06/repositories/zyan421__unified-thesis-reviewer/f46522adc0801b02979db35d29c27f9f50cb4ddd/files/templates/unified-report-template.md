<!--
Unified_Report 模板 v2.0.0

v2 相对 v1 的关键变化：
- 新增开头"时效性自检"小节（R8.9）
- 新增开头"自动推进模式声明"小节（如果是自动模式）
- ⑦ 整体评价改为"分维度评分表"（U7）
- 末尾新增⑩"交叉引用对比表"章节（U8）
- 每条 issue 使用"证据卡"格式（U10），必须含证据来源标签
- 末尾新增"指控可信度表"（U5，自动模式下必须）

Agent 填入时：
- 占位符 {{...}} 按 `templates/interaction-prompts.md` §E 的匿名化规则处理
- <!-- SECTION --> 注释标记由合并器填充
- 章节标题（##）不得改动
-->

# 法学论文统一审查报告

<!-- REPORT_META
- 生成时间: {{generated_at}}
- skill 版本: unified-thesis-reviewer v2.0.0
- 底层 skill: legal-thesis-reviewer + legal-citation-checker
- 当前日期（current_date）: {{current_date}}
- 宿主联网能力: {{network_tools_status}}
-->

---

## 时效性自检

- 当前日期（current_date）：{{current_date}}
- 论文中出现的最晚日期：{{latest_date_in_thesis}}（定位：{{latest_date_location}}）
- 差距：{{gap_months}} 个月
- 时效性评估：{{timeliness_assessment}}

---

## 自动推进模式声明

<!-- AUTO_MODE_NOTICE: 仅在用户选择"自行推进"时展示;否则删除本段 -->

本次审查在自动推进模式下执行，5 个交互节点采用以下默认值：

- 节点 A（论文类型）：{{type}}（依据：{{type_reason}}，置信度：{{type_confidence}}）
- 节点 B（引注方案）：{{scheme}}（依据：{{scheme_reason}}，置信度：{{scheme_confidence}}）
- 节点 C（分章）：{{chapter_split}}
- 节点 D（批注）：{{annotate}}
- 节点 E（匿名）：{{anonymize}}

如任一节点推断与用户期望不符，请告知 Agent 重新执行对应环节。

---

## ① 论文基本信息与元数据

- 题目：{{thesis_title}}
- 培养单位：{{institution}}
- 作者：{{author}}
- 指导教师：{{supervisor}}
- 论文类型：{{type}}（节点 A 确认）
- 校对方案：{{scheme}}（节点 B 确认）
- 篇幅：约 {{word_count}} 字
- 章节数：{{chapter_count}} 章
- 脚注数：{{footnote_count}} 条
- 参考文献：{{reference_count}} 条
- 是否具备页码：{{has_page_number}}
- 输入形态：{{input_type}}
- 批注产物可用性：{{annotation_availability}}

---

## ② ⛔ 致命问题（R1–R4 红牌）

<!-- FATAL_ISSUES
按证据闭环的 fatal issue 列出。每条按"证据卡"格式（见 `rules/report-merging.md` §2.1）：
- 必须有 [联网核实] 或 [原文核对] 证据标签
- 自动推进模式下,未联网核实的 fatal 自动降级为 major(不出现在 ②)
如无 fatal 致命问题,填入"—(本轮未发现致命问题)"
-->

---

## ③ 论文深度审查结论（九大维度，按严重程度排序）

<!-- TR_RESULT
分 fatal / major / minor 三档,每档按 paragraph_index 升序。
每条 issue 使用"证据卡"格式。
-->

---

## ④ 引注格式校对结论（{{scheme}} 方案）

<!-- CC_RESULT
按问题类型分组:
- 结构性问题(M 规则: 编号重复、序号缺失等)
- 格式问题(逐条)
- 信息缺失
每组按 page 升序。

多方案对比模式(节点 B 选 C 时)：
- 先列 GB/T 7714 视角的问题
- 再列《法学引注手册》视角的问题
- 两视角都认为有问题的标记 [两方案共识]
-->

<!-- CROSS_REFS
与 ③ 相关 issue 的交叉引用
-->

---

## ⑤ 联网核实结果（四步式）

<!-- ONLINE_VERIFY
每条按 `rules/online-verification-unified.md` §1 的四步式呈现:
1) 定位
2) 原文复述
3) 联网核实(尝试 ≥ 2 次,多源验证时 §3)
4) 学理判断

整章顶部报告:
- 调用了哪些联网工具
- 总核实对象数、成功数、失败数
- 多源冲突的条目数(若有)

若完全无联网工具 → 走"待用户核实"降级(§4)
-->

---

## ⑥ 遗漏但应讨论的问题清单

<!-- MISSING_DISCUSSIONS
本属题中应有之义但论文未展开的问题。每条一行,不少于 3 条(高质量审查应有 5-10 条)
-->

---

## ⑦ 分维度评分表

<!-- DIMENSIONS_SCORE
分 9 个维度独立评分(A/B/C/D),不给总评。
-->

| 维度 | 评分 | 说明 |
|---|---|---|
| ① 选题与问题意识 | {{s1}} | {{s1_note}} |
| ② 结构与逻辑 | {{s2}} | {{s2_note}} |
| ③ 论证深度 | {{s3}} | {{s3_note}} |
| ④ 文献综述 | {{s4}} | {{s4_note}} |
| ⑤ 实证 / 案例 | {{s5}} | {{s5_note}} |
| ⑥ 法律规范适用 | {{s6}} | {{s6_note}} |
| ⑦ 语言与学术规范 | {{s7}} | {{s7_note}} |
| ⑧ 对策建议 | {{s8}} | {{s8_note}} |
| ⑨ 引注格式 | {{s9}} | {{s9_note}} |

**评分说明**：

- **A**：基本无问题或仅轻微建议
- **B**：有改进空间但不影响整体质量
- **C**：需要重要修改
- **D**：需根本性重写或紧急核实

**由用户 / 导师综合这 9 个维度的评分独立判断整体是否达标。本 skill 不做总体定性。**

---

## ⑧ 修改优先级 Top 10

<!-- TOP10
按 rules/report-merging.md §3 打分规则生成(含 v2 新增的 evidence_boost)
每条格式:
N. [score: X.X] 【{category_cn}】({severity_cn}) {problem} → {suggestion[0]}
   定位：{chapter} 第 {page} 页(group_id: {group_id})
   证据：[联网核实] / [原文核对] / [文本分析] / [规则依据]
   详见：§2 / §3 / §4 / §5
-->

---

## ⑨ 答辩质询问题（5–10 条）

<!-- VIVA_QUESTIONS
面向答辩委员会的质询建议,与 ⑦ 评价不重复。
聚焦论文中"论证不充分 / 论据可疑 / 反例未回应"的具体点。
-->

---

## ⑩ 交叉引用对比表（v2 新增）

<!-- CROSSREF_TABLES
来自 tools/citation-crossref.py 的三份对比表。
-->

### ⑩.1 疑似脱钩作者（正文引用但参考文献表无条目）

<!-- IN_TEXT_NOT_IN_REFS -->

> ⚠️ 本表由 citation-crossref.py 自动生成，可能存在误报（如作者名在参考文献以"拼音 / 繁体 / 合著者首位"形式出现时未能匹配）。建议用户对每条逐一核对后再做修改。

### ⑩.2 匹配成功统计

<!-- MATCHED_STATS -->

> **v2.6 改动**：取消"参考文献列出但正文未引用"小节。参考文献本质是"阅读/参考过的文献清单"，并不要求每条都在脚注中显式调用——这不是规范问题，不再纳入报告。仅保留"脚注引但参考文献漏"（脱钩）这一种真问题。

---

## 指控可信度表（自动模式必须）

<!-- CREDIBILITY_TABLE
仅在自动推进模式下展示;交互模式可省略。
-->

本报告共 {{total_issues}} 条指控，按可信度分布：

| 级别 | 数量 | 说明 |
|---|---|---|
| 高可信度（联网核实 + 证据闭环） | {{high}} | 建议优先核对与修复 |
| 中可信度（文本分析 + 规则依据） | {{medium}} | 建议逐条验证 |
| 低可信度（仅 grep / 推断） | {{low}} | 建议谨慎采信 |

**建议用户按从高到低可信度优先核对。**

---

## 附录 A：批注 pdf / docx 导入指引

<!-- INCLUDE_ANNOTATION_GUIDE
pdf 输入 → 展示"嵌入式 pdf 直接打开"说明(默认)
docx 输入 → 展示"Word/WPS 打开 .annotated.docx"说明
用户明确要 XFDF → 展示旧 XFDF 导入指引
-->

---

<!-- BEGIN_OPTIONAL_FAIL_BLOCK
仅在 issues.json 自校验失败时附以下块,否则删除
-->

---

## ⚠️ 结构化清单未生成，批注文档不可用

本次执行产出了 Markdown 报告，但 `issues.json` 未通过自校验，因此批注 pdf / docx 不会生成。

**失败原因（前 5 条）**：

<!-- FAIL_REASON_LIST -->

**可重试**：修复原因后运行：

```bash
# pdf 批注（v2 主路径）
python3 tools/annotate-pdf.py 原.pdf issues.json 输出.annotated.pdf

# docx 批注
python3 tools/inject-docx-comments.py 原.docx issues.json 输出.annotated.docx
```

<!-- END_OPTIONAL_FAIL_BLOCK -->

---

*报告由 `unified-thesis-reviewer` v2.0.0 生成*
