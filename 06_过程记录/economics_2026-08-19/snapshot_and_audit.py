from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import subprocess
import time
import urllib.parse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any


AUDIT_DATE = "2026-08-19"
ALLOWED_LICENSES = {
    "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "GPL-2.0", "GPL-2.0-only",
    "GPL-2.0-or-later", "GPL-3.0", "GPL-3.0-only", "GPL-3.0-or-later", "LGPL-2.1",
    "LGPL-2.1-only", "LGPL-2.1-or-later", "LGPL-3.0", "LGPL-3.0-only",
    "LGPL-3.0-or-later", "MPL-2.0", "CC-BY-4.0", "CC-BY-SA-4.0", "CC-BY-NC-4.0",
    "CC-BY-NC-SA-4.0",
}
FIXED_GITHUB_RE = re.compile(r"^https://github\.com/([^/]+/[^/]+)/blob/([0-9a-f]{40})/(.+)$", re.I)
URL_RE = re.compile(r"https?://([^/\s)>'\"]+)([^\s)>'\"]*)", re.I)


def jsonl_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def package_manifest(files: dict[str, bytes]) -> list[dict[str, Any]]:
    return [
        {"path": path.replace("\\", "/"), "size": len(content), "sha256": hashlib.sha256(content).hexdigest()}
        for path, content in sorted(files.items(), key=lambda item: item[0].casefold())
    ]


