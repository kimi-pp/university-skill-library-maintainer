"""Single-authority publication primitives shared by the coordinator and Task 11."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
from typing import Callable

if os.name == "nt":
    import ctypes
    import msvcrt
    from ctypes import wintypes

from .office import (
    OfficeEvidenceBundle,
    OfficeVerificationError,
    clear_office_run_state,
    consume_office_evidence,
)
from .paths import assert_ordinary_path, is_link_or_reparse


class PublishError(RuntimeError):
    """A publish input changed or a safe single-authority commit failed."""


@dataclass(frozen=True)
class PublishFile:
    relative_path: str
    sha256: str


@dataclass(frozen=True)
class PublishPlan:
    staging_root: Path
    production_root: Path
    run_id: str
    staged_ledger: Path
    staged_ledger_sha256: str
    authority_path: Path
    expected_authority_sha256: str
    deliveries_root: Path
    delivery_files: tuple[PublishFile, ...]
    generation_path: Path
    backup_path: Path
    generations_parent_identity: tuple[int, int, int, int]
    archive_parent_identity: tuple[int, int, int, int]
    office_evidence: OfficeEvidenceBundle
    office_evidence_sha256: str


@dataclass(frozen=True)
class PublishReceipt:
    run_id: str
    authority_path: Path
    authority_sha256: str
    backup_path: Path
    backup_sha256: str
    generation_path: Path
    generation_manifest_sha256: str
    office_evidence_sha256: str


class _GenerationPins:
    """Deny-write/delete Windows handles for authority trees and parent paths."""

    _GENERIC_READ = 0x80000000
    _FILE_SHARE_READ = 0x00000001
    _FILE_SHARE_WRITE = 0x00000002
    _OPEN_EXISTING = 3
    _FILE_ATTRIBUTE_NORMAL = 0x00000080
    _FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
    _FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
    _INVALID_HANDLE_VALUE = -1
    _DUPLICATE_SAME_ACCESS = 0x00000002

    def __init__(self) -> None:
        self._files: dict[Path, int] = {}
        self._handles: list[int] = []
        self._identities: dict[Path, tuple[int, int, int, int]] = {}

    def pin(self, path: Path, *, directory: bool) -> None:
        if os.name != "nt":
            raise PublishError("正式发布仅支持 Windows handle pin")
        if is_link_or_reparse(path):
            raise PublishError(f"拒绝固定链接或重解析点：{path}")
        try:
            assert_ordinary_path(path, require_directory=directory)
        except ValueError as exc:
            raise PublishError(f"无法固定非普通 authority 路径：{path}") from exc
        flags = self._FILE_FLAG_OPEN_REPARSE_POINT
        flags |= self._FILE_FLAG_BACKUP_SEMANTICS if directory else self._FILE_ATTRIBUTE_NORMAL
        create_file = ctypes.windll.kernel32.CreateFileW
        create_file.argtypes = (
            wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
            wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
        )
        create_file.restype = wintypes.HANDLE
        handle = create_file(
            str(path), self._GENERIC_READ,
            self._FILE_SHARE_READ | (self._FILE_SHARE_WRITE if directory else 0), None,
            self._OPEN_EXISTING, flags, None,
        )
        if handle == wintypes.HANDLE(self._INVALID_HANDLE_VALUE).value:
            raise PublishError(f"无法固定 authority 路径：{path}")
        value = int(handle)
        self._handles.append(value)
        self._identities[path] = _directory_identity(path) if directory else _stat_identity(path)
        if not directory:
            self._files[path] = value

    def assert_path(self, path: Path) -> None:
        expected = self._identities[path]
        current = _directory_identity(path) if expected[2:] == (0, 0) else _stat_identity(path)
        if is_link_or_reparse(path) or current != expected:
            raise PublishError(f"已固定 authority 路径身份变化：{path}")

    def sha256(self, path: Path) -> str:
        handle = self._files[path]
        set_pointer = ctypes.windll.kernel32.SetFilePointerEx
        set_pointer.argtypes = (wintypes.HANDLE, ctypes.c_longlong, ctypes.POINTER(ctypes.c_longlong), wintypes.DWORD)
        set_pointer.restype = wintypes.BOOL
        if not set_pointer(wintypes.HANDLE(handle), 0, None, 0):
            raise PublishError(f"无法复位已固定 authority 文件：{path}")
        digest = sha256()
        buffer = ctypes.create_string_buffer(64 * 1024)
        read = wintypes.DWORD()
        read_file = ctypes.windll.kernel32.ReadFile
        read_file.argtypes = (
            wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID,
        )
        read_file.restype = wintypes.BOOL
        while True:
            if not read_file(wintypes.HANDLE(handle), buffer, len(buffer), ctypes.byref(read), None):
                raise PublishError(f"无法读取已固定 authority 文件：{path}")
            if not read.value:
                return digest.hexdigest()
            digest.update(buffer.raw[:read.value])

    def identity(self, path: Path) -> tuple[int, int, int, int]:
        duplicate_handle = ctypes.windll.kernel32.DuplicateHandle
        duplicate_handle.argtypes = (
            wintypes.HANDLE, wintypes.HANDLE, wintypes.HANDLE,
            ctypes.POINTER(wintypes.HANDLE), wintypes.DWORD, wintypes.BOOL, wintypes.DWORD,
        )
        duplicate_handle.restype = wintypes.BOOL
        process = ctypes.windll.kernel32.GetCurrentProcess()
        duplicate = wintypes.HANDLE()
        if not duplicate_handle(
            process, wintypes.HANDLE(self._files[path]), process,
            ctypes.byref(duplicate), 0, False, self._DUPLICATE_SAME_ACCESS,
        ):
            raise PublishError(f"无法复验已固定 authority 文件身份：{path}")
        descriptor = msvcrt.open_osfhandle(int(duplicate.value), os.O_RDONLY)
        try:
            result = os.fstat(descriptor)
            return (getattr(result, "st_dev", 0), getattr(result, "st_ino", 0), result.st_size, result.st_mtime_ns)
        finally:
            os.close(descriptor)

    def release(self) -> None:
        if os.name == "nt":
            close_handle = ctypes.windll.kernel32.CloseHandle
            close_handle.argtypes = (wintypes.HANDLE,)
            close_handle.restype = wintypes.BOOL
            for handle in reversed(self._handles):
                close_handle(wintypes.HANDLE(handle))
        self._handles.clear()
        self._files.clear()
        self._identities.clear()


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stat_identity(path: Path) -> tuple[int, int, int, int]:
    result = path.stat()
    return (getattr(result, "st_dev", 0), getattr(result, "st_ino", 0), result.st_size, result.st_mtime_ns)


def _directory_identity(path: Path) -> tuple[int, int, int, int]:
    result = path.stat()
    return (getattr(result, "st_dev", 0), getattr(result, "st_ino", 0), 0, 0)


def build_publish_plan(
    staging: str | Path,
    production: str | Path,
    *,
    office_evidence: OfficeEvidenceBundle,
) -> PublishPlan:
    staging_root = Path(staging).absolute()
    production_root = Path(production).absolute()
    _require_ordinary_directory(staging_root, label="暂存根目录")
    _require_ordinary_directory(production_root, label="生产根目录")
    run_id = staging_root.name
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", run_id):
        raise PublishError("run ID 不能安全地用作发布代次目录名。")
    staged_ledger = staging_root / "Skills主台账.xlsx"
    authority = production_root / "ledger" / "Skills主台账.xlsx"
    deliveries = staging_root / "deliveries"
    _require_ordinary_file(staged_ledger, label="暂存主台账")
    _require_ordinary_file(authority, label="生产主台账")
    _require_ordinary_directory(deliveries, label="暂存交付目录")
    files: list[PublishFile] = []
    delivery_paths: list[Path] = []
    for path in sorted(deliveries.rglob("*"), key=lambda item: item.relative_to(deliveries).as_posix().casefold()):
        if is_link_or_reparse(path):
            raise PublishError(f"暂存交付目录包含链接或重解析点：{path}")
        if path.is_file():
            files.append(PublishFile(path.relative_to(deliveries).as_posix(), _sha256(path)))
            delivery_paths.append(path)
    if not files:
        raise PublishError("暂存交付目录没有可发布文件。")
    generations = production_root / "output" / "generations"
    archive = production_root / "ledger" / "archive"
    _require_ordinary_directory(generations, label="发布代次目录")
    _require_ordinary_directory(archive, label="主台账备份目录")
    generation = generations / run_id
    if generation.exists() or generation.is_symlink():
        raise PublishError("发布代次已存在，不允许覆盖。")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = archive / f"Skills主台账_{timestamp}.xlsx"
    suffix = 1
    while backup.exists() or backup.is_symlink():
        backup = archive / f"Skills主台账_{timestamp}_{suffix}.xlsx"
        suffix += 1
    if not isinstance(office_evidence, OfficeEvidenceBundle):
        raise PublishError("发布计划必须绑定结构化 Office 证据。")
    if office_evidence.run_id != run_id:
        raise PublishError("Office 发布证据未绑定当前发布运行标识。")
    try:
        office_evidence.assert_publication_roles(
            staged_ledger, (staged_ledger, *delivery_paths),
        )
    except OfficeVerificationError as exc:
        raise PublishError(f"Office 发布证据无效：{exc}") from exc
    return PublishPlan(
        staging_root=staging_root, production_root=production_root, run_id=run_id,
        staged_ledger=staged_ledger, staged_ledger_sha256=_sha256(staged_ledger),
        authority_path=authority, expected_authority_sha256=_sha256(authority),
        deliveries_root=deliveries, delivery_files=tuple(files), generation_path=generation,
        backup_path=backup, generations_parent_identity=_directory_identity(generations),
        archive_parent_identity=_directory_identity(archive), office_evidence=office_evidence,
        office_evidence_sha256=office_evidence.sha256,
    )


def publish_atomically(
    plan: PublishPlan,
    *,
    fail_at: str | None = None,
    before_backup_replace: Callable[[], None] | None = None,
    before_authority_replace: Callable[[], None] | None = None,
) -> PublishReceipt:
    """Install one immutable generation and linearize solely through the ledger."""
    try:
        _validate_plan_shape(plan)
    except BaseException:
        clear_office_run_state(plan.run_id)
        raise
    pending_generation = plan.generation_path.parent / f".{plan.run_id}.pending"
    authority_temp = plan.authority_path.parent / f".{plan.authority_path.name}.{plan.run_id}.pending"
    backup_temp = plan.backup_path.parent / f".{plan.backup_path.name}.pending"
    parent_pins = _GenerationPins()
    generation_installed = False
    committed = False
    manifest_hash = ""
    try:
        _verify_plan_inputs(plan)
        parent_pins.pin(plan.generation_path.parent, directory=True)
        parent_pins.pin(plan.backup_path.parent, directory=True)
        _verify_pinned_parents(plan, parent_pins)

        _copy_fsynced(plan.authority_path, backup_temp)
        if _sha256(backup_temp) != plan.expected_authority_sha256:
            raise PublishError("生产主台账备份哈希不一致。")
        if before_backup_replace:
            before_backup_replace()
        _verify_pinned_parents(plan, parent_pins)
        _move_no_replace(backup_temp, plan.backup_path, label="主台账备份")

        pending_generation.mkdir(mode=0o700)
        for item in plan.delivery_files:
            _inject(fail_at, f"delivery:{item.relative_path}")
            source = plan.deliveries_root / Path(item.relative_path)
            destination = pending_generation / Path(item.relative_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            _copy_fsynced(source, destination)
            if _sha256(destination) != item.sha256:
                raise PublishError(f"发布代次文件哈希不一致：{item.relative_path}")
        manifest = pending_generation / "generation-manifest.json"
        manifest_payload = {
            "run_id": plan.run_id, "staged_ledger_sha256": plan.staged_ledger_sha256,
            "office_evidence_sha256": plan.office_evidence_sha256,
            "files": [{"path": item.relative_path, "sha256": item.sha256} for item in plan.delivery_files],
        }
        manifest.write_text(json.dumps(manifest_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")), encoding="utf-8")
        _fsync_file(manifest)
        manifest_hash = _sha256(manifest)
        _inject(fail_at, "generation-replace")
        _verify_pinned_parents(plan, parent_pins)
        _move_no_replace(pending_generation, plan.generation_path, label="发布代次")
        generation_installed = True

        _inject(fail_at, "authority-temp")

        def final_boundary() -> None:
            _verify_plan_inputs(plan)
            _verify_pinned_parents(plan, parent_pins)
            if before_authority_replace:
                before_authority_replace()
            _verify_plan_inputs(plan)
            _verify_pinned_parents(plan, parent_pins)
            _inject(fail_at, "authority-replace")

        receipt = commit_prepared_generation(
            production_root=plan.production_root,
            run_id=plan.run_id,
            staged_ledger=plan.staged_ledger,
            expected_authority_sha256=plan.expected_authority_sha256,
            generation_path=plan.generation_path,
            generation_manifest_sha256=manifest_hash,
            office_evidence=plan.office_evidence,
            office_paths=(
                plan.staged_ledger,
                *(plan.deliveries_root / Path(item.relative_path) for item in plan.delivery_files),
            ),
            backup_path=plan.backup_path,
            before_authority_replace=final_boundary,
        )
        committed = True
        return receipt
    except BaseException as exc:
        if generation_installed and _authority_committed(plan, manifest_hash):
            committed = True
        if isinstance(exc, Exception) and not isinstance(exc, PublishError):
            raise PublishError(f"发布失败：{exc}") from exc
        raise
    finally:
        try:
            parent_pins.release()
        except BaseException:
            pass
        if not committed:
            _remove_file_if_owned(authority_temp, plan.authority_path.parent)
            _remove_file_if_owned(backup_temp, plan.backup_path.parent)
            _remove_tree_if_owned(pending_generation, plan.generation_path.parent)
            if generation_installed:
                _remove_tree_if_owned(plan.generation_path, plan.generation_path.parent)
        clear_office_run_state(plan.run_id)


def commit_prepared_generation(
    *,
    production_root: str | Path,
    run_id: str,
    staged_ledger: str | Path,
    expected_authority_sha256: str,
    generation_path: str | Path,
    generation_manifest_sha256: str,
    office_evidence: OfficeEvidenceBundle,
    office_paths: tuple[Path, ...],
    backup_path: Path | None = None,
    before_authority_replace: Callable[[], None] | None = None,
) -> PublishReceipt:
    """Commit a Task9-prepared generation through the same pinned ledger boundary.

    Generation ownership and rollback stay with ``RunCoordinator``.  This
    function owns the archive backup, parent/tree pins and the sole visible
    authority replacement, and it never deletes a committed generation.
    """
    production = Path(production_root).absolute()
    staged = Path(staged_ledger).absolute()
    generation = Path(generation_path).absolute()
    authority = production / "ledger" / "Skills主台账.xlsx"
    generations = production / "output" / "generations"
    archive = production / "ledger" / "archive"
    ledger_parent = production / "ledger"
    output_parent = production / "output"
    try:
        _require_ordinary_directory(production, label="生产根目录")
        _require_ordinary_directory(ledger_parent, label="生产 ledger 目录")
        _require_ordinary_directory(output_parent, label="生产 output 目录")
        _require_ordinary_directory(generations, label="发布代次目录")
    except BaseException:
        clear_office_run_state(run_id)
        raise
    container_pins = _GenerationPins()
    container_paths = (production, ledger_parent, output_parent, generations)
    try:
        container_identities = tuple(_directory_identity(path) for path in container_paths)
        for path in container_paths:
            container_pins.pin(path, directory=True)
        _assert_container_paths(container_paths, container_identities, container_pins)
        if not archive.exists():
            archive.mkdir(mode=0o700)
        _require_ordinary_directory(archive, label="主台账备份目录")
        _assert_container_paths(container_paths, container_identities, container_pins)
    except BaseException:
        container_pins.release()
        clear_office_run_state(run_id)
        raise
    try:
        staged_hash, manifest, backup, backup_exists = _prepare_commit_arguments(
            staged=staged, authority=authority, generation=generation,
            generations=generations, archive=archive, run_id=run_id,
            expected_authority_sha256=expected_authority_sha256,
            generation_manifest_sha256=generation_manifest_sha256,
            office_evidence=office_evidence, office_paths=office_paths,
            backup_path=backup_path,
        )
    except BaseException:
        container_pins.release()
        clear_office_run_state(run_id)
        raise
    backup_temp = archive / f".{backup.name}.{run_id}.pending"
    authority_temp = authority.parent / f".{authority.name}.{run_id}.commit"
    parent_pins = _GenerationPins()
    generation_pins: _GenerationPins | None = None
    try:
        parent_identities = (_directory_identity(generations), _directory_identity(archive))
        parent_pins.pin(generations, directory=True)
        parent_pins.pin(archive, directory=True)
        _assert_prepared_parents(production, generations, archive, parent_identities, parent_pins)
        if backup_exists:
            _require_ordinary_file(backup, label="既有 Runner 主台账备份")
            if _sha256(backup) != expected_authority_sha256:
                raise PublishError("既有 Runner 主台账备份哈希不一致。")
        else:
            _copy_fsynced(authority, backup_temp)
            if _sha256(backup_temp) != expected_authority_sha256:
                raise PublishError("Runner 主台账备份哈希不一致。")
            _move_no_replace(backup_temp, backup, label="Runner 主台账备份")
        generation_pins = _pin_tree(generation)

        _copy_fsynced(staged, authority_temp)
        if _sha256(authority_temp) != staged_hash:
            raise PublishError("Runner 主台账提交副本哈希不一致。")
        _verify_prepared_commit_inputs(
            authority=authority, expected_authority_sha256=expected_authority_sha256,
            staged=staged, staged_hash=staged_hash, manifest=manifest,
            generation_manifest_sha256=generation_manifest_sha256,
            office_evidence=office_evidence, office_paths=office_paths,
            production=production, generations=generations, archive=archive,
            parent_identities=parent_identities, parent_pins=parent_pins,
            generation=generation, generation_pins=generation_pins,
            container_paths=container_paths, container_identities=container_identities,
            container_pins=container_pins,
        )
        if before_authority_replace:
            before_authority_replace()
        _verify_prepared_commit_inputs(
            authority=authority, expected_authority_sha256=expected_authority_sha256,
            staged=staged, staged_hash=staged_hash, manifest=manifest,
            generation_manifest_sha256=generation_manifest_sha256,
            office_evidence=office_evidence, office_paths=office_paths,
            production=production, generations=generations, archive=archive,
            parent_identities=parent_identities, parent_pins=parent_pins,
            generation=generation, generation_pins=generation_pins,
            container_paths=container_paths, container_identities=container_identities,
            container_pins=container_pins,
        )
        try:
            consume_office_evidence(office_evidence, run_id=run_id)
        except OfficeVerificationError as exc:
            raise PublishError(f"Runner Office verifier capability 无效或已消费：{exc}") from exc
        os.replace(authority_temp, authority)
        return PublishReceipt(
            run_id=run_id, authority_path=authority, authority_sha256=staged_hash,
            backup_path=backup, backup_sha256=expected_authority_sha256,
            generation_path=generation, generation_manifest_sha256=generation_manifest_sha256,
            office_evidence_sha256=office_evidence.sha256,
        )
    except BaseException as exc:
        if isinstance(exc, Exception) and not isinstance(exc, PublishError):
            raise PublishError(f"Runner 发布失败：{exc}") from exc
        raise
    finally:
        if generation_pins is not None:
            try:
                generation_pins.release()
            except BaseException:
                pass
        try:
            parent_pins.release()
        except BaseException:
            pass
        try:
            container_pins.release()
        except BaseException:
            pass
        _remove_file_if_owned(authority_temp, authority.parent)
        _remove_file_if_owned(backup_temp, archive)
        clear_office_run_state(run_id)


def _assert_prepared_parents(
    production: Path,
    generations: Path,
    archive: Path,
    identities: tuple[tuple[int, int, int, int], tuple[int, int, int, int]],
    pins: _GenerationPins,
) -> None:
    expected_generations = production / "output" / "generations"
    expected_archive = production / "ledger" / "archive"
    for path, expected, identity in (
        (generations, expected_generations, identities[0]),
        (archive, expected_archive, identities[1]),
    ):
        if path != expected or is_link_or_reparse(path):
            raise PublishError("Runner 发布父目录越界、被替换或成为重解析点。")
        _require_ordinary_directory(path, label="Runner 发布父目录")
        if _directory_identity(path) != identity:
            raise PublishError("Runner 发布父目录身份变化。")
        pins.assert_path(path)


def _prepare_commit_arguments(
    *,
    staged: Path,
    authority: Path,
    generation: Path,
    generations: Path,
    archive: Path,
    run_id: str,
    expected_authority_sha256: str,
    generation_manifest_sha256: str,
    office_evidence: OfficeEvidenceBundle,
    office_paths: tuple[Path, ...],
    backup_path: Path | None,
) -> tuple[str, Path, Path, bool]:
    _require_ordinary_file(staged, label="暂存主台账")
    _require_ordinary_file(authority, label="生产主台账")
    try:
        generation.relative_to(generations)
    except ValueError as exc:
        raise PublishError("发布代次越出 production/output/generations。") from exc
    if generation.parent != generations or generation.name != run_id:
        raise PublishError("发布代次路径未绑定当前运行标识。")
    if _sha256(authority) != expected_authority_sha256:
        raise PublishError("生产主台账在提交前发生变化。")
    if not isinstance(office_evidence, OfficeEvidenceBundle):
        raise PublishError("Runner 必须提供结构化 Office 证据。")
    try:
        office_evidence.assert_publication_roles(staged, office_paths)
    except OfficeVerificationError as exc:
        raise PublishError(f"Runner Office 证据无效：{exc}") from exc
    _assert_generation_office_binding(staged, generation, office_evidence)
    staged_hash = _sha256(staged)
    manifest = generation / "generation-manifest.json"
    if _sha256(manifest) != generation_manifest_sha256:
        raise PublishError("Runner generation manifest 哈希不一致。")
    if backup_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = archive / f"Skills主台账_{timestamp}.xlsx"
        suffix = 1
        while backup.exists() or backup.is_symlink():
            backup = archive / f"Skills主台账_{timestamp}_{suffix}.xlsx"
            suffix += 1
        return staged_hash, manifest, backup, False
    backup = Path(backup_path).absolute()
    if backup.parent != archive:
        raise PublishError("既有 Runner 备份路径越出 ledger/archive。")
    return staged_hash, manifest, backup, True


def _assert_container_paths(
    paths: tuple[Path, ...],
    identities: tuple[tuple[int, int, int, int], ...],
    pins: _GenerationPins,
) -> None:
    for path, identity in zip(paths, identities):
        _require_ordinary_directory(path, label="发布容器目录")
        if _directory_identity(path) != identity:
            raise PublishError("发布容器目录身份变化。")
        pins.assert_path(path)


def _pin_tree(root: Path) -> _GenerationPins:
    _require_ordinary_directory(root, label="Runner generation")
    pins = _GenerationPins()
    try:
        directories = [root, *(path for path in root.rglob("*") if path.is_dir())]
        for directory in sorted(directories, key=lambda path: (len(path.parts), str(path).casefold())):
            pins.pin(directory, directory=True)
        for path in sorted((path for path in root.rglob("*") if path.is_file()), key=lambda path: str(path).casefold()):
            pins.pin(path, directory=False)
        return pins
    except BaseException:
        pins.release()
        raise


def _verify_pinned_tree(root: Path, pins: _GenerationPins) -> None:
    _require_ordinary_directory(root, label="Runner generation")
    for path in sorted(root.rglob("*"), key=lambda item: str(item).casefold()):
        pins.assert_path(path)
        if path.is_file() and (pins.sha256(path) != _sha256(path) or pins.identity(path) != _stat_identity(path)):
            raise PublishError(f"Runner generation 在提交边界变化：{path}")


def _verify_prepared_commit_inputs(
    *,
    authority: Path,
    expected_authority_sha256: str,
    staged: Path,
    staged_hash: str,
    manifest: Path,
    generation_manifest_sha256: str,
    office_evidence: OfficeEvidenceBundle,
    office_paths: tuple[Path, ...],
    production: Path,
    generations: Path,
    archive: Path,
    parent_identities: tuple[tuple[int, int, int, int], tuple[int, int, int, int]],
    parent_pins: _GenerationPins,
    generation: Path,
    generation_pins: _GenerationPins,
    container_paths: tuple[Path, ...],
    container_identities: tuple[tuple[int, int, int, int], ...],
    container_pins: _GenerationPins,
) -> None:
    if _sha256(authority) != expected_authority_sha256 or _sha256(staged) != staged_hash:
        raise PublishError("Runner ledger authority 在提交边界变化。")
    if _sha256(manifest) != generation_manifest_sha256:
        raise PublishError("Runner manifest 在提交边界变化。")
    try:
        office_evidence.assert_publication_roles(staged, office_paths)
    except OfficeVerificationError as exc:
        raise PublishError(f"Runner Office 证据在提交边界失效：{exc}") from exc
    _assert_generation_office_binding(staged, generation, office_evidence)
    _assert_container_paths(container_paths, container_identities, container_pins)
    _assert_prepared_parents(production, generations, archive, parent_identities, parent_pins)
    _verify_pinned_tree(generation, generation_pins)


def _assert_generation_office_binding(
    staged_ledger: Path,
    generation: Path,
    evidence: OfficeEvidenceBundle,
) -> None:
    deliveries = staged_ledger.parent / "deliveries"
    evidence_relative: set[Path] = set()
    ledger_checks = 0
    for check in evidence.checks:
        source = check.source_path.absolute()
        if source == staged_ledger:
            ledger_checks += 1
            continue
        try:
            relative = source.relative_to(deliveries)
        except ValueError as exc:
            raise PublishError("Office 交付证据未绑定 staging/deliveries 内文件。") from exc
        published = generation / relative
        if not published.is_file() or is_link_or_reparse(published):
            raise PublishError(f"generation 缺少 Office 证据对应文件：{relative}")
        if _sha256(published) != check.source_sha256:
            raise PublishError(f"generation Office 文件与批准证据哈希不一致：{relative}")
        evidence_relative.add(relative)
    if ledger_checks != 1:
        raise PublishError("Office 证据必须精确包含一份暂存主台账。")
    generation_relative = {
        path.relative_to(generation)
        for path in generation.rglob("*")
        if path.is_file() and path.suffix.casefold() in {".docx", ".xlsx"}
    }
    if generation_relative != evidence_relative:
        missing = sorted(path.as_posix() for path in generation_relative - evidence_relative)
        extra = sorted(path.as_posix() for path in evidence_relative - generation_relative)
        raise PublishError(f"generation Office 文件集合与 verifier 证据不精确相等；无证据={missing}；无文件={extra}")


def _verify_plan_inputs(plan: PublishPlan) -> None:
    _require_ordinary_file(plan.staged_ledger, label="暂存主台账")
    _require_ordinary_file(plan.authority_path, label="生产主台账")
    _fsync_file(plan.staged_ledger)
    if _sha256(plan.staged_ledger) != plan.staged_ledger_sha256:
        raise PublishError("暂存主台账在发布计划形成后发生变化。")
    if _sha256(plan.authority_path) != plan.expected_authority_sha256:
        raise PublishError("生产主台账在发布计划形成后发生变化。")
    for item in plan.delivery_files:
        _validate_relative_path(item.relative_path)
        source = plan.deliveries_root / Path(item.relative_path)
        _require_ordinary_file(source, label=f"暂存交付文件 {item.relative_path}")
        _fsync_file(source)
        if _sha256(source) != item.sha256:
            raise PublishError(f"暂存交付文件在发布计划形成后发生变化：{item.relative_path}")
    try:
        plan.office_evidence.assert_publication_roles(
            plan.staged_ledger,
            (plan.staged_ledger, *(plan.deliveries_root / Path(item.relative_path) for item in plan.delivery_files)),
        )
    except OfficeVerificationError as exc:
        raise PublishError(f"Office 发布证据在提交边界无效：{exc}") from exc
    if plan.office_evidence.sha256 != plan.office_evidence_sha256:
        raise PublishError("Office 发布证据摘要不一致。")


def _validate_plan_shape(plan: PublishPlan) -> None:
    expected_staged = plan.staging_root / "Skills主台账.xlsx"
    expected_authority = plan.production_root / "ledger" / "Skills主台账.xlsx"
    expected_deliveries = plan.staging_root / "deliveries"
    expected_generation = plan.production_root / "output" / "generations" / plan.run_id
    if plan.staged_ledger != expected_staged or plan.authority_path != expected_authority:
        raise PublishError("发布计划的主台账权威路径不符合项目结构。")
    if plan.deliveries_root != expected_deliveries or plan.generation_path != expected_generation:
        raise PublishError("发布计划的版本化交付路径不符合项目结构。")
    if plan.backup_path.parent != plan.production_root / "ledger" / "archive":
        raise PublishError("发布计划的主台账备份路径不符合项目结构。")
    if not re.fullmatch(r"Skills主台账_\d{8}_\d{6}(?:_\d+)?\.xlsx", plan.backup_path.name):
        raise PublishError("发布计划的主台账备份文件名不符合约定。")
    if not plan.delivery_files:
        raise PublishError("发布计划没有交付文件。")
    for item in plan.delivery_files:
        _validate_relative_path(item.relative_path)


def _verify_pinned_parents(plan: PublishPlan, pins: _GenerationPins) -> None:
    pairs = (
        (plan.generation_path.parent, plan.generations_parent_identity, plan.production_root / "output" / "generations"),
        (plan.backup_path.parent, plan.archive_parent_identity, plan.production_root / "ledger" / "archive"),
    )
    for path, identity, expected in pairs:
        if path != expected or is_link_or_reparse(path):
            raise PublishError("发布父目录越界、被替换或成为重解析点。")
        _require_ordinary_directory(path, label="发布父目录")
        if _directory_identity(path) != identity:
            raise PublishError("发布父目录身份在计划形成后变化。")
        pins.assert_path(path)


def _authority_committed(plan: PublishPlan, manifest_hash: str) -> bool:
    try:
        if _sha256(plan.authority_path) != plan.staged_ledger_sha256:
            return False
        _verify_generation(plan, manifest_hash)
        return True
    except BaseException:
        return False


def _verify_generation(plan: PublishPlan, manifest_hash: str) -> None:
    _require_ordinary_directory(plan.generation_path, label="已安装发布代次")
    for item in plan.delivery_files:
        path = plan.generation_path / Path(item.relative_path)
        _require_ordinary_file(path, label=f"发布代次文件 {item.relative_path}")
        if _sha256(path) != item.sha256:
            raise PublishError(f"发布代次在权威提交前发生变化：{item.relative_path}")
    manifest = plan.generation_path / "generation-manifest.json"
    _require_ordinary_file(manifest, label="发布代次清单")
    if _sha256(manifest) != manifest_hash:
        raise PublishError("发布代次清单在权威提交前发生变化。")


def _move_no_replace(source: Path, destination: Path, *, label: str) -> None:
    if destination.exists() or destination.is_symlink():
        raise PublishError(f"{label}已存在，拒绝覆盖：{destination}")
    if os.name != "nt":
        raise PublishError("正式发布 no-replace 提交仅支持 Windows。")
    move = ctypes.windll.kernel32.MoveFileExW
    move.argtypes = (wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD)
    move.restype = wintypes.BOOL
    if not move(str(source), str(destination), 0x00000008):
        error = ctypes.get_last_error()
        raise PublishError(f"{label} no-replace 提交失败（Windows error={error}）。")


def _copy_fsynced(source: Path, destination: Path) -> None:
    if destination.exists() or destination.is_symlink():
        raise PublishError(f"拒绝覆盖既有暂存提交文件：{destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    _fsync_file(destination)


def _fsync_file(path: Path) -> None:
    with path.open("r+b") as stream:
        stream.flush()
        os.fsync(stream.fileno())


def _require_ordinary_file(path: Path, *, label: str) -> None:
    if not path.is_file() or is_link_or_reparse(path):
        raise PublishError(f"{label}必须是普通文件：{path}")
    try:
        assert_ordinary_path(path)
    except ValueError as exc:
        raise PublishError(f"{label}路径不安全：{path}") from exc


def _require_ordinary_directory(path: Path, *, label: str) -> None:
    if not path.is_dir() or is_link_or_reparse(path):
        raise PublishError(f"{label}必须是普通目录：{path}")
    try:
        assert_ordinary_path(path, require_directory=True)
    except ValueError as exc:
        raise PublishError(f"{label}路径不安全：{path}") from exc


def _validate_relative_path(relative: str) -> None:
    if not relative or "\\" in relative or relative.startswith("/"):
        raise PublishError(f"交付文件必须使用安全相对路径：{relative}")
    if any(part in {"", ".", ".."} for part in relative.split("/")):
        raise PublishError(f"交付文件必须使用安全相对路径：{relative}")


def _inject(configured: str | None, point: str) -> None:
    if configured == point:
        raise PublishError(f"注入失败：{point}")


def _remove_file_if_owned(path: Path, root: Path) -> None:
    try:
        path.relative_to(root)
    except ValueError:
        return
    if path.is_file() and not is_link_or_reparse(path):
        path.unlink()


def _remove_tree_if_owned(path: Path, root: Path) -> None:
    try:
        path.relative_to(root)
    except ValueError:
        return
    if path.is_dir() and not is_link_or_reparse(path):
        for item in path.rglob("*"):
            if is_link_or_reparse(item):
                return
        shutil.rmtree(path)
