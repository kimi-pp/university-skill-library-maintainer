"""Validate the source ledger and build a plain-language derived catalog."""

import json
import re
from pathlib import Path


PLAIN_FIELDS = (
    "plain_purpose",
    "plain_outputs",
    "plain_audience",
    "plain_when_to_use",
    "plain_prerequisites",
    "plain_limitations",
    "plain_integration",
    "plain_verification",
)

TERM_EXPLANATIONS = {
    "MCP": "MCP（让 AI 连接外部工具的通用方式）",
    "API": "API（软件之间交换信息的接口）",
    "OCR": "OCR（把图片中的文字识别为可编辑文本）",
    "RAG": "RAG（先查资料再生成回答的方法）",
    "MLOps": "MLOps（管理机器学习模型开发和维护的流程）",
    "ETL": "ETL（抽取、整理并保存数据的流程）",
    "PMC-OAI": "PMC-OAI（批量获取开放医学论文资料的服务）",
    "OAI-PMH": "OAI-PMH（批量交换文献基本信息的标准）",
    "PRISMA": "PRISMA（规范系统综述过程和报告的标准）",
    "D3.js": "D3.js（制作网页交互图表的工具）",
    "DBLP": "DBLP（计算机领域文献数据库）",
    "DOI": "DOI（论文等数字资源的永久标识）",
    "CFP": "CFP（会议征稿通知）",
    "BGPT": "BGPT（检索并整理生物医学论文的服务）",
    "GPU": "GPU（适合大量并行计算的图形处理器）",
    "CPU": "CPU（执行通用计算任务的处理器）",
    "PDF": "PDF（常用的固定版式文档格式）",
    "PPTX": "PPTX（PowerPoint 演示文稿格式）",
    "DOCX": "DOCX（Word 文档格式）",
    "XLSX": "XLSX（Excel 工作簿格式）",
    "CLI": "CLI（通过输入命令操作软件的方式）",
    "HTTP": "HTTP（网页服务常用的通信规则）",
    "REST": "REST（通过网址使用网络服务的一种方式）",
    "SQL": "SQL（查询和管理数据库的语言）",
    "FTS5": "FTS5（SQLite 数据库的全文检索功能）",
    "ELN": "ELN（电子实验记录本）",
    "I/O": "I/O（数据的输入与输出）",
    "UMAP 嵌入": "UMAP 嵌入（把高维数据转换成便于绘图的一组坐标）",
    "UMAP": "UMAP（把高维数据压缩成二维或三维图形的方法）",
    "JSON": "JSON（一种结构化文本数据格式）",
    "UI": "UI（用户看到并操作的界面）",
    "ZIP": "ZIP（压缩文件格式）",
    "PMC": "PMC（开放获取的生物医学论文全文库）",
    "SIFT": "SIFT（先停下、查来源、找更好报道、追溯原始依据的核查方法）",
    "LLM": "LLM（能理解并生成文本的大型语言模型）",
    ".NET": ".NET（微软的软件开发平台）",
    "COM": "COM（Windows 软件之间互相控制的方式）",
    "AAA": "AAA（准备、执行、检查结果的测试写法）",
    "CS": "CS（计算机科学）",
    "DOT": "DOT（用文本描述关系图的格式）",
    "MATLAB": "MATLAB（用于数值计算与工程分析的软件）",
    "PMID": "PMID（生物医学论文在 PubMed 中的编号）",
    "URL": "URL（网页地址）",
    "Python": "Python（常用于数据处理和自动化的编程语言）",
    "JavaScript": "JavaScript（常用于网页和自动化的编程语言）",
    "Node.js": "Node.js（运行网页类小程序的环境）",
    "Markdown": "Markdown（用简单符号排版文本的格式）",
    "LaTeX": "LaTeX（常用于学术论文排版的工具）",
    "BibTeX": "BibTeX（保存和排版参考文献的格式）",
    "Docker": "Docker（把软件及其运行环境打包部署的工具）",
    "Pandoc": "Pandoc（转换多种文档格式的工具）",
    "Poppler": "Poppler（读取和转换 PDF 的工具）",
    "LibreOffice": "LibreOffice（可批量处理办公文档的软件）",
    "IMRaD": "IMRaD（按引言、方法、结果和讨论组织论文的结构）",
    "python-docx": "python-docx（自动创建和修改 Word 文档的软件）",
    "GitHub Release": "GitHub Release（项目维护者正式发布的版本包）",
    "humanize": "humanize（让机器生成文本更接近自然表达的处理步骤）",
    "APA": "APA（常用于学术写作的引用格式）",
    "嵌入对象": "嵌入对象（放在 Office 文件内的图片、图表或其他内容）",
    "Dask": "Dask（把大型计算任务拆开处理的软件）",
    "Polars": "Polars（快速处理表格数据的软件）",
    "Vaex": "Vaex（减少内存占用来分析超大表格的软件）",
    "Zarr": "Zarr（把大型多维数据分块保存的工具）",
    "Matplotlib": "Matplotlib（制作和细调二维图表的软件）",
    "Seaborn": "Seaborn（快速制作统计图表的软件）",
    "NetworkX": "NetworkX（分析关系网络的软件）",
    "GeoPandas": "GeoPandas（处理地图和空间数据的软件）",
    "Scikit-learn": "Scikit-learn（用于传统机器学习的软件）",
    "Statsmodels": "Statsmodels（用于统计建模和推断的软件）",
    "PyMC": "PyMC（用于贝叶斯统计建模的软件）",
    "SymPy": "SymPy（进行符号数学计算的软件）",
    "SHAP": "SHAP（解释模型预测受各项因素影响程度的方法）",
    "TimesFM": "TimesFM（用于时间序列预测的模型）",
    "SimPy": "SimPy（模拟排队、资源等离散事件的软件）",
    "Pymoo": "Pymoo（求解多个相互制约目标的软件）",
    "PyTorch Lightning": "PyTorch Lightning（组织深度学习训练的软件）",
    "Transformers": "Transformers（使用和调整预训练模型的软件库）",
    "PostgreSQL": "PostgreSQL（开源关系型数据库软件）",
    "dbt": "dbt（组织和检查数据转换流程的工具）",
    "Apache Spark": "Apache Spark（把大数据任务分散处理的软件）",
    "Spark": "Spark（把大数据任务分散处理的软件）",
    "Jest": "Jest（检查 JavaScript 程序的测试工具）",
    "Vitest": "Vitest（检查 JavaScript 程序的测试工具）",
    "TypeScript": "TypeScript（在 JavaScript 基础上增加类型检查的编程语言）",
    "Vega-Lite": "Vega-Lite（用结构化说明生成图表的工具）",
    "Vega": "Vega（用结构化说明生成图表的工具）",
    "Graphviz": "Graphviz（根据文字说明生成关系图的工具）",
    "Lean": "Lean（由计算机检查数学证明的工具）",
    "mathlib": "mathlib（供 Lean 使用的数学定理资料库）",
    "元数据": "元数据（描述资料的信息，如题名、作者和日期）",
    "本体": "本体（规定概念及其关系的标准术语体系）",
    "缓存": "缓存（为加快使用而临时保存的数据）",
    "插件": "插件（给现有软件增加功能的小程序）",
    "框架": "框架（组织工作步骤和配套工具的一套结构）",
    "索引": "索引（帮助快速查找资料或数据的检索结构）",
    "并发": "并发（同时推进多个任务）",
    "异步": "异步（等待某项工作时继续处理其他工作）",
    "内存映射": "内存映射（按需读取磁盘数据以减少内存占用的方法）",
    "惰性执行": "惰性执行（先记录步骤，需要结果时再计算）",
    "列式计算": "列式计算（按数据列处理以提高效率的方法）",
    "Meta 分析": "Meta 分析（合并多项研究结果的统计方法）",
    "主动学习": "主动学习（让模型优先推荐最值得人工判断的条目）",
}

