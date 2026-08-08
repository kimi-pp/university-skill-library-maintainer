#!/usr/bin/env python3
"""Generate the formal FD06 Markdown knowledge base from the frozen catalog."""

from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "06_过程记录" / "fd06_catalog.json"
KB_ROOT = ROOT / "02_知识库" / "functional_domains" / "06_课程设计教学材料与教学评估"
DATE = "2026-08-09"

SUBCATEGORIES = {
    "06-01": ("课程体系、目标与能力设计", "06-01_课程体系目标与能力设计"),
    "06-02": ("教学大纲、教案与课时规划", "06-02_教学大纲教案与课时规划"),
    "06-03": ("讲义、课件与阅读材料", "06-03_讲义课件与阅读材料"),
    "06-04": ("案例、实验、讨论与课堂活动", "06-04_案例实验讨论与课堂活动"),
    "06-05": ("作业、测验与考试命题", "06-05_作业测验与考试命题"),
    "06-06": ("作业批改与形成性反馈", "06-06_作业批改与形成性反馈"),
    "06-07": ("评分量规与评价方案", "06-07_评分量规与评价方案"),
    "06-08": ("考试评卷、成绩分析与学情诊断", "06-08_考试评卷成绩分析与学情诊断"),
    "06-09": ("个性化、无障碍与多语言教学适配", "06-09_个性化无障碍与多语言教学适配"),
    "06-10": ("课程质量、教学反思与持续改进", "06-10_课程质量教学反思与持续改进"),
    "06-11": ("课程论文与毕业论文评阅", "06-11_课程论文与毕业论文评阅"),
    "06-12": ("期刊与会议论文同行评审", "06-12_期刊与会议论文同行评审"),
}


def md_cell(value: object) -> str:
    if isinstance(value, list):
        value = "；".join(str(item) for item in value)
    return str(value).replace("|", "\\|").replace("\n", " ")


def rel_link(from_file: Path, to_file: Path) -> str:
    return Path(os.path.relpath(to_file, from_file.parent)).as_posix()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def skill_page(skill: dict) -> str:
    category_name, category_dir = SUBCATEGORIES[skill["primary_subcategory"]]
    page_path = KB_ROOT / "skills" / f'{skill["skill_id"]}.md'
    category_index = KB_ROOT / "subcategories" / category_dir / "INDEX.md"
    adaptation = skill["adaptation_requirements"] or ["无额外强制改造项；采用前仍应按本校制度复核。"]
    evidence_lines = []
    for raw_path in skill["evidence_paths"]:
        evidence = ROOT / raw_path
        if evidence.exists():
            evidence_lines.append(f"- [{evidence.name}]({rel_link(page_path, evidence)})")
        else:
            evidence_lines.append(f"- `{raw_path}`")
    return f"""# {skill['skill_id']} {skill['name']}

最后更新：{DATE}

返回：[本小分类]({rel_link(page_path, category_index)}) · [FD06 总入口](../INDEX.md)

## 它能做什么

{skill['plain_function']}

{skill['detailed_function']}

## 谁适合在什么情况下使用

- 适用对象：{md_cell(skill['audience'])}
- 典型场景：{skill['when_to_use']}
- 使用前准备：{skill['inputs']}
- 可得到的结果：{skill['outputs']}

## 使用边界

{skill['limitations']}

- 人工复核：{skill['human_review']}
- 公平与无障碍：{skill['fairness_accessibility']}
- 学术诚信：{skill['academic_integrity']}
- 外来材料处理：{skill['untrusted_input']}
- 敏感数据：{skill['sensitive_data']}

## 采用与安全建议

- 采用建议：**{skill['adoption_level']}**
- 安全等级：**{skill['security_grade']}**
- 通俗结论：{skill['security_plain']}
- 需要落实的改造：{'；'.join(adaptation)}
- 核验深度：{skill['verification_depth']}
- 联网行为：{skill['network_behavior']}
- 账号或密钥：{skill['credential_behavior']}
- 文件行为：{skill['file_behavior']}

## 来源与追溯

- 来源平台：{skill['source_label']}
- 维护者：{skill['maintainer']}
- 仓库或项目：{skill['repository']}
- 固定版本：`{skill['fixed_version']}`
- 许可证：{skill['license']}
- 核验日期：{skill['verified_at']}
- 原始地址：[打开公开来源]({skill['canonical_url']})

证据文件：

{chr(10).join(evidence_lines)}
"""


