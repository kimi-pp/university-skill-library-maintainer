# Tests 目录

本目录包含 `unified-thesis-reviewer` 的测试套件。**不随 skill 分发**（构建脚本会从发布包排除）。

## 运行

```bash
# 从 skill 根目录运行全部测试
python3 -m unittest discover tests -v
```

## 结构

```
tests/
├── __init__.py
├── conftest.py                 # 共享夹具、枚举、随机种子
├── fixtures/                   # 测试夹具
│   ├── build_minimal_docx.py   # 构造最小合法 docx
│   ├── build_minimal_pdf.py    # 构造最小合法 pdf
│   ├── minimal.docx            # 运行 build 脚本后生成
│   ├── minimal.pdf             # 同上
│   ├── issues_valid.json
│   ├── issues_invalid_*.json
│   └── issues_boundary_*.json
├── test_issues_json.py         # Property 1–4：issues.json 自校验与 group_id
├── test_docx_injection.py      # Property 5–9：docx 批注注入
├── test_xfdf_generation.py     # Property 10–11：XFDF 生成
├── test_network_tool_discovery.py  # Property 12：联网工具发现
├── test_skill_meta.py          # 非 PBT：前置元数据、stdlib-only、bundle 纯净性
└── README.md                   # 本文件
```

## Property-Based Testing 策略

本项目**不依赖 Hypothesis**等第三方库。性质测试用 Python 标准 `random` 模块 + 固定种子生成大量样本（默认每条 property ≥ 100 examples），等效覆盖。

测试固定种子 `42`，保证 CI 重现。

## 先决条件

- Python 3.8+
- 无第三方依赖

## 首次运行

需要先构造测试夹具：

```bash
python3 tests/fixtures/build_minimal_docx.py
python3 tests/fixtures/build_minimal_pdf.py
```

这两步会生成 `tests/fixtures/minimal.docx` 和 `tests/fixtures/minimal.pdf`。已自动集成到测试 setUp 中，通常无需手动执行。
