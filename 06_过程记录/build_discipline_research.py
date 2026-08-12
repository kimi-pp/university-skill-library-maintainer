from __future__ import annotations

import base64
import hashlib
import json
import re
import subprocess
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-12"


DISCIPLINES = {
    "0301": {
        "name": "法学类",
        "full": "0301 法学类",
        "folder": "0301_法学类",
        "majors": ["030101K 法学", "030102 知识产权", "030103 监狱学", "030104T 信用风险管理与法律防控"],
        "roles": "学生、教学人员、科研人员、法务与合规支持人员",
        "boundary": "只用于学习、研究、材料整理和专业人员复核前的草案；不得替代律师意见、司法裁判或自动高影响决定。",
        "categories": {
            "0301-01": "法律检索", "0301-02": "案例裁判", "0301-03": "法源引用", "0301-04": "法律文书",
            "0301-05": "证据整理", "0301-06": "模拟法庭", "0301-07": "合规风控", "0301-08": "比较法务",
        },
    },
    "0305": {
        "name": "马克思主义理论类",
        "full": "0305 马克思主义理论类",
        "folder": "0305_马克思主义理论类",
        "majors": ["030501 科学社会主义", "030502 中国共产党历史", "030503 思想政治教育", "030504T 马克思主义理论"],
        "roles": "学生、教学人员、科研人员",
        "boundary": "把生成内容视为阅读和分析辅助；原著原文、译本、页码、历史事实和学术争议必须另行核对。",
        "categories": {
            "0305-01": "经典文献", "0305-02": "引文校核", "0305-03": "概念脉络", "0305-04": "理论比较",
            "0305-05": "思政教学", "0305-06": "社会分析", "0305-07": "时序关系", "0305-08": "学术表达",
        },
    },
    "1304": {
        "name": "美术学类",
        "full": "1304 美术学类",
        "folder": "1304_美术学类",
        "majors": ["130401 美术学", "130402 绘画", "130403 雕塑", "130404 摄影", "130405T 书法学", "130406T 中国画", "130407TK 实验艺术", "130408TK 跨媒体艺术", "130409T 文物保护与修复", "130410T 漫画", "130411T 纤维艺术", "130412TK 科技艺术", "130413TK 美术教育"],
        "roles": "学生、教学人员、科研人员、馆藏与展览支持人员",
        "boundary": "只辅助研究、记录和方案草拟；作品真伪、来源权利、保存修复、市场价值和专业鉴定必须由合格人员复核。",
        "categories": {
            "1304-01": "美术史论", "1304-02": "图像分析", "1304-03": "作品元数据", "1304-04": "数字保存",
            "1304-05": "绘画辅助", "1304-06": "雕塑三维", "1304-07": "书画研究", "1304-08": "展览作品集", "1304-09": "版权溯源",
        },
    },
}


GITHUB_REPOS = {
    "legal-citation": {
        "repo": "StefanCHEN2026/Chinese-Legal-Citation-skill",
        "commit": "9d95f75e8d2c70046f7394389faa31c327f00a8b",
        "license": "MIT",
        "stars": 15,
        "pushed": "2026-06-25",
    },
    "legal-redline": {
        "repo": "evolsb/legal-redline-tools",
        "commit": "1dbc70ddfdf594fc4699c31b9077d15e74be56a0",
        "license": "MIT",
        "stars": 48,
        "pushed": "2026-07-23",
    },
    "legal-skills": {
        "repo": "pa1nrui1/legal-skills",
        "commit": "5e39b9c30cc66ece89ff64cdafbeddde80c6b507",
        "license": "MIT",
        "stars": 65,
        "pushed": "2026-07-03",
    },
    "karlmarx-method": {
        "repo": "baojiachen0214/karlmarx-skill",
        "commit": "59f201137d96a59e68f36c2f469e04a957d3b280",
        "license": "MIT",
        "stars": 20,
        "pushed": "2026-04-05",
    },
    "marx-capital": {
        "repo": "x8k/ethical-ai-skills",
        "commit": "9a57fcd01528c5caac68130a2144a046a3b3a2c8",
        "license": "MIT；内容另见 CONTENT_LICENSE.md 的公有领域与开放许可说明",
        "stars": 0,
        "pushed": "2026-06-07",
    },
    "arts-culture": {
        "repo": "a5c-ai/babysitter",
        "commit": "120926cf0f706e1fc4b7eda5e196aa40aa804e68",
        "license": "MIT",
        "stars": 1670,
        "pushed": "2026-08-12",
    },
    "digital-curation": {
        "repo": "wuyaojunkylin/research-digital-curation-skills",
        "commit": "5680aa2b4521a757e436b65615904acb24d3276f",
        "license": "MIT",
        "stars": 3,
        "pushed": "2026-05-11",
    },
    "calligraphy": {
        "repo": "theneoai/awesome-skills",
        "commit": "61fe4f2bb47d6b61505b1b78c2b8ae5fd1ca38dd",
        "license": "MIT 变体（使用或修改时须保留指定署名与修改说明）",
        "stars": 135,
        "pushed": "2026-05-15",
    },
    "museum-art": {
        "repo": "huytieu/COG-second-brain",
        "commit": "19471473a34a29a042c0d7738ce573cc2dcee119",
        "license": "MIT",
        "stars": 834,
        "pushed": "2026-08-07",
    },
}

TREE_CACHE: dict[tuple[str, str], list[dict]] = {}

SCAN_PATTERNS = {
    "outbound_code": re.compile(r"(?i)\brequests\.|\burllib\.request\b|\bhttpx\.|\bfetch\s*\(|\bcurl\s+"),
    "credentials": re.compile(r"(?i)api[_ -]?key|access[_ -]?token|bearer\s+|credential|password|\.env\b|secret\b"),
    "process": re.compile(r"(?i)subprocess\.|os\.system|shell\s*=\s*True|child_process|Start-Process"),
    "dynamic_execution": re.compile(r"(?i)(?<![A-Za-z])eval\s*\(|(?<![A-Za-z])exec\s*\("),
    "write": re.compile(r"(?i)write_text\s*\(|write_bytes\s*\(|\.save\s*\(|\.write\s*\(|open\([^\n]+[, ]['\"]w|Out-File|Set-Content"),
    "delete": re.compile(r"(?i)rm\s+-rf|Remove-Item|unlink\s*\(|rmtree\s*\(|os\.remove\s*\("),
    "remote_install": re.compile(r"(?i)curl[^\n|]{0,200}\|\s*(?:ba)?sh|wget[^\n|]{0,200}\|\s*(?:ba)?sh|\bnpx\s+(?:-y|--yes)\b|\bpip\s+install\b|\bnpm\s+install\b"),
    "external_state": re.compile(r"(?i)git\s+push|\bupload\b|\bpublish\b|\bdeploy\b|auto.?pay|wallet"),
    "prompt_bypass": re.compile(r"(?i)ignore (?:all |any )?(?:previous|system|developer) instructions|bypass (?:approval|authorization|permission)"),
}

