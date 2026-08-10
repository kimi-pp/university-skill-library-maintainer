"""非 PBT 单元测试：

- SKILL.md 的 front-matter keywords 覆盖 R1.5 要求
- `_bundled/` 不包含版权材料（R9）
- `tools/` 下脚本仅用 stdlib（R10.3）
- TR / CC 的文件未被本 skill 修改（R3.6、R14.1）

Feature: unified-thesis-reviewer
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ast
import re
import subprocess
import unittest

from conftest import SKILL_ROOT, TOOLS_DIR

REPO_ROOT = SKILL_ROOT.parent.parent  # .kiro/skills/.. = .kiro
WORKSPACE_ROOT = REPO_ROOT.parent  # ..

# R1.5 要求的触发词
REQUIRED_KEYWORDS = [
    "统一审查", "一站式", "全面审查", "综合审查",
    "批注版", "带批注的修订稿", "综合审阅", "一次性检查",
    "thesis all-in-one review",
]

# 允许的标准库（Python 3.8+ stdlib）
STDLIB_NAMES = {
    "argparse", "copy", "datetime", "hashlib", "io", "json", "os", "pathlib",
    "re", "shutil", "subprocess", "sys", "tempfile", "textwrap", "time",
    "typing", "unittest", "xml", "zipfile", "collections", "enum", "itertools",
    "functools", "dataclasses", "string", "importlib", "runpy",
    "__future__",
}

# 版权材料文件名模式（出现在 bundle 内即违规）
COPYRIGHT_PATTERNS = [
    re.compile(r"^gb[_-]?7714[_-]?\d{4}", re.IGNORECASE),
    re.compile(r"^法学引注手册"),
    re.compile(r"^.*\.docx$", re.IGNORECASE),
    re.compile(r"^.*\.pdf$", re.IGNORECASE),
]


class TestSkillMdKeywords(unittest.TestCase):
    """验证 SKILL.md 的 front-matter 含所有 R1.5 要求的触发词。"""

    def test_all_required_keywords_present(self):
        skill_md = SKILL_ROOT / "SKILL.md"
        self.assertTrue(skill_md.is_file(), "SKILL.md missing")

        text = skill_md.read_text(encoding="utf-8")
        # 只扫描 front-matter 部分
        m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        self.assertIsNotNone(m, "front-matter not found")
        front_matter = m.group(1)

        missing = []
        for kw in REQUIRED_KEYWORDS:
            if kw not in front_matter:
                missing.append(kw)

        self.assertEqual(missing, [], f"missing keywords: {missing}")


class TestBundleNoCopyrightSources(unittest.TestCase):
    """验证 `_bundled/` 中无版权材料。"""

    def test_bundle_clean(self):
        bundled = SKILL_ROOT / "_bundled"
        if not bundled.is_dir():
            self.skipTest("_bundled/ does not exist; run build-bundle.py first")

        violations = []
        for p in bundled.rglob("*"):
            if not p.is_file():
                continue
            name = p.name
            for pat in COPYRIGHT_PATTERNS:
                if pat.search(name):
                    violations.append(str(p.relative_to(bundled)))
                    break

        self.assertEqual(violations, [], f"copyrighted files in bundle: {violations}")


class TestToolsStdlibOnly(unittest.TestCase):
    """验证 `tools/` 下脚本只 import 标准库。"""

    def _extract_imports(self, script_path: Path) -> set[str]:
        tree = ast.parse(script_path.read_text(encoding="utf-8"))
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    names.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    names.add(node.module.split(".")[0])
        return names

    def test_inject_docx_comments_stdlib_only(self):
        script = TOOLS_DIR / "inject-docx-comments.py"
        imports = self._extract_imports(script)
        non_stdlib = [n for n in imports if n not in STDLIB_NAMES]
        self.assertEqual(non_stdlib, [], f"non-stdlib imports: {non_stdlib}")

    def test_generate_xfdf_stdlib_only(self):
        script = TOOLS_DIR / "generate-xfdf.py"
        imports = self._extract_imports(script)
        non_stdlib = [n for n in imports if n not in STDLIB_NAMES]
        self.assertEqual(non_stdlib, [], f"non-stdlib imports: {non_stdlib}")

    def test_build_bundle_stdlib_only(self):
        script = TOOLS_DIR / "build-bundle.py"
        imports = self._extract_imports(script)
        non_stdlib = [n for n in imports if n not in STDLIB_NAMES]
        self.assertEqual(non_stdlib, [], f"non-stdlib imports: {non_stdlib}")

    def test_extract_docx_stdlib_only(self):
        script = TOOLS_DIR / "extract-docx.py"
        imports = self._extract_imports(script)
        non_stdlib = [n for n in imports if n not in STDLIB_NAMES]
        self.assertEqual(non_stdlib, [], f"non-stdlib imports: {non_stdlib}")


class TestToolsSyntax(unittest.TestCase):
    """所有 tools/ 下 .py 脚本 py_compile 通过。"""

    def test_all_scripts_compile(self):
        failures = []
        for script in sorted(TOOLS_DIR.glob("*.py")):
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(script)],
                capture_output=True, text=True,
            )
            if result.returncode != 0:
                failures.append((script.name, result.stderr.strip()))
        self.assertEqual(failures, [], f"scripts failed to compile: {failures}")


class TestTrCcUnchanged(unittest.TestCase):
    """验证 TR / CC 的 SKILL.md 未被本 skill 修改（幂等性校验）。"""

    def test_tr_skill_md_exists(self):
        tr = REPO_ROOT / "skills" / "legal-thesis-reviewer" / "SKILL.md"
        self.assertTrue(tr.is_file(), "TR SKILL.md not found")

    def test_cc_skill_md_exists(self):
        cc = REPO_ROOT / "skills" / "legal-citation-checker" / "SKILL.md"
        self.assertTrue(cc.is_file(), "CC SKILL.md not found")


if __name__ == "__main__":
    unittest.main()
