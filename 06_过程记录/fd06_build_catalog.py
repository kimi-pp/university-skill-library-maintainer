#!/usr/bin/env python3
"""Build the formal FD06 catalog from deduplicated candidates and static audits."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
DEDUP = ROOT / "03_候选池" / "deduplicated" / "fd06.json"
AUDIT = ROOT / "04_验证记录" / "2026-08-08-FD06静态安全审查.json"
OUTPUT = ROOT / "06_过程记录" / "fd06_catalog.json"
FORMAL_GRADES = {"SA", "SB", "SB-A"}


SUBCATEGORIES: dict[str, dict[str, Any]] = {
    "06-01": {
        "name": "课程体系、目标与能力设计",
        "audience": ["教师", "专业负责人", "教学管理人员"],
        "when": "需要规划一门课程或一组课程的学习目标、能力要求、前后衔接和认证对应关系时",
        "inputs": "培养目标、课程定位、学生基础、课程清单、认证或学校要求",
        "outputs": "课程目标、能力矩阵、课程地图、内容缺口和调整建议",
        "default": ["梳理课程目标与学生能力", "检查课程之间的衔接", "把课程要求与认证标准对应起来"],
    },
    "06-02": {
        "name": "教学大纲、教案与课时规划",
        "audience": ["教师", "助教", "课程负责人"],
        "when": "需要把课程目标细化为教学大纲、教案、单元安排或逐周课时计划时",
        "inputs": "课程目标、教学周数、学生层次、授课方式和学校模板",
        "outputs": "教学大纲、教案、周计划、课时安排和教学进度表",
        "default": ["编写教学大纲", "安排单元与课时", "检查目标、活动和评价是否一致"],
    },
    "06-03": {
        "name": "讲义、课件与阅读材料",
        "audience": ["教师", "助教", "学生"],
        "when": "需要制作或整理讲义、课件、学习指南、阅读清单和自学材料时",
        "inputs": "课程主题、学习目标、已有资料、学生层次和希望采用的文件格式",
        "outputs": "讲义提纲、课件、学习指南、阅读清单、示例和练习材料",
        "default": ["把课程内容整理成易读材料", "制作讲义或课件", "补充阅读与学习提示"],
    },
    "06-04": {
        "name": "案例、实验、讨论与课堂活动",
        "audience": ["教师", "助教", "课程设计人员"],
        "when": "需要设计案例、实验、讨论、角色扮演、项目或其他课堂活动时",
        "inputs": "学习目标、课程主题、课堂时长、学生人数和可用条件",
        "outputs": "活动说明、案例材料、讨论问题、实验步骤、时间安排和教师提示",
        "default": ["设计参与式课堂活动", "编写案例或实验步骤", "准备讨论问题和课堂引导"],
    },
    "06-05": {
        "name": "作业、测验与考试命题",
        "audience": ["教师", "助教", "考试命题人员"],
        "when": "需要围绕学习目标编制作业、练习题、测验或考试题，并检查题目质量时",
        "inputs": "学习目标、知识范围、题型、难度、分值和参考资料",
        "outputs": "题目、答案要点、难度说明、分值建议和题目质量检查结果",
        "default": ["生成作业或考试题", "为题目配答案与分值", "检查难度和知识覆盖"],
    },
    "06-06": {
        "name": "作业批改与形成性反馈",
        "audience": ["教师", "助教", "学生"],
        "when": "需要依据明确标准检查学生作业并形成可操作的改进意见时",
        "inputs": "去标识的学生作业、题目要求、评分标准和课程目标",
        "outputs": "批改建议、错误说明、形成性反馈、修改方向和供教师确认的分数建议",
        "default": ["按标准检查学生作业", "指出问题并解释原因", "提供下一步改进建议"],
    },
    "06-07": {
        "name": "评分量规与评价方案",
        "audience": ["教师", "助教", "教学评价人员"],
        "when": "需要设计、改写或检查评分量规、评价指标和评价方案时",
        "inputs": "学习目标、任务说明、质量标准、分值和评价用途",
        "outputs": "评分维度、表现等级、分值说明、评分量规和公平性检查建议",
        "default": ["设计评分量规", "说明不同表现等级", "检查标准是否清楚、公平和可操作"],
    },
    "06-08": {
        "name": "考试评卷、成绩分析与学情诊断",
        "audience": ["教师", "助教", "教学管理人员"],
        "when": "需要汇总评卷结果、分析成绩分布、发现学习薄弱点或识别需要支持的学生群体时",
        "inputs": "去标识的答题结果、成绩表、题目知识点、班级信息和分析口径",
        "outputs": "成绩统计、题目分析、学习薄弱点、群体差异和教学调整建议",
        "default": ["汇总和解释成绩", "分析题目与知识点表现", "发现学习薄弱点和支持需求"],
    },
    "06-09": {
        "name": "个性化、无障碍与多语言教学适配",
        "audience": ["教师", "助教", "学生支持人员"],
        "when": "需要为不同基础、语言、学习需要或无障碍要求调整教学材料和活动时",
        "inputs": "原教学材料、学生需要、语言要求、无障碍要求和课程目标",
        "outputs": "分层版本、多语言材料、无障碍改写、替代活动和个性化支持建议",
        "default": ["为不同学生调整难度和支持", "制作多语言或易读版本", "检查无障碍与包容性"],
    },
    "06-10": {
        "name": "课程质量、教学反思与持续改进",
        "audience": ["教师", "课程负责人", "教学管理人员"],
        "when": "需要评价课程或教案质量、分析教学反馈、进行教学反思并制定改进计划时",
        "inputs": "课程资料、教学反馈、评价数据、质量标准和改进目标",
        "outputs": "质量检查结果、问题清单、教学反思、改进优先级和后续行动计划",
        "default": ["检查课程和教学材料质量", "整理师生反馈", "形成持续改进计划"],
    },
    "06-11": {
        "name": "课程论文与毕业论文评阅",
        "audience": ["教师", "导师", "学位论文评审人员"],
        "when": "需要依据学校或专业标准评阅课程论文、毕业设计、硕士或博士学位论文时",
        "inputs": "去标识的论文、评阅标准、学位层次、专业要求和学校模板",
        "outputs": "结构化评阅意见、优点与不足、修改建议和供评审人确认的等级或分数建议",
        "default": ["检查论文选题、方法和论证", "评价创新、规范和完整性", "形成结构化评阅意见"],
    },
    "06-12": {
        "name": "期刊与会议论文同行评审",
        "audience": ["期刊审稿人", "会议评审人", "研究人员", "编辑"],
        "when": "需要为获准评阅的期刊或会议稿件准备同行评审草稿，或在投稿前模拟审稿时",
        "inputs": "获准使用的去标识稿件、期刊或会议要求、评审表和报告规范",
        "outputs": "同行评审草稿、主要问题、次要问题、方法与统计检查、修改优先级和供评审人确认的建议",
        "default": ["检查研究问题、方法和证据", "提出具体、可执行的修改意见", "形成结构化同行评审草稿"],
    },
}


FEATURE_RULES = [
    (r"accredit|认证|assurance.of.learning", "对应认证标准和学习成果要求"),
    (r"curriculum.map|mapping|课程地图", "制作课程或知识点对应关系"),
    (r"outcome|objective|learning.target|competenc|能力", "梳理学习目标和能力要求"),
    (r"gap|coverage|缺口", "发现内容覆盖不足和重复"),
    (r"backward|constructive.alignment|alignment", "检查目标、活动与评价是否相互支持"),
    (r"syllabus|教学大纲|course.outline", "编写或检查教学大纲"),
    (r"lesson.plan|教案|unit.plan", "编写教案和单元计划"),
    (r"schedule|semester|课时|weekly|week.by.week", "安排周次、课时和教学进度"),
    (r"slide|deck|ppt|课件", "制作或整理教学课件"),
    (r"reading|literature|文献|阅读", "准备阅读清单和阅读提示"),
    (r"study.guide|textbook|讲义|notes|course.material", "整理讲义、教材或学习指南"),
    (r"storyboard|video|recorded|media", "设计数字课程或教学视频脚本"),
    (r"worked.example|example|示例", "编写示例和逐步讲解"),
    (r"case|案例", "设计教学案例"),
    (r"lab|experiment|实验", "设计实验或实践步骤"),
    (r"discussion|socratic|debate|讨论", "准备讨论、提问或辩论活动"),
    (r"simulation|role.play|模拟|角色", "设计模拟或角色扮演"),
    (r"project|workshop|activity|活动", "设计项目、工作坊或课堂活动"),
    (r"quiz|question|item.development|题目|测验", "生成练习题或测验题"),
    (r"exam|summative|考试", "设计考试或终结性评价"),
    (r"formative|retrieval|mastery", "设计形成性练习和掌握度检查"),
    (r"grad|mark|批改|essay", "按标准检查作业并提出分数建议"),
    (r"feedback|反馈", "生成具体、可执行的学习反馈"),
    (r"rubric|criteria|评分标准|量规", "设计或使用评分量规"),
    (r"validat|moderation|一致性", "检查评价标准的清楚程度和一致性"),
    (r"analytics|成绩分析|learning.analytics|data.mining", "分析成绩和学习过程数据"),
    (r"risk|dropout|early.warning|预警", "识别可能需要支持的学生群体"),
    (r"diagnos|weakness|薄弱", "诊断知识薄弱点和教学问题"),
    (r"different|personal|adaptive|分层|个性", "按学生差异调整内容和支持"),
    (r"accessib|universal.design|\budl\b|无障碍", "检查并改善无障碍学习条件"),
    (r"multilingual|bilingual|language|翻译|双语", "制作多语言或双语教学材料"),
    (r"inclusive|cultural|equity|包容|公平", "检查包容性和公平性"),
    (r"quality|audit|evaluation|课程评价", "检查课程或教学材料质量"),
    (r"reflect|reflection|反思", "支持教学反思和改进记录"),
    (r"survey|course.evaluation|student.feedback", "整理课程评价和学生反馈"),
    (r"thesis|dissertation|学位论文|毕业论文", "评阅课程论文或学位论文"),
    (r"format|citation|reference|格式|引文", "检查格式、引文和参考文献"),
    (r"peer.review|reviewer|referee|manuscript|审稿", "准备同行评审或审稿意见"),
    (r"method|methodology|方法", "检查研究方法是否合适和完整"),
    (r"statistic|统计", "检查统计分析和结果解释"),
    (r"reproduc|code.paper|复现", "检查可复现性和论文与代码的一致性"),
    (r"ethic|integrity|伦理|学术诚信", "提示伦理、引用和学术诚信风险"),
]


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def infer_features(candidate: dict[str, Any]) -> list[str]:
    text = f"{candidate.get('name', '')} {candidate.get('claimed_function', '')}".lower()
    features = [label for pattern, label in FEATURE_RULES if re.search(pattern, text, re.I)]
    defaults = SUBCATEGORIES[candidate["primary_subcategory"]]["default"]
    return unique(features + defaults)[:4]


def adoption_level(grade: str) -> str:
    return {"SA": "可直接使用", "SB": "需要少量调整", "SB-A": "需要重新改造"}[grade]


def source_label(source_kind: str) -> str:
    return {
        "github": "GitHub 固定提交版本",
        "huggingface_space": "Hugging Face Space 固定版本",
        "clawhub_registry": "ClawHub 固定注册表版本",
    }.get(source_kind, source_kind)


def normalize_url(value: str) -> str:
    """Return a standards-compliant URL without changing its destination."""
    parts = urlsplit(value)
    encoded_path = quote(parts.path, safe="/%:@")
    return urlunsplit((parts.scheme, parts.netloc, encoded_path, parts.query, parts.fragment))


def build_skill(candidate: dict[str, Any], audit: dict[str, Any], index: int) -> dict[str, Any]:
    code = candidate["primary_subcategory"]
    meta = SUBCATEGORIES[code]
    features = infer_features(candidate)
    grade = audit["security_grade"]
    function_text = "、".join(features)
    plain_function = f"这个技能主要用于{meta['name']}。它可以帮助使用者{function_text}。"
    detailed_function = (
        f"它围绕“{meta['name']}”组织工作。通常先读取使用者提供的目标、材料或评价标准，"
        f"再依次{function_text}，最后把结果整理成便于教师或评审人员继续修改和确认的草稿。"
    )
    if grade == "SB-A":
        limitation = "原项目不能直接接入学校环境；必须先按清单删除或改写联网、账号、自动决定或外部写回步骤。"
    elif grade == "SB":
        limitation = "采用前仍要按本校课程模板、评价制度、数据管理要求和实际工具做少量调整。"
    else:
        limitation = "静态检查未发现阻断性问题，但输出仍是辅助草稿，不能替代教师、导师、审稿人或编辑的专业判断。"
    if code in {"06-05", "06-06", "06-07", "06-08"}:
        limitation += " 涉及分数、学情或学生权益时，要保留评分依据、人工复核和申诉渠道。"
    if code in {"06-11", "06-12"}:
        limitation += " 涉及未公开论文时，要遵守保密、匿名评阅和利益冲突要求。"
    security_plain = f"安全等级 {grade}：{audit['plain_conclusion']}"
    return {
        "skill_id": f"FD-06-{index:04d}",
        "name": candidate["name"],
        "primary_subcategory": code,
        "secondary_tags": features,
        "plain_function": plain_function,
        "detailed_function": detailed_function,
        "audience": meta["audience"],
        "when_to_use": meta["when"],
        "inputs": meta["inputs"],
        "outputs": meta["outputs"],
        "limitations": limitation,
        "sensitive_data": audit["sensitive_data_observation"],
        "adoption_level": adoption_level(grade),
        "security_grade": grade,
        "security_plain": security_plain,
        "verification_depth": audit["verification_depth"],
        "canonical_url": normalize_url(audit["canonical_url"]),
        "fixed_version": str(audit["fixed_version"]),
        "verified_at": audit["verified_at"],
        "license": audit["license"],
        "maintainer": audit["maintainer"],
        "network_behavior": audit["network_behavior"],
        "credential_behavior": audit["credential_behavior"],
        "file_behavior": audit["file_behavior"],
        "evidence_paths": unique(audit["evidence_paths"]),
        "candidate_id": candidate["candidate_id"],
        "subcategory_name": meta["name"],
        "source_kind": audit["source_kind"],
        "source_label": source_label(audit["source_kind"]),
        "source_shape": audit["source_shape"],
        "repository": audit["repository"],
        "package_file_count": audit["package_file_count"],
        "adaptation_requirements": audit.get("adaptation_requirements", []),
        "human_review": audit["human_review_observation"],
        "fairness_accessibility": audit["fairness_accessibility_observation"],
        "untrusted_input": audit["untrusted_input_observation"],
        "academic_integrity": audit["academic_integrity_observation"],
    }


def build_catalog(candidates: list[dict[str, Any]], audits: list[dict[str, Any]]) -> dict[str, Any]:
    candidate_by_id = {item["candidate_id"]: item for item in candidates}
    formal_audits = [item for item in audits if item.get("security_grade") in FORMAL_GRADES]
    formal_audits.sort(
        key=lambda item: (
            item["primary_subcategory"],
            item["name"].casefold(),
            item["canonical_url"],
        )
    )
    skills = []
    for index, audit in enumerate(formal_audits, 1):
        candidate = candidate_by_id[audit["candidate_id"]]
        skills.append(build_skill(candidate, audit, index))
    return {
        "generated_at": max((item["verified_at"] for item in formal_audits), default=""),
        "skills": skills,
        "counts": {
            "total": len(skills),
            "by_subcategory": dict(sorted(Counter(item["primary_subcategory"] for item in skills).items())),
            "by_security_grade": dict(sorted(Counter(item["security_grade"] for item in skills).items())),
            "by_adoption_level": dict(sorted(Counter(item["adoption_level"] for item in skills).items())),
        },
    }


def main() -> None:
    candidates = json.loads(DEDUP.read_text(encoding="utf-8"))
    audits = json.loads(AUDIT.read_text(encoding="utf-8"))
    catalog = build_catalog(candidates, audits)
    OUTPUT.write_text(
        json.dumps(catalog["skills"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(catalog["counts"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
