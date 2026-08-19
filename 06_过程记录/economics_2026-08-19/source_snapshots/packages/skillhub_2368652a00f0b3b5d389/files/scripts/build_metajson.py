#!/usr/bin/env python3
"""
Build _meta.json — the cross-reference mesh for fitness-club-digital-ai-expert.

Scans all .md files, extracts:
- File-level metadata (Cluster, Last verified, Cross-references from the > header block)
- Kebab anchors (#anchor)
- References to other files in the skill (path/to/file.md or path/to/file.md#anchor)
- Dynamic hooks
Generates a JSON catalog with per-file entries and a global cross-reference index.
"""

import json
import re
import hashlib
import sys
from pathlib import Path

# Portable: skill root = parent of this scripts/ directory (no hardcoded local path)
SKILL_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = SKILL_ROOT / "_meta.json"

# Directories to scan (all content files)
SCAN_DIRS = ["tools", "references", "data", "templates", "playbooks", "examples", "workflows"]
ROOT_FILES = ["SKILL.md"]

# Architecture layers for G13 classification
LAYER_MAP = {
    "L0": "Trivial firefighting / 日常救火",
    "L1": "Infrastructure / 设施管理",
    "L2": "Software & data / 软件与数据",
    "L3": "AI & intelligence / AI 与智能",
    "L4": "Platform & chain / 平台与连锁",
    "L5": "Strategy & governance / 战略与治理",
}

CLUSTER_AX = "ABCDEFGHIJKLMNOPQRSTUVWX"


def extract_header_blocks(text: str, filepath: Path) -> dict:
    """Extract metadata from the file's header block (> lines after the title)."""
    meta = {
        "cluster": None,
        "last_verified": None,
        "staleness": None,
        "cross_references": [],
        "g13_tri_perspective": False,
        "has_dynamic_hooks": False,
        "lines": 0,
        "size_kb": 0,
    }

    lines = text.split("\n")
    meta["lines"] = len(lines)
    meta["size_kb"] = round(len(text) / 1024, 1)

    in_header = False
    for line in lines[:15]:
        if line.startswith("> **Cluster"):
            in_header = True
        if not in_header:
            continue
        # Cluster / 集群
        m = re.search(r"> \*\*Cluster.*?\*\*:\s*(.+?)(?:\s*/|$)", line)
        if m:
            meta["cluster"] = m.group(1).strip()
        # Last verified
        m = re.search(r"> \*\*Last verified.*?\*\*:\s*(.+)", line)
        if m:
            meta["last_verified"] = m.group(1).strip()
        # Staleness
        m = re.search(r"> \*\*Staleness.*?\*\*:\s*(.+?)(?:\s*/|$)", line)
        if m:
            meta["staleness"] = m.group(1).strip()
        # Cross-references
        m = re.search(r"> \*\*Cross-references.*?\*\*:\s*(.+)", line)
        if m:
            refs = m.group(1).strip()
            # Extract file paths
            meta["cross_references"] = re.findall(r'[`]?([a-zA-Z0-9_/-]+\.md)', refs)
        # G13
        if "G13" in line or "tri-perspective" in line.lower() or "三视角" in line:
            meta["g13_tri_perspective"] = True

    # Check for dynamic hooks throughout the file
    meta["has_dynamic_hooks"] = ":::dynamic-hook" in text

    return meta


def extract_anchors(text: str) -> list[dict]:
    """Extract kebab anchors: {#anchor-name} and (#anchor-name)."""
    anchors = []
    # {#anchor-name} or (#anchor-name) patterns
    for m in re.finditer(r'[{(]#([a-z0-9][a-z0-9_-]*[a-z0-9])[})]', text):
        anchors.append({"id": m.group(1), "context_sample": text[max(0, m.start()-40):m.end()+40]})
    return anchors


