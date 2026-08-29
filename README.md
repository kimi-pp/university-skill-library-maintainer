# 高校 AI 技能库调研

本项目面向高校学生与员工，调查、验证并整理可直接使用、需要适配或值得借鉴的 agent skills。

## 下载与安装

仓库默认以私有方式发布。登录有权限的 GitHub 账号后，可以选择以下任一方式下载：

```powershell
git clone https://github.com/kimi-pp/university-skill-library-maintainer.git
Set-Location .\university-skill-library-maintainer
```

也可以在 GitHub 仓库页面选择 **Code → Download ZIP**，解压后进入项目根目录。

运行环境要求：Windows 10/11、64 位 Python 3.11–3.13、Microsoft Word/Excel 桌面版、GitHub CLI，以及 Codex 桌面应用。首次安装前请确认 Python 可执行文件的真实路径：

```powershell
$ProjectRoot = (Get-Location).Path
$PythonExe = (Get-Command python.exe).Source
$CodexSkillsRoot = Join-Path $env:USERPROFILE '.codex\skills'

powershell -NoProfile -ExecutionPolicy Bypass `
  -File "$ProjectRoot\07_自动维护工作流\install.ps1" `
  -ProjectRoot $ProjectRoot `
  -PythonExe $PythonExe `
  -CodexSkillsRoot $CodexSkillsRoot
```

安装器会创建项目专用虚拟环境、安装工作流、部署 Codex Skill，并保持 `workflow.enabled=false`、`schedule.mode="manual"`。安装完成后重新打开 Codex 任务，使新的 Skill 生效。

## 快速使用

```powershell
$ProjectRoot = (Get-Location).Path
$CliPython = "$ProjectRoot\07_自动维护工作流\.venv\Scripts\python.exe"

# 查看状态和基础诊断
& $CliPython -I -m skill_maintainer.cli status --project-root $ProjectRoot
& $CliPython -I -m skill_maintainer.cli doctor --project-root $ProjectRoot

# 编辑运行频率、启动时间和启用状态
& $CliPython -I -m skill_maintainer.cli edit-settings --project-root $ProjectRoot
```

涉及设置应用、完整诊断或正式运行时，必须从当前 Codex 桌面任务取得工作区依赖加载器的原始返回文本：

```powershell
$LoaderOutput = '<Codex 工作区依赖加载器的原始返回文本>'

& $CliPython -I -m skill_maintainer.cli apply-settings `
  --project-root $ProjectRoot --loader-output $LoaderOutput

& $CliPython -I -m skill_maintainer.cli run-now `
  --project-root $ProjectRoot --loader-output $LoaderOutput
```

`run-now` 使用同一受信进程完成候选材料审查、项目判断、真实 Office 验证、Word 逐页确认和原子发布。候选 Skill 只做静态读取，不会被安装或执行。运行设置保存在 TOML 文件中，不使用 Excel 作为配置文件；默认不会创建或启用自动任务。

完整的首次导入、网络诊断、修复台账、重建报告、迁移和卸载说明见[自动维护工作流操作手册](07_自动维护工作流/README.md)。

## 已完成任务

- 来源平台：GitHub
- 功能分类：学术写作、引用与出版
- 功能分类：文档、表格、演示文稿与办公自动化
- 功能分类：文献检索与学术研究
- 功能分类：图书馆与信息素养
- 功能分类：编程、数学、数据分析和可视化
- 默认验证：阅读说明与检查包内容
- 交付方式：每个分类分别生成独立 Excel 和独立 Word
- 学科打样：0809 计算机类；公开开源平台范围；14 个专业、8 个能力群
- 学科打样验证：静态拆包与安全审查；未安装、未运行

## 当前成果

- 功能分类入选 skill：157 个（20 / 22 / 31 / 29 / 55）
- 0809 计算机类正式候选：88 个（SA 27 / SB 35 / SB-A 26）
- 功能验证：70 个二级包内容验证，87 个说明核验
- 运行验证：0；按规则等待用户对具体候选另行指令
- 正式交付：6 份 Excel、6 份 DOCX

## 快速入口

- [项目总索引](00_索引/INDEX.md)
- [项目设计](01_规则/2026-08-06-高校AI技能库调研设计.md)
- [首轮三类实施计划](01_规则/2026-08-06-三类GitHub技能调研实施计划.md)
- [第二轮两类实施计划](01_规则/2026-08-06-图书馆与编程数据两类GitHub技能调研实施计划.md)
- [本轮调研范围](01_规则/RESEARCH_SCOPE.md)
- [本科专业目录学科分类索引](02_知识库/discipline_catalog/INDEX.md)
- [0809 计算机类调研索引](02_知识库/discipline_pilots/0809_计算机类/INDEX.md)
- [十二个正式交付物](05_交付物/)

工作区原始文件 `国内大学本科专业目录.xlsx` 不在本项目中改写。