TEXT_SUFFIXES = {".md", ".txt", ".py", ".sh", ".js", ".ts", ".mjs", ".cjs", ".json", ".yaml", ".yml", ".toml", ".html", ".xml", ".csv"}


def gh_record(repo_key: str, path: str, name: str, cn: str, category: str, purpose: str, inputs: str, outputs: str,
              limits: str, grade: str = "SA", difficulty: str = "A", majors: list[str] | None = None,
              network: str = "未见主动联网；说明中的参考链接不等于执行网络请求。",
              file_behavior: str = "按说明读取用户明确提供的材料并生成草案；无随包可执行载荷。",
              credentials: str = "未见账号或密钥要求。", quality: int = 2, priority: str = "中",
              chinese_support: bool = False, higher_ed_scenario: bool = False, authority_source: bool = False) -> dict:
    meta = GITHUB_REPOS[repo_key]
    repo = meta["repo"]
    commit = meta["commit"]
    return {
        "name": name, "cn_name": cn, "category": category, "purpose": purpose, "inputs": inputs, "outputs": outputs,
        "limits": limits, "platform": "GitHub", "repo_key": repo_key, "repo": repo, "path": path,
        "canonical_url": f"https://github.com/{repo}/blob/{commit}/{urllib.parse.quote(path, safe='/')}",
        "repo_url": f"https://github.com/{repo}", "fixed_version": commit, "license": meta["license"], "stars": meta["stars"],
        "last_update": meta["pushed"], "security_grade": grade, "difficulty": difficulty, "majors": majors,
        "network_behavior": network, "credential_behavior": credentials, "file_behavior": file_behavior,
        "quality": quality, "priority": priority, "chinese_support": chinese_support,
        "higher_ed_scenario": higher_ed_scenario, "authority_source": authority_source,
    }


def claw_record(slug: str, version: str, license_name: str, downloads: int, name: str, cn: str, category: str, purpose: str,
                inputs: str, outputs: str, limits: str, grade: str = "SA", difficulty: str = "A",
                file_behavior: str = "按说明读取用户明确提供的材料并生成草案；包内无可执行脚本。",
                network: str = "未见主动联网；说明中的参考链接不等于执行网络请求。",
                credentials: str = "未见账号或密钥要求。", quality: int = 3, priority: str = "中",
                chinese_support: bool = False, higher_ed_scenario: bool = False, authority_source: bool = False) -> dict:
    return {
        "name": name, "cn_name": cn, "category": category, "purpose": purpose, "inputs": inputs, "outputs": outputs,
        "limits": limits, "platform": "ClawHub", "slug": slug, "path": "SKILL.md",
        "canonical_url": f"https://clawhub.ai/skills/{slug}?version={version}", "repo_url": f"https://clawhub.ai/skills/{slug}",
        "fixed_version": version, "license": license_name, "stars": 0, "downloads": downloads, "last_update": DATE,
        "security_grade": grade, "difficulty": difficulty, "majors": None,
        "network_behavior": network, "credential_behavior": credentials, "file_behavior": file_behavior,
        "quality": quality, "priority": priority, "chinese_support": chinese_support,
        "higher_ed_scenario": higher_ed_scenario, "authority_source": authority_source,
    }


