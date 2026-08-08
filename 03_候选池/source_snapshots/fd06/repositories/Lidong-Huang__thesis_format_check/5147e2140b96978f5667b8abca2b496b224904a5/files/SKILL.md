---
name: thesis-review
description: Comprehensive review of Chinese master's thesis formatting, content quality, and academic rigor. Check punctuation consistency, Chinese-English punctuation mixing, language fluency, logical flow, statistical expression, chart labeling, reference numbering, fake reference detection, abstract balance, method order, title-content alignment, heading hierarchy, and decimal places in tables. Outputs detailed review comments in a text file (.txt). Use this skill whenever the user asks for thesis review, paper formatting check, academic writing feedback, or document quality assessment for Chinese master's theses.
compatibility: Requires python-docx library for reading Word documents and WebSearch for reference verification.
---

# Thesis Review Skill

A comprehensive skill for reviewing Chinese master's theses for formatting, content quality, and academic rigor.

## Overview

This skill helps reviewers systematically examine master's theses in Chinese, focusing on both formal requirements and substantive quality. The skill extracts text from `.docx` files, analyzes multiple aspects, and generates a detailed review document with specific improvement suggestions.

## Prerequisites

Before using this skill, ensure the following:

1. **Python environment** with `python-docx` library installed:
   ```bash
   pip install python-docx
   ```

2. **WebSearch tool access** for reference verification (automatically available in Claude Code).

## Workflow

### Step 1: Extract and analyze the thesis

Read the provided `.docx` file using `python-docx`. Extract:
- Full text with paragraph structures
- Headings and their hierarchy
- Tables and their captions
- Figures and their captions
- Reference list

### Step 2: Perform comprehensive checks

Examine the thesis for the following issues:

#### A. Punctuation and formatting
- **Chinese vs English punctuation**: Identify mixed full-width (Chinese) and half-width (English) punctuation marks
- **Punctuation consistency**: Ensure consistent use of punctuation types throughout
- **Decimal places in tables**: Flag any table cells with more than 2 decimal places (unless justified by measurement precision)

#### B. Language and logic
- **Chinese fluency**: Assess sentence structure, word choice, and readability
- **Paragraph coherence**: Check for contradictions between paragraphs
- **Logical flow**: Evaluate logical connections between paragraphs and sections
- **Heading hierarchy**: Verify that subheadings are合理且连续 (reasonable and continuous)

#### C. Academic content
- **Statistical significance expressions**:
  - Check p-value formatting (e.g., `p < 0.05`, `p = 0.023`)
  - Review interpretation wording (e.g., "statistically significant difference" vs "significant difference")
- **Chart and figure titles**: Ensure titles are self-explanatory with clear data description and context
- **Numbering consistency**: Verify that charts/tables are numbered consecutively throughout
- **Reference numbering**: Check that references are numbered consecutively

#### D. Structural issues
- **Abstract balance**: Identify "头重脚轻" (head-heavy) abstracts with excessive background and minimal results
- **Materials & Methods order**: Assess logical and chronological organization
- **Title-content alignment**: Detect mismatches between main title and actual content scope
- **Subheading合理性**: Evaluate whether subheadings appropriately reflect content and flow logically

#### E. Reference quality
- **Format consistency**: Check uniform citation style throughout
- **Fake reference detection**: Randomly select 5-10 references and verify online using WebSearch

### Step 3: Generate review document

Create a new text file (`.txt`) with:

1. **Executive summary**: Overall assessment and major issues
2. **Detailed findings by section**: For each issue found:
   - **Location**: Specific section, paragraph, or line reference
   - **Issue description**: Clear explanation of the problem
   - **Suggestion**: Concrete improvement recommendation
   - **Priority**: High/Medium/Low based on impact
3. **Priority recommendations**: Top 5-10 critical fixes
4. **Positive feedback**: Aspects done well (for balance)

## Output Format

The review text file (`.txt`) MUST follow this structure:

```
[Thesis Title] - 评审意见
生成日期: [YYYY-MM-DD]

1. 总体评价
   - 主要优点
   - 主要问题
   - 修改优先级

2. 具体问题及修改建议
   2.1 格式问题
      - [具体问题1] (位置: [具体位置])
        建议: [修改建议]
      - [具体问题2] (位置: [具体位置])
        建议: [修改建议]
   
   2.2 语言与逻辑问题
      - [具体问题] (位置: [具体位置])
        建议: [修改建议]
   
   2.3 学术内容问题
      - [具体问题] (位置: [具体位置])
        建议: [修改建议]
   
   2.4 结构问题
      - [具体问题] (位置: [具体位置])
        建议: [修改建议]
   
   2.5 参考文献问题
      - [具体问题] (位置: [具体位置])
        建议: [修改建议]

3. 关键修改项 (Top 10)
   - [修改项1]
   - [修改项2]
   ...

4. 鼓励与肯定
   - [做得好的方面1]
   - [做得好的方面2]
```

## Implementation Notes

- Use `python-docx` to read the input document
- Use standard file operations to write the review as a `.txt` file
- For text extraction, iterate through `document.paragraphs` and check `paragraph.style` for headings
- For tables, examine `document.tables` and extract cell text
- For reference verification, use the WebSearch tool with queries like `"[author] [title] [year]"` to check existence
- When reporting locations, be as specific as possible: "Section 3.2, paragraph 4", "Table 5, row 3", "Reference #23"
- Balance criticism with constructive suggestions and positive reinforcement

## Common Pitfalls to Avoid

- Don't assume all punctuation mixing is wrong—some technical terms may require English punctuation
- Statistical expressions vary by field—consider disciplinary norms
- Some references may be obscure but legitimate—verify with multiple sources
- Abstract "head-heavy" assessment is subjective—provide specific word count ratios if possible

## Examples

**Example input**: A Chinese master's thesis on "人工智能在医疗诊断中的应用研究"

**Example output**: Review text file with 15 specific issues including:
- Mixed Chinese/English punctuation in literature review section
- Table 3.4 has 4 decimal places where 2 would suffice
- Reference #45 appears suspicious (not found in academic databases)
- Abstract spends 80% on background, only 20% on results
- Methods section jumps between chronological and thematic organization

---

Remember: The goal is to help students improve their work, not just criticize. Provide clear, actionable feedback that empowers revision.