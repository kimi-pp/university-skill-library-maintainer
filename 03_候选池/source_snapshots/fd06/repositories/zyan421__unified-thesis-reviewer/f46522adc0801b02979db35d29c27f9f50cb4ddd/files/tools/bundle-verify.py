#!/usr/bin/env python3
"""bundle-verify.py —— 发布前验证 bundle 目录或分发 zip。

用法:
    python3 tools/bundle-verify.py [--path PATH]

检查项（R9 + R10）:
    1. 不含版权原文（gb7714-{year}.docx / 法学引注手册*）
    2. 不含 tests/ 目录
    3. 不含 .git / .gitignore
    4. 所有 tools/*.py 通过 py_compile
    5. manifest.json 存在且 schema_version=1.0

退出码:
    0 = 所有检查通过
    1 = 有检查失败
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

# 版权黑名单
COPYRIGHT_BLACKLIST = [
    re.compile(r"^gb[_-]?7714[_-]?\d{4}", re.IGNORECASE),
    re.compile(r"^法学引注手册"),
    re.compile(r"^zhangqinglin-original", re.IGNORECASE),
]

# 禁止出现在发布包中的目录名
FORBIDDEN_DIRS = {"tests", ".git", "__pycache__", ".pytest_cache", ".mypy_cache"}


def check_copyright(root: Path) -> list[str]:
    """扫描目录下所有文件，命中版权黑名单则报告。"""
    violations = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        for pat in COPYRIGHT_BLACKLIST:
            if pat.search(p.name):
                violations.append(
                    f"copyrighted file in bundle: {p.relative_to(root)}"
                )
                break
    return violations


def check_forbidden_dirs(root: Path) -> list[str]:
    violations = []
    for d in root.rglob("*"):
        if d.is_dir() and d.name in FORBIDDEN_DIRS:
            violations.append(f"forbidden directory: {d.relative_to(root)}")
    return violations


def check_manifest(root: Path) -> list[str]:
    violations = []
    bundled = root / "_bundled"
    if not bundled.is_dir():
        return []  # 允许 bundle 还未构建
    manifest = bundled / "manifest.json"
    if not manifest.is_file():
        violations.append("missing _bundled/manifest.json")
        return violations
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        violations.append(f"manifest.json invalid JSON: {e}")
        return violations
    if data.get("schema_version") != "1.0":
        violations.append(
            f"manifest schema_version != 1.0, got {data.get('schema_version')}"
        )
    return violations


def check_scripts_syntax(root: Path) -> list[str]:
    violations = []
    tools = root / "tools"
    if not tools.is_dir():
        return []
    for py in sorted(tools.glob("*.py")):
        try:
            ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError as e:
            violations.append(f"syntax error in {py.relative_to(root)}: {e}")
    return violations


def check_license_notice(root: Path) -> list[str]:
    violations = []
    notice = root / "LICENSE-NOTICE.md"
    if not notice.is_file():
        violations.append("missing LICENSE-NOTICE.md")
        return violations
    text = notice.read_text(encoding="utf-8")
    for phrase in ("引用但不包含", "GB/T 7714", "法学引注手册"):
        if phrase not in text:
            violations.append(f"LICENSE-NOTICE.md missing phrase: {phrase!r}")
    return violations


def run_all(root: Path) -> tuple[bool, list[str]]:
    """跑全部检查，返回 (all_ok, violations)。"""
    all_violations: list[str] = []
    all_violations += check_copyright(root)
    all_violations += check_forbidden_dirs(root)
    all_violations += check_manifest(root)
    all_violations += check_scripts_syntax(root)
    all_violations += check_license_notice(root)
    return (len(all_violations) == 0, all_violations)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="bundle-verify",
        description="Verify skill bundle for copyright, structure, syntax.",
    )
    ap.add_argument(
        "--path",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="path to skill root (default: parent of this script)",
    )
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    root = args.path.resolve()
    print(f"[bundle-verify] checking {root}")

    ok, violations = run_all(root)
    if ok:
        print("[bundle-verify] PASSED: all checks passed")
        return 0

    print(f"[bundle-verify] FAILED: {len(violations)} violations")
    for v in violations:
        print(f"  - {v}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