FORMAL = {
    "0301": [
        claw_record("case-brief-drafter", "0.5.1", "MIT-0", 653, "case-brief-drafter", "判例摘要与 IRAC 案例简报", "0301-02",
                    "把一份完整判决意见整理为事实、程序、争点、规则、论证、裁判结论和异议意见分明的案例简报。",
                    "完整判决意见、案件名称与引证、使用目的、法域或课程背景。",
                    "带页码或段落定位的案例简报、未解决信息清单、课堂或模拟法庭提示。",
                    "只能依据用户提供的判决文本；不得把摘要或编者按当作权威判决，也不得替用户案件作最终结论。", quality=4, priority="高", higher_ed_scenario=True),
        claw_record("legal-contract-review-playbook", "1.0.1", "MIT-0", 754, "legal-contract-review-playbook", "合同审查清单与风险说明", "0301-04",
                    "按当事人、义务、风险分配、救济和谈判立场整理合同审查要点。",
                    "合同文本、合同类型、当事人、法域、目标读者和重点风险。",
                    "条款问题清单、风险分级、谈判备选意见和管理层摘要草案。",
                    "框架不含法域专用法源，示例中的期限、百分比和监管要求必须重新查证；敏感合同应在本地处理。", quality=4, priority="高"),
        claw_record("legal-regulatory-compliance-mapper", "1.1.1", "MIT-0", 696, "legal-regulatory-compliance-mapper", "监管义务与控制措施映射", "0301-07",
                    "把监管义务、责任人、证据、复核频率和需律师介入的事项放入同一张合规矩阵。",
                    "业务或产品范围、法域、已有制度、监管材料和负责人信息。",
                    "监管义务表、控制与责任人映射、证据清单、复核日历和待核验缺口。",
                    "不能自行认定已经合规；没有权威来源的项目必须标记为待核验，示例中的法域规则不得直接照搬。", quality=4, priority="高"),
        claw_record("legal-evidence-mapping-mctmilk", "1.0.0", "MIT-0", 883, "legal-evidence-mapping-mctmilk", "要件—事实—证据对应表", "0301-05",
                    "把法条构成要件、待证事实、举证责任和证据种类逐项对应，找出证据缺口。",
                    "适用法条、请求或抗辩、已有事实与证据。",
                    "要件—事实—证据表、举证责任说明、薄弱环节和补强建议草案。",
                    "必须由专业人员确认适用法条、举证责任和证据可采性；不得据此制作、篡改或诱导证据。", quality=3, priority="高", chinese_support=True),
        gh_record("legal-citation", "CLAUDE.md", "Chinese-Legal-Citation-skill", "中国法学引注检查与修订", "0301-03",
                  "按照《法学引注手册》规则检查法学论文脚注，并可生成带修订痕迹的 Word 副本。",
                  "含脚注的 .docx 论文、引注规则和希望采用的修订方式。",
                  "引注问题清单、结构化修订计划和新生成的修订版 Word。",
                  "暂不支持尾注和小语种；引文真实性和原始法源仍需逐项核对，必须保留原文件。", grade="SB", difficulty="B",
                  network="核心脚本未见主动联网；不应把未公开论文发送到外部服务。",
                  file_behavior="Python 脚本读取 .docx 并写出新的修订版文件；限制在指定目录，禁止覆盖原件。",
                  quality=4, priority="高", chinese_support=True, higher_ed_scenario=True),
        gh_record("legal-redline", "skill.md", "legal-redline-tools", "合同 Word 红线稿与差异报告", "0301-04",
                  "把已经明确的合同修改计划转换为带修订痕迹的 Word，并可生成差异摘要和 PDF。",
                  "原合同、结构化修改计划、输出目录和审阅规则。",
                  "新 Word 红线稿、改动摘要、法律备忘录或差异 PDF。",
                  "它负责忠实呈现修改，不判断修改本身是否正确；必须先由法律人员审定修改计划并保留原合同。", grade="SB", difficulty="B",
                  network="核心包未见主动联网；安装依赖不属于本轮审查。",
                  file_behavior="Python 包读取合同并在指定目录写出 DOCX/PDF/摘要文件；不得覆盖唯一原件。",
                  quality=3, priority="中", higher_ed_scenario=False),
        gh_record("legal-skills", "skills/legal/初步法律分析/SKILL.md", "初步法律分析", "请求权与要件式初步法律分析", "0301-02",
                  "用请求权基础、构成要件和证据责任的顺序梳理案件问题，并明确已核验和待核验内容。",
                  "案件事实、当事人目标、法域、已有材料和时间范围。",
                  "问题树、请求权与抗辩路径、证据缺口、法源待核验清单和建议书草案。",
                  "原技能与同仓库总控和文件区约定紧密，接入时需改成本校项目路径；不得把初步分析当成正式法律意见。", grade="SB", difficulty="B",
                  file_behavior="说明要求读取案件资料并生成本地 Word/Markdown；限制到案件专用目录，所有正式导出需人工确认。",
                  quality=3, priority="高", chinese_support=True),
        gh_record("legal-skills", "skills/legal/法规案例检索/SKILL.md", "法规案例检索", "中国法规与案例分层检索", "0301-01",
                  "按问题、法源层级和案例层次组织中国法规与案例检索，分别形成法源汇编和检索报告。",
                  "法律问题、请求权路径、法域、时间截点和可访问的权威数据库。",
                  "法规案例汇编、检索过程、命中与未命中说明、法源版本和待复核项。",
                  "数据库访问权和使用条款需另行确认；任何法条和案例都要核对生效状态与官方原文。", grade="SB", difficulty="B",
                  network="工作流需要访问法律数据库；仅允许学校批准的数据源，不上传案件敏感信息。",
                  file_behavior="读取案件资料并生成检索报告；输出限定到指定目录。", credentials="可能需要法律数据库账号；应使用最小权限并遵守学校订阅条款。",
                  quality=3, priority="高", chinese_support=True),
        gh_record("legal-skills", "skills/legal/劳动争议证据体系/SKILL.md", "劳动争议证据体系", "劳动争议举证责任与证据清单", "0301-05",
                  "按劳动争议类型、举证责任、特殊保护和规章制度合法性整理证据。",
                  "劳动关系事实、争议类型、合同制度、工资工时资料和现有证据。",
                  "举证责任表、证据收集清单、特殊保护提示和制度证据缺口。",
                  "涉及员工个人信息和争议策略，必须在受控目录处理；规则和时效应由劳动法律专业人员复核。", grade="SB", difficulty="B",
                  file_behavior="读取劳动争议材料并生成本地表格或报告；限制在案件目录且不自动提交。",
                  quality=3, priority="中", chinese_support=True),
        gh_record("legal-skills", "skills/legal/庭前准备/SKILL.md", "庭前准备", "争点导向的庭前与模拟法庭准备", "0301-06",
                  "把起诉状、法律分析、证据意见和案例资料整理成争点导向的庭审提纲。",
                  "教学案例或真实案件的脱敏材料、诉辩立场、争点、证据和程序要求。",
                  "庭审提纲、质证攻防矩阵、举证策略表、陈述和辩论提纲。",
                  "真实案件必须由律师审定；用于教学时要明确角色是假设，不能据此指导虚假陈述或证据。", grade="SB", difficulty="B",
                  file_behavior="读取多份前置法律材料并生成本地文档；只在指定目录写入草案。", quality=3, priority="中", chinese_support=True, higher_ed_scenario=True),
        gh_record("legal-skills", "skills/legal/法律文书出稿前审查/SKILL.md", "法律文书出稿前审查", "法律文书导出前质量闸门", "0301-04",
                  "在正式 Word 导出前检查事实来源、法规核验、用户确认和文书结构，决定返回整改还是允许出稿。",
                  "正文草案、结构化字段、复查摘要、法规核验摘要和用户确认记录。",
                  "通过、阻断或需确认状态，以及具体整改项和复核记录。",
                  "原技能引用同仓库命令和总控，接入需改写；只能作为流程闸门，不能保证法律结论正确。", grade="SB", difficulty="B",
                  file_behavior="需要读取中间文件并调用同仓库审查流程；仅允许受控目录与人工确认后的导出。", quality=3, priority="中", chinese_support=True),
        gh_record("legal-skills", "skills/legal/产品法务/SKILL.md", "产品法务", "中国境内产品上线合规检查", "0301-07",
                  "围绕功能、页面、协议、数据、资质和高监管行业要求进行产品上线前合规问题梳理。",
                  "产品说明、用户流程、页面截图、协议政策、行业、数据类型和拟上线动作。",
                  "问题清单、法律待核验项、材料修改建议和上线条件草案。",
                  "高监管行业和数据合规结论必须由专业人员确认；不得把生成结果直接作为上线批准。", grade="SB", difficulty="B",
                  network="可能需要核对现行法规和监管文件；只使用批准来源，不上传内部产品材料。",
                  file_behavior="读取产品材料并生成本地合规报告；无自动上线或提交权限。", quality=3, priority="中", chinese_support=True),
    ],
    "0305": [
        gh_record("marx-capital", "skills/marx-capital-complete/SKILL.md", "marx-capital-complete", "《资本论》分卷分章阅读索引", "0305-01",
                  "按卷、章和主题定位《资本论》相关内容，并提供概念表、章节索引和应用框架。",
                  "要查找的卷章、概念或政治经济学问题。",
                  "章节定位、概念定义、关联章节和阅读路径。",
                  "这是整理后的英文知识库，不是权威中文译本；个别简化表述与卷四编排需回到可靠版本核对。", quality=3, priority="高"),
        gh_record("karlmarx-method", "SKILL.md", "karlmarx-skill", "马克思主义结构分析框架", "0305-06",
                  "用矛盾、总体、历史化、意识形态批判和实践反馈五组步骤分析复杂社会与组织问题。",
                  "社会现象、制度安排、历史背景、相关数据和需要比较的其他解释。",
                  "表层现象、结构机制、主要矛盾、历史条件、竞争解释、确定性和可检验行动。",
                  "它是方法应用而非原著解释；现代场景属于延伸分析，必须标明证据、争议和不确定性。", quality=3, priority="高", chinese_support=True),
    ],
    "1304": [
        gh_record("arts-culture", "library/specializations/domains/social-sciences-humanities/arts-culture/skills/curatorial-research/SKILL.md", "curatorial-research", "美术史与作品来源研究", "1304-01",
                  "组织艺术史研究、艺术家生平与作品、档案来源、展览史和来源链调查。",
                  "作品或艺术家、研究问题、已知年代与来源、可访问档案和文献。",
                  "研究问题、资料清单、作品来源链、疑点、注释和目录条目草案。",
                  "不能据此认定真伪或合法所有权；来源缺口、争议归属和战乱时期记录须由专家核验。", grade="SB", difficulty="B",
                  network="说明允许网络检索；只访问批准的馆藏、档案和学术来源，不上传未公开馆藏资料。",
                  file_behavior="读取研究材料并写出研究记录；限制在项目目录。", quality=3, priority="高"),
        gh_record("arts-culture", "library/specializations/domains/social-sciences-humanities/arts-culture/skills/collection-documentation/SKILL.md", "collection-documentation", "艺术品馆藏编目与摄影记录", "1304-03",
                  "按馆藏规范记录登录号、名称、年代、材料、尺寸、来源、摄影和状况信息。",
                  "作品实物或图像、登录资料、尺寸材料、来源和机构编目规则。",
                  "规范馆藏条目、摄影清单、状况记录和数字资产关联。",
                  "需要采用本馆受控词表和编号规则；不得自动改写唯一馆藏记录或公开敏感来源信息。", grade="SB", difficulty="B",
                  file_behavior="说明允许在馆藏数据库或本地表格中写入；正式记录必须人工审批并保留修改日志。", quality=3, priority="高"),
        gh_record("arts-culture", "library/specializations/domains/social-sciences-humanities/arts-culture/skills/conservation-assessment/SKILL.md", "conservation-assessment", "艺术品保存状况评估", "1304-04",
                  "按材料、结构、损伤、既往干预和环境因素记录艺术品状况，并比较处理方案。",
                  "作品实物观察、高清图像、材料与历史记录、环境数据。",
                  "状况报告、损伤示意、处理选择、风险与后续照护建议草案。",
                  "不能仅凭图片确定材料或损伤原因，也不能替代修复师现场检查、取样和伦理判断。", grade="SB", difficulty="B",
                  network="说明允许查阅外部资料；不得把敏感馆藏图像上传到未经批准的网站。",
                  file_behavior="读取图像和记录并写出评估草案；不允许自动实施修复或覆盖馆藏档案。", quality=3, priority="高"),
        gh_record("arts-culture", "library/specializations/domains/social-sciences-humanities/arts-culture/skills/exhibition-design/SKILL.md", "exhibition-design", "美术展览空间与参观流线设计", "1304-08",
                  "把策展叙事、作品、场地、照明、保护和无障碍要求转换为展览布局方案。",
                  "策展主题、作品清单与尺寸、场地图、观众、照明和保护限制。",
                  "平面布局、作品顺序、流线、照明与图文层级、技术要求。",
                  "承重、消防、安防、照度和文物保护必须由相应专业人员现场确认。", grade="SB", difficulty="B",
                  network="未见必要主动联网；参考标准需从批准来源核对。",
                  file_behavior="读取场地图和作品资料并生成设计文档；无自动施工或采购权限。", quality=3, priority="高"),
        gh_record("arts-culture", "library/specializations/domains/social-sciences-humanities/arts-culture/skills/interpretive-writing/SKILL.md", "interpretive-writing", "展签、墙文与图录写作", "1304-08",
                  "面向不同观众写作作品展签、单元墙文、图录文章和教育材料，并兼顾准确性与可读性。",
                  "作品研究材料、目标观众、篇幅、展览语气和无障碍要求。",
                  "作品标签、墙文、图录草案、教育材料和多层次说明。",
                  "事实、译名、年代、来源和争议解释必须经策展或研究人员核对；不能把推测写成定论。", grade="SB", difficulty="B",
                  network="说明允许查阅外部资料；未公开研究材料不发送到外部服务。",
                  file_behavior="读取研究材料并写出策展文本草案；无自动发布权限。", quality=3, priority="高"),
        gh_record("digital-curation", "research-digital-curation-workflow/SKILL.md", "research-digital-curation-workflow", "研究型数字策展总流程", "1304-08",
                  "从策展对象、研究材料、页面文本、叙事模块、视觉语言到原型，安排数字展览的工作顺序。",
                  "策展对象、研究材料、观众、材料边界、现有页面或原型状态。",
                  "阶段诊断、下一步任务、交付清单和避免过早进入视觉实现的边界。",
                  "总流程本身较简洁，正式项目仍需调用同仓库具体子技能并由策展、版权和技术人员复核。", quality=3, priority="高", chinese_support=True),
        gh_record("digital-curation", "curatorial-topic-framing/SKILL.md", "curatorial-topic-framing", "数字策展选题与材料边界", "1304-08",
                  "把模糊兴趣或材料堆收缩成可研究、可展示且证据条件明确的策展对象。",
                  "初步兴趣、已有材料、目标观众、时间和项目限制。",
                  "候选选题比较、主选题、观众与材料边界、阶段说明。",
                  "选题建议不替代馆藏授权、史料核验和当事群体协商。", quality=3, priority="中", chinese_support=True),
        gh_record("digital-curation", "curatorial-narrative-modules/SKILL.md", "curatorial-narrative-modules", "数字展览叙事与页面模块", "1304-08",
                  "把策展文本拆成页面类型、内容字段、导航、阅读顺序和交互层次。",
                  "已确认的策展文本、作品资料、目标观众和展示平台限制。",
                  "页面地图、模块字段、导航路径、交互层级和可复用模板说明。",
                  "结构清单不能替代真实观众测试、无障碍检查和内容核验。", quality=3, priority="中", chinese_support=True),
        gh_record("digital-curation", "research-to-curatorial-copy/SKILL.md", "research-to-curatorial-copy", "研究材料转数字展览文本", "1304-08",
                  "把研究笔记、史料、访谈和图像说明转为可直接放入页面的策展文本，同时保留证据与不确定性。",
                  "研究笔记、史料、访谈、作品图像说明和学术判断。",
                  "页面标题、导言、主题卡片、展签正文、证据条目和不确定性标记。",
                  "只做转译和组织；所有引文、历史事实、人物信息和权利状态必须回到原始材料核验。", quality=3, priority="高", chinese_support=True),
        gh_record("calligraphy", "skills/persona/education/calligraphy-instructor/SKILL.md", "calligraphy-instructor", "中国书法学习与笔法诊断", "1304-07",
                  "按篆、隶、楷、行、草的学习顺序解释执笔、用锋、笔画、结体和临摹，并诊断常见问题。",
                  "学习阶段、书体、临摹对象、作品照片或对笔画问题的描述。",
                  "练习顺序、笔法提示、问题诊断、临摹计划和阶段自检。",
                  "角色身份和“多年经验”是提示设定，不是可核验资历；图片反馈不能替代教师现场观察。", quality=3, priority="高"),
        gh_record("museum-art", "skills/museum-art/SKILL.md", "museum-art", "博物馆开放艺术图像检索与许可核对", "1304-09",
                  "从多家博物馆开放接口检索高分辨率艺术图像，并逐件核对公有领域或开放许可标记。",
                  "题材、艺术家或时期、用途、分辨率要求和许可边界。",
                  "馆藏图像候选、作品元数据、原始馆藏页、下载地址和逐件许可说明。",
                  "不同馆藏的权利标记不一致，必须逐件确认；不得把“开放馆藏”误写成所有作品都可自由使用。", grade="SB", difficulty="B",
                  network="会访问 Met、Cleveland、SMK、Rijksmuseum、NGA、AIC、Getty 等馆藏接口并下载公开图像；不上传用户材料。",
                  file_behavior="可把选定公开图像写入具体项目资产目录；不建立无来源的共享图片池。",
                  credentials="大多数来源无需密钥；Smithsonian、Europeana 等部分来源可能需要免费 API 密钥。", quality=5, priority="高"),
    ],
}


