"""Property 12 测试：联网工具发现。

关键字匹配规则（rules/network-tool-discovery.md §2）：
- 白名单关键字（子串，不区分大小写）：search, web, browse, fetch, google, bing,
  baidu, scholar, 裁判文书, 北大法宝, 威科先行, 法律检索
- 工具名含其中任一即视为具备联网能力
- 不含任何关键字 → 判为非联网工具

Feature: unified-thesis-reviewer, Property 12
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import random
import string
import unittest

from conftest import DEFAULT_EXAMPLES, DEFAULT_SEED


NETWORK_KEYWORDS = [
    "search", "web", "browse", "fetch",
    "google", "bing", "baidu", "scholar",
    "裁判文书", "北大法宝", "威科先行", "法律检索",
]


def has_network_tool(tool_names: list[str]) -> bool:
    """纯函数实现：按 rules/network-tool-discovery.md §2 的关键字子串匹配规则。"""
    for name in tool_names:
        lower_name = name.lower()
        for kw in NETWORK_KEYWORDS:
            if kw.lower() in lower_name:
                return True
    return False


class TestP12KeywordHitRule(unittest.TestCase):
    """Property 12：工具名含任一关键字 → 判联网；否则 → 非联网。"""

    def test_positive_examples(self):
        """随机在工具名中嵌入关键字，应被判为联网。"""
        rng = random.Random(DEFAULT_SEED + 30)
        for i in range(DEFAULT_EXAMPLES):
            kw = rng.choice(NETWORK_KEYWORDS)
            # 构造工具名：前后加随机字符
            prefix = "".join(rng.choices(string.ascii_letters + "_", k=rng.randint(0, 5)))
            suffix = "".join(rng.choices(string.ascii_letters + "_", k=rng.randint(0, 5)))
            # 随机改变大小写
            variant = kw.swapcase() if rng.random() < 0.5 and kw.isascii() else kw
            tool_name = f"{prefix}{variant}{suffix}"

            # 可以和其他无关工具混合
            tools = [tool_name]
            if rng.random() < 0.5:
                tools += ["read_file", "fs_write", "list_directory"]
                rng.shuffle(tools)

            self.assertTrue(
                has_network_tool(tools),
                f"example {i}: tools {tools} should be detected as having network"
            )

    def test_negative_examples(self):
        """工具名完全不含关键字 → 判非联网。"""
        rng = random.Random(DEFAULT_SEED + 31)
        # 一批"明显非联网"的工具名
        non_network_names = [
            "read_file", "fs_write", "execute_bash", "list_directory",
            "delete_file", "str_replace", "py_compile",
            "ast_parse", "json_loads", "md5",
            "compile_template", "render_markdown",
        ]

        for i in range(DEFAULT_EXAMPLES):
            tool = rng.choice(non_network_names)
            # 加随机后缀但避免意外命中关键字
            suffix = "".join(rng.choices(string.ascii_lowercase, k=rng.randint(0, 3)))
            tool_name = f"{tool}{suffix}"

            # 验证构造的名字确实不含关键字（自我一致性检查）
            contains_kw = any(kw.lower() in tool_name.lower() for kw in NETWORK_KEYWORDS)
            if contains_kw:
                # 如果意外命中，跳过这个 example
                continue

            self.assertFalse(
                has_network_tool([tool_name]),
                f"example {i}: {tool_name} should NOT be detected as network"
            )

    def test_case_insensitivity(self):
        """大小写变体都应命中。"""
        variants = ["WEB_SEARCH", "Web_Search", "web_search", "WeB_sEaRcH"]
        for v in variants:
            self.assertTrue(
                has_network_tool([v]),
                f"case variant {v!r} should be detected"
            )

    def test_chinese_keywords(self):
        """中文关键字命中。"""
        chinese_tools = [
            "裁判文书查询",
            "北大法宝_case_search",
            "威科先行_law_lookup",
            "法律检索插件",
        ]
        for tool in chinese_tools:
            self.assertTrue(
                has_network_tool([tool]),
                f"chinese tool {tool!r} should be detected"
            )

    def test_empty_tools(self):
        """空工具列表 → 非联网。"""
        self.assertFalse(has_network_tool([]))

    def test_single_substring_match(self):
        """子串匹配即可命中。"""
        self.assertTrue(has_network_tool(["oc_browse_page"]))  # browse
        self.assertTrue(has_network_tool(["remote_web_search"]))  # web, search
        self.assertTrue(has_network_tool(["scholar_lookup"]))  # scholar


if __name__ == "__main__":
    unittest.main()
