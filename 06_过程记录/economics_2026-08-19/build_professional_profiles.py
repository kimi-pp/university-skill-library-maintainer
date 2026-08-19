from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ACCESSED_AT = "2026-08-19"

SOURCE_RECORDS = [
    {
        "source_id": "moe_undergraduate_catalog_2026",
        "title": "普通高等学校本科专业目录（2026年）",
        "publisher": "教育部",
        "authority": "教育部",
        "url": "https://www.moe.gov.cn/srcsite/A08/moe_1034/s3882/202604/W020260427440749576927.pdf",
        "accessed_at": ACCESSED_AT,
        "major_codes": [],
        "evidence_use": "确定经济学门类、专业类、专业代码、专业名称及学位门类。",
    },
    {
        "source_id": "moe_economics_quality_standard",
        "title": "普通高等学校本科专业类教学质量国家标准（经济学门类）",
        "publisher": "教育部高等学校教学指导委员会",
        "authority": "教育部",
        "url": "https://jwc.cueb.edu.cn/pgzx/docs/2023-12/882f50ac15434106b120a27f44e3d303.pdf",
        "accessed_at": ACCESSED_AT,
        "major_codes": [],
        "evidence_use": "约束经济学、财政学、金融学、经济与贸易四个专业类的共同理论、方法和能力基础。",
    },
    {
        "source_id": "tsinghua_economics_program",
        "title": "清华大学经济学专业本科培养方案",
        "publisher": "清华大学",
        "authority": "高校官网",
        "url": "https://www.tsinghua.edu.cn/jxjywj/bkzy2023/zxzy/51-1.pdf",
        "accessed_at": ACCESSED_AT,
        "major_codes": [],
        "evidence_use": "用于经济学类共同的微观、宏观、计量与劳动、环境资源等应用经济学内容校准。",
    },
    {
        "source_id": "lzufe_digital_economy_program",
        "title": "数字经济专业本科人才培养方案",
        "publisher": "兰州财经大学",
        "authority": "高校官网",
        "url": "https://economic.lzufe.edu.cn/info/2556/5609.htm",
        "accessed_at": ACCESSED_AT,
        "major_codes": ["020109T"],
        "evidence_use": "限定数字经济专业的数据分析、平台经济、数字化转型和信息技术交叉内容。",
    },
    {
        "source_id": "ucass_low_altitude_economy_program",
        "title": "低空经济与管理专业介绍",
        "publisher": "中国社会科学院大学",
        "authority": "高校官网",
        "url": "https://fae.ucass.edu.cn/info/1021/3968.htm",
        "accessed_at": ACCESSED_AT,
        "major_codes": ["020110TK"],
        "evidence_use": "限定低空经济运行、产业与政策法规、管理、数据处理和风险意识等培养内容。",
    },
    {
        "source_id": "nau_resource_environment_audit_program",
        "title": "资源环境审计专业本科人才培养方案研讨会",
        "publisher": "南京审计大学",
        "authority": "高校官网",
        "url": "https://news.nau.edu.cn/2026/0604/c5797a158413/page.htm",
        "accessed_at": ACCESSED_AT,
        "major_codes": ["020111T"],
        "evidence_use": "限定审计学与资源环境、经济管理、法学、数据科学、地理科学和生态学的交叉边界。",
    },
    {
        "source_id": "zufe_public_finance_tax_programs",
        "title": "财政学、税收学与国际税收专业介绍",
        "publisher": "浙江财经大学",
        "authority": "高校官网",
        "url": "https://cz.zufe.edu.cn/rcpy/bks/zyjs1.htm",
        "accessed_at": ACCESSED_AT,
        "major_codes": ["020201K", "020202", "020203TK"],
        "evidence_use": "区分公共财政、国内税收和跨境税收治理、合规及实务。",
    },
    {
        "source_id": "nufe_finance_programs",
        "title": "金融学院本科培养方案",
        "publisher": "南京财经大学",
        "authority": "高校官网",
        "url": "https://jrxy.nufe.edu.cn/bksjy/pyfa.htm",
        "accessed_at": ACCESSED_AT,
        "major_codes": [],
        "evidence_use": "用于金融学类共同基础及金融工程、保险等专业差异校准。",
    },
    {
        "source_id": "pku_financial_mathematics_program",
        "title": "金融数学系本科生培养方案",
        "publisher": "北京大学",
        "authority": "高校官网",
        "url": "https://www.math.pku.edu.cn/finance/jxgz/pyfa/117222.htm",
        "accessed_at": ACCESSED_AT,
        "major_codes": ["020305T", "020308T"],
        "evidence_use": "限定金融数学与精算中的概率、随机过程、金融时间序列、寿险精算和衍生证券内容。",
    },
    {
        "source_id": "ahut_internet_finance_program",
        "title": "互联网金融本科指导性培养方案（2023版）",
        "publisher": "安徽工业大学",
        "authority": "高校官网",
        "url": "https://jwc.ahut.edu.cn/__local/B/52/79/0B84148CA72E14EA6456BAB3A4C_1209671A_24A8F.pdf",
        "accessed_at": ACCESSED_AT,
        "major_codes": ["020309T"],
        "evidence_use": "限定互联网金融业务、平台运营、大数据金融、支付结算、风险管理和监管内容。",
    },
    {
        "source_id": "bit_fintech_program",
        "title": "金融科技专业培养方案（2024版）",
        "publisher": "北京理工大学",
        "authority": "高校官网",
        "url": "https://jwb.bit.edu.cn/docs/2026-03/b8af4e36bbce45a990ec3d04c3710f3c.pdf",
        "accessed_at": ACCESSED_AT,
        "major_codes": ["020310T"],
        "evidence_use": "限定金融理论、Python、大数据、人工智能与金融应用的交叉培养内容。",
    },
    {
        "source_id": "nau_financial_audit_program",
        "title": "金融工程（金融审计方向）专业介绍",
        "publisher": "南京审计大学",
        "authority": "高校官网",
        "url": "https://skema.nau.edu.cn/jrgcwjrsjfxw/list.htm",
        "accessed_at": ACCESSED_AT,
        "major_codes": ["020311TK"],
        "evidence_use": "限定金融学、金融工程、金融法规、风险和审计方法的复合边界。",
    },
    {
        "source_id": "pku_digital_finance_program",
        "title": "北京大学数智金融项目培养方案",
        "publisher": "北京大学",
        "authority": "高校官网",
        "url": "https://www.gsm.pku.edu.cn/undergraduate/info/1166/7567.htm",
        "accessed_at": ACCESSED_AT,
        "major_codes": ["020312TK"],
        "evidence_use": "限定数字金融中的金融、经济、人工智能、大数据和云计算交叉应用。",
    },
    {
        "source_id": "zju_international_trade_program",
        "title": "国际经济与贸易专业介绍",
        "publisher": "浙江大学",
        "authority": "高校官网",
        "url": "https://zdzsc.zju.edu.cn/2023/0623/c87426a2775174/page.htm",
        "accessed_at": ACCESSED_AT,
        "major_codes": ["020401", "020402"],
        "evidence_use": "限定国际贸易理论、政策、实务、国际商法、数字贸易与跨文化能力。",
    },
    {
        "source_id": "sdufe_development_cooperation_program",
        "title": "国际经济发展合作专业培养方案",
        "publisher": "山东财经大学",
        "authority": "高校官网",
        "url": "https://site.sdufe.edu.cn/info/1044/2171.htm",
        "accessed_at": ACCESSED_AT,
        "major_codes": ["020403T"],
        "evidence_use": "限定发展经济学、国际组织、发展援助和国际合作项目的培养内容。",
    },
    {
        "source_id": "btbu_digital_trade_program",
        "title": "贸易经济（数字贸易方向）专业介绍",
        "publisher": "北京工商大学",
        "authority": "高校官网",
        "url": "https://zsb.btbu.edu.cn/bkzn/zyjj/jjxy1/0806e3b4c01a420a8959e199d080b432.htm",
        "accessed_at": ACCESSED_AT,
        "major_codes": ["020404TK"],
        "evidence_use": "限定数字贸易规则、数字服务、平台、供应链、跨境业务和数据分析内容。",
    },
]