def package_manifest_sha256(files: dict[str, bytes]) -> str:
    encoded = json.dumps(package_manifest(files), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _all_text(files: dict[str, bytes]) -> str:
    parts = []
    for path, content in sorted(files.items()):
        if Path(path).suffix.lower() in {".md", ".txt", ".py", ".r", ".js", ".ts", ".sh", ".json", ".yaml", ".yml", ".toml"} or Path(path).name.lower() in {"skill.md", "license", "copying"}:
            parts.append(content.decode("utf-8", errors="replace"))
    return "\n".join(parts)


def _fixed_version(candidate: dict[str, Any]) -> str | None:
    if candidate.get("fixed_version"):
        return str(candidate["fixed_version"])
    url = str(candidate.get("candidate_url") or "")
    match = FIXED_GITHUB_RE.match(url)
    if match:
        return match.group(2).lower()
    raw = candidate.get("raw") or {}
    if candidate.get("platform") == "SkillHub" and raw.get("version"):
        return str(raw["version"])
    return None


def _license_spdx(repo_meta: dict[str, Any], files: dict[str, bytes]) -> str | None:
    fixed = repo_meta.get("_fixed_license") or {}
    license_obj = fixed.get("license") or repo_meta.get("license") or {}
    spdx = str(license_obj.get("spdx_id") or "").strip()
    if spdx and spdx not in {"NOASSERTION", "OTHER"}:
        return spdx
    names = " ".join(Path(path).name.lower() for path in files)
    text = _all_text({path: content for path, content in files.items() if "license" in Path(path).name.lower() or "copying" in Path(path).name.lower()}).lower()
    if "mit license" in text:
        return "MIT"
    if "apache license" in text and "version 2.0" in text:
        return "Apache-2.0"
    if "mozilla public license" in text and "2.0" in text:
        return "MPL-2.0"
    if "license" not in names and "copying" not in names:
        return None
    return None


def _network_evidence(text: str) -> tuple[str, str]:
    lower = text.lower()
    hosts = []
    for host, path in URL_RE.findall(text):
        host_lower = host.lower().strip(".,")
        context_is_api = (
            host_lower.startswith("api.")
            or "/api/" in path.lower()
            or any(token in lower for token in ("requests.get", "requests.post", "curl ", "fetch(", "http.get", "api endpoint"))
        )
        if context_is_api and host_lower not in {"github.com", "www.github.com"}:
            hosts.append(host_lower)
    hosts = sorted(set(hosts))
    if hosts:
        return "是", "公共或外部网络端点: " + ", ".join(hosts)
    return "否", "无"


def _local_runtime(text: str) -> str:
    lower = text.lower()
    runtimes = []
    if re.search(r"\bpython\b|\.py\b|\bpandas\b|\bstatsmodels\b", lower):
        runtimes.append("Python")
    if re.search(r"\brscript\b|\br language\b|\.r\b|\btidyverse\b", lower):
        runtimes.append("R")
    if "stata" in lower:
        runtimes.append("Stata")
    if "matlab" in lower:
        runtimes.append("MATLAB")
    if "excel" in lower:
        runtimes.append("Microsoft Excel")
    return "、".join(runtimes) if runtimes else "不使用"


def _local_interface(text: str) -> str:
    lower = text.lower()
    interfaces = []
    for token, label in ((".csv", "CSV"), (".xlsx", "XLSX"), (".xls", "Excel"), (".json", "JSON"),
                         (".pdf", "PDF"), (".docx", "DOCX"), (".dta", "Stata DTA"), (".rds", "RDS")):
        if token in lower:
            interfaces.append(label)
    if re.search(r"\bcli\b|command line|terminal|shell command", lower):
        interfaces.append("本地CLI")
    return "、".join(dict.fromkeys(interfaces)) if interfaces else "不使用"


def _behaviors(text: str) -> dict[str, Any]:
    lower = text.lower()
    external_api, network_behavior = _network_evidence(text)
    credential = bool(re.search(r"api[_ -]?key|access[_ -]?token|secret|credentials|\.env\b", lower))
    install = bool(re.search(r"pip install|npm install|conda install|apt-get|brew install|curl[^\n|]*\|\s*(?:bash|sh)", lower))
    shell = bool(re.search(r"subprocess\.|os\.system|invoke-expression|powershell\s+-|bash\s+", lower))
    destructive = bool(re.search(r"rm\s+-rf|remove-item\s+.*-recurse|drop\s+database|delete\s+from\s+\w+|format\s+[a-z]:", lower))
    write = bool(re.search(r"save\s+(?:the\s+)?(?:file|report)|write\s+(?:to|the)|export\s+.*\.(?:csv|xlsx|json|pdf)|to_csv\(|to_excel\(", lower))
    read = bool(re.search(r"read\s+(?:the\s+)?(?:file|data|table)|load\s+.*\.(?:csv|xlsx|json)|read_csv\(|read_excel\(", lower))
    executable_behavior = "无"
    if install:
        executable_behavior = "包含依赖安装或动态获取指令"
    elif shell:
        executable_behavior = "包含本地命令或脚本执行指令"
    credential_behavior = "需要凭据或密钥" if credential else "无"
    if destructive:
        file_behavior = "存在删除或破坏性写入指令"
    elif write:
        file_behavior = "存在受控文件写出"
    elif read:
        file_behavior = "只读本地文件"
    else:
        file_behavior = "无"
    if destructive:
        grade = "SX"
    elif install or credential or shell:
        grade = "SB-A"
    elif external_api == "是" or write or read:
        grade = "SB"
    else:
        grade = "SA"
    return {
        "external_api": external_api,
        "network_behavior": network_behavior,
        "local_runtime": _local_runtime(text),
        "local_interface": _local_interface(text),
        "credential_behavior": credential_behavior,
        "executable_behavior": executable_behavior,
        "file_behavior": file_behavior,
        "security_grade": grade,
    }


def audit_fixture(candidate: dict[str, Any], files: dict[str, bytes], repo_meta: dict[str, Any]) -> dict[str, Any]:
    fixed_version = _fixed_version(candidate)
    license_spdx = _license_spdx(repo_meta, files)
    text = _all_text(files)
    behaviors = _behaviors(text)
    blocking = []
    if not fixed_version:
        blocking.append("fixed_version_missing")
    if not license_spdx:
        blocking.append("license_missing")
    elif license_spdx not in ALLOWED_LICENSES:
        blocking.append("license_not_allowed")
    if not any(Path(path).name.lower() == "skill.md" for path in files):
        blocking.append("skill_definition_missing")
    if behaviors["security_grade"] not in {"SA", "SB"}:
        blocking.append("security_grade_not_formal")
    formal_eligible = not blocking
    raw = candidate.get("raw") or {}
    repository = raw.get("repository") or {}
    return {
        "candidate_key": hashlib.sha256(
            f"{candidate.get('platform')}\0{candidate.get('candidate_native_id')}".encode("utf-8")
        ).hexdigest(),
        "platform": candidate.get("platform"),
        "candidate_native_id": candidate.get("candidate_native_id"),
        "canonical_url": candidate.get("candidate_url"),
        "repository": repository.get("full_name"),
        "skill_path": raw.get("path"),
        "fixed_version": fixed_version,
        "package_manifest_sha256": package_manifest_sha256(files),
        "file_inventory": package_manifest(files),
        "license": license_spdx or "未明确",
        "license_allowed": bool(license_spdx in ALLOWED_LICENSES),
        "maintenance_date": repo_meta.get("pushed_at") or raw.get("updated_at") or raw.get("lastModified") or raw.get("updated_at"),
        **behaviors,
        "verification_status": "全部通过（未实测）" if formal_eligible else "静态核验未通过",
        "formal_eligible": formal_eligible,
        "blocking_reasons": blocking,
        "audit_date": AUDIT_DATE,
    }


def _github_identity(candidate: dict[str, Any]) -> tuple[str, str, str] | None:
    match = FIXED_GITHUB_RE.match(str(candidate.get("candidate_url") or ""))
    if not match:
        return None
    return match.group(1), match.group(2).lower(), urllib.parse.unquote(match.group(3))


def _api_get_json(url: str, token: str, attempts: int = 3) -> dict[str, Any]:
    import requests

    headers = {"Accept": "application/vnd.github+json", "User-Agent": "University-Skills-Research/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            response = requests.get(url, headers=headers, timeout=60)
            if response.status_code == 404:
                return {"_http_status": 404}
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(0.7 * (attempt + 1))
    raise RuntimeError(f"GET failed: {url}: {last}")


def _raw_get(url: str, attempts: int = 3) -> bytes:
    import requests

    last: Exception | None = None
    for attempt in range(attempts):
        try:
            response = requests.get(url, headers={"User-Agent": "University-Skills-Research/1.0"}, timeout=60)
            response.raise_for_status()
            return response.content
        except Exception as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(0.7 * (attempt + 1))
    raise RuntimeError(f"GET failed: {url}: {last}")


def _github_token() -> str:
    run = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    return run.stdout.strip() if run.returncode == 0 else ""


def group_candidates(raw_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    for row in raw_rows:
        key = (row["platform"], row["candidate_native_id"])
        if key not in grouped:
            grouped[key] = {
                "platform": row["platform"],
                "candidate_native_id": row["candidate_native_id"],
                "candidate_url": row.get("candidate_url"),
                "raw": row.get("raw") or {},
                "query_ids": [],
                "major_codes": [],
                "major_names": [],
                "discovery_queries": [],
            }
        target = grouped[key]
        for field, value in (
            ("query_ids", row["query_id"]),
            ("major_codes", row["major_code"]),
            ("major_names", row["major_name"]),
            ("discovery_queries", row["query"]),
        ):
            if value not in target[field]:
                target[field].append(value)
    return [grouped[key] for key in sorted(grouped)]


def _snapshot_github(candidate: dict[str, Any], package_root: Path, repo_meta: dict[str, Any],
                     fixed_license: dict[str, Any]) -> dict[str, Any]:
    identity = _github_identity(candidate)
    if not identity:
        raise RuntimeError("fixed GitHub URL missing")
    repo, commit, path = identity
    quoted_path = "/".join(urllib.parse.quote(part, safe="") for part in path.split("/"))
    raw_url = f"https://raw.githubusercontent.com/{repo}/{commit}/{quoted_path}"
    skill_bytes = _raw_get(raw_url)
    files = {path: skill_bytes}
    license_content = fixed_license.get("content")
    license_path = fixed_license.get("path")
    if license_content and license_path:
        files[str(license_path)] = base64.b64decode(license_content)
    digest = hashlib.sha256(f"GitHub\0{candidate['candidate_native_id']}".encode("utf-8")).hexdigest()[:20]
    package_dir = package_root / f"github_{digest}"
    for relative, content in files.items():
        destination = package_dir / "files" / Path(relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
    manifest = package_manifest(files)
    (package_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    meta = dict(repo_meta)
    meta["_fixed_license"] = fixed_license
    audit = audit_fixture({**candidate, "fixed_version": commit}, files, meta)
    audit.update(
        {
            "query_ids": sorted(candidate["query_ids"]),
            "major_codes": sorted(candidate["major_codes"]),
            "major_names": sorted(candidate["major_names"]),
            "discovery_queries": sorted(candidate["discovery_queries"]),
            "snapshot_status": "success",
            "snapshot_scope": "fixed SKILL.md and fixed-commit repository license",
            "evidence_paths": [
                (package_dir / "manifest.json").as_posix(),
                *((package_dir / "files" / Path(relative)).as_posix() for relative in sorted(files)),
            ],
            "repository_stars": repo_meta.get("stargazers_count"),
            "repository_updated_at": repo_meta.get("updated_at"),
            "repository_pushed_at": repo_meta.get("pushed_at"),
            "publisher": (repo_meta.get("owner") or {}).get("login"),
        }
    )
    return audit


def _snapshot_skillhub(candidate: dict[str, Any], package_root: Path) -> dict[str, Any]:
    raw = candidate.get("raw") or {}
    namespace = str((raw.get("namespace") or {}).get("handle") or raw.get("ownerName") or "").lstrip("@")
    slug = str(raw.get("slug") or "")
    version = str(raw.get("version") or "")
    base = "https://api.skillhub.cn/api/v1/skills/" + urllib.parse.quote(slug, safe="")
    listing_url = base + "/files?" + urllib.parse.urlencode({"version": version, "namespace": namespace})
    listing = json.loads(_raw_get(listing_url).decode("utf-8"))
    records = list(listing.get("files") or [])
    files: dict[str, bytes] = {}
    for record in records[:100]:
        path = str(record.get("path") or "")
        size = int(record.get("size") or 0)
        if not path or size > 2_000_000:
            continue
        file_url = base + "/file?" + urllib.parse.urlencode(
            {"path": path, "version": version, "namespace": namespace}
        )
        files[path] = _raw_get(file_url)
    digest = hashlib.sha256(f"SkillHub\0{candidate['candidate_native_id']}".encode("utf-8")).hexdigest()[:20]
    package_dir = package_root / f"skillhub_{digest}"
    for relative, content in files.items():
        destination = package_dir / "files" / Path(relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
    manifest = package_manifest(files)
    (package_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit = audit_fixture({**candidate, "fixed_version": version}, files, {"pushed_at": raw.get("updated_at")})
    audit.update(
        {
            "query_ids": sorted(candidate["query_ids"]),
            "major_codes": sorted(candidate["major_codes"]),
            "major_names": sorted(candidate["major_names"]),
            "discovery_queries": sorted(candidate["discovery_queries"]),
            "snapshot_status": "success",
            "snapshot_scope": "fixed SkillHub package file listing and readable files",
            "evidence_paths": [(package_dir / "manifest.json").as_posix()],
            "publisher": namespace,
            "repository_stars": raw.get("stars"),
            "repository_updated_at": raw.get("updated_at"),
            "repository_pushed_at": raw.get("updated_at"),
        }
    )
    return audit


def run_snapshot_audit(raw_path: Path, package_root: Path, audit_path: Path, workers: int = 8) -> dict[str, Any]:
    raw_rows = jsonl_rows(raw_path)
    candidates = group_candidates(raw_rows)
    package_root.mkdir(parents=True, exist_ok=True)
    token = _github_token()

    repo_names = sorted({identity[0] for candidate in candidates if (identity := _github_identity(candidate))})
    repo_refs = sorted({(identity[0], identity[1]) for candidate in candidates if (identity := _github_identity(candidate))})
    repo_meta: dict[str, dict[str, Any]] = {}
    fixed_licenses: dict[tuple[str, str], dict[str, Any]] = {}

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(_api_get_json, f"https://api.github.com/repos/{repo}", token): ("repo", repo)
            for repo in repo_names
        }
        futures.update(
            {
                pool.submit(
                    _api_get_json,
                    f"https://api.github.com/repos/{repo}/license?ref={commit}",
                    token,
                ): ("license", (repo, commit))
                for repo, commit in repo_refs
            }
        )
        for future in as_completed(futures):
            kind, key = futures[future]
            try:
                payload = future.result()
            except Exception as exc:
                payload = {"_fetch_error": str(exc)}
            if kind == "repo":
                repo_meta[str(key)] = payload
            else:
                fixed_licenses[key] = payload

    results: list[dict[str, Any]] = []

    def process(candidate: dict[str, Any]) -> dict[str, Any]:
        try:
            if candidate["platform"] == "GitHub":
                identity = _github_identity(candidate)
                if not identity:
                    raise RuntimeError("fixed GitHub identity unavailable")
                repo, commit, _ = identity
                return _snapshot_github(
                    candidate,
                    package_root,
                    repo_meta.get(repo, {}),
                    fixed_licenses.get((repo, commit), {}),
                )
            if candidate["platform"] == "SkillHub":
                return _snapshot_skillhub(candidate, package_root)
            raise RuntimeError(f"unsupported platform snapshot: {candidate['platform']}")
        except Exception as exc:
            return {
                "candidate_key": hashlib.sha256(
                    f"{candidate.get('platform')}\0{candidate.get('candidate_native_id')}".encode("utf-8")
                ).hexdigest(),
                "platform": candidate.get("platform"),
                "candidate_native_id": candidate.get("candidate_native_id"),
                "canonical_url": candidate.get("candidate_url"),
                "fixed_version": _fixed_version(candidate),
                "query_ids": sorted(candidate["query_ids"]),
                "major_codes": sorted(candidate["major_codes"]),
                "major_names": sorted(candidate["major_names"]),
                "snapshot_status": "failed",
                "snapshot_error": str(exc),
                "formal_eligible": False,
                "verification_status": "静态核验未通过",
                "security_grade": "SX",
                "license": "未明确",
                "license_allowed": False,
                "blocking_reasons": ["snapshot_failed"],
                "audit_date": AUDIT_DATE,
                "evidence_paths": [],
            }

    with ThreadPoolExecutor(max_workers=workers) as pool:
        future_map = {pool.submit(process, candidate): candidate for candidate in candidates}
        for future in as_completed(future_map):
            results.append(future.result())

    results.sort(key=lambda row: (str(row.get("platform")), str(row.get("candidate_native_id"))))
    if audit_path.exists():
        audit_path.unlink()
    append_jsonl(audit_path, results)
    return {
        "raw_record_count": len(raw_rows),
        "unique_candidate_count": len(candidates),
        "audit_row_count": len(results),
        "snapshot_success_count": sum(row.get("snapshot_status") == "success" for row in results),
        "snapshot_failed_count": sum(row.get("snapshot_status") == "failed" for row in results),
        "formal_audit_gate_count": sum(row.get("formal_eligible") is True for row in results),
        "security_grade_counts": dict(sorted(defaultdict(int, {
            grade: sum(row.get("security_grade") == grade for row in results)
            for grade in {str(row.get("security_grade")) for row in results}
        }).items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="固定并静态核验经济学候选Skill")
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--packages", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    summary = run_snapshot_audit(args.raw, args.packages, args.audit, args.workers)
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 1 if summary["snapshot_failed_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