COMPATIBILITY_TEXT = {
    "A": "基本可以直接放入现有 AI 工作台使用，但仍需按本校制度和工具设置进行检查。",
    "B": "经过少量调整后可以使用，常见调整包括更换工具、路径或账号设置。",
    "C": "需要较多改写或配套服务，建议先做小范围试用再决定是否建设。",
    "D": "主要适合参考其中的方法或模板，不建议原样接入。",
}

VERIFICATION_TEXT = {
    "说明已核验": "说明已核验：已核对用途与使用说明；本次未安装、未运行，不能据此判断实际效果。",
    "二级包内容验证": "包内容已核验：已核对用途说明和包内文件；本次未安装、未运行，不能据此判断实际效果。",
}

OUTPUT_TEXT_BY_SUBCATEGORY = {
    "01-01": "可得到论文整体计划、章节蓝图或投稿前审计清单。",
    "01-02": "可得到论文章节草稿、结构提纲或修订稿。",
    "01-03": "可得到符合篇幅要求的摘要、关键词清单或压缩稿。",
    "01-04": "可得到语言润色后的修订稿和术语一致性清单。",
    "01-05": "可得到参考文献清单、核验报告或整理后的文献记录。",
    "01-06": "可得到排版后的论文文档、协作配置或修改记录。",
    "01-07": "可得到投稿要求清单、文档模板或倒排计划。",
    "01-08": "可得到终稿检查清单和出版前材料方案。",
    "01-09": "可得到审查意见、逐点回复信或论文修改清单。",
    "02-01": "可得到创建或修改后的 Word 文档及版式检查报告。",
    "02-02": "可得到 Excel 工作簿、数据表、公式检查或基础图表。",
    "02-03": "可得到演示文稿、讲者备注和逐页检查报告。",
    "02-04": "可得到整理后的 PDF 文档、提取文本或版式检查报告。",
    "02-05": "可得到需求清单和经过分阶段确认的文档草稿。",
    "02-06": "可得到转换后的 Office 文档或 Markdown 文档及转换报告。",
    "02-07": "可得到一批转换文件、失败清单和质量检查报告。",
    "02-08": "可得到处理后的 Office 文档、工作簿或自动化执行报告。",
    "02-09": "可得到无障碍问题清单、修复方案或修复后的文档。",
    "03-01": "可得到跨数据库检索结果、去重后的文献记录和来源清单。",
    "03-02": "可得到指定数据库的文献检索结果和文献记录。",
    "03-03": "可得到合法开放全文清单、下载结果或获取报告。",
    "03-04": "可得到可检索的文献记录、研究笔记或本地文档库。",
    "03-05": "可得到论文摘要、证据分析报告或主张核对清单。",
    "03-06": "可得到研究问题清单、可检验假设和预测。",
    "03-07": "可得到带来源的证据包、调研报告或政策简报。",
    "03-08": "可得到主题阅读清单、文献比较表或综述草稿。",
    "03-09": "可得到检索与筛选记录、纳排清单或系统综述报告。",
    "03-10": "可得到合并后的统计结果数据表和 Meta 分析报告。",
    "03-11": "可得到有证据依据的审查意见和改进清单。",
    "04-01": "可得到信息素养学习方案、练习材料或来源评价清单。",
    "04-02": "可得到来源可信度分析报告和证据清单。",
    "04-03": "可得到媒体素养课程方案、案例分析报告或评价清单。",
    "04-04": "可得到事实核查报告、证据清单和结论说明。",
    "04-05": "可得到数据素养课程方案、练习数据表或评价清单。",
    "04-06": "可得到图书馆服务方案、活动计划或推广清单。",
    "04-07": "可得到数字图书馆建设方案、系统清单或实施计划。",
    "04-08": "可得到来源台账、书目记录或导入配置。",
    "04-09": "可得到馆藏或开放资源检索结果和文献记录。",
    "04-10": "可得到字段规则、术语结果或数据规范清单。",
    "04-11": "可得到开放科学检查清单、数据管理计划或资源记录。",
    "04-12": "可得到同步配置、可检索文献记录或实验记录。",
    "05-01": "可得到计算资源清单和任务运行方案。",
    "05-02": "可得到数据质量报告、问题清单和清理后的数据表。",
    "05-03": "可得到处理后的数据表、转换代码和分析报告。",
    "05-04": "可得到表结构或存储配置、查询代码和性能报告。",
    "05-05": "可得到并行或优化代码和性能测试结果。",
    "05-06": "可得到统计结果数据表、诊断报告和文字结论。",
    "05-07": "可得到统计模型、预测结果和模型诊断报告。",
    "05-08": "可得到贝叶斯或因果分析报告、实验方案和结果数据表。",
    "05-09": "可得到机器学习模型、评估报告和解释图表。",
    "05-10": "可得到深度学习模型、预测结果或受控调整配置。",
    "05-11": "可得到计算结果数据表、公式或误差报告。",
    "05-12": "可得到仿真模型、模拟结果数据表或多目标方案。",
    "05-13": "可得到可由证明软件检查的证明代码和检查结果。",
    "05-14": "可得到科研图表、图表配置和表达审计清单。",
    "05-15": "可得到地图、网络图、流程图或交互图表。",
    "05-16": "可得到面向特定读者的分析报告、图表或行动建议。",
    "05-17": "可得到原因分析报告、修复代码或异常处理方案。",
    "05-18": "可得到测试代码、测试结果和缺陷清单。",
    "05-19": "可得到审查意见、代码规范清单或项目结构方案。",
    "05-20": "可得到数据与模型处理流程、配置和运行检查报告。",
}

