---
name: audit-book-writing-v1
description: Write comprehensive audit books and review materials with systematic workflow. Use when writing audit survey books, practical guides, case analyses, or review materials on topics like financial audit, internal control audit, compliance audit, performance audit, IT audit, internal audit, government audit. Triggers on requests for "审计书籍", "审计综述", "审计实务", "写书", "审校", "审计案例分析", or mentions of writing audit-related books or review materials.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - TodoWrite
---

# Audit Book Writing and Review Skill

A systematic workflow for writing comprehensive audit books and conducting thorough reviews with quality assurance.

## Quick Start

When user requests to write an audit book:

1. **Initialize project** with three core files:
   - `CLAUDE.md` - Writing guidelines and terminology standards
   - `IMPLEMENTATION_PLAN.md` - Staged execution plan
   - `book_draft.md` - Main book manuscript

2. **Follow the 7-phase workflow** (see [WORKFLOW.md](WORKFLOW.md))

3. **Use standard templates** (see [TEMPLATES.md](TEMPLATES.md))

4. **Apply 4-round review process** for quality assurance

## Core Principles

### Writing Style
- Use **precise professional language**: Audit terminology should be accurate and consistent
- Cite authoritative sources: Audit standards, laws and regulations, regulatory documents
- Every claim needs supporting evidence or references
- Balance academic rigor with practical applicability
- Maintain neutrality and objectivity

### ⚠️ DATA VERIFICATION PRINCIPLE (CRITICAL)

**绝对禁止编造数据或引用材料**

#### 数据和法规引用的严格要求：

1. **法律法规引用**：
   - ✅ 必须使用法律法规库进行精准匹配查询
   - ✅ 引用时必须注明法规名称、条款号、发布日期、生效日期
   - ❌ 禁止编造或猜测法律条款内容
   - ❌ 禁止引用不确定或未经核实的法规

2. **统计数据引用**：
   - ✅ 必须使用联网工具(WebSearch)查询并标注来源网址
   - ✅ 标注数据发布机构和发布时间
   - ❌ 禁止编造或估算统计数据
   - ⚠️ 如无法查询到准确数据，必须标注："**[待核实：该数据需要人工核对后补充]**"

3. **案例数据引用**：
   - ✅ 案例中的公司名称、日期、金额等必须准确
   - ✅ 来源于公开审计报告或监管文件
   - ❌ 禁止编造案例或虚构事实

4. **标准和准则引用**：
   - ✅ 必须查阅标准原文或权威来源
   - ✅ 注明标准号、条款号、适用范围
   - ❌ 禁止凭记忆或推测引用

#### 数据查询优先级：

**优先级1：法律法规库** → 使用Grep在已转换的法规库中查询
**优先级2：联网查询** → 使用WebSearch/WebFetch查询权威网站
**优先级3：标注待核实** → 明确标注需要人工核对

#### 查询工具使用规范：

```bash
# 法律法规查询（优先）
Grep -pattern "关键词" -path="D:\project\审计书籍撰写\法律法规库\*.md"

# 统计数据查询（必须标注来源）
WebSearch "统计关键词 年份" + "来源网站"
```

#### 违规后果：

如发现编造数据或引用材料，整章节需要重新审核和修正。

### Required Elements
- **Structure overview** (table of contents with clear hierarchy)
- **Comparison tables** for each major section (standards, methods, cases)
- **Case studies** with detailed background, process, findings, and insights
- **Regulatory references** with accurate citations (standard number, clause, scope)
- **Practical guidance** with actionable steps and procedures
- **References organized by type** (standards, regulations, books, cases, papers)

### Book Structure Principles
1. **Part 1: Theoretical Foundation** - Concepts, frameworks, development history
2. **Part 2: Practical Operations** - Procedures, methods, implementation steps
3. **Part 3: Typical Cases** - Real cases with background, process, findings, insights
4. **Part 4: Regulatory Interpretation** - Standards, laws, practical applications
5. **Part 5: Emerging Topics** - Digital audit, trends, future directions

### Paragraph Structure
1. Topic sentence (main point)
2. Supporting evidence (citations + data)
3. Analysis (professional interpretation)
4. Transition to next paragraph

## Material Sources

### Audit Standards (Primary Sources)

**Chinese Audit Standards:**
- CAS (Chinese Audit Standards) - 注册会计师审计准则
- Government Audit Standards - 政府审计准则
- Internal Audit Standards - 内部审计准则

**International Standards:**
- ISA (International Standards on Auditing)
- IIA Standards - Institute of Internal Auditors
- COSO Framework - Internal Control

