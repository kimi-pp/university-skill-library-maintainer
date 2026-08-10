# XFDF 批注导入指引

**本段内容由 README.md 与 Unified_Report 附录共同 include，是同源内容；如需修改，只改这一份。**

当 `unified-thesis-reviewer` 处理 pdf 输入时，会在原 pdf 旁生成同名的 `.xfdf` 文件（例如 `我的论文.pdf` → `我的论文.xfdf`）。XFDF 是旁路文件，不修改原 pdf，需要在支持 XFDF 的 PDF 阅读器中手动导入才能看到批注。

---

## 支持的阅读器

| 软件 | 版本要求 | 操作系统 | 是否推荐 |
|---|---|---|---|
| **Adobe Acrobat Reader DC** | 2020 以上 | Windows / macOS | ✅ 推荐（免费） |
| **Adobe Acrobat Pro** | 任意版本 | Windows / macOS | ✅ 推荐 |
| **Foxit PhantomPDF** | 9.0 以上 | Windows / macOS | ✅ 推荐 |
| **Foxit PDF Reader** | 9.0 以上 | Windows / macOS | ✅ 推荐（免费） |

---

## 不支持的阅读器

以下阅读器**不支持**导入 XFDF，有此需求的用户请改用上方推荐阅读器：

- **macOS 自带 Preview**（预览.app）
- **浏览器内置 PDF 查看器**（Chrome / Edge / Safari / Firefox 内嵌的 PDF 查看）
- **WPS PDF**（部分版本支持不完整，不建议）
- **Sumatra PDF** / **Okular** / 等轻量阅读器

---

## 导入步骤

将原 `.pdf` 与生成的 `.xfdf` 放在同一目录（脚本默认已如此）。在阅读器中打开 pdf 后按以下路径导入 xfdf：

### Adobe Acrobat Reader DC（推荐）

1. 打开原 pdf
2. 菜单：**Tools → Comments → Options**（齿轮图标）**→ Import Data File**
3. 在文件选择对话框中选择同目录下的 `{原名}.xfdf`
4. 批注会自动加载并叠加在 pdf 上，右侧出现批注面板

如果菜单文案是中文版：**工具 → 注释 → 选项（齿轮）→ 导入数据文件**。

### Adobe Acrobat Pro

1. 打开原 pdf
2. 菜单：**Edit → Import Comments**（或 **Comments → Import Comments**）
3. 选择同目录下的 `{原名}.xfdf`
4. 批注加载完毕

中文版：**编辑 → 导入注释**。

### Foxit PhantomPDF / Foxit PDF Reader

1. 打开原 pdf
2. 菜单：**Comment → Import**
3. 选择同目录下的 `{原名}.xfdf`
4. 批注加载完毕

中文版：**注释 → 导入**。

---

## 批注的使用

导入后，每条批注在 pdf 上以以下形式呈现：

- **高亮（highlight）**：有精确坐标的批注，对应区域会被高亮标记（红/橙/黄）；点击弹出批注正文
- **便签（text）**：精确坐标缺失时退化为左上角的浮动图标；点击展开批注正文

**批注颜色含义**：

- 🔴 红色 `#E74C3C` —— 致命（fatal）：不修复可能影响答辩通过
- 🟠 橙色 `#F39C12` —— 重要（major）：需要修改
- 🟡 黄色 `#F1C40F` —— 轻微（minor）：建议优化

**批注作者**：统一显示为 `unified-thesis-reviewer`，缩写 `UTR`。

---

## 批注面板与交叉对照

在阅读器的右侧批注面板中，可以：

- 按 **作者** / **页** / **日期** 排序
- 按 **颜色** 过滤（只看 fatal 或 major）
- **双击** 某条批注跳转到 pdf 中对应位置

每条批注正文的末尾含 `[id: {issue_id}]` 标识，与 Unified_Report.md 中的 issue id 一一对应，便于在 MD 报告和 pdf 之间交叉查找。

---

## 常见问题

### Q1：为什么 macOS Preview 不能用？

Preview 不支持 Adobe XFDF 格式的导入。只能改用 Adobe Reader（免费下载）或 Foxit PDF Reader。

### Q2：导入后批注位置不准？

XFDF 批注的坐标由 Agent 在分析阶段依据 pdf 文本位置预填。若原 pdf 是扫描件或文本层不规则，批注可能落在接近但不精确的位置。每条批注正文首行含 `{category_cn}` 和 `{problem}`，可通过 pdf 内文本搜索辅助核对。

### Q3：批注显示为小便签而非区域高亮？

这是**正常退化行为**：当 issue 没有精确 bbox 时，批注退化为页面左上角的浮动便签（yellow note 图标）。点击图标展开后与高亮批注的正文一致。

### Q4：如何保存批注到 pdf 本身？

Adobe Reader / Foxit 导入 XFDF 后，可选择 **Save As / 另存为**，把批注合并入 pdf 保存。保存后的 pdf 在任何阅读器（包括 Preview、浏览器）都能看到批注。

### Q5：想离线重新生成 XFDF？

XFDF 由 `tools/generate-xfdf.py` 生成，支持命令行独立运行：

```bash
python3 tools/generate-xfdf.py 原.pdf issues.json 输出.xfdf
```

参数：原 pdf 路径、issues.json 路径、输出 xfdf 路径。仅使用 Python 3.8+ 标准库，无需安装任何第三方包。

---

## 安全与隐私

- XFDF 文件**不包含**原 pdf 的任何字节；只包含批注文本、坐标、元数据
- 分享 XFDF 时请同时分享原 pdf，两者需放在同目录
- 批注作者统一为 `unified-thesis-reviewer`，不会泄露用户真实身份