# Only exceptions found by the all-record readability audit belong here.  Keeping
# them keyed by Skill ID makes editorial changes reviewable instead of implicit.
PLAIN_OVERRIDES: dict[str, dict[str, str]] = {
    "GH-01-0005": {
        "plain_purpose": "帮助安排论文从形成研究想法、撰写到投稿的全过程。",
    },
    "GH-01-0020": {
        "plain_integration": "基本可以直接放入现有 AI 工作台使用，但仍需按本校制度和工具设置进行检查。具体建议：高校部署时固定采用经过审核的版本，按本地工具调整设置，并默认停用未经审核的自动更新。",
    },
    "GH-02-0001": {
        "plain_prerequisites": "需要由技术人员准备用于处理 Office 文档的 Node.js 或 Python 工具。",
    },
    "GH-02-0002": {
        "plain_prerequisites": "需要由技术人员准备表格处理工具；含公式的文件还要用表格软件重新计算。",
    },
    "GH-02-0003": {
        "plain_prerequisites": "需要由技术人员准备生成 PowerPoint 和检查页面效果的工具。",
    },
    "GH-02-0022": {
        "plain_prerequisites": "需要由技术人员准备用于处理 Word、Excel 和 PowerPoint 的软件；部分问题仍要在 Office 界面中人工修复。",
    },
    "GH-03-0019": {
        "plain_prerequisites": "需要能搜索和读取网页、并行处理多条检索线索的工具。",
    },
    "GH-03-0022": {
        "plain_purpose": "根据检索目标选择不同学术平台，并按步骤逐步扩大或缩小搜索范围。",
    },
    "GH-04-0022": {
        "plain_purpose": "使用 PMC-OAI 批量取得开放论文的基本信息和可用全文地址。",
    },
    "GH-04-0023": {
        "plain_prerequisites": "需要准备对应的数据平台或标准；部分功能还要由技术人员配置 Python、服务授权信息或本地检索目录。",
        "plain_integration": "建议先盘点现状、用少量样本试验，并保持只查看不修改；涉及授权信息、写入或批量修改时需另行审批。",
    },
    "GH-04-0024": {
        "plain_prerequisites": "需要准备对应的数据平台或标准；部分功能还要由技术人员配置 Python、服务授权信息或本地检索目录。",
        "plain_integration": "建议先盘点现状、用少量样本试验，并保持只查看不修改；涉及授权信息、写入或批量修改时需另行审批。",
    },
    "GH-04-0025": {
        "plain_prerequisites": "需要准备对应的数据平台或标准；部分功能还要由技术人员配置 Python、服务授权信息或本地检索目录。",
        "plain_integration": "建议先盘点现状、用少量样本试验，并保持只查看不修改；涉及授权信息、写入或批量修改时需另行审批。",
    },
    "GH-04-0026": {
        "plain_purpose": "把 Zotero 文献分批同步到本地检索库，方便围绕个人馆藏查找资料并生成带出处的回答。",
        "plain_prerequisites": "需要准备对应的数据平台或标准；部分功能还要由技术人员配置 Python、服务授权信息或本地检索目录。",
        "plain_integration": "建议先盘点现状、用少量样本试验，并保持只查看不修改；涉及授权信息、写入或批量修改时需另行审批。",
    },
    "GH-04-0027": {
        "plain_purpose": "在指定标准术语体系内，把自由文本对应到规范术语，并列出无法匹配或含义不清的部分。",
        "plain_prerequisites": "需要准备对应的数据平台或标准；部分功能还要由技术人员配置 Python、服务授权信息或本地检索目录。",
        "plain_integration": "建议先盘点现状、用少量样本试验，并保持只查看不修改；涉及授权信息、写入或批量修改时需另行审批。",
    },
    "GH-04-0028": {
        "plain_purpose": "规划 LabArchives 电子实验记录和库存服务的身份验证、区域地址、资料读取及受控写入。",
        "plain_prerequisites": "需要准备对应的数据平台或标准；部分功能还要由技术人员配置 Python、服务授权信息或本地检索目录。",
        "plain_integration": "建议先盘点现状、用少量样本试验，并保持只查看不修改；涉及授权信息、写入或批量修改时需另行审批。",
    },
    "GH-04-0029": {
        "plain_purpose": "分析网站结构并制作 Zotero 网页翻译器，以改善题名、作者和日期等书目信息的抓取与导入。",
        "plain_prerequisites": "需要准备目标网站、Zotero 以及网站页面结构信息；遇到访问限制时需要人工处理。",
    },
    "GH-05-0003": {
        "plain_purpose": "在一台电脑内存不足或需要加快处理时，用 Dask 把大型数据任务拆开并同时计算。",
    },
    "GH-05-0006": {
        "plain_purpose": "用 Zarr 创建、读取和管理多维数据，可保存在本机或网络存储中。",
    },
    "GH-05-0038": {
        "plain_purpose": "规划机器学习从检查数据、准备特征、训练、评估到发布和持续观察的完整流程。",
    },
    "GH-05-0044": {
        "plain_purpose": "帮助判断程序是否需要在等待期间继续处理其他任务，并正确处理取消、超时和资源释放。",
    },
    "GH-05-0046": {
        "plain_purpose": "按照规定的图形元素，生成数据处理流程图和系统结构图。",
        "plain_prerequisites": "需要准备支持 Markdown、Vega 或 Graphviz 的图形生成工具。",
    },
}

