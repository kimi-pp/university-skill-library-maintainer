"""第二轮分类 04/05 的规范候选数据。

数据由 2026-08-06 GitHub 只读核验记录生成；不会安装或执行候选 skill。
"""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "03_候选池" / "raw"

ROUND2_CATEGORIES = {
    "04": "图书馆与信息素养",
    "05": "编程、数学、数据分析和可视化",
}


def _load_jsonl(category: str) -> list[dict]:
    path = RAW_DIR / f"2026-08-06-category-{category}-github.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


_repo_raw = json.loads(
    (RAW_DIR / "2026-08-06-category-04-05-repositories.json").read_text(encoding="utf-8")
)
ROUND2_REPOSITORIES = {
    repo: {
        "stars": meta["stars"],
        "pushed": meta["pushed"],
        "license": meta["license"],
        "branch": meta["branch"],
    }
    for repo, meta in _repo_raw.items()
}


# path: (中文定位, 功能标签, 简略功能)
SPECS_04 = {
    "examples/skills/reading/information-literacy/SKILL.md": ("信息素养与研究流程", "信息素养、研究问题、来源评估、引用", "用分阶段流程训练从研究问题到检索、评价、综合和规范归因的信息素养。"),
    "examples/skills/digital-literacy/information-evaluation/SKILL.md": ("网络信息评价与横向阅读", "SIFT、横向阅读、来源评价、反向检索", "运用 SIFT、横向阅读和反向图像检索快速判断网络信息与来源可信度。"),
    "examples/skills/communication/media-literacy/SKILL.md": ("媒体与新闻素养", "媒体生态、框架分析、新闻素养、算法意识", "分析媒介形式、新闻框架、算法分发和受众解码，提升媒体内容辨识能力。"),
    "examples/skills/history/source-analysis/SKILL.md": ("一手与二手资料分析", "史料分析、来源语境、作者目的、证据", "用来源类型、作者、语境、目的和相互印证框架分析一手与二手资料。"),
    ".agents/skills/research-information-literacy/SKILL.md": ("研究与信息素养综合指南", "数据库检索、文献综合、研究方法、引文管理", "把数据库高级检索、来源评价、文献综合、研究方法和引文管理汇总为入门指南。"),
    "skills/digital-library-plan/SKILL.md": ("数字图书馆规划模板", "数字图书馆、需求分析、实施路线、指标", "生成数字图书馆建设的目标、关键组件、行动计划和成功指标。"),
    "skills/library-outreach-plan/SKILL.md": ("图书馆推广与外联计划", "读者服务、社区外联、活动传播、评估", "围绕目标群体、传播渠道、行动安排和指标制定图书馆外联计划。"),
    "skills/library-program-design/SKILL.md": ("图书馆项目与活动设计", "用户需求、项目设计、资源配置、评估", "把用户需求转化为图书馆项目方案、资源安排、行动计划和成效指标。"),
    "skills/library-technology-plan/SKILL.md": ("图书馆技术建设规划", "图书馆系统、技术路线、治理、实施", "规划图书馆技术现状评估、目标架构、实施步骤和质量检查。"),
    "skills/media-literacy-program/SKILL.md": ("媒体素养教育项目", "媒体素养、课程设计、学习活动、评价", "设计面向学习者的媒体素养项目，覆盖目标、核心内容、活动和评价指标。"),
    "skills/fact-checking-protocol/SKILL.md": ("事实核查教学协议", "事实核查、证据链、来源交叉验证、记录", "提供轻量事实核查流程模板，用于定义取证步骤、输出结构和质量清单。"),
    "skills/data-literacy-program/SKILL.md": ("数据素养教育项目", "数据素养、课程设计、数据解读、评价", "设计数据获取、理解、解释与沟通能力培养项目及其评估指标。"),
    "skills/source-management/SKILL.md": ("信息来源管理流程", "来源台账、标签、版本、可追溯性", "为来源采集、分类、记录、更新和复核建立轻量管理流程。"),
    "skills/fact-check-x-unified/SKILL.md": ("可复现事实核查统一入口", "事实核查、证据优先、答案比较、交付门禁", "编排证据优先的主张拆解、并行取证、答案比较、裁决与可复现报告流程。"),
    "skills/fact-check-x-authoritative-verify/SKILL.md": ("权威来源证据核验", "权威证据、并行取证、主张裁决、审计", "针对单一知识点从权威来源取证，由当前智能体裁决并形成可审计报告。"),
    "SKILL.md::SamaritanOC/fact-checker": ("系统化事实核查与提示注入防护", "事实核查、来源分级、提示注入、安全边界", "按专业核查协议完成主张拆分、证据搜索、来源分级和结论表达，并处理恶意网页指令。"),
    "skills/literature/fulltext/institutional-repository-guide/SKILL.md": ("机构知识库发现与使用", "机构知识库、DSpace、OAI-PMH、开放获取", "识别和检索机构知识库，理解常见平台，并通过 OAI-PMH 发现开放资源。"),
    "skills/literature/search/worldcat-search-api/SKILL.md": ("WorldCat 联合目录检索", "WorldCat、馆藏发现、书目元数据、API", "通过 WorldCat Search API 检索全球图书馆馆藏和书目元数据。"),
    "skills/research/funding/open-science-guide/SKILL.md": ("开放科学实践指南", "开放科学、预注册、注册报告、数据共享", "指导预注册、注册报告、开放数据、开放材料和透明研究实践。"),
    "skills/tools/scraping/repository-harvesting-guide/SKILL.md": ("开放知识库元数据采集", "OAI-PMH、元数据采集、增量同步、Python", "说明 OAI-PMH 六类请求、选择性与增量采集，并给出 Python 采集工作流。"),
    "skills/research/funding/figshare-api/SKILL.md": ("Figshare 科研资源管理", "Figshare、数据集、研究对象、API", "使用 Figshare API 检索、读取和管理公开研究数据集及文件元数据。"),
    "skills/literature/fulltext/pmc-oai-api/SKILL.md": ("PMC 开放文献元数据采集", "PubMed Central、OAI-PMH、全文、元数据", "通过 PMC-OAI 接口批量获取开放论文记录、元数据及可用全文入口。"),
    "skills/general/fair-data/SKILL.md": ("FAIR 数据原则速查", "FAIR、科研数据、数据存储库、复用", "按可发现、可访问、可互操作和可复用四项原则检查科研数据管理。"),
    "codex/fair-check/SKILL.md": ("FAIR 论文与研究对象检查", "FAIR、论文审计、研究对象、透明报告", "清点论文关联研究对象并逐项检查其可发现性、可访问性、互操作性与复用性。"),
    "skills/design-metadata-schema/SKILL.md": ("元数据模式设计", "元数据、字段约束、验证、模式文档", "从业务与检索需求出发定义字段、约束、验证规则和可维护的元数据模式。"),
    "SKILL.md::Albert-Libra/nanobot-zotero-bridge": ("Zotero 本地知识库桥接", "Zotero、全文索引、RAG、混合检索", "把 Zotero 馆藏分层同步到本地 FTS5 与 RAG 索引，支持基于个人文献库的可引用检索。"),
    "skills/ontology-term-resolution/SKILL.md": ("本体术语规范化与解析", "本体、受控词表、术语映射、数据规范", "在指定本体范围内把自由文本解析为规范术语，并显式报告未匹配或模糊结果。"),
    "skills/labarchive-integration/SKILL.md": ("LabArchives 电子实验记录集成", "ELN、实验记录、库存、API、权限", "规划 LabArchives ELN 与库存接口的认证、区域端点、读取和受控写入请求。"),
    ".agent/skills/develop-web-translator/SKILL.md": ("Zotero 网页翻译器开发", "Zotero Translator、网页元数据、测试、馆藏导入", "分析网站结构并开发、测试 Zotero 网页翻译器，以改善书目元数据抓取与导入。"),
}