**Data Collection Strategy:**
```
Source: Official websites (Ministry of Finance, CICPA, Audit Office)
Types: Standards, implementation guidance, interpretation bulletins
Date: Focus on latest versions and revisions
Format: Official PDF documents, authoritative interpretations
```

### Regulatory Documents

**Regulatory Bodies:**
- Ministry of Finance (财政部)
- China Securities Regulatory Commission (CSRC, 证监会)
- China Banking and Insurance Regulatory Commission (CBIRC, 银保监会)
- National Audit Office (审计署)

**Document Types:**
- Laws and regulations (会计法, 注册会计师法, 审计法)
- Regulatory guidelines (监管指引, 通知, 规范)
- Enforcement actions (处罚决定书, 监管函)

### Practical Cases

**Case Sources:**
- Listed company audit cases (上市公司审计案例)
- SOE audit cases (央企审计案例)
- Government audit reports (政府审计报告)
- Regulatory enforcement cases (监管处罚案例)

**Case Elements:**
- Company background (industry, size, business model)
- Audit scope and objectives
- Audit process and procedures
- Key findings and issues
- Audit opinions and recommendations
- Lessons and insights

### Professional Resources

**Books and Journals:**
- Academic textbooks (审计学教材)
- Professional monographs (审计专著)
- Academic journals (审计研究, 会计研究)
- Industry reports (审计行业报告, 白皮书)

**Online Resources:**
- Professional websites (CICPA, IIA China)
- Training materials (继续教育, 培训课件)
- Best practices (实务指南, 操作手册)

### Zotero Integration (Reference Management)

Access local Zotero database:
```bash
# List collections
curl -s "http://localhost:23119/api/users/[USER_ID]/collections"

# Get items from collection
curl -s "http://localhost:23119/api/users/[USER_ID]/collections/[KEY]/items"
```

Extract: title, publication info, standard number, issuing body, effective date

### Source Selection Guide

| Source | Best For | Strengths |
|--------|----------|-----------|
| **Audit Standards** | Authoritative requirements | Legal force, mandatory compliance |
| **Regulatory Documents** | Compliance requirements | Current regulations, enforcement trends |
| **Practical Cases** | Real-world application | Representative, practical insights |
| **Professional Books** | Systematic knowledge | Comprehensive, theoretical foundation |
| **Academic Papers** | Research findings | Theoretical analysis, empirical studies |

## Standard Book Structure

```markdown
# [Book Title]: Theory, Practice, and Cases

## Preface
- Background and motivation
- Target readers
- Content framework
- Usage guide

## Part 1: Theoretical Foundation

### Chapter 1: Audit Overview
#### 1.1 Definition and Classification
#### 1.2 History and Development
#### 1.3 Functions and Roles
**Table 1. Audit Type Comparison**

### Chapter 2: Audit Theoretical Foundation
#### 2.1 Audit Assumptions and Principles
#### 2.2 Audit Risk Model
#### 2.3 Materiality and Audit Evidence
**Table 2. Theory Development Timeline**

## Part 2: Practical Operations

### Chapter 3: Audit Planning and Preparation
#### 3.1 Engagement Letter
#### 3.2 Risk Assessment and Planning
#### 3.3 Team Organization
**Table 3. Audit Plan Template**

### Chapter 4: Audit Procedures
#### 4.1 Tests of Controls
##### 4.1.1 Test Methods
##### 4.1.2 Test Procedures
##### 4.1.3 Result Evaluation
**Table 4. Control Test Procedures**

#### 4.2 Substantive Procedures
##### 4.2.1 Tests of Details
##### 4.2.3 Analytical Procedures
##### 4.2.3 Sampling Techniques
**Table 5. Substantive Procedures Comparison**

## Part 3: Typical Cases

### Chapter 5: Financial Audit Cases
#### 5.1 Case Background
#### 5.2 Audit Process
##### 5.2.1 Planning
##### 5.2.2 Execution
##### 5.2.3 Findings
#### 5.3 Case Insights
**Case Study 5-1: [Company Name] Financial Statement Audit**

### Chapter 6: Internal Control Audit Cases
#### 6.1 Case Background
#### 6.2 Evaluation Process
##### 6.2.1 Control System Mapping
##### 6.2.2 Deficiency Identification
##### 6.2.3 Audit Report
#### 6.3 Case Insights
**Case Study 6-1: [Company Name] Internal Control Audit**

## Part 4: Regulatory Interpretation

### Chapter 7: Audit Standards Interpretation
#### 7.1 Chinese Audit Standards Framework
#### 7.2 International Standards Comparison
#### 7.3 Practical Application
**Table 7. Standards Cross-Reference**

### Chapter 8: Related Laws and Regulations
#### 8.1 Accounting Law and CPA Law
#### 8.2 Securities Law and Disclosure
#### 8.3 Regulatory Requirements and Enforcement Cases
**Table 8. Regulation Citation Index**

## Part 5: Emerging Topics

### Chapter 9: Digital Audit
#### 9.1 Big Data in Audit
#### 9.2 Continuous Audit
#### 9.3 AI-Assisted Audit
**Table 9. Digital Audit Tools Comparison**

### Chapter 10: Audit Development Trends
#### 10.1 Theoretical Innovation
#### 10.2 Technology Development
#### 10.3 Professional Development

## Appendices
### Appendix A: Audit Working Paper Templates
### Appendix B: Audit Report Reference Format
### Appendix C: Regulation Catalog
### Appendix D: Glossary (Chinese-English)

## References
- Audit Standards
- Professional Books
- Academic Papers
- Practical Cases
```

