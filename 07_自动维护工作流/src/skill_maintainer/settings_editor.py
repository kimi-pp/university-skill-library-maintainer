"""Chinese Tk editor and pure conversions for workflow settings."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from datetime import datetime
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Callable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .models import (
    DeliverySettings,
    ResearchSettings,
    ScheduleSettings,
    Settings,
    WorkflowSettings,
)
from .scheduling import schedule_preview
from .settings import SettingsError, load_settings


_MODE_TO_CHINESE = {
    "daily": "每天",
    "weekly": "每周",
    "interval": "按间隔天数",
    "monthly": "每月",
    "manual": "手动",
}
_CHINESE_TO_MODE = {label: mode for mode, label in _MODE_TO_CHINESE.items()}
_WEEKDAY_TO_CHINESE = {
    "Monday": "星期一",
    "Tuesday": "星期二",
    "Wednesday": "星期三",
    "Thursday": "星期四",
    "Friday": "星期五",
    "Saturday": "星期六",
    "Sunday": "星期日",
}
_CHINESE_TO_WEEKDAY = {label: day for day, label in _WEEKDAY_TO_CHINESE.items()}
_TIME_RE = re.compile(r"\d{2}:\d{2}\Z")


@dataclass(frozen=True)
class SettingsForm:
    """White-listed values exposed by the settings form."""

    enabled: bool
    timezone: str
    mode: str
    start_time: str
    weekdays: tuple[str, ...]
    interval_days: str
    day_of_month: str
    incremental_search: bool
    full_recheck_interval_days: str
    check_existing_skill_updates: bool
    include_generic_skills: bool
    generate_word: bool
    generate_excel: bool
    only_refresh_affected_classes: bool
    notify_on_no_change: bool


def settings_to_form(settings: Settings) -> SettingsForm:
    """Convert validated settings to the Chinese form representation."""
    return SettingsForm(
        enabled=settings.workflow.enabled,
        timezone=settings.workflow.timezone,
        mode=_MODE_TO_CHINESE[settings.schedule.mode],
        start_time=settings.schedule.start_time.strftime("%H:%M"),
        weekdays=tuple(_WEEKDAY_TO_CHINESE[day] for day in settings.schedule.weekdays),
        interval_days=str(settings.schedule.interval_days),
        day_of_month=str(settings.schedule.day_of_month),
        incremental_search=settings.research.incremental_search,
        full_recheck_interval_days=str(settings.research.full_recheck_interval_days),
        check_existing_skill_updates=settings.research.check_existing_skill_updates,
        include_generic_skills=settings.research.include_generic_skills,
        generate_word=settings.delivery.generate_word,
        generate_excel=settings.delivery.generate_excel,
        only_refresh_affected_classes=settings.delivery.only_refresh_affected_classes,
        notify_on_no_change=settings.delivery.notify_on_no_change,
    )


def form_to_settings(form: SettingsForm) -> Settings:
    """Validate and convert Chinese form values without opening a window."""
    _validate_boolean_fields(form)
    mode = _CHINESE_TO_MODE.get(form.mode)
    if mode is None:
        raise SettingsError("运行模式不是支持的中文选项")
    if not _TIME_RE.fullmatch(form.start_time):
        raise SettingsError("启动时间必须为 HH:MM")
    try:
        start_time = datetime.strptime(form.start_time, "%H:%M").time()
    except ValueError as exc:
        raise SettingsError("启动时间必须为有效时间") from exc
    if type(form.timezone) is not str:
        raise SettingsError("时区必须为 IANA 名称")
    try:
        ZoneInfo(form.timezone)
    except (ValueError, ZoneInfoNotFoundError) as exc:
        raise SettingsError("时区不是有效 IANA 名称") from exc
    if type(form.weekdays) is not tuple or not form.weekdays:
        raise SettingsError("星期必须为非空中文选项列表")
    if len(set(form.weekdays)) != len(form.weekdays):
        raise SettingsError("星期不能重复")
    try:
        weekdays = tuple(_CHINESE_TO_WEEKDAY[label] for label in form.weekdays)
    except (KeyError, TypeError) as exc:
        raise SettingsError("星期包含不支持的中文选项") from exc

    return Settings(
        config_version=1,
        workflow=WorkflowSettings(enabled=form.enabled, timezone=form.timezone),
        schedule=ScheduleSettings(
            mode=mode,
            start_time=start_time,
            weekdays=weekdays,
            interval_days=_positive_integer(form.interval_days, "间隔天数"),
            day_of_month=_positive_integer(form.day_of_month, "每月日期", maximum=28),
        ),
        research=ResearchSettings(
            incremental_search=form.incremental_search,
            full_recheck_interval_days=_positive_integer(
                form.full_recheck_interval_days, "全量复核间隔"
            ),
            check_existing_skill_updates=form.check_existing_skill_updates,
            include_generic_skills=form.include_generic_skills,
        ),
        delivery=DeliverySettings(
            generate_word=form.generate_word,
            generate_excel=form.generate_excel,
            only_refresh_affected_classes=form.only_refresh_affected_classes,
            notify_on_no_change=form.notify_on_no_change,
        ),
    )


def settings_to_toml(settings: Settings) -> str:
    """Serialize the complete settings model to deterministic UTF-8 TOML."""
    quote = lambda value: json.dumps(value, ensure_ascii=False)
    boolean = lambda value: "true" if value else "false"
    weekdays = ", ".join(quote(day) for day in settings.schedule.weekdays)
    return (
        f"config_version = {settings.config_version}\n\n"
        "[workflow]\n"
        f"enabled = {boolean(settings.workflow.enabled)}\n"
        f"timezone = {quote(settings.workflow.timezone)}\n\n"
        "[schedule]\n"
        f"mode = {quote(settings.schedule.mode)}\n"
        f"start_time = {quote(settings.schedule.start_time.strftime('%H:%M'))}\n"
        f"weekdays = [{weekdays}]\n"
        f"interval_days = {settings.schedule.interval_days}\n"
        f"day_of_month = {settings.schedule.day_of_month}\n\n"
        "[research]\n"
        f"incremental_search = {boolean(settings.research.incremental_search)}\n"
        f"full_recheck_interval_days = {settings.research.full_recheck_interval_days}\n"
        f"check_existing_skill_updates = {boolean(settings.research.check_existing_skill_updates)}\n"
        f"include_generic_skills = {boolean(settings.research.include_generic_skills)}\n\n"
        "[delivery]\n"
        f"generate_word = {boolean(settings.delivery.generate_word)}\n"
        f"generate_excel = {boolean(settings.delivery.generate_excel)}\n"
        f"only_refresh_affected_classes = {boolean(settings.delivery.only_refresh_affected_classes)}\n"
        f"notify_on_no_change = {boolean(settings.delivery.notify_on_no_change)}\n"
    )


def save_settings_atomic(
    path: Path,
    settings: Settings,
    *,
    replace_file: Callable[[str | os.PathLike[str], str | os.PathLike[str]], None] = os.replace,
) -> None:
    """Validate a same-directory temporary file, then atomically replace target."""
    target = Path(path).absolute()
    if not target.parent.is_dir():
        raise SettingsError("设置文件目录不存在")
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=f".{target.name}.",
            suffix=".tmp",
            dir=target.parent,
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(settings_to_toml(settings))
            handle.flush()
            os.fsync(handle.fileno())
        if load_settings(temporary) != settings:
            raise SettingsError("临时设置复读不一致")
        replace_file(temporary, target)
    except OSError as exc:
        raise SettingsError("无法原子保存设置") from exc
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def apply_form_edit(
    path: Path,
    form: SettingsForm | None,
    *,
    replace_file: Callable[[str | os.PathLike[str], str | os.PathLike[str]], None] = os.replace,
) -> bool:
    """Apply a validated form; a cancelled form is an exact no-op."""
    if form is None:
        return False
    settings = form_to_settings(form)
    save_settings_atomic(path, settings, replace_file=replace_file)
    return True


def run_editor(path: Path) -> bool:
    """Open the Chinese Tk wrapper around the pure form operations."""
    import tkinter as tk
    from tkinter import messagebox, ttk

    original = settings_to_form(load_settings(path))
    root = tk.Tk()
    root.title("修改运行设置")
    root.resizable(False, False)
    frame = ttk.Frame(root, padding=16)
    frame.grid(sticky="nsew")

    enabled = tk.BooleanVar(value=original.enabled)
    mode = tk.StringVar(value=original.mode)
    start_time = tk.StringVar(value=original.start_time)
    interval_days = tk.StringVar(value=original.interval_days)
    day_of_month = tk.StringVar(value=original.day_of_month)
    full_recheck = tk.StringVar(value=original.full_recheck_interval_days)
    weekday_values = {
        label: tk.BooleanVar(value=label in original.weekdays)
        for label in _CHINESE_TO_WEEKDAY
    }
    result = {"saved": False}

    ttk.Checkbutton(frame, text="启用自动运行", variable=enabled).grid(row=0, column=0, columnspan=2, sticky="w")
    ttk.Label(frame, text="运行模式").grid(row=1, column=0, sticky="w", pady=4)
    ttk.Combobox(frame, textvariable=mode, state="readonly", values=tuple(_CHINESE_TO_MODE), width=18).grid(row=1, column=1, sticky="ew")
    ttk.Label(frame, text="启动时间（HH:MM）").grid(row=2, column=0, sticky="w", pady=4)
    ttk.Entry(frame, textvariable=start_time, width=20).grid(row=2, column=1, sticky="ew")
    ttk.Label(frame, text="每周运行日").grid(row=3, column=0, sticky="nw", pady=4)
    days = ttk.Frame(frame)
    days.grid(row=3, column=1, sticky="w")
    for index, (label, variable) in enumerate(weekday_values.items()):
        ttk.Checkbutton(days, text=label[-1], variable=variable).grid(row=index // 4, column=index % 4, sticky="w")
    ttk.Label(frame, text="间隔天数").grid(row=4, column=0, sticky="w", pady=4)
    ttk.Entry(frame, textvariable=interval_days, width=20).grid(row=4, column=1, sticky="ew")
    ttk.Label(frame, text="每月日期（1–28）").grid(row=5, column=0, sticky="w", pady=4)
    ttk.Entry(frame, textvariable=day_of_month, width=20).grid(row=5, column=1, sticky="ew")
    ttk.Label(frame, text="全量复核间隔（天）").grid(row=6, column=0, sticky="w", pady=4)
    ttk.Entry(frame, textvariable=full_recheck, width=20).grid(row=6, column=1, sticky="ew")

    def current_form() -> SettingsForm:
        return replace(
            original,
            enabled=enabled.get(),
            mode=mode.get(),
            start_time=start_time.get(),
            weekdays=tuple(label for label, variable in weekday_values.items() if variable.get()),
            interval_days=interval_days.get(),
            day_of_month=day_of_month.get(),
            full_recheck_interval_days=full_recheck.get(),
        )

    def save() -> None:
        try:
            form = current_form()
            preview = schedule_preview(form_to_settings(form))
        except SettingsError as exc:
            messagebox.showerror("设置无效", str(exc), parent=root)
            return
        if not messagebox.askokcancel("确认保存", preview, parent=root):
            return
        try:
            apply_form_edit(path, form)
        except SettingsError as exc:
            messagebox.showerror("保存失败", str(exc), parent=root)
            return
        result["saved"] = True
        root.destroy()

    buttons = ttk.Frame(frame)
    buttons.grid(row=7, column=0, columnspan=2, sticky="e", pady=(12, 0))
    ttk.Button(buttons, text="取消", command=root.destroy).grid(row=0, column=0, padx=4)
    ttk.Button(buttons, text="预览并保存", command=save).grid(row=0, column=1, padx=4)
    root.mainloop()
    return result["saved"]


def _positive_integer(value: str, name: str, maximum: int | None = None) -> int:
    if type(value) is not str or not re.fullmatch(r"[1-9]\d*", value):
        raise SettingsError(f"{name}必须为正整数")
    number = int(value)
    if maximum is not None and number > maximum:
        raise SettingsError(f"{name}必须为 1 到 {maximum}")
    return number


def _validate_boolean_fields(form: SettingsForm) -> None:
    fields = (
        "enabled",
        "incremental_search",
        "check_existing_skill_updates",
        "include_generic_skills",
        "generate_word",
        "generate_excel",
        "only_refresh_affected_classes",
        "notify_on_no_change",
    )
    if any(type(getattr(form, field)) is not bool for field in fields):
        raise SettingsError("开关字段必须为布尔值")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="打开中文工作流设置表单")
    parser.add_argument("--settings", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        run_editor(args.settings.absolute())
    except SettingsError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
