from __future__ import annotations

import json
import re
import subprocess
from datetime import date
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "03_候选池" / "raw" / "2026-08-08-fd06-discovery.jsonl"


REPOSITORY_SPECS = [
    {"repo": "GarethManning/education-agent-skills", "mode": "gareth_registry"},
    {"repo": "YujxZJCN/teaching-skills", "mode": "all_skills"},
    {"repo": "YujxZJCN/teaching-skills-codex", "paths": ["skills/teaching-suite/SKILL.md"]},
    {
        "repo": "anthropics/k12-teacher-skills",
        "paths": [
            "plugin/skills/k12-lesson-planning/SKILL.md",
            "plugin/skills/k12-lesson-differentiation/SKILL.md",
        ],
    },
    {
        "repo": "learning-commons-org/agent-skills",
        "paths": [
            "skills/k12-lesson-planning/SKILL.md",
            "skills/k12-lesson-differentiation/SKILL.md",
        ],
    },
    {"repo": "Jellypod-Inc/school-skills", "mode": "all_skills"},
    {"repo": "alirezarezvani/claude-skills", "paths": ["research/syllabus/skills/syllabus/SKILL.md"]},
    {"repo": "K-Dense-AI/claude-scientific-skills", "paths": ["skills/peer-review/SKILL.md"]},
    {"repo": "bytedance/deer-flow", "paths": ["skills/public/academic-paper-review/SKILL.md"]},
    {"repo": "Imbad0202/academic-research-skills", "paths": ["academic-paper-reviewer/SKILL.md"]},
    {"repo": "BESSER-PEARL/research-agent-skills", "paths": ["research-paper-review/SKILL.md"]},
    {"repo": "AlexWortega/ai-peer-review-skill", "paths": ["SKILL.md"]},
    {"repo": "Yuan1z0825/nature-skills", "paths": ["skills/nature-reviewer/SKILL.md"]},
    {"repo": "Agents365-ai/thesis-reviewer", "paths": ["SKILL.md"]},
    {"repo": "rudini/claude-edu-plugins", "mode": "all_skills"},
    {
        "repo": "sickn33/antigravity-awesome-skills",
        "paths": [
            "skills/examprep-ai/SKILL.md",
            "skills/lesson-generator/SKILL.md",
            "skills/teach/SKILL.md",
        ],
    },
    {
        "repo": "aiskillstore/marketplace",
        "paths": [
            "skills/92bilal26/ai-collaborate-teaching/SKILL.md",
            "skills/92bilal26/assessment-builder/SKILL.md",
            "skills/92bilal26/quiz-generator/SKILL.md",
            "skills/92bilal26/content-evaluation-framework/SKILL.md",
            "skills/yunshu0909/lesson-builder/SKILL.md",
            "skills/davila7/peer-review/SKILL.md",
            "skills/k-dense-ai/peer-review/SKILL.md",
            "skills/yuan1z0825/nature-reviewer/SKILL.md",
        ],
    },
    {
        "repo": "srednoff888-art/srednoff-os",
        "paths": [".codex/skills/education-ai-guardrails/SKILL.md"],
    },
    {
        "repo": "dmccreary/claude-skills",
        "paths": [
            "skills/course-description-analyzer/SKILL.md",
            "skills/quiz-generator/SKILL.md",
        ],
    },
    {
        "repo": "lyndonkl/claude",
        "paths": [
            "skills/abstraction-concrete-examples/SKILL.md",
            "skills/chain-roleplay-debate-synthesis/SKILL.md",
            "skills/evaluation-rubrics/SKILL.md",
            "skills/experiential-kolb-teaching/SKILL.md",
            "skills/mastery-assessment/SKILL.md",
            "skills/scientific-manuscript-review/SKILL.md",
            "skills/section-portfolio-assessment/SKILL.md",
            "skills/socratic-teaching-scaffolds/SKILL.md",
            "skills/worked-example-walkthrough/SKILL.md",
        ],
    },
    {"repo": "zarazhangrui/codebase-to-course", "paths": ["SKILL.md"]},
    {"repo": "labarba/sciwrite", "paths": ["SKILL.md"]},
    {"repo": "wmpluto/academic-thesis-review-skill", "paths": ["SKILL.md"]},
    {"repo": "zyan421/unified-thesis-reviewer", "paths": ["SKILL.md"]},
    {"repo": "Lidong-Huang/thesis_format_check", "paths": ["SKILL.md"]},
    {"repo": "1carusalwayswa/cs-thesis-reviewer", "paths": ["SKILL.md"]},
    {
        "repo": "yylonly/buaa-thesis-checker",
        "paths": [
            "skills/buaa-thesis-checking/SKILL.md",
            "skills/buaa-thesis-content-checking/SKILL.md",
            "skills/buaa-thesis-format-checking/SKILL.md",
            "skills/icse-seet-review/SKILL.md",
        ],
    },
    {
        "repo": "brycewang-stanford/Auto-Empirical-Research-Skills",
        "paths": ["skills/67-econfin-workflow-toolkit/master-thesis-review/SKILL.md"],
    },
    {
        "repo": "affaan-m/everything-claude-code",
        "paths": ["skills/scientific-thinking-scholar-evaluation/SKILL.md"],
    },
    {"repo": "AlemTuzlak/skills", "paths": ["skills/teach-me/SKILL.md"]},
    {
        "repo": "jeremiahvanwagner-droid/openclaw",
        "paths": [
            "skills/curriculum-generator/SKILL.md",
            "skills/education-adaptive-curriculum-sequencing/SKILL.md",
            "skills/education-automated-assessment-generation/SKILL.md",
            "skills/education-interactive-assignment-grading/SKILL.md",
            "skills/education-micro-lesson-atomization/SKILL.md",
            "skills/education-performance-rubric-application/SKILL.md",
        ],
    },
    {
        "repo": "argythana/uoa_py_course",
        "paths": [
            ".claude/skills/uoa-py-course-create-excellent-lecture/SKILL.md",
            ".claude/skills/uoa-py-course-final-assignment-feedback/SKILL.md",
            ".claude/skills/uoa-py-course-final-assignment-grade/SKILL.md",
            ".claude/skills/uoa-py-course-lecture-eval/SKILL.md",
            ".claude/skills/uoa-py-course-lecture-outline/SKILL.md",
            ".claude/skills/uoa-py-course-update-lecture-post-teaching/SKILL.md",
        ],
    },
    {
        "repo": "francojc/dauber",
        "paths": [
            ".pi/skills/assess-ai-pass/SKILL.md",
            ".pi/skills/assess-refine/SKILL.md",
            ".pi/skills/assess-setup/SKILL.md",
            ".pi/skills/assess-submit/SKILL.md",
            ".pi/skills/course-overview/SKILL.md",
            ".pi/skills/course-setup/SKILL.md",
            ".pi/skills/grading-overview/SKILL.md",
            ".pi/skills/rubrics-create/SKILL.md",
        ],
    },
    {
        "repo": "revfactory/harness-100",
        "paths": [
            "en/08-course-builder/.claude/skills/assessment-engineering/skill.md",
            "en/08-course-builder/.claude/skills/course-builder/skill.md",
            "en/08-course-builder/.claude/skills/lab-scaffolding/skill.md",
            "en/08-course-builder/.claude/skills/learning-design/skill.md",
        ],
    },
    {
        "repo": "mohitagw15856/pm-claude-skills",
        "paths": [
            "plugins/pm-teaching/skills/lesson-plan-builder/SKILL.md",
            "plugins/pm-cross/skills/teaching-lesson-plan/SKILL.md",
            "plugins/pm-education/skills/student-feedback/SKILL.md",
            "skills/lesson-plan/SKILL.md",
        ],
    },
    {
        "repo": "piriya33/antigravity-skills",
        "paths": [
            "education-stack/aligning-curriculum/SKILL.md",
            "education-stack/planning-courses/SKILL.md",
        ],
    },
    {"repo": "kc0506/ntucool", "paths": ["plugins/ntucool/skills/ntucool/SKILL.md"]},
    {
        "repo": "pengkangzhen/academic-review-skill",
        "paths": ["skills/academic-reviewer-or/SKILL.md"],
    },
    {"repo": "shaowen-ye/manuscript-review-skill", "paths": ["SKILL.md"]},
    {
        "repo": "cmertdalli/polisci-review",
        "paths": [
            "adapters/claude-skill/polisci-review/SKILL.md",
            "adapters/codex-skill/polisci-review/SKILL.md",
        ],
    },
    {
        "repo": "richard-kim-79/archora-skills",
        "paths": ["skills/peer-review/SKILL.md"],
    },
    {
        "repo": "claesbackman/AI-research-feedback",
        "paths": [
            "Skills/review-pap/SKILL.md",
            "Skills/review-paper-code/SKILL.md",
            "Skills/review-paper-light/SKILL.md",
            "Skills/review-paper/SKILL.md",
        ],
    },
    {
        "repo": "aipoch/medical-research-skills",
        "paths": [
            "scientific-skills/Academic Writing/peer-review/SKILL.md",
            "scientific-skills/Academic Writing/peer-review-response-drafter/SKILL.md",
        ],
    },
    {
        "repo": "MattArtzAnthro/AI-Anthropology-Toolkit",
        "paths": ["skills/academic-review/SKILL.md"],
    },
    {
        "repo": "HaipingXu/social-science-claude-scholar",
        "paths": ["skills/review-paper/SKILL.md"],
    },
    {
        "repo": "caishengold/ai-agent-ops",
        "paths": ["skills/edu-course-designer/SKILL.md"],
    },
    {
        "repo": "tobiasblask/open-paper-machine",
        "paths": [
            "scientific-skills/peer-review/SKILL.md",
            "skills/peer-review-engine/SKILL.md",
        ],
    },
    {
        "repo": "tinh2/skills-hub-registry",
        "paths": ["analysis/student-personalization/SKILL.md"],
    },
]


