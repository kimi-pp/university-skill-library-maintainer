# XFDF 旁路文件：PDF 批注生成的结构契约与算法

本规则文件把 `unified-thesis-reviewer` v3 阶段的 pdf 批注旁路文件生成规范沉淀为 agent 可读的规则。脚本实现在 `tools/generate-xfdf.py`，输入为 `issues.json` + 原 pdf，输出为 `{原名}.xfdf`（与原 pdf 同目录存放）。

**XFDF 全称**：Adobe XML Forms Data Format。它是 PDF 批注的旁路格式——**不修改原 pdf**，Adobe Reader / Acrobat / Foxit 打开原 pdf 时手动导入 `.xfdf` 文件后，批注会叠加显示。

核心原则：**只写 XFDF，不改原 pdf**；**纯 stdlib，零第三方依赖**；**坐标由 Agent 预先填入，脚本不自提**。

---

## §1 职责边界

### §1.1 本脚本做什么

- 消费 `issues.json` 中已经填好 `locator.page_number` + `locator.bbox` 的 issue
- 按 XFDF 2.0 规范组装 `.xfdf` 文件
- 对坐标缺失的 issue 走退化链路（参见 §8），不丢问题
- 生成后回读自校验

### §1.2 本脚本**不**做什么

- **不**从 pdf 中提取文字或坐标（bbox 由 Agent 在分析阶段通过宿主平台的 pdf 能力预填）
- **不**修改原 pdf 字节
- **不**引入 `pdfplumber` / `pypdf` 等第三方库
- **不**渲染 pdf 预览

---

## §2 最小完整示例

一份合法的 XFDF（含 `<highlight>` 和 `<text>` 各一条）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xfdf xmlns="http://ns.adobe.com/xfdf/">
  <f href="thesis.pdf"/>
  <annots>
    <highlight page="2"
               name="thesis-argumentation-007"
               title="unified-thesis-reviewer"
               date="2026-05-12T14:30:00+08:00"
               creationdate="2026-05-12T14:30:00+08:00"
               color="#E74C3C"
               coords="72.0,720.0,252.0,720.0,72.0,708.0,252.0,708.0">
      <contents>【论证深度】【重要】论证跳跃:前一段断言"X 导致 Y"但未给出依据。 → 补充至少一条权威文献或一条可证伪的经验证据。
[id: thesis-argumentation-007]</contents>
    </highlight>
    <text page="5"
          name="citation-citation-format-042"
          title="unified-thesis-reviewer"
          date="2026-05-12T14:30:15+08:00"
          creationdate="2026-05-12T14:30:15+08:00"
          color="#F39C12"
          rect="0,822,20,842">
      <contents>【引注格式】【重要】脚注 38 缺页码。 → 请补充"第 XX 页"。
[id: citation-citation-format-042]</contents>
    </text>
  </annots>
</xfdf>
```

---

## §3 根结构

### §3.1 三级结构

```
<xfdf xmlns="http://ns.adobe.com/xfdf/">
  <f href="{pdf_basename}"/>
  <annots>
    <highlight .../>  <!-- 或 <text .../> -->
    ...
  </annots>
</xfdf>
```

| 元素 | 必填 | 说明 |
|---|---|---|
| `<xfdf>` | ✅ | 根元素；必须声明 XFDF 命名空间 `http://ns.adobe.com/xfdf/` |
| `<f>` | ✅ | 指向原 pdf 的相对路径引用；`href` 为**纯文件名**（无目录前缀、无 `./`） |
| `<annots>` | ✅ | 批注容器；即使无批注也必须存在 |
| `<highlight>` / `<text>` | 0..n | 具体批注元素，见 §4 / §5 |

### §3.2 XML 声明头

文件首行**必须**是 XML 声明：

```
<?xml version="1.0" encoding="UTF-8"?>
```

**编码约定**：UTF-8 **不带 BOM**。若写盘时带了 BOM，Adobe Reader 可能拒绝加载（R7A 要求）。

---

## §4 `<highlight>` 元素（有 bbox 时首选）

### §4.1 完整属性表

| 属性 | 来源 | 说明 |
|---|---|---|
| `page` | `locator.page_number - 1` | **0-based** 非负整数 |
| `name` | `issue.id` | 全清单唯一，用于批注标识 |
| `title` | 固定 `"unified-thesis-reviewer"` | 作者名 |
| `date` | 当前 ISO 8601 | 形如 `"2026-05-12T14:30:00+08:00"` |
| `creationdate` | 与 `date` 同值双写 | Foxit 兼容需要 |
| `color` | severity 映射 | 见 §7 |
| `coords` | `locator.bbox` 转换 | 每 8 浮点数 1 行 |

### §4.2 `coords` 属性

格式：`"x1,y1,x2,y2,x3,y3,x4,y4"`（8 个浮点数，英文逗号分隔，不带空格）

