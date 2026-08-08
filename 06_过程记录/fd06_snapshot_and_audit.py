#!/usr/bin/env python3
"""Create fixed-version evidence snapshots and a draft static audit for FD06.

This program is deliberately read-only with respect to candidate projects: it only
downloads public files pinned to an immutable commit.  It never installs packages,
imports candidate code, executes candidate scripts, logs in to a teaching system,
or submits real student/manuscript data.
"""

from __future__ import annotations

import base64
import hashlib
import http.client
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "03_候选池" / "deduplicated" / "fd06.json"
SNAPSHOT_ROOT = ROOT / "03_候选池" / "source_snapshots" / "fd06"
AUDIT_DIR = ROOT / "04_验证记录"
AUDIT_JSON = AUDIT_DIR / "2026-08-08-FD06静态安全审查.json"
AUDIT_MD = AUDIT_DIR / "2026-08-08-FD06静态安全审查.md"
AUDIT_EXCLUSIONS_MD = ROOT / "06_过程记录" / "2026-08-08-FD06安全审查落选明细.md"
DEDUP_EXCLUSIONS_JSON = ROOT / "06_过程记录" / "fd06_dedup_exclusions.json"
INDEX_MD = (
    ROOT
    / "02_知识库"
    / "functional_domains"
    / "06_课程设计教学材料与教学评估"
    / "SOURCE_SNAPSHOT_INDEX.md"
)
OVERRIDES = ROOT / "06_过程记录" / "fd06_audit_overrides.json"
VERIFIED_AT = str(date.today())

TEXT_EXTENSIONS = {
    ".md", ".mdx", ".txt", ".rst", ".adoc",
    ".json", ".jsonl", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".xml",
    ".py", ".pyw", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd",
    ".rb", ".php", ".pl", ".go", ".rs", ".java", ".kt", ".kts",
    ".html", ".htm", ".css", ".scss", ".sql", ".graphql",
    ".env", ".gitignore", ".dockerignore", ".properties", ".csv", ".tsv",
}
EXECUTABLE_EXTENSIONS = {
    ".py", ".pyw", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd",
    ".rb", ".php", ".pl", ".go", ".rs", ".java", ".kt", ".kts", ".exe", ".dll",
}
DEPENDENCY_NAMES = {
    "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb",
    "pyproject.toml", "poetry.lock", "pdm.lock", "requirements.txt", "requirements-dev.txt",
    "setup.py", "setup.cfg", "pipfile", "pipfile.lock", "environment.yml", "environment.yaml",
    "cargo.toml", "cargo.lock", "go.mod", "go.sum", "gemfile", "gemfile.lock",
    "dockerfile", "docker-compose.yml", "docker-compose.yaml",
}
LICENSE_NAMES = re.compile(r"^(license|licence|copying|notice)(\..*)?$", re.I)
SKIP_PARTS = {
    ".git", "node_modules", "vendor", "dist", "build", "coverage", ".next",
    "__pycache__", ".venv", "venv", "site-packages", ".mypy_cache", ".pytest_cache",
}

PATTERNS: dict[str, list[re.Pattern[str]]] = {
    "network": [
        re.compile(r"\b(?:requests\.(?:get|post|put|delete)|urllib\.request|httpx\.|aiohttp\.|fetch\s*\(|axios\.|curl\s+|wget\s+)", re.I),
        re.compile(r"\b(?:web[_ -]?search|browser|internet access|external api|api endpoint|联网|网络搜索|外部接口)\b", re.I),
        re.compile(r"\b(?:openai|anthropic|gemini|ollama|huggingface|perplexity)[_ -]?(?:api|client|key|model)\b", re.I),
        re.compile(r"[\"']transport[\"']\s*:\s*[\"']https?[\"']", re.I),
        re.compile(r"[\"']url[\"']\s*:\s*[\"'](?:https?://|\$\{[^}]+\}/mcp)", re.I),
    ],
    "credential": [
        re.compile(r"\b(?:api[_ -]?key|access[_ -]?token|auth[_ -]?token|oauth|client[_ -]?secret|password|cookie|credential|secret key)\b", re.I),
        re.compile(r"\b(?:登录|账号凭据|密钥|令牌|口令|密码)\b", re.I),
        re.compile(r"(?:os\.(?:getenv|environ)|process\.env|\$\{?[A-Z][A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD))", re.I),
    ],
    "file_write": [
        re.compile(r"\b(?:write_text|write_bytes|writefile|appendfile|mkdir|makedirs|savefig|document\.save|workbook\.save)\b", re.I),
        re.compile(r"open\s*\([^\n]{0,120},\s*['\"](?:w|a|x|wb|ab)['\"]", re.I),
        re.compile(r"\b(?:create|write|save|export|overwrite|modify|edit|append)\b.{0,40}\b(?:file|document|report|spreadsheet|slide|output)\b", re.I),
        re.compile(r"(?:写入|保存|导出|覆盖|修改|编辑|生成).{0,20}(?:文件|文档|报告|表格|课件|输出)", re.I),
    ],
    "file_delete": [
        re.compile(r"\b(?:rm\s+-rf|rmdir\s+/s|remove-item\s+.*-recurse|unlink\s*\(|rmtree\s*\(|shutil\.rmtree|os\.remove)\b", re.I),
        re.compile(r"(?:删除|清空|递归移除).{0,20}(?:文件|目录|文件夹)", re.I),
    ],
    "process": [
        re.compile(r"\b(?:subprocess\.|os\.system|child_process|execsync|spawn\s*\(|shell\s*=\s*true|powershell|cmd\.exe)\b", re.I),
        re.compile(r"\b(?:bash|shell)\b.{0,30}\b(?:run|execute|command|script)\b", re.I),
        re.compile(r"(?:执行|运行|调用).{0,20}(?:命令|脚本|程序|终端)", re.I),
    ],
    "remote_install": [
        re.compile(r"curl\s+[^\n|]{0,240}\|\s*(?:ba)?sh", re.I),
        re.compile(r"\bnpx\s+(?:-y|--yes)\b", re.I),
        re.compile(r"[\"']command[\"']\s*:\s*[\"']npx[\"'][\s\S]{0,200}[\"']args[\"']\s*:\s*\[\s*[\"'](?:-y|--yes)[\"']", re.I),
        re.compile(r"\b(?:pip|pip3)\s+install\s+(?:git\+|https?://|[^=\s]+\s*$)", re.I | re.M),
        re.compile(r"\b(?:npm|pnpm|yarn)\s+(?:install|add)\b", re.I),
    ],
    "lms": [
        re.compile(r"\b(?:canvas|moodle|blackboard|brightspace|schoology|google classroom|ntu ?cool|kahoot)\b", re.I),
        re.compile(r"(?:教学平台|学习管理系统|教务系统|成绩系统)", re.I),
    ],
    "external_write": [
        re.compile(r"\b(?:upload|submit|publish|post|push|send|write back|sync)\b.{0,60}\b(?:grade|score|feedback|assignment|canvas|moodle|lms|review|comment|email)\b", re.I),
        re.compile(r"\b(?:grade|score|feedback|assignment|review|comment)\b.{0,60}\b(?:upload|submit|publish|post|push|send|write back|sync)\b", re.I),
        re.compile(r"\b(?:propose_update|flag_outdated|report_knowledge_gap|log_conversation)\b", re.I),
        re.compile(r"(?:上传|提交|发布|推送|回写|同步).{0,30}(?:成绩|分数|反馈|作业|评语|审稿意见|教学平台)", re.I),
    ],
    "sensitive": [
        re.compile(r"\b(?:student|learner|pupil)\b.{0,50}\b(?:name|id|email|record|grade|score|assignment|submission|work)\b", re.I),
        re.compile(r"\b(?:confidential|unpublished|double[- ]blind|single[- ]blind|personally identifiable|pii|ferpa|gdpr)\b", re.I),
        re.compile(r"(?:学生|学号|成绩|分数|作业|个人信息|隐私|未公开|保密|盲审|匿名评审|论文原稿|审稿意见)", re.I),
    ],
    "auto_decision": [
        re.compile(r"\b(?:automatically|autonomously)\b.{0,60}\b(?:grade|score|accept|reject|pass|fail|publish)\b", re.I),
        re.compile(r"\b(?:final grade|acceptance decision|rejection decision|admission decision)\b", re.I),
        re.compile(r"(?:自动|无需人工).{0,30}(?:评分|打分|录用|拒稿|通过|不通过|发布成绩|回写成绩)", re.I),
    ],
    "human_review": [
        re.compile(r"\b(?:human|teacher|instructor|educator|reviewer|editor|supervisor)\b.{0,70}\b(?:review|verify|approve|confirm|final decision|judgment|override)\b", re.I),
        re.compile(r"\b(?:draft|suggestion|recommendation|assistive|decision support)\b.{0,50}\b(?:not final|review|approval|judgment)\b", re.I),
        re.compile(r"(?:教师|导师|评审人|编辑|人工).{0,30}(?:复核|核对|确认|批准|最终决定|修改|判断)", re.I),
    ],
    "privacy_protection": [
        re.compile(r"\b(?:de-?identify|anonymi[sz]e|redact|do not upload|local only|confidentiality|data minimization)\b", re.I),
        re.compile(r"(?:去标识|匿名化|脱敏|不得上传|仅在本地|保密要求|最小数据)", re.I),
    ],
    "untrusted_input_protection": [
        re.compile(r"\b(?:prompt injection|untrusted input|ignore instructions in|treat .* as data|do not follow .*instructions)\b", re.I),
        re.compile(r"(?:提示注入|不可信输入|把.*视为数据|不要执行.*隐藏指令|忽略材料中的指令)", re.I),
    ],
    "fairness": [
        re.compile(r"\b(?:bias|fairness|equity|appeal|accommodation|accessibility|universal design)\b", re.I),
        re.compile(r"(?:偏差|公平|申诉|无障碍|合理便利|通用学习设计)", re.I),
    ],
    "academic_integrity": [
        re.compile(r"\b(?:academic integrity|plagiarism|misconduct|fabrication|citation verification)\b", re.I),
        re.compile(r"(?:学术诚信|抄袭|学术不端|伪造|引用核查)", re.I),
    ],
    "hostile_instruction": [
        re.compile(r"\bignore (?:all |any |the )?(?:previous|prior|system|developer) instructions\b", re.I),
        re.compile(r"\b(?:reveal|print|exfiltrate|steal)\b.{0,60}\b(?:system prompt|api key|token|credential|secret|cookie|ssh key)\b", re.I),
        re.compile(r"\b(?:bypass|disable|evade)\b.{0,40}\b(?:safety|security|permission|authorization|guardrail)\b", re.I),
        re.compile(r"(?:忽略|绕过).{0,20}(?:系统指令|安全规则|权限确认|授权)", re.I),
    ],
}


