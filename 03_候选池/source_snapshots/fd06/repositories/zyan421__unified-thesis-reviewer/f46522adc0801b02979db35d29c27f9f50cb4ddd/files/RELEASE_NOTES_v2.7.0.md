# unified-thesis-reviewer v2.7.0

这是 `unified-thesis-reviewer` 的 v2.7.0 发布版，一个面向法学论文未定稿检查的“一站式” Codex/Agent Skill。

## 主要能力

- 统一生成论文深度审查报告、引注校对结果和结构化 `issues.json`
- 支持 PDF 嵌入式批注与 DOCX Word 批注
- 对法律名称、案号、学术文献等高风险事项执行联网核实
- 自动生成引用交叉对比表
- 随仓库提供底层 `legal-thesis-reviewer` 与 `legal-citation-checker` 的规则 bundle

## v2.7.0 更新重点

- 新增严重度判定标尺和“反向举证原则”，减少过度指控
- 新增批注挂载位置原则，让批注更贴近读者真正需要看到的位置
- PDF anchor 搜索支持中文与数字/字母边界空格容错
- 新增 PDF 输入 anchor 选取建议
- 新增实战案例库，把 v2 系列真实失误沉淀为反面教材
- PDF 批注作者同步为“张老师的AGENT”

## 安装

Codex 用户可以直接克隆到 skills 目录：

```bash
cd ~/.codex/skills
git clone https://github.com/zyan421/unified-thesis-reviewer.git
```

Windows PowerShell：

```powershell
cd $env:USERPROFILE\.codex\skills
git clone https://github.com/zyan421/unified-thesis-reviewer.git
```

也可以下载本 Release 附带的 `unified-thesis-reviewer-v2.7.0.zip`，解压到 `~/.codex/skills/unified-thesis-reviewer`。

## 校验

本次发布前已执行：

```bash
python -m unittest discover -s tests -v
python tools/build-bundle.py
python tools/make-dist.py --version 2.7.0 --output-dir .release/unified-thesis-reviewer --dist-dir dist
python tools/bundle-verify.py --path .release/unified-thesis-reviewer
```

详见仓库内 `README.md`、`CHANGELOG.md` 和 `RELEASE-CHECKLIST.md`。
