# Unified Thesis Reviewer（法学论文统一审查 Skill）v2.7.0

面向法学院师生的论文未定稿检查“一站式”入口。一次提交论文（docx / 文本版 pdf / 纯文本），一次拿回统一审查报告、结构化问题清单和可直接打开的批注文档。

本仓库是一个可直接分发的 Codex/Agent Skill。核心入口是 [`SKILL.md`](./SKILL.md)，规则、模板、命令行辅助工具和底层法学审查规则 bundle 均已随仓库提供。

## 适合什么场景

- 本科、硕士、博士法学论文定稿前自查
- 课程论文、期刊投稿初稿的结构和论证审阅
- 引注格式校对、参考文献与脚注交叉检查
- 需要生成 Word/PDF 批注版审阅稿的场景
- 需要把实质性问题、形式问题、引注问题合并成一份统一报告的场景

## 一次审查会输出什么

- **统一审查报告**：9+1 章节 Markdown，覆盖选题、结构、论证、文献综述、实证、规范适用、语言、对策、学术不端线索和引注格式。
- **结构化问题清单**：`issues.json`，含 severity、evidence、anchor_text、page/bbox 等字段，供后续批注工具使用。
- **嵌入式批注 PDF**：PDF 输入时生成 `{原名}.annotated.pdf`，WPS、Chrome、Adobe、Foxit 等阅读器直接打开可见。
- **Word 批注文档**：docx 输入时生成 `{原名}.annotated.docx`。
- **引用交叉对比表**：由 `tools/citation-crossref.py` 自动生成脚注/参考文献机械对比结果。
- **联网核实记录**：对法律名称、案号、学术文献等高风险事项执行联网核实，失败时降级说明。

## v2.7.0 关键升级

v2.7.0 是在 v2.6 多轮真实论文测试后的修复发布，重点处理 Agent 判断偏差和 PDF anchor 定位问题。

- **严重度判定标尺**：新增 fatal / major / minor 判定规则，并引入“反向举证原则”，避免把可合理解释的问题误判为致命问题。
- **批注挂载位置原则**：全文级问题挂在读者最该看到的位置，比较性问题挂在贡献说明位置，减少“问题发现处”和“读者需要处”错位。
- **PDF anchor 空格容错**：自动尝试中文与数字/字母边界空格变体，例如把“第188条”匹配到 PDF 文本层中的“第 188 条”。
- **PDF 输入 anchor 选取建议**：引导 Agent 优先选择连续中文短句，避开 PDF 文本层常见的数字、英文、符号断裂。
- **实战案例库**：收录 v2 系列真实失误案例，作为未来审查时的反面教材。
- **批注作者统一**：PDF 批注作者同步为“张老师的AGENT”。

完整变更见 [`CHANGELOG.md`](./CHANGELOG.md)。

## 快速安装

### Codex Desktop / Codex CLI

在 `$CODEX_HOME/skills` 下克隆本仓库即可：

```bash
cd ~/.codex/skills
git clone https://github.com/zyan421/unified-thesis-reviewer.git
```

Windows PowerShell 示例：

```powershell
cd $env:USERPROFILE\.codex\skills
git clone https://github.com/zyan421/unified-thesis-reviewer.git
```

重启 Codex 后，Skill 会按 `SKILL.md` front matter 自动被发现。触发时可以直接说：

- “帮我对这篇论文做一站式严格审查”
- “生成统一审查报告和带批注的修订稿”
- “按盲审标准全面检查这篇法学论文”

### 从 Release ZIP 安装

也可以从 GitHub Releases 下载 `unified-thesis-reviewer-v2.7.0.zip`，解压后把目录放到：

```text
~/.codex/skills/unified-thesis-reviewer
```

Windows 对应：

```text
C:\Users\<你的用户名>\.codex\skills\unified-thesis-reviewer
```

## 依赖

- Python 3.8+
- PyMuPDF（推荐，用于嵌入式 PDF 批注和 PDF 文本提取）

安装 PyMuPDF：

```bash
pip install --user PyMuPDF
```

如果系统 pip 受 PEP 668 保护，可按环境改用虚拟环境或：

```bash
pip install --break-system-packages --user PyMuPDF
```

不安装 PyMuPDF 时，部分 PDF 工具会不可用或降级到 XFDF 备用路径。

## 仓库结构

```text
unified-thesis-reviewer/
├── SKILL.md                         # Skill 主入口和编排流程
├── README.md                        # 安装、使用、发布说明
├── CHANGELOG.md                     # 版本变更记录
├── LICENSE                          # Apache-2.0
├── LICENSE-NOTICE.md                # 版权与引用说明
├── rules/                           # 统一审查规则
├── templates/                       # 报告、交互、issues.json 模板
├── tools/                           # PDF/DOCX 批注、交叉引用、打包工具
├── tests/                           # 单元测试和 fixtures
├── examples/                        # 示例 issues/report
└── _bundled/                        # 底层法学审查 skill 的规则 bundle
```

## 命令行工具

已有 `issues.json` 后，可以单独运行这些工具：

```bash
# PDF 嵌入式批注
python tools/annotate-pdf.py input.pdf issues.json output.annotated.pdf

# PDF 文本与坐标预提取
python tools/extract-pdf-text.py input.pdf output.positions.json

# 引用交叉对比
python tools/citation-crossref.py input.pdf output.crossref.json

# DOCX 批注
python tools/inject-docx-comments.py input.docx issues.json output.annotated.docx

# XFDF 备用路径
python tools/generate-xfdf.py input.pdf issues.json output.xfdf
```

## 发布前验证

```bash
python -m unittest discover -s tests -v
python tools/build-bundle.py
python tools/make-dist.py --version 2.7.0 --output-dir .release/unified-thesis-reviewer --dist-dir dist
python tools/bundle-verify.py --path .release/unified-thesis-reviewer
```

`make-dist.py` 会生成：

- `.release/unified-thesis-reviewer/`
- `dist/unified-thesis-reviewer-v2.7.0.zip`

## 重要限制

- 扫描件 PDF 需要先 OCR，纯图片 PDF 无法直接审查文本。
- 加密 docx 需要先解除密码。
- 超长论文建议按章拆分审查。
- 联网核实依赖 Agent 环境可用的搜索/浏览工具；不可联网时会在报告中说明降级。
- 本 Skill 是审阅辅助工具，不替代导师、评审专家或正式学术不端检测系统的最终判断。

## 许可

本项目采用 Apache License 2.0。详见 [`LICENSE`](./LICENSE) 和 [`LICENSE-NOTICE.md`](./LICENSE-NOTICE.md)。
