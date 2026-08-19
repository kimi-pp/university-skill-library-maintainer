---
name: econ-paper-reader
version: 0.8.2
author: ohjerryho
description: >
  Systematic reading, interpretation, and critical analysis of economics papers — empirical,
  theoretical, structural, or mixed; English top-journal or Chinese CSSCI style. Use this skill
  whenever the user needs to read, summarize, analyze, critique, or understand an economics
  paper. Trigger on phrases like: "read this paper", "help me understand this paper", "what's
  the identification strategy", "explain this model", "is this paper convincing", "what does
  this table show", "summarize the findings", "what's the contribution", "how does the theory
  work", "is this identification valid", "what are the main assumptions", "should I cite this",
  "analyze this working paper", "help me understand the econometrics", "what's the story here".
---

# econ-paper-reader

Economics papers communicate through a strict narrative logic — understanding that logic is the
key to reading them well. This skill reverses the conventions of top-journal writing to decode
what each section is *supposed* to contain, then reads accordingly.

## Step 1: Classify the paper

Before reading in depth, determine the paper's dominant mode:

| Type | Defining signals |
|------|-----------------|
| **Empirical — Reduced Form** | Identification section, regression tables, DiD/IV/RDD/SC design, robustness checks |
| **Empirical — Structural** | Model primitives → equilibrium → estimation (GMM/MLE/SMM), counterfactual simulations |
| **Theoretical** | Formal assumptions, propositions, proofs, corollaries, comparative statics |
| **Mixed** | Theory motivates empirics, or empirics validate a structural model |
| **Methodology** | New estimator/test, asymptotic theory, Monte Carlo simulations, methods critique, "how to do X" guide |
| **Survey / Perspective** | Literature mapping, broad citations, no primary identification, often invited |

Most serious papers are **Mixed**. The dominant mode determines which subskill leads; load
additional subskills for supporting sections.

For detailed taxonomy and edge cases → `references/paper-taxonomy.md`

## Step 2: Route to subskills

After classifying the paper type in Step 1, load subskills according to this **deterministic table**. Do not deviate.

| Paper type | Load these subskills (in order) |
|------------|--------------------------------|
| Empirical — Reduced Form | epr-structural → epr-empirical → epr-causal-inference → epr-tables-figures |
| Empirical — Structural | epr-structural → epr-empirical → epr-theoretical → epr-tables-figures |
| Theoretical | epr-structural → epr-theoretical |
| Methodology | epr-structural → epr-methodology → epr-causal-inference (if ID strategies critiqued) |
| Mixed | epr-structural → epr-empirical → epr-theoretical → epr-causal-inference → epr-tables-figures |
| Survey / Perspective | epr-structural → epr-review |

**Always add additionally:**
- `epr-policy-context` — if the paper studies a policy/event/reform, OR is Chinese-language
- `epr-related-refs` — always load last, for every paper type

Additional reference files (load only if the relevant subskill instructs it):
```
references/causal-methods-ref.md        ← deep reference on 10 CI methods
references/theory-components-ref.md     ← model primitives, equilibria, proof reading
references/chinese-vs-english.md        ← when reading Chinese-language papers
```

## Step 3: Read with purpose

Choose reading depth based on the user's goal:

**Quick scan** (5 min): Abstract → Introduction → Conclusion → skim tables.
Activate: `epr-structural` only. Output: 3–5 sentence summary.

**Standard read**: Full paper. All relevant subskills.
Output: Full reading report (format below).

**Referee read**: All subskills + section-by-section critical evaluation.
Output: Reading report with extended Concerns section and a verdict.

## Reading report format

Always produce a structured report. Depth scales with reading mode.