MANUAL_DISCOVERIES = [
    {
        "query": "learning assessor grading rubric educational assessment skill",
        "source_path": "skill_market",
        "discovery_url": "https://mcpmarket.com/tools/skills/learning-assessor-1",
        "title": "Learning Assessor",
        "claimed_function": "设计测验、考试、评分标准表，并根据结果生成学习分析和改进反馈。",
        "proposed_subcategory": "06-05",
        "upstream_hint": "partme-ai；原始公开仓库仍需回溯",
        "evidence_level": "discovery_only",
    },
    {
        "query": "education grading open source skill Moodle assignment feedback",
        "source_path": "public_project_page",
        "discovery_url": "https://rudini.github.io/claude-edu-plugins/",
        "title": "Claude Edu Plugins public project page",
        "claimed_function": "管理 Moodle 作业、批改、成绩册和题库，也能创建并发布 Kahoot 测验。",
        "proposed_subcategory": "06-06",
        "upstream_hint": "https://github.com/rudini/claude-edu-plugins",
        "evidence_level": "discovery_page_with_versioned_upstream",
    },
    {
        "query": "Hugging Face open source essay grader rubric",
        "source_path": "huggingface_space",
        "discovery_url": "https://huggingface.co/spaces/lowrollr/essay_grader/tree/main",
        "title": "lowrollr/essay_grader",
        "claimed_function": "根据作文题目和评分标准辅助给作文评分。",
        "proposed_subcategory": "06-06",
        "upstream_hint": "Hugging Face Space；需固定提交并检查数据上传和模型调用",
        "evidence_level": "versioned_host_to_review",
    },
    {
        "query": "Hugging Face Canvas discussion grader feedback",
        "source_path": "huggingface_space",
        "discovery_url": "https://huggingface.co/spaces/rohan13/canvas-discussion-grader-with-feedback",
        "title": "Canvas Discussion Grader with Feedback",
        "claimed_function": "读取 Canvas 讨论区作业，按评分标准给出分数拆分和学生反馈。",
        "proposed_subcategory": "06-06",
        "upstream_hint": "Hugging Face Space；需检查学生数据、OpenAI 调用和成绩写回",
        "evidence_level": "versioned_host_to_review",
    },
    {
        "query": "Hugging Face open source syllabus generator",
        "source_path": "huggingface_space",
        "discovery_url": "https://huggingface.co/spaces/SyllabusCraft/SyllabusGenerator/tree/main",
        "title": "SyllabusCraft/SyllabusGenerator",
        "claimed_function": "根据课程主题和基本要求生成课程大纲。",
        "proposed_subcategory": "06-02",
        "upstream_hint": "Hugging Face Space；需固定提交并检查外部模型、文件写入和许可证",
        "evidence_level": "versioned_host_to_review",
    },
    {
        "query": "Hugging Face open source syllabus formatter",
        "source_path": "huggingface_space",
        "discovery_url": "https://huggingface.co/spaces/Kuberwastaken/Syllabus-Formatter/tree/main",
        "title": "Kuberwastaken/Syllabus-Formatter",
        "claimed_function": "读取课程大纲内容并整理为更统一、易读的格式。",
        "proposed_subcategory": "06-02",
        "upstream_hint": "Hugging Face Space；需固定提交并检查上传内容、生成服务和许可证",
        "evidence_level": "versioned_host_to_review",
    },
    {
        "query": "GitLab agent skill education SKILL.md curriculum grading rubric",
        "source_path": "gitlab_search",
        "discovery_url": "https://gitlab.com/search?search=SKILL.md%20education&nav_source=navbar",
        "title": "GitLab 教育技能组合检索",
        "claimed_function": "用于检查 GitLab 是否存在可回溯的课程设计、评价和评阅技能包。",
        "proposed_subcategory": None,
        "upstream_hint": "首轮未发现达到固定版本证据门槛的直接候选",
        "evidence_level": "search_path_no_formal_candidate_yet",
    },
    {
        "query": "Codeberg agent skill lesson curriculum assessment",
        "source_path": "codeberg_search",
        "discovery_url": "https://codeberg.org/explore/repos?q=agent+skill+education",
        "title": "Codeberg 教育技能组合检索",
        "claimed_function": "用于检查 Codeberg 是否存在可回溯的教学技能包。",
        "proposed_subcategory": None,
        "upstream_hint": "搜索访问受限，未把搜索摘要作为正式证据",
        "evidence_level": "search_path_access_limited",
    },
    {
        "query": "Gitee SKILL.md 教学 课程 评分 智能体",
        "source_path": "gitee_search",
        "discovery_url": "https://search.gitee.com/?q=SKILL.md%20%E6%95%99%E5%AD%A6",
        "title": "Gitee 教育技能组合检索",
        "claimed_function": "用于检查 Gitee 是否存在可回溯的中文教学技能包。",
        "proposed_subcategory": None,
        "upstream_hint": "首轮未发现达到固定版本证据门槛的直接候选",
        "evidence_level": "search_path_no_formal_candidate_yet",
    },
    {
        "query": "open academic agent skills index peer review thesis review teaching",
        "source_path": "curated_index",
        "discovery_url": "https://github.com/O0000-code/awesome-academic-skills",
        "title": "Awesome Academic Skills 索引",
        "claimed_function": "汇总学术工作公开技能，并标注许可证、联网、钩子和权限绕过等已披露能力；本项目只把它作为发现入口。",
        "proposed_subcategory": None,
        "upstream_hint": "每个候选必须继续回到原始仓库和固定提交版本核验",
        "evidence_level": "curated_discovery_index_only",
    },
    {
        "query": "open source academic teaching plugin syllabus exams grading feedback",
        "source_path": "plugin_directory",
        "discovery_url": "https://www.claudepluginhub.com/plugins/data-wise-scholar",
        "title": "Scholar teaching plugin directory page",
        "claimed_function": "生成统计学课程大纲、讲义、课件、作业、考试、评分标准和作业反馈，并支持 Canvas 导出。",
        "proposed_subcategory": "06-01",
        "upstream_hint": "目录页指向的 data-wise/scholar 仓库当前无法由 GitHub API 访问；未找到可固定的当前上游版本",
        "evidence_level": "discovery_page_upstream_unavailable",
    },
    {
        "query": "Gemini academic paper reviewer agent skill",
        "source_path": "skill_market",
        "discovery_url": "https://skillsmp.com/creators/davideriboli/gemini-cli-academic-research-skills/academic-paper-reviewer",
        "title": "Gemini CLI Academic Paper Reviewer directory page",
        "claimed_function": "对论文进行对抗式同行评审、引用核查和学术诚信审查。",
        "proposed_subcategory": "06-12",
        "upstream_hint": "目录页所列 GitHub 仓库当前无法访问，不能固定上游版本",
        "evidence_level": "discovery_page_upstream_unavailable",
    },
    {
        "query": "homework grading scanned assignments roster gradebook skill",
        "source_path": "skill_market",
        "discovery_url": "https://mcpmarket.com/tools/skills/homework-grading-workflow",
        "title": "Homework Grading Workflow directory page",
        "claimed_function": "把整批扫描作业按学生拆分，核对花名册并更新完成情况表格，强调人工确认姓名匹配。",
        "proposed_subcategory": "06-06",
        "upstream_hint": "目录页未给出可回溯的固定版本仓库；涉及学生姓名、作业扫描件和成绩表写入",
        "evidence_level": "discovery_only_high_privacy_risk",
    },
]


