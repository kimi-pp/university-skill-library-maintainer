import json
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "discipline_mapping" / "catalogs"
ug = json.loads((ROOT / "undergraduate_2026.json").read_text("utf-8"))["records"]
grad_base = json.loads((ROOT / "graduate_2022_base.json").read_text("utf-8"))["records"]
grad = json.loads((ROOT / "graduate_effective.json").read_text("utf-8"))["records"]

assert len(ug) == 883
assert len({x["category_code"] for x in ug}) == 13
assert len({x["class_code"] for x in ug}) == 92
assert len({x["major_code"] for x in ug}) == 883
assert {"具身智能", "脑机科学与技术"} <= {x["major_name"] for x in ug}
assert all(isinstance(x["major_code"], str) for x in ug)

academic = [x for x in grad_base if x["object_type"] == "学术学位一级学科"]
professional = [x for x in grad_base if x["object_type"] == "专业学位类别"]
assert len({x["object_code"] for x in academic}) == 117
assert len({x["object_code"] for x in professional}) == 67
assert len({(x["object_type"], x["object_code"]) for x in grad}) == len(grad)
assert any(x["object_code"] == "1056" and x["object_name"] == "中药" for x in grad)
assert any(x["object_code"] == "1403" and x["object_name"] == "设计学" for x in grad)

assert all(
    json.loads((ROOT / name).read_text("utf-8"))["exceptions"] == []
    for name in (
        "undergraduate_2026.json",
        "graduate_2022_base.json",
        "graduate_correspondence.json",
        "graduate_effective.json",
    )
)
assert any(x["major_code"] == "0502107TK" and x["major_name"] == "语言智能" for x in ug)
assert all(
    x["major_code"].startswith(x["class_code"])
    for x in ug
    if x["category_code"] != "14"
)
assert {
    (x["object_type"], x["object_code"]): x["object_name"] for x in grad_base
} == {(x["object_type"], x["object_code"]): x["object_name"] for x in grad}

MODULE_PATH = ROOT.parent / "extract_official_catalogs.py"
spec = importlib.util.spec_from_file_location("extract_official_catalogs", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

malformed_ug = module.parse_undergraduate(
    "[[PAGE 7]]\n01 学科门类：哲学\n0101 哲学类\n010101 哲学\n010102\n01010X 错误专业\n01010"
)
assert [x["major_code"] for x in malformed_ug] == ["010101"]
assert malformed_ug.exceptions == [
    {"page": 7, "raw_line": "010102", "reason": "unparseable digit-leading catalog line"},
    {"page": 7, "raw_line": "01010X 错误专业", "reason": "unparseable digit-leading catalog line"},
    {"page": 7, "raw_line": "01010", "reason": "unparseable digit-leading catalog line"},
]

correspondence_fixture = module.parse_correspondence(
    """<table>
    <tr><th colspan="3">研究生教育学科专业目录（2022年）</th><th colspan="3">原目录</th></tr>
    <tr><th>门类</th><th>代码</th><th>名称</th><th>门类</th><th>代码</th><th>名称</th></tr>
    <tr><td rowspan="2">工学</td><td rowspan="2">0862</td><td rowspan="2">风景园林</td>
        <td>工学</td><td>0834</td><td>风景园林学</td></tr>
    <tr><td>农学</td><td>0953</td><td>风景园林</td></tr>
    </table>"""
)
assert len(correspondence_fixture) == 2
assert {x["relation_type"] for x in correspondence_fixture} == {"merge"}
assert correspondence_fixture.exceptions == []

conflicting_lineage = [
    {
        "current_category_name": "哲学",
        "current_object_code": "0101",
        "current_object_name": "错误名称",
        "current_object_type": "学术学位一级学科",
        "previous_category_name": "哲学",
        "previous_code": "0101",
        "previous_name": "旧称",
        "relation_type": "rename",
        "source_id": "graduate_2025_correspondence",
    }
]
effective_fixture = module.enrich_with_correspondence(
    [
        {
            "category_code": "01",
            "category_name": "哲学",
            "object_code": "0101",
            "object_name": "哲学",
            "object_type": "学术学位一级学科",
            "degree_levels": ["博士", "硕士"],
            "notes": [],
            "status": "current",
            "source_ids": ["graduate_2022_pdf"],
            "previous_names": [],
        }
    ],
    conflicting_lineage,
)
assert effective_fixture[0]["object_name"] == "哲学"
assert effective_fixture[0]["previous_names"] == []
assert effective_fixture.exceptions[0]["reason"] == "2022-side code/name conflicts with the 2022 PDF"

catalog_names = (
    "undergraduate_2026.json",
    "graduate_2022_base.json",
    "graduate_correspondence.json",
    "graduate_effective.json",
)
before_regeneration = {name: (ROOT / name).read_bytes() for name in catalog_names}
module.main()
assert before_regeneration == {name: (ROOT / name).read_bytes() for name in catalog_names}