**CRITICAL output rules**:
1. Begin the report immediately with the paper title. Never write processing notes, progress summaries, or internal comments such as "Now I have enough material…", "Based on my reading…", or any similar meta-commentary before or after the report body. The report is the only output.
2. Section headers must be **consistent in language throughout the report** — either all Chinese or all English. Never mix. Parenthetical translation is allowed (e.g., "核心问题 (Core Question)" or "Key Results（主要发现）"). Choose the language that matches the main body language of the report.
3. **LaTeX formatting**: All mathematical expressions — equations, formulas, variables ($Y$, $D_{it}$), Greek letters ($\alpha$, $\beta$, $\sigma$), subscripts, superscripts — must use inline math (`$...$`) or display math (`$$...$$`). This includes isolated symbols appearing in running text. Never use fenced code blocks (` ```tex ``` `, ` ```latex ``` `, any ` ``` ` variant, or single backtick `` `x_i` `` style) for math. This ensures formulas render correctly in all Markdown viewers.
4. **Bilingual terminology**: Key terms, concept names, variable names, and technical jargon must preserve the original-language form on first use. When writing in Chinese about an English paper, write the Chinese translation followed by the English original in parentheses on first occurrence — e.g., "买方势力（buyer power）"、"双重差分法（difference-in-differences, DiD）". When writing in English about a Chinese paper, write the English followed by the Chinese in parentheses — e.g., "event study method（事件研究法）". Subsequent occurrences may use either form alone.

```
# [论文标题 / Paper Title]

**作者**: [Authors]
**来源**: [Journal / Source, Year]  *(no page numbers)*
**研究领域**: [e.g., 国际贸易、产业组织、劳动经济学]
**Paper type**: [e.g., Empirical-RF / Theory / Mixed / Methodology]

---

### 这篇文章讲了个什么故事

[一段完整的研究叙事（通常4–8句），按这个逻辑展开：
①现实中有什么问题或谜题？②为什么既有文献没有解决，或解决得不够好？③这篇文章的核心思路或方法是什么？④发现了什么？⑤这意味着什么（对理论、政策或未来研究的意义）。
不要只是列要点——要像讲故事一样，让读者在开篇就能完整感受到这篇文章的来龙去脉和价值所在。]

### 政策与背景 *(有政策内容或中文文献时填写，按 epr-policy-context 子技能填写；纯理论/方法论文略去)*

### 核心问题

[一句话：本文回答什么问题？]

### 研究设计

[研究设计是故事到模型/实证方法之间的桥梁，要回答以下问题：
- **从问题到模型**：文章关心的现实问题，在模型或实证框架中对应哪些变量、方程或估计量？（e.g., "贸易开放程度对应关税变量 $\tau_{it}$，劳动力市场扭曲对应工资加成 $\mu$"）
- **分析维度**：文章从哪些维度展开研究？（基准结果、机制、异质性、进一步验证等——说明各维度如何与核心问题相联系）
- **识别策略/理论核心**：用1–2句说清楚因果识别的来源（e.g., 利用某政策的交错实施作为准自然实验），或理论模型的核心假设与均衡机制。
不要简单复述故事；要揭示"作者用什么手段来回答问题"。]

### 模型设定 *(理论/结构估计文章必填，按 epr-theoretical 子技能的 Mandatory output block 填写；纯RF实证文章略去)*

### 实证设计 *(reduced-form 实证文章必填，按 epr-empirical 子技能的 Mandatory output block 填写；纯理论文章略去)*

**回归方程** — [LaTeX 方程，完整呈现文中所有关键估计方程]

**变量说明**

| 变量 | 含义 | 构造方式 | 选择动机 |
|------|------|----------|----------|
| ... | ... | ... | ... |

**⚠️ 设计注意事项** — [作者明确提及的问题 + 读者独立识别的潜在威胁]

### 主要发现

- [发现1——实证类请给出经济量级]
- [发现2]
- [发现3（如有）]

### 核心贡献

[作者主张的创新点是什么？如何与既有文献区分？]

### 亮点

[每一点必须锚定本文的具体特征——特定的识别设计选择、独特数据集、某个优雅的理论洞察、出人意料的发现。引用具体章节、表格或方法。不得使用"识别策略干净"等泛泛表述，除非说明是什么让它干净。]

### 不足与疑问

[先列出作者自己明确承认的局限（注明章节或脚注）。再列出读者独立识别的疑问——每条必须是针对本文具体论断的有据之言，说明为什么这个问题对本文的特定主张重要。不得写没有依据的检查清单条目。]

### 综合评价

[是否令人信服？为何？如有必要，粗略评估发表价值或引用价值。]

---

### 延伸阅读

[Top 3 most relevant references from this paper's reference list.
Follow epr-related-refs subskill for selection criteria and ref-format formatting rules.
If fewer than 3 clearly relevant references exist in the paper's reference list, only list those that are genuinely relevant — never fabricate or guess.]
```

## Core reading principles

Economics papers tell a **story with logic**, not just a sequence of results. Read to
understand the argument, not just collect findings.

- **Introduction as a map**: A well-written intro contains the whole paper in miniature —
  motivation, gap, research design, main results, contribution. Read it twice: once at the
  start to orient, once at the end to assess whether the paper delivered its promise.

- **Follow the identification logic**: In empirical papers, the central question is always
  "why should we believe this is causal?" The identification section is the paper's spine.
  If it's weak, everything downstream is weakened.

- **Model ≠ empirics**: In mixed papers, the theory model and the empirical section often
  make different claims. Check whether they actually connect — does the theory generate
  testable predictions that the empirics test, or do they run in parallel?

- **Coefficients need economic interpretation**: A statistically significant coefficient
  only matters if the economic magnitude is meaningful. Always ask: "How big is this in
  real-world terms?"

- **Robustness tells you about the authors' confidence**: The choice of robustness checks
  reveals what threats the authors are most worried about. Note what's *missing* from the
  robustness section as much as what's present.