@dataclass
class DownloadedFile:
    path: str
    size: int
    local_path: Path
    text: str


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def retry_delays() -> tuple[float, ...]:
    return (0.0, 0.5, 1.5, 3.0, 6.0)


def gh_json(endpoint: str, allow_missing: bool = False) -> Any:
    last = ""
    for delay in retry_delays():
        if delay:
            time.sleep(delay)
        proc = subprocess.run(
            ["gh", "api", endpoint],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if proc.returncode == 0:
            return json.loads(proc.stdout)
        last = proc.stderr.strip()
        if allow_missing and ("HTTP 404" in last or "Not Found" in last):
            return None
    raise RuntimeError(f"GitHub API failed for {endpoint}: {last}")


def url_bytes(url: str, allow_missing: bool = False) -> bytes | None:
    last: Exception | None = None
    for delay in retry_delays():
        if delay:
            time.sleep(delay)
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "FD06-static-audit/1.0"})
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            last = exc
            if allow_missing and exc.code == 404:
                return None
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError, http.client.HTTPException) as exc:
            last = exc
    if allow_missing:
        return None
    raise RuntimeError(f"Download failed for {url}: {last}")


def decode_text(data: bytes) -> str:
    if b"\x00" in data[:4096]:
        return ""
    for encoding in ("utf-8-sig", "utf-8", "utf-16", "gb18030", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def safe_local_path(base: Path, repository_path: str) -> Path:
    parts = [part for part in PurePosixPath(repository_path).parts if part not in ("", ".", "..")]
    return base.joinpath(*parts)


def is_text_candidate(path: str, size: int) -> bool:
    pure = PurePosixPath(path)
    if any(part.lower() in SKIP_PARTS for part in pure.parts):
        return False
    if size > 1_500_000:
        return False
    lower_name = pure.name.lower()
    if lower_name in DEPENDENCY_NAMES:
        return True
    if LICENSE_NAMES.match(lower_name):
        return True
    if lower_name.startswith(("readme", "skill", "agents", "claude", "codex")):
        return True
    return pure.suffix.lower() in TEXT_EXTENSIONS


def package_entries(tree: list[dict[str, Any]], skill_path: str | None) -> list[dict[str, Any]]:
    blobs = [entry for entry in tree if entry.get("type") in ("blob", "file")]
    if not skill_path:
        return blobs
    parent = str(PurePosixPath(skill_path).parent)
    if parent == ".":
        # Root-level skills may refer to the whole repository.  Keep a complete
        # manifest but only download readable, security-relevant files later.
        return blobs
    if PurePosixPath(skill_path).name.lower() != "skill.md":
        stem = PurePosixPath(skill_path).stem
        reference_prefix = f"{parent}/references/{stem}/"
        return [
            entry for entry in blobs
            if entry.get("path") == skill_path or entry.get("path", "").startswith(reference_prefix)
        ]
    prefix = parent.rstrip("/") + "/"
    selected = [entry for entry in blobs if entry.get("path", "").startswith(prefix)]
    if not any(entry.get("path") == skill_path for entry in selected):
        selected.append({"path": skill_path, "type": "blob", "size": 0, "sha": None})
    return selected


def github_raw_url(repo: str, commit: str, path: str) -> str:
    quoted = "/".join(urllib.parse.quote(part, safe="") for part in PurePosixPath(path).parts)
    return f"https://raw.githubusercontent.com/{repo}/{commit}/{quoted}"


def hf_raw_url(repo: str, commit: str, path: str) -> str:
    quoted = "/".join(urllib.parse.quote(part, safe="") for part in PurePosixPath(path).parts)
    return f"https://huggingface.co/spaces/{repo}/resolve/{commit}/{quoted}?download=true"


def spdx_from_text(text: str) -> str | None:
    lower = re.sub(r"\s+", " ", text.lower())
    checks = [
        ("Open-Scholar-Academic-Noncommercial", "open scholar skill license", "academic, educational, and non-commercial research purposes"),
        ("PolyForm-Noncommercial-1.0.0", "polyform noncommercial license 1.0.0", "noncommercial purpose"),
        ("CC-BY-NC-4.0", "creative commons attribution-noncommercial 4.0", "international"),
        ("Apache-2.0", "apache license", "version 2.0"),
        ("MIT", "permission is hereby granted, free of charge", "the software"),
        ("BSD-3-Clause", "redistribution and use in source and binary forms", "neither the name"),
        ("BSD-2-Clause", "redistribution and use in source and binary forms", "this list of conditions"),
        ("GPL-3.0", "gnu general public license", "version 3"),
        ("GPL-2.0", "gnu general public license", "version 2"),
        ("AGPL-3.0", "gnu affero general public license", "version 3"),
        ("MPL-2.0", "mozilla public license", "version 2.0"),
        ("CC-BY-SA-4.0", "creative commons attribution-sharealike 4.0", "international"),
        ("CC-BY-4.0", "creative commons attribution 4.0", "international"),
        ("Unlicense", "this is free and unencumbered software released into the public domain", "unlicense"),
    ]
    for spdx, first, second in checks:
        if first in lower and second in lower:
            return spdx
    return None


def license_is_usable(spdx: str) -> bool:
    return spdx in {
        "Apache-2.0", "MIT", "MIT-0", "BSD-3-Clause", "BSD-2-Clause", "GPL-3.0", "GPL-2.0",
        "AGPL-3.0", "MPL-2.0", "CC-BY-4.0", "CC-BY-SA-4.0", "CC-BY-NC-4.0",
        "PolyForm-Noncommercial-1.0.0", "Open-Scholar-Academic-Noncommercial", "Unlicense",
    }


def normalize_license_id(value: str) -> str:
    aliases = {
        "mit": "MIT",
        "mit license": "MIT",
        "mit-0": "MIT-0",
        "apache-2.0": "Apache-2.0",
        "cc-by-4.0": "CC-BY-4.0",
        "cc-by-sa-4.0": "CC-BY-SA-4.0",
        "cc-by-nc-4.0": "CC-BY-NC-4.0",
        "creative commons attribution-noncommercial 4.0 international (cc by-nc 4.0)": "CC-BY-NC-4.0",
        "gpl-3.0": "GPL-3.0",
        "gpl-2.0": "GPL-2.0",
        "agpl-3.0": "AGPL-3.0",
        "mpl-2.0": "MPL-2.0",
    }
    return aliases.get(value.strip().lower(), value.strip())


def license_status_text(spdx: str) -> str:
    if spdx in {"CC-BY-NC-4.0", "PolyForm-Noncommercial-1.0.0", "Open-Scholar-Academic-Noncommercial"}:
        return "许可证明确但限制为学术、教育或非商业用途；采用前需确认机构和项目用途符合条款。"
    if license_is_usable(spdx):
        return "可确认开放许可证"
    return "未能确认可复用许可证"


def frontmatter_license_id(text: str) -> str | None:
    match = re.match(r"\A---\s*\r?\n(.*?)\r?\n---(?:\s*\r?\n|\Z)", text, re.DOTALL)
    if not match:
        return None
    license_line = re.search(r"(?im)^license\s*:\s*([^\r\n#]+)", match.group(1))
    if not license_line:
        return None
    value = license_line.group(1).strip().strip("'\"")
    return normalize_license_id(value) if value else None


def resolve_package_license(repo_license: dict[str, Any], downloaded: list[DownloadedFile]) -> dict[str, Any]:
    package_license_files = [item for item in downloaded if LICENSE_NAMES.match(PurePosixPath(item.path).name)]
    if not package_license_files:
        declared = [
            (item, frontmatter_license_id(item.text))
            for item in downloaded
            if PurePosixPath(item.path).name.lower() == "skill.md"
        ]
        declared = [(item, value) for item, value in declared if value]
        if not declared:
            return repo_license
        names = list(dict.fromkeys(value for _, value in declared))
        evidence = list(dict.fromkeys(
            [rel(item.local_path) for item, _ in declared] + repo_license["evidence_paths"]
        ))
        if len(names) > 1:
            return {"name": "多重许可证声明：" + " + ".join(names), "usable": False, "evidence_paths": evidence}
        return {"name": names[0], "usable": license_is_usable(names[0]), "evidence_paths": evidence}
    detected: list[str] = []
    for item in package_license_files:
        value = spdx_from_text(item.text)
        if value:
            detected.append(value)
    evidence = list(dict.fromkeys([rel(item.local_path) for item in package_license_files] + repo_license["evidence_paths"]))
    if not detected:
        return {"name": "特定技能许可证无法确认", "usable": False, "evidence_paths": evidence}
    names = list(dict.fromkeys(detected))
    if len(names) > 1:
        return {"name": "多重许可证：" + " + ".join(names), "usable": False, "evidence_paths": evidence}
    return {"name": names[0], "usable": license_is_usable(names[0]), "evidence_paths": evidence}


def match_patterns(text: str) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    for group, patterns in PATTERNS.items():
        snippets: list[str] = []
        for pattern in patterns:
            for match in pattern.finditer(text):
                start = max(0, match.start() - 90)
                end = min(len(text), match.end() + 120)
                snippet = re.sub(r"\s+", " ", text[start:end]).strip()
                if snippet not in snippets:
                    snippets.append(snippet[:360])
                if len(snippets) >= 8:
                    break
            if len(snippets) >= 8:
                break
        if snippets:
            hits[group] = snippets
    return hits


def aggregate_hits(files: Iterable[DownloadedFile]) -> dict[str, list[dict[str, str]]]:
    aggregated: dict[str, list[dict[str, str]]] = defaultdict(list)
    for item in files:
        for group, snippets in match_patterns(item.text).items():
            for snippet in snippets:
                if len(aggregated[group]) >= 12:
                    break
                aggregated[group].append({"file": item.path, "snippet": snippet})
    return dict(aggregated)


def hit(hits: dict[str, Any], key: str) -> bool:
    return bool(hits.get(key))


def summarize_behavior(hits: dict[str, Any], package_files: list[dict[str, Any]]) -> tuple[str, str, str]:
    network = "说明和已读文件中未发现必须联网的操作。"
    if hit(hits, "network"):
        network = "说明或代码提到网络搜索、网页访问或外部接口；采用前应限定可访问网站和可发送内容。"
    if hit(hits, "lms"):
        network = "涉及 Canvas、Moodle 等教学平台或类似在线服务；不得直接连接真实课程，需先确认授权和数据处理规则。"

    credential = "说明和已读文件中未发现必须提供账号、令牌或密钥。"
    if hit(hits, "credential"):
        credential = "说明或代码提到账号、令牌或接口密钥；不得使用个人长期密钥，需采用最小权限和临时凭据。"

    file_behavior = "主要是说明或模板型工作流，未发现删除文件的要求。"
    if hit(hits, "file_write"):
        file_behavior = "会创建、编辑或导出本地教学材料；使用前应指定独立输出目录并保留原文件。"
    if hit(hits, "file_delete"):
        file_behavior = "已读内容出现删除或清理文件的操作；不得直接用于真实工作区，需删去该步骤或在隔离副本中人工确认。"
    executable = [x for x in package_files if PurePosixPath(x.get("path", "")).suffix.lower() in EXECUTABLE_EXTENSIONS]
    if executable and not hit(hits, "file_write") and not hit(hits, "file_delete"):
        file_behavior = "包内含可执行脚本，但静态文字扫描未确认其必然修改文件；如需使用仍应先限定目录并逐步确认。"
    return network, credential, file_behavior


def classify(
    candidate: dict[str, Any],
    license_name: str,
    license_ok: bool,
    entry_ok: bool,
    hits: dict[str, Any],
    package_files: list[dict[str, Any]],
) -> dict[str, Any]:
    category = candidate["primary_subcategory"]
    executable = [x for x in package_files if PurePosixPath(x.get("path", "")).suffix.lower() in EXECUTABLE_EXTENSIONS]
    dependency = [x for x in package_files if PurePosixPath(x.get("path", "")).name.lower() in DEPENDENCY_NAMES]
    risks: list[str] = []
    adaptations: list[str] = []

    if not entry_ok:
        return {
            "security_grade": "SC",
            "admission": "不进入正式目录",
            "plain_conclusion": "固定版本的核心入口或关键内容无法完整读取，现有证据不足以支持采用。",
            "risk_flags": ["核心入口或关键证据无法读取"],
            "adaptation_requirements": [],
        }
    if not license_ok:
        return {
            "security_grade": "SC",
            "admission": "不进入正式目录",
            "plain_conclusion": f"公开项目未提供可确认的开放许可证（当前记录：{license_name}），不能把其内容纳入可复用技能库。",
            "risk_flags": ["许可证缺失或无法确认复用权限"],
            "adaptation_requirements": [],
        }
    if hit(hits, "hostile_instruction") and hit(hits, "credential"):
        return {
            "security_grade": "SX",
            "admission": "不进入正式目录",
            "plain_conclusion": "已读内容同时出现绕过指令边界和访问秘密信息的高危信号，必须排除并人工复核原文。",
            "risk_flags": ["疑似绕过安全指令", "疑似访问秘密信息"],
            "adaptation_requirements": [],
        }

    if executable:
        risks.append(f"包内含 {len(executable)} 个可执行脚本或代码文件")
    if dependency:
        risks.append(f"包内含 {len(dependency)} 个依赖或运行环境文件")
    if hit(hits, "network"):
        risks.append("会使用网络搜索、网页或外部接口")
    if hit(hits, "credential"):
        risks.append("会接触账号、令牌或接口密钥")
    if hit(hits, "file_write"):
        risks.append("会创建、修改或导出文件")
    if hit(hits, "file_delete"):
        risks.append("出现删除或清理文件的操作")
    if hit(hits, "process"):
        risks.append("会调用命令、脚本或外部进程")
    if hit(hits, "remote_install"):
        risks.append("出现在线安装或未充分固定版本的依赖命令")
    if hit(hits, "lms"):
        risks.append("涉及教学平台或在线课堂系统")
    if hit(hits, "external_write"):
        risks.append("可能向外部系统上传、提交或回写内容")
    if hit(hits, "sensitive"):
        risks.append("可能处理学生、成绩或未公开论文等敏感材料")
    if hit(hits, "auto_decision"):
        risks.append("说明中出现自动评分或自动决定倾向")

    grade = "SA"
    if executable or dependency or any(hit(hits, key) for key in ("network", "credential", "file_write", "file_delete", "process")):
        grade = "SB"

    high_stakes_category = category in {"06-06", "06-08", "06-11", "06-12"}
    needs_adaptation = False
    if hit(hits, "remote_install") or hit(hits, "external_write") or hit(hits, "auto_decision"):
        needs_adaptation = True
    if hit(hits, "sensitive") and hit(hits, "network"):
        needs_adaptation = True
    if high_stakes_category and not hit(hits, "human_review"):
        needs_adaptation = True
    if category in {"06-11", "06-12"} and not hit(hits, "privacy_protection"):
        needs_adaptation = True
    if category in {"06-06", "06-08"} and not hit(hits, "fairness"):
        needs_adaptation = True
    if hit(hits, "file_delete"):
        needs_adaptation = True
    if hit(hits, "hostile_instruction"):
        needs_adaptation = True

    if needs_adaptation:
        grade = "SB-A"
    if grade == "SB-A":
        keep_entry = candidate.get("skill_path") or "README.md 与不依赖在线服务的核心任务说明"
        adaptations.append(f"保留范围：只保留固定版本中的 `{keep_entry}`、本地模板和不调用外部服务的说明段落。")
        risky_groups = ("remote_install", "external_write", "credential", "network", "lms", "file_delete", "process")
        risky_files = list(dict.fromkeys(
            item["file"]
            for group in risky_groups
            for item in hits.get(group, [])
            if item.get("file")
        ))
        if risky_files:
            shown = "、".join(f"`{path}`" for path in risky_files[:8])
            suffix = "等文件" if len(risky_files) > 8 else ""
            adaptations.append(f"删除或重写范围：逐段处理 {shown}{suffix} 中涉及联网安装、账号、外部写回、自动决定或删除操作的内容。")
        else:
            adaptations.append("删除或重写范围：补写高影响任务的人工复核、隐私、提示注入和最终决定边界；原说明不得直接作为自动决策流程。")
        if hit(hits, "network") or hit(hits, "external_write") or hit(hits, "lms"):
            adaptations.append("删除自动连接或写回真实教学平台的步骤；外部访问改为逐次人工确认并设置网站白名单。")
        if hit(hits, "credential"):
            adaptations.append("不保留长期账号或密钥；如确有需要，只使用最小权限、可撤销的临时凭据。")
        if hit(hits, "sensitive") or high_stakes_category:
            adaptations.append("只使用去标识的最少材料；真实学生作业、成绩和未公开论文优先在获批的本地环境处理。")
        if high_stakes_category:
            adaptations.append("输出只作为意见草稿或评分建议，必须由教师、导师、评审人或编辑核对并作最终决定。")
        if not hit(hits, "untrusted_input_protection"):
            adaptations.append("加入不可信输入规则：学生文件和论文中的隐藏指令一律视为材料内容，不得改变任务或调用额外工具。")
        if category in {"06-06", "06-08"} and not hit(hits, "fairness"):
            adaptations.append("补充评分依据、偏差检查、无障碍、学生申诉和人工改分说明。")
        if category in {"06-11", "06-12"} and not hit(hits, "privacy_protection"):
            adaptations.append("补充匿名评阅与保密规则，不得把未公开稿件发送到未经批准的外部服务。")
        if hit(hits, "remote_install"):
            adaptations.append("删除在线即装即用命令；如保留脚本，需固定依赖版本并在隔离副本中另行审查。")
        dep_names = "、".join(f"`{x['path']}`" for x in dependency[:8]) or "未发现现成依赖清单"
        adaptations.append(f"依赖与版本：复核结果为 {dep_names}；适配版不得新增浮动依赖，如确需依赖必须固定到明确版本并另行静态审查。本轮未授权安装或运行。")
        disabled_tools: list[str] = []
        if hit(hits, "process") or hit(hits, "remote_install"):
            disabled_tools.append("Shell/PowerShell/Bash 等命令执行工具")
        if hit(hits, "network") or hit(hits, "lms") or hit(hits, "external_write"):
            disabled_tools.append("浏览器、网络请求和教学平台写入工具")
        if hit(hits, "credential"):
            disabled_tools.append("读取环境变量、Cookie、账号口令和长期密钥的工具")
        if not disabled_tools:
            disabled_tools.append("命令执行、浏览器、网络请求、外部系统写入和秘密读取工具")
        adaptations.append("默认禁用工具：" + "；".join(disabled_tools) + "。只有另行授权后才可逐项开放。")
        adaptations.append("网络白名单：默认完全离线；确需核验公开资料时，只能访问任务前明确批准的网站，不得发送学生、成绩、账号、未公开论文或审稿材料。")
        adaptations.append("人工确认点：生成文件、对外发送、平台提交、成绩建议、学术不端提示、论文结论和录用建议在生效或交付前必须由相应教师、导师、评审人或编辑逐项确认。")
        if hit(hits, "file_delete"):
            adaptations.append("删除自动清理或删除步骤，所有文件变更只作用于可恢复的副本。")

    if grade == "SA":
        conclusion = "固定版本主要由说明、清单或模板组成，静态检查未发现账号、外部写回或可执行载荷方面的阻断性问题。"
        admission = "可进入正式目录"
    elif grade == "SB":
        conclusion = "固定版本存在可识别的脚本、联网或受控文件操作；在限定目录、最小权限和人工确认下可作为候选采用。"
        admission = "可进入正式目录，但需写明限制"
    else:
        conclusion = "原包含需要删减或重写的网络、数据、自动决定或权限步骤；正式库只能收录明确列出改造要求的适配方案。"
        admission = "仅适配后进入正式目录"
    return {
        "security_grade": grade,
        "admission": admission,
        "plain_conclusion": conclusion,
        "risk_flags": list(dict.fromkeys(risks)),
        "adaptation_requirements": list(dict.fromkeys(adaptations)),
    }


def github_repo_snapshot(repo: str, candidates: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    commit = candidates[0]["fixed_version"]
    if any(item["fixed_version"] != commit for item in candidates):
        raise RuntimeError(f"Repository has multiple commits in one group: {repo}")
    repo_dir = SNAPSHOT_ROOT / "repositories" / repo.replace("/", "__") / commit
    metadata_path = repo_dir / "repo_metadata.json"
    tree_path = repo_dir / "tree_manifest.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    else:
        metadata = gh_json(f"repos/{repo}")
        write_json(metadata_path, metadata)
    if tree_path.exists():
        cached_tree = json.loads(tree_path.read_text(encoding="utf-8"))
        tree = cached_tree.get("tree", [])
    else:
        tree_response = gh_json(f"repos/{repo}/git/trees/{commit}?recursive=1")
        tree = tree_response.get("tree", [])
        slim_tree = [
            {key: entry.get(key) for key in ("path", "mode", "type", "sha", "size") if entry.get(key) is not None}
            for entry in tree
        ]
        write_json(
            tree_path,
            {"repository": repo, "fixed_version": commit, "truncated": bool(tree_response.get("truncated")), "tree": slim_tree},
        )

    license_api_path = repo_dir / "license_api.json"
    license_api = (
        json.loads(license_api_path.read_text(encoding="utf-8"))
        if license_api_path.exists()
        else gh_json(f"repos/{repo}/license?ref={commit}", allow_missing=True)
    )
    license_files: list[dict[str, Any]] = []
    if license_api:
        write_json(license_api_path, license_api)
        content = license_api.get("content")
        if content:
            data = base64.b64decode(content)
            text = decode_text(data)
            local = repo_dir / "license" / (license_api.get("name") or "LICENSE")
            write_text(local, text)
            license_files.append({"path": license_api.get("path") or "LICENSE", "local_path": rel(local), "text": text})

    root_license_paths = [
        entry.get("path") for entry in tree
        if entry.get("type") == "blob"
        and "/" not in entry.get("path", "")
        and LICENSE_NAMES.match(PurePosixPath(entry.get("path", "")).name)
    ]
    for path in root_license_paths:
        if any(item["path"] == path for item in license_files):
            continue
        local = safe_local_path(repo_dir / "license", path)
        if local.exists():
            text = local.read_text(encoding="utf-8", errors="replace")
        else:
            data = url_bytes(github_raw_url(repo, commit, path), allow_missing=True)
            if not data:
                continue
            text = decode_text(data)
            write_text(local, text)
        license_files.append({"path": path, "local_path": rel(local), "text": text})

    spdx = ((metadata.get("license") or {}).get("spdx_id") or "").strip()
    if spdx in {"", "NOASSERTION", "OTHER"}:
        api_spdx = ((license_api or {}).get("license") or {}).get("spdx_id") if license_api else None
        if api_spdx not in (None, "", "NOASSERTION", "OTHER"):
            spdx = api_spdx
    # Prefer the fixed-version license text over platform auto-detection.  Some
    # custom academic-use licenses begin with MIT-like wording and GitHub labels
    # them MIT even though they later prohibit commercial use.
    for item in license_files:
        detected = spdx_from_text(item["text"])
        if detected:
            spdx = detected
            break
    if spdx in {"", "NOASSERTION", "OTHER"}:
        spdx = "未声明或无法确认"

    license_info = {
        "name": spdx,
        "usable": license_is_usable(spdx),
        "evidence_paths": [item["local_path"] for item in license_files] or [rel(repo_dir / "repo_metadata.json")],
    }
    return metadata, tree, license_info


def download_github_package(
    repo: str,
    commit: str,
    tree: list[dict[str, Any]],
    candidate: dict[str, Any],
    shared_dir: Path,
) -> tuple[list[dict[str, Any]], list[DownloadedFile], bool, list[str]]:
    entries = package_entries(tree, candidate.get("skill_path"))
    for extra in candidate.get("additional_paths", []):
        prefix = extra.rstrip("/") + "/"
        for entry in tree:
            if entry.get("type") != "blob":
                continue
            if entry.get("path") == extra or entry.get("path", "").startswith(prefix):
                if not any(existing.get("path") == entry.get("path") for existing in entries):
                    entries.append(entry)
    manifest = [
        {key: entry.get(key) for key in ("path", "type", "size", "sha") if entry.get(key) is not None}
        for entry in entries
    ]
    selected = [entry for entry in entries if is_text_candidate(entry.get("path", ""), int(entry.get("size") or 0))]
    # Always fetch the skill entry even when a very large/truncated repository tree omits it.
    skill_path = candidate.get("skill_path")
    if skill_path:
        skill_entry = next((entry for entry in selected if entry.get("path") == skill_path), None)
        selected = [entry for entry in selected if entry.get("path") != skill_path]
        selected.insert(0, skill_entry or {"path": skill_path, "size": 0, "type": "blob", "sha": None})
    selected = selected[:240]
    downloaded: list[DownloadedFile] = []
    errors: list[str] = []
    for entry in selected:
        path = entry.get("path")
        if not path:
            continue
        local = safe_local_path(shared_dir / "files", path)
        if local.exists():
            text = local.read_text(encoding="utf-8", errors="replace")
        else:
            data = url_bytes(github_raw_url(repo, commit, path), allow_missing=True)
            if data is None:
                errors.append(f"无法读取：{path}")
                continue
            text = decode_text(data)
            if not text:
                continue
            write_text(local, text)
        downloaded.append(DownloadedFile(path=path, size=len(text.encode("utf-8")), local_path=local, text=text))
    entry_ok = bool(skill_path and any(item.path == skill_path and item.text.strip() for item in downloaded))
    return manifest, downloaded, entry_ok, errors


def hf_repo_snapshot(candidate: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any], str]:
    repo = candidate["repository"].removeprefix("huggingface.co/spaces/")
    commit = candidate["fixed_version"]
    repo_dir = SNAPSHOT_ROOT / "repositories" / ("huggingface__" + repo.replace("/", "__")) / commit
    metadata_path = repo_dir / "repo_metadata.json"
    tree_path = repo_dir / "tree_manifest.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    else:
        metadata = json.loads(url_bytes(f"https://huggingface.co/api/spaces/{repo}").decode("utf-8"))
        write_json(metadata_path, metadata)
    if tree_path.exists():
        tree = json.loads(tree_path.read_text(encoding="utf-8")).get("tree", [])
    else:
        tree = json.loads(
            url_bytes(f"https://huggingface.co/api/spaces/{repo}/tree/{commit}?recursive=true&expand=false").decode("utf-8")
        )
        write_json(tree_path, {"repository": repo, "fixed_version": commit, "tree": tree})

    card_license = normalize_license_id(str((metadata.get("cardData") or {}).get("license") or ""))
    spdx = card_license if license_is_usable(card_license) else ""
    license_evidence: list[str] = []
    for entry in tree:
        path = entry.get("path", "")
        if entry.get("type") == "file" and LICENSE_NAMES.match(PurePosixPath(path).name):
            local = safe_local_path(repo_dir / "license", path)
            if local.exists():
                text = local.read_text(encoding="utf-8", errors="replace")
            else:
                data = url_bytes(hf_raw_url(repo, commit, path), allow_missing=True)
                if not data:
                    continue
                text = decode_text(data)
                write_text(local, text)
            license_evidence.append(rel(local))
            if not spdx:
                spdx = spdx_from_text(text) or ""
    if not spdx:
        spdx = "未声明或无法确认"
    license_info = {
        "name": spdx,
        "usable": license_is_usable(spdx),
        "evidence_paths": license_evidence or [rel(repo_dir / "repo_metadata.json")],
    }
    return metadata, tree, license_info, repo


def download_hf_package(
    repo: str,
    commit: str,
    tree: list[dict[str, Any]],
    shared_dir: Path,
) -> tuple[list[dict[str, Any]], list[DownloadedFile], bool, list[str]]:
    files = [entry for entry in tree if entry.get("type") == "file"]
    manifest = [
        {key: entry.get(key) for key in ("path", "type", "size", "oid") if entry.get(key) is not None}
        for entry in files
    ]
    selected = [entry for entry in files if is_text_candidate(entry.get("path", ""), int(entry.get("size") or 0))][:240]
    downloaded: list[DownloadedFile] = []
    errors: list[str] = []
    for entry in selected:
        path = entry.get("path")
        local = safe_local_path(shared_dir / "files", path)
        if local.exists():
            text = local.read_text(encoding="utf-8", errors="replace")
        else:
            data = url_bytes(hf_raw_url(repo, commit, path), allow_missing=True)
            if data is None:
                errors.append(f"无法读取：{path}")
                continue
            text = decode_text(data)
            if not text:
                continue
            write_text(local, text)
        downloaded.append(DownloadedFile(path=path, size=len(text.encode("utf-8")), local_path=local, text=text))
    # A public Space is an application-style workflow rather than a SKILL.md package.
    # The entry is considered readable when its README or declared app file was saved;
    # suitability as a skill is decided by license and later classification.
    entry_ok = any(PurePosixPath(item.path).name.lower() == "readme.md" for item in downloaded) or bool(downloaded)
    return manifest, downloaded, entry_ok, errors


def clawhub_skill_snapshot(
    candidate: dict[str, Any],
) -> tuple[dict[str, Any], list[DownloadedFile], list[dict[str, Any]], dict[str, Any]]:
    owner = candidate["registry_owner"]
    slug = candidate["registry_slug"]
    version = candidate["fixed_version"]
    repo_dir = SNAPSHOT_ROOT / "repositories" / f"clawhub__{owner}__{slug}" / version
    metadata_path = repo_dir / "version_metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    else:
        metadata_url = (
            f"https://clawhub.ai/api/v1/skills/{urllib.parse.quote(slug)}/versions/"
            f"{urllib.parse.quote(version)}"
        )
        metadata_bytes = url_bytes(metadata_url)
        assert metadata_bytes is not None
        metadata = json.loads(metadata_bytes.decode("utf-8"))
        write_json(metadata_path, metadata)
    version_info = metadata.get("version") or {}
    if version_info.get("version") != version:
        raise ValueError(f"ClawHub fixed version mismatch: expected {version}")
    manifest = [
        {key: item.get(key) for key in ("path", "size", "sha256", "contentType") if item.get(key) is not None}
        for item in version_info.get("files", [])
    ]
    downloaded: list[DownloadedFile] = []
    for item in manifest:
        path = item.get("path")
        if not path or not is_text_candidate(path, int(item.get("size") or 0)):
            continue
        local = safe_local_path(repo_dir / "files", path)
        if local.exists():
            data = local.read_bytes()
        else:
            # Download the exact stored bytes. The preview route can normalize a
            # BOM and therefore cannot be used for manifest hash verification.
            query = urllib.parse.urlencode({"path": path, "version": version})
            data = url_bytes(
                f"https://clawhub.ai/api/v1/skills/{urllib.parse.quote(slug)}/file?{query}"
            )
            assert data is not None
        if hashlib.sha256(data).hexdigest() != item.get("sha256"):
            raise ValueError(f"ClawHub file SHA-256 mismatch: {path}")
        if not local.exists():
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_bytes(data)
        text = decode_text(data)
        if text:
            downloaded.append(DownloadedFile(path=path, size=len(data), local_path=local, text=text))
    license_name = normalize_license_id(
        str(version_info.get("license") or candidate.get("declared_license") or "未声明或无法确认")
    )
    license_info = {
        "name": license_name,
        "usable": license_is_usable(license_name),
        "evidence_paths": [rel(metadata_path)],
    }
    return metadata, downloaded, manifest, license_info


def apply_override(record: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    override = overrides.get(record["candidate_id"])
    if not override:
        return record
    allowed = {
        "security_grade", "admission", "plain_conclusion", "risk_flags",
        "adaptation_requirements", "review_note", "license", "license_status",
    }
    unknown = set(override) - allowed
    if unknown:
        raise ValueError(f"Unknown override fields for {record['candidate_id']}: {sorted(unknown)}")
    record.update(override)
    record["manual_override"] = True
    return record


def markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def make_audit_markdown(records: list[dict[str, Any]]) -> str:
    grades = Counter(item["security_grade"] for item in records)
    admitted = [item for item in records if item["security_grade"] in {"SA", "SB", "SB-A"}]
    lines = [
        "# FD06 固定版本静态安全审查",
        "",
        f"核验日期：{VERIFIED_AT}",
        "",
        "## 结论边界",
        "",
        "本次只读取公开固定版本的说明、许可证、目录清单、脚本、模板、依赖和配置文件。没有安装或运行候选，没有登录真实教学平台，也没有使用真实学生、成绩、论文或审稿数据。静态审查通过只表示在已读版本中没有发现阻断性问题，不等于对未来版本或真实运行环境作绝对安全保证。",
        "",
        "## 汇总",
        "",
        f"- 去重候选：{len(records)} 个。",
        f"- 可进入正式目录或仅适配后进入：{len(admitted)} 个。",
        f"- SA：{grades.get('SA', 0)}；SB：{grades.get('SB', 0)}；SB-A：{grades.get('SB-A', 0)}；SC：{grades.get('SC', 0)}；SX：{grades.get('SX', 0)}。",
        "- SC、SX 以及许可证无法确认的候选不进入正式 Excel、Word 或技能知识页。",
        "",
        "## 等级说明",
        "",
        "| 等级 | 通俗含义 | 正式处理 |",
        "|---|---|---|",
        "| SA | 主要是说明、清单或模板，没有发现必须运行代码、提供账号或向外部系统写入的要求 | 可收录 |",
        "| SB | 有可识别的脚本、联网或受控文件操作，但可通过限定目录、最小权限和人工确认来控制 | 可收录并写清限制 |",
        "| SB-A | 原包含需要删除或重写的联网、账号、自动评分、敏感数据或外部写回步骤 | 只收录适配方案，不能直接整包采用 |",
        "| SC | 许可证、关键证据或权限边界不足，或风险无法在本轮静态审查中充分限制 | 不收录 |",
        "| SX | 发现恶意或明显绕过授权、窃取秘密等高危行为 | 不收录 |",
        "",
        "## 逐项结果",
        "",
        "| 候选 ID | 小分类 | 名称 | 许可证 | 等级 | 处理结论 |",
        "|---|---|---|---|---|---|",
    ]
    for item in records:
        lines.append(
            "| {candidate_id} | {primary_subcategory} | {name} | {license} | {security_grade} | {admission} |".format(
                **{key: markdown_escape(item.get(key, "")) for key in (
                    "candidate_id", "primary_subcategory", "name", "license", "security_grade", "admission"
                )}
            )
        )
    lines += [
        "",
        "逐项风险线索、网络/账号/文件行为、适配要求和本地证据路径见同名 JSON。",
    ]
    return "\n".join(lines) + "\n"


def make_index_markdown(records: list[dict[str, Any]]) -> str:
    lines = [
        "# FD06 来源快照索引",
        "",
        f"取得日期：{VERIFIED_AT}",
        "",
        "本索引指向调研时保存的公开固定版本证据。快照只用于说明验证、包内容验证和静态安全审查；没有运行其中的程序。为了节省重复文件，同一仓库的元数据、许可证和源码文件按固定提交共享保存。",
        "",
        "| 候选 ID | 小分类 | 名称 | 来源 | 固定版本 | 主要证据 |",
        "|---|---|---|---|---|---|",
    ]
    for item in records:
        evidence = "；".join(item.get("evidence_paths", [])[:3])
        lines.append(
            f"| {markdown_escape(item['candidate_id'])} | {markdown_escape(item['primary_subcategory'])} | "
            f"{markdown_escape(item['name'])} | {markdown_escape(item['canonical_url'])} | "
            f"{markdown_escape(item['fixed_version'])} | {markdown_escape(evidence)} |"
        )
    lines.append("")
    return "\n".join(lines)


def make_audit_exclusions_markdown(
    records: list[dict[str, Any]], dedup_exclusion_count: int
) -> str:
    excluded = [item for item in records if item["security_grade"] in {"SC", "SX"}]
    lines = [
        "# FD06 安全审查落选明细",
        "",
        f"核验日期：{VERIFIED_AT}",
        "",
        f"本文件只保存静态安全审查阶段的内部落选项。这些项目不进入正式 Excel、Word 或知识库技能页。去重阶段的 {dedup_exclusion_count} 条合并、搜索路径和无法确认上游记录另见《FD06 内部落选记录》。",
        "",
        f"当前安全审查落选数：{len(excluded)}。",
        "",
        "| 候选 ID | 小分类 | 名称 | 等级 | 通俗理由 | 固定版本来源 |",
        "|---|---|---|---|---|---|",
    ]
    for item in excluded:
        lines.append(
            f"| {markdown_escape(item['candidate_id'])} | {markdown_escape(item['primary_subcategory'])} | "
            f"{markdown_escape(item['name'])} | {markdown_escape(item['security_grade'])} | "
            f"{markdown_escape(item['plain_conclusion'])} | {markdown_escape(item['canonical_url'])} |"
        )
    lines += [
        "",
        "逐项许可证证据、文件清单和静态扫描记录见 `04_验证记录/2026-08-08-FD06静态安全审查.json` 以及 `03_候选池/source_snapshots/fd06/`。",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    candidates = json.loads(INPUT.read_text(encoding="utf-8"))
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8")) if OVERRIDES.exists() else {}
    SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_MD.parent.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    github_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    hf_items: list[dict[str, Any]] = []
    clawhub_items: list[dict[str, Any]] = []
    for candidate in candidates:
        if candidate["source_kind"] == "github":
            github_groups[candidate["repository"]].append(candidate)
        elif candidate["source_kind"] == "huggingface_space":
            hf_items.append(candidate)
        elif candidate["source_kind"] == "clawhub_registry":
            clawhub_items.append(candidate)
        else:
            raise ValueError(f"Unsupported source kind: {candidate['source_kind']}")

    for repo_index, repo in enumerate(sorted(github_groups), 1):
        repo_candidates = sorted(github_groups[repo], key=lambda item: item["candidate_id"])
        print(f"[GitHub {repo_index}/{len(github_groups)}] {repo} ({len(repo_candidates)} candidates)", flush=True)
        metadata, tree, license_info = github_repo_snapshot(repo, repo_candidates)
        commit = repo_candidates[0]["fixed_version"]
        shared_dir = SNAPSHOT_ROOT / "repositories" / repo.replace("/", "__") / commit
        for candidate in repo_candidates:
            manifest, downloaded, entry_ok, errors = download_github_package(
                repo, commit, tree, candidate, shared_dir
            )
            candidate_dir = SNAPSHOT_ROOT / "candidates" / candidate["candidate_id"]
            write_json(candidate_dir / "package_manifest.json", manifest)
            entry_path = candidate.get("skill_path")
            entry = next((item for item in downloaded if item.path == entry_path), None)
            if entry:
                write_text(candidate_dir / "entry.md", entry.text)
            hits = aggregate_hits(downloaded)
            write_json(candidate_dir / "static_scan.json", {"hits": hits, "read_errors": errors})
            candidate_license = resolve_package_license(license_info, downloaded)
            result = classify(candidate, candidate_license["name"], candidate_license["usable"], entry_ok, hits, manifest)
            network, credential, file_behavior = summarize_behavior(hits, manifest)
            evidence = [
                rel(candidate_dir / "entry.md") if entry else rel(candidate_dir / "package_manifest.json"),
                rel(candidate_dir / "package_manifest.json"),
                rel(candidate_dir / "static_scan.json"),
                rel(shared_dir / "repo_metadata.json"),
                *candidate_license["evidence_paths"],
            ]
            record = {
                "candidate_id": candidate["candidate_id"],
                "name": candidate["name"],
                "primary_subcategory": candidate["primary_subcategory"],
                "source_kind": candidate["source_kind"],
                "source_shape": candidate.get("source_shape", "agent_skill"),
                "repository": repo,
                "source_skill_path": candidate.get("skill_path"),
                "maintainer": metadata.get("owner", {}).get("login") or repo.split("/", 1)[0],
                "canonical_url": candidate["canonical_url"],
                "fixed_version": candidate["fixed_version"],
                "verified_at": VERIFIED_AT,
                "license": candidate_license["name"],
                "license_status": license_status_text(candidate_license["name"]),
                "repository_archived": bool(metadata.get("archived")),
                "repository_pushed_at": metadata.get("pushed_at"),
                "verification_depth": "固定版本静态核验；未安装、未运行、未登录真实教学平台、未使用真实学生或论文数据。",
                "package_file_count": len(manifest),
                "readable_file_count": len(downloaded),
                "executable_files": [x["path"] for x in manifest if PurePosixPath(x.get("path", "")).suffix.lower() in EXECUTABLE_EXTENSIONS],
                "dependency_files": [x["path"] for x in manifest if PurePosixPath(x.get("path", "")).name.lower() in DEPENDENCY_NAMES],
                "network_behavior": network,
                "credential_behavior": credential,
                "file_behavior": file_behavior,
                "sensitive_data_observation": "可能涉及学生、成绩或未公开论文等敏感材料。" if hit(hits, "sensitive") else "已读说明未明确要求处理真实个人信息或未公开稿件；实际使用仍应遵守最小数据原则。",
                "human_review_observation": "说明中发现人工复核、确认或最终判断边界。" if hit(hits, "human_review") else "说明中未清楚识别人工最终复核边界；高影响任务需在适配时补充。",
                "fairness_accessibility_observation": "说明中提到公平、偏差、无障碍、合理便利或申诉相关事项。" if hit(hits, "fairness") else "说明中未清楚识别公平、无障碍或申诉边界。",
                "untrusted_input_observation": "说明中提到提示注入或不可信材料处理边界。" if hit(hits, "untrusted_input_protection") else "说明中未清楚识别学生文件或论文内隐藏指令的处理规则。",
                "academic_integrity_observation": "说明中提到学术诚信、抄袭、引用或不端线索。" if hit(hits, "academic_integrity") else "说明中未明确讨论学术诚信边界。",
                "static_scan_groups": sorted(hits),
                "read_errors": errors,
                "review_note": "已结合许可证、完整目录清单、静态扫描线索和本小分类的教育场景门槛复核。",
                "evidence_paths": list(dict.fromkeys(evidence)),
                **result,
            }
            records.append(apply_override(record, overrides))

    for hf_index, candidate in enumerate(hf_items, 1):
        print(f"[Hugging Face {hf_index}/{len(hf_items)}] {candidate['name']}", flush=True)
        metadata, tree, license_info, repo = hf_repo_snapshot(candidate)
        commit = candidate["fixed_version"]
        shared_dir = SNAPSHOT_ROOT / "repositories" / ("huggingface__" + repo.replace("/", "__")) / commit
        manifest, downloaded, entry_ok, errors = download_hf_package(repo, commit, tree, shared_dir)
        candidate_dir = SNAPSHOT_ROOT / "candidates" / candidate["candidate_id"]
        write_json(candidate_dir / "package_manifest.json", manifest)
        readme = next((item for item in downloaded if PurePosixPath(item.path).name.lower() == "readme.md"), None)
        if readme:
            write_text(candidate_dir / "entry.md", readme.text)
        hits = aggregate_hits(downloaded)
        write_json(candidate_dir / "static_scan.json", {"hits": hits, "read_errors": errors})
        candidate_license = resolve_package_license(license_info, downloaded)
        result = classify(candidate, candidate_license["name"], candidate_license["usable"], entry_ok, hits, manifest)
        network, credential, file_behavior = summarize_behavior(hits, manifest)
        evidence = [
            rel(candidate_dir / "entry.md") if readme else rel(candidate_dir / "package_manifest.json"),
            rel(candidate_dir / "package_manifest.json"),
            rel(candidate_dir / "static_scan.json"),
            rel(shared_dir / "repo_metadata.json"),
            *candidate_license["evidence_paths"],
        ]
        record = {
            "candidate_id": candidate["candidate_id"],
            "name": candidate["name"],
            "primary_subcategory": candidate["primary_subcategory"],
            "source_kind": candidate["source_kind"],
            "source_shape": candidate.get("source_shape", "public_application_workflow"),
            "repository": candidate["repository"],
            "source_skill_path": candidate.get("skill_path"),
            "maintainer": metadata.get("author") or repo.split("/", 1)[0],
            "canonical_url": candidate["canonical_url"],
            "fixed_version": commit,
            "verified_at": VERIFIED_AT,
            "license": candidate_license["name"],
            "license_status": license_status_text(candidate_license["name"]),
            "repository_archived": bool(metadata.get("disabled")),
            "repository_pushed_at": metadata.get("lastModified"),
            "verification_depth": "固定版本公开 Space 静态核验；未安装、未运行、未登录真实教学平台、未使用真实学生或论文数据。",
            "package_file_count": len(manifest),
            "readable_file_count": len(downloaded),
            "executable_files": [x["path"] for x in manifest if PurePosixPath(x.get("path", "")).suffix.lower() in EXECUTABLE_EXTENSIONS],
            "dependency_files": [x["path"] for x in manifest if PurePosixPath(x.get("path", "")).name.lower() in DEPENDENCY_NAMES],
            "network_behavior": network,
            "credential_behavior": credential,
            "file_behavior": file_behavior,
            "sensitive_data_observation": "可能涉及学生、成绩或未公开论文等敏感材料。" if hit(hits, "sensitive") else "已读说明未明确要求处理真实个人信息；实际使用仍应遵守最小数据原则。",
            "human_review_observation": "说明中发现人工复核或最终判断边界。" if hit(hits, "human_review") else "说明中未清楚识别人工最终复核边界。",
            "fairness_accessibility_observation": "说明中提到公平、偏差、无障碍或申诉事项。" if hit(hits, "fairness") else "说明中未清楚识别公平、无障碍或申诉边界。",
            "untrusted_input_observation": "说明中提到提示注入或不可信材料处理边界。" if hit(hits, "untrusted_input_protection") else "说明中未清楚识别学生文件内隐藏指令的处理规则。",
            "academic_integrity_observation": "说明中提到学术诚信、抄袭或不端线索。" if hit(hits, "academic_integrity") else "说明中未明确讨论学术诚信边界。",
            "static_scan_groups": sorted(hits),
            "read_errors": errors,
            "review_note": "已结合许可证、完整目录清单、静态扫描线索和本小分类的教育场景门槛复核。",
            "evidence_paths": list(dict.fromkeys(evidence)),
            **result,
        }
        records.append(apply_override(record, overrides))

    for clawhub_index, candidate in enumerate(clawhub_items, 1):
        print(f"[ClawHub {clawhub_index}/{len(clawhub_items)}] {candidate['name']}", flush=True)
        metadata, downloaded, manifest, candidate_license = clawhub_skill_snapshot(candidate)
        candidate_dir = SNAPSHOT_ROOT / "candidates" / candidate["candidate_id"]
        write_json(candidate_dir / "package_manifest.json", manifest)
        entry = next((item for item in downloaded if item.path.lower() == "skill.md"), None)
        if entry:
            write_text(candidate_dir / "entry.md", entry.text)
        errors: list[str] = []
        hits = aggregate_hits(downloaded)
        write_json(candidate_dir / "static_scan.json", {"hits": hits, "read_errors": errors})
        entry_ok = entry is not None
        result = classify(
            candidate,
            candidate_license["name"],
            candidate_license["usable"],
            entry_ok,
            hits,
            manifest,
        )
        network, credential, file_behavior = summarize_behavior(hits, manifest)
        version_info = metadata.get("version") or {}
        evidence = [
            rel(candidate_dir / "entry.md") if entry else rel(candidate_dir / "package_manifest.json"),
            rel(candidate_dir / "package_manifest.json"),
            rel(candidate_dir / "static_scan.json"),
            *candidate_license["evidence_paths"],
        ]
        record = {
            "candidate_id": candidate["candidate_id"],
            "name": candidate["name"],
            "primary_subcategory": candidate["primary_subcategory"],
            "source_kind": candidate["source_kind"],
            "source_shape": candidate.get("source_shape", "registry_skill"),
            "repository": candidate["repository"],
            "source_skill_path": candidate.get("skill_path"),
            "maintainer": candidate.get("registry_owner") or candidate["repository"].split("/", 1)[-1],
            "canonical_url": candidate["canonical_url"],
            "fixed_version": candidate["fixed_version"],
            "verified_at": VERIFIED_AT,
            "license": candidate_license["name"],
            "license_status": license_status_text(candidate_license["name"]),
            "repository_archived": False,
            "repository_pushed_at": version_info.get("createdAt"),
            "verification_depth": "固定注册表版本和文件哈希静态核验；未安装、未运行、未登录真实教学平台、未使用真实学生或论文数据。",
            "package_file_count": len(manifest),
            "readable_file_count": len(downloaded),
            "executable_files": [x["path"] for x in manifest if PurePosixPath(x.get("path", "")).suffix.lower() in EXECUTABLE_EXTENSIONS],
            "dependency_files": [x["path"] for x in manifest if PurePosixPath(x.get("path", "")).name.lower() in DEPENDENCY_NAMES],
            "network_behavior": network,
            "credential_behavior": credential,
            "file_behavior": file_behavior,
            "sensitive_data_observation": "可能涉及学生、成绩或未公开论文等敏感材料。" if hit(hits, "sensitive") else "已读说明未明确要求处理真实个人信息或未公开稿件；实际使用仍应遵守最小数据原则。",
            "human_review_observation": "说明中发现人工复核、确认或最终判断边界。" if hit(hits, "human_review") else "说明中未清晰识别人工最终复核边界；高影响任务需在适配时补入。",
            "fairness_accessibility_observation": "说明中提到公平、偏差、无障碍、合理便利或申诉相关事项。" if hit(hits, "fairness") else "说明中未清晰识别公平、无障碍或申诉边界。",
            "untrusted_input_observation": "说明中提到提示注入或不可信材料处理边界。" if hit(hits, "untrusted_input_protection") else "说明中未清晰识别学生文件或论文内隐藏指令的处理规则。",
            "academic_integrity_observation": "说明中提到学术诚信、抄袭、引用或不端线索。" if hit(hits, "academic_integrity") else "说明中未明确讨论学术诚信边界。",
            "static_scan_groups": sorted(hits),
            "read_errors": errors,
            "review_note": "已结合固定注册表版本、逐文件哈希、许可声明、完整目录清单、静态扫描线索和本小分类的教育场景门槛复核。",
            "evidence_paths": list(dict.fromkeys(evidence)),
            **result,
        }
        records.append(apply_override(record, overrides))

    records.sort(key=lambda item: item["candidate_id"])
    write_json(AUDIT_JSON, records)
    write_text(AUDIT_MD, make_audit_markdown(records))
    dedup_exclusions = (
        json.loads(DEDUP_EXCLUSIONS_JSON.read_text(encoding="utf-8"))
        if DEDUP_EXCLUSIONS_JSON.exists()
        else []
    )
    write_text(
        AUDIT_EXCLUSIONS_MD,
        make_audit_exclusions_markdown(records, len(dedup_exclusions)),
    )
    write_text(INDEX_MD, make_index_markdown(records))
    write_json(
        SNAPSHOT_ROOT / "snapshot_index.json",
        {
            "verified_at": VERIFIED_AT,
            "candidate_count": len(records),
            "grade_counts": dict(Counter(item["security_grade"] for item in records)),
            "records": [
                {
                    "candidate_id": item["candidate_id"],
                    "canonical_url": item["canonical_url"],
                    "fixed_version": item["fixed_version"],
                    "license": item["license"],
                    "security_grade": item["security_grade"],
                    "evidence_paths": item["evidence_paths"],
                }
                for item in records
            ],
        },
    )
    print(
        json.dumps(
            {
                "records": len(records),
                "grades": dict(Counter(item["security_grade"] for item in records)),
                "licenses": dict(Counter(item["license"] for item in records)),
                "read_errors": sum(bool(item["read_errors"]) for item in records),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