SPECS_05 = {
    "skills/get-available-resources/SKILL.md": ("计算资源侦测与策略建议", "CPU、GPU、内存、磁盘、计算规划", "在计算密集任务前只读盘点 CPU、GPU、内存和磁盘，并据此建议并行、分块或外存策略。"),
    "skills/exploratory-data-analysis/SKILL.md": ("可复现探索性数据分析", "EDA、数据质量、分布、异常、报告", "以授权范围、数据质量、分布、关系、异常和可复现输出为主线开展探索性分析。"),
    "skills/dask/SKILL.md": ("Dask 并行与大数据处理", "Dask、并行计算、分布式、DataFrame", "用 Dask DataFrame、Array 和任务调度扩展超出单机内存或需并行的数据工作负载。"),
    "skills/polars/SKILL.md": ("Polars 高性能表格处理", "Polars、DataFrame、惰性执行、ETL", "使用 Polars 的表达式、惰性执行和列式计算构建快速、可审计的数据转换流程。"),
    "skills/vaex/SKILL.md": ("Vaex 超大表格分析", "Vaex、内存映射、大数据、可视化", "借助内存映射和延迟计算交互分析超大表格数据，减少内存占用。"),
    "skills/zarr-python/SKILL.md": ("Zarr 分块数组存储", "Zarr、分块、压缩、云存储、数组", "创建、读写和组织带分块与压缩的 N 维数组，支持本地或对象存储工作流。"),
    "skills/matplotlib/SKILL.md": ("Matplotlib 通用绘图", "Matplotlib、静态图、子图、导出", "用面向对象接口完成可控的二维绘图、布局、标注和多格式导出。"),
    "skills/seaborn/SKILL.md": ("Seaborn 统计可视化", "Seaborn、统计图、分布、关系、分类", "以统计语义快速制作分布、关系和分类比较图，并与 Matplotlib 精细控制协同。"),
    "skills/scientific-visualization/SKILL.md": ("科学图表设计与审计", "科学可视化、证据编码、无障碍、出版", "从证据与传播目标出发选择诚实编码，落实无障碍、导出和来源追踪检查。"),
    "skills/networkx/SKILL.md": ("NetworkX 网络分析", "图网络、中心性、路径、社区、可视化", "创建和分析复杂网络，覆盖路径、中心性、聚类、社区和基础网络可视化。"),
    "skills/geopandas/SKILL.md": ("GeoPandas 空间数据分析", "GeoPandas、GIS、CRS、空间连接、地图", "处理矢量空间数据、坐标系、几何有效性、空间连接与地图输出。"),
    "skills/scikit-learn/SKILL.md": ("Scikit-learn 机器学习", "机器学习、预处理、模型选择、评估、管道", "构建预处理、训练、验证、模型选择和解释相衔接的传统机器学习流程。"),
    "skills/statistical-analysis/SKILL.md": ("统计分析选择与报告", "统计检验、假设、效应量、报告、诊断", "依据研究设计、变量类型和假设条件选择统计方法，并完成诊断、效应量和结果报告。"),
    "skills/statistical-power/SKILL.md": ("统计功效与样本量规划", "统计功效、样本量、效应量、模拟", "围绕目标效应、显著性水平和功效进行样本量估计及复杂模型的模拟功效分析。"),
    "skills/statsmodels/SKILL.md": ("Statsmodels 统计建模", "回归、GLM、混合模型、时间序列、诊断", "使用 Statsmodels 完成回归、广义模型、时间序列与严格推断，并保留诊断输出。"),
    "skills/pymc/SKILL.md": ("PyMC 贝叶斯建模", "贝叶斯、MCMC、先验、后验、诊断", "按标准贝叶斯工作流选择先验与似然、采样、诊断和解释后验不确定性。"),
    "skills/sympy/SKILL.md": ("SymPy 符号数学", "符号计算、代数、微积分、方程、代码生成", "用精确符号对象完成代数化简、求解、微积分、矩阵和数值代码转换。"),
    "skills/uncertainty-and-units/SKILL.md": ("测量不确定度与单位计算", "单位、误差传播、测量、不确定度、量纲", "在计算中保留单位和不确定度，防止尺度、偏移温度及对数单位等常见错误。"),
    "skills/shap/SKILL.md": ("SHAP 模型解释", "SHAP、可解释机器学习、特征贡献、公平性", "选择合适解释器与背景分布，计算并审计局部和全局特征贡献。"),
    "skills/umap-learn/SKILL.md": ("UMAP 降维与嵌入", "UMAP、降维、聚类可视化、参数调优", "对标准化数据构建 UMAP 嵌入，调节邻域与距离参数并避免过度解释二维图。"),
    "skills/timesfm-forecasting/SKILL.md": ("TimesFM 时间序列预测", "时间序列、基础模型、预测、硬件预检", "在硬件和版本预检后使用 TimesFM 进行零样本或微调时间序列预测与评估。"),
    "skills/matlab/SKILL.md": ("MATLAB 与 GNU Octave 计算", "MATLAB、Octave、数值计算、表格、绘图", "在许可证与安全边界内编写 MATLAB/Octave 脚本、函数、数值分析和可视化。"),
    "skills/simpy/SKILL.md": ("SimPy 离散事件仿真", "仿真、离散事件、资源、队列、实验", "用事件、进程和资源构建可重复的离散事件模型，并设计有界仿真实验。"),
    "skills/optimize-for-gpu/SKILL.md": ("Python GPU 性能优化", "GPU、性能分析、CUDA、向量化、优化", "先分析性能瓶颈和数据搬运成本，再选择 GPU 库并分阶段优化 Python 工作负载。"),
    "skills/pymoo/SKILL.md": ("Pymoo 多目标优化", "多目标优化、Pareto、约束、进化算法", "定义目标、约束与算法，求解并解释多目标优化中的 Pareto 解集。"),
    "skills/pytorch-lightning/SKILL.md": ("PyTorch Lightning 训练工程", "深度学习、训练循环、分布式、复现、日志", "用 LightningModule、Trainer 和 DataModule 组织可复现、可扩展的深度学习训练。"),
    "skills/transformers/SKILL.md": ("Transformers 模型应用", "Transformer、NLP、推理、微调、模型仓库", "使用 Transformers 完成模型加载、推理、任务管道和受控微调，并处理认证与版本差异。"),
    "skills/systematic-debugging/SKILL.md": ("系统化调试", "调试、根因分析、假设检验、证据", "按根因调查、模式分析、假设验证和修复确认四阶段处理软件缺陷。"),
    "skills/test-driven-development/SKILL.md": ("测试驱动开发", "TDD、红绿重构、单元测试、设计", "执行先失败测试、最小实现和重构循环，确保每次行为变更都有可观察证据。"),
    "skills/requesting-code-review/SKILL.md": ("发起代码审查", "代码审查、变更范围、审查请求、质量门", "在关键节点整理变更范围、验证证据和审查重点，发起可执行的代码审查。"),
    "skills/receiving-code-review/SKILL.md": ("处理代码审查反馈", "代码审查、反馈验证、技术判断、沟通", "先理解和验证审查意见，再按技术证据实施，妥善处理含糊或不适用建议。"),
    "plugins/business-analytics/skills/data-storytelling/SKILL.md": ("数据叙事与洞察表达", "数据故事、受众、叙事结构、图表、建议", "把分析结论组织为面向特定受众的背景、冲突、洞察和行动建议。"),
    "plugins/database-design/skills/postgresql/SKILL.md": ("PostgreSQL 表结构设计", "PostgreSQL、数据类型、约束、索引、RLS", "依据 PostgreSQL 特性设计数据类型、约束、索引、表类别和行级安全。"),
    "plugins/data-engineering/skills/data-quality-frameworks/SKILL.md": ("数据质量框架", "数据质量、测试金字塔、校验、可观测性", "按准确性、完整性、一致性等维度设计数据质量规则、测试层级和监控。"),
    "plugins/data-engineering/skills/dbt-transformation-patterns/SKILL.md": ("dbt 数据转换模式", "dbt、分层建模、测试、文档、血缘", "使用分层模型、命名、测试和文档惯例组织可维护的 dbt 转换项目。"),
    "plugins/data-engineering/skills/spark-optimization/SKILL.md": ("Apache Spark 性能优化", "Spark、执行计划、分区、缓存、性能", "通过执行计划、分区、连接策略和资源配置诊断并优化 Spark 作业。"),
    "plugins/developer-essentials/skills/sql-optimization-patterns/SKILL.md": ("SQL 查询优化", "SQL、执行计划、索引、连接、性能", "读取执行计划并应用索引、连接、过滤和重写模式优化 SQL 查询。"),
    "plugins/machine-learning-ops/skills/ml-pipeline-workflow/SKILL.md": ("机器学习管道工作流", "MLOps、训练管道、评估、部署、监控", "规划从数据验证、特征、训练、评估到部署和监控的机器学习管道。"),
    "plugins/python-development/skills/python-testing-patterns/SKILL.md": ("Python 测试模式", "pytest、单元测试、集成测试、隔离、覆盖率", "用测试层级、AAA 结构、夹具、模拟和隔离策略构建 Python 测试体系。"),
    "plugins/python-development/skills/python-code-style/SKILL.md": ("Python 代码风格与文档", "Python、格式化、类型标注、文档、命名", "统一 Python 格式化、命名、类型标注、文档字符串和自动检查。"),
    "plugins/python-development/skills/python-error-handling/SKILL.md": ("Python 错误处理", "异常、上下文、部分失败、日志、恢复", "设计明确异常类型、上下文保留、部分失败和恢复策略，避免吞错。"),
    "plugins/python-development/skills/python-project-structure/SKILL.md": ("Python 项目结构", "Python、模块、包、接口、项目架构", "按内聚模块、显式接口和一致约定组织可测试、可维护的 Python 项目。"),
    "plugins/python-development/skills/python-performance-optimization/SKILL.md": ("Python 性能分析与优化", "Python、profiling、基准、内存、优化", "先建立基准并定位 CPU、内存或 I/O 瓶颈，再选择针对性优化手段。"),
    "plugins/python-development/skills/async-python-patterns/SKILL.md": ("Python 异步编程模式", "asyncio、并发、任务、取消、超时", "判断同步与异步适用边界，并正确处理任务、取消、超时和资源生命周期。"),
    "plugins/javascript-typescript/skills/javascript-testing-patterns/SKILL.md": ("JavaScript/TypeScript 测试模式", "JavaScript、TypeScript、Jest、Vitest、端到端测试", "使用 Jest、Vitest 等工具组织单元、集成和端到端测试及常见测试模式。"),
    "data-analytics/SKILL.md": ("数据分析架构图生成", "数据架构、ETL、数据库、mxGraph、图示", "按照图形语法和分析/ETL 图元生成数据平台、管道和分析架构图。"),
    "vega/SKILL.md": ("Vega/Vega-Lite 图表生成", "Vega、Vega-Lite、JSON、交互图表", "依据字段类型和语法约束生成可渲染的 Vega 或 Vega-Lite JSON 可视化。"),
    "graphviz/SKILL.md": ("Graphviz DOT 图示", "Graphviz、DOT、关系图、流程图、布局", "用正确的 DOT、子图、标签和边语法生成流程、依赖与网络结构图。"),
    "skills/lean-proof/SKILL.md": ("Lean 定理证明方法", "Lean、形式化证明、定理、错误定位、mathlib", "以小步验证和错误优先策略构造、调试并清理 Lean 形式化证明。"),
    "skills/mathlib-review/SKILL.md": ("Mathlib 代码审查", "Lean、mathlib、PR 审查、API、风格", "依据 mathlib 的属性、API 和风格要求审查形式化数学贡献。"),
    "skills/bayesian-reasoning-calibration/SKILL.md": ("贝叶斯推理与概率校准", "贝叶斯、先验、似然、概率、决策", "显式记录先验和新证据的似然，更新概率判断并校准决策信心。"),
    "skills/causal-inference-root-cause/SKILL.md": ("因果推断与根因分析", "因果推断、反事实、假设、根因、实验", "提出竞争性因果假设，利用反事实与可区分检验寻找更可信的根因。"),
    "skills/design-of-experiments/SKILL.md": ("实验设计", "实验设计、随机化、对照、功效、分析计划", "把研究问题转化为因素、处理、对照、随机化和预先分析计划。"),
    "skills/visualization-choice-reporting/SKILL.md": ("可视化选择与结果报告", "图表选择、数据类型、叙事、报告、误导防范", "根据问题和数据类型选择图表，完成设计检查、叙事组织和误导风险审计。"),
    "skills/d3-visualization/SKILL.md": ("D3.js 交互可视化", "D3.js、SVG、交互、布局、数据绑定", "用数据绑定、比例尺、轴、过渡和布局创建可复用的交互式 Web 可视化。"),
}


