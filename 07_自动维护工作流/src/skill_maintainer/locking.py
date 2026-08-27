"""One project writer lock; the operating system, not diagnostic text, owns it."""

from __future__ import annotations

from datetime import datetime, timezone
import msvcrt
import os
from pathlib import Path

from .paths import assert_ordinary_path, is_link_or_reparse


class LockUnavailable(RuntimeError):
    """Another process currently holds the project writer lock."""


class SingleWriterLock:
    """A non-blocking one-byte Windows OS lock held until :meth:`release`."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path).absolute()
        self._handle = None

    @property
    def held(self) -> bool:
        return self._handle is not None

    def acquire(self) -> bool:
        if self.held:
            raise RuntimeError("当前对象已持有写者锁")
        assert_ordinary_path(self.path.parent)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        assert_ordinary_path(self.path.parent, require_directory=True)
        if self.path.exists() and is_link_or_reparse(self.path):
            raise ValueError("锁文件不得是链接或重解析点")
        handle = self.path.open("a+b")
        try:
            if is_link_or_reparse(self.path):
                raise ValueError("锁文件不得是链接或重解析点")
            if self.path.stat().st_size == 0:
                handle.write(b"\0")
                handle.flush()
                os.fsync(handle.fileno())
            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise LockUnavailable("已有进程持有项目写者锁") from exc
            handle.seek(0)
            message = f"pid={os.getpid()} started_at={datetime.now(timezone.utc).isoformat()}\n".encode("utf-8")
            handle.truncate(0)
            handle.write(message)
            handle.flush()
            os.fsync(handle.fileno())
            self._handle = handle
            return True
        except Exception:
            handle.close()
            raise

    def release(self) -> None:
        handle, self._handle = self._handle, None
        if handle is None:
            return
        try:
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        finally:
            handle.close()

    def __enter__(self) -> "SingleWriterLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.release()