def generate() -> dict:
    skills = json.loads(CATALOG.read_text(encoding="utf-8"))
    grouped: dict[str, list[dict]] = defaultdict(list)
    for skill in skills:
        grouped[skill["primary_subcategory"]].append(skill)
        write(KB_ROOT / "skills" / f'{skill["skill_id"]}.md', skill_page(skill))

    all_index = [
        "# FD06 正式技能页总索引",
        "",
        f"最后更新：{DATE}",
        "",
        "本索引只列入通过静态安全准入的正式技能。落选、重复、SC 和 SX 条目不在这里出现。",
        "",
    ]
    for code, (name, _) in SUBCATEGORIES.items():
        all_index.extend([f"## {code} {name}", ""])
        all_index.extend(
            f"- [{item['skill_id']} {item['name']}]({item['skill_id']}.md) — {item['plain_function']}"
            for item in grouped[code]
        )
        all_index.append("")
    write(KB_ROOT / "skills" / "INDEX.md", "\n".join(all_index))

    subcategory_index = [
        "# FD06 十二个小分类索引",
        "",
        f"最后更新：{DATE}",
        "",
        "| 编号 | 小分类 | 正式技能数 | SA | SB | SB-A | 入口 |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for code, (name, dirname) in SUBCATEGORIES.items():
        rows = grouped[code]
        grades = Counter(item["security_grade"] for item in rows)
        subcategory_index.append(
            f"| {code} | {name} | {len(rows)} | {grades['SA']} | {grades['SB']} | {grades['SB-A']} | "
            f"[进入](subcategories/{dirname}/INDEX.md) |"
        )

        category_lines = [
            f"# {code} {name}",
            "",
            f"最后更新：{DATE}",
            "",
            f"本小分类共收录 **{len(rows)}** 项正式技能。它们均完成固定版本静态检查，未安装、未运行。",
            "",
            "| Skill ID | 名称 | 通俗功能 | 采用建议 | 安全等级 | 来源 |",
            "|---|---|---|---|---|---|",
        ]
        for item in rows:
            category_lines.append(
                f"| [{item['skill_id']}](../../skills/{item['skill_id']}.md) | {md_cell(item['name'])} | "
                f"{md_cell(item['plain_function'])} | {item['adoption_level']} | {item['security_grade']} | "
                f"[公开地址]({item['canonical_url']}) |"
            )
        category_lines.extend(["", "返回：[十二个小分类](../../SUBCATEGORY_INDEX.md) · [FD06 总入口](../../INDEX.md)"])
        write(KB_ROOT / "subcategories" / dirname / "INDEX.md", "\n".join(category_lines))

    subcategory_index.extend(["", f"当前正式技能合计：**{len(skills)}**。"])
    write(KB_ROOT / "SUBCATEGORY_INDEX.md", "\n".join(subcategory_index))

    grades = Counter(item["security_grade"] for item in skills)
    main_lines = [
        "# 06 课程设计、教学材料与教学评估",
        "",
        f"最后更新：{DATE}",
        "",
        "## 本轮结果",
        "",
        f"全网公开来源调研已完成，共有 **{len(skills)}** 项技能进入正式目录。安全等级分布为 SA {grades['SA']} 项、SB {grades['SB']} 项、SB-A {grades['SB-A']} 项。全部仅做固定版本说明读取、文件拆包和静态安全审查，未安装、未运行。",
        "",
        "正式目录不含落选、重复、SC 或 SX 条目。SB-A 表示原技能需要按列出的要求重新改造后才能接入学校环境，并不表示已经完成改造。",
        "",
        "## 快速入口",
        "",
        "- [十二个小分类及数量](SUBCATEGORY_INDEX.md)",
        "- [298 项正式技能页总索引](skills/INDEX.md)",
        "- [固定版本来源快照索引](SOURCE_SNAPSHOT_INDEX.md)",
        "- [全网检索矩阵](../../findings/2026-08-08-FD06全网检索矩阵.md)",
        "- [静态安全审查总表](../../../04_验证记录/2026-08-08-FD06静态安全审查.md)",
        "- [内部落选记录](../../../06_过程记录/2026-08-08-FD06内部落选记录.md)",
        "",
        "## 小分类导航",
        "",
    ]
    main_lines.extend(
        f"- [{code} {name}](subcategories/{dirname}/INDEX.md)（{len(grouped[code])} 项）"
        for code, (name, dirname) in SUBCATEGORIES.items()
    )
    main_lines.extend([
        "",
        "## 阅读顺序",
        "",
        "先在小分类入口按任务找到候选，再打开单项技能页查看适用对象、输入输出、使用边界、安全等级、改造要求和固定版本来源。涉及学生成绩、未公开论文、个人信息或最终评价决定时，必须由有权限的教师或评审人员复核。",
    ])
    write(KB_ROOT / "INDEX.md", "\n".join(main_lines))

    assert len(list((KB_ROOT / "skills").glob("FD-06-*.md"))) == len(skills)
    assert len(list((KB_ROOT / "subcategories").glob("*/INDEX.md"))) == len(SUBCATEGORIES)
    return {
        "skills": len(skills),
        "subcategory_indexes": len(SUBCATEGORIES),
        "grades": dict(sorted(grades.items())),
    }


if __name__ == "__main__":
    print(json.dumps(generate(), ensure_ascii=False, sort_keys=True))
