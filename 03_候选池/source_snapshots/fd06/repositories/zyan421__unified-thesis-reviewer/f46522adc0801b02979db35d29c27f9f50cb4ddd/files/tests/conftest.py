"""共享夹具与路径常量。

测试使用 Python 标准 unittest，不依赖 pytest 或 hypothesis。
property-based 风格靠 random + 大量样本实现，默认每条 property 生成 100 个 examples。
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SKILL_ROOT = TESTS_DIR.parent
TOOLS_DIR = SKILL_ROOT / "tools"
FIXTURES_DIR = TESTS_DIR / "fixtures"

# 把 tests/ 与 tools/ 加入 sys.path，以便
#   - 跨测试模块 import（from _script_loader import ...）
#   - 从脚本文件加载（通过 importlib.util）
for p in (TESTS_DIR, TOOLS_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# 每条 property 的默认样本数
DEFAULT_EXAMPLES = 100

# 固定随机种子以便 CI 可复现
DEFAULT_SEED = 42


def get_random(seed: int = DEFAULT_SEED) -> random.Random:
    """返回一个确定性 Random 实例。"""
    return random.Random(seed)


# ---- 枚举（与 rules/issues-schema.md 同步） ----

ENUM_SOURCE = ["thesis", "citation"]
ENUM_CATEGORY = [
    "structure", "argumentation", "literature-review",
    "empirical", "legal-norms", "language", "policy",
    "academic-integrity", "citation-format", "citation-missing-info",
]
ENUM_SEVERITY = ["fatal", "major", "minor"]
ENUM_SCOPE = ["document", "chapter", "paragraph", "sentence", "span"]
