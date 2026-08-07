# GitHub 分类 04/05 检索矩阵

日期：2026-08-06

## 共同结构词

- `filename:SKILL.md`
- `path:skills SKILL.md`
- `agent skill`、`Claude Code skill`、`Codex skill`、`Agent Skills`
- 仓库描述、主题标签、README 与高相关集合仓库相邻目录

## 04 图书馆与信息素养

### 图书馆服务与教学

- library、librarian、reference interview、research consultation
- information literacy、library instruction、research guide、database navigation
- source evaluation、CRAAP、SIFT、lateral reading、media literacy

### 信息可信度与合规使用

- fact checking、misinformation、verification、source credibility
- copyright literacy、fair use、open access、scholarly communication
- citation literacy、academic integrity、plagiarism education

### 馆藏、元数据与研究支持

- MARC、RDA、BIBFRAME、Dublin Core、metadata crosswalk
- cataloging、authority control、digital collections、archives、IIIF
- institutional repository、research data management、data management plan、FAIR data

## 05 编程、数学、数据分析和可视化

### 编程与软件质量

- programming、coding、repository navigation、code review、refactoring
- debugging、systematic debugging、testing、TDD、property testing
- Python、R、Julia、JavaScript、TypeScript、SQL、Jupyter、notebook

### 数学、统计与建模

- mathematics、proof、symbolic math、numerical methods、optimization
- statistics、hypothesis testing、regression、Bayesian、time series
- machine learning、feature engineering、model evaluation、experiment design

### 数据处理与可视化

- data analysis、data cleaning、EDA、data wrangling、reproducible analysis
- matplotlib、seaborn、plotly、Altair、ggplot、dashboard
- geospatial、GIS、network visualization、scientific visualization

## 去重与停止规则

- 同名技能优先保留可确认的上游仓库，镜像和聚合副本仅内部记录。
- 同一技能在多个生态存在官方适配时保留一个主体记录并独立标注生态。
- 普通软件仓库只有在包含可执行 agent 工作流或可合理封装的任务模板时才作为候选。
- 每个未覆盖子领域完成两轮补充检索；连续两轮没有新增实质能力后停止。
