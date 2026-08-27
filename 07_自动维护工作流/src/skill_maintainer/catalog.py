"""教育部本科专业目录的只读核验、差异与研究范围构造。"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any, Callable, Mapping, Sequence
from urllib.request import urlopen


class CatalogSourceChangedError(RuntimeError):
    """目录公开源发生变化、但新快照和逐记录差异尚未归档。"""


class TaskProfileReadError(ValueError):
    """Excel 主台账中的专业任务画像不可作为完整、唯一的检索输入。"""


@dataclass(frozen=True)
class CatalogSourceStatus:
    url: str
    expected_sha: str
    actual_sha: str
    changed: bool


@dataclass(frozen=True)
class CatalogSnapshot:
    """待启用的新目录记录及其所对应的公开源内容哈希。"""

    rows: tuple["CatalogRow", ...]
    source_sha: str


@dataclass(frozen=True)
class CatalogRow:
    category_code: str
    category_name: str
    class_code: str | None
    class_name: str | None
    major_code: str
    major_name: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> "CatalogRow":
        return cls(
            category_code=str(value["category_code"]),
            category_name=str(value["category_name"]),
            class_code=_optional_text(value.get("class_code")),
            class_name=_optional_text(value.get("class_name")),
            major_code=str(value["major_code"]),
            major_name=str(value["major_name"]),
        )


@dataclass(frozen=True)
class CatalogRecordChange:
    old: CatalogRow
    new: CatalogRow


@dataclass(frozen=True)
class CatalogDiff:
    added: tuple[CatalogRow, ...] = ()
    removed: tuple[CatalogRow, ...] = ()
    renamed: tuple[CatalogRecordChange, ...] = ()
    major_code_changes: tuple[CatalogRecordChange, ...] = ()
    class_moves: tuple[CatalogRecordChange, ...] = ()
    category_moves: tuple[CatalogRecordChange, ...] = ()

    @property
    def has_record_changes(self) -> bool:
        return any((self.added, self.removed, self.renamed, self.major_code_changes, self.class_moves, self.category_moves))


@dataclass(frozen=True)
class TaskProfile:
    """从 Excel 主台账读取的六维专业任务画像。"""

    professional_aliases: tuple[str, ...] = ()
    core_courses: tuple[str, ...] = ()
    methods: tuple[str, ...] = ()
    work_tasks: tuple[str, ...] = ()
    outputs_and_data: tuple[str, ...] = ()
    software_databases_processes: tuple[str, ...] = ()


@dataclass(frozen=True)
class ResearchScope:
    scope_id: str
    scope_name: str
    scope_kind: str
    category_code: str
    category_name: str
    rows: tuple[CatalogRow, ...]
    task_profile: TaskProfile


@dataclass(frozen=True)
class Catalog:
    rows: tuple[CatalogRow, ...]
    task_profiles: Mapping[str, TaskProfile] = field(default_factory=dict)
    source_status: CatalogSourceStatus | None = None
    staged_snapshot: CatalogSnapshot | None = None
    staged_diff: CatalogDiff | None = None

    def stage_new_snapshot(self, rows: Sequence[CatalogRow], *, snapshot_sha: str) -> "Catalog":
        """绑定实际获取内容的哈希与显式解析出的新目录记录。"""
        if not self.source_status or not self.source_status.changed:
            raise CatalogSourceChangedError("只有已确认变化的目录源可以暂存新快照。")
        if snapshot_sha != self.source_status.actual_sha:
            raise CatalogSourceChangedError("新目录快照哈希必须等于本次公开源实际 SHA-256。")
        new_rows = tuple(rows)
        _require_unique_major_codes(new_rows)
        return Catalog(
            self.rows,
            self.task_profiles,
            self.source_status,
            staged_snapshot=CatalogSnapshot(new_rows, snapshot_sha),
            staged_diff=None,
        )

    def stage_record_diff(self, diff: CatalogDiff) -> "Catalog":
        """只接受由旧记录与已暂存新记录重新计算出的非空逐条差异。"""
        if not self.source_status or not self.source_status.changed or self.staged_snapshot is None:
            raise CatalogSourceChangedError("必须先绑定发生变化的公开源和新目录快照。")
        expected = diff_catalog(self.rows, self.staged_snapshot.rows)
        if not expected.has_record_changes or diff != expected:
            raise CatalogSourceChangedError("必须暂存与旧、新目录逐记录比较完全一致的非空差异。")
        return Catalog(
            self.rows,
            self.task_profiles,
            self.source_status,
            staged_snapshot=self.staged_snapshot,
            staged_diff=diff,
        )


def verify_catalog_source(
    url: str,
    expected_sha: str,
    *,
    fetch: Callable[[str], bytes] | None = None,
) -> CatalogSourceStatus:
    """对公开目录原始字节取哈希；调用者可注入只读 fetch 以便离线核验。"""
    fetcher = fetch or _read_public_bytes
    actual_sha = sha256(fetcher(url)).hexdigest()
    return CatalogSourceStatus(url=url, expected_sha=expected_sha, actual_sha=actual_sha, changed=actual_sha != expected_sha)


def load_catalog(path: Path) -> Catalog:
    """读取既有目录证据，不复制或写出新的目录业务文件。"""
    source = json.loads(path.read_text(encoding="utf-8"))
    rows = tuple(CatalogRow.from_mapping(record) for record in source["records"])
    _require_unique_major_codes(rows)
    return Catalog(rows=rows)


_PROFILE_COLUMNS = (
    "专业别名",
    "核心课程",
    "研究方法",
    "工作任务",
    "成果或数据对象",
    "软件/数据库/流程",
)
_PROFILE_SPLIT_RE = re.compile(r"[；;、,\r\n]+")


def load_catalog_with_ledger(catalog_path: Path, ledger_path: Path) -> Catalog:
    """将目录证据与保存后的 Excel 主台账六维画像合并为内存 Catalog。"""
    catalog = load_catalog(catalog_path)
    return Catalog(rows=catalog.rows, task_profiles=load_task_profiles_from_ledger(ledger_path))


def load_task_profiles_from_ledger(ledger_path: Path) -> Mapping[str, TaskProfile]:
    """通过 LedgerStore 的命名列读取画像，不依赖工作表坐标，也不创建侧车文件。"""
    from .ledger import LedgerStore

    rows = LedgerStore.load(ledger_path).rows("专业任务映射")
    profiles: dict[str, TaskProfile] = {}
    for row_data in rows:
        if not any(_has_visible_value(row_data.get(column)) for column in _PROFILE_COLUMNS):
            continue
        scope_id = _required_text(row_data.get("专业代码"), "专业代码")
        if scope_id in profiles:
            raise TaskProfileReadError(f"专业代码 {scope_id} 存在重复或歧义的六维任务画像。")
        values = [_parse_visible_list(row_data.get(column), column, scope_id) for column in _PROFILE_COLUMNS]
        profiles[scope_id] = TaskProfile(
            professional_aliases=values[0],
            core_courses=values[1],
            methods=values[2],
            work_tasks=values[3],
            outputs_and_data=values[4],
            software_databases_processes=values[5],
        )
    return profiles


def diff_catalog(old_rows: Sequence[CatalogRow], new_rows: Sequence[CatalogRow]) -> CatalogDiff:
    """逐记录比较目录，明确区分新增、撤销、改名、代码和归属移动。"""
    old_by_code = {item.major_code: item for item in old_rows}
    new_by_code = {item.major_code: item for item in new_rows}
    _require_unique_major_codes(old_rows)
    _require_unique_major_codes(new_rows)

    renamed: list[CatalogRecordChange] = []
    class_moves: list[CatalogRecordChange] = []
    category_moves: list[CatalogRecordChange] = []
    for major_code in sorted(old_by_code.keys() & new_by_code.keys()):
        old, new = old_by_code[major_code], new_by_code[major_code]
        if old.major_name != new.major_name:
            renamed.append(CatalogRecordChange(old, new))
        if old.category_code != new.category_code:
            category_moves.append(CatalogRecordChange(old, new))
        elif old.class_code != new.class_code:
            class_moves.append(CatalogRecordChange(old, new))

    unmatched_old = [old_by_code[code] for code in sorted(old_by_code.keys() - new_by_code.keys())]
    unmatched_new = [new_by_code[code] for code in sorted(new_by_code.keys() - old_by_code.keys())]
    old_name_counts = _name_counts(unmatched_old)
    new_name_counts = _name_counts(unmatched_new)
    new_by_name = {
        item.major_name: item
        for item in unmatched_new
        if old_name_counts.get(item.major_name) == 1 and new_name_counts[item.major_name] == 1
    }
    code_changes: list[CatalogRecordChange] = []
    remaining_old: list[CatalogRow] = []
    changed_new_codes: set[str] = set()
    for old in unmatched_old:
        new = new_by_name.get(old.major_name)
        if new is None:
            remaining_old.append(old)
            continue
        code_changes.append(CatalogRecordChange(old, new))
        changed_new_codes.add(new.major_code)

    return CatalogDiff(
        added=tuple(item for item in unmatched_new if item.major_code not in changed_new_codes),
        removed=tuple(remaining_old),
        renamed=tuple(renamed),
        major_code_changes=tuple(code_changes),
        class_moves=tuple(class_moves),
        category_moves=tuple(category_moves),
    )


def build_scopes(catalog: Catalog) -> tuple[ResearchScope, ...]:
    """构造 13 个非军事门类的检索范围，另加 99 跨学科通用。"""
    active_rows = _require_staged_catalog_change(catalog)
    class_groups: dict[str, list[CatalogRow]] = {}
    for item in active_rows:
        if item.category_code in {"11", "14"}:
            continue
        if item.class_code:
            class_groups.setdefault(item.class_code, []).append(item)

    scopes = [
        _scope_for_class(class_code, rows, catalog.task_profiles)
        for class_code, rows in sorted(class_groups.items())
    ]
    interdisciplinary = [item for item in active_rows if item.category_code == "14"]
    scopes.extend(_scope_for_major(item, catalog.task_profiles) for item in interdisciplinary)
    scopes.append(
        ResearchScope(
            scope_id="99",
            scope_name="跨学科通用",
            scope_kind="generic",
            category_code="99",
            category_name="跨学科通用",
            rows=(),
            task_profile=catalog.task_profiles.get("99", TaskProfile()),
        )
    )
    return tuple(scopes)


def _scope_for_class(class_code: str, rows: list[CatalogRow], profiles: Mapping[str, TaskProfile]) -> ResearchScope:
    first = rows[0]
    return ResearchScope(
        scope_id=class_code,
        scope_name=first.class_name or class_code,
        scope_kind="professional_class",
        category_code=first.category_code,
        category_name=first.category_name,
        rows=tuple(rows),
        task_profile=profiles.get(class_code, TaskProfile()),
    )


def _scope_for_major(item: CatalogRow, profiles: Mapping[str, TaskProfile]) -> ResearchScope:
    return ResearchScope(
        scope_id=item.major_code,
        scope_name=item.major_name,
        scope_kind="interdisciplinary_major",
        category_code=item.category_code,
        category_name=item.category_name,
        rows=(item,),
        task_profile=profiles.get(item.major_code, TaskProfile()),
    )


def _require_staged_catalog_change(catalog: Catalog) -> tuple[CatalogRow, ...]:
    if catalog.source_status and catalog.source_status.changed:
        if catalog.staged_snapshot is None or catalog.staged_diff is None:
            raise CatalogSourceChangedError("目录公开源内容已变化；必须先暂存新快照和逐记录差异，才能生成检索范围。")
        if catalog.staged_snapshot.source_sha != catalog.source_status.actual_sha:
            raise CatalogSourceChangedError("暂存目录快照未绑定本次公开源实际 SHA-256。")
        expected = diff_catalog(catalog.rows, catalog.staged_snapshot.rows)
        if not expected.has_record_changes or catalog.staged_diff != expected:
            raise CatalogSourceChangedError("暂存目录差异不是旧、新快照的精确非空逐记录差异。")
        return catalog.staged_snapshot.rows
    return catalog.rows


def _read_public_bytes(url: str) -> bytes:
    with urlopen(url, timeout=30) as response:  # nosec B310 - only the explicit official URL is passed by the caller
        return response.read()


def _optional_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _has_visible_value(value: Any) -> bool:
    return type(value) is str and bool(value.strip())


def _required_text(value: Any, column: str) -> str:
    if not _has_visible_value(value):
        raise TaskProfileReadError(f"专业任务映射缺少 {column}。")
    return value.strip()


def _parse_visible_list(value: Any, column: str, scope_id: str) -> tuple[str, ...]:
    if not _has_visible_value(value):
        raise TaskProfileReadError(f"专业代码 {scope_id} 缺少完整六维画像字段：{column}。")
    terms = tuple(dict.fromkeys(term.strip() for term in _PROFILE_SPLIT_RE.split(value) if term.strip()))
    if not terms:
        raise TaskProfileReadError(f"专业代码 {scope_id} 的 {column} 没有可见检索词。")
    return terms


def _name_counts(rows: Sequence[CatalogRow]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in rows:
        counts[item.major_name] = counts.get(item.major_name, 0) + 1
    return counts


def _require_unique_major_codes(rows: Sequence[CatalogRow]) -> None:
    codes = [item.major_code for item in rows]
    if len(codes) != len(set(codes)):
        raise ValueError("目录专业代码必须唯一")