def gh_json(endpoint: str):
    completed = subprocess.run(
        ["gh", "api", endpoint],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(completed.stdout)


def gh_raw(repo: str, path: str, ref: str) -> str:
    completed = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{repo}/contents/{path}?ref={ref}",
            "-H",
            "Accept: application/vnd.github.raw+json",
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return None
    lines = match.group(1).splitlines()
    for index, line in enumerate(lines):
        prefix = f"{key}:"
        if not line.startswith(prefix):
            continue
        value = line[len(prefix) :].strip().strip("'\"")
        if value not in {"", ">", ">-", "|", "|-"}:
            return value
        continuation = []
        for following in lines[index + 1 :]:
            if following.startswith((" ", "\t")):
                continuation.append(following.strip())
            else:
                break
        return " ".join(continuation) or None
    return None


def first_heading(text: str, fallback: str) -> str:
    name = frontmatter_value(text, "name")
    if name:
        return name
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def first_description(text: str) -> str:
    description = frontmatter_value(text, "description")
    if description:
        return re.sub(r"\s+", " ", description).strip()
    body = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.DOTALL)
    for paragraph in re.split(r"\n\s*\n", body):
        cleaned = re.sub(r"^#+\s*", "", paragraph.strip())
        if cleaned and not cleaned.startswith(("```", "<")):
            return re.sub(r"\s+", " ", cleaned)[:1000]
    return "公开技能入口已发现，功能说明需要在固定版本静态核验阶段读取。"


