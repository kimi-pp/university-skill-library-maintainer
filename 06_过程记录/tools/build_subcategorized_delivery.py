"""Build Task 6 through recoverable directory transactions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable

from build_subcategorized_documents import generate_documents, load_inputs
from verify_subcategorized_documents import verify_selected_documents


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_RELATIVE = Path("05_交付物") / "通俗细分版_2026-08-07"
ARCHIVE_NAME = "原始版_2026-08-06"
ASSIGNMENT_RELATIVE = Path("03_候选池") / "derived" / "subcategory_assignments.json"
NODE = Path(r"C:\Users\34927\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
XLSX_BUILDER = PROJECT_ROOT / "06_过程记录" / "tools" / "build_subcategorized_spreadsheets.mjs"
XLSX_VERIFIER = PROJECT_ROOT / "06_过程记录" / "tools" / "verify_subcategorized_spreadsheets.mjs"
ORIGINAL_PATTERN = re.compile(r"^(0[1-5])_(.+)\.(docx|xlsx)$", re.IGNORECASE)
AMBIGUOUS_PREFIX_PATTERN = re.compile(r"^(0[1-5]).*\.(docx|xlsx)$", re.IGNORECASE)


@dataclass(frozen=True)
class TransactionPaths:
    name: str
    project_root: Path
    final: Path
    stage_root: Path
    stage_dir: Path
    backup: Path
    marker: Path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _absolute(path: Path) -> Path:
    """Return a normalized absolute path without following links/reparse points."""
    return Path(os.path.abspath(path))


def _inside(path: Path, root: Path) -> bool:
    try:
        _absolute(path).relative_to(_absolute(root))
        return True
    except ValueError:
        return False


def _require_exact(path: Path, expected: Path, label: str) -> Path:
    actual = _absolute(path)
    wanted = _absolute(expected)
    if actual != wanted:
        raise ValueError(f"{label}不安全: expected={wanted} actual={actual}")
    return actual


def _path_exists_unfollowed(path: Path) -> bool:
    return os.path.lexists(path)


def _is_reparse_point(path: Path) -> bool:
    if not _path_exists_unfollowed(path):
        return False
    if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
        return True
    attributes = getattr(os.lstat(path), "st_file_attributes", 0)
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _expected_transaction_locations(paths: TransactionPaths) -> tuple[dict[str, Path], dict[str, Path]]:
    project = _absolute(paths.project_root)
    delivery_root = project / "05_交付物"
    if paths.name == "archive":
        expected = {
            "final": delivery_root / ARCHIVE_NAME,
            "stage_root": delivery_root / ".task6_archive.stage",
            "stage_dir": delivery_root / ".task6_archive.stage",
            "backup": delivery_root / ".task6_archive.backup",
            "marker": delivery_root / ".task6_archive.transaction.json",
            "marker_tmp": delivery_root / ".task6_archive.transaction.json.tmp",
        }
        allowed_parents = {field: delivery_root for field in expected}
    elif paths.name == "delivery":
        stage_root = project / "06_过程记录" / ".task6_delivery.stage"
        expected = {
            "final": delivery_root / "通俗细分版_2026-08-07",
            "stage_root": stage_root,
            "stage_dir": stage_root / OUTPUT_RELATIVE,
            "backup": delivery_root / ".task6_delivery.backup",
            "marker": delivery_root / ".task6_delivery.transaction.json",
            "marker_tmp": delivery_root / ".task6_delivery.transaction.json.tmp",
        }
        allowed_parents = {
            "final": delivery_root,
            "stage_root": project / "06_过程记录",
            "stage_dir": stage_root,
            "backup": delivery_root,
            "marker": delivery_root,
            "marker_tmp": delivery_root,
        }
    else:
        raise ValueError(f"未知任务事务: {paths.name}")
    return ({field: _absolute(path) for field, path in expected.items()}, allowed_parents)


def _validate_owned_transaction_path(paths: TransactionPaths, field: str) -> Path:
    expected, allowed_parents = _expected_transaction_locations(paths)
    if field not in expected:
        raise ValueError(f"未知任务路径字段: {field}")
    actual_value = paths.marker.with_name(f"{paths.marker.name}.tmp") if field == "marker_tmp" else getattr(paths, field)
    actual = _absolute(actual_value)
    if actual != expected[field]:
        raise ValueError(f"{paths.name}.{field} 字面路径不安全: expected={expected[field]} actual={actual}")
    allowed_parent = _absolute(allowed_parents[field])
    if field == "stage_dir" and paths.name == "delivery":
        if not _inside(actual, allowed_parent) or actual == allowed_parent:
            raise ValueError(f"{paths.name}.{field} 父目录越界: {actual}")
    elif actual.parent != allowed_parent:
        raise ValueError(f"{paths.name}.{field} 父目录不安全: {actual.parent}")
    project = _absolute(paths.project_root)
    try:
        relative = actual.relative_to(project)
    except ValueError as error:
        raise ValueError(f"{paths.name}.{field} 超出项目范围: {actual}") from error
    current = project
    for component in relative.parts:
        current /= component
        if _is_reparse_point(current):
            raise ValueError(f"{paths.name}.{field} 含链接或重解析点: {current}")
    return actual


def _validate_transaction_paths(paths: TransactionPaths) -> None:
    for field in ("final", "stage_root", "stage_dir", "backup", "marker", "marker_tmp"):
        _validate_owned_transaction_path(paths, field)


def _remove_owned_directory(paths: TransactionPaths, field: str) -> None:
    target = _validate_owned_transaction_path(paths, field)
    if not _path_exists_unfollowed(target):
        return
    if not target.is_dir():
        raise ValueError(f"{paths.name}.{field} 不是普通目录: {target}")
    shutil.rmtree(target)


def _remove_owned_file(paths: TransactionPaths, field: str) -> None:
    target = _validate_owned_transaction_path(paths, field)
    if not _path_exists_unfollowed(target):
        return
    if not target.is_file():
        raise ValueError(f"{paths.name}.{field} 不是普通文件: {target}")
    target.unlink()


def _replace_transaction_path(
    paths: TransactionPaths,
    source_field: str,
    target_field: str,
    replace_path: Callable[[Path, Path], object],
) -> None:
    source = _validate_owned_transaction_path(paths, source_field)
    target = _validate_owned_transaction_path(paths, target_field)
    replace_path(source, target)


def discover_originals(delivery_root: Path) -> list[Path]:
    """Require exactly one DOCX and one XLSX for each code 01 through 05."""
    root = _absolute(delivery_root)
    if not root.is_dir():
        raise ValueError(f"原始文件根目录不存在: {root}")
    buckets: dict[str, dict[str, list[Path]]] = {
        f"{number:02d}": {"docx": [], "xlsx": []} for number in range(1, 6)
    }
    ambiguous: list[str] = []
    for path in root.iterdir():
        if not path.is_file():
            continue
        match = ORIGINAL_PATTERN.fullmatch(path.name)
        if match:
            code, _stem, suffix = match.groups()
            buckets[code][suffix.lower()].append(path.resolve())
        elif AMBIGUOUS_PREFIX_PATTERN.fullmatch(path.name):
            ambiguous.append(path.name)
    issues: list[str] = []
    for code in sorted(buckets):
        for suffix in ("docx", "xlsx"):
            matches = buckets[code][suffix]
            if len(matches) != 1:
                issues.append(f"{code}.{suffix}={len(matches)}")
    if ambiguous:
        issues.append(f"同名前缀歧义={sorted(ambiguous)}")
    if issues:
        raise ValueError(f"原始文件格式配对不明确: {'; '.join(issues)}")
    return [buckets[code][suffix][0] for code in sorted(buckets) for suffix in ("docx", "xlsx")]


def _snapshot_sources(sources: list[Path]) -> dict[str, tuple[int, str]]:
    if len(sources) != 10 or len({path.name.casefold() for path in sources}) != 10:
        raise ValueError("原始文件必须恰好是 10 个唯一文件")
    snapshot = {path.name: (path.stat().st_size, _sha256(path)) for path in sources}
    return dict(sorted(snapshot.items()))


def _inventory(sources: list[Path], archive_root: Path | None = None) -> list[dict[str, object]]:
    inventory: list[dict[str, object]] = []
    for source in sources:
        row: dict[str, object] = {
            "source": str(source.resolve()),
            "bytes": source.stat().st_size,
            "sha256": _sha256(source),
        }
        if archive_root is not None:
            row["archived"] = str((_absolute(archive_root) / source.name))
        inventory.append(row)
    return inventory


def expected_delivery_paths(manifest: list[dict]) -> set[Path]:
    """Validate the exact 5 overview pairs and 61 subcategory pairs."""
    if len(manifest) != 132:
        raise ValueError(f"manifest 必须恰好 132 项，实际 {len(manifest)}")
    expected: set[Path] = set()
    formats: Counter[str] = Counter()
    scopes: Counter[str] = Counter()
    stems: defaultdict[str, set[str]] = defaultdict(set)
    overview_codes: set[str] = set()
    subcategory_codes: set[str] = set()
    prefix = PurePosixPath("05_交付物/通俗细分版_2026-08-07")
    for item in manifest:
        raw = item.get("path")
        file_format = item.get("format")
        scope = item.get("scope")
        if not isinstance(raw, str) or "\\" in raw:
            raise ValueError(f"manifest 路径不安全: {raw!r}")
        pure = PurePosixPath(raw)
        if pure.is_absolute() or ".." in pure.parts or pure.parts[: len(prefix.parts)] != prefix.parts:
            raise ValueError(f"manifest 路径越界: {raw}")
        if file_format not in {"docx", "xlsx"} or pure.suffix != f".{file_format}":
            raise ValueError(f"manifest 格式不一致: {raw}")
        relative = Path(*pure.parts)
        if relative in expected:
            raise ValueError(f"manifest 路径重复: {raw}")
        expected.add(relative)
        formats[file_format] += 1
        scopes[scope] += 1
        stems[str(pure.with_suffix(""))].add(file_format)
        if scope == "overview":
            overview_codes.add(str(item.get("big_category_code")))
        elif scope == "subcategory":
            subcategory_codes.add(str(item.get("subcategory_code")))
        else:
            raise ValueError(f"manifest scope 无效: {scope!r}")
    if formats != {"docx": 66, "xlsx": 66} or scopes != {"overview": 10, "subcategory": 122}:
        raise ValueError(f"manifest 统计错误: formats={dict(formats)} scopes={dict(scopes)}")
    if overview_codes != {f"{number:02d}" for number in range(1, 6)} or len(subcategory_codes) != 61:
        raise ValueError("manifest 未完整覆盖 5 个概览或 61 个小分类")
    unpaired = sorted(stem for stem, suffixes in stems.items() if suffixes != {"docx", "xlsx"})
    if unpaired or len(stems) != 66:
        raise ValueError(f"manifest DOCX/XLSX 配对错误: {unpaired}")
    return expected


def _expected_delivery_contents(manifest: list[dict]) -> set[Path]:
    return {path.relative_to(OUTPUT_RELATIVE) for path in expected_delivery_paths(manifest)}


def _validate_exact_files(directory: Path, expected: dict[str, tuple[int, str]]) -> None:
    if not directory.is_dir():
        raise ValueError(f"目录不存在: {directory}")
    actual_files = [path for path in directory.rglob("*") if path.is_file()]
    actual_names = {path.relative_to(directory).as_posix() for path in actual_files}
    if actual_names != set(expected):
        raise ValueError(
            f"目录文件集合不一致: missing={sorted(set(expected) - actual_names)} "
            f"extra={sorted(actual_names - set(expected))}"
        )
    for relative, (size, digest) in expected.items():
        path = directory / Path(*relative.split("/"))
        if path.stat().st_size != size or _sha256(path) != digest:
            raise ValueError(f"目录文件校验失败: {relative}")


def _validate_archive(directory: Path, source_snapshot: dict[str, tuple[int, str]]) -> None:
    _validate_exact_files(directory, source_snapshot)


def _validate_delivery(directory: Path, manifest: list[dict]) -> None:
    if not directory.is_dir():
        raise ValueError(f"交付目录不存在: {directory}")
    expected = _expected_delivery_contents(manifest)
    actual = {path.relative_to(directory) for path in directory.rglob("*") if path.is_file()}
    if actual != expected:
        raise ValueError(
            f"交付集合不完整: missing={sorted(map(str, expected - actual))} "
            f"extra={sorted(map(str, actual - expected))}"
        )
    empty = [str(path) for path in expected if (directory / path).stat().st_size <= 0]
    if empty:
        raise ValueError(f"交付文件为空: {empty}")


def archive_transaction_paths(project_root: Path, archive_root: Path | None = None) -> TransactionPaths:
    project = _absolute(project_root)
    delivery_root = project / "05_交付物"
    expected_final = delivery_root / ARCHIVE_NAME
    final = _require_exact(archive_root or expected_final, expected_final, "归档目标")
    if final in {project, delivery_root} or not _inside(final, delivery_root):
        raise ValueError(f"归档目标不安全: {final}")
    stage = delivery_root / ".task6_archive.stage"
    return TransactionPaths(
        name="archive",
        project_root=project,
        final=final,
        stage_root=stage,
        stage_dir=stage,
        backup=delivery_root / ".task6_archive.backup",
        marker=delivery_root / ".task6_archive.transaction.json",
    )


def delivery_transaction_paths(project_root: Path) -> TransactionPaths:
    project = _absolute(project_root)
    delivery_root = project / "05_交付物"
    final = _require_exact(project / OUTPUT_RELATIVE, delivery_root / "通俗细分版_2026-08-07", "交付目标")
    stage_root = project / "06_过程记录" / ".task6_delivery.stage"
    return TransactionPaths(
        name="delivery",
        project_root=project,
        final=final,
        stage_root=stage_root,
        stage_dir=stage_root / OUTPUT_RELATIVE,
        backup=delivery_root / ".task6_delivery.backup",
        marker=delivery_root / ".task6_delivery.transaction.json",
    )


def _write_marker(paths: TransactionPaths, phase: str) -> None:
    _validate_transaction_paths(paths)
    paths.marker.parent.mkdir(parents=True, exist_ok=True)
    temporary = _validate_owned_transaction_path(paths, "marker_tmp")
    temporary.write_text(
        json.dumps(
            {
                "task": "subcategory-delivery-task6",
                "name": paths.name,
                "phase": phase,
                "final": str(paths.final),
                "stage": str(paths.stage_root),
                "backup": str(paths.backup),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    _replace_transaction_path(paths, "marker_tmp", "marker", os.replace)


def _cleanup_transaction_artifacts(paths: TransactionPaths, *, remove_backup: bool = False) -> None:
    _remove_owned_directory(paths, "stage_root")
    if remove_backup:
        _remove_owned_directory(paths, "backup")
    _remove_owned_file(paths, "marker")
    _remove_owned_file(paths, "marker_tmp")


def recover_directory_transaction(
    paths: TransactionPaths,
    validator: Callable[[Path], None],
    *,
    replace_path: Callable[[Path, Path], object] = os.replace,
) -> None:
    """Recover a previous crash using stable task-owned stage/backup paths."""
    _validate_transaction_paths(paths)
    final_exists = _path_exists_unfollowed(paths.final)
    backup_exists = _path_exists_unfollowed(paths.backup)
    if final_exists and backup_exists:
        try:
            validator(paths.final)
        except Exception:
            validator(paths.backup)
            _remove_owned_directory(paths, "final")
            _replace_transaction_path(paths, "backup", "final", replace_path)
        else:
            _remove_owned_directory(paths, "backup")
    elif not final_exists and backup_exists:
        validator(paths.backup)
        _replace_transaction_path(paths, "backup", "final", replace_path)
    elif final_exists:
        validator(paths.final)
    _cleanup_transaction_artifacts(paths, remove_backup=False)


def _rollback_transaction(
    paths: TransactionPaths,
    *,
    had_final: bool,
    replace_path: Callable[[Path, Path], object],
) -> None:
    _validate_transaction_paths(paths)
    if _path_exists_unfollowed(paths.final) and (_path_exists_unfollowed(paths.backup) or not had_final):
        _remove_owned_directory(paths, "final")
    if _path_exists_unfollowed(paths.backup):
        _replace_transaction_path(paths, "backup", "final", replace_path)
    _cleanup_transaction_artifacts(paths, remove_backup=False)


def publish_directory_transaction(
    paths: TransactionPaths,
    validator: Callable[[Path], None],
    *,
    replace_path: Callable[[Path, Path], object] = os.replace,
    transaction_hook: Callable[[str, str], object] | None = None,
) -> None:
    """Publish a complete stage; ordinary exceptions roll back, BaseException is recovered next run."""
    _validate_transaction_paths(paths)
    validator(paths.stage_dir)
    if _path_exists_unfollowed(paths.backup) or _path_exists_unfollowed(paths.marker):
        raise RuntimeError(f"{paths.name} 事务尚未恢复")
    had_final = _path_exists_unfollowed(paths.final)
    _write_marker(paths, "prepared")
    try:
        if had_final:
            _replace_transaction_path(paths, "final", "backup", replace_path)
            _write_marker(paths, "final-to-backup")
            if transaction_hook:
                transaction_hook(paths.name, "after_final_to_backup")
        _replace_transaction_path(paths, "stage_dir", "final", replace_path)
        _write_marker(paths, "stage-to-final")
        if transaction_hook:
            transaction_hook(paths.name, "after_stage_to_final")
        validator(paths.final)
        _remove_owned_directory(paths, "backup")
        _cleanup_transaction_artifacts(paths, remove_backup=False)
    except Exception:
        _rollback_transaction(paths, had_final=had_final, replace_path=replace_path)
        raise


def archive_originals(
    sources: list[Path],
    archive_root: Path,
    *,
    project_root: Path | None = None,
    copy_file: Callable[[Path, Path], object] = shutil.copy2,
    replace_path: Callable[[Path, Path], object] = os.replace,
    transaction_hook: Callable[[str, str], object] | None = None,
) -> list[dict[str, object]]:
    """Copy all originals to a stage and publish the archive as one directory transaction."""
    project = _absolute(project_root or _absolute(archive_root).parents[1])
    paths = archive_transaction_paths(project, archive_root)
    _validate_transaction_paths(paths)
    source_snapshot = _snapshot_sources(sources)
    recover_directory_transaction(
        paths,
        lambda directory: _validate_archive(directory, source_snapshot),
        replace_path=replace_path,
    )
    paths.stage_root.parent.mkdir(parents=True, exist_ok=True)
    _remove_owned_directory(paths, "stage_root")
    paths.stage_root.mkdir()
    try:
        for source in sources:
            copying = paths.stage_root / f".{source.name}.copying"
            target = paths.stage_root / source.name
            copy_file(source, copying)
            expected_size, expected_hash = source_snapshot[source.name]
            if copying.stat().st_size != expected_size or _sha256(copying) != expected_hash:
                raise ValueError(f"归档暂存副本校验失败: {source.name}")
            os.replace(copying, target)
        if _snapshot_sources(sources) != source_snapshot:
            raise ValueError("归档复制过程中源文件发生变化")
        _validate_archive(paths.stage_dir, source_snapshot)
        publish_directory_transaction(
            paths,
            lambda directory: _validate_archive(directory, source_snapshot),
            replace_path=replace_path,
            transaction_hook=transaction_hook,
        )
    except Exception:
        _remove_owned_directory(paths, "stage_root")
        raise
    if _snapshot_sources(sources) != source_snapshot:
        raise ValueError("归档发布后源文件发生变化")
    return _inventory(sources, paths.final)


def seed_existing_delivery(project_root: Path, staging_root: Path, manifest: list[dict]) -> list[Path]:
    project = _absolute(project_root)
    staging = _absolute(staging_root)
    seeded: list[Path] = []
    for relative in sorted(expected_delivery_paths(manifest), key=str):
        source = project / relative
        if not source.is_file():
            continue
        if source.stat().st_size <= 0:
            raise ValueError(f"现有交付文件为空: {source}")
        target = staging / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        seeded.append(target)
    return seeded


def _run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    completed = subprocess.run(command, cwd=cwd, env=env, text=True)
    if completed.returncode:
        raise RuntimeError(f"命令失败({completed.returncode}): {' '.join(command)}")


def _default_input_loader(project: Path) -> dict:
    if _absolute(project) != PROJECT_ROOT.resolve():
        raise ValueError("临时项目必须注入 input_loader")
    records, taxonomy, manifest, repositories = load_inputs()
    assignment = json.loads((project / ASSIGNMENT_RELATIVE).read_text(encoding="utf-8"))
    return {
        "records": records,
        "taxonomy": taxonomy,
        "manifest": manifest,
        "repositories": repositories,
        "assignments": assignment.get("assignments"),
    }


def _default_document_builder(staging_root: Path, inputs: dict) -> list[Path]:
    return generate_documents(inputs["records"], inputs["taxonomy"], inputs["manifest"], staging_root)


def _default_spreadsheet_builder(staging_root: Path, _inputs: dict) -> list[Path]:
    environment = os.environ.copy()
    environment["SUBCATEGORY_OUTPUT_ROOT"] = str(staging_root)
    _run([str(NODE), str(XLSX_BUILDER)], cwd=PROJECT_ROOT, env=environment)
    return [staging_root / path for path in expected_delivery_paths(_inputs["manifest"]) if path.suffix == ".xlsx"]


def _default_document_verifier(staging_root: Path, inputs: dict) -> None:
    results = verify_selected_documents(
        inputs["records"],
        inputs["manifest"],
        staging_root,
        taxonomy=inputs["taxonomy"],
        assignments=inputs["assignments"],
        repositories=inputs["repositories"],
        expected_total=157,
        source_project_root=PROJECT_ROOT,
    )
    failed = {key: issues for key, issues in results.items() if issues}
    if failed:
        first = sorted(failed)[0]
        raise ValueError(f"暂存 DOCX 结构验证失败 {first}: {failed[first]}")


def _default_spreadsheet_verifier(staging_root: Path, _inputs: dict) -> None:
    environment = os.environ.copy()
    environment["SUBCATEGORY_OUTPUT_ROOT"] = str(staging_root)
    _run([str(NODE), str(XLSX_VERIFIER)], cwd=PROJECT_ROOT, env=environment)


def _validate_inputs(inputs: dict) -> list[dict]:
    manifest = inputs.get("manifest")
    records = inputs.get("records")
    assignments = inputs.get("assignments")
    if not isinstance(manifest, list):
        raise ValueError("manifest 格式错误")
    expected_delivery_paths(manifest)
    if not isinstance(records, list) or not isinstance(assignments, dict):
        raise ValueError("157 项输入格式错误")
    record_ids = [record.get("id") for record in records]
    if len(records) != 157 or len(set(record_ids)) != 157 or set(assignments) != set(record_ids):
        raise ValueError("157 项成员存在遗漏或重复")
    return manifest


def build_complete_delivery(
    project_root: Path = PROJECT_ROOT,
    *,
    archive_root: Path | None = None,
    input_loader: Callable[[Path], dict] = _default_input_loader,
    document_builder: Callable[[Path, dict], list[Path]] = _default_document_builder,
    spreadsheet_builder: Callable[[Path, dict], list[Path]] = _default_spreadsheet_builder,
    document_verifier: Callable[[Path, dict], None] = _default_document_verifier,
    spreadsheet_verifier: Callable[[Path, dict], None] = _default_spreadsheet_verifier,
    copy_file: Callable[[Path, Path], object] = shutil.copy2,
    replace_path: Callable[[Path, Path], object] = os.replace,
    transaction_hook: Callable[[str, str], object] | None = None,
) -> dict[str, object]:
    """Run the real Task 6 orchestration with injectable content builders for integration tests."""
    project = _absolute(project_root)
    inputs = input_loader(project)
    manifest = _validate_inputs(inputs)
    archive_paths = archive_transaction_paths(project, archive_root)
    delivery_paths = delivery_transaction_paths(project)
    # Validate both transaction layouts before discovering, copying, deleting,
    # or moving anything. This prevents one unsafe layout from allowing the
    # other transaction to mutate the project first.
    _validate_transaction_paths(archive_paths)
    _validate_transaction_paths(delivery_paths)
    sources = discover_originals(project / "05_交付物")
    source_before = _snapshot_sources(sources)

    recover_directory_transaction(
        archive_paths,
        lambda directory: _validate_archive(directory, source_before),
        replace_path=replace_path,
    )
    recover_directory_transaction(
        delivery_paths,
        lambda directory: _validate_delivery(directory, manifest),
        replace_path=replace_path,
    )
    archive_inventory = archive_originals(
        sources,
        archive_paths.final,
        project_root=project,
        copy_file=copy_file,
        replace_path=replace_path,
        transaction_hook=transaction_hook,
    )

    delivery_paths.stage_root.parent.mkdir(parents=True, exist_ok=True)
    _remove_owned_directory(delivery_paths, "stage_root")
    delivery_paths.stage_root.mkdir()
    try:
        seed_existing_delivery(project, delivery_paths.stage_root, manifest)
        document_paths = document_builder(delivery_paths.stage_root, inputs)
        spreadsheet_paths = spreadsheet_builder(delivery_paths.stage_root, inputs)
        if len(document_paths) != 66 or len(spreadsheet_paths) != 66:
            raise ValueError(f"生成数量错误: docx={len(document_paths)} xlsx={len(spreadsheet_paths)}")
        _validate_delivery(delivery_paths.stage_dir, manifest)
        document_verifier(delivery_paths.stage_root, inputs)
        spreadsheet_verifier(delivery_paths.stage_root, inputs)
        publish_directory_transaction(
            delivery_paths,
            lambda directory: _validate_delivery(directory, manifest),
            replace_path=replace_path,
            transaction_hook=transaction_hook,
        )
    except Exception:
        _remove_owned_directory(delivery_paths, "stage_root")
        raise

    if _snapshot_sources(sources) != source_before:
        raise ValueError("完整生成过程中原位置文件发生变化")
    published = [project / path for path in sorted(expected_delivery_paths(manifest), key=str)]
    _validate_delivery(delivery_paths.final, manifest)
    return {
        "published": published,
        "archive_inventory": archive_inventory,
        "source_inventory": _inventory(sources),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    result = build_complete_delivery()
    published = result["published"]
    formats = Counter(path.suffix.lower() for path in published)
    print(
        f"published={len(published)} docx={formats['.docx']} xlsx={formats['.xlsx']} "
        f"archived={len(result['archive_inventory'])} source_unchanged=10"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