PLAIN_OVERRIDES.update({
    "GH-01-0010": {
        "plain_integration": "先用目标出版要求检查终稿副本，保留人工确认和本地自动文字检查，禁止自动提交出版表单。",
    },
    "GH-01-0014": {
        "plain_outputs": "可得到中文论文各章节草稿、修订稿或逐点审稿回复信。",
    },
    "GH-01-0020": {
        **PLAIN_OVERRIDES["GH-01-0020"],
        "plain_outputs": "可得到材料清单、章节蓝图、论文草稿或重写稿，以及投稿前审计清单。",
    },
    "GH-02-0015": {
        "plain_limitations": "需要注意：转换可能丢失样式或嵌入对象；项目资料库没有提供可直接运行的专用小程序。",
    },
    "GH-03-0019": {
        **PLAIN_OVERRIDES["GH-03-0019"],
        "plain_outputs": "可得到带 APA 引用和证据分级的调研报告、政策简报或主题综述。",
    },
    "GH-04-0029": {
        **PLAIN_OVERRIDES["GH-04-0029"],
        "plain_when_to_use": "当 Zotero 不能从目标网站正确导入题名、作者等书目信息，需要制作或更新网页翻译器时使用。",
        "plain_prerequisites": "需要准备目标网站、能代表不同页面类型的样例网页、预期书目信息和 Zotero 测试环境。",
        "plain_limitations": "需要注意：网站改版、访问限制或反自动访问措施会使翻译器失效；许可证仍需另行核验。",
        "plain_integration": "先为目标网站编写翻译规则和测试记录，用多种样例网页核对导入结果，再决定是否纳入馆内维护。",
        "plain_outputs": "可得到目标网站的 Zotero 网页翻译器代码、书目信息测试结果和维护记录。",
    },
    "GH-05-0001": {
        "plain_when_to_use": "在大型计算任务开跑前，需要判断现有算力、内存和磁盘是否够用时使用。",
        "plain_prerequisites": "需要允许工具查看系统信息，并准备任务规模、预计时长和可使用的设备范围。",
        "plain_limitations": "需要注意：资源快照只代表检查当时，不能保证任务一定完成；不得采集无关的敏感系统信息。",
        "plain_integration": "先以只查看、不修改的方式盘点，把处理器、显卡、内存和磁盘清单交给任务规划环节，不自动修改系统。",
        "plain_outputs": "可得到计算资源清单，以及并行、分块或使用磁盘暂存的任务方案。",
    },
    "GH-05-0002": {
        "plain_when_to_use": "收到一份新数据、尚未决定清理和分析方法，需要先了解质量与分布时使用。",
        "plain_prerequisites": "需要准备已获授权的数据副本、字段说明、研究问题和允许输出的范围。",
        "plain_limitations": "需要注意：探索中发现的关系不等于因果；缺失值和异常值必须结合业务含义判断。",
        "plain_integration": "先对小样本做只查看、不修改的分析，保存每一步数据检查与图表，再由负责人批准清理规则。",
        "plain_outputs": "可得到数据质量报告、描述统计数据表、异常清单和探索图表。",
    },
    "GH-05-0003": {
        **PLAIN_OVERRIDES["GH-05-0003"],
        "plain_when_to_use": "当表格或数组超过一台电脑内存，或计算可拆成多份同时处理时使用。",
        "plain_prerequisites": "需要准备 Dask、Python、输入数据规模说明，以及可用处理器或计算集群信息。",
        "plain_limitations": "需要注意：小任务可能因拆分和协调反而变慢；数据重排成本必须用真实任务测量。",
        "plain_integration": "先在一台电脑上验证分块结果，再按实际规模连接集群，并固定软件版本和分块设置。",
        "plain_outputs": "可得到并行数据处理代码、分块后的数据表和任务执行报告。",
    },
    "GH-05-0004": {
        "plain_when_to_use": "需要加快多列表格筛选、连接和转换，并希望保留可复查步骤时使用。",
        "plain_prerequisites": "需要准备 Polars、字段类型说明、输入样表和期望输出样表。",
        "plain_limitations": "需要注意：延后计算和字段类型规则可能改变执行顺序，结果必须与原处理流程逐列比较。",
        "plain_integration": "先替换一段最慢的表格流程，同时保留原结果作为对照，再逐步扩大使用范围。",
        "plain_outputs": "可得到表格转换代码、处理后的数据表和速度对比报告。",
    },
    "GH-05-0005": {
        "plain_when_to_use": "需要在内存有限的电脑上浏览、筛选或汇总超大表格时使用。",
        "plain_prerequisites": "需要准备 Vaex、受支持的数据文件、字段说明和要计算的统计指标。",
        "plain_limitations": "需要注意：并非所有文件格式和表格操作都受支持；延后计算的速度要用实际文件检验。",
        "plain_integration": "先以不改原文件的方式打开样本，核对筛选和统计结果，再建立固定的导出目录。",
        "plain_outputs": "可得到超大表格的筛选结果数据表、汇总统计和分析报告。",
    },
    "GH-05-0006": {
        **PLAIN_OVERRIDES["GH-05-0006"],
        "plain_when_to_use": "需要把大型多维数组分块保存，并在本机或网络存储中按需读取时使用。",
        "plain_prerequisites": "需要准备 Zarr、数组形状和数据类型、分块方案及目标存储位置。",
        "plain_limitations": "需要注意：分块和压缩设置不合适会拖慢读写；多人写入同一数据时要防止冲突。",
        "plain_integration": "先用一份小数组比较分块大小和压缩效果，确认读取软件兼容后再迁移正式数据。",
        "plain_outputs": "可得到分块存储配置、Zarr 数据文件和读写测试报告。",
    },
    "GH-05-0007": {
        "plain_when_to_use": "需要精确控制二维科研图的坐标轴、标注、布局和导出格式时使用。",
        "plain_prerequisites": "需要准备 Matplotlib、绘图数据、图表尺寸和期刊或课程的版式要求。",
        "plain_limitations": "需要注意：代码能生成图不代表表达正确；颜色、尺度、字体和可读性仍需人工审查。",
        "plain_integration": "先建立本校常用图表样式和导出设置，用代表性数据检查屏幕与打印效果。",
        "plain_outputs": "可得到可重复生成的绘图代码、科研图表和版式检查清单。",
    },
    "GH-05-0008": {
        "plain_when_to_use": "需要快速比较数据分布、变量关系或不同组别，并制作统计图时使用。",
        "plain_prerequisites": "需要准备 Seaborn、整理好的数据表、分组字段和要回答的比较问题。",
        "plain_limitations": "需要注意：默认统计汇总可能掩盖样本差异；图形不能代替统计检验和数据说明。",
        "plain_integration": "先为常用分布图和分组图建立示例，再用 Matplotlib 补充学校要求的标注和导出格式。",
        "plain_outputs": "可得到分布或关系图表、配套绘图代码和图形解释说明。",
    },
    "GH-05-0009": {
        "plain_when_to_use": "准备论文、报告或课程图表，需要检查图形是否诚实、清楚且便于不同读者理解时使用。",
        "plain_prerequisites": "需要准备原始数据、图表草稿、预期读者、传播目的和最终使用载体。",
        "plain_limitations": "需要注意：美观不能替代证据；截断坐标、颜色误导和来源缺失必须单独纠正。",
        "plain_integration": "把图表审计放在发布前，要求每张图保留数据来源、尺度选择和无障碍检查记录。",
        "plain_outputs": "可得到修订后的科研图表、来源说明和图表质量审计清单。",
    },
    "GH-05-0010": {
        "plain_when_to_use": "研究对象之间存在关系，需要计算路径、关键节点、群组或连接结构时使用。",
        "plain_prerequisites": "需要准备 NetworkX、节点与关系数据表，以及每条关系的含义和方向说明。",
        "plain_limitations": "需要注意：中心性或群组结果受网络边界影响，不能脱离数据采集范围解释。",
        "plain_integration": "先用小网络核对节点和关系，再选择与研究问题对应的指标并保存计算参数。",
        "plain_outputs": "可得到网络分析数据表、关键节点清单、关系网络图和计算代码。",
    },
    "GH-05-0011": {
        "plain_when_to_use": "数据带有地点、边界或坐标，需要空间连接、区域统计或地图展示时使用。",
        "plain_prerequisites": "需要准备 GeoPandas、空间数据文件、坐标系说明和有效的地理边界。",
        "plain_limitations": "需要注意：坐标系或几何错误会造成位置偏差；敏感地点数据不得未经处理公开。",
        "plain_integration": "先统一坐标系并检查无效几何，再对少量区域核对空间连接结果后批量处理。",
        "plain_outputs": "可得到清理后的空间数据表、区域统计、地图图表和处理报告。",
    },
    "GH-05-0012": {
        "plain_when_to_use": "需要用结构化数据训练分类或预测模型，并比较多个传统机器学习方法时使用。",
        "plain_prerequisites": "需要准备 Scikit-learn、带目标字段的数据表、训练与验证划分及评价指标。",
        "plain_limitations": "需要注意：数据泄漏和不平衡样本会夸大效果；模型必须在未参与训练的数据上评价。",
        "plain_integration": "把数据预处理、模型训练和验证组成一条可重复流程，保存版本、随机种子和评价结果。",
        "plain_outputs": "可得到机器学习模型、预测结果数据表、评估报告和处理代码。",
    },
    "GH-05-0013": {
        "plain_when_to_use": "面对研究数据但不确定应选哪种统计检验或怎样规范报告结果时使用。",
        "plain_prerequisites": "需要准备研究设计、变量类型、样本量、数据表和需要检验的假设。",
        "plain_limitations": "需要注意：自动推荐不能替代研究设计判断；使用条件不满足时必须改用合适方法。",
        "plain_integration": "先把研究设计和变量说明作为必填输入，再把诊断、效应量和结论一起纳入报告模板。",
        "plain_outputs": "可得到统计方法选择方案、结果数据表、诊断报告和规范文字结论。",
    },
    "GH-05-0014": {
        "plain_when_to_use": "在研究开始前估计样本量，或判断现有样本能否发现目标效应时使用。",
        "plain_prerequisites": "需要准备目标效应、显著性水平、期望把握度、研究设计和预计数据波动。",
        "plain_limitations": "需要注意：样本量取决于输入假设；效应估计过于乐观会低估实际所需样本。",
        "plain_integration": "把样本量计算放进研究设计审批，保存参数来源，并用多个合理假设做敏感性比较。",
        "plain_outputs": "可得到样本量方案、统计功效数据表、敏感性分析图表和计算报告。",
    },
})