def map_subcategory(repo: str, path: str, description: str) -> str | None:
    key = f"{repo}/{path} {description}".lower()
    normalized_path = path.replace("\\", "/").rstrip("/")
    path_parts = normalized_path.split("/")
    if normalized_path.lower().endswith("/skill.md") and len(path_parts) >= 2:
        skill_slug = path_parts[-2].lower()
    elif normalized_path.lower() == "skill.md":
        skill_slug = repo.rsplit("/", 1)[-1].lower()
    else:
        skill_slug = path_parts[-1].lower()

    if repo == "GarethManning/education-agent-skills" and len(path_parts) >= 3:
        domain = path_parts[-3].lower()
        domain_defaults = {
            "ai-learning-science": "06-09",
            "ai-literacy": "06-04",
            "curriculum-alignment": "06-01",
            "curriculum-assessment": "06-01",
            "eal-language-development": "06-09",
            "environmental-experiential-learning": "06-04",
            "explicit-instruction": "06-02",
            "global-cross-cultural-pedagogies": "06-04",
            "historical-thinking": "06-04",
            "inclusive-design": "06-09",
            "literacy-critical-thinking": "06-03",
            "memory-learning-science": "06-03",
            "montessori-alternative-approaches": "06-04",
            "original-frameworks": "06-04",
            "professional-learning": "06-10",
            "questioning-discussion": "06-04",
            "self-regulated-learning": "06-09",
            "student-learning": "06-09",
            "systems-thinking": "06-04",
            "wellbeing-motivation-agency": "06-09",
        }
        gareth_exceptions = {
            "ai-facilitated-collaborative-learning-designer": "06-04",
            "ai-feedback-design-principles": "06-06",
            "cognitive-tutoring-architecture-designer": "06-01",
            "digital-worked-example-sequence": "06-03",
            "erroneous-example-designer": "06-03",
            "formative-assessment-loop-designer": "06-06",
            "learning-analytics-interpretation-guide": "06-08",
            "metacognitive-monitoring-ai-contexts": "06-05",
            "productive-failure-desirable-difficulty-designer": "06-04",
            "self-explanation-prompt-designer": "06-03",
            "worked-example-to-problem-solving-transition-designer": "06-03",
            "ai-learning-boundary-mapper": "06-05",
            "disciplinary-ai-literacy-sequence-designer": "06-02",
            "prompt-literacy-sequence-designer": "06-02",
            "assessment-validity-checker": "06-10",
            "criterion-referenced-rubric-generator": "06-07",
            "differentiation-adapter": "06-09",
            "discipline-specific-critical-thinking-task-designer": "06-05",
            "formative-assessment-technique-selector": "06-05",
            "gap-analysis-from-student-work": "06-08",
            "project-brief-designer": "06-05",
            "checking-for-understanding-protocol-designer": "06-05",
            "practice-problem-sequence-designer": "06-05",
            "think-aloud-script-generator": "06-03",
            "cross-cultural-task-validity-checker": "06-09",
            "culturally-responsive-teaching-designer": "06-09",
            "central-historical-question-evaluator": "06-05",
            "document-based-lesson-designer": "06-02",
            "historical-document-set-curator": "06-03",
            "historical-source-adapter": "06-03",
            "historical-thinking-assessment-designer": "06-05",
            "historical-thinking-strategy-modelling-guide": "06-03",
            "critical-thinking-task-designer": "06-05",
            "media-literacy-deconstruction-protocol": "06-04",
            "source-credibility-evaluation-protocol": "06-04",
            "text-complexity-analyser": "06-09",
            "feedback-quality-analyser": "06-06",
            "interleaving-unit-planner": "06-02",
            "retrieval-practice-generator": "06-05",
            "spaced-practice-scheduler": "06-02",
            "mixed-age-learning-task-designer": "06-09",
            "three-part-lesson-designer": "06-02",
            "assessment-design-orchestrator": "06-07",
            "coherent-rubric-logic-builder": "06-07",
            "developmental-band-system-designer": "06-01",
            "developmental-progression-synthesis": "06-01",
            "dilemma-navigation-for-education-design": "06-01",
            "dispositional-knowledge-assessment-designer": "06-05",
            "inclusive-design-orchestrator": "06-09",
            "place-based-curriculum-orchestrator": "06-01",
            "learning-target-authoring-guide": "06-01",
            "single-point-rubric-designer": "06-07",
            "competency-framework-translator": "06-01",
            "pedagogical-content-knowledge-developer": "06-02",
            "hinge-question-designer": "06-05",
            "error-analysis-protocol": "06-08",
            "goal-setting-protocol-designer": "06-04",
            "metacognitive-prompt-library": "06-03",
            "study-strategy-selector": "06-03",
            "ai-claim-checker": "06-04",
            "confidence-calibration-check": "06-08",
            "explain-first-interrogator": "06-06",
            "productive-failure-protocol": "06-04",
            "retrieve-first-gate": "06-05",
            "stuck-and-error-diagnosis-coach": "06-06",
            "teach-back-evaluator": "06-05",
            "transfer-bridge": "06-05",
            "unassisted-evidence-checkpoint": "06-05",
            "weekly-agency-review": "06-08",
            "ladder-of-inference-reflection": "06-10",
            "awe-wonder-experience-designer": "06-04",
            "perma-based-lesson-designer": "06-02",
            "ruler-emotional-literacy-sequence": "06-04",
            "wellbeing-learning-connection-mapper": "06-01",
        }
        return gareth_exceptions.get(skill_slug, domain_defaults.get(domain))

    explicit = {
        "accreditation-mapper": "06-01",
        "course-designer": "06-01",
        "teaching-pipeline": "06-01",
        "lesson-builder": "06-02",
        "course-publisher": "06-03",
        "deck-studio": "06-03",
        "media-scripter": "06-03",
        "lab-forge": "06-04",
        "assessment-architect": "06-05",
        "assessment-builder": "06-05",
        "student-mentor": "06-06",
        "submission-auditor": "06-06",
        "ta-coordinator": "06-07",
        "cohort-analyst": "06-08",
        "bilingual-courseware": "06-09",
        "teaching-reflector": "06-10",
        "thesis-reviewer": "06-11",
        "academic-paper-review": "06-12",
        "academic-paper-reviewer": "06-12",
        "research-paper-review": "06-12",
        "ai-peer-review-skill": "06-12",
        "peer-review": "06-12",
        "nature-reviewer": "06-12",
        "k12-lesson-planning": "06-02",
        "k12-lesson-differentiation": "06-09",
        "lecture-to-study-guide": "06-03",
        "lesson-plan": "06-02",
        "concept-map": "06-03",
        "rubric": "06-07",
        "syllabus": "06-02",
        "moodle": "06-06",
        "kahoot": "06-05",
        "examprep-ai": "06-05",
        "lesson-generator": "06-02",
        "content-evaluation-framework": "06-10",
        "education-ai-guardrails": "06-10",
        "teaching-suite": "06-01",
        "course-description-analyzer": "06-01",
        "evaluation-rubrics": "06-07",
        "mastery-assessment": "06-05",
        "section-portfolio-assessment": "06-05",
        "experiential-kolb-teaching": "06-04",
        "socratic-teaching-scaffolds": "06-04",
        "worked-example-walkthrough": "06-03",
        "abstraction-concrete-examples": "06-03",
        "chain-roleplay-debate-synthesis": "06-04",
        "scientific-manuscript-review": "06-12",
        "codebase-to-course": "06-01",
        "sciwrite": "06-12",
        "academic-thesis-review-skill": "06-11",
        "unified-thesis-reviewer": "06-11",
        "thesis_format_check": "06-11",
        "cs-thesis-reviewer": "06-11",
        "master-thesis-review": "06-11",
        "buaa-thesis-checking": "06-11",
        "buaa-thesis-content-checking": "06-11",
        "buaa-thesis-format-checking": "06-11",
        "scientific-thinking-scholar-evaluation": "06-12",
        "teach-me": "06-03",
        "curriculum-generator": "06-01",
        "education-adaptive-curriculum-sequencing": "06-09",
        "education-automated-assessment-generation": "06-05",
        "education-interactive-assignment-grading": "06-06",
        "education-micro-lesson-atomization": "06-02",
        "education-performance-rubric-application": "06-06",
        "uoa-py-course-create-excellent-lecture": "06-03",
        "uoa-py-course-final-assignment-feedback": "06-06",
        "uoa-py-course-final-assignment-grade": "06-06",
        "uoa-py-course-lecture-eval": "06-10",
        "uoa-py-course-lecture-outline": "06-02",
        "uoa-py-course-update-lecture-post-teaching": "06-10",
        "assess-ai-pass": "06-10",
        "assess-refine": "06-10",
        "assess-setup": "06-05",
        "assess-submit": "06-05",
        "course-overview": "06-01",
        "course-setup": "06-01",
        "grading-overview": "06-06",
        "rubrics-create": "06-07",
        "assessment-engineering": "06-05",
        "course-builder": "06-01",
        "lab-scaffolding": "06-04",
        "learning-design": "06-01",
        "lesson-plan-builder": "06-02",
        "teaching-lesson-plan": "06-02",
        "ntucool": "06-06",
        "academic-reviewer-or": "06-12",
        "manuscript-review-skill": "06-12",
        "polisci-review": "06-12",
        "review-pap": "06-12",
        "review-paper-code": "06-12",
        "review-paper-light": "06-12",
        "review-paper": "06-12",
        "student-feedback": "06-06",
        "aligning-curriculum": "06-01",
        "planning-courses": "06-01",
        "academic-review": "06-12",
        "edu-course-designer": "06-01",
        "peer-review-engine": "06-12",
        "peer-review-response-drafter": "06-12",
        "icse-seet-review": "06-12",
        "student-personalization": "06-09",
    }
    if skill_slug in explicit:
        return explicit[skill_slug]

    rules = [
        ("06-11", r"thesis|dissertation|degree paper"),
        ("06-12", r"peer.review|manuscript.review|journal.review|conference.review|paper.review"),
        ("06-07", r"rubric|grading criteria|assessment criteria"),
        ("06-08", r"learning.analytics|cohort|grade analysis|student.performance|gap.analysis.from.student.work"),
        ("06-09", r"differenti|inclusive|udl|accessib|bilingual|multilingual|eal|language.development|cross.cultural|culturally.responsive"),
        ("06-10", r"reflect|lesson.observation|teacher.inquiry|teaching.evaluation|quality|feedback.quality|panel.review|lesson.study"),
        ("06-06", r"submission|student.work|homework|assignment.grad|formative.feedback|ai.feedback|feedback writing"),
        ("06-05", r"quiz|exam|assessment|question|retrieval.practice|practice.problem|validity.checker"),
        ("06-01", r"curriculum|competency|learning.target|learning.progression|scope.and.sequence|coverage.audit|kud.chart|developmental.band"),
        ("06-02", r"syllabus|lesson.plan|unit.plan|sequence.builder|spaced.practice|interleaving"),
        ("06-03", r"lecture|slides|study.guide|worked.example|think.aloud|sentence.frame|vocabulary|reading|scaffold"),
        ("06-04", r"activity|discussion|socratic|case|lab|project|inquiry|experiential|outdoor|service.learning|historical|systems.thinking|questioning"),
    ]
    for code, pattern in rules:
        if re.search(pattern, key):
            return code

    return None


