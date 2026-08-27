"""确定性的本地日历调度计算。"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from .models import Settings


_WEEKDAY_INDEX = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}
_WEEKDAY_CHINESE = {
    "Monday": "一",
    "Tuesday": "二",
    "Wednesday": "三",
    "Thursday": "四",
    "Friday": "五",
    "Saturday": "六",
    "Sunday": "日",
}


def next_run_at(
    settings: Settings,
    after: datetime,
    last_success_at: datetime | None = None,
) -> datetime | None:
    """返回严格晚于 ``after`` 的下一个本地运行时刻。"""
    zone = ZoneInfo(settings.workflow.timezone)
    local_after = _to_local(after, zone, "after")
    mode = settings.schedule.mode
    if mode == "manual":
        return None
    if mode == "daily":
        return _next_daily(settings, local_after, zone)
    if mode == "weekly":
        return _next_weekly(settings, local_after, zone)
    if mode == "monthly":
        return _next_monthly(settings, local_after, zone)

    if last_success_at is None:
        return _next_daily(settings, local_after, zone)
    candidate = _to_local(last_success_at, zone, "last_success_at") + timedelta(
        days=settings.schedule.interval_days
    )
    while candidate <= local_after:
        candidate += timedelta(days=settings.schedule.interval_days)
    return candidate


def schedule_preview(settings: Settings) -> str:
    """生成不创建任何自动任务的中文设置预览。"""
    schedule = settings.schedule
    time_text = schedule.start_time.strftime("%H:%M")
    if schedule.mode == "daily":
        cadence = f"每天 {time_text}（{settings.workflow.timezone}）运行"
    elif schedule.mode == "weekly":
        weekdays = "、".join(_WEEKDAY_CHINESE[day] for day in schedule.weekdays)
        cadence = f"每周{weekdays} {time_text}（{settings.workflow.timezone}）运行"
    elif schedule.mode == "interval":
        cadence = f"每 {schedule.interval_days} 天于 {time_text}（{settings.workflow.timezone}）运行"
    elif schedule.mode == "monthly":
        cadence = f"每月 {schedule.day_of_month} 日 {time_text}（{settings.workflow.timezone}）运行"
    else:
        cadence = f"手动运行（{settings.workflow.timezone}）"
    enabled = "已启用" if settings.workflow.enabled else "未启用"
    return f"{enabled}；{cadence}；每 {settings.research.full_recheck_interval_days} 天执行一次全量复核。"


def _to_local(value: datetime, zone: ZoneInfo, name: str) -> datetime:
    if value.tzinfo is None:
        raise ValueError(f"{name} 必须带有时区")
    return value.astimezone(zone)


def _next_daily(settings: Settings, after: datetime, zone: ZoneInfo) -> datetime:
    candidate = datetime.combine(after.date(), settings.schedule.start_time, tzinfo=zone)
    if candidate <= after:
        candidate += timedelta(days=1)
    return candidate


def _next_weekly(settings: Settings, after: datetime, zone: ZoneInfo) -> datetime:
    allowed = {_WEEKDAY_INDEX[day] for day in settings.schedule.weekdays}
    for offset in range(8):
        date = after.date() + timedelta(days=offset)
        candidate = datetime.combine(date, settings.schedule.start_time, tzinfo=zone)
        if date.weekday() in allowed and candidate > after:
            return candidate
    raise AssertionError("有效星期配置必须在七天内产生候选时刻")


def _next_monthly(settings: Settings, after: datetime, zone: ZoneInfo) -> datetime:
    year, month = after.year, after.month
    candidate = datetime(year, month, settings.schedule.day_of_month, settings.schedule.start_time.hour, settings.schedule.start_time.minute, tzinfo=zone)
    if candidate <= after:
        if month == 12:
            year, month = year + 1, 1
        else:
            month += 1
        candidate = datetime(year, month, settings.schedule.day_of_month, settings.schedule.start_time.hour, settings.schedule.start_time.minute, tzinfo=zone)
    return candidate