HIGH_PRIORITY = {
    "information-literacy", "information-evaluation", "source-analysis", "fact-check-x-unified",
    "institutional-repository-guide", "worldcat-search-api", "open-science-guide", "repository-harvesting-guide",
    "fair-check", "zotero-bridge", "ontology-term-resolution",
    "get-available-resources", "exploratory-data-analysis", "scientific-visualization", "statistical-analysis",
    "statistical-power", "statsmodels", "sympy", "uncertainty-and-units", "systematic-debugging",
    "test-driven-development", "data-storytelling", "python-testing-patterns", "visualization-choice-reporting",
}


def _slug(row: dict) -> str:
    if row["path"] == "SKILL.md":
        return row["name"].strip().lower().replace(" ", "-").replace("&", "and")
    return Path(row["path"]).parent.name


def _spec_key(row: dict) -> str:
    if row["path"] == "SKILL.md":
        return f"SKILL.md::{row['repo']}"
    return row["path"]


def _ecosystem(repo: str) -> str:
    return {
        "K-Dense-AI/scientific-agent-skills": "Agent Skills（兼容 Codex、Claude Code、Cursor 等）",
        "obra/superpowers": "Agent Skills（兼容 Codex、Claude Code）",
        "wshobson/agents": "多智能体生态（Codex、Claude Code、Cursor、Gemini CLI 等）",
        "markdown-viewer/skills": "AI 编程智能体通用工作流",
        "leanprover/skills": "Agent Skills（Lean 生态）",
        "lyndonkl/claude": "Anthropic Claude Code / 可移植工作流",
        "wentorai/research-plugins": "Research-Claw / 可移植工作流",
        "lionelsimai/claude-skills-collection": "Anthropic Claude Code / 可移植模板",
        "ASI2030/Fact-Check-X": "Agent Skills（跨生态）",
        "SamaritanOC/fact-checker": "Agent Skills（跨生态）",
        "Tibsfox/gsd-skill-creator": "Agent Skills 社区示例",
        "AhmedAnwar-Gazy/latex_templet": "Agent Skills（.agents 目录）",
        "wu-yc/LabClaw": "LabClaw / 可移植工作流",
        "scdenney/open-science-skills": "OpenAI Codex、Anthropic Claude Code",
        "dandye/ai-runbooks": "Agent Skills（通用）",
        "Albert-Libra/nanobot-zotero-bridge": "nanobot / 可适配 Agent Skill",
        "zotero/translators": "Zotero 开发工作流 / Agent Skill",
    }.get(repo, "Agent Skills / 可移植工作流")


