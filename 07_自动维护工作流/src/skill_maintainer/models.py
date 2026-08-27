"""不可变的工作流配置模型。"""

from dataclasses import dataclass
from datetime import time
from typing import Literal


@dataclass(frozen=True)
class WorkflowSettings:
    enabled: bool
    timezone: str


@dataclass(frozen=True)
class ScheduleSettings:
    mode: Literal["daily", "weekly", "interval", "monthly", "manual"]
    start_time: time
    weekdays: tuple[str, ...]
    interval_days: int
    day_of_month: int


@dataclass(frozen=True)
class ResearchSettings:
    incremental_search: bool
    full_recheck_interval_days: int
    check_existing_skill_updates: bool
    include_generic_skills: bool


@dataclass(frozen=True)
class DeliverySettings:
    generate_word: bool
    generate_excel: bool
    only_refresh_affected_classes: bool
    notify_on_no_change: bool


@dataclass(frozen=True)
class Settings:
    config_version: int
    workflow: WorkflowSettings
    schedule: ScheduleSettings
    research: ResearchSettings
    delivery: DeliverySettings
