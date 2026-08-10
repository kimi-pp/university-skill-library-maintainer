# PDF 批注生成（v2.0.0 新主路径）

本规则文件替代 v1 的 `rules/xfdf-annotation.md`，把 pdf 批注主路径从 XFDF 旁路文件切换到**嵌入式批注 pdf**。

## 索引

- §1 背景：v1 XFDF 方案的痛点
- §2 v2 新主路径：嵌入式批注 pdf
- §3 定位策略（5 级）
- §4 批注元素类型
- §5 与 XFDF 的关系
- §6 对脚本的契约

---

## §1 背景：v1 XFDF 方案的痛点

v1 的 `tools/generate-xfdf.py` 生成 Adobe XFDF 2.0 规范的旁路文件，理论上任何 Adobe Reader / Foxit 都能导入。但实战暴露：

1. **WPS PDF / Chrome 内嵌查看器 / 浏览器 / macOS Preview 都不支持 XFDF 导入**——国内用户最常用的 pdf 阅读器其实是 WPS
2. 即便 Adobe Reader 支持，用户要找 "Tools → Comments → Options → Import Data File" 菜单，**操作成本高**
3. XFDF 和 pdf 分开存放容易丢失，分发时还要提醒"两个文件要一起"

→ **v1.0.0 首次实战中用户反馈"xfdf 我用了 WPS 和 Chrome 都打不开"**，直接暴露了方案问题。

---

## §2 v2 新主路径：嵌入式批注 pdf

`tools/annotate-pdf.py`（v2 新增）**直接把批注写入原 pdf 的副本**，输出 `.annotated.pdf`。

### §2.1 核心优势

- 任何 pdf 阅读器（WPS / Chrome / Preview / Adobe / Foxit / Firefox）**打开即见**，零配置
- 单个 pdf 文件，分发时不再需要同时带旁路文件
- 与 Word 的 .annotated.docx 形成一致的"副本 + 批注"产物模式
- 批注正文、作者、时间戳、颜色等元数据全部在 pdf 内，独立于任何工具

### §2.2 依赖

v2 接受**引入第三方依赖 PyMuPDF**（`pip install --user PyMuPDF`）。这突破了 v1 的"纯 stdlib"约束，但换回了用户体验的根本提升。

**安装与降级**：

- 脚本顶部 `try: import fitz / except ImportError`：PyMuPDF 不可用时给出清晰安装提示
- v1 的 `generate-xfdf.py` 保留为备用路径（纯 stdlib），用户明确要 XFDF 时才调用

---

## §3 定位策略（5 级，按优先级）

`tools/annotate-pdf.py` 的 `resolve_annotation_location(doc, issue)` 按以下优先级决定批注位置：

### §3.1 Level 1：anchor_text 在指定页附近搜

```python
search_near_page(doc, anchor_text, start_page=loc.page_number - 1, radius=3)
```

- 最常用路径
- radius=3 意味着在目标页 ±3 页范围内搜索
- **要求 anchor_text 是 pdf 原文中实际存在的短语**（由 extract-pdf-text.py 或 Agent 抽取确保）

### §3.2 Level 2：anchor_text 全文搜

```python
search_fulltext(doc, anchor_text)
```

- L1 失败时的兜底
- 适用于 page_number 推断不准的场景（前封面 / 罗马数字页码 / 目录干扰）

### §3.3 Level 3：excerpt 全文搜

```python
search_fulltext(doc, excerpt)
```

- 当 anchor_text 为空但 excerpt 非空时（scope=paragraph/sentence/span）
- 对 scope=chapter/document，excerpt 强制为空，此级别不起作用

### §3.4 Level 4：bbox 坐标

```python
convert_bbox_to_pymupdf_rect(loc.bbox, page)
```

- 当 anchor/excerpt 都搜不到但 bbox 有值时
- **坐标系转换**：locator.bbox 约定"左下原点、y 向上"，PyMuPDF 是"左上原点、y 向下"，需翻转

### §3.5 Level 5：章节首段 / 页首便签（兜底）

- 所有上面都失败 → 在 locator.page_number 对应页的左上角放一个 20×20 points 的便签
- 便签上显示完整批注正文
- **不丢问题**：即使视觉效果不如高亮，批注内容仍然存在

---

## §4 批注元素类型

### §4.1 高亮批注（首选）