## Chapter Writing Templates

### Theory Chapter Template

```markdown
### Chapter X: [Topic]

#### X.1 [Section Title]

**Definition and Concept:**
[Professional definition with authoritative source citation]

**Theoretical Framework:**
- [Component 1]: [description]
- [Component 2]: [description]

**Development History:**
- [Period 1] ([year-range]): [characteristics]
- [Period 2] ([year-range]): [characteristics]

**Key Principles:**
1. **[Principle 1]:** [explanation with citation]
2. **[Principle 2]:** [explanation with citation]

**Current Challenges:**
Despite established frameworks, [topic] faces:
(1) [challenge 1]; (2) [challenge 2]

**Future Directions:**
[discuss emerging trends and developments]
```

### Practice Chapter Template

```markdown
### Chapter X: [Audit Process/Area]

#### X.1 [Process Stage]

**Objective:**
[clear statement of what this stage achieves]

**Prerequisites:**
- [requirement 1]
- [requirement 2]

**Procedures:**
**Step 1: [Procedure Name]**
- Purpose: [what it achieves]
- Actions: [specific steps]
- Output: [deliverable]
- Timing: [when to perform]

**Step 2: [Procedure Name]**
- Purpose: [what it achieves]
- Actions: [specific steps]
- Output: [deliverable]
- Timing: [when to perform]

**Common Issues and Solutions:**
| Issue | Cause | Solution |
|-------|-------|----------|
| [issue 1] | [cause] | [solution] |
| [issue 2] | [cause] | [solution] |

**Quality Control Points:**
- ✓ [control point 1]
- ✓ [control point 2]
```

### Case Chapter Template

```markdown
### Chapter X: [Case Type] Cases

#### Case Study X-1: [Descriptive Case Title]

**Background:**
- **Company:** [company name, industry, size]
- **Audit Period:** [year/period]
- **Audit Type:** [financial audit/internal control/compliance audit/etc.]
- **Audit Firm:** [firm name, if applicable]
- **Key Characteristics:** [what makes this case notable]

**Audit Objectives:**
1. [objective 1]
2. [objective 2]
3. [objective 3]

**Audit Process:**

**Planning Phase:**
- Risk assessment: [key risks identified]
- Audit strategy: [overall approach]
- Resource allocation: [team composition]

**Execution Phase:**
- Tests performed:
  - [test 1]: [purpose and findings]
  - [test 2]: [purpose and findings]
  - [test 3]: [purpose and findings]
- Data analysis:
  - [analysis 1]: [method and conclusion]
  - [analysis 2]: [method and conclusion]

**Key Findings:**
1. **[Finding 1]:**
   - Description: [what was found]
   - Impact: [materiality/significance]
   - Root cause: [underlying reason]
   - Evidence: [supporting documentation]

2. **[Finding 2]:**
   - Description: [what was found]
   - Impact: [materiality/significance]
   - Root cause: [underlying reason]
   - Evidence: [supporting documentation]

**Audit Recommendations:**
1. [recommendation 1]: [specific action + responsible party + timeline]
2. [recommendation 2]: [specific action + responsible party + timeline]

**Case Insights:**
- **What worked well:** [successful practices]
- **Key challenges:** [difficulties faced and how addressed]
- **Lessons learned:** [takeaways for similar audits]
- **Applicability:** [when to apply this approach]

**Related Regulations:**
- [citation 1]: [relevant standard clause]
- [citation 2]: [relevant regulatory requirement]
```

