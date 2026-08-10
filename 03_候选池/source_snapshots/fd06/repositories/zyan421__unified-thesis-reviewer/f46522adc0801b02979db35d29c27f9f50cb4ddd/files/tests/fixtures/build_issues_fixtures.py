#!/usr/bin/env python3
"""构造 issues.json 各类测试夹具（合法 / 违规 / 边界）。"""
from __future__ import annotations

import json
from pathlib import Path

FIX = Path(__file__).resolve().parent


def save(name: str, data: dict) -> None:
    path = FIX / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {path.name}: {len(data.get('issues', [])) if isinstance(data, dict) else 'non-dict'} issues")


# ---- 合法样本 ----
VALID = {
    "schema_version": "1.0",
    "issues": [
        {
            "id": "thesis-structure-001",
            "source": "thesis",
            "category": "structure",
            "severity": "fatal",
            "scope": "document",
            "locator": {"chapter": "全文", "paragraph_index": 0},
            "excerpt": "",
            "problem": "全文缺少研究综述",
            "suggestion": ["补写独立综述章节"],
            "group_id": "g-001",
        },
        {
            "id": "thesis-argumentation-001",
            "source": "thesis",
            "category": "argumentation",
            "severity": "major",
            "scope": "paragraph",
            "locator": {"chapter": "3.2.1", "paragraph_index": 5, "sentence_index": 2},
            "excerpt": "Beauchamp Fischer Childress",
            "problem": "罗列未做比较分析",
            "suggestion": ["新增三派学说取舍小节"],
            "group_id": "g-002",
        },
        {
            "id": "citation-citation-format-001",
            "source": "citation",
            "category": "citation-format",
            "severity": "minor",
            "scope": "paragraph",
            "locator": {"chapter": "脚注[12]", "paragraph_index": 11},
            "excerpt": "(02)",
            "problem": "期号不应前导 0",
            "suggestion": ["(02) 改为 (2)"],
            "group_id": "g-003",
        },
    ],
}
save("issues_valid.json", VALID)

# ---- 违规：id 格式错误 ----
INVALID_ID = {
    "schema_version": "1.0",
    "issues": [
        {
            "id": "thesis_structure_001",  # 应为短横线
            "source": "thesis",
            "category": "structure",
            "severity": "fatal",
            "scope": "document",
            "locator": {"chapter": "全文", "paragraph_index": 0},
            "excerpt": "",
            "problem": "问题描述",
            "suggestion": ["修复建议"],
            "group_id": "g-001",
        }
    ],
}
save("issues_invalid_id_pattern.json", INVALID_ID)

# ---- 违规：枚举越界 ----
INVALID_ENUM = {
    "schema_version": "1.0",
    "issues": [
        {
            "id": "thesis-structure-001",
            "source": "unknown",  # 枚举越界
            "category": "structure",
            "severity": "fatal",
            "scope": "document",
            "locator": {"chapter": "全文", "paragraph_index": 0},
            "excerpt": "",
            "problem": "问题",
            "suggestion": ["建议"],
            "group_id": "g-001",
        }
    ],
}
save("issues_invalid_enum.json", INVALID_ENUM)

# ---- 违规：id 重复 ----
INVALID_DUP = {
    "schema_version": "1.0",
    "issues": [
        {
            "id": "thesis-structure-001",
            "source": "thesis", "category": "structure", "severity": "fatal",
            "scope": "document", "locator": {"chapter": "全文", "paragraph_index": 0},
            "excerpt": "", "problem": "a", "suggestion": ["x"], "group_id": "g-001",
        },
        {
            "id": "thesis-structure-001",  # 重复
            "source": "thesis", "category": "structure", "severity": "major",
            "scope": "document", "locator": {"chapter": "2", "paragraph_index": 5},
            "excerpt": "", "problem": "b", "suggestion": ["y"], "group_id": "g-002",
        },
    ],
}
save("issues_invalid_duplicate_id.json", INVALID_DUP)

# ---- 违规：长度超限 ----
INVALID_LENGTH = {
    "schema_version": "1.0",
    "issues": [
        {
            "id": "thesis-structure-001",
            "source": "thesis", "category": "structure", "severity": "fatal",
            "scope": "paragraph",
            "locator": {"chapter": "1", "paragraph_index": 0},
            "excerpt": "x" * 61,  # > 60 码点
            "problem": "超长问题 " + "a" * 200,  # > 200 码点
            "suggestion": ["x" * 501],  # > 500 码点
            "group_id": "g-001",
        }
    ],
}
save("issues_invalid_length.json", INVALID_LENGTH)

# ---- 违规：scope=chapter 但 excerpt 非空 ----
INVALID_SCOPE_EXCERPT = {
    "schema_version": "1.0",
    "issues": [
        {
            "id": "thesis-structure-001",
            "source": "thesis", "category": "structure", "severity": "fatal",
            "scope": "chapter",
            "locator": {"chapter": "2", "paragraph_index": 0},
            "excerpt": "整章内容占位",  # 违规：scope=chapter 必须为空
            "problem": "第二章结构问题",
            "suggestion": ["修复建议"],
            "group_id": "g-001",
        }
    ],
}
save("issues_invalid_scope_excerpt.json", INVALID_SCOPE_EXCERPT)

