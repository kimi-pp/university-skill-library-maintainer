import hashlib
import tempfile
import unittest
from pathlib import Path

from skill_maintainer.settings import SettingsError, load_settings, settings_sha256


VALID = '''config_version = 1

[workflow]
enabled = true
timezone = "Asia/Shanghai"

[schedule]
mode = "weekly"
start_time = "22:00"
weekdays = ["Monday", "Wednesday", "Friday"]
interval_days = 1
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


class SettingsTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)

    def write(self, text: str) -> Path:
        path = Path(self.tempdir.name) / "settings.toml"
        path.write_text(text, encoding="utf-8")
        return path

    def fixture(self, name: str) -> Path:
        if name != "manual.toml":
            raise ValueError(name)
        return self.write(
            VALID.replace('enabled = true', 'enabled = false').replace(
                'mode = "weekly"', 'mode = "manual"'
            )
        )

    def test_manual_disabled_default(self):
        settings = load_settings(self.fixture("manual.toml"))
        self.assertFalse(settings.workflow.enabled)
        self.assertEqual(settings.schedule.mode, "manual")

    def test_rejects_unknown_and_invalid_values(self):
        for text in (
            VALID.replace('[workflow]', '[workflow]\nunknown = 1'),
            VALID.replace('start_time = "22:00"', 'start_time = "25:61"'),
            VALID.replace('timezone = "Asia/Shanghai"', 'timezone = "Mars/Base"'),
            VALID.replace('interval_days = 1', 'interval_days = 0'),
            VALID.replace('day_of_month = 1', 'day_of_month = 29'),
        ):
            with self.subTest(text=text):
                with self.assertRaises(SettingsError):
                    load_settings(self.write(text))

    def test_rejects_missing_keys_wrong_types_and_boolean_integers(self):
        for text in (
            VALID.replace('generate_word = true\n', ''),
            VALID.replace('enabled = true', 'enabled = "true"'),
            VALID.replace('interval_days = 1', 'interval_days = true'),
            VALID.replace('weekdays = ["Monday", "Wednesday", "Friday"]', 'weekdays = "Monday"'),
            VALID.replace('mode = "weekly"', 'mode = "yearly"'),
            VALID.replace('full_recheck_interval_days = 7', 'full_recheck_interval_days = 0'),
        ):
            with self.subTest(text=text):
                with self.assertRaises(SettingsError):
                    load_settings(self.write(text))

    def test_rejects_duplicate_toml_keys(self):
        with self.assertRaises(SettingsError):
            load_settings(self.write(VALID.replace("config_version = 1", "config_version = 1\nconfig_version = 1")))

    def test_rejects_malformed_timezone_as_settings_error(self):
        for timezone in ("", "/absolute/path", "../bad"):
            with self.subTest(timezone=timezone):
                with self.assertRaises(SettingsError):
                    load_settings(self.write(VALID.replace('timezone = "Asia/Shanghai"', f'timezone = "{timezone}"')))

    def test_settings_hash_matches_file_bytes(self):
        path = self.write(VALID)
        self.assertEqual(settings_sha256(path), hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
