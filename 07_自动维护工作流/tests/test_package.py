import unittest

from skill_maintainer import __version__
from skill_maintainer.cli import build_parser


class PackageTest(unittest.TestCase):
    def test_package_and_commands_are_importable(self):
        self.assertEqual(__version__, "0.1.0")
        parser = build_parser()
        commands = parser._subparsers._group_actions[0].choices
        self.assertEqual(
            set(commands),
            {
                "setup", "import-existing", "doctor", "edit-settings",
                "apply-settings", "run-now", "scheduled-run", "status",
                "repair-ledger", "rebuild-report", "prepare", "apply-reviews",
                "finalize",
            },
        )


if __name__ == "__main__":
    unittest.main()