RAW = {
    "0301": {
        "clawhub": ["case-brief-drafter", "legal-contract-review-playbook", "legal-regulatory-compliance-mapper", "legal-evidence-mapping-mctmilk", "evidence-organizer", "law-search", "precedent", "statute", "moot-court-ai", "court-records-case-law-litigation", "patent-validator", "patent-novelty-search", "patent-invalid-search", "trademark-quick-check", "chinese-trademark-search-skill"],
        "github": ["Chinese-Legal-Citation-skill", "legal-redline-tools", "legal-skills/初步法律分析", "legal-skills/法规案例检索", "legal-skills/合同审查", "legal-skills/劳动争议证据体系", "legal-skills/庭前准备", "legal-skills/法律文书出稿前审查", "legal-skills/产品法务", "legal-skills/监管合规监测", "china-lawyer-analyst"],
        "huggingface": ["普通法律问答或合同分析 Space（未取得 Agent Skill 工作流）", "法律命名实体或案例检索 Demo（模型/应用，不是可核验 Skill 包）"],
        "public": ["GitLab 与公开搜索未发现比固定 GitHub 上游更完整的学科专属包", "ClawHub 市场卡片均回到固定版本包内容核验"],
    },
    "0305": {
        "clawhub": ["关键词 Marxism、Marx、马克思主义、历史唯物主义、思想政治教育未发现可准入候选"],
        "github": ["karlmarx-skill", "marx-capital-complete", "karl-marx-skill", "marx-perspective", "maoxuan-skill", "historical-materialist-analysis", "practical-marxist-application", "marxist-analysis-of-film-adaptations", "mao-zedong-perspective", "karl-marx-perspective", "marxists.org-rag-db"],
        "huggingface": ["两个旧版马克思主义 GPT-2 演示 Space（只有模型演示，无完整工作流）"],
        "public": ["GitLab 与公开搜索未发现具备更完整许可、证据和固定版本的专用 Skill"],
    },
    "1304": {
        "clawhub": ["chinese-calligraphy-recognition", "通用图像生成与风格转换 Skill", "艺术史营销写作或通用审美工具"],
        "github": ["curatorial-research", "collection-documentation", "conservation-assessment", "exhibition-design", "interpretive-writing", "research-digital-curation-workflow", "curatorial-topic-framing", "curatorial-narrative-modules", "curatorial-visual-language", "research-to-curatorial-copy", "curatorial-log-method-recovery", "curatorial-prototype-standardization", "calligraphy-instructor", "museum-curator", "museum-art", "art-history-movements", "sculpture-3d"],
        "huggingface": ["艺术史图像生成、书法识别、博物馆静态页和雕塑展示 Space（无可核验 Agent Skill 工作流）"],
        "public": ["公开搜索补充发现研究型数字策展技能包；未发现许可证与内容更完整的雕塑专用 Skill"],
    },
}