PLAIN_OVERRIDES.update({
    "GH-05-0015": {
        "plain_when_to_use": "需要建立回归、广义模型或时间序列模型，并保留严格的统计诊断时使用。",
        "plain_prerequisites": "需要准备 Statsmodels、分析数据表、模型公式、变量说明和推断目标。",
        "plain_limitations": "需要注意：系数显著不代表因果；残差、相关性和模型设定错误会影响结论。",
        "plain_integration": "先固定模型公式与诊断清单，要求每次结果同时保存系数表、置信区间和残差检查。",
        "plain_outputs": "可得到统计模型、系数数据表、诊断图表和推断报告。",
    },
    "GH-05-0016": {
        "plain_when_to_use": "需要用贝叶斯方法结合先前认识与新数据，并表达结论不确定性时使用。",
        "plain_prerequisites": "需要准备 PyMC、观测数据、先验依据、候选模型和需要回答的概率问题。",
        "plain_limitations": "需要注意：先验和模型选择会影响结果；采样没有稳定收敛时不能解释后验结论。",
        "plain_integration": "先用简化模型检查采样与诊断，再记录先验理由、收敛指标和替代模型比较。",
        "plain_outputs": "可得到贝叶斯模型、后验结果数据表、诊断图表和不确定性报告。",
    },
    "GH-05-0017": {
        "plain_when_to_use": "需要保留数学符号精确性来化简表达式、解方程、求导积分或处理矩阵时使用。",
        "plain_prerequisites": "需要准备 SymPy、明确的数学表达式、变量假设和期望的结果形式。",
        "plain_limitations": "需要注意：符号结果可能很复杂；变量范围或假设缺失会得到不适用的解。",
        "plain_integration": "先把变量条件写入计算步骤，对关键结果做代入或数值复核，再导出可读公式。",
        "plain_outputs": "可得到精确公式、方程解数据表、推导代码和核对结果。",
    },
    "GH-05-0018": {
        "plain_when_to_use": "计算涉及物理单位、测量误差或不确定度传播，担心量纲和尺度出错时使用。",
        "plain_prerequisites": "需要准备各数值的单位、不确定度、测量来源和所用计算公式。",
        "plain_limitations": "需要注意：输入单位或误差假设错误会传递到结果；相关误差不能一律按独立处理。",
        "plain_integration": "先统一单位并标记每个测量来源，再把单位检查和误差传播作为计算必经步骤。",
        "plain_outputs": "可得到带单位和不确定度的结果数据表、换算公式和误差报告。",
    },
    "GH-05-0019": {
        "plain_when_to_use": "已有机器学习模型，需要解释单个预测或整体上哪些因素影响结果时使用。",
        "plain_prerequisites": "需要准备 SHAP、已训练模型、用于解释的样本和合适的参考数据。",
        "plain_limitations": "需要注意：因素贡献不等于因果作用；参考数据选取不同会改变解释结果。",
        "plain_integration": "先在少量已知样本上核对解释方向，再分别输出个体与整体结果并记录参考数据。",
        "plain_outputs": "可得到模型解释数据表、因素贡献图表和解释限制报告。",
    },
    "GH-05-0020": {
        "plain_when_to_use": "高维数据难以直接观察，需要压缩到二维或三维来发现群组和异常点时使用。",
        "plain_prerequisites": "需要准备 UMAP、完成标准化的数据表、距离含义和要比较的样本标签。",
        "plain_limitations": "需要注意：二维位置会随设置和随机性变化，图上距离不能被当作精确原始距离。",
        "plain_integration": "先固定随机种子并比较多组邻域设置，只把稳定出现的结构交给后续分析。",
        "plain_outputs": "可得到 UMAP 嵌入坐标数据表、二维图表和设置比较报告。",
    },
    "GH-05-0021": {
        "plain_when_to_use": "有按时间排列的数据，需要快速建立预测基线或在小样本上调整 TimesFM 时使用。",
        "plain_prerequisites": "需要准备连续时间序列、预测区间、TimesFM 对应硬件和明确的软件版本。",
        "plain_limitations": "需要注意：时间间隔、缺失值和版本差异会影响预测；未来数据不得混入训练。",
        "plain_integration": "先做硬件与版本检查，用历史留出区间比较基线，再决定是否进行小样本调整。",
        "plain_outputs": "可得到时间序列预测模型、预测结果数据表和基线评估报告。",
    },
    "GH-05-0022": {
        "plain_when_to_use": "课程或科研已有 MATLAB 或 Octave 代码，需要数值计算、函数实现或绘图时使用。",
        "plain_prerequisites": "需要准备 MATLAB 或 GNU Octave、可用许可证、输入数据和预期数值结果。",
        "plain_limitations": "需要注意：两种软件并非完全兼容；外部命令、文件写入和许可证范围要受控。",
        "plain_integration": "先确认使用哪种软件和许可证，在隔离目录运行示例，并用已知结果核对数值误差。",
        "plain_outputs": "可得到 MATLAB 或 Octave 代码、计算结果数据表和科学图表。",
    },
    "GH-05-0023": {
        "plain_when_to_use": "要模拟排队、服务台、生产流程或资源竞争等随事件变化的系统时使用。",
        "plain_prerequisites": "需要准备 SimPy、事件规则、资源数量、时间分布和要比较的运行方案。",
        "plain_limitations": "需要注意：模拟结果取决于输入分布与边界；单次运行不能代表稳定规律。",
        "plain_integration": "先建立有明确终止条件的小模型，用多次重复运行检查波动，再增加现实细节。",
        "plain_outputs": "可得到离散事件仿真模型、模拟结果数据表和方案比较报告。",
    },
    "GH-05-0024": {
        "plain_when_to_use": "Python 计算已经过慢，怀疑处理器、显卡传输或内存是瓶颈时使用。",
        "plain_prerequisites": "需要准备可重复运行的 Python 任务、性能基线、兼容的 GPU 和候选加速软件。",
        "plain_limitations": "需要注意：把数据搬到显卡也有成本；并非所有任务都会因 GPU 而加速。",
        "plain_integration": "先测量瓶颈，只替换最耗时步骤，并逐阶段比较速度、内存和数值一致性。",
        "plain_outputs": "可得到性能基线报告、GPU 优化代码和分阶段测试结果。",
    },
    "GH-05-0025": {
        "plain_when_to_use": "一个方案同时受成本、效果、时间等多个目标约束，需要比较折中选择时使用。",
        "plain_prerequisites": "需要准备 Pymoo、各项目标和约束、允许范围以及评价一个方案的方法。",
        "plain_limitations": "需要注意：得到的是一组折中方案而非唯一答案；目标定义不当会误导选择。",
        "plain_integration": "先用少量方案验证目标计算，再保存约束、算法设置和最终人工选择理由。",
        "plain_outputs": "可得到多目标优化模型、候选方案数据表、折中图表和选择报告。",
    },
    "GH-05-0026": {
        "plain_when_to_use": "深度学习项目需要统一训练步骤、记录实验并扩展到多块显卡时使用。",
        "plain_prerequisites": "需要准备 PyTorch Lightning、训练与验证数据、模型结构、评价指标和计算设备。",
        "plain_limitations": "需要注意：封装训练流程不能保证模型有效；多设备结果仍受版本和随机性影响。",
        "plain_integration": "先把现有一台电脑上的训练拆成数据、模型和训练配置，验证结果一致后再扩展设备。",
        "plain_outputs": "可得到深度学习训练代码、模型文件、实验配置和评估报告。",
    },
    "GH-05-0027": {
        "plain_when_to_use": "需要加载预训练模型完成文本分类、生成或其他既定任务，并评估是否要调整模型时使用。",
        "plain_prerequisites": "需要准备 Transformers、可信模型来源、任务数据、评价指标和所需账号授权。",
        "plain_limitations": "需要注意：模型版本、授权和数据偏差会影响结果；下载的模型代码必须先审查。",
        "plain_integration": "先锁定模型和软件版本，用小样本评估输出与资源消耗，再决定是否受控调整。",
        "plain_outputs": "可得到预训练模型使用代码、预测结果数据表、受控调整配置和评估报告。",
    },
    "GH-05-0032": {
        "plain_when_to_use": "分析已经完成，但需要把发现讲给管理者、教师或其他特定读者并推动行动时使用。",
        "plain_prerequisites": "需要准备可靠分析结果、目标读者、沟通目的和能够支撑结论的图表。",
        "plain_limitations": "需要注意：故事结构不能掩盖不确定性，也不能把相关关系写成因果结论。",
        "plain_integration": "把背景、冲突、洞察和建议写入报告提纲，并让数据负责人核对每项主张。",
        "plain_outputs": "可得到数据故事提纲、面向受众的分析报告、配套图表和行动建议。",
    },
    "GH-05-0033": {
        "plain_when_to_use": "新建或修改 PostgreSQL 数据表，需要确定字段、约束、索引和访问规则时使用。",
        "plain_prerequisites": "需要准备业务字段说明、数据量、查询方式、保留期限和访问规则。",
        "plain_limitations": "需要注意：表结构变更可能锁表或丢数据；迁移方案必须先备份并验证回退。",
        "plain_integration": "先在测试库建立表结构和样例数据，检查查询与权限后再安排正式迁移。",
        "plain_outputs": "可得到 PostgreSQL 表结构代码、索引与权限配置和迁移方案。",
    },
    "GH-05-0034": {
        "plain_when_to_use": "数据平台频繁出现缺失、重复或口径不一致，需要建立持续质量检查时使用。",
        "plain_prerequisites": "需要准备关键数据表、字段口径、可接受范围、责任人和检查频率。",
        "plain_limitations": "需要注意：质量阈值过严会产生大量误报；规则通过也不代表数据适合所有用途。",
        "plain_integration": "先为少数关键字段建立准确性和完整性规则，再接入告警与责任人处理流程。",
        "plain_outputs": "可得到数据质量规则、自动测试代码、问题清单和监控报告。",
    },
    "GH-05-0035": {
        "plain_when_to_use": "数据库转换项目层次混乱，需要统一 dbt 模型分层、命名、测试和文档时使用。",
        "plain_prerequisites": "需要准备 dbt 项目、数据来源、目标数据表、命名约定和可用数据库连接。",
        "plain_limitations": "需要注意：分层过多会增加维护成本；转换正确性仍要用业务数据和测试确认。",
        "plain_integration": "先选择一条数据链按分层规范改造，补齐字段说明与测试后再推广到其他模型。",
        "plain_outputs": "可得到 dbt 转换代码、分层模型配置、数据测试和项目文档。",
    },
    "GH-05-0036": {
        "plain_when_to_use": "Spark 作业运行缓慢或资源浪费，需要检查分区、数据连接和执行计划时使用。",
        "plain_prerequisites": "需要准备 Spark 作业代码、执行计划、数据规模、集群资源和性能基线。",
        "plain_limitations": "需要注意：一种分区或连接策略不适合所有数据；优化必须在真实规模下复测。",
        "plain_integration": "先记录现有作业时间和资源，再一次只改变一项设置并比较执行计划。",
        "plain_outputs": "可得到 Spark 优化代码、资源配置、执行计划对比和性能报告。",
    },
    "GH-05-0037": {
        "plain_when_to_use": "数据库查询响应过慢，需要找出扫描、连接或过滤环节的问题时使用。",
        "plain_prerequisites": "需要准备 SQL 查询、表结构、索引、执行计划和具有代表性的数据量。",
        "plain_limitations": "需要注意：新增索引会增加写入和存储成本；测试数据过小可能看不出真实效果。",
        "plain_integration": "先在测试环境保存原执行计划，逐项尝试索引或查询改写并核对结果一致。",
        "plain_outputs": "可得到优化后的 SQL 代码、索引方案、执行计划对比和性能测试结果。",
    },
    "GH-05-0038": {
        **PLAIN_OVERRIDES["GH-05-0038"],
        "plain_when_to_use": "机器学习项目从数据准备到发布由多人接力，需要统一步骤和质量检查时使用。",
        "plain_prerequisites": "需要准备数据来源、特征说明、训练代码、评价标准、发布环境和负责人。",
        "plain_limitations": "需要注意：流程自动化不能消除数据漂移或模型失效；每个阶段仍需明确批准条件。",
        "plain_integration": "先把现有项目画成阶段流程，逐步加入数据检查、模型评估和发布记录。",
        "plain_outputs": "可得到机器学习流程图、阶段配置、模型评估报告和发布检查清单。",
    },
    "GH-05-0039": {
        "plain_when_to_use": "Python 项目缺少一致测试，需要覆盖单个函数、组件协作和完整使用流程时使用。",
        "plain_prerequisites": "需要准备待测代码、预期行为、测试数据和项目现有测试工具。",
        "plain_limitations": "需要注意：过度模拟会让测试脱离真实行为；测试通过也不能证明没有遗漏。",
        "plain_integration": "先沿用现有测试目录和运行命令，从关键失败场景开始增加可重复测试。",
        "plain_outputs": "可得到 Python 测试代码、测试数据、覆盖层级清单和测试结果。",
    },
    "GH-05-0040": {
        "plain_when_to_use": "多人维护 Python 项目，需要统一格式、命名、类型说明和代码文档时使用。",
        "plain_prerequisites": "需要准备现有代码、团队命名约定、支持版本和自动检查工具。",
        "plain_limitations": "需要注意：统一格式不能代替清晰设计；一次性改动过多会增加审查困难。",
        "plain_integration": "先确定最小代码规范并对新增代码执行，再分批整理旧代码和补充文档。",
        "plain_outputs": "可得到格式化后的代码、代码规范清单、类型说明和项目文档。",
    },
    "GH-05-0041": {
        "plain_when_to_use": "Python 程序错误信息含糊、失败被忽略或需要在部分失败后安全恢复时使用。",
        "plain_prerequisites": "需要准备会失败的代码路径、真实错误示例、允许恢复的范围和日志要求。",
        "plain_limitations": "需要注意：捕获范围过宽会隐藏真正问题；错误日志不得泄露密码或敏感数据。",
        "plain_integration": "先为关键边界定义明确错误类型和恢复规则，再用失败测试验证日志与清理动作。",
        "plain_outputs": "可得到错误处理代码、恢复方案、日志规则和失败测试结果。",
    },
    "GH-05-0042": {
        "plain_when_to_use": "Python 项目文件混乱、模块互相牵连，导致测试、复用或维护困难时使用。",
        "plain_prerequisites": "需要准备现有目录、模块职责、对外功能、启动方式和部署限制。",
        "plain_limitations": "需要注意：大规模搬动文件可能破坏导入路径；重组不能与功能修改混在一起。",
        "plain_integration": "先画出模块关系并确定公开入口，再小步移动文件，每一步运行原有测试。",
        "plain_outputs": "可得到 Python 项目结构方案、模块关系图、调整后的代码和迁移清单。",
    },
    "GH-05-0043": {
        "plain_when_to_use": "Python 程序耗时或占内存过高，需要确定真正瓶颈后再优化时使用。",
        "plain_prerequisites": "需要准备可重复任务、代表性输入、时间与内存基线和性能分析工具。",
        "plain_limitations": "需要注意：微小样本上的加速可能无实际价值；优化后必须核对输出一致。",
        "plain_integration": "先保存基准结果并定位最耗资源步骤，一次只优化一个瓶颈并重新测量。",
        "plain_outputs": "可得到性能基线报告、瓶颈清单、优化代码和前后测试结果。",
    },
    "GH-05-0044": {
        **PLAIN_OVERRIDES["GH-05-0044"],
        "plain_when_to_use": "Python 程序经常等待网络或文件读写，希望等待期间继续处理其他任务时使用。",
        "plain_prerequisites": "需要准备等待型任务清单、超时要求、取消规则和资源关闭方式。",
        "plain_limitations": "需要注意：异步代码更难排错；遗漏取消和关闭处理会造成任务或连接泄漏。",
        "plain_integration": "先确认任务确实以等待为主，从单一入口改造，并为超时、取消和清理增加测试。",
        "plain_outputs": "可得到异步处理代码、超时与取消配置、资源清理方案和测试结果。",
    },
    "GH-05-0045": {
        "plain_when_to_use": "JavaScript 或 TypeScript 项目需要补齐单元、组件协作或端到端测试时使用。",
        "plain_prerequisites": "需要准备待测网页或程序、预期交互、测试数据，以及 Jest 或 Vitest 环境。",
        "plain_limitations": "需要注意：端到端测试较慢且易受环境影响；模拟对象必须与真实连接方式一致。",
        "plain_integration": "先沿用项目现有测试工具，按单元到端到端分层补充，并固定浏览器和运行版本。",
        "plain_outputs": "可得到 JavaScript 或 TypeScript 测试代码、测试配置和分层测试结果。",
    },
})

