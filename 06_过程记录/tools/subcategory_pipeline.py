"""Validate the source ledger and build a plain-language derived catalog."""

import json
import re
from pathlib import Path


PLAIN_FIELDS = (
    "plain_purpose",
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
    "Jest": "Jest（检查 JavaScript 程序的测试工具）",
    "Vitest": "Vitest（检查 JavaScript 程序的测试工具）",
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
    "嵌入": "嵌入（把复杂数据转成便于比较的一组数字）",
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
        "plain_audience": f"适合{_plain_text(record.get('roles'))}使用。",
        "plain_when_to_use": f"适用于{_plain_text(record.get('scenario'))}。",
        "plain_prerequisites": prerequisites,
        "plain_limitations": f"需要注意：{_plain_text(record.get('risk'))}",
        "plain_integration": f"{compatibility} 具体建议：{adaptation}",
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

    joined = " ".join(plain_values.values())
    unexplained = [
        term
        for term, explanation in TERM_EXPLANATIONS.items()
        if _term_pattern((term,)).search(joined) and explanation not in joined
    ]
    if unexplained:
        issues.append(f"{skill_id}:未解释缩写 {sorted(unexplained)}")

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