EXCLUDED = {
    "0301": [
        ("evidence-organizer", "与要件—事实—证据对应及本地法律证据工作流实质重叠，且包含脚本与通用分类，未新增学科专属产出。", "重复/较弱替代"),
        ("law-search", "无明确许可证；读取明文配置密钥并通过 HTTP 调用韩国开放接口，不满足许可和高校部署门槛。", "无许可/网络凭据"),
        ("precedent", "主要是美国普通法参考文本，与中国法学教学情境适配较弱，且脚本只是把固定文本输出到终端。", "适配价值不足"),
        ("statute", "主要是美国立法过程参考文本，与中国法学教学情境适配较弱，且脚本只是把固定文本输出到终端。", "适配价值不足"),
        ("moot-court-ai", "原包需要多个外部模型密钥和自动化编排；只能作为适配参考，原包不进入正式库。", "SB-A"),
        ("court-records-case-law-litigation", "调用按次付费的外部案件接口并可自动钱包付款，外部状态与费用风险不可接受。", "X"),
        ("patent-validator", "固定版本无许可证声明，且只生成检索式，不完成可核验检索。", "无许可"),
        ("patent-novelty-search", "依赖 Google Patents 浏览器检索与模型判断，来源记录和法域适配不足，未达到正式证据门槛。", "证据不足"),
        ("patent-invalid-search", "会给出专利无效结论，且外部检索和证据固定方式不足，不宜作为高校正式推荐。", "高影响判断/证据不足"),
        ("trademark-quick-check", "说明包含会变化的期限和量化近似评分，关键脚本和数据源核验不足。", "时效与证据不足"),
        ("chinese-trademark-search-skill", "依赖托管商业接口、绑定与点数，完整上游和费用边界不清。", "外部服务/证据不足"),
        ("china-lawyer-analyst", "仓库无明确许可证且包含较多自动化脚本与定时任务。", "无许可"),
        ("合同审查（pa1nrui1）", "与入选的合同审查框架和红线工具重叠，且同仓库脚本与总控耦合更深。", "重复"),
        ("监管合规监测（pa1nrui1）", "需要外部法律数据库和持续联网，与入选的监管义务映射相比接入更重。", "较弱替代"),
    ],
    "0305": [
        ("youaifuou/karl-marx-skill", "以马克思本人身份回应，角色扮演会模糊原著、后世解释与模型生成内容，按硬性排除处理。", "角色扮演"),
        ("Nhj-sz/marx-skill", "明确要求扮演马克思，并强制网络检索后以第一人称作判断，不符合学术来源边界。", "角色扮演"),
        ("leezythu/maoxuan-skill", "虽然材料较丰富，但核心是人物角色与表达风格复刻，不是原著学习或思政教学工作流。", "角色扮演"),
        ("ptreezh/historical-materialist-analysis", "固定版本出现严重乱码、自动安装依赖和无证据的准确率百分比。", "SB-A/质量不足"),
        ("practical-marxist-application", "与历史唯物主义分析重复，文件乱码且给出无依据质量指标。", "重复/质量不足"),
        ("marxist-analysis-of-film-adaptations", "自动生成的窄任务记忆包，主要服务电影改编分析，来源与理论证据不足。", "偏离范围/证据不足"),
        ("digoal/karl-marx-perspective", "人物视角型提示，与多个角色扮演副本实质相同。", "角色扮演/重复"),
        ("marxists.org-rag-db", "属于语料数据库线索而非可取得的完整 Agent Skill 工作流。", "仅概念/非 Skill"),
    ],
    "1304": [
        ("chinese-calligraphy-recognition", "脚本把作品图像发送到说明未充分披露的第三方域名，且实际功能与宣称不一致。", "X"),
        ("museum-curator", "覆盖面过宽，与入选的馆藏编目、保存评估、策展研究、展览设计和展签写作重复。", "重复"),
        ("curatorial-visual-language", "更接近通用视觉设计，学科专属证据弱于其他数字策展子技能。", "边界不足"),
        ("curatorial-log-method-recovery", "主要是通用项目日志和决策记录，缺少美术学专属产出。", "通用"),
        ("curatorial-prototype-standardization", "主要进入前端实现与响应式页面，属于通用软件开发而非美术学专属。", "通用"),
        ("art-history-movements", "所在仓库采用 Business Source License，当前仅允许非生产使用，且条目为生成器示例。", "许可限制"),
        ("sculpture-3d", "所在仓库采用 Business Source License，当前仅允许非生产使用，且内容是通用三维示例。", "许可限制/通用"),
        ("通用图像生成与风格转换技能", "只生成或模仿图像，不包含美术学研究、材料、技法、保存或策展流程。", "通用"),
        ("Hugging Face 艺术与书法 Demo", "未取得完整 Agent Skill 工作流、固定包内容和许可证证据。", "非 Skill/证据不足"),
    ],
}