JARGON_REPLACEMENTS = {
    "逐页渲染检查": "逐页生成预览并检查",
    "渲染抽查": "生成预览后抽查页面",
    "渲染核验": "生成预览后核对版面",
    "渲染路径": "生成预览的路径",
    "渲染工具": "生成预览的工具",
    "图像渲染": "生成图像预览",
    "可渲染": "可生成图表",
    "专用调用": "专用工具用法",
    "视觉检查门": "必须完成视觉检查",
    "渲染门": "必须完成页面效果检查",
    "路由": "调用安排",
    "编排": "流程安排",
    "脚手架": "项目基础结构",
    "门禁": "必须通过的检查",
    "适配": "调整",
    "端点": "服务地址",
    "凭据": "登录或授权信息",
    "工具链": "配套工具",
    "预检": "使用前检查",
    "渲染器": "图形生成工具",
    "渲染": "生成预览",
    "本地脚本": "本地小程序",
    "版本控制": "修改记录管理",
    "认证": "身份验证",
    "映射": "对应",
    "只读": "仅查看、不修改",
    "写操作": "修改或新增数据",
    "批量变更": "一次修改多项数据",
    "调用": "使用",
    "工作流": "处理流程",
    "调度": "安排",
    "工作负载": "处理任务",
    "单机": "一台电脑",
    "N 维": "多维",
    "管道": "流程",
    "技术栈": "使用的一组技术",
    "验证门": "必须通过的检查",
    "仓库脚本": "项目资料库中的小程序",
    "仓库包含": "项目资料库中包含",
    "同仓库": "同一项目资料库中的",
    "兄弟技能": "配套 AI 技能",
    "子技能": "配套 AI 技能",
    "仓库": "项目资料库",
    "程序化": "通过程序自动",
    "原生工具": "内置工具",
    "数据模型": "数据组织方式",
    "运行时": "运行环境",
    "回写": "把修改写回原处",
    "lint": "自动文字检查",
}

