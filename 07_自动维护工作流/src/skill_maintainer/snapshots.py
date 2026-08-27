"""固定版本候选的只读快照构建；绝不导入、执行或安装候选内容。"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import os
from pathlib import Path, PurePosixPath
from stat import S_ISLNK, S_ISREG
import tarfile
from typing import Iterable
import zipfile


@dataclass(frozen=True)
class SnapshotLimits:
    max_files: int = 10_000
    max_total_bytes: int = 128 * 1024 * 1024
    max_file_bytes: int = 32 * 1024 * 1024

    def __post_init__(self) -> None:
        if min(self.max_files, self.max_total_bytes, self.max_file_bytes) <= 0:
            raise ValueError("快照边界必须为正数")


@dataclass(frozen=True)
class SnapshotCandidate:
    candidate_id: str
    fixed_version: str
    source_path: Path
    source_evidence_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class SnapshotFile:
    path: str
    size: int
    sha256: str | None


@dataclass(frozen=True)
class SnapshotManifest:
    candidate_id: str
    fixed_version: str
    destination: Path
    source_evidence_paths: tuple[str, ...]
    evidence_paths: tuple[str, ...]
    files: tuple[SnapshotFile, ...]
    total_bytes: int


_HASHABLE_SUFFIXES = frozenset({
    ".md", ".txt", ".rst", ".adoc", ".py", ".pyi", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".sh", ".ps1", ".bat", ".cmd", ".rb", ".go", ".rs", ".java", ".c", ".h", ".cpp", ".hpp",
    ".cs", ".php", ".swift", ".kt", ".kts", ".lua", ".r", ".sql", ".json", ".toml", ".yaml", ".yml",
    ".ini", ".cfg", ".conf", ".xml", ".properties", ".env", ".dockerfile",
})
_HASHABLE_NAMES = frozenset({"license", "copying", "notice", "makefile", "dockerfile", "skill"})


def build_snapshot(
    candidate: SnapshotCandidate,
    destination: str | Path,
    limits: SnapshotLimits | None = None,
) -> SnapshotManifest:
    """复制一个固定版本的本地证据到安全目录，并仅哈希可审阅的文本内容。"""
    if not isinstance(candidate, SnapshotCandidate):
        candidate = _coerce_candidate(candidate)
    if not candidate.fixed_version or not candidate.fixed_version.strip():
        raise ValueError("固定版本是构建快照的必填项")
    source = candidate.source_path.resolve(strict=True)
    if _is_link_or_reparse(candidate.source_path):
        raise ValueError("候选来源不得是链接或重解析点")
    target = Path(destination).resolve()
    if target.exists():
        if _is_link_or_reparse(target) or not target.is_dir():
            raise ValueError("快照目标必须是非链接目录或不存在目录")
    else:
        _create_safe_target(target)
    active_limits = limits or SnapshotLimits()
    if source.is_dir():
        records = tuple(_directory_records(source, active_limits))
    elif source.is_file():
        records = tuple(_archive_records(source, active_limits))
    else:
        raise ValueError("候选来源必须是普通目录或归档文件")
    files: list[SnapshotFile] = []
    for relative, size, content in records:
        target_file = _safe_target_file(target, relative)
        target_file.parent.mkdir(parents=True, exist_ok=True)
        digest = sha256(content).hexdigest() if _is_hashable(relative) else None
        with target_file.open("xb") as handle:
            handle.write(content)
        files.append(SnapshotFile(relative.as_posix(), size, digest))
    evidence_prefix = target.name
    return SnapshotManifest(
        candidate.candidate_id,
        candidate.fixed_version,
        target,
        tuple(candidate.source_evidence_paths),
        tuple(f"{evidence_prefix}/{item.path}" for item in files),
        tuple(files),
        sum(item.size for item in files),
    )


def _coerce_candidate(candidate: object) -> SnapshotCandidate:
    """兼容来源适配器的轻量对象，但仍要求调用方给出固定版本和本地快照。"""
    if isinstance(candidate, dict):
        read = candidate.get
    else:
        read = lambda name, default=None: getattr(candidate, name, default)
    identifier = read("candidate_id") or read("native_id") or read("identity")
    version = read("fixed_version") or read("version") or read("version_hint")
    source = read("source_path") or read("snapshot_path") or read("path") or read("destination")
    evidence = read("source_evidence_paths") or read("evidence_paths") or ()
    if not identifier or not source:
        raise ValueError("候选必须提供标识和本地固定版本快照路径")
    if isinstance(evidence, str):
        evidence = (evidence,)
    return SnapshotCandidate(str(identifier), str(version or ""), Path(source), tuple(str(item) for item in evidence))


@dataclass
class _Budget:
    limits: SnapshotLimits
    file_count: int = 0
    total_bytes: int = 0

    def accept(self, size: int) -> None:
        self.file_count += 1
        if self.file_count > self.limits.max_files:
            raise ValueError("快照文件数量超过边界")
        if size > self.limits.max_file_bytes:
            raise ValueError("快照单文件字节数超过边界")
        self.total_bytes += size
        if self.total_bytes > self.limits.max_total_bytes:
            raise ValueError("快照总字节数超过边界")


def _directory_records(source: Path, limits: SnapshotLimits) -> Iterable[tuple[PurePosixPath, int, bytes]]:
    budget = _Budget(limits)
    for path in sorted(source.rglob("*"), key=lambda item: item.as_posix()):
        if _is_link_or_reparse(path):
            raise ValueError("候选目录包含链接或重解析点")
        if path.is_dir():
            continue
        if not path.is_file() or not S_ISREG(path.stat().st_mode):
            raise ValueError("候选目录包含非普通文件")
        relative = PurePosixPath(path.relative_to(source).as_posix())
        _validate_relative(relative)
        size = path.stat().st_size
        budget.accept(size)
        content = path.read_bytes()
        if len(content) != size:
            raise ValueError("快照文件大小在读取时变化")
        yield relative, size, content


def _archive_records(source: Path, limits: SnapshotLimits) -> Iterable[tuple[PurePosixPath, int, bytes]]:
    budget = _Budget(limits)
    suffixes = tuple(item.lower() for item in source.suffixes)
    if source.suffix.lower() == ".zip":
        with zipfile.ZipFile(source) as archive:
            for info in sorted(archive.infolist(), key=lambda item: item.filename):
                relative = _archive_relative(info.filename)
                if info.is_dir():
                    continue
                mode = info.external_attr >> 16
                if S_ISLNK(mode):
                    raise ValueError("归档包含链接或重解析点")
                budget.accept(info.file_size)
                content = archive.read(info)
                if len(content) != info.file_size:
                    raise ValueError("快照文件大小在读取时变化")
                yield relative, info.file_size, content
        return
    if suffixes[-2:] in ((".tar", ".gz"), (".tar", ".bz2"), (".tar", ".xz")) or source.suffix.lower() == ".tar":
        with tarfile.open(source, "r:*") as archive:
            for member in sorted(archive.getmembers(), key=lambda item: item.name):
                relative = _archive_relative(member.name)
                if member.isdir():
                    continue
                if member.issym() or member.islnk() or not member.isfile():
                    raise ValueError("归档包含链接、重解析点或非普通文件")
                budget.accept(member.size)
                handle = archive.extractfile(member)
                if handle is None:
                    raise ValueError("归档文件不可读取")
                with handle:
                    content = handle.read()
                if len(content) != member.size:
                    raise ValueError("快照文件大小在读取时变化")
                yield relative, member.size, content
        return
    raise ValueError("候选快照只支持目录、zip 或 tar 归档")


def _create_safe_target(target: Path) -> None:
    parent = target.parent
    if _is_link_or_reparse(parent):
        raise ValueError("快照目标父目录不得是链接或重解析点")
    target.mkdir(parents=False)
    if _is_link_or_reparse(target):
        raise ValueError("快照目标不得是链接或重解析点")


def _safe_target_file(root: Path, relative: PurePosixPath) -> Path:
    _validate_relative(relative)
    target = root.joinpath(*relative.parts)
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        if current.exists():
            if _is_link_or_reparse(current) or not current.is_dir():
                raise ValueError("快照目标包含链接、重解析点或普通文件")
        else:
            current.mkdir()
    resolved_parent = target.parent.resolve(strict=True)
    if root not in (resolved_parent, *resolved_parent.parents):
        raise ValueError("归档路径穿越快照目标")
    return target


def _archive_relative(name: str) -> PurePosixPath:
    return _validate_relative(PurePosixPath(name.replace("\\", "/")))


def _validate_relative(path: PurePosixPath) -> PurePosixPath:
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("候选快照包含路径穿越")
    return path


def _is_hashable(path: PurePosixPath) -> bool:
    return path.suffix.lower() in _HASHABLE_SUFFIXES or path.name.casefold() in _HASHABLE_NAMES


def _is_link_or_reparse(path: Path) -> bool:
    try:
        stat = path.lstat()
    except FileNotFoundError:
        return False
    attributes = getattr(stat, "st_file_attributes", 0)
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return path.is_symlink() or bool(attributes & reparse)