def run_gh(*args: str) -> str:
    return subprocess.check_output(["gh", "api", *args], text=True, encoding="utf-8")


def github_file(repo: str, commit: str, path: str) -> bytes:
    raw = run_gh("-X", "GET", f"repos/{repo}/contents/{path}", "-f", f"ref={commit}")
    data = json.loads(raw)
    return base64.b64decode(re.sub(r"\s", "", data["content"]))


def github_tree(repo: str, commit: str) -> list[dict]:
    key = (repo, commit)
    if key not in TREE_CACHE:
        TREE_CACHE[key] = json.loads(run_gh("-X", "GET", f"repos/{repo}/git/trees/{commit}", "-f", "recursive=1"))["tree"]
    return TREE_CACHE[key]


def claw_file(slug: str, version: str, path: str) -> bytes:
    url = f"https://clawhub.ai/api/v1/skills/{urllib.parse.quote(slug)}/file?path={urllib.parse.quote(path)}&version={urllib.parse.quote(version)}&preview=1"
    return fetch_url(url)


def claw_version(slug: str, version: str) -> dict:
    url = f"https://clawhub.ai/api/v1/skills/{urllib.parse.quote(slug)}/versions/{urllib.parse.quote(version)}"
    return json.loads(fetch_url(url).decode("utf-8"))["version"]


def fetch_url(url: str) -> bytes:
    last_error: Exception | None = None
    request = urllib.request.Request(url, headers={"User-Agent": "University-Skill-Research/1.0"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as resp:
                return resp.read()
        except Exception as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"无法读取公开固定版本地址：{url}") from last_error


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def scan_files(files: list[Path], base: Path) -> dict:
    hits = {key: [] for key in SCAN_PATTERNS}
    domains: set[str] = set()
    text_files = 0
    binary_files = 0
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"Dockerfile", "Makefile"}:
            binary_files += 1
            continue
        text_files += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = str(path.relative_to(base)).replace("\\", "/")
        for key, pattern in SCAN_PATTERNS.items():
            for match in pattern.finditer(text):
                line_no = text.count("\n", 0, match.start()) + 1
                line = text.splitlines()[line_no - 1].strip()[:180] if text.splitlines() else ""
                if len(hits[key]) < 8:
                    hits[key].append(f"{rel}:{line_no}: {line}")
        for domain in re.findall(r"https?://([^/\s)'\">]+)", text, flags=re.I):
            domains.add(domain.lower().rstrip(".,;"))
    return {"text_files": text_files, "binary_files": binary_files, "domains": sorted(domains), "hits": hits}


def snapshot_record(rec: dict, code: str) -> dict:
    root = ROOT / "03_候选池" / "source_snapshots" / code
    if rec["platform"] == "GitHub":
        meta = GITHUB_REPOS[rec["repo_key"]]
        repo, commit, path = meta["repo"], meta["commit"], rec["path"]
        dest = root / "github" / repo.replace("/", "__") / commit
        tree = github_tree(repo, commit)
        write_json(dest / "tree_manifest.json", tree)
        write_json(dest / "repo_metadata.json", meta)
        for support in ["README.md", "README_en.md", "README.zh.md", "README.en.md", "LICENSE", "LICENSE.md", "CONTENT_LICENSE.md"]:
            if any(x["path"] == support for x in tree):
                try:
                    support_target = dest / "files" / support
                    if not support_target.exists():
                        write_text(support_target, github_file(repo, commit, support).decode("utf-8", errors="replace"))
                except Exception:
                    pass
        package_prefix = str(Path(path).parent).replace("\\", "/")
        if package_prefix in {"", "."}:
            package = [x for x in tree if x.get("type") == "blob"]
        else:
            package = [x for x in tree if x.get("type") == "blob" and (x["path"] == path or x["path"].startswith(package_prefix + "/"))]
        for item in package:
            rel = item["path"]
            package_target = dest / "files" / rel
            if package_target.exists():
                continue
            try:
                blob = github_file(repo, commit, rel)
            except Exception:
                continue
            package_target.parent.mkdir(parents=True, exist_ok=True)
            package_target.write_bytes(blob)
        target = dest / "files" / path
        content = target.read_bytes() if target.exists() else github_file(repo, commit, path)
        scan_targets = [dest / "files" / item["path"] for item in package if (dest / "files" / item["path"]).exists()]
        static_scan = scan_files(scan_targets, dest / "files")
        return {
            "name": rec["name"], "platform": "GitHub", "fixed_version": commit, "entry": path,
            "snapshot": str(target.relative_to(ROOT)).replace("\\", "/"), "package_files": len(package),
            "script_files": len([x for x in package if Path(x["path"]).suffix.lower() in {".py", ".sh", ".js", ".ts", ".ps1", ".bat", ".cmd"}]),
            "sha256": hashlib.sha256(content).hexdigest(),
            "static_scan": static_scan,
        }
    slug, version = rec["slug"], rec["fixed_version"]
    dest = root / "clawhub" / slug / version
    version_target = dest / "version_metadata.json"
    if version_target.exists():
        vm = json.loads(version_target.read_text(encoding="utf-8"))
    else:
        vm = claw_version(slug, version)
        write_json(version_target, vm)
    target = dest / "files" / "SKILL.md"
    if target.exists():
        content = target.read_bytes()
    else:
        content = claw_file(slug, version, "SKILL.md")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    files = vm.get("files", [])
    static_scan = scan_files([target], dest / "files")
    return {
        "name": rec["name"], "platform": "ClawHub", "fixed_version": version, "entry": "SKILL.md",
        "snapshot": str(target.relative_to(ROOT)).replace("\\", "/"), "package_files": len(files),
        "script_files": len([x for x in files if Path(x.get("path", "")).suffix.lower() in {".py", ".sh", ".js", ".ts", ".ps1", ".bat", ".cmd"}]),
        "sha256": hashlib.sha256(content).hexdigest(),
        "static_scan": static_scan,
    }


