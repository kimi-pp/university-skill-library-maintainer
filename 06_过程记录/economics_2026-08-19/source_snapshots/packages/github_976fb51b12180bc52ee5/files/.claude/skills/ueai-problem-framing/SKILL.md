---
name: ueai-problem-framing
description: Decompose a broad economic topic into a researchable course-project question. Triggers at stage 00 of ueaiworkflow. Use when a student or teacher says they want to "do" a paper about a topic, or invokes /ueai-stage 00.
---

# Problem framing (stage 00)

## Inputs you receive

- `{{TOPIC}}` — short title
- `{{QUESTION}}` — one-sentence draft
- `{{COURSE}}` — `贸易数据库与分析工具` or `经济建模与写作`

## What you produce

A filled `00_problem/problem_brief.md` with the following five fields:

1. **研究对象**：what country / sector / firm / period
2. **核心变量**：dependent + 2–4 candidate independent vars; clarify units
3. **可用数据**：1–3 candidate databases with concrete table/field names
4. **可能方法**：1–2 methods, each with the *minimum* assumption set
5. **结果展示**：figure types, table types — be specific (e.g. "2×2 福利分解表" not "results table")

Plus a **可核验口径 checklist** — 3–5 items the student must verify offline (HS code, country list, exchange rate base, deflator base year, etc.).

## Decomposition heuristics

For *trade-policy* topics: object = countries × HS chapters × year window. Method = SMART / GTAP / partial-equilibrium / event-study.
For *digital-economy / FDI / GVC* topics: identify a treatment or shock, identify a measurable outcome.
For *modelling-course* topics: prefer a model the student can actually run (panel FE, DID, GTAP) over fancy ones (DSGE).

If the topic is too broad (e.g. "数字经济与中国发展"), refuse to scope and ask for one country + one period + one outcome.

## Output template

```markdown
# 问题拆解

项目题目：{{TOPIC}}
对应课程：{{COURSE}}
研究问题：{{QUESTION}}

## 本阶段任务
把宽泛兴趣转化为可研究、可检验、可表达的课程任务。

## AI辅助记录
- 使用时间：{{ISO timestamp}}
- 使用工具：{{model name}}
- 使用提示词：prompts/problem-framing.md
- AI反馈摘要：
  - 研究对象：...
  - 核心变量：...
  - 可用数据：...
  - 可能方法：...
  - 结果展示：...

## 可核验口径
- [ ] ...
- [ ] ...

## 人工核验与修改
- 数据来源或课程材料核验：
- 教师要求对照：
- 人工修改说明：

## 本阶段产出
- 提交文件：00_problem/problem_brief.md
- 课堂展示或讨论记录：
- 教师反馈：
```

## What you DO NOT do

- Do not invent a "novelty" claim.
- Do not write a literature review here (that's stage 02 / 04).
- Do not pick the method definitively — propose 1–2 with tradeoffs.
- Do not fill `## 人工核验与修改`. That's the student's column.
