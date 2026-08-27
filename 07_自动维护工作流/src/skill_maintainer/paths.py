"""Project-local paths with containment and reparse-point protection."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def is_link_or_reparse(path: Path) -> bool:
    """Return true for a symlink or a Windows reparse point without following it."""
    try:
        stat = path.lstat()
    except FileNotFoundError:
        return False
    return path.is_symlink() or bool(getattr(stat, "st_file_attributes", 0) & 0x400)


def assert_ordinary_path(path: Path, *, require_directory: bool = False) -> None:
    """Reject a link/reparse point in any existing component of *path*."""
    absolute = path.absolute()
    chain = (absolute, *absolute.parents)
    for current in chain:
        if not current.exists() and not current.is_symlink():
            continue
        if is_link_or_reparse(current):
            raise ValueError(f"路径不得包含链接或重解析点：{current}")
    if require_directory and (not absolute.is_dir() or is_link_or_reparse(absolute)):
        raise ValueError(f"必须是普通目录：{absolute}")


def contained_child(root: Path, *parts: str) -> Path:
    """Build a relative, root-contained child path; never accept caller path injection."""
    if not parts or any(not isinstance(part, str) or not part or Path(part).is_absolute() for part in parts):
        raise ValueError("子路径必须由非空相对路径段组成")
    if any(part in {".", ".."} or "/" in part or "\\" in part for part in parts):
        raise ValueError("子路径不得包含遍历或分隔符")
    root = root.absolute()
    result = root.joinpath(*parts)
    try:
        result.relative_to(root)
    except ValueError as exc:
        raise ValueError("路径越出项目根目录") from exc
    return result


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    settings: Path
    ledger: Path
    output: Path
    runtime: Path
    staging_root: Path
    lock: Path

    @classmethod
    def from_root(cls, root: str | Path) -> "ProjectPaths":
        project = Path(root).absolute()
        assert_ordinary_path(project, require_directory=True)
        return cls(
            root=project,
            settings=project / "workflow-settings.toml",
            ledger=project / "ledger" / "Skills主台账.xlsx",
            output=project / "output",
            runtime=project / ".runtime",
            staging_root=project / ".runtime" / "staging",
            lock=project / ".runtime" / "writer.lock",
        )

    def ensure_runtime(self) -> None:
        assert_ordinary_path(self.root, require_directory=True)
        for directory in (self.runtime, self.staging_root):
            if directory.exists():
                assert_ordinary_path(directory, require_directory=True)
            else:
                directory.mkdir(parents=True, exist_ok=False)
                assert_ordinary_path(directory, require_directory=True)
