"""把 tools/ 下文件名带连字符的脚本作为模块加载，供测试 import 使用。"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"


def load_script(filename: str, module_name: str | None = None) -> ModuleType:
    """把 tools/<filename> 作为 module_name 加载并返回模块对象。"""
    path = TOOLS_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(path)
    name = module_name or path.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_inject_docx():
    return load_script("inject-docx-comments.py", "inject_docx_comments")


def load_generate_xfdf():
    return load_script("generate-xfdf.py", "generate_xfdf")


def load_build_bundle():
    return load_script("build-bundle.py", "build_bundle")
