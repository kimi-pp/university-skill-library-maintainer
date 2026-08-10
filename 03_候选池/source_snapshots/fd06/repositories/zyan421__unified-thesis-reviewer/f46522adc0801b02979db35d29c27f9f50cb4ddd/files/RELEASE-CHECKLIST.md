# 发布前检查清单（v2.7.0）

## 版本映射

| 阶段 | Semver | 触发条件 |
|---|---|---|
| v2.0.0 | 2.0.0 | 嵌入式 PDF 批注、联网核实、引用交叉对比等 v2 主路径落地 |
| v2.6.0 | 2.6.0 | docx anchor_text 主路径、实质性维度审查、OOXML 样式核查、表格审查落地 |
| **v2.7.0** | **2.7.0** | 严重度标尺、批注挂载位置原则、PDF anchor 空格容错、实战案例库落地 |

## v2.7.0 发布前检查

### 1. 单元测试全绿

```bash
python -m unittest discover -s tests -v
```

期待：全部测试通过。

### 2. 底层 skill bundle 刷新

```bash
python tools/build-bundle.py
```

期待：

- `_bundled/legal-thesis-reviewer.rules/` 与 `_bundled/legal-citation-checker.rules/` 刷新
- `_bundled/manifest.json` 生成，`schema_version` 为 `1.0`
- bundle 不含 GB/T 7714 原文、《法学引注手册》原文、论文样本或评阅书原始材料

### 3. 分发包生成

```bash
python tools/make-dist.py --version 2.7.0 --output-dir .release/unified-thesis-reviewer --dist-dir dist
```

期待：

- `.release/unified-thesis-reviewer/` 重建
- `dist/unified-thesis-reviewer-v2.7.0.zip` 生成
- 分发包不含 `tests/`、`__pycache__/`、`.git/`、`*.pyc`

### 4. 发布包验证

```bash
python tools/bundle-verify.py --path .release/unified-thesis-reviewer
```

期待：版权、目录结构、脚本语法、LICENSE-NOTICE、manifest 全部通过。

### 5. PyMuPDF 可用性验证

```bash
python -c "import fitz; print(fitz.version)"
```

期待：输出版本号。若目标环境未安装，README 已提示安装方式。

### 6. v2.7 PDF anchor 容错 smoke test

```bash
python tools/annotate-pdf.py tests/fixtures/minimal.pdf tests/fixtures/issues_boundary_pdf_bbox.json dist/smoke.annotated.pdf
```

期待：输出 PDF 可生成且可被 PyMuPDF 回读。

### 7. 文档一致性

- `SKILL.md` front matter version 为 `2.7.0`
- `README.md` 标题、安装说明、验证命令均指向 `2.7.0`
- `CHANGELOG.md` 含 `2.7.0`
- `RELEASE_NOTES_v2.7.0.md` 可直接用于 GitHub Release

## 发布动作

```bash
git tag v2.7.0
git push origin main
git push origin v2.7.0
gh release create v2.7.0 dist/unified-thesis-reviewer-v2.7.0.zip --title "unified-thesis-reviewer v2.7.0" --notes-file RELEASE_NOTES_v2.7.0.md
```

## 发布后回归

- 用一个 docx 样本确认 `.annotated.docx` 批注位置合理
- 用一个文本版 PDF 样本确认 `.annotated.pdf` 在 WPS/Chrome 可见
- 检查 GitHub Release 页面说明和 ZIP 下载链接