def _profile(cat: str, slug: str, repo: str) -> tuple[str, str, str, str, str, str]:
    if cat == "04":
        if any(word in slug for word in ("library", "worldcat", "repository", "oai", "figshare", "pmc")):
            return (
                "学生、教师、科研人员、图书馆人员",
                "馆藏发现、开放资源检索、知识库建设与服务规划",
                "B",
                "将示例端点、认证方式和输出字段映射到本校图书馆系统；先以只读方式接入。",
                "网络；部分功能需要 API 密钥、机构订阅或本地脚本",
                "外部接口、馆藏覆盖和访问政策会变化；不得绕过权限或版权限制。",
            )
        if any(word in slug for word in ("fact", "information-evaluation", "source-analysis")):
            return (
                "学生、教师、科研人员、图书馆与宣传人员",
                "课程信息辨识、新闻与网络主张核验、来源教育",
                "B",
                "保留证据分级和人工裁决，把搜索工具替换为本项目可用的浏览与数据库接口。",
                "网络检索；必要时使用网页归档或反向图像检索",
                "检索不到不等于主张为假；恶意网页内容、时效性和来源偏差需单独处理。",
            )
        if any(word in slug for word in ("zotero", "metadata", "ontology", "fair", "labarchive")):
            return (
                "科研人员、研究生、图书馆与科研数据管理人员",
                "个人/机构知识库、科研数据治理、元数据规范与术语控制",
                "B",
                "从只读盘点和小样本映射开始；凭据、写操作和批量变更另设审批。",
                "对应平台或数据标准；部分功能需要 Python、API 凭据或本地索引",
                "元数据映射可能丢失语义；凭据、未公开研究对象和批量写入必须受控。",
            )
        return (
            "学生、教师、图书馆人员",
            "信息素养课程、读者培训、图书馆项目与服务设计",
            "B",
            "可作为课程或服务模板，需补充本校资源、制度、学习目标和评价量规。",
            "无硬性运行依赖；实施时需要本校资源与受众信息",
            "内容较通用或较轻量，不能替代本校政策、专业馆员判断和学习成效评估。",
        )

    if repo == "K-Dense-AI/scientific-agent-skills":
        deps = "Python 及相应科学计算包；部分技能需要 GPU、网络、许可证或较大内存"
        risk = "必须先核对数据授权、版本、计算资源和方法假设；示例代码不等同于已验证结果。"
        return (
            "学生、教师、科研人员、数据与技术支持人员",
            "课程作业、科研数据处理、统计建模、机器学习和科学图表",
            "A",
            "按 Codex skill 结构接入；固定依赖版本，并为本校数据与算力环境补充预检。",
            deps,
            risk,
        )
    if repo == "obra/superpowers":
        return (
            "学生、教师、开发与技术支持人员",
            "课程项目、科研软件、系统开发中的调试、测试与审查",
            "A",
            "可直接采用方法流程；与项目现有测试、版本控制和审查规则对齐。",
            "代码库、测试工具和版本控制环境",
            "方法会改变开发节奏；不能把流程完成当作功能正确，仍需真实测试证据。",
        )
    if repo == "wshobson/agents":
        return (
            "学生、教师、数据工程与开发人员",
            "教学项目、数据平台、数据库、Python/JavaScript 工程和 MLOps",
            "B",
            "抽取单一 skill 并替换 Claude 插件路由；保留与现有工具链相匹配的章节。",
            "对应语言、数据库或数据平台；部分流程需要云服务或测试框架",
            "技术栈与版本差异较大；性能、安全和数据质量结论必须由实际环境验证。",
        )
    if repo == "markdown-viewer/skills":
        return (
            "学生、教师、科研与数据分析人员",
            "分析报告、课程讲义和技术文档中的图表或架构图",
            "B",
            "保留输出语法约束，将渲染器替换为项目支持的 Markdown、Vega 或 Graphviz 工具。",
            "相应图形渲染器或支持的 Markdown 查看器",
            "仓库许可证未明确；语法正确不保证数据表达诚实，必须复核来源与尺度。",
        )
    if repo == "leanprover/skills":
        return (
            "数学、计算机专业学生与教师、形式化方法研究人员",
            "Lean 课程、形式化证明、mathlib 贡献与代码审查",
            "B",
            "对接本校 Lean/mathlib 版本和构建命令，所有证明以实际编译通过为准。",
            "Lean 工具链、mathlib 与项目构建环境",
            "本轮未编译证明；版本和导入差异会影响结论。",
        )
    return (
        "学生、教师、科研与数据分析人员",
        "实验设计、因果与贝叶斯推理、可视化选择和交互图表",
        "B",
        "将 Claude 专用调用替换为 Codex 可用工具，并补充学科统计假设和验证门。",
        "按任务可能需要统计软件、D3.js 或浏览器环境",
        "仓库许可证未明确；方法模板不能代替数据诊断、因果识别条件或真实运行验证。",
    )