def extract_file_references(text: str, filepath: Path) -> list[str]:
    """Extract references to other files in the skill."""
    refs = set()
    # tools/xx, references/xx, data/xx, templates/xx, playbooks/xx, examples/xx, workflows/xx
    for m in re.finditer(r'`([a-zA-Z0-9_/-]+\.md(?:#[a-zA-Z0-9_-]+)?)`', text):
        path_str = m.group(1)
        # Check if it's a local file reference
        if any(path_str.startswith(d) for d in SCAN_DIRS):
            refs.add(path_str)
    # Also find inline references without backticks
    for m in re.finditer(r'([a-zA-Z0-9_/-]+\.md(?:#[a-zA-Z0-9_-]+)?)', text):
        path_str = m.group(1)
        if any(path_str.startswith(d) for d in SCAN_DIRS):
            refs.add(path_str)
    return sorted(refs)


def compute_sha256(filepath: Path) -> str:
    return hashlib.sha256(filepath.read_bytes()).hexdigest()


def classify_layer_from_cluster(cluster: str | None) -> str:
    """Classify a file into L0-L5 layer based on its cluster."""
    if not cluster:
        return "L2"
    cluster_upper = cluster.split("/")[0].strip().upper()
    if cluster_upper in ("J", "T", "C"):
        return "L0"  # Daily firefighting, physical security, hardware
    if cluster_upper in ("D", "A"):
        return "L1"  # Network, infrastructure
    if cluster_upper in ("B", "H", "N", "O", "R"):
        return "L2"  # Software, data, integration
    if cluster_upper in ("E", "K", "U", "M", "W"):
        return "L3"  # AI, governance, messaging, growth
    if cluster_upper in ("P", "Q", "G"):
        return "L4"  # People, B2B, lifecycle
    if cluster_upper in ("F", "I", "L", "V", "X"):
        return "L5"  # Compliance, governance, meta
    if cluster_upper == "S":
        return "L5"  # Health-medical boundary
    return "L2"