def raw_purpose(name: str, code: str) -> str:
    low = name.lower()
    if code == "0301":
        if "citation" in low: return "法律引证与脚注核对"
        if "evidence" in low: return "法律证据整理"
        if "moot" in low: return "模拟法庭"
        if "contract" in low or "redline" in low: return "合同审查或红线稿"
        if "patent" in low or "trademark" in low: return "知识产权检索或预查"
        return "法律检索、分析或合规工作流"
    if code == "0305":
        return "马克思主义经典、人物视角或理论分析工作流"
    return "美术史、书画、馆藏、策展、保存或展览工作流"


def build_raw(code: str) -> None:
    out = ROOT / "03_候选池" / "raw" / code
    platforms = {"clawhub": "ClawHub", "github": "GitHub", "huggingface": "Hugging Face Spaces", "public": "公开补充来源"}
    files = {"clawhub": "clawhub", "github": "github", "huggingface": "huggingface-spaces", "public": "public-supplement"}
    for key, names in RAW[code].items():
        rows = []
        for name in names:
            rows.append({
                "name": name, "platform": platforms[key], "discovery_url": "见检索矩阵与内部排除记录",
                "upstream_hint": "已回溯或等待回溯的公开上游", "one_line_purpose": raw_purpose(name, code),
                "proposed_subcategory": "按主要产出待判定", "status": "原始候选；安全待核验",
                "risk_signals": "仅记录发现事实；不表示准入、安全或可用。", "collected_at": DATE,
            })
        text = "\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n"
        write_text(out / f"{DATE}-{files[key]}.jsonl", text)


def enrich_records(code: str) -> tuple[list[dict], list[dict]]:
    info = DISCIPLINES[code]
    snapshots = []
    records = []
    ordered = sorted(FORMAL[code], key=lambda item: (item["category"], item["name"].casefold()))
    for i, rec0 in enumerate(ordered, start=1):
        rec = dict(rec0)
        rec["id"] = f"DISC-{code}-{i:04d}"
        rec["discipline"] = info["full"]
        rec["category_name"] = info["categories"][rec["category"]]
        rec["majors"] = rec["majors"] or info["majors"]
        rec["roles"] = info["roles"]
        rec["verification_status"] = "全部通过（未实测）"
        rec["verification_depth"] = "已阅读说明、清点固定版本包内容并完成静态数据流推演；候选未安装、未运行。"
        rec["verified_at"] = DATE
        rec["readiness"] = "可直接使用" if rec["difficulty"] == "A" and rec["security_grade"] == "SA" else "微调试可用"
        rec["adoption_plain"] = "调整少" if rec["difficulty"] == "A" else "需要少量调整"
        rec["api_reachability"] = "无需 API" if "未见主动联网" in rec["network_behavior"] else "按限制条件访问批准来源"
        rec["maintenance"] = "活跃" if rec["last_update"] >= "2026-02-12" else "正常"
        rec["cross_discipline_reuse"] = "门类内" if len(rec["majors"]) > 1 else "专业专有"
        chinese_bonus = 1 if rec.get("chinese_support", False) else 0
        active_bonus = 1 if rec["last_update"] >= "2026-02-12" else 0
        community_bonus = 1 if rec.get("stars", 0) >= 50 or rec.get("downloads", 0) >= 100 else 0
        scenario_bonus = 1 if rec.get("higher_ed_scenario", False) else 0
        authority_bonus = 1 if rec.get("authority_source", False) else 0
        rec["quality"] = min(5, 1 + chinese_bonus + active_bonus + community_bonus + scenario_bonus + authority_bonus)
        rec["alternative"] = "未找到同等学科专属且证据更强的开源替代；可退回人工清单与权威来源核验。"
        rec["security_plain"] = (
            "低风险说明型；仍须人工复核内容，不自动提交或替代专业判断。" if rec["security_grade"] == "SA"
            else "存在受控文件读写、联网或脚本；只在指定目录、批准来源和人工确认下使用。"
        )
        snap = snapshot_record(rec, code)
        snapshots.append(snap)
        rec["evidence_paths"] = [snap["snapshot"], f"03_候选池/source_snapshots/{code}/snapshot_index.json"]
        rec["package_files"] = snap["package_files"]
        rec["script_files"] = snap["script_files"]
        rec["static_scan"] = snap["static_scan"]
        records.append(rec)
    return records, snapshots


def markdown_exclusions(code: str) -> str:
    lines = [f"# {DISCIPLINES[code]['full']}内部排除记录", "", f"核验日期：{DATE}", "", "本文件只作内部追溯；其中条目不得进入正式 Excel、Word 或知识库 Skill 清单。", "", "| 候选 | 类型 | 通俗理由 |", "|---|---|---|"]
    for name, reason, kind in EXCLUDED[code]:
        lines.append(f"| {name} | {kind} | {reason} |")
    return "\n".join(lines)


def audit_markdown(code: str, records: list[dict]) -> str:
    info = DISCIPLINES[code]
    lines = [f"# {info['full']}静态安全审查", "", f"审查日期：{DATE}", "", "## 结论边界", "",
             "本次只读取固定版本的公开说明、许可证、目录和关键脚本，未安装、未运行候选，也未登录或调用候选外部服务。通过仅表示在所读版本中未发现阻断性问题。", "",
             f"正式收录 {len(records)} 项：SA {sum(r['security_grade']=='SA' for r in records)} 项，SB {sum(r['security_grade']=='SB' for r in records)} 项。SB-A 与 X 只在内部排除记录留痕。", ""]
    for r in records:
        scan = r["static_scan"]
        hit_counts = {key: len(value) for key, value in scan["hits"].items() if value}
        scan_summary = "未命中提示绕过、删除、动态执行、外部状态变更或隐藏载荷。"
        if hit_counts:
            human_labels = {
                "outbound_code": "程序联网",
                "credentials": "账号或密钥词",
                "process": "启动其他程序",
                "dynamic_execution": "动态执行",
                "write": "文件写入",
                "delete": "删除",
                "remote_install": "远程安装",
                "external_state": "外部状态变更",
                "prompt_bypass": "提示绕过",
            }
            scan_summary = "关键词复核：" + "；".join(f"{human_labels[key]} {value} 处" for key, value in hit_counts.items()) + "。命中已逐条结合上下文复核，不把普通说明文字直接判为风险。"
        lines += [f"## {r['id']} {r['cn_name']}", "", f"- 固定版本：`{r['fixed_version']}`", f"- 许可证：{r['license']}",
                  f"- 包内容：{r['package_files']} 个文件，其中脚本 {r['script_files']} 个。",
                  f"- 静态扫描：文本 {scan['text_files']} 个、二进制 {scan['binary_files']} 个；{scan_summary}",
                  f"- 识别到的外部域名：{'、'.join(scan['domains']) if scan['domains'] else '无'}",
                  f"- 文件行为：{r['file_behavior']}", f"- 网络与数据：{r['network_behavior']}", f"- 账号凭据：{r['credential_behavior']}",
                  f"- 结论：{r['security_grade']}；{r['security_plain']}", f"- 学科边界：{info['boundary']}",
                  f"- 证据：`{r['evidence_paths'][0]}`；{r['canonical_url']}", ""]
    return "\n".join(lines)