def repository_skill_paths(repo: str, ref: str) -> list[str]:
    tree = gh_json(f"repos/{repo}/git/trees/{ref}?recursive=1")
    return sorted(
        item["path"]
        for item in tree.get("tree", [])
        if item.get("type") == "blob" and item["path"].endswith("SKILL.md")
    )


def github_records() -> Iterable[dict]:
    for spec in REPOSITORY_SPECS:
        requested_repo = spec["repo"]
        metadata = gh_json(f"repos/{requested_repo}")
        repo = metadata["full_name"]
        branch = metadata["default_branch"]
        commit = gh_json(f"repos/{repo}/commits/{branch}")["sha"]

        if spec.get("mode") == "gareth_registry":
            registry = json.loads(gh_raw(repo, "registry.json", commit))
            for item in registry["skills"]:
                path = item["path"]
                description = item["description"]
                yield {
                    "discovered_at": str(date.today()),
                    "query": "evidence-grounded education agent skills curriculum assessment teaching",
                    "source_path": "code_hosting_github",
                    "discovery_url": f"https://github.com/{repo}/blob/{commit}/{path}",
                    "title": item.get("display_name") or item["name"],
                    "claimed_function": description,
                    "proposed_subcategory": map_subcategory(repo, path, description),
                    "upstream_hint": f"https://github.com/{repo}@{commit}",
                    "evidence_level": "fixed_version_source_identified",
                }
            continue

        paths = spec.get("paths")
        if spec.get("mode") == "all_skills":
            paths = repository_skill_paths(repo, commit)
        if not paths:
            raise RuntimeError(f"No SKILL.md paths configured for {repo}")

        for path in paths:
            text = gh_raw(repo, path, commit)
            title = first_heading(text, Path(path).parent.name or repo.split("/")[-1])
            description = first_description(text)
            yield {
                "discovered_at": str(date.today()),
                "query": "SKILL.md education curriculum teaching grading peer review",
                "source_path": "code_hosting_github",
                "discovery_url": f"https://github.com/{repo}/blob/{commit}/{path}",
                "title": title,
                "claimed_function": description,
                "proposed_subcategory": map_subcategory(repo, path, description),
                "upstream_hint": f"https://github.com/{repo}@{commit}",
                "evidence_level": "fixed_version_source_identified",
            }


def main() -> None:
    records = list(github_records())
    for item in MANUAL_DISCOVERIES:
        records.append({"discovered_at": str(date.today()), **item})

    unique = {}
    for record in records:
        unique[record["discovery_url"]] = record
    ordered = sorted(
        unique.values(),
        key=lambda item: (
            item["proposed_subcategory"] or "99",
            item["source_path"],
            item["title"].casefold(),
            item["discovery_url"],
        ),
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for record in ordered:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    counts = {}
    for record in ordered:
        code = record["proposed_subcategory"] or "unmapped"
        counts[code] = counts.get(code, 0) + 1
    print(json.dumps({"records": len(ordered), "counts": counts}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