每 8 个数字代表一行高亮的**四个顶点**，顺序固定为：**左上、右上、左下、右下**。多行高亮时追加到同一 `coords` 字符串（总长度必为 8 的倍数）。

### §4.3 `<contents>` 子元素

包含批注正文。模板与 Word 批注共用 `templates/annotation-body-template.md`，格式：

```
【{category_cn}】【{severity_cn}】{problem} → {suggestion[0]}
（多条 suggestion 续行）
[id: {issue_id}]
```

**换行处理**：XFDF 的 `<contents>` 是普通 XML 文本节点，直接用字符 `\n`（与 Word 批注的 `<w:br/>` 不同）。

---

## §5 `<text>` 元素（无 bbox 时退化用）

### §5.1 职责

当 issue 有 `page_number` 但无 `bbox` 时，用 `<text>` 浮动便签挂在页面左上角 20×20 points 区域，不丢问题。

### §5.2 属性表

与 `<highlight>` 共享 `page / name / title / date / creationdate / color`，**不同**点：

| 属性 | 值 | 说明 |
|---|---|---|
| `rect` | `"x0,y0,x1,y1"` | 4 浮点数；页面左上 20×20 points 区域 |
| ~~`coords`~~ | 不用 | text 不需要 |

### §5.3 rect 计算

PDF 坐标系原点在左下角、y 轴向上；页面左上角 20×20 points 即：

```
rect = "0,{H-20},20,{H}"   # H 是页面高度（points）
```

例：A4 页面高度 792 points，`rect="0,772,20,792"`。

---

## §6 坐标系

**一句话**：PDF 用户空间 points，原点左下角，y 轴向上，单位 1/72 英寸。

常见页面尺寸（points）：

| 页面 | 宽 | 高 |
|---|---|---|
| A4 | 595.28 | 841.89 |
| US Letter | 612 | 792 |
| B5 | 498.90 | 708.66 |

Agent 在分析 pdf 时通过平台能力读取 `MediaBox` 获得实际页面尺寸；脚本也**独立解析**原 pdf 的 `MediaBox` 用于退化与 clip 计算（参见 §8 和 §9）。

### §6.1 bbox 与 coords 的转换

`bbox = [x0, y0, x1, y1]`，约定 `y0 < y1`（左下 + 右上两点）。转换为 coords 4 顶点：

```python
def bbox_to_coords(x0, y0, x1, y1):
    return [
        x0, y1,  # 左上
        x1, y1,  # 右上
        x0, y0,  # 左下
        x1, y0,  # 右下
    ]
```

示例：`bbox = [72, 708, 252, 720]` → `coords = "72,720,252,720,72,708,252,708"`。

---

## §7 颜色映射

按 issue.severity 映射固定颜色：

| severity | color hex | 视觉 |
|---|---|---|
| `fatal` | `#E74C3C` | 红色系（警戒） |
| `major` | `#F39C12` | 橙色系（重要） |
| `minor` | `#F1C40F` | 黄色系（提示） |

硬编码在脚本的 `severity_to_color()` 函数中；不由用户配置。

---

## §8 退化矩阵

| `page_number` 字段 | `bbox` 字段 | 生成元素 | 备注 |
|---|---|---|---|
| 有 | 有 | `<highlight>` | coords 按 §6.1 转 4 顶点 |
| 有 | 无 | `<text>` | rect 为该页左上 20×20 points |
| 无 | 任意 | **跳过 annotation** | 日志写 `skipped: <id> reason=no-page-number`；不中断其余 issue |

`page_number` 在 pdf 输入下按 R5.10 是**必填**，但 Agent 在异常情况下可能遗漏——此时脚本宽容处理（skip 而非 raise）。

---

## §9 bbox 越界保护

若 `bbox` 的任一顶点超出页面尺寸（`MediaBox` 给出的宽高），把越界顶点 clip 到页面边界内；**不触发 skip**，仍生成 `<highlight>`。

```python
def clip_bbox(bbox, page_w, page_h):
    x0, y0, x1, y1 = bbox
    return [
        max(0.0, min(x0, page_w)),
        max(0.0, min(y0, page_h)),
        max(0.0, min(x1, page_w)),
        max(0.0, min(y1, page_h)),
    ]
```

clip 发生时在日志写一条 `clipped: <id> reason=bbox-out-of-bounds`。

### §9.1 原 pdf 页面尺寸的读取

脚本需独立解析原 pdf 的 `/MediaBox` 以获得各页尺寸。方法：

- 用正则扫描 pdf 字节内容的 `/MediaBox [ x0 y0 x1 y1 ]`
- 按页顺序收集，返回 `{page_index: (w, h)}`
- 解析失败（加密 pdf / 损坏）时回退为默认 A4 尺寸，仍继续生成 XFDF，在日志记录一条 `fallback-page-size-default`

参见 `generate-xfdf.py` 的 `load_pdf_page_sizes()` 实现。

