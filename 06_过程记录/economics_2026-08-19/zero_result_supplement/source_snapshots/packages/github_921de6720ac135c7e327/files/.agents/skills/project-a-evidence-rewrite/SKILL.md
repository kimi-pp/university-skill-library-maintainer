---
name: project-a-evidence-rewrite
description: Controlled Project A explanation rewrite workflow. Use when a task explicitly authorizes writing simple_explanation from a specific EVIDENCE_AUDIT_BATCHN_REWRITE_PLAN.md.
---

# Project A Evidence Rewrite

Use this skill only when the user explicitly authorizes JSON writing or explanation rewriting.

## Golden Sample Driven Rewrite

Before rewriting any `simple_explanation`, identify the question type and choose the closest golden sample from `GOLDEN_EXPLANATION_SAMPLES.md`.

Required mapping:

| Scenario | Golden sample |
|---|---|
| Utmost good faith / no disclosure / exception question | P1-553 |
| Contract privity / positive legal-principle definition | P1-244 / P1-245 |
| Combination question / agency responsibility direction | P1-279 |
| Reverse question / absolute wording / insurance-agent liability | P1-1291 |

Rewrite rules:

- Similar P1-553 questions must state the exception/no-disclosure direction, explain why the answer is exempt from disclosure, and explain why other facts must be disclosed.
- Similar P1-244 / P1-245 questions must be treated as positive definition questions, not reverse questions.
- Similar P1-279 questions must use the two-step combination structure: first i/ii/iii/iv, then A/B/C/D.
- Similar P1-1291 questions must explain that "lower chance" is not "no risk"; Section 2 explains the answer, Section 3 explains only the non-answer choices.
- The selected golden sample should be recorded in the rewrite plan or audit for reviewability.

## Workflow

1. Read only the specified rewrite plan.
2. Extract the exact planned IDs and field scope.
3. Create protected-field snapshots before writing.
4. Modify only planned IDs' `simple_explanation`.
5. Do not modify:
   - `original_explanation`
   - question text
   - options
   - `correct_answer`
   - `source_page`
   - `reference`
   - chapter / section fields
6. Generate:
   - Use 4-section format from `project-a-explanation-style`: 1. 考点 2. 结论 + 解释 3. 逐项解释其他选项为什么错 4. 记忆口诀
- **Strict 4-section only**：`simple_explanation` 必须严格只有 4 个一级编号标题：
  - `1. 考点`
  - `2. 结论 + 解释`
  - `3. 逐项解释其他选项为什么错`
  - `4. 记忆口诀`
- **No 5th section**：禁止任何第 5 段（`5. 遇到类似题怎么快速判断`、`5. 快速判断`、`5. 做题技巧` 等）。如需做题技巧，必须合并进第 4 段。
- **Exact headings only**：第 3 段标题必须固定为 `3. 逐项解释其他选项为什么错`，禁止 `3. ——解释其他选项为什么错`、`3. 一一解释其他选项为什么错`、`3. 其他选项为什么不适合`、`3. 其他选项为什么错`、`3. 逐项解释` 或任何带破折号 / 不完整标题。
- **No duplicate memory heading**：第 4 段标题必须固定为 `4. 记忆口诀`，正文中不要再次重复"记忆口诀"四个字。
- **Correct answer only in section 2**：正确答案为什么对，必须集中在第 2 段说明。
- **Section 3 excludes correct answer**：普通 A/B/C/D 题第 3 段只能解释非正确选项为什么错；如果正确答案是 A，只解释 B/C/D；如果正确答案是 B，只解释 A/C/D；如果正确答案是 C，只解释 A/B/D；如果正确答案是 D，只解释 A/B/C。禁止在普通题第 3 段写 "A 对" / "B 对" / "C 对" / "D 对"。组合题例外：第 3 段标题仍固定为 `3. 逐项解释其他选项为什么错`，但段内必须先解释 i/ii/iii/iv 小项对错，再解释 A/B/C/D 组合；不得把正确选项的完整理由搬到第 3 段。
- **No internal audit notes**：用户可见 `simple_explanation` 禁止出现 "新增题待复核"、"待人工复核"、"先确认答案"、"教材依据待确认"、"rewrite_basis"、"risk_note"、"audit"、"spotcheck"。
- **Simplified Chinese only**：禁止繁体字。禁止"原始解析/教材第X章/1.1.2a"等教材引用。
- **Concrete wrong-option reasons**：每个错误选项必须说具体错因，禁止"和正确答案不同"等空泛句。
- **组合题特殊规则**：第 3 段标题不变，内部分两步写。第一步判断 i/ii/iii/iv：`i 对/错：原因`、`ii 对/错：原因`、`iii 对/错：原因`、`iv 对/错：原因`。第二步判断 A/B/C/D：正确组合为什么刚好包含正确小项；错误组合具体多了哪个错误小项、漏了哪个正确小项。禁止只写"多包或少包某个小项"、不解释小项、直接凭感觉说组合、跳过小项判断。
- **图三教学风格**：采用白话+生活化类比风格。第 2 段禁止模板句（"贴合原始解析/符合教材规则/符合题意"），必须写因果解释。第 3 段禁止空泛句（"没有抓住核心判断点/只是相邻概念/概念不同"），必须说明具体错因类型（主体错/关系错/方向相反/漏关键条件等）。
- **代理/委托**类题：分清委托人/代理人/第三方三方关系。转承责任是雇主为雇员担责，不误套到代理购物场景。
- **合约相对性**类题：题干问"这是哪个法律原则"是正向定义题，不误判为反向题。
- **生活化类比**：可加入简短类比，不能太长。
   - Spotcheck must include: `simplified_chinese_check`, `no_source_reference_check`, `four_section_only_check`, `concrete_wrong_option_reason_check`, `no_generic_comparison_check`, `exact_four_headings_check`, `no_duplicate_heading_check`, `no_fifth_section_check`, `section3_exact_title_check`, `section4_no_repeated_memory_title_check`, `section3_excludes_correct_answer_check`, `no_internal_audit_note_check`, `section4_single_memory_heading_check`, `teaching_style_check`, `no_original_explanation_reference_check`, `concrete_option_reason_check`, `agency_relationship_check`, `contract_privity_direction_check`, `no_empty_template_phrase_check`.
   - If any format check fails, `format_failure_count` must be > 0 and `generic_explanation_count` must be > 0; stop and do not commit.
- `EVIDENCE_AUDIT_BATCHN_REWRITE_AUDIT.md`
   - `EVIDENCE_AUDIT_BATCHN_REWRITE_SPOTCHECK.md`
7. Run validation:
   - JSON parse
   - P1/P3 counts
   - ID continuity
   - changed-ID scope
   - changed-field scope
   - protected-field diff
   - Do Not Auto overlap
   - encoding checks

## Boundaries

- Stop on any validation failure.
- Do not stage, commit, or push unless the user explicitly asks for that task.
