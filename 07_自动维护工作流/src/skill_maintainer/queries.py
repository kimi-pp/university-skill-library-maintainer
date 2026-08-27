"""从已冻结研究范围生成内存中的六维检索任务。"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from .catalog import ResearchScope, TaskProfile


PLATFORM_ORDER = ("SkillHub", "ClawHub", "GitHub", "Hugging Face Spaces")


class TaskProfileIncompleteError(ValueError):
    """Excel 主台账尚未提供完整的六维专业任务画像。"""


@dataclass(frozen=True)
class QueryJob:
    query_id: str
    scope_id: str
    platform: str
    dimension: str
    query: str


def build_queries(scope: ResearchScope) -> tuple[QueryJob, ...]:
    """按固定平台顺序构造任务；只返回内存对象，不建立检索任务仓库。"""
    dimensions = _dimensions(scope.task_profile)
    missing = [name for name, terms in dimensions if not terms]
    if missing:
        raise TaskProfileIncompleteError(f"{scope.scope_id} 缺少 Excel 专业任务画像维度：{', '.join(missing)}")

    jobs: list[QueryJob] = []
    for platform in PLATFORM_ORDER:
        for dimension, terms in dimensions:
            for term in terms:
                query = f"{term} Skill"
                identity = f"{scope.scope_id}|{platform}|{dimension}|{query}"
                jobs.append(QueryJob(
                    query_id=f"Q-{sha256(identity.encode('utf-8')).hexdigest()[:16]}",
                    scope_id=scope.scope_id,
                    platform=platform,
                    dimension=dimension,
                    query=query,
                ))
    return tuple(jobs)


def _dimensions(profile: TaskProfile) -> tuple[tuple[str, tuple[str, ...]], ...]:
    return (
        ("professional_alias", _unique_terms(profile.professional_aliases)),
        ("core_course", _unique_terms(profile.core_courses)),
        ("method", _unique_terms(profile.methods)),
        ("work_task", _unique_terms(profile.work_tasks)),
        ("output_or_data", _unique_terms(profile.outputs_and_data)),
        ("software_database_or_process", _unique_terms(profile.software_databases_processes)),
    )


def _unique_terms(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value.strip() for value in values if value.strip()))
