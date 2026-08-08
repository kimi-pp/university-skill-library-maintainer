#!/usr/bin/env python3
"""make-dist.py —— 把本 skill 打包为 repo/unified-thesis-reviewer/ 分发目录 + zip。

用法:
    python3 tools/make-dist.py
    python3 tools/make-dist.py --output-dir /custom/repo/dir
    python3 tools/make-dist.py --skip-zip

输出:
    - <workspace>/repo/unified-thesis-reviewer/  （完整分发目录）
    - <workspace>/dist/unified-thesis-reviewer-v{VERSION}.zip

排除清单:
    - tests/   测试不随分发
    - __pycache__/  Python 字节码缓存
    - .git / .gitignore
    - *.pyc
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = SKILL_ROOT.parent.parent.parent  # .kiro/skills/<skill>/tools/.. = .kiro/skills/<skill> → ../../../ = workspace
REPO_DEFAULT = WORKSPACE_ROOT / "repo" / "unified-thesis-reviewer"
DIST_DEFAULT = WORKSPACE_ROOT / "dist"

EXCLUDE_DIRS = {
    "tests",
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    ".release",
    "dist",
    "repo",
}
EXCLUDE_FILES = {".gitignore", ".gitkeep", ".DS_Store"}
EXCLUDE_PATTERNS = (re.compile(r".*\.pyc$"), re.compile(r".*\.pyo$"))

VERSION = "2.7.0"


def should_skip(rel: Path) -> bool:
    """判断相对路径是否需要排除。"""
    for part in rel.parts:
        if part in EXCLUDE_DIRS:
            return True
        if part in EXCLUDE_FILES:
            return True
    for pat in EXCLUDE_PATTERNS:
        if pat.match(rel.name):
            return True
    return False


def copy_to_repo(skill_root: Path, repo_dir: Path) -> int:
    """复制 skill 文件到 repo_dir，排除白名单指定的目录/文件。"""
    if repo_dir.exists():
        shutil.rmtree(repo_dir)
    repo_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for src in skill_root.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(skill_root)
        if should_skip(rel):
            continue
        dst = repo_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        count += 1
    return count


def make_zip(repo_dir: Path, dist_dir: Path, version: str) -> Path:
    """把 repo_dir 打包为 dist/unified-thesis-reviewer-v{version}.zip。"""
    dist_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dist_dir / f"unified-thesis-reviewer-v{version}.zip"
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        root_name = repo_dir.name
        for p in repo_dir.rglob("*"):
            if p.is_file():
                arcname = Path(root_name) / p.relative_to(repo_dir)
                z.write(p, arcname.as_posix())
    return zip_path


def run_bundle(skill_root: Path) -> bool:
    """运行 build-bundle.py 确保 _bundled/ 最新。"""
    script = skill_root / "tools" / "build-bundle.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True, text=True,
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return False
    return True


def run_verify(repo_dir: Path) -> bool:
    """对 repo_dir 跑 bundle-verify.py 验证。"""
    script = SKILL_ROOT / "tools" / "bundle-verify.py"
    result = subprocess.run(
        [sys.executable, str(script), "--path", str(repo_dir)],
        capture_output=True, text=True,
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return False
    return True


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="make-dist",
        description="Build repo/unified-thesis-reviewer/ distribution dir and zip.",
    )
    ap.add_argument("--output-dir", type=Path, default=REPO_DEFAULT)
    ap.add_argument("--dist-dir", type=Path, default=DIST_DEFAULT)
    ap.add_argument("--version", default=VERSION)
    ap.add_argument("--skip-zip", action="store_true")
    ap.add_argument("--skip-bundle", action="store_true",
                    help="skip running build-bundle.py before packaging")
    ap.add_argument("--skip-verify", action="store_true",
                    help="skip running bundle-verify.py after packaging")
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    print(f"[make-dist] skill root: {SKILL_ROOT}")
    print(f"[make-dist] repo dir:   {args.output_dir}")
    print(f"[make-dist] version:    {args.version}")

    # Step 1: 运行 build-bundle 确保 _bundled/ 最新
    if not args.skip_bundle:
        print("[make-dist] running build-bundle.py ...")
        if not run_bundle(SKILL_ROOT):
            print("[make-dist] build-bundle failed", file=sys.stderr)
            return 2

    # Step 2: 复制到 repo/
    n = copy_to_repo(SKILL_ROOT, args.output_dir)
    print(f"[make-dist] copied {n} files to {args.output_dir}")

    # Step 3: 跑 bundle-verify
    if not args.skip_verify:
        print("[make-dist] running bundle-verify.py ...")
        if not run_verify(args.output_dir):
            print("[make-dist] bundle-verify failed", file=sys.stderr)
            return 3

    # Step 4: 打 zip
    if not args.skip_zip:
        zip_path = make_zip(args.output_dir, args.dist_dir, args.version)
        size_kb = zip_path.stat().st_size / 1024
        print(f"[make-dist] wrote {zip_path} ({size_kb:.1f} KB)")

    print("[make-dist] done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
