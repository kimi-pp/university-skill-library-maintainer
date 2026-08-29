"""固定版本候选的只读快照构建；绝不导入、执行或安装候选内容。"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
import os
from pathlib import Path, PurePosixPath
from stat import S_ISLNK, S_ISREG
import tarfile
from typing import Iterable
import weakref
import zipfile


@dataclass(frozen=True)
class SnapshotLimits:
    max_files: int = 10_000
    max_total_bytes: int = 128 * 1024 * 1024
    max_file_bytes: int = 32 * 1024 * 1024
    max_archive_bytes: int = 32 * 1024 * 1024

    def __post_init__(self) -> None:
        if min(self.max_files, self.max_total_bytes, self.max_file_bytes, self.max_archive_bytes) <= 0:
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
    fixed_content_hash: str


_TRUSTED_MANIFESTS: dict[int, tuple[weakref.ReferenceType[SnapshotManifest], tuple[object, ...]]] = {}


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
    target = _safe_destination(destination)
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
    return _materialize_snapshot(candidate, target, records)


def build_archive_snapshot(
    *, candidate_id: str, fixed_version: str, archive_bytes: bytes, archive_name: str,
    destination: str | Path, source_evidence_paths: tuple[str, ...] = (),
    limits: SnapshotLimits | None = None,
) -> SnapshotManifest:
    """Extract one immutable archive byte snapshot, never reopening its source path."""
    if not candidate_id.strip() or not fixed_version.strip():
        raise ValueError("候选标识和固定版本是构建归档快照的必填项")
    active_limits = limits or SnapshotLimits()
    if len(archive_bytes) > active_limits.max_archive_bytes:
        raise ValueError("固定包压缩字节数超过硬边界")
    target = _safe_destination(destination)
    if target.exists():
        if _is_link_or_reparse(target) or not target.is_dir():
            raise ValueError("快照目标必须是非链接目录或不存在目录")
    else:
        _create_safe_target(target)
    candidate = SnapshotCandidate(candidate_id, fixed_version, Path(archive_name), source_evidence_paths)
    records = tuple(_archive_byte_records(bytes(archive_bytes), archive_name, active_limits))
    return _materialize_snapshot(candidate, target, records)


def archive_skill_entries(
    archive_bytes: bytes, archive_name: str, limits: SnapshotLimits | None = None,
) -> tuple[str, ...]:
    """Return exact repository-relative SKILL.md entry paths from one archive."""
    active = limits or SnapshotLimits()
    if len(archive_bytes) > active.max_archive_bytes:
        raise ValueError("固定包压缩字节数超过硬边界")
    records = _repository_records(tuple(_archive_byte_records(bytes(archive_bytes), archive_name, active)))
    entries = tuple(path.as_posix() for path, _, _ in records if path.name.casefold() == "skill.md")
    return tuple(sorted(entries, key=str.casefold))


def build_archive_entry_snapshot(
    *, candidate_id: str, fixed_version: str, archive_bytes: bytes, archive_name: str,
    skill_entry_path: str, destination: str | Path,
    source_evidence_paths: tuple[str, ...] = (), limits: SnapshotLimits | None = None,
) -> SnapshotManifest:
    """Build a candidate-exact snapshot for one verified SKILL.md entry."""
    active = limits or SnapshotLimits()
    if len(archive_bytes) > active.max_archive_bytes:
        raise ValueError("固定包压缩字节数超过硬边界")
    entry = _validate_relative(PurePosixPath(skill_entry_path.replace("\\", "/")))
    records = _repository_records(tuple(_archive_byte_records(bytes(archive_bytes), archive_name, active)))
    available = {path.as_posix() for path, _, _ in records if path.name.casefold() == "skill.md"}
    if entry.as_posix() not in available:
        raise ValueError("Skill 入口路径不属于固定归档")
    base = entry.parent
    selected = []
    for path, size, content in records:
        if path == entry or (base != PurePosixPath(".") and path.is_relative_to(base)) or (
            path.parent == PurePosixPath(".") and path.name.casefold() in {"license", "license.md", "copying", "notice"}
        ):
            selected.append((path, size, content))
    target = _safe_destination(destination)
    if target.exists():
        if _is_link_or_reparse(target) or not target.is_dir():
            raise ValueError("快照目标必须是非链接目录或不存在目录")
    else:
        _create_safe_target(target)
    candidate = SnapshotCandidate(candidate_id, fixed_version, Path(archive_name), source_evidence_paths)
    return _materialize_snapshot(candidate, target, selected)


def _materialize_snapshot(
    candidate: SnapshotCandidate, target: Path,
    records: Iterable[tuple[PurePosixPath, int, bytes]],
) -> SnapshotManifest:
    files: list[SnapshotFile] = []
    content_fingerprint = sha256()
    for relative, size, content in records:
        target_file = _safe_target_file(target, relative)
        target_file.parent.mkdir(parents=True, exist_ok=True)
        digest = sha256(content).hexdigest() if _is_hashable(relative) else None
        with target_file.open("xb") as handle:
            handle.write(content)
        files.append(SnapshotFile(relative.as_posix(), size, digest))
        content_fingerprint.update(relative.as_posix().encode("utf-8"))
        content_fingerprint.update(b"\0")
        content_fingerprint.update(str(size).encode("ascii"))
        content_fingerprint.update(b"\0")
        content_fingerprint.update(sha256(content).digest())
    evidence_prefix = target.name
    manifest = SnapshotManifest(
        candidate.candidate_id,
        candidate.fixed_version,
        target,
        tuple(candidate.source_evidence_paths),
        tuple(f"{evidence_prefix}/{item.path}" for item in files),
        tuple(files),
        sum(item.size for item in files),
        content_fingerprint.hexdigest(),
    )
    _register_manifest(manifest)
    return manifest


def consume_trusted_snapshot(manifest: object) -> SnapshotManifest:
    """只允许真实构建出的未篡改快照进入一次审查包构建。"""
    record = _TRUSTED_MANIFESTS.get(id(manifest))
    if record is None or record[0]() is not manifest or _manifest_facts(manifest) != record[1]:
        raise ValueError("审查包必须使用已构建且未篡改的快照清单")
    _TRUSTED_MANIFESTS.pop(id(manifest), None)
    return manifest


def clear_snapshot_run_state() -> None:
    """供编排层 finally 调用，释放未消费的本次运行快照身份。"""
    _TRUSTED_MANIFESTS.clear()


def _register_manifest(manifest: SnapshotManifest) -> None:
    identity = id(manifest)

    def _discard(reference: weakref.ReferenceType[SnapshotManifest]) -> None:
        record = _TRUSTED_MANIFESTS.get(identity)
        if record is not None and record[0] is reference:
            _TRUSTED_MANIFESTS.pop(identity, None)

    _TRUSTED_MANIFESTS[identity] = (weakref.ref(manifest, _discard), _manifest_facts(manifest))


def _manifest_facts(manifest: object) -> tuple[object, ...]:
    if not isinstance(manifest, SnapshotManifest):
        return ()
    return (
        manifest.candidate_id, manifest.fixed_version, manifest.destination,
        tuple(manifest.source_evidence_paths), tuple(manifest.evidence_paths), tuple(manifest.files),
        manifest.total_bytes, manifest.fixed_content_hash,
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
            seen: set[str] = set()
            for info in sorted(archive.infolist(), key=lambda item: item.filename):
                relative = _archive_relative(info.filename)
                _accept_archive_name(relative, seen)
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
            seen: set[str] = set()
            for member in sorted(archive.getmembers(), key=lambda item: item.name):
                relative = _archive_relative(member.name)
                _accept_archive_name(relative, seen)
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


def _archive_byte_records(
    content: bytes, archive_name: str, limits: SnapshotLimits,
) -> Iterable[tuple[PurePosixPath, int, bytes]]:
    budget = _Budget(limits)
    archive_path = Path(archive_name)
    suffixes = tuple(item.lower() for item in archive_path.suffixes)
    stream = BytesIO(content)
    if archive_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(stream) as archive:
            seen: set[str] = set()
            for info in sorted(archive.infolist(), key=lambda item: item.filename):
                relative = _archive_relative(info.filename)
                _accept_archive_name(relative, seen)
                if info.is_dir():
                    continue
                mode = info.external_attr >> 16
                if S_ISLNK(mode):
                    raise ValueError("归档包含链接或重解析点")
                budget.accept(info.file_size)
                member = archive.read(info)
                if len(member) != info.file_size:
                    raise ValueError("快照文件大小在读取时变化")
                yield relative, info.file_size, member
        return
    if suffixes[-2:] in ((".tar", ".gz"), (".tar", ".bz2"), (".tar", ".xz")) or archive_path.suffix.lower() == ".tar":
        with tarfile.open(fileobj=stream, mode="r:*") as archive:
            seen: set[str] = set()
            for member_info in sorted(archive.getmembers(), key=lambda item: item.name):
                relative = _archive_relative(member_info.name)
                _accept_archive_name(relative, seen)
                if member_info.isdir():
                    continue
                if member_info.issym() or member_info.islnk() or not member_info.isfile():
                    raise ValueError("归档包含链接、重解析点或非普通文件")
                budget.accept(member_info.size)
                handle = archive.extractfile(member_info)
                if handle is None:
                    raise ValueError("归档文件不可读取")
                with handle:
                    member = handle.read()
                if len(member) != member_info.size:
                    raise ValueError("快照文件大小在读取时变化")
                yield relative, member_info.size, member
        return
    raise ValueError("候选快照只支持 zip 或 tar 归档")


def _create_safe_target(target: Path) -> None:
    _assert_existing_components_are_safe(target.parent)
    target.mkdir(parents=False)
    if _is_link_or_reparse(target):
        raise ValueError("快照目标不得是链接或重解析点")


def _safe_destination(destination: str | Path) -> Path:
    """在 resolve 前保留调用方指定路径的链接/重解析点边界。"""
    requested = Path(destination)
    target = requested.absolute()
    _assert_existing_components_are_safe(target)
    return target


def _assert_existing_components_are_safe(path: Path) -> None:
    """逐段检查原始路径；不能让 resolve 把中间链接折叠到外部目录。"""
    if not path.is_absolute():
        path = path.absolute()
    parts = path.parts
    current = Path(parts[0]) if parts else path
    if _is_link_or_reparse(current):
        raise ValueError("快照目标包含链接或重解析点")
    for part in parts[1:]:
        current = current / part
        if current.exists() or current.is_symlink():
            if _is_link_or_reparse(current):
                raise ValueError("快照目标包含链接或重解析点")
        else:
            break


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
    reserved = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("候选快照包含路径穿越")
    for part in path.parts:
        stem = part.split(".", 1)[0].casefold()
        if ":" in part or part.endswith((".", " ")) or stem in reserved:
            raise ValueError("候选快照包含 Windows 不安全路径")
    return path


def _accept_archive_name(path: PurePosixPath, seen: set[str]) -> None:
    identity = path.as_posix().casefold()
    if identity in seen:
        raise ValueError("归档包含大小写冲突或重复路径")
    seen.add(identity)


def _repository_records(
    records: tuple[tuple[PurePosixPath, int, bytes], ...],
) -> tuple[tuple[PurePosixPath, int, bytes], ...]:
    if not records:
        return ()
    first_parts = {record[0].parts[0] for record in records}
    strip_root = len(first_parts) == 1 and all(len(record[0].parts) > 1 for record in records)
    normalized = []
    seen: set[str] = set()
    for path, size, content in records:
        relative = PurePosixPath(*path.parts[1:]) if strip_root else path
        _validate_relative(relative)
        _accept_archive_name(relative, seen)
        normalized.append((relative, size, content))
    return tuple(normalized)


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