CLASS_ANCHOR = {
    "0201": "tsinghua_economics_program",
    "0202": "zufe_public_finance_tax_programs",
    "0203": "nufe_finance_programs",
    "0204": "zju_international_trade_program",
}

SPECIAL_SOURCES = {
    "020109T": ["lzufe_digital_economy_program"],
    "020110TK": ["ucass_low_altitude_economy_program"],
    "020111T": ["nau_resource_environment_audit_program"],
    "020203TK": ["zufe_public_finance_tax_programs"],
    "020305T": ["pku_financial_mathematics_program"],
    "020308T": ["pku_financial_mathematics_program"],
    "020309T": ["ahut_internet_finance_program"],
    "020310T": ["bit_fintech_program"],
    "020311TK": ["nau_financial_audit_program"],
    "020312TK": ["pku_digital_finance_program"],
    "020403T": ["sdufe_development_cooperation_program"],
    "020404TK": ["btbu_digital_trade_program"],
}


def p(domains, tasks, include, exclude, zh, en):
    return {
        "core_learning_domains": domains,
        "typical_tasks": tasks,
        "inclusion_rules": include,
        "exclusion_boundaries": exclude,
        "search_terms": {"zh": zh, "en": en},
    }


PROFILE_DEFINITIONS = {
    "020101": p(
        ["微观经济学与宏观经济学", "计量经济学与因果推断", "经济政策与制度分析"],
        ["建立并检验经济模型", "分析宏观与微观经济数据", "评估经济政策和制度效果"],
        ["直接支持经济模型、经济数据或政策分析", "方法能用于实证经济研究或经济预测"],
        ["仅做泛财经资讯摘要", "仅做企业文案、销售或通用办公"],
        ["经济学分析", "计量经济学", "因果推断", "经济政策评估"],
        ["economics analysis", "econometrics", "causal inference", "economic policy evaluation"],
    ),
    "020102": p(
        ["概率统计与抽样调查", "国民经济核算与经济指标", "经济计量与数据建模"],
        ["清洗和汇总经济统计数据", "构造经济指标与统计报表", "完成回归、预测和统计推断"],
        ["直接处理经济统计数据或指标", "提供可复核的统计建模、抽样或预测能力"],
        ["只生成图表而不含统计分析", "面向自然科学实验且不能迁移到经济数据"],
        ["经济统计", "国民经济核算", "抽样调查", "经济预测"],
        ["economic statistics", "national accounts", "survey sampling", "economic forecasting"],
    ),
    "020103T": p(
        ["宏观经济运行与调控", "国民经济核算与规划", "产业、区域与发展政策"],
        ["监测国民经济运行", "编制发展规划与情景方案", "评估产业和区域政策"],
        ["直接服务宏观监测、规划或政策模拟", "能将多部门经济数据组织为决策依据"],
        ["企业内部的一般项目管理", "只做新闻汇编而不支持经济决策"],
        ["国民经济管理", "宏观经济监测", "经济规划", "政策模拟"],
        ["national economic management", "macroeconomic monitoring", "economic planning", "policy simulation"],
    ),
    "020104T": p(
        ["资源与环境经济学", "外部性、公共品与环境政策", "自然资源价值核算与成本收益分析"],
        ["评估环境政策经济影响", "开展资源环境价值核算", "分析碳市场、能源与生态治理机制"],
        ["经济学方法必须直接作用于资源环境问题", "支持估值、政策评估或资源配置"],
        ["仅做环境科普或污染监测", "纯生态建模但没有经济决策或估值环节"],
        ["资源环境经济学", "环境估值", "碳市场分析", "环境政策评估"],
        ["environmental economics", "environmental valuation", "carbon market analysis", "environmental policy evaluation"],
    ),
    "020105T": p(
        ["管理经济学与企业决策", "需求、定价与市场结构", "产业竞争与商业数据分析"],
        ["预测市场需求", "分析价格与竞争策略", "评估企业经营方案的经济效果"],
        ["直接支持企业经济决策或市场结构分析", "包含需求、成本、定价或竞争的量化依据"],
        ["纯营销文案与社媒运营", "通用商业计划模板而无经济分析"],
        ["商务经济学", "管理经济学", "需求预测", "定价分析"],
        ["business economics", "managerial economics", "demand forecasting", "pricing analysis"],
    ),
    "020106T": p(
        ["能源市场与能源政策", "能源需求、价格与投资经济", "碳约束和能源转型经济学"],
        ["预测能源需求与价格", "评估能源项目经济性", "分析能源政策和转型路径"],
        ["能源对象与经济分析必须同时存在", "支持能源市场、政策、投资或碳约束决策"],
        ["纯电力工程仿真", "泛ESG文案或能源新闻聚合"],
        ["能源经济", "能源市场", "能源项目经济评价", "能源转型"],
        ["energy economics", "energy markets", "energy project appraisal", "energy transition"],
    ),
    "020107T": p(
        ["劳动市场与就业理论", "工资、收入分配与人力资本", "劳动微观计量与社会保障"],
        ["分析就业和工资数据", "评估劳动与社会保障政策", "研究人力资本和劳动力流动"],
        ["直接处理劳动市场、工资或就业政策", "采用经济学或计量方法而非仅人事流程"],
        ["通用招聘筛选或绩效管理", "劳动法文本问答但无劳动经济分析"],
        ["劳动经济学", "就业分析", "工资差距", "人力资本"],
        ["labor economics", "employment analysis", "wage inequality", "human capital"],
    ),
    "020108T": p(
        ["数量经济与系统分析", "运筹优化与决策科学", "工程项目经济与资源配置"],
        ["建立经济系统仿真模型", "优化资源配置与项目组合", "开展技术经济和项目评价"],
        ["必须把优化、系统或工程方法用于经济决策", "支持资源配置、项目评价或复杂决策"],
        ["纯机械、土木或软件工程设计", "只有通用项目管理而无经济模型"],
        ["经济工程", "数量经济", "运筹优化", "技术经济评价"],
        ["economic engineering", "quantitative economics", "operations research", "engineering economy"],
    ),
    "020109T": p(
        ["平台经济、网络效应与数据要素", "数字产业与产业数字化", "数字经济测度与实证分析"],
        ["测度数字经济发展", "分析平台市场和网络效应", "评估企业或产业数字化转型"],
        ["经济机制与数字技术场景必须同时存在", "支持数字经济测度、平台分析或转型决策"],
        ["纯软件开发或通用数据工程", "仅做电商营销和内容生成"],
        ["数字经济", "平台经济", "数据要素", "产业数字化"],
        ["digital economy", "platform economics", "data as a factor", "industrial digitalization"],
    ),
    "020110TK": p(
        ["低空产业经济与商业模式", "低空运行管理与政策法规", "安全风险、基础设施与数据决策"],
        ["分析低空产业链与市场规模", "评估低空运营和基础设施方案", "研究空域政策、合规和风险管理"],
        ["必须直接作用于低空经济运行或管理", "经济管理内容须与航空、空域或低空产业对象绑定"],
        ["无人机飞控或航模制作本身", "航空新闻、旅游宣传或泛商业策划"],
        ["低空经济", "低空运营管理", "低空产业规划", "空域政策"],
        ["low-altitude economy", "low-altitude operations", "low-altitude industry planning", "airspace policy"],
    ),
    "020111T": p(
        ["资源环境审计理论与方法", "自然资源资产与环境绩效核算", "生态环境法规、数据和审计证据"],
        ["核验资源环境数据和审计证据", "开展自然资源资产或环境绩效审计", "识别生态环境合规与政策执行风险"],
        ["审计方法必须与资源环境对象直接结合", "支持证据核验、绩效评价或责任认定"],
        ["普通会计记账或通用财务审计", "单纯环境监测、GIS制图或环保宣传"],
        ["资源环境审计", "自然资源资产审计", "环境绩效审计", "生态审计数据"],
        ["environmental audit", "natural resource asset audit", "environmental performance audit", "ecological audit data"],
    ),
    "020201K": p(
        ["公共经济学与财政理论", "政府预算、支出与绩效", "财政政策、政府债务与财政关系"],
        ["分析财政收支和预算数据", "评估公共支出绩效", "模拟财政政策和政府债务影响"],
        ["直接服务政府财政、预算或公共支出决策", "支持财政政策、债务或绩效的可复核分析"],
        ["企业财务会计和报销流程", "泛公共管理文案而无财政数据"],
        ["财政学", "政府预算", "财政政策", "公共支出绩效"],
        ["public finance", "government budgeting", "fiscal policy", "public expenditure performance"],
    ),
    "020202": p(
        ["税收理论与中国税制", "税法、税务会计与征管", "税收合规、筹划与风险管理"],
        ["计算和复核涉税事项", "分析税收政策影响", "识别企业税务合规与风险"],
        ["直接处理税制、税务数据或合规规则", "输出须可追溯到具体税种、规则或业务事实"],
        ["普通财务记账而无涉税事项", "无来源的自动报税或规避监管建议"],
        ["税收学", "中国税制", "税务合规", "税收政策分析"],
        ["taxation", "China tax system", "tax compliance", "tax policy analysis"],
    ),
    "020203TK": p(
        ["国际税收规则与税收协定", "跨境税务、转让定价与反避税", "数字经济税收与全球税收治理"],
        ["分析税收协定适用", "开展跨境税务合规和转让定价分析", "评估BEPS及全球最低税规则影响"],
        ["必须直接服务跨境税收规则或业务", "支持协定、转让定价、反避税或全球治理分析"],
        ["国内单一税种计算且无跨境要素", "无合规依据的避税方案生成"],
        ["国际税收", "税收协定", "转让定价", "BEPS"],
        ["international taxation", "tax treaties", "transfer pricing", "BEPS"],
    ),
    "020301K": p(
        ["货币金融与金融机构", "金融市场、公司金融与投资", "金融风险、监管与数据分析"],
        ["分析利率、市场和金融机构数据", "评估融资与资产配置方案", "识别信用、市场与流动性风险"],
        ["直接服务金融市场、机构、融资或风险分析", "具备金融数据、模型或业务规则支撑"],
        ["泛财经新闻或荐股文案", "仅做个人记账、报销或营销"],
        ["金融学", "金融市场分析", "公司金融", "金融风险"],
        ["finance", "financial market analysis", "corporate finance", "financial risk"],
    ),
    "020302": p(
        ["衍生品定价与资产定价", "随机过程、数值方法与金融计算", "对冲、组合与量化风险管理"],
        ["定价期权和衍生工具", "构建对冲与组合优化模型", "计算VaR及压力情景"],
        ["必须包含金融产品的数学建模或风险量化", "方法须支持定价、对冲或组合决策"],
        ["纯软件工程或一般机器学习", "只做交易观点生成而无模型与验证"],
        ["金融工程", "衍生品定价", "组合优化", "量化风险"],
        ["financial engineering", "derivatives pricing", "portfolio optimization", "quantitative risk"],
    ),
    "020303": p(
        ["保险原理与风险管理", "寿险、非寿险与再保险", "核保、理赔、产品和保险监管"],
        ["设计和分析保险产品", "辅助核保、理赔与风险分类", "评估保险经营和监管数据"],
        ["直接服务保险产品、经营或风险转移", "使用保险规则、保单、赔付或风险数据"],
        ["普通合同摘要或客服机器人", "泛金融工具而无保险业务对象"],
        ["保险学", "核保理赔", "保险产品", "保险风险管理"],
        ["insurance", "underwriting and claims", "insurance products", "insurance risk management"],
    ),
    "020304": p(
        ["证券估值与投资分析", "资产配置与投资组合", "公司价值、另类投资与绩效评价"],
        ["开展证券和公司估值", "构建并回测投资组合", "分析投资绩效、风险和归因"],
        ["直接支持资产估值、配置或绩效分析", "必须提供数据、模型或可核验分析过程"],
        ["只生成荐股、喊单或收益承诺", "泛理财内容营销"],
        ["投资学", "证券估值", "资产配置", "投资组合绩效"],
        ["investment analysis", "security valuation", "asset allocation", "portfolio performance"],
    ),
    "020305T": p(
        ["概率、随机过程与金融数学", "资产定价和衍生证券", "金融时间序列与数值计算"],
        ["推导和计算金融模型", "模拟随机价格和利率过程", "分析金融时间序列和定价误差"],
        ["数学方法必须直接用于金融问题", "支持定价、随机建模或金融计算"],
        ["一般数学解题器而无金融应用", "泛财经写作和市场资讯摘要"],
        ["金融数学", "随机过程", "资产定价", "金融时间序列"],
        ["financial mathematics", "stochastic processes", "asset pricing", "financial time series"],
    ),
    "020306T": p(
        ["信用信息、评级与征信", "信用风险计量与评分", "信用政策、合规和不良资产管理"],
        ["构建信用评分和评级模型", "分析企业或个人信用报告", "监测违约、授信与组合信用风险"],
        ["直接处理信用主体、信用数据或授信风险", "支持评级、评分、征信或信用政策"],
        ["社交信誉打分或不透明的人格判断", "普通客户关系管理与催收话术"],
        ["信用管理", "信用评分", "征信分析", "违约风险"],
        ["credit management", "credit scoring", "credit reporting", "default risk"],
    ),
    "020307T": p(
        ["经济学理论与宏观分析", "货币金融、金融市场与机构", "计量经济与经济金融预测"],
        ["联动分析宏观经济和金融市场", "预测经济金融指标", "评估货币、金融与产业政策"],
        ["经济与金融两个维度均有实质支撑", "用于宏观金融、政策或经济金融数据分析"],
        ["仅覆盖企业财务或个人理财", "泛经济新闻摘要而无模型或政策分析"],
        ["经济与金融", "宏观金融", "经济金融预测", "货币政策分析"],
        ["economics and finance", "macro-finance", "economic and financial forecasting", "monetary policy analysis"],
    ),
    "020308T": p(
        ["概率统计、风险模型与生存分析", "寿险与年金精算", "非寿险精算、准备金与偿付能力"],
        ["计算保费、准备金和年金", "建立损失分布与风险模型", "开展经验分析、偿付能力和精算评估"],
        ["必须直接支持精算定价、准备金或风险模型", "包含概率统计、生命表、损失或生存数据"],
        ["泛财经写作、荐股或一般金融资讯", "仅做保险客服、营销或合同摘要"],
        ["精算学", "寿险精算", "非寿险精算", "风险模型"],
        ["actuarial science", "life contingencies", "non-life actuarial", "actuarial risk models"],
    ),
    "020309T": p(
        ["互联网金融模式与平台经济", "数字支付、网络借贷与平台运营", "大数据风控、监管与消费者保护"],
        ["分析互联网金融交易与用户风险", "评估支付、借贷或平台业务模式", "监测互联网金融合规和运营指标"],
        ["金融业务对象与互联网平台机制必须同时存在", "支持支付、借贷、平台运营或数字风控"],
        ["普通电商运营或社媒营销", "纯网站开发和支付接口接入"],
        ["互联网金融", "数字支付", "网络借贷", "互联网金融风控"],
        ["internet finance", "digital payments", "online lending", "internet financial risk"],
    ),
    "020310T": p(
        ["金融理论与金融业务", "Python、机器学习与金融大数据", "区块链、智能风控与监管科技"],
        ["开发金融数据分析和风控模型", "分析量化投资或智能投顾", "评估支付、区块链和监管科技应用"],
        ["技术必须直接作用于金融场景", "支持金融数据、产品、风险或监管的可复核实现"],
        ["通用AI或区块链开发而无金融任务", "只做金融营销内容和资讯问答"],
        ["金融科技", "金融机器学习", "智能风控", "监管科技"],
        ["fintech", "machine learning in finance", "intelligent risk control", "regtech"],
    ),
    "020311TK": p(
        ["金融学、会计与审计理论", "金融机构内部控制与风险", "银行、证券、保险及金融大数据审计"],
        ["执行金融机构审计程序", "分析金融业务内部控制和风险", "利用数据识别金融审计异常与证据"],
        ["审计对象必须是金融机构、业务或监管活动", "支持审计证据、控制测试或金融风险核验"],
        ["普通财务审计或会计记账", "纯金融预测、交易或荐股工具"],
        ["金融审计", "商业银行审计", "金融内部控制", "金融大数据审计"],
        ["financial audit", "bank audit", "financial internal control", "financial data audit"],
    ),
    "020312TK": p(
        ["数字金融基础设施与业务", "金融数据、人工智能与云计算", "数字普惠金融、智能风控与数字监管"],
        ["设计和评估数字金融产品", "分析数字金融数据和用户风险", "研究数字支付、普惠金融和监管机制"],
        ["数字技术与金融业务必须形成闭环", "支持数字产品、数据决策、风控或监管"],
        ["纯软件、云平台或通用数据工具", "互联网营销和泛金融内容生成"],
        ["数字金融", "数智金融", "数字普惠金融", "数字金融风控"],
        ["digital finance", "intelligent finance", "digital financial inclusion", "digital finance risk"],
    ),
    "020401": p(
        ["国际经济学与国际贸易理论", "贸易政策、WTO规则与国际商法", "国际贸易实务、结算、物流与跨境电商"],
        ["分析国际贸易数据和市场准入", "处理贸易合同、结算与单证", "评估贸易政策、关税和供应链影响"],
        ["直接服务跨境贸易理论、政策或实务", "涉及贸易规则、交易、结算、物流或国际市场"],
        ["国内电商营销和通用商务文案", "仅翻译文本而无国际经贸任务"],
        ["国际经济与贸易", "国际贸易分析", "贸易政策", "跨境贸易实务"],
        ["international economics and trade", "international trade analysis", "trade policy", "cross-border trade operations"],
    ),
    "020402": p(
        ["流通经济、产业与市场组织", "批发零售、商业模式与消费市场", "供应链、物流与商品流通"],
        ["分析流通渠道和零售数据", "优化商品供应链与商业网络", "评估消费市场和商业模式"],
        ["直接服务商品流通、批零市场或供应链经济", "支持渠道、零售、物流或商业组织分析"],
        ["泛企业管理和营销文案", "纯仓储软件或物流路径算法而无贸易经济决策"],
        ["贸易经济", "流通经济", "零售分析", "商业供应链"],
        ["trade economics", "circulation economics", "retail analytics", "commercial supply chain"],
    ),
    "020403T": p(
        ["发展经济学与国际发展理论", "国际组织、发展援助与合作政策", "发展项目评价、融资与国别风险"],
        ["设计和评估国际发展合作项目", "监测援助项目绩效和资金", "开展国别、贫困与可持续发展分析"],
        ["必须直接服务国际发展或合作项目", "支持项目评价、援助管理、发展融资或国别分析"],
        ["一般国际商务或外贸营销", "公益宣传、翻译或旅行规划"],
        ["国际经济发展合作", "发展援助", "发展项目评价", "国别风险"],
        ["international development cooperation", "development aid", "development project evaluation", "country risk"],
    ),
    "020404TK": p(
        ["数字贸易理论、测度与国际规则", "跨境电商、数字服务与平台贸易", "跨境数据流、数字支付和智慧供应链"],
        ["分析数字贸易规模、结构和规则", "评估跨境平台与数字服务业务", "研究数据跨境、数字支付与供应链合规"],
        ["必须直接服务跨境数字交易、规则或基础设施", "支持数字贸易测度、平台、数据流或供应链决策"],
        ["普通电商文案、直播脚本或国内店铺运营", "泛AI工具、网站开发或数字营销"],
        ["数字贸易", "跨境电商分析", "跨境数据流", "数字贸易规则"],
        ["digital trade", "cross-border e-commerce analytics", "cross-border data flows", "digital trade rules"],
    ),
}