- 由 L1/L2/L3 文本搜索或 L4 bbox 命中时使用
- PyMuPDF API: `page.add_highlight_annot(rect)`
- **颜色**：按 severity 映射
  - fatal: `#E74C3C` 红
  - major: `#F39C12` 橙
  - minor: `#F1C40F` 黄
- **不透明度**：0.45（既显眼又不遮挡原文）
- **正文**：鼠标悬停显示批注文本

### §4.2 便签批注（兜底）

- 由 L5 兜底时使用
- PyMuPDF API: `page.add_text_annot(point, body, icon="Comment")`
- 左上角小图标，点击展开正文

### §4.3 元数据

所有批注必填：

```python
info = annot.info
info["title"] = "unified-thesis-reviewer"  # 作者
info["content"] = body                      # 批注正文
info["creationDate"] = fitz.get_pdf_now()
annot.set_info(info)
annot.update()
```

---

## §5 与 XFDF 的关系

| 场景 | v2 使用的工具 |
|---|---|
| 默认（99% 场景） | `tools/annotate-pdf.py` → 嵌入式 pdf |
| 用户明确要 XFDF 旁路 | `tools/generate-xfdf.py` → XFDF 文件 |
| docx 输入 | `tools/inject-docx-comments.py` → .annotated.docx |

- `generate-xfdf.py` **保留**在仓库中，文档里不再主推
- 交互节点 D 默认引导用户选 "generate .annotated.pdf"
- 用户说"我要 XFDF 供 Acrobat 导入"时才启用 XFDF 路径

---

## §6 对脚本的契约

### §6.1 `tools/annotate-pdf.py` 输入输出

- 输入：`(原.pdf, issues.json, 输出.annotated.pdf)`
- 输出退出码：
  - 0：成功
  - 2：文件不存在
  - 3：issues.json 自校验失败
  - 4：回读校验失败
  - 5：I/O 错误
  - 10：PyMuPDF 未安装

### §6.2 回读验证

副本生成后 **必须**：

1. PyMuPDF 重新打开 `.annotated.pdf`
2. 统计所有页的批注数
3. 与输入 issues 的数量比较
4. 不一致 → 回读失败（退出码 4）

### §6.3 策略分布日志

脚本结束时必须打印每个 issue 走了哪条策略：

```
[annotate-pdf] mounted N annotations -> output.pdf
  strategy distribution:
    anchor-near:     X
    anchor-fulltext: Y
    excerpt-fulltext: Z
    bbox:            W
    top-left-note:   V
```

**关键健康指标**：`top-left-note` 占比应 ≤ 20%。占比过高表明 issues.json 的 anchor_text 质量不佳，应当返工 Agent 阶段的锚点抽取。

---

## §7 跨平台兼容

嵌入式批注 pdf 的 **阅读器支持矩阵**：

| 阅读器 | 高亮可见 | 便签可见 | 悬停显示正文 | 颜色 |
|---|---|---|---|---|
| Adobe Acrobat Reader DC | ✅ | ✅ | ✅ | ✅ |
| Adobe Acrobat Pro | ✅ | ✅ | ✅ | ✅ |
| Foxit PhantomPDF | ✅ | ✅ | ✅ | ✅ |
| Foxit PDF Reader | ✅ | ✅ | ✅ | ✅ |
| WPS PDF | ✅ | ✅ | ✅ | ✅ |
| macOS Preview | ✅ | ✅ | ✅ | ✅ |
| Chrome 内嵌 PDF | ✅ | ✅ | 部分 | ✅ |
| Edge 内嵌 PDF | ✅ | ✅ | 部分 | ✅ |
| Safari | ✅ | ✅ | ✅ | ✅ |

**所有主流阅读器全部支持**。这是相比 v1 XFDF 方案的决定性优势。

---

## §8 pdf 批注文件的安全与隐私

- 嵌入式 pdf 会把批注正文（含原论文问题描述）写入 pdf
- 若用户选择**匿名化**（interaction-prompts §E），批注正文中的作者 / 单位信息会用占位符代替
- 分发含批注 pdf 时，请注意批注正文可能暴露的审查意见

---

相关规则：

- `rules/orchestration-flow.md` §8：批注生成在主工作流的位置
- `rules/issues-schema.md`：anchor_text 字段规范
- `rules/academic-integrity-guard.md`：批注内容的证据要求
- `templates/annotation-body-template.md`：批注正文统一格式
- `tools/annotate-pdf.py`：实现文件
