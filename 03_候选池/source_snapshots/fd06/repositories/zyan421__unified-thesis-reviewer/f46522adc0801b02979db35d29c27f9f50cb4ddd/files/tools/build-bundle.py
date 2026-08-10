#!/usr/bin/env python3
"""Build bundle for unified-thesis-reviewer.

把 `legal-thesis-reviewer` 与 `legal-citation-checker` 两个底层 skill 的
`rules/` 和 `templates/` 目录白名单复制到本 skill 的 `_bundled/` 下，
再为整个 bundle 生成 manifest.json（含 SHA256 + 时间戳 + 底层 skill 版本），
并做版权合规检查（严禁把 GB/T 7714 原文、《法学引注手册》原文、
或张庆霖老师评阅书原始素材打入 bundle）。

用法:
    python3 tools/build-bundle.py
    python3 tools/build-bundle.py --tr /path/to/legal-thesis-reviewer \
                                  --cc /path/to/legal-citation-checker

约束:
    - 仅使用 Python 3.8+ 标准库：shutil / json / hashlib / os / pathlib /
      datetime / sys / re / argparse
    - 不修改底层 skill 任何文件；是单向复制
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------- #
# 常量
# --------------------------------------------------------------------------- #

SKILL_ROOT = Path(__file__).resolve().parent.parent
BUNDLED_DIR = SKILL_ROOT / "_bundled"
SKILLS_ROOT = SKILL_ROOT.parent  # .kiro/skills/

# 底层 skill 默认路径（可被 CLI 参数覆盖）
DEFAULT_TR = SKILLS_ROOT / "legal-thesis-reviewer"
DEFAULT_CC = SKILLS_ROOT / "legal-citation-checker"

# 白名单子目录：只复制这些，不复制 examples / tools / tests / .git / _bundled
WHITELIST_SUBDIRS = ("rules", "templates")

# 本地保留但不打包的文件模式（R9.4：不向第三方分发张老师原始素材）
# 匹配到这些的文件在复制阶段就被跳过，不会进 bundle
LOCAL_ONLY_PATTERNS = [
    re.compile(r"^zhangqinglin-original", re.IGNORECASE),
    re.compile(r"张庆霖.*原始"),
]

# 版权合规检查：这些文件名模式若出现在 bundle 内即视为违规
# 注意：gb7714-checklist.md / manual-checklist.md 等派生规则不在此列表——
# 它们是规则要点提炼，不是原文。block 的是标准原文命名（如 gb7714-2015.docx）
COPYRIGHT_BLACKLIST_PATTERNS = [
    re.compile(r"^gb[_-]?7714[_-]?\d{4}", re.IGNORECASE),  # 如 gb7714-2015
    re.compile(r"^法学引注手册"),  # 整本原文命名
    re.compile(r"^.*\.docx$", re.IGNORECASE),  # bundle 内不应出现任何 docx
    re.compile(r"^.*\.pdf$", re.IGNORECASE),   # bundle 内不应出现任何 pdf
]

# manifest.json schema 版本（与 issues.json 的 schema_version 独立）
MANIFEST_SCHEMA_VERSION = "1.0"


# --------------------------------------------------------------------------- #
# 段 1：白名单复制
# --------------------------------------------------------------------------- #

def clean_bundle_dir(dst: Path) -> None:
    """清空 bundle 目录；保留父目录以避免重建时出现权限问题。"""
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)


def copy_subdir(src_skill: Path, dst_sub: Path, subdir: str) -> tuple[int, list[str]]:
    """从 `<src_skill>/<subdir>/` 复制所有内容到 `<dst_sub>/<subdir>/`。

    LOCAL_ONLY_PATTERNS 命中的文件会被跳过，不进入 bundle。
    返回 (复制的文件数, 被跳过文件的相对路径列表)。
    """
    src_dir = src_skill / subdir
    if not src_dir.is_dir():
        return 0, []
    dst_dir = dst_sub / subdir
    dst_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    skipped: list[str] = []
    for path in src_dir.rglob("*"):
        if path.is_file():
            # 检查是否命中 LOCAL_ONLY_PATTERNS
            if any(pat.search(path.name) for pat in LOCAL_ONLY_PATTERNS):
                skipped.append(path.relative_to(src_dir).as_posix())
                continue
            rel = path.relative_to(src_dir)
            target = dst_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            count += 1
    return count, skipped


def whitelist_copy_underlying(tr_path: Path, cc_path: Path, dst: Path) -> dict:
    """把 TR 与 CC 各自的 rules/ 与 templates/ 按白名单复制到 dst 下。"""
    result: dict = {}
    for src_skill, sub_name in (
        (tr_path, "legal-thesis-reviewer.rules"),
        (cc_path, "legal-citation-checker.rules"),
    ):
        dst_sub = dst / sub_name
        dst_sub.mkdir(parents=True, exist_ok=True)

        per_skill: dict = {}
        if not src_skill.is_dir():
            print(f"[warn] source skill not found: {src_skill}", file=sys.stderr)
            result[sub_name] = {"__missing__": True}
            continue

        skipped_all: list[str] = []
        for subdir in WHITELIST_SUBDIRS:
            n, skipped = copy_subdir(src_skill, dst_sub, subdir)
            per_skill[subdir] = n
            skipped_all.extend(f"{subdir}/{p}" for p in skipped)
        if skipped_all:
            per_skill["_skipped_local_only"] = skipped_all
        result[sub_name] = per_skill
    return result


# --------------------------------------------------------------------------- #
# 段 2：manifest 生成
# --------------------------------------------------------------------------- #

def sha256_of_file(path: Path, chunk: int = 65536) -> str:
    """计算文件的 SHA256 十六进制摘要。"""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            buf = f.read(chunk)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


def read_skill_version(skill_path: Path) -> str:
    """从 SKILL.md YAML front-matter 中读取 version 字段。

    若缺失则返回 'unversioned'。不引入 yaml 第三方库；仅支持
    `version: x.y.z` 形式的一行字段。
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.is_file():
        return "unversioned"
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return "unversioned"
    # 只扫描首个 --- ... --- 之间的内容
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return "unversioned"
    fm = m.group(1)
    vm = re.search(r"^version:\s*(\S+)\s*$", fm, re.MULTILINE)
    if vm:
        return vm.group(1).strip()
    return "unversioned"