def _load_scope(scope_path: Path) -> dict[str, Any]:
    return json.loads(scope_path.read_text(encoding="utf-8"))


def _major_rows(scope: dict[str, Any]) -> list[dict[str, Any]]:
    return [major for class_row in scope["classes"] for major in class_row["majors"]]


def _materialize_sources(scope: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [dict(row) for row in SOURCE_RECORDS]
    all_codes = [major["major_code"] for major in _major_rows(scope)]
    class_codes: dict[str, list[str]] = {}
    for major in _major_rows(scope):
        class_codes.setdefault(major["class_code"], []).append(major["major_code"])

    by_id = {row["source_id"]: row for row in rows}
    by_id["moe_undergraduate_catalog_2026"]["major_codes"] = all_codes
    by_id["moe_economics_quality_standard"]["major_codes"] = all_codes
    by_id["tsinghua_economics_program"]["major_codes"] = class_codes["0201"]
    by_id["nufe_finance_programs"]["major_codes"] = class_codes["0203"]
    return rows


def _build_payload(scope: dict[str, Any]) -> dict[str, Any]:
    profiles = []
    for major in _major_rows(scope):
        code = major["major_code"]
        definition = PROFILE_DEFINITIONS[code]
        source_ids = [
            "moe_undergraduate_catalog_2026",
            "moe_economics_quality_standard",
            CLASS_ANCHOR[major["class_code"]],
            *SPECIAL_SOURCES.get(code, []),
        ]
        profiles.append(
            {
                "major_code": code,
                "major_name": major["major_name"],
                "class_code": major["class_code"],
                "class_name": major["class_name"],
                "degree_categories": major["degree_categories"],
                "attributes": major["attributes"],
                **definition,
                "source_ids": list(dict.fromkeys(source_ids)),
            }
        )
    return {
        "schema_version": "1.0",
        "review_date": ACCESSED_AT,
        "category_code": scope["category_code"],
        "category_name": scope["category_name"],
        "method": "先依据教育部目录确定专业身份，再用专业类质量标准和高校官方培养方案界定学习内容。名称和关键词只用于发现；正式归属必须由核心学习领域、典型任务或直接培养能力支撑。",
        "profile_count": len(profiles),
        "profiles": profiles,
    }


def _ledger_text(sources: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in sources)


def build_profiles(scope_path: Path, output_path: Path, ledger_path: Path) -> None:
    scope = _load_scope(scope_path)
    payload = _build_payload(scope)
    sources = _materialize_sources(scope)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ledger_path.write_text(_ledger_text(sources), encoding="utf-8")


def validate_checked_in_outputs(scope_path: Path, output_path: Path, ledger_path: Path) -> list[str]:
    errors: list[str] = []
    scope = _load_scope(scope_path)
    expected_payload = _build_payload(scope)
    expected_ledger = _ledger_text(_materialize_sources(scope))
    try:
        actual_payload = json.loads(output_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"professional_profiles.json不可读: {exc}")
    else:
        if actual_payload != expected_payload:
            errors.append("professional_profiles.json与构建器输出不一致")
    try:
        actual_ledger = ledger_path.read_text(encoding="utf-8")
    except Exception as exc:
        errors.append(f"profile_source_ledger.jsonl不可读: {exc}")
    else:
        if actual_ledger != expected_ledger:
            errors.append("profile_source_ledger.jsonl与构建器输出不一致")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="构建经济学门类30个专业的学习内容画像")
    parser.add_argument("--scope", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    args = parser.parse_args()
    build_profiles(args.scope, args.output, args.ledger)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