---

## §10 跨页 issue 单条生成

一条 issue 的 `locator` 只取**首个** `page_number` + `bbox` 生成**唯一一条** annotation。即便 Agent 未来扩展数据结构允许多页，脚本也只取第一个；原因：

- `name=issue.id` 必须在 XFDF 文件内**唯一**（Adobe Reader 不允许重复 name，否则拒绝加载）
- 跨页高亮在 XFDF 规范下需要用多条 annotation 实现，但这会让 `name` 冲突；宁可单条不拆分

跨页 issue 的现象在 agent 分析阶段罕见（单句跨页的极少数情形），本脚本不做特殊优化。

---

## §11 Foxit 兼容约定

以下约定确保生成的 XFDF 在 Foxit PhantomPDF / Foxit PDF Reader 导入时零警告：

1. `date` 与 `creationdate` **双写**同值（Foxit 对 `creationdate` 缺失敏感）
2. **不**使用 `subject` 属性（Foxit 某些版本解析 buggy，可能导致批注正文串到标题栏）
3. 颜色用 `#RRGGBB` 十六进制字符串（不支持 `rgba()` 或纯浮点 0-1 的表达）
4. `name` 属性必须唯一，否则 Foxit 只显示第一条同名批注
5. `<contents>` 元素只存纯文本，不嵌入 HTML / Markdown 标记

---

## §12 回读自校验

脚本生成 XFDF 后必须重新 `ET.parse` 并校验两条不变式：

1. **可解析**：`ET.parse(xfdf_path)` 不抛异常
2. **数量匹配**：`<annots>` 下 `<highlight>` + `<text>` 元素总数 == 输入的（剔除 skip 后的）issue 数

```python
def readback_verify_xfdf(xfdf_path, expected_count):
    tree = ET.parse(xfdf_path)
    root = tree.getroot()
    annots = root.find(".//{http://ns.adobe.com/xfdf/}annots")
    if annots is None:
        return (False, ["missing <annots>"])
    actual = len([e for e in annots if e.tag.endswith("highlight") or e.tag.endswith("text")])
    if actual != expected_count:
        return (False, [f"annotation count mismatch: expected {expected_count}, got {actual}"])
    return (True, [])
```

失败时删除 XFDF 副本并向上报错（保留 MD + issues.json 作为兜底交付）。

---

## §13 跨阅读器兼容

### §13.1 支持的阅读器

- **Adobe Acrobat Reader DC**（推荐）
- **Adobe Acrobat Pro**
- **Foxit PhantomPDF**
- **Foxit PDF Reader**

### §13.2 不支持的阅读器

- **macOS 自带 Preview**（不支持 XFDF 导入）
- **浏览器内置 PDF 查看器**（Chrome / Edge / Safari 内嵌查看器）
- **WPS PDF**（部分版本支持不完全，建议用 Adobe / Foxit）

### §13.3 导入操作指引

导入步骤文档由 `templates/readme-section-import-xfdf.md` 统一维护，由 README.md 与 Unified_Report 附录都 `include` 引用。不要在本文件重复。

---

## §14 对脚本的契约

本规则文件对 `tools/generate-xfdf.py`（T3.3–T3.10 阶段实现）提出硬性契约：

| 契约 | 落实位置 |
|---|---|
| 仅依赖 stdlib（`xml.etree.ElementTree` / `re` / `json` / `sys` / `os` / `datetime` / `pathlib` / `argparse` / `hashlib`） | `import` 段 |
| CLI: `python3 generate-xfdf.py <原.pdf> <issues.json> <输出.xfdf>` | `argparse` |
| 根结构按 §3.1 | `build_xfdf_root` |
| `<f href>` 为纯文件名 | §3.1 |
| `<highlight>` 按 §4，`<text>` 按 §5 | `build_highlight` / `build_text` |
| 坐标系 PDF 用户空间 points，原点左下、y 向上 | §6 |
| bbox→coords 四顶点顺序固定为左上/右上/左下/右下 | `bbox_to_coords` |
| severity→color 按 §7 | `severity_to_color` |
| 退化链路按 §8 | `dispatch_annotation` |
| bbox 越界 clip，不 skip | `clip_bbox` |
| 跨页 issue 只取首个 page+bbox | §10 |
| Foxit 兼容 5 点（date/creationdate 双写、禁用 subject、hex 颜色、name 唯一、contents 纯文本） | §11 |
| 回读两不变式通过才保留副本 | `readback_verify_xfdf` |

相关规则：

- `rules/docx-annotation.md` —— v2 批注注入（与本文件并行，覆盖 docx 输入）
- `rules/issues-schema.md` —— issues.json 数据契约
- `rules/error-handling.md` —— 生成失败的错误路径
- `templates/readme-section-import-xfdf.md` —— 导入操作指引（同源引用）
- `templates/annotation-body-template.md` —— 批注正文模板（v2/v3 共用）