# ---- 违规：表格 locator 不完整 ----
INVALID_TABLE = {
    "schema_version": "1.0",
    "issues": [
        {
            "id": "thesis-empirical-001",
            "source": "thesis", "category": "empirical", "severity": "major",
            "scope": "paragraph",
            "locator": {
                "chapter": "4.2",
                "paragraph_index": -1,
                "table_index": 0,
                "row": 2,
                # 缺 col 和 paragraph_index_in_cell
            },
            "excerpt": "表格内容",
            "problem": "样本过少",
            "suggestion": ["补充样本"],
            "group_id": "g-001",
        }
    ],
}
save("issues_invalid_table_incomplete.json", INVALID_TABLE)

# ---- 违规：group_id 不一致 ----
INVALID_GID = {
    "schema_version": "1.0",
    "issues": [
        {
            "id": "thesis-argumentation-001",
            "source": "thesis", "category": "argumentation", "severity": "major",
            "scope": "paragraph",
            "locator": {"chapter": "3.2.1", "paragraph_index": 5},
            "excerpt": "a", "problem": "a", "suggestion": ["a"],
            "group_id": "g-007",
        },
        {
            "id": "thesis-argumentation-002",
            "source": "thesis", "category": "argumentation", "severity": "minor",
            "scope": "paragraph",
            "locator": {"chapter": "3.2.1", "paragraph_index": 5},  # 四元组相同
            "excerpt": "b", "problem": "b", "suggestion": ["b"],
            "group_id": "g-009",  # 但 group_id 不同——违规
        },
    ],
}
save("issues_invalid_group_id.json", INVALID_GID)

# ---- 边界：同 group_id 两条（合法聚合） ----
BOUNDARY_GID_CONSISTENT = {
    "schema_version": "1.0",
    "issues": [
        {
            "id": "thesis-argumentation-001",
            "source": "thesis", "category": "argumentation", "severity": "major",
            "scope": "paragraph",
            "locator": {"chapter": "3.2.1", "paragraph_index": 5},
            "excerpt": "a", "problem": "a", "suggestion": ["a"],
            "group_id": "g-010",
        },
        {
            "id": "thesis-argumentation-002",
            "source": "thesis", "category": "argumentation", "severity": "minor",
            "scope": "sentence",
            "locator": {"chapter": "3.2.1", "paragraph_index": 5, "sentence_index": 1},
            "excerpt": "b", "problem": "b", "suggestion": ["b"],
            "group_id": "g-010",  # 与上一条四元组相同,共享 g-010
        },
    ],
}
save("issues_boundary_same_group_id.json", BOUNDARY_GID_CONSISTENT)

# ---- 边界：600 条 issues（验证 500 条上限） ----
BOUNDARY_600 = {"schema_version": "1.0", "issues": []}
categories = ["structure", "argumentation", "language"]
severities = ["fatal", "major", "minor"]
group_map = {}
next_gid = 1
for i in range(600):
    sev = severities[i % 3]
    cat = categories[i % 3]
    chapter = f"{(i % 5) + 1}.{(i % 3) + 1}"
    pidx = i % 7
    key = ("thesis", cat, chapter, pidx)
    if key not in group_map:
        group_map[key] = f"g-{next_gid:03d}"
        next_gid += 1
    BOUNDARY_600["issues"].append({
        "id": f"thesis-{cat}-{i:03d}",
        "source": "thesis",
        "category": cat,
        "severity": sev,
        "scope": "paragraph",
        "locator": {"chapter": chapter, "paragraph_index": pidx},
        "excerpt": f"条目 {i}",
        "problem": f"问题 {i}",
        "suggestion": [f"建议 {i}"],
        "group_id": group_map[key],
    })
save("issues_boundary_600.json", BOUNDARY_600)

# ---- 边界：跨段 span ----
BOUNDARY_SPAN = {
    "schema_version": "1.0",
    "issues": [
        {
            "id": "thesis-argumentation-001",
            "source": "thesis", "category": "argumentation", "severity": "major",
            "scope": "span",
            "locator": {"chapter": "3.3", "paragraph_index": 8},
            "excerpt": "连续四段单线推进",
            "problem": "未回应反对意见",
            "suggestion": ["新增反对观点与回应段"],
            "group_id": "g-020",
        }
    ],
}
save("issues_boundary_span.json", BOUNDARY_SPAN)

# ---- 边界：pdf bbox 完整 ----
BOUNDARY_PDF_BBOX = {
    "schema_version": "1.0",
    "issues": [
        {
            "id": "thesis-argumentation-001",
            "source": "thesis", "category": "argumentation", "severity": "major",
            "scope": "paragraph",
            "locator": {
                "chapter": "3", "paragraph_index": 2,
                "page_number": 1, "bbox": [72, 700, 500, 720],
            },
            "excerpt": "pdf bbox 示例",
            "problem": "问题",
            "suggestion": ["建议"],
            "group_id": "g-030",
        }
    ],
}
save("issues_boundary_pdf_bbox.json", BOUNDARY_PDF_BBOX)

# ---- 边界：pdf bbox 越界（需 clip） ----
BOUNDARY_PDF_BBOX_OOB = {
    "schema_version": "1.0",
    "issues": [
        {
            "id": "thesis-language-001",
            "source": "thesis", "category": "language", "severity": "minor",
            "scope": "sentence",
            "locator": {
                "chapter": "5.1", "paragraph_index": 3,
                "page_number": 1, "bbox": [10000, 10000, 20000, 20000],
            },
            "excerpt": "越界 bbox",
            "problem": "越界问题",
            "suggestion": ["测试 clip 正确性"],
            "group_id": "g-040",
        }
    ],
}
save("issues_boundary_pdf_bbox_oob.json", BOUNDARY_PDF_BBOX_OOB)

if __name__ == "__main__":
    print("All fixtures written to", FIX)
