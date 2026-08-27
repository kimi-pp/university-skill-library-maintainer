"""严格读取工作流 TOML 配置。"""

from datetime import datetime, time
from hashlib import sha256
from pathlib import Path
import re
import tomllib
from typing import Any, Final, cast
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .models import (
    DeliverySettings,
    ResearchSettings,
    ScheduleSettings,
    Settings,
    WorkflowSettings,
)


class SettingsError(ValueError):
    """配置文件不符合工作流的受支持格式。"""


_TOP_LEVEL_KEYS: Final = frozenset({"config_version", "workflow", "schedule", "research", "delivery"})
_WORKFLOW_KEYS: Final = frozenset({"enabled", "timezone"})
_SCHEDULE_KEYS: Final = frozenset({"mode", "start_time", "weekdays", "interval_days", "day_of_month"})
_RESEARCH_KEYS: Final = frozenset(
    {
        "incremental_search",
        "full_recheck_interval_days",
        "check_existing_skill_updates",
        "include_generic_skills",
    }
)
_DELIVERY_KEYS: Final = frozenset(
    {"generate_word", "generate_excel", "only_refresh_affected_classes", "notify_on_no_change"}
)
_MODES: Final = frozenset({"daily", "weekly", "interval", "monthly", "manual"})
_WEEKDAYS: Final = frozenset({"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"})
_TIME_RE: Final = re.compile(r"\d{2}:\d{2}\Z")


def settings_sha256(path: Path) -> str:
    """返回配置文件原始字节的 SHA-256，供运行记录追溯。"""
    return sha256(path.read_bytes()).hexdigest()


def load_settings(path: Path) -> Settings:
    """读取完整、无未知键且类型正确的 TOML 设置。"""
    try:
        with path.open("rb") as handle:
            raw = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise SettingsError(f"无法读取有效 TOML 配置：{path}") from exc

    _expect_keys(raw, _TOP_LEVEL_KEYS, "根配置")
    config_version = _expect_int(raw["config_version"], "config_version", minimum=1)
    if config_version != 1:
        raise SettingsError("config_version 必须为 1")

    workflow = _expect_table(raw["workflow"], "workflow")
    schedule = _expect_table(raw["schedule"], "schedule")
    research = _expect_table(raw["research"], "research")
    delivery = _expect_table(raw["delivery"], "delivery")
    _expect_keys(workflow, _WORKFLOW_KEYS, "workflow")
    _expect_keys(schedule, _SCHEDULE_KEYS, "schedule")
    _expect_keys(research, _RESEARCH_KEYS, "research")
    _expect_keys(delivery, _DELIVERY_KEYS, "delivery")

    timezone = _expect_timezone(workflow["timezone"])
    return Settings(
        config_version=config_version,
        workflow=WorkflowSettings(
            enabled=_expect_bool(workflow["enabled"], "workflow.enabled"),
            timezone=timezone,
        ),
        schedule=ScheduleSettings(
            mode=cast(str, _expect_choice(schedule["mode"], "schedule.mode", _MODES)),
            start_time=_expect_time(schedule["start_time"]),
            weekdays=_expect_weekdays(schedule["weekdays"]),
            interval_days=_expect_int(schedule["interval_days"], "schedule.interval_days", minimum=1),
            day_of_month=_expect_int(schedule["day_of_month"], "schedule.day_of_month", minimum=1, maximum=28),
        ),
        research=ResearchSettings(
            incremental_search=_expect_bool(research["incremental_search"], "research.incremental_search"),
            full_recheck_interval_days=_expect_int(
                research["full_recheck_interval_days"],
                "research.full_recheck_interval_days",
                minimum=1,
            ),
            check_existing_skill_updates=_expect_bool(
                research["check_existing_skill_updates"], "research.check_existing_skill_updates"
            ),
            include_generic_skills=_expect_bool(research["include_generic_skills"], "research.include_generic_skills"),
        ),
        delivery=DeliverySettings(
            generate_word=_expect_bool(delivery["generate_word"], "delivery.generate_word"),
            generate_excel=_expect_bool(delivery["generate_excel"], "delivery.generate_excel"),
            only_refresh_affected_classes=_expect_bool(
                delivery["only_refresh_affected_classes"], "delivery.only_refresh_affected_classes"
            ),
            notify_on_no_change=_expect_bool(delivery["notify_on_no_change"], "delivery.notify_on_no_change"),
        ),
    )


def _expect_table(value: Any, name: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise SettingsError(f"{name} 必须是 TOML 表")
    return value


def _expect_keys(table: dict[str, Any], allowed: frozenset[str], name: str) -> None:
    actual = frozenset(table)
    missing = allowed - actual
    extra = actual - allowed
    if missing or extra:
        details = []
        if missing:
            details.append(f"缺少键：{', '.join(sorted(missing))}")
        if extra:
            details.append(f"未知键：{', '.join(sorted(extra))}")
        raise SettingsError(f"{name} 键不精确：{'；'.join(details)}")


def _expect_bool(value: Any, name: str) -> bool:
    if type(value) is not bool:
        raise SettingsError(f"{name} 必须为布尔值")
    return value


def _expect_int(value: Any, name: str, *, minimum: int, maximum: int | None = None) -> int:
    if type(value) is not int:
        raise SettingsError(f"{name} 必须为整数")
    if value < minimum or (maximum is not None and value > maximum):
        boundary = f"{minimum} 到 {maximum}" if maximum is not None else f"不小于 {minimum}"
        raise SettingsError(f"{name} 必须为{boundary}")
    return value


def _expect_choice(value: Any, name: str, choices: frozenset[str]) -> str:
    if type(value) is not str or value not in choices:
        raise SettingsError(f"{name} 不是支持的值")
    return value


def _expect_time(value: Any) -> time:
    if type(value) is not str or not _TIME_RE.fullmatch(value):
        raise SettingsError("schedule.start_time 必须为 HH:MM")
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError as exc:
        raise SettingsError("schedule.start_time 必须为有效时间") from exc


def _expect_weekdays(value: Any) -> tuple[str, ...]:
    if type(value) is not list or not value or any(type(day) is not str for day in value):
        raise SettingsError("schedule.weekdays 必须为非空星期名称列表")
    weekdays = tuple(value)
    if len(set(weekdays)) != len(weekdays) or any(day not in _WEEKDAYS for day in weekdays):
        raise SettingsError("schedule.weekdays 包含无效或重复的星期名称")
    return weekdays


def _expect_timezone(value: Any) -> str:
    if type(value) is not str:
        raise SettingsError("workflow.timezone 必须为时区名称")
    try:
        ZoneInfo(value)
    except ZoneInfoNotFoundError as exc:
        raise SettingsError("workflow.timezone 不是有效 IANA 时区") from exc
    return value
