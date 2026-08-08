"""Build the complete Task 6 delivery through a validated staging directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import uuid
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

from build_subcategorized_documents import generate_documents, load_inputs
from verify_subcategorized_documents import verify_selected_documents


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DELIVERY_ROOT = PROJECT_ROOT / "05_交付物"
OUTPUT_RELATIVE = Path("05_交付物") / "通俗细分版_2026-08-07"
ARCHIVE_ROOT = DELIVERY_ROOT / "原始版_2026-08-06"
MANIFEST_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "subcategory_manifest.json"
ASSIGNMENT_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "subcategory_assignments.json"
NODE = Path(r"C:\Users\34927\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
XLSX_BUILDER = PROJECT_ROOT / "06_过程记录" / "tools" / "build_subcategorized_spreadsheets.mjs"
XLSX_VERIFIER = PROJECT_ROOT / "06_过程记录" / "tools" / "verify_subcategorized_spreadsheets.mjs"
ORIGINAL_PATTERN = re.compile(r"^0[1-5]_.+\.(docx|xlsx)$", re.IGNORECASE)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def discover_originals(delivery_root: Path) -> list[Path]:
    """Return the exact five DOCX/five XLSX root-level originals."""
    root = delivery_root.resolve()
    candidates = sorted(
        (path for path in root.iterdir() if path.is_file() and ORIGINAL_PATTERN.fullmatch(path.name)),
        key=lambda path: path.name,
    )
    counts = Counter(path.suffix.lower() for path in candidates)
    codes = Counter(path.name[:2] for path in candidates)
    if len(candidates) != 10 or counts != {".docx": 5, ".xlsx": 5}:
        raise ValueError(f"原始文件范围不明确: total={len(candidates)} formats={dict(counts)}")
    if codes != {f"{number:02d}": 2 for number in range(1, 6)}:
        raise ValueError(f"原始文件大分类配对不完整: {dict(codes)}")
    return candidates


def _inventory_entry(source: Path, archived: Path | None = None) -> dict[str, object]:
    result: dict[str, object] = {
        "source": str(source.resolve()),
        "bytes": source.stat().st_size,
        "sha256": _sha256(source),
    }
    if archived is not None:
        result["archived"] = str(archived.resolve())
    return result


def archive_originals(sources: list[Path], archive_root: Path) -> list[dict[str, object]]:
    """Copy originals atomically; refuse to replace a differing archive file."""
    if len(sources) != 10:
        raise ValueError(f"原始文件必须恰好 10 份，实际 {len(sources)}")
    archive = archive_root.resolve()
    archive.mkdir(parents=True, exist_ok=True)
    inventory: list[dict[str, object]] = []
    for source in sources:
        source = source.resolve()
        target = archive / source.name
        before = _inventory_entry(source, target)
        if target.exists():
            if target.stat().st_size != source.stat().st_size or _sha256(target) != before["sha256"]:
                raise FileExistsError(f"归档目标已存在且与源文件不同: {target}")
        else:
            temporary = archive / f".{source.name}.{uuid.uuid4().hex}.copying"
            shutil.copy2(source, temporary)
            if temporary.stat().st_size != source.stat().st_size or _sha256(temporary) != before["sha256"]:
                temporary.unlink(missing_ok=True)
                raise IOError(f"归档复制校验失败: {source}")
            os.replace(temporary, target)
        if _inventory_entry(source)["sha256"] != before["sha256"]:
            raise IOError(f"复制过程中源文件发生变化: {source}")
        if target.stat().st_size != before["bytes"] or _sha256(target) != before["sha256"]:
            raise IOError(f"归档副本与源文件不一致: {target}")
        inventory.append(before)
    archived_names = {path.name for path in archive.iterdir() if path.is_file()}
    expected_names = {path.name for path in sources}
    if archived_names != expected_names:
        raise ValueError(f"归档目录包含非预期文件: {sorted(archived_names - expected_names)}")
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


def _assert_exact_staged_set(staging_root: Path, manifest: list[dict]) -> set[Path]:
    expected = expected_delivery_paths(manifest)
    output = staging_root.resolve() / OUTPUT_RELATIVE
    actual = {
        path.relative_to(staging_root.resolve())
        for path in output.rglob("*")
        if path.is_file()
    }
    if actual != expected:
        raise ValueError(
            f"暂存交付集合不完整: missing={sorted(map(str, expected - actual))} "
            f"extra={sorted(map(str, actual - expected))}"
        )
    empty = sorted(str(path) for path in expected if (staging_root / path).stat().st_size <= 0)
    if empty:
        raise ValueError(f"暂存文件为空: {empty}")
    return expected


def publish_staged_delivery(staging_root: Path, project_root: Path, manifest: list[dict]) -> list[Path]:
    """Atomically replace only the fixed Task 6 output directory."""
    expected = _assert_exact_staged_set(staging_root, manifest)
    project = project_root.resolve()
    final = (project / OUTPUT_RELATIVE).resolve()
    staged = (staging_root.resolve() / OUTPUT_RELATIVE).resolve()
    allowed_parent = (project / "05_交付物").resolve()
    if not _inside(final, allowed_parent) or final.name != "通俗细分版_2026-08-07":
        raise ValueError(f"发布目标不安全: {final}")
    final.parent.mkdir(parents=True, exist_ok=True)
    backup = final.parent / f".task6-previous-{uuid.uuid4().hex}"
    moved_existing = False
    try:
        if final.exists():
            os.replace(final, backup)
            moved_existing = True
        os.replace(staged, final)
    except BaseException:
        if moved_existing and backup.exists() and not final.exists():
            os.replace(backup, final)
        raise
    if backup.exists():
        shutil.rmtree(backup)
    published = [project / path for path in sorted(expected, key=str)]
    _assert_exact_staged_set(project, manifest)
    return published


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def staging_parent(project_root: Path) -> Path:
    """Keep staging on the project volume so directory publication is atomic."""
    return project_root.resolve() / "06_过程记录" / ".task6_staging"


def seed_existing_delivery(project_root: Path, staging_root: Path, manifest: list[dict]) -> list[Path]:
    """Seed only manifest files so semantic-equivalent XLSX bytes can be retained."""
    project = project_root.resolve()
    staging = staging_root.resolve()
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


def _run(command: list[str], *, env: dict[str, str] | None = None) -> None:
    completed = subprocess.run(command, cwd=PROJECT_ROOT, env=env, text=True)
    if completed.returncode:
        raise RuntimeError(f"命令失败({completed.returncode}): {' '.join(command)}")


def build_complete_delivery(project_root: Path = PROJECT_ROOT) -> dict[str, object]:
    project = project_root.resolve()
    if project != PROJECT_ROOT.resolve():
        raise ValueError("任务6仅允许在当前隔离工作区运行")
    manifest = _load_json(MANIFEST_FILE)
    if not isinstance(manifest, list):
        raise ValueError("manifest 格式错误")
    expected_delivery_paths(manifest)
    sources = discover_originals(DELIVERY_ROOT)
    source_before = {path: (path.stat().st_size, _sha256(path)) for path in sources}
    archive_inventory = archive_originals(sources, ARCHIVE_ROOT)

    records, taxonomy, loaded_manifest, repositories = load_inputs()
    assignment = _load_json(ASSIGNMENT_FILE)
    if manifest != loaded_manifest or not isinstance(assignment, dict):
        raise ValueError("生成器读取的 manifest 或归属数据不一致")
    assignments = assignment.get("assignments")
    if not isinstance(assignments, dict) or len(records) != 157 or len(assignments) != 157:
        raise ValueError("157 项输入成员不完整")
    if len({record["id"] for record in records}) != 157 or set(assignments) != {record["id"] for record in records}:
        raise ValueError("157 项成员存在遗漏或重复")

    stage_base = staging_parent(project)
    stage_base.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix="subcategory-task6-", dir=stage_base) as temporary_directory:
            staging_root = Path(temporary_directory).resolve()
            seed_existing_delivery(project, staging_root, manifest)
            document_paths = generate_documents(records, taxonomy, manifest, staging_root)
            if len(document_paths) != 66:
                raise ValueError(f"DOCX 生成数量错误: {len(document_paths)}")
            environment = os.environ.copy()
            environment["SUBCATEGORY_OUTPUT_ROOT"] = str(staging_root)
            _run([str(NODE), str(XLSX_BUILDER)], env=environment)
            _assert_exact_staged_set(staging_root, manifest)

            doc_results = verify_selected_documents(
                records,
                manifest,
                staging_root,
                taxonomy=taxonomy,
                assignments=assignments,
                repositories=repositories,
                expected_total=157,
                source_project_root=PROJECT_ROOT,
            )
            failed_docs = {key: issues for key, issues in doc_results.items() if issues}
            if failed_docs:
                first_key = sorted(failed_docs)[0]
                raise ValueError(f"暂存 DOCX 结构验证失败 {first_key}: {failed_docs[first_key]}")
            _run([str(NODE), str(XLSX_VERIFIER)], env=environment)
            published = publish_staged_delivery(staging_root, project, manifest)
    finally:
        try:
            stage_base.rmdir()
        except OSError:
            pass

    for source, before in source_before.items():
        after = (source.stat().st_size, _sha256(source))
        if after != before:
            raise IOError(f"原位置文件发生变化: {source}")
    return {
        "published": published,
        "archive_inventory": archive_inventory,
        "source_inventory": [_inventory_entry(path) for path in sources],
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
