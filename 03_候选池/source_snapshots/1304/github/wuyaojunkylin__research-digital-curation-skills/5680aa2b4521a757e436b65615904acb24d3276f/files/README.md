# Research Digital Curation Skills

一套面向研究型数字策展、线上展览与数字博物馆工作流的 Claude Skills。

这套 skills 来源于[《汴京十二时辰》数字策展项目](https://www.bianjing-hours.art/)的方法沉淀，但并不限定于历史城市、时辰结构或单一项目案例。它关注的是一类更通用的工作链条：从研究材料出发，转译为策展文本，拆解为页面结构，再进入视觉语言、原型实现和方法复盘。

## Skills

- `research-digital-curation-workflow`：研究型数字策展工作流总控，用于判断项目阶段并安排下一步。
- `curatorial-topic-framing`：策展选题与对象界定，用于明确策展对象、进入尺度、材料边界和阶段目标。
- `research-to-curatorial-copy`：研究转策展文本，用于把研究材料转译成可落位的页面文本。
- `curatorial-narrative-modules`：叙事结构与页面模块，用于拆解页面类型、模块字段、导航关系和交互层级。
- `curatorial-visual-language`：策展视觉语言，用于定义视觉参照系、材料身份、字体层级、色彩和交互语法。
- `curatorial-prototype-standardization`：原型实现与标准单元扩展，用于把已确认结构实现为标准原型并扩展到同类单元。
- `curatorial-log-method-recovery`：项目日志与方法回收，用于记录关键判断、阶段结论、自检问题和可复用方法。

## Installation

将需要使用的 skill 文件夹复制到 Claude Skills 目录中。每个 skill 文件夹都包含一个 `SKILL.md`，没有额外依赖。

```text
curatorial-topic-framing/
└── SKILL.md
```

## Method

这套 skills 默认遵循以下顺序：

```text
研究材料 -> 策展文本 -> 叙事结构 -> 视觉呈现 -> 原型实现 -> 方法回收
```

其中，《汴京十二时辰》线上博物馆项目只是作为参考范式。后续项目可以是城市、人物、物件、档案、地方记忆、机构史、非遗、科技史或其他研究型展览主题。

## About Scripts In The First Release

本套 skills 暂未加入脚本或自动化工具。

这套 skills 的核心能力是策展判断、文本转译、结构拆解和视觉语言校准。这些工作具有较高自由度，需要根据不同研究主题、材料条件和展览对象做判断，避免因自动化脚本而产生的相似性。

后续版本会考虑加入辅助脚本，服务于工作流，但策展判断始终需要用户自己把控。

## License

MIT License. See [LICENSE](LICENSE).