def walk_bundle_files(dst: Path) -> list[Path]:
    """返回 bundle 目录下所有文件路径（不含目录），相对路径升序。"""
    files = [p for p in dst.rglob("*") if p.is_file()]
    files.sort(key=lambda p: p.relative_to(dst).as_posix())
    return files


def build_manifest(
    tr_path: Path,
    cc_path: Path,
    dst: Path,
    copy_stats: dict,
) -> dict:
    """构造 manifest 字典。"""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    entries: list[dict] = []
    for p in walk_bundle_files(dst):
        if p.name == "manifest.json":
            continue  # 不把 manifest 本身计入
        rel = p.relative_to(dst).as_posix()
        entries.append({
            "path": rel,
            "size": p.stat().st_size,
            "sha256": sha256_of_file(p),
        })

    manifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "generated_at": now,
        "bundler": "unified-thesis-reviewer/tools/build-bundle.py",
        "underlying_skills": {
            "legal-thesis-reviewer": {
                "source_path": str(tr_path),
                "version": read_skill_version(tr_path),
                "files_copied": copy_stats.get("legal-thesis-reviewer.rules", {}),
            },
            "legal-citation-checker": {
                "source_path": str(cc_path),
                "version": read_skill_version(cc_path),
                "files_copied": copy_stats.get("legal-citation-checker.rules", {}),
            },
        },
        "files": entries,
    }
    return manifest


def write_manifest(dst: Path, manifest: dict) -> Path:
    path = dst / "manifest.json"
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    return path


# --------------------------------------------------------------------------- #
# 段 3：版权合规检查
# --------------------------------------------------------------------------- #

class CopyrightViolation(RuntimeError):
    """bundle 内出现了版权黑名单文件。"""


def check_copyright(dst: Path) -> list[str]:
    """扫描 bundle 目录，命中黑名单则 raise。返回命中文件的相对路径列表（空表示合规）。"""
    violations: list[str] = []
    for p in dst.rglob("*"):
        if not p.is_file():
            continue
        name = p.name
        for pat in COPYRIGHT_BLACKLIST_PATTERNS:
            if pat.search(name):
                violations.append(p.relative_to(dst).as_posix())
                break
    if violations:
        raise CopyrightViolation(
            "bundle 内检测到版权黑名单文件，请确认底层 skill 未把原文材料打入 rules/:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )
    return violations


# --------------------------------------------------------------------------- #
# 主入口
# --------------------------------------------------------------------------- #

def parse_args(argv: list[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        prog="build-bundle",
        description="Bundle legal-thesis-reviewer + legal-citation-checker "
                    "rules/ + templates/ into unified-thesis-reviewer/_bundled/",
    )
    ap.add_argument(
        "--tr", type=Path, default=DEFAULT_TR,
        help=f"path to legal-thesis-reviewer skill dir (default: {DEFAULT_TR})",
    )
    ap.add_argument(
        "--cc", type=Path, default=DEFAULT_CC,
        help=f"path to legal-citation-checker skill dir (default: {DEFAULT_CC})",
    )
    ap.add_argument(
        "--dst", type=Path, default=BUNDLED_DIR,
        help=f"destination bundle dir (default: {BUNDLED_DIR})",
    )
    ap.add_argument(
        "--dry-run", action="store_true",
        help="do not write files; print what would be done",
    )
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    tr_path: Path = args.tr.resolve()
    cc_path: Path = args.cc.resolve()
    dst: Path = args.dst.resolve()

    print(f"[build-bundle] TR  = {tr_path}")
    print(f"[build-bundle] CC  = {cc_path}")
    print(f"[build-bundle] DST = {dst}")

    if args.dry_run:
        print("[build-bundle] dry-run; no files written.")
        return 0

    # 段 1：白名单复制
    clean_bundle_dir(dst)
    stats = whitelist_copy_underlying(tr_path, cc_path, dst)
    for name, per in stats.items():
        print(f"[build-bundle] copied: {name} -> {per}")

    # 段 3 早期执行：在写 manifest 之前先过版权合规
    # 之所以放在 manifest 前，是为了命中违规时 manifest 不留脏痕迹
    try:
        check_copyright(dst)
    except CopyrightViolation as e:
        print(str(e), file=sys.stderr)
        # 清空脏 bundle，避免后续误用
        clean_bundle_dir(dst)
        return 2

    # 段 2：manifest 生成
    manifest = build_manifest(tr_path, cc_path, dst, stats)
    manifest_path = write_manifest(dst, manifest)
    print(f"[build-bundle] wrote manifest: {manifest_path}")
    print(f"[build-bundle] total files in bundle: {len(manifest['files'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
