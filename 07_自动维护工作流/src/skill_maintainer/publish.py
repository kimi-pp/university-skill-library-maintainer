"""Versioned delivery publication with the Excel ledger as sole authority."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil

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


@dataclass(frozen=True)
class PublishReceipt:
    run_id: str
    authority_path: Path
    authority_sha256: str
    backup_path: Path
    backup_sha256: str
    generation_path: Path
    generation_manifest_sha256: str


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def build_publish_plan(staging: str | Path, production: str | Path) -> PublishPlan:
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
    for path in sorted(deliveries.rglob("*"), key=lambda item: item.relative_to(deliveries).as_posix().casefold()):
        if is_link_or_reparse(path):
            raise PublishError(f"暂存交付目录包含链接或重解析点：{path}")
        if path.is_file():
            files.append(PublishFile(path.relative_to(deliveries).as_posix(), _sha256(path)))
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
    return PublishPlan(
        staging_root=staging_root,
        production_root=production_root,
        run_id=run_id,
        staged_ledger=staged_ledger,
        staged_ledger_sha256=_sha256(staged_ledger),
        authority_path=authority,
        expected_authority_sha256=_sha256(authority),
        deliveries_root=deliveries,
        delivery_files=tuple(files),
        generation_path=generation,
        backup_path=backup,
    )


def publish_atomically(plan: PublishPlan, *, fail_at: str | None = None) -> PublishReceipt:
    """Publish a private generation, then replace the ledger authority exactly once."""
    _validate_plan_shape(plan)
    pending_generation = plan.generation_path.parent / f".{plan.run_id}.pending"
    authority_temp = plan.authority_path.parent / f".{plan.authority_path.name}.{plan.run_id}.pending"
    backup_temp = plan.backup_path.parent / f".{plan.backup_path.name}.pending"
    generation_installed = False
    committed = False
    try:
        _verify_plan_inputs(plan)
        _copy_fsynced(plan.authority_path, backup_temp)
        if _sha256(backup_temp) != plan.expected_authority_sha256:
            raise PublishError("生产主台账备份哈希不一致。")
        os.replace(backup_temp, plan.backup_path)

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
            "run_id": plan.run_id,
            "staged_ledger_sha256": plan.staged_ledger_sha256,
            "files": [{"path": item.relative_path, "sha256": item.sha256} for item in plan.delivery_files],
        }
        manifest.write_text(json.dumps(manifest_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")), encoding="utf-8")
        _fsync_file(manifest)
        manifest_hash = _sha256(manifest)
        _inject(fail_at, "generation-replace")
        os.replace(pending_generation, plan.generation_path)
        generation_installed = True

        _inject(fail_at, "authority-temp")
        _copy_fsynced(plan.staged_ledger, authority_temp)
        if _sha256(authority_temp) != plan.staged_ledger_sha256:
            raise PublishError("主台账提交副本哈希不一致。")
        # These are the final checks immediately before the sole visible authority replace.
        _verify_plan_inputs(plan)
        _verify_generation(plan, manifest_hash)
        _inject(fail_at, "authority-replace")
        os.replace(authority_temp, plan.authority_path)
        committed = True
        # Nothing fallible follows the authority linearization point.
        return PublishReceipt(
            run_id=plan.run_id,
            authority_path=plan.authority_path,
            authority_sha256=plan.staged_ledger_sha256,
            backup_path=plan.backup_path,
            backup_sha256=plan.expected_authority_sha256,
            generation_path=plan.generation_path,
            generation_manifest_sha256=manifest_hash,
        )
    except PublishError:
        raise
    except Exception as exc:
        raise PublishError(f"发布失败：{exc}") from exc
    finally:
        if not committed:
            _remove_file_if_owned(authority_temp, plan.authority_path.parent)
            _remove_file_if_owned(backup_temp, plan.backup_path.parent)
            _remove_tree_if_owned(pending_generation, plan.generation_path.parent)
            if generation_installed:
                _remove_tree_if_owned(plan.generation_path, plan.generation_path.parent)


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
        try:
            source.relative_to(plan.deliveries_root)
        except ValueError as exc:
            raise PublishError("暂存交付路径越出根目录。") from exc
        _fsync_file(source)
        if _sha256(source) != item.sha256:
            raise PublishError(f"暂存交付文件在发布计划形成后发生变化：{item.relative_path}")


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


def _validate_relative_path(relative: str) -> None:
    if not relative or "\\" in relative or relative.startswith("/"):
        raise PublishError(f"交付文件必须使用安全相对路径：{relative}")
    parts = relative.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise PublishError(f"交付文件必须使用安全相对路径：{relative}")


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