def _build_category(category: str, specs: dict[str, tuple[str, str, str]]) -> list[dict]:
    records = []
    for index, raw in enumerate(_load_jsonl(category), start=1):
        key = _spec_key(raw)
        if key not in specs:
            raise KeyError(f"缺少规范说明：{category} {raw['repo']} {raw['path']}")
        cn, tags, summary = specs[key]
        slug = _slug(raw)
        roles, scenario, compat, adapt, deps, risk = _profile(category, slug, raw["repo"])
        if raw["license"] in {"未明确", "NOASSERTION"}:
            risk += " 仓库许可证未明确或无法由 GitHub 自动识别，采用前需单独核验。"
        headings = "、".join(raw["headings"][:5])
        detail = (
            f"{summary} 本轮读取了 {raw['line_count']} 行说明"
            f"，重点核对了{headings or '功能定位、输入输出、依赖和边界'}。"
            "该结论仅反映说明与包结构，不代表依赖已安装或任务已成功运行。"
        )
        verify = "二级包内容验证" if raw["package_files"] > 1 else "说明已核验"
        records.append(
            {
                "id": f"GH-{category}-{index:04d}",
                "name": slug,
                "cn": cn,
                "cat": category,
                "repo": raw["repo"],
                "path": raw["path"],
                "ecosystem": _ecosystem(raw["repo"]),
                "form": "社区 skill、GitHub 开源仓库" if raw["license"] not in {"未明确", "NOASSERTION"} else "社区 skill、GitHub 公开仓库（许可证待核）",
                "tags": tags,
                "summary": summary,
                "detail": detail,
                "roles": roles,
                "scenario": scenario,
                "compat": compat,
                "adapt": adapt,
                "deps": deps,
                "risk": risk,
                "verify": verify,
                "priority": "高" if slug in HIGH_PRIORITY else "中",
                "related": "同类技能按任务粒度并存；部署时优先选择覆盖需求且许可证、依赖和维护状态更合适者。",
                "package_files": raw["package_files"],
                "script_files": raw["script_files"],
                "reference_asset_files": raw["reference_asset_files"],
                "line_count": raw["line_count"],
            }
        )
    return records


ROUND2_CANDIDATES = _build_category("04", SPECS_04) + _build_category("05", SPECS_05)

