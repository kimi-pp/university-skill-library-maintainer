import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from skill_maintainer.scheduling import next_run_at, schedule_preview
from skill_maintainer.settings import load_settings


BASE = '''config_version = 1

[workflow]
enabled = true
timezone = "Asia/Shanghai"

[schedule]
mode = "{mode}"
start_time = "22:00"
weekdays = ["Monday", "Wednesday", "Friday"]
interval_days = 7
day_of_month = 1

[research]
incremental_search = true
full_recheck_interval_days = 7
check_existing_skill_updates = true
include_generic_skills = false

[delivery]
generate_word = true
generate_excel = true
only_refresh_affected_classes = true
notify_on_no_change = false
'''


class SchedulingTest(unittest.TestCase):
    zone = ZoneInfo("Asia/Shanghai")
    clock = datetime(2026, 8, 27, 20, 0, tzinfo=zone)

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)

    def settings(self, mode: str):
        path = Path(self.tempdir.name) / f"{mode}.toml"
        path.write_text(BASE.format(mode=mode), encoding="utf-8")
        return load_settings(path)

    def test_next_run_for_every_mode(self):
        cases = (
            ("daily", None, datetime(2026, 8, 27, 22, 0, tzinfo=self.zone)),
            ("weekly", None, datetime(2026, 8, 28, 22, 0, tzinfo=self.zone)),
            ("interval", datetime(2026, 8, 20, 22, 0, tzinfo=self.zone), datetime(2026, 8, 27, 22, 0, tzinfo=self.zone)),
            ("monthly", None, datetime(2026, 9, 1, 22, 0, tzinfo=self.zone)),
            ("manual", None, None),
        )
        for mode, last_success_at, expected in cases:
            with self.subTest(mode=mode):
                actual = next_run_at(self.settings(mode), self.clock, last_success_at)
                self.assertEqual(actual, expected)

    def test_interval_without_history_uses_next_configured_local_start(self):
        self.assertEqual(
            next_run_at(self.settings("interval"), self.clock),
            datetime(2026, 8, 27, 22, 0, tzinfo=self.zone),
        )

    def test_returned_timezone_is_always_asia_shanghai(self):
        for mode in ("daily", "weekly", "interval", "monthly"):
            with self.subTest(mode=mode):
                actual = next_run_at(self.settings(mode), self.clock)
                self.assertEqual(actual.tzinfo, self.zone)
                self.assertEqual(actual.tzinfo.key, "Asia/Shanghai")

    def test_chinese_preview_describes_enabled_weekly_schedule_and_recheck(self):
        self.assertEqual(
            schedule_preview(self.settings("weekly")),
            "已启用；每周一、三、五 22:00（Asia/Shanghai）运行；每 7 天执行一次全量复核。",
        )


if __name__ == "__main__":
    unittest.main()