AUDIT_TAIL_MARKERS = (
    "本轮读取了",
    "重点核对了",
    "不能推定成功运行",
    "该结论仅反映说明与包结构",
)

PLACEHOLDER_MARKERS = (
    "TODO",
    "TBD",
    "PLACEHOLDER",
    "待补充",
    "同上",
    "可用于相关工作",
    "满足相关需求",
)

OUTPUT_TYPE_PATTERN = re.compile(
    r"报告|清单|检索结果|文献记录|数据表|图表|方案|计划|草稿|修订稿|"
    r"回复信|代码|配置|模型|预测结果|分析结果|审查意见|证明|演示文稿|"
    r"文档|工作簿|转换文件|术语结果|证据包|流程图|结构图|测试结果|规则"
)

GENERIC_OUTPUT_MARKERS = ("相关结果", "相应成果", "具体形式见", "满足需求")

BANNED_JARGON = tuple(JARGON_REPLACEMENTS)


def _term_pattern(terms: list[str] | tuple[str, ...]) -> re.Pattern:
    alternatives = "|".join(re.escape(term) for term in sorted(terms, key=len, reverse=True))
    return re.compile(rf"(?<![A-Za-z0-9-])(?:{alternatives})(?![A-Za-z0-9-])")


TERM_PATTERN = _term_pattern(tuple(TERM_EXPLANATIONS))


def _object_without_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    """Build JSON objects while preserving duplicate-key evidence."""
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"重复 JSON 键: {key}")
        result[key] = value
    return result


def load_source_records(data_dir: Path) -> list[dict]:
    """Load the five approved source-category files in stable code order."""
    records: list[dict] = []
    for category_code in range(1, 6):
        source_path = data_dir / f"category_{category_code:02d}.json"
        with source_path.open(encoding="utf-8") as source_file:
            payload = json.load(source_file)
        records.extend(payload["records"])
    return records


def load_assignment_file(path: Path) -> dict:
    """Load the standalone, reviewable Skill-ID-to-subcategory ledger."""
    with path.open(encoding="utf-8") as assignment_file:
        return json.load(assignment_file, object_pairs_hook=_object_without_duplicate_keys)


def validate_assignments(records: list[dict], assignment_data: dict) -> None:
    """Reject incomplete, unknown, or cross-big-category assignments."""
    source_ids = {row["id"] for row in records}
    assignments = assignment_data["assignments"]
    taxonomy = {item["code"]: item for item in assignment_data["taxonomy"]}

    if len(source_ids) != len(records):
        raise ValueError("原始数据包含重复 Skill ID")
    if len(taxonomy) != len(assignment_data["taxonomy"]):
        raise ValueError("小分类代码重复")
    if set(assignments) != source_ids:
        missing = sorted(source_ids - set(assignments))
        extra = sorted(set(assignments) - source_ids)
        raise ValueError(f"小分类归属不完整: missing={missing}, extra={extra}")
    for skill_id, subcategory_code in assignments.items():
        if subcategory_code not in taxonomy:
            raise ValueError(f"{skill_id} 使用未知小分类 {subcategory_code}")
        if not skill_id.startswith(f"GH-{subcategory_code[:2]}-"):
            raise ValueError(f"{skill_id} 与 {subcategory_code} 的大分类不一致")