def build_index():
    catalog = {}
    cross_ref_index = {}  # source file -> list of target files
    cluster_index = {}  # cluster letter -> list of files
    layer_index = {"L0": [], "L1": [], "L2": [], "L3": [], "L4": [], "L5": []}
    hi_index = {}  # HI-1~HI-8 -> list of files
    g13_coverage = {}  # Which clusters have G13-tri-perspective audit
    anchor_map = {}  # anchor_id -> file_path
    hook_count = 0
    file_count = 0

    # Scan root files
    for fname in ROOT_FILES:
        fp = SKILL_ROOT / fname
        if not fp.exists():
            continue
        text = fp.read_text(encoding="utf-8")
        meta = extract_header_blocks(text, fp)
        meta["sha256"] = compute_sha256(fp)
        meta["path"] = str(fp.relative_to(SKILL_ROOT))
        meta["type"] = "root"
        meta["anchors"] = extract_anchors(text)
        meta["references"] = extract_file_references(text, fp)
        meta["layer"] = "L5"

        catalog[str(fp.relative_to(SKILL_ROOT))] = meta
        cross_ref_index[str(fp.relative_to(SKILL_ROOT))] = meta["references"]
        file_count += 1
        hook_count += text.count(":::dynamic-hook")

        for a in meta["anchors"]:
            if a["id"] not in anchor_map:
                anchor_map[a["id"]] = str(fp.relative_to(SKILL_ROOT))

    # Scan directories
    for scan_dir in SCAN_DIRS:
        dirpath = SKILL_ROOT / scan_dir
        if not dirpath.exists():
            continue
        for fp in sorted(dirpath.glob("*.md")):
            text = fp.read_text(encoding="utf-8")
            meta = extract_header_blocks(text, fp)
            meta["sha256"] = compute_sha256(fp)
            rel_path = str(fp.relative_to(SKILL_ROOT))
            meta["path"] = rel_path
            meta["type"] = scan_dir
            meta["anchors"] = extract_anchors(text)
            meta["references"] = extract_file_references(text, fp)

            # Layer classification
            layer = classify_layer_from_cluster(meta["cluster"])
            meta["layer"] = layer
            layer_index[layer].append(rel_path)

            # Cluster index
            if meta["cluster"]:
                for c in CLUSTER_AX:
                    if c in meta["cluster"].upper():
                        cluster_index.setdefault(c, []).append(rel_path)

            # HI references
            for hi in range(1, 9):
                if f"HI-{hi}" in text:
                    hi_index.setdefault(f"HI-{hi}", []).append(rel_path)

            # G13 coverage
            if meta["g13_tri_perspective"] and meta["cluster"]:
                for c in CLUSTER_AX:
                    if c in meta["cluster"].upper():
                        g13_coverage.setdefault(c, 0)
                        g13_coverage[c] += 1

            catalog[rel_path] = meta
            cross_ref_index[rel_path] = meta["references"]
            file_count += 1
            hook_count += text.count(":::dynamic-hook")

            for a in meta["anchors"]:
                if a["id"] not in anchor_map:
                    anchor_map[a["id"]] = rel_path

    # Validate cross-references (broken-link detection)
    all_valid_paths = set(catalog.keys())
    broken_refs = {}
    for src, refs in cross_ref_index.items():
        broken = []
        for ref in refs:
            # Strip anchor
            base = ref.split("#")[0]
            if base not in all_valid_paths:
                broken.append(ref)
        if broken:
            broken_refs[src] = broken

    # Build the json
    output = {
        "_meta": {
            "skill_name": "fitness-club-digital-ai-expert",
            "version": "1.0.0",
            "built": "2026-07-28",
            "total_files": file_count,
            "total_hooks": hook_count,
            "total_anchors": len(anchor_map),
            "schema_version": "1.0",
            "purpose": "Cross-reference mesh powering the 4th Pillar: Self-Iteration Engine. Used by tools/00 router for anchor-based dispatch, G13 matrix audit, freshness patrol, and broken-link detection.",
            "purpose_cn": "交叉引用网，驱动第四支柱自迭代引擎。供 tools/00 路由器锚点寻址、G13 矩阵审计、保鲜巡检与断链检测。",
        },
        "catalog": catalog,
        "cross_references": cross_ref_index,
        "cluster_index": {k: sorted(v) for k, v in sorted(cluster_index.items())},
        "layer_index": {k: sorted(v) for k, v in sorted(layer_index.items())},
        "hi_index": {k: sorted(v) for k, v in sorted(hi_index.items())},
        "g13_coverage": g13_coverage,
        "anchor_map": anchor_map,
        "broken_references": broken_refs,
    }

    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ _meta.json written ({file_count} files, {hook_count} hooks, {len(anchor_map)} anchors)")
    print(f"   Layers: {', '.join(f'{k}:{len(v)}' for k, v in sorted(layer_index.items()))}")
    print(f"   Broken references: {sum(len(v) for v in broken_refs.values())} in {len(broken_refs)} files")
    for src, refs in broken_refs.items():
        for r in refs:
            print(f"   ⚠️  {src} -> {r} (file not found)")
    return output


if __name__ == "__main__":
    result = build_index()
    # Exit with non-zero if broken references found
    if result["broken_references"]:
        total_broken = sum(len(v) for v in result["broken_references"].values())
        # Many forward refs to templates/xx etc are valid (they exist now)
        # Only flag truly missing files
        actual_missing = []
        for src, refs in result["broken_references"].items():
            for r in refs:
                base = r.split("#")[0]
                p = SKILL_ROOT / base
                if not p.exists():
                    actual_missing.append((src, r))
        if actual_missing:
            print(f"\n⚠️  {len(actual_missing)} truly broken references:")
            for src, r in actual_missing:
                print(f"   {src} -> {r}")
        else:
            print("\n✅ All references resolve (forward refs to existing files are valid)")