### Regulatory Interpretation Chapter Template

```markdown
### Chapter X: [Standard/Regulation Topic]

#### X.1 [Standard/Regulation] Overview

**Background and Purpose:**
[Why this standard/regulation was issued]

**Effective Date and Status:**
- Issued: [date]
- Effective: [date]
- Latest Revision: [date]
- Status: [current/amended/replaced]

**Applicability:**
- Scope: [who/what it applies to]
- Exemptions: [if any]
- Transition provisions: [if applicable]

#### X.2 Key Requirements

**[Requirement Category 1]:**
- **Requirement:** [specific requirement text]
- **Compliance steps:** [how to comply]
- **Common issues:** [typical challenges]
- **Practical application:** [real-world examples]

**[Requirement Category 2]:**
- **Requirement:** [specific requirement text]
- **Compliance steps:** [how to comply]
- **Common issues:** [typical challenges]
- **Practical application:** [real-world examples]

#### X.3 Comparison with Related Standards

**Table X.1: Standards Comparison**

| Aspect | [Standard 1] | [Standard 2] | [Standard 3] |
|--------|--------------|--------------|--------------|
| [dimension 1] | [difference] | [difference] | [difference] |
| [dimension 2] | [difference] | [difference] | [difference] |

#### X.4 Practical Application

**Case Example:**
[describe how the standard is applied in practice]

**Compliance Checklist:**
- ✓ [compliance item 1]
- ✓ [compliance item 2]
- ✓ [compliance item 3]

**Common Violations:**
| Violation Type | Description | Penalty | Prevention |
|----------------|-------------|---------|------------|
| [violation 1] | [what it is] | [consequence] | [how to prevent] |
| [violation 2] | [what it is] | [consequence] | [how to prevent] |
```

## Citation Patterns

```markdown
# Standard citation
"According to CAS No. 1101 [Year], audit working papers should..."

# Regulation citation
"Under Article X of the Audit Law of the PRC [year]..."

# Case citation
"In XX Company's 20XX financial statement audit case [reference]..."

# Multiple citation
"Several studies have demonstrated... [ref1, ref2, ref3]"

# Comparative citation
"While CAS requires..., ISA standards emphasize..."

# Sequential citation
"First, [process step 1] (Standard X, Clause Y)...
Then, [process step 2] (Standard Z, Clause W)..."
```

## 4-Round Review Process

### Round 1: Content Accuracy Review
- ✓ **Regulatory accuracy:** Standard numbers, clause numbers, effective dates, scope of application
- ✓ **Case accuracy:** Company names, dates, amounts, events, findings
- ✓ **Terminology accuracy:** Audit terms, accounting terms, legal terms

### Round 2: Logical Coherence Review
- ✓ **Chapter logic:** Smooth transitions, clear hierarchy
- ✓ **Argumentation:** Complete logical chain (premise → reasoning → conclusion)
- ✓ **Consistency:** Unified terminology, consistent data, aligned references

### Round 3: Practical Applicability Review
- ✓ **Procedural feasibility:** Complete steps, actionable procedures
- ✓ **Case representativeness:** Typical cases, current relevance
- ✓ **Recommendation value:** Actionable suggestions, practical insights

### Round 4: Format Standardization Review
- ✓ **Citation format:** Standard references, case citations, literature citations
- ✓ **Table consistency:** Unified titles, column names, formatting
- ✓ **Heading hierarchy:** Standard chapter numbering, clear levels

## Quality Checklist

Before completion, verify:
- [ ] Structure overview with clear table of contents
- [ ] Comparison table for each major section
- [ ] Case studies with all required elements
- [ ] Accurate regulatory citations (standard number, clause, scope)
- [ ] Practical guidance with actionable steps
- [ ] Consistent terminology throughout
- [ ] All claims cited and supported
- [ ] References organized by type
- [ ] Completed 4-round review process
- [ ] Figure and table placeholders with captions

## File References

- [WORKFLOW.md](WORKFLOW.md) - Detailed 7-phase workflow with 4-round review
- [TEMPLATES.md](TEMPLATES.md) - CLAUDE.md and IMPLEMENTATION_PLAN.md templates
- [DOMAINS.md](DOMAINS.md) - Domain-specific audit areas and categories
- [DATA_VERIFICATION.md](DATA_VERIFICATION.md) - **⚠️ CRITICAL: 数据验证规范，防止编造数据和引用材料**