def enrich_with_subcategory(records: list[dict], assignment_data: dict) -> list[dict]:
    """Return copies of source records annotated from a validated ledger."""
    validate_assignments(records, assignment_data)
    taxonomy = {item["code"]: item for item in assignment_data["taxonomy"]}
    decision_notes = assignment_data.get("decision_notes", {})
    enriched_records: list[dict] = []
    for record in records:
        subcategory_code = assignment_data["assignments"][record["id"]]
        enriched_record = {
            **record,
            "subcategory_code": subcategory_code,
            "subcategory_name": taxonomy[subcategory_code]["name"],
        }
        if record["id"] in decision_notes:
            enriched_record["decision_note"] = decision_notes[record["id"]]
        enriched_records.append(enriched_record)
    return enriched_records


def _plain_text(value: object) -> str:
    """Normalize punctuation and replace project jargon without adding claims."""
    text = str(value or "").strip()
    for jargon, replacement in JARGON_REPLACEMENTS.items():
        text = text.replace(jargon, replacement)
    text = re.sub(r"(?i)(?<![A-Za-z])skill(?![A-Za-z])", "AI 技能", text)
    text = text.replace("接口", "连接方式")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"本地\s+自动文字检查", "本地自动文字检查", text)
    return text


def _explain_terms_once(plain_values: dict[str, str]) -> dict[str, str]:
    """Explain each managed technical term at its first appearance in a record."""
    explained: set[str] = set()

    def explain(match: re.Match) -> str:
        term = match.group(0)
        if term in explained:
            return term
        explained.add(term)
        return TERM_EXPLANATIONS[term]

    explained_values: dict[str, str] = {}
    for field in PLAIN_FIELDS:
        value = TERM_PATTERN.sub(explain, plain_values[field])
        value = re.sub(r"）\s+(?=[\u3400-\u9fff])", "）", value)
        value = re.sub(r"AI 技能\s+(?=[\u3400-\u9fff])", "AI 技能", value)
        value = value.replace("图形图形生成工具", "图形生成工具")
        explained_values[field] = value
    return explained_values


def simplify_record(record: dict) -> dict:
    """Add seven concise user-facing fields while preserving every source field."""
    verification = VERIFICATION_TEXT.get(record.get("verify"))
    if verification is None:
        raise ValueError(f"{record.get('id', '<unknown>')} 使用未知核验状态 {record.get('verify')!r}")
    compatibility = COMPATIBILITY_TEXT.get(record.get("compat"))
    if compatibility is None:
        raise ValueError(f"{record.get('id', '<unknown>')} 使用未知兼容等级 {record.get('compat')!r}")

    dependencies = _plain_text(record.get("deps"))
    if dependencies == "无明确外部依赖":
        prerequisites = "通常不需要额外安装其他工具；实际使用前仍应检查本校环境。"
    elif dependencies == "无硬性运行依赖；实施时需要本校资源与受众信息":
        prerequisites = "无需额外安装工具；需要先准备本校资源信息和使用对象需求。"
    else:
        prerequisites = f"需要准备：{dependencies}。" if not dependencies.endswith("。") else f"需要准备：{dependencies}"

    adaptation = _plain_text(record.get("adapt"))
    plain_values = {
        "plain_purpose": _plain_text(record.get("summary")),
        "plain_outputs": OUTPUT_TEXT_BY_SUBCATEGORY[record["subcategory_code"]],
        "plain_audience": f"适合{_plain_text(record.get('roles'))}使用。",
        "plain_when_to_use": f"适用于{_plain_text(record.get('scenario'))}。",
        "plain_prerequisites": prerequisites,
        "plain_limitations": f"需要注意：{_plain_text(record.get('risk'))}",
        "plain_integration": f"{compatibility}具体建议：{adaptation}",
        "plain_verification": verification,
    }
    for field, override in PLAIN_OVERRIDES.get(record.get("id", ""), {}).items():
        if field not in PLAIN_FIELDS:
            raise ValueError(f"{record.get('id')} 的通俗化覆盖字段无效: {field}")
        plain_values[field] = override
    plain_values = _explain_terms_once(plain_values)
    return {**record, **plain_values}


def readability_issues(record: dict) -> list[str]:
    """Return actionable issues for a single derived record."""
    skill_id = str(record.get("id", "<unknown>"))
    issues: list[str] = []
    plain_values: dict[str, str] = {}
    for field in PLAIN_FIELDS:
        value = str(record.get(field, "")).strip()
        plain_values[field] = value
        if not value:
            issues.append(f"{skill_id}:{field}:字段为空")
            continue
        if any(marker in value for marker in PLACEHOLDER_MARKERS):
            issues.append(f"{skill_id}:{field}:占位或空话")
        if any(marker in value for marker in AUDIT_TAIL_MARKERS):
            issues.append(f"{skill_id}:{field}:含技术审计尾句")
        for paragraph in value.splitlines():
            if len(re.findall(r"[\u3400-\u9fff]", paragraph)) > 180:
                issues.append(f"{skill_id}:{field}:单段超过 180 个汉字")
                break
        jargon = sorted(term for term in BANNED_JARGON if term in value)
        if jargon:
            issues.append(f"{skill_id}:{field}:未转换技术措辞 {jargon}")

    seen_terms: set[str] = set()
    for field in PLAIN_FIELDS:
        value = plain_values[field]
        for match in TERM_PATTERN.finditer(value):
            term = match.group(0)
            if term in seen_terms:
                continue
            # Terms used inside another term's parenthetical explanation are
            # explanatory prose, not a new first use in the record body.
            if value.rfind("（", 0, match.start()) > value.rfind("）", 0, match.start()):
                continue
            seen_terms.add(term)
            if not value.startswith(TERM_EXPLANATIONS[term], match.start()):
                issues.append(f"{skill_id}:{field}:未解释缩写或技术词首次出现未解释 {term}")

    output = plain_values["plain_outputs"]
    if output and (
        not OUTPUT_TYPE_PATTERN.search(output)
        or any(marker in output for marker in GENERIC_OUTPUT_MARKERS)
    ):
        issues.append(f"{skill_id}:plain_outputs:缺少具体产出")

    verification = plain_values["plain_verification"]
    overclaims = ("运行成功", "已成功运行", "已经运行", "已经安装", "已证明有效", "确认可用")
    if any(claim in verification for claim in overclaims):
        issues.append(f"{skill_id}:plain_verification:误写核验状态")
    if verification not in VERIFICATION_TEXT.values():
        issues.append(f"{skill_id}:plain_verification:核验说明不受支持")
    return issues


def write_plain_catalog(output_path: Path, records: list[dict]) -> None:
    """Write the audited derived catalog without modifying its source records."""
    plain_records = [simplify_record(record) for record in records]
    issues = [issue for record in plain_records for issue in readability_issues(record)]
    if issues:
        raise ValueError("通俗化审计未通过:\n" + "\n".join(issues))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as output_file:
        json.dump(plain_records, output_file, ensure_ascii=False, indent=2)
        output_file.write("\n")


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    data_dir = project_root / "03_候选池" / "deduplicated"
    assignment_path = project_root / "03_候选池" / "derived" / "subcategory_assignments.json"
    output_path = project_root / "03_候选池" / "derived" / "plain_language_catalog.json"
    records = enrich_with_subcategory(
        load_source_records(data_dir),
        load_assignment_file(assignment_path),
    )
    write_plain_catalog(output_path, records)
    print(
        f"records={len(records)}, "
        f"subcategories={len({row['subcategory_code'] for row in records})}, "
        "readability_issues=0"
    )


if __name__ == "__main__":
    main()
