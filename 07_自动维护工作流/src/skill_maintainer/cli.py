"""命令行入口。"""

import argparse
from collections.abc import Callable


COMMANDS = (
    "setup",
    "import-existing",
    "doctor",
    "edit-settings",
    "apply-settings",
    "run-now",
    "scheduled-run",
    "status",
    "repair-ledger",
    "rebuild-report",
    "prepare",
    "apply-reviews",
    "finalize",
)


def _not_connected(_: argparse.Namespace) -> int:
    print("该命令尚未接线")
    return 2


def build_parser() -> argparse.ArgumentParser:
    """构建文件化维护工作流的命令解析器。"""
    parser = argparse.ArgumentParser(prog="skill-maintainer")
    subparsers = parser.add_subparsers(dest="command")
    for command in COMMANDS:
        subparser = subparsers.add_parser(command)
        subparser.set_defaults(handler=_not_connected)
    return parser


def main() -> int:
    """运行已选择的命令。"""
    args = build_parser().parse_args()
    handler: Callable[[argparse.Namespace], int] | None = getattr(args, "handler", None)
    if handler is None:
        build_parser().print_help()
        return 2
    return handler(args)