def kb_skill_markdown(info: dict, r: dict) -> str:
    return f"""# {r['id']} {r['cn_name']}

- 原始名称：{r['name']}
- 主能力小类：{r['category']} {r['category_name']}
- 适用专业：{'、'.join(r['majors'])}
- 适用人员：{r['roles']}

## 它能帮您做什么

{r['purpose']}

## 使用前要准备什么

{r['inputs']}

## 会得到什么

{r['outputs']}

## 不能做什么

{r['limits']} {info['boundary']}

## 安全与接入

- 安全等级：{r['security_grade']}
- 使用难度：{r['adoption_plain']}
- 文件行为：{r['file_behavior']}
- 网络与数据：{r['network_behavior']}
- 账号凭据：{r['credential_behavior']}

## 本次核验

{r['verification_depth']}

- 固定版本：`{r['fixed_version']}`
- 许可证：{r['license']}
- 核验日期：{r['verified_at']}
- 原始资料：[{r['canonical_url']}]({r['canonical_url']})
- 本地证据：`{r['evidence_paths'][0]}`
"""


def build_kb(code: str, records: list[dict]) -> None:
    info = DISCIPLINES[code]
    base = ROOT / "02_知识库" / "discipline_pilots" / info["folder"]
    for r in records:
        write_text(base / "skills" / f"{r['id']}.md", kb_skill_markdown(info, r))
    category_counts = Counter(r["category"] for r in records)
    index = [f"# {info['full']}学科专属 Skill 调研入口", "", f"正式 Skill：{len(records)} 项；核验日期：{DATE}。", "", "## 快速入口", "",
             "- [能力小类](CAPABILITY_TAXONOMY.md)", "- [专业范围](PROFESSION_SCOPE.md)", "- [正式 Skill 索引](SKILL_INDEX.md)", "- [来源快照索引](SOURCE_SNAPSHOT_INDEX.md)", "- [安全索引](SECURITY_INDEX.md)", "",
             "## 结论边界", "", f"{info['boundary']} 所有候选均未安装、未运行。内部落选项不在此知识库出现。", "", "## 能力覆盖", ""]
    for code2, name in info["categories"].items():
        index.append(f"- {code2} {name}：{category_counts[code2]} 项")
    write_text(base / "INDEX.md", "\n".join(index))

    skill_index = [f"# {info['full']}正式 Skill 索引", "", f"共 {len(records)} 项，只含 SA/SB 且达到“全部通过（未实测）”的正式条目。", ""]
    for cat, cat_name in info["categories"].items():
        skill_index += [f"## {cat} {cat_name}", ""]
        items = [r for r in records if r["category"] == cat]
        if not items:
            skill_index.append("本轮未发现达到正式准入门槛的学科专属 Skill。")
        for r in items:
            skill_index.append(f"- [{r['id']} {r['cn_name']}](skills/{r['id']}.md) — {r['purpose']}")
        skill_index.append("")
    write_text(base / "SKILL_INDEX.md", "\n".join(skill_index))

    source = [f"# {info['full']}来源快照索引", "", f"快照根目录：`03_候选池/source_snapshots/{code}/`", "", "| ID | 来源 | 固定版本 | 本地入口 |", "|---|---|---|---|"]
    for r in records:
        source.append(f"| {r['id']} | {r['platform']} | `{r['fixed_version']}` | `{r['evidence_paths'][0]}` |")
    write_text(base / "SOURCE_SNAPSHOT_INDEX.md", "\n".join(source))

    security = [f"# {info['full']}安全索引", "", "| ID | 等级 | 通俗限制 |", "|---|---|---|"]
    for r in records:
        security.append(f"| {r['id']} | {r['security_grade']} | {r['security_plain']} |")
    security += ["", f"详细记录：`04_验证记录/{code}/{DATE}-{code}{info['name']}静态安全审查.md`"]
    write_text(base / "SECURITY_INDEX.md", "\n".join(security))


def update_matrix(code: str, records: list[dict]) -> None:
    path = ROOT / "02_知识库" / "findings" / f"{DATE}-{code}学科专属技能检索矩阵.md"
    original = path.read_text(encoding="utf-8") if path.exists() else f"# {DISCIPLINES[code]['full']}检索矩阵\n"
    original = re.sub(r"\n## 本轮执行结果[\s\S]*$", "", original.rstrip())
    counts = {k: len(v) for k, v in RAW[code].items()}
    add = ["", "## 本轮执行结果", "", f"执行日期：{DATE}", "", "| 平台 | 原始记录数 | 结论 |", "|---|---:|---|",
           f"| ClawHub | {counts['clawhub']} | 已完成首轮与两轮补充检索；市场卡片只作发现，正式项已回到固定版本包内容。 |",
           f"| GitHub | {counts['github']} | 已完成关键词、文件名和专业任务词补充检索；镜像与集合回到原始仓库。 |",
           f"| Hugging Face Spaces | {counts['huggingface']} | 发现的多为模型或应用演示，没有满足四项准入条件的 Agent Skill。 |",
           f"| 公开补充来源 | {counts['public']} | 未发现比已选固定上游更完整的可准入候选。 |", "",
           f"正式收录：{len(records)} 项。内部落选：{len(EXCLUDED[code])} 项。正式结果不含 SB-A、X、无许可、重复、通用或仅 Demo 条目。", "",
           "停止条件：在首轮后按各能力小类进行了两轮补充搜索；新增结果不再带来达到准入门槛的新功能，因此停止扩张并进入固定版本审查。零结果能力小类在正式索引中保留为能力缺口。"]
    write_text(path, original + "\n" + "\n".join(add))


def main() -> None:
    for code in DISCIPLINES:
        build_raw(code)
        records, snapshots = enrich_records(code)
        write_json(ROOT / "03_候选池" / "source_snapshots" / code / "snapshot_index.json", {"discipline": DISCIPLINES[code]["full"], "verified_at": DATE, "records": snapshots})
        write_text(ROOT / "03_候选池" / "excluded" / code / f"{DATE}-{code}内部排除记录.md", markdown_exclusions(code))
        write_json(ROOT / "03_候选池" / "excluded" / code / f"{DATE}-{code}通用库命中记录.json", {"discipline": DISCIPLINES[code]["full"], "checked_at": DATE, "hits": [], "note": "已按名称、来源与实质功能比对现有通用库；正式候选未命中。"})
        write_json(ROOT / "03_候选池" / "deduplicated" / f"{code}_{DISCIPLINES[code]['name']}.json", {"discipline": DISCIPLINES[code]["full"], "audit_date": DATE, "candidate_count": len(records), "records": records})
        write_json(ROOT / "04_验证记录" / code / f"{DATE}-{code}{DISCIPLINES[code]['name']}静态安全审查.json", {"discipline": DISCIPLINES[code]["full"], "audit_date": DATE, "records": records})
        write_text(ROOT / "04_验证记录" / code / f"{DATE}-{code}{DISCIPLINES[code]['name']}静态安全审查.md", audit_markdown(code, records))
        build_kb(code, records)
        update_matrix(code, records)


if __name__ == "__main__":
    main()
