# 批注正文模板（v2.0.0）

v2 批注生成路径有 3 条：

- **docx 输入** → `tools/inject-docx-comments.py`（Word comments，v1 路径保留）
- **pdf 输入** → `tools/annotate-pdf.py`（嵌入式 pdf 批注，v2 主路径）
- **pdf 输入 + 用户明确要 XFDF** → `tools/generate-xfdf.py`（v1 备用）

三条路径**共用**本模板的批注正文格式，确保视觉与文本一致。

---

## § 1 模板定义

```
【{category_cn}】【{severity_cn}】{problem}
→ {suggestion[0]}
[id: {issue_id}]
```

### § 1.1 占位符

| 占位符 | 来源 | 长度约束 |
|---|---|---|
| `{category_cn}` | issue.category → 中文映射 | — |
| `{severity_cn}` | issue.severity → 中文映射 | — |
| `{problem}` | issue.problem | ≤ 200 码点 |
| `{suggestion[0]}` | issue.suggestion[0] | ≤ 500 码点 |
| `{issue_id}` | issue.id | ≤ 80 字符 |

### § 1.2 多条 suggestion 扩展

若 `len(issue.suggestion) > 1`，模板变为：

```
【{category_cn}】【{severity_cn}】{problem}
→ {suggestion[0]}
其他建议：
  · {suggestion[1]}
  · {suggestion[2]}
  ...
[id: {issue_id}]
```

### § 1.3 定位失败前缀（v2 约定）

当批注无法精确定位到原文（策略 5 "top-left-note" 兜底）时，批注正文顶部加前缀：

```
⚠️ 定位回退至章节首段/页首：
【{category_cn}】【{severity_cn}】{problem}
→ {suggestion[0]}
[id: {issue_id}]
```

---

## § 2 category → 中文映射

| category | 中文 |
|---|---|
| `structure` | 结构 |
| `argumentation` | 论证深度 |
| `literature-review` | 文献综述 |
| `empirical` | 实证 |
| `legal-norms` | 规范适用 |
| `language` | 语言 |
| `policy` | 对策 |
| `academic-integrity` | 学术不端线索 |
| `citation-format` | 引注格式 |
| `citation-missing-info` | 引注信息 |

## § 3 severity → 中文映射

| severity | 中文 |
|---|---|
| `fatal` | 致命 |
| `major` | 重要 |
| `minor` | 轻微 |

---

## § 4 长度与换行处理

- 单条批注正文建议 ≤ 400 字符，超过时考虑拆分 issue
- 换行：
  - pdf 批注（PyMuPDF）：直接用 `\n`
  - docx 批注：用 `<w:br/>` 元素
  - XFDF `<contents>`：用 `\n`

## § 5 示例（5 条，覆盖 fatal/major/minor + thesis-*/citation-*）

### 5.1 thesis-structure，致命

```
【结构】【致命】绪论缺失研究综述，仅有立法综述
→ 补写独立的研究综述章节
[id: thesis-structure-001]
```

### 5.2 thesis-argumentation，重要

```
【论证深度】【重要】本节仅罗列学说未作比较分析
→ 增补"三种学说的分歧与取舍"小节
其他建议：
  · 补一句明确本文立场
  · 参考陈景辉 2022 年《法律移植中的本土性检验》的反思框架
[id: thesis-argumentation-005]
```

### 5.3 citation-citation-format，轻微

```
【引注格式】【轻微】GB/T 7714 期号不应前导 0: (02) → (2)
→ 把脚注 [12] 以及同刊其他脚注的期号 (02) 统一改为 (2)
[id: citation-citation-format-042]
```

### 5.4 citation-citation-missing-info，重要

```
【引注信息】【重要】脚注 [17] 缺页码
→ 补全 "第 XX 页"
[id: citation-citation-missing-info-017]
```

### 5.5 thesis-academic-integrity，致命（含证据链闭环要求）

```
【学术不端线索】【致命】参考文献 [38] 所示期刊论文经联网核实不存在
→ 删除或重新查证
其他建议：
  · 在 CNKI / 万方 / 百度学术三平台交叉核实
  · 若确无原文，改为"一般学术观点"的泛指叙述
[id: thesis-academic-integrity-003]
```

---

## § 6 对脚本的契约

- `tools/annotate-pdf.py`：`render_annotation_body(issue)` 函数按本模板生成字符串
- `tools/inject-docx-comments.py`：同一函数，换行用 `<w:br/>`
- `tools/generate-xfdf.py`：同一函数，换行用 `\n`

**三脚本各自保留一份渲染函数**（不抽共享模块，保持独立可执行）。每次模板变更需**同步三处**。
