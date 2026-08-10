from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "03_候选池" / "raw" / "2026-08-08-fd06-discovery.jsonl"
OUTPUT = ROOT / "03_候选池" / "deduplicated" / "fd06.json"
EXCLUSIONS = ROOT / "06_过程记录" / "fd06_dedup_exclusions.json"
INTERNAL_EXCLUSIONS_MD = ROOT / "06_过程记录" / "2026-08-08-FD06内部落选记录.md"
PRIOR_AUDIT = ROOT / "04_验证记录" / "2026-08-08-FD06静态安全审查.json"
USER_AGENT = "FD06-static-research/1.0"


def load_records() -> list[dict]:
    return [json.loads(line) for line in RAW.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_github_url(url: str) -> tuple[str, str, str] | None:
    match = re.match(r"https://github\.com/([^/]+/[^/]+)/blob/([^/]+)/(.+)$", url)
    if not match:
        return None
    return match.group(1), match.group(2), urllib.parse.unquote(match.group(3))


def raw_github_url(repo: str, commit: str, path: str) -> str:
    quoted = urllib.parse.quote(path, safe="/")
    return f"https://raw.githubusercontent.com/{repo}/{commit}/{quoted}"


def fetch_bytes(url: str) -> bytes:
    last_error: Exception | None = None
    for delay in (0.0, 0.5, 1.5, 3.0):
        if delay:
            time.sleep(delay)
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read()
        except Exception as exc:  # noqa: BLE001 - retried and recorded by caller
            last_error = exc
    assert last_error is not None
    raise last_error


def fetch_text(url: str) -> str:
    return fetch_bytes(url).decode("utf-8-sig", errors="replace")


def normalize_text(text: str) -> str:
    text = text.lstrip("\ufeff")
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    return "\n".join(lines).strip() + "\n"


def body_text(text: str) -> str:
    normalized = normalize_text(text)
    return re.sub(r"\A---\s*\n.*?\n---\s*\n", "", normalized, flags=re.DOTALL).strip()


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_identity(item: dict) -> str:
    path = item.get("skill_path")
    if path is None:
        path = item.get("source_skill_path")
    return "|".join((item.get("source_kind", ""), item.get("repository", ""), path or ""))


def source_priority(candidate: dict) -> tuple[int, str]:
    repo = candidate["repository"].lower()
    path = (candidate.get("skill_path") or "").lower()
    score = 50
    if repo == "anthropics/k12-teacher-skills":
        score += 80
    if repo == "learning-commons-org/agent-skills":
        score += 60
    if repo.startswith("k-dense-ai/"):
        score += 60
    if repo == "yuan1z0825/nature-skills":
        score += 60
    if repo == "aiskillstore/marketplace":
        score -= 100
    if repo == "yujxzjcn/teaching-skills-codex":
        score -= 100
    if "/codex-skill/" in path:
        score += 10
    if "/claude-skill/" in path:
        score += 5
    return score, candidate["canonical_url"]


def logical_group_key(candidate: dict) -> str:
    repo = candidate["repository"].lower()
    path = (candidate.get("skill_path") or "").replace("\\", "/").lower()
    slug = path.split("/")[-2] if path.endswith("/skill.md") else path
    if repo in {"anthropics/k12-teacher-skills", "learning-commons-org/agent-skills"}:
        return f"partner-k12:{slug}"
    if repo == "cmertdalli/polisci-review" and slug == "polisci-review":
        return "cmertdalli:polisci-review"
    if slug == "peer-review" and (
        repo == "k-dense-ai/scientific-agent-skills"
        or (repo == "aiskillstore/marketplace" and "/k-dense-ai/peer-review/" in path)
    ):
        return "k-dense-ai:peer-review"
    if slug == "nature-reviewer" and repo in {"yuan1z0825/nature-skills", "aiskillstore/marketplace"}:
        return "yuan1z0825:nature-reviewer"
    return f"body:{candidate['body_sha256']}"


def exclusion(record: dict, exclusion_type: str, reason: str, retained: str | None = None) -> dict:
    return {
        "name": record["title"],
        "discovery_url": record["discovery_url"],
        "primary_subcategory": record.get("proposed_subcategory"),
        "exclusion_type": exclusion_type,
        "plain_reason": reason,
        "retained_candidate": retained,
        "evidence_level": record.get("evidence_level"),
    }


def markdown_escape(value: object) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def internal_exclusions_markdown(exclusions: list[dict]) -> str:
    audit_excluded = 0
    if PRIOR_AUDIT.exists():
        try:
            audit = json.loads(PRIOR_AUDIT.read_text(encoding="utf-8"))
            audit_excluded = sum(item.get("security_grade") in {"SC", "SX"} for item in audit)
        except (json.JSONDecodeError, TypeError):
            audit_excluded = 0
    lines = [
        "# FD06 内部落选记录",
        "",
        f"最后更新：{date.today()}",
        "",
        "本文件保存去重阶段的重复、越界、搜索入口和证据不足记录，并链接到静态安全审查落选明细。这里的内容不进入正式 Excel、Word 或正式技能页。",
        "",
        "## 当前数量",
        "",
        f"- 去重阶段内部记录：{len(exclusions)} 条。",
        f"- 静态安全审查落选：{audit_excluded} 条。",
        f"- 两阶段内部记录合计：{len(exclusions) + audit_excluded} 条。",
        "",
        "## 去重阶段逐项记录",
        "",
        "| 序号 | 拟定小分类 | 候选或线索 | 落选类型 | 通俗理由 | 保留对象或说明 | 发现地址 |",
        "|---:|---|---|---|---|---|---|",
    ]
    for index, item in enumerate(exclusions, 1):
        retained = item.get("retained_candidate") or "不保留"
        lines.append(
            f"| {index} | {markdown_escape(item.get('primary_subcategory') or '未归类')} | "
            f"{markdown_escape(item['name'])} | {markdown_escape(item['exclusion_type'])} | "
            f"{markdown_escape(item['plain_reason'])} | {markdown_escape(retained)} | "
            f"{markdown_escape(item['discovery_url'])} |"
        )
    lines += [
        "",
        "机器可读记录见 [`fd06_dedup_exclusions.json`](fd06_dedup_exclusions.json)。",
        "",
        "## 静态安全审查落选项",
        "",
        f"静态安全审查另有 {audit_excluded} 条 SC/SX 记录。逐项名称、通俗理由和固定版本地址见 [`2026-08-08-FD06安全审查落选明细.md`](2026-08-08-FD06安全审查落选明细.md)。",
        "",
        "完整安全等级、许可证、网络与账号行为、文件行为和证据路径见 [`../04_验证记录/2026-08-08-FD06静态安全审查.md`](../04_验证记录/2026-08-08-FD06静态安全审查.md) 及同名 JSON。",
        "",
    ]
    return "\n".join(lines)


def non_github_reason(record: dict) -> tuple[str, str]:
    source = record["source_path"]
    if not record.get("proposed_subcategory"):
        if source.endswith("_search"):
            return "搜索路径", "这是一条平台搜索入口，不是可以固定版本并审查的技能包。"
        if source == "curated_index":
            return "发现索引", "这是帮助寻找候选的公开索引，不是要直接采用的技能。"
        return "偏离范围", "主要功能不属于本轮十二个教学设计与评价小分类。"
    if source == "public_project_page":
        return "实质重复", "项目介绍页与已经记录的原始仓库是同一套功能，不重复计为一个技能。"
    if source == "plugin_directory":
        return "无法固定版本", "目录页所指原始仓库当前无法访问，不能确认实际文件和版本。"
    if source == "skill_market":
        return "无法确认上游", "市场页没有提供当前可访问并可固定版本的原始技能包。"
    if source == "public_gist":
        return "许可证不清", "公开内容虽有固定修订，但没有声明复用许可证，且包含需要另行安全审查的外部命令。"
    return "证据不足", "现有页面不足以完成固定版本、许可证和包内容核验。"


def pin_huggingface(record: dict) -> tuple[dict | None, dict | None]:
    match = re.match(r"https://huggingface\.co/spaces/([^/]+/[^/]+)", record["discovery_url"])
    if not match:
        return None, exclusion(record, "无法固定版本", "无法从页面地址识别 Hugging Face Space。")
    space_id = match.group(1)
    try:
        metadata = json.loads(fetch_text(f"https://huggingface.co/api/spaces/{space_id}"))
    except Exception as exc:  # noqa: BLE001 - recorded as evidence failure
        return None, exclusion(record, "无法固定版本", f"无法读取 Hugging Face 固定版本信息：{type(exc).__name__}。")
    commit = metadata.get("sha")
    if not commit:
        return None, exclusion(record, "无法固定版本", "Hugging Face 页面没有返回可核对的提交编号。")
    candidate = {
        "candidate_id": None,
        "name": record["title"],
        "primary_subcategory": record["proposed_subcategory"],
        "secondary_tags": [],
        "canonical_url": f"https://huggingface.co/spaces/{space_id}/tree/{commit}",
        "source_kind": "huggingface_space",
        "repository": f"huggingface.co/spaces/{space_id}",
        "skill_path": None,
        "source_shape": "public_application_workflow",
        "additional_paths": [],
        "fixed_version": commit,
        "content_sha256": None,
        "body_sha256": None,
        "claimed_function": record["claimed_function"],
        "discovery_query": record["query"],
        "alternate_sources": [],
        "dedup_note": "可改造的公开应用；尚未完成包内容和许可证审查。",
    }
    return candidate, None


def pin_clawhub(record: dict) -> tuple[dict | None, dict | None]:
    match = re.match(r"https://(?:hub\.openclaw\.ai|clawhub\.ai)/([^/]+)/skills/([^/?#]+)", record["discovery_url"])
    owner = record.get("owner_hint") or (match.group(1) if match else None)
    slug = match.group(2) if match else None
    version = record.get("fixed_version_hint")
    if not owner or not slug or not version:
        return None, exclusion(record, "无法固定版本", "ClawHub 记录缺少所有者、技能名或明确版本号。")
    metadata_url = f"https://clawhub.ai/api/v1/skills/{urllib.parse.quote(slug)}/versions/{urllib.parse.quote(version)}"
    try:
        metadata = json.loads(fetch_text(metadata_url))
        version_info = metadata["version"]
        if version_info.get("version") != version:
            raise ValueError("返回版本与请求版本不一致")
        skill_file = next(item for item in version_info.get("files", []) if item.get("path") == "SKILL.md")
        # The preview route may strip a UTF-8 BOM, so it is suitable for display
        # but not for validating the registry's byte-level SHA-256 declaration.
        query = urllib.parse.urlencode({"path": "SKILL.md", "version": version})
        skill_bytes = fetch_bytes(
            f"https://clawhub.ai/api/v1/skills/{urllib.parse.quote(slug)}/file?{query}"
        )
        skill_text = skill_bytes.decode("utf-8-sig", errors="replace")
        normalized = normalize_text(skill_text)
        actual_hash = hashlib.sha256(skill_bytes).hexdigest()
        if actual_hash != skill_file.get("sha256"):
            raise ValueError("SKILL.md SHA-256 与版本清单不一致")
    except Exception as exc:  # noqa: BLE001 - recorded as evidence failure
        return None, exclusion(record, "证据不足", f"ClawHub 固定版本读取或哈希核验失败：{type(exc).__name__}。")
    candidate = {
        "candidate_id": None,
        "name": record["title"],
        "primary_subcategory": record["proposed_subcategory"],
        "secondary_tags": [],
        "canonical_url": f"https://clawhub.ai/{owner}/skills/{slug}?version={version}",
        "source_kind": "clawhub_registry",
        "repository": f"clawhub.ai/{owner}/{slug}",
        "skill_path": "SKILL.md",
        "source_shape": "registry_skill",
        "additional_paths": [],
        "fixed_version": version,
        "content_sha256": sha256(normalized),
        "body_sha256": sha256(body_text(normalized)),
        "declared_license": version_info.get("license") or "未声明或无法确认",
        "registry_owner": owner,
        "registry_slug": slug,
        "claimed_function": record["claimed_function"],
        "discovery_query": record["query"],
        "alternate_sources": [],
        "dedup_note": "公开技能市场的固定版本、逐文件哈希和核心入口已核对；等待静态安全审查。",
    }
    return candidate, None


def main() -> None:
    records = load_records()
    exclusions: list[dict] = []
    github_jobs: list[tuple[dict, str, str, str]] = []
    candidates: list[dict] = []

    for record in records:
        parsed = parse_github_url(record["discovery_url"])
        if parsed:
            repo, commit, path = parsed
            if not record.get("proposed_subcategory"):
                exclusions.append(exclusion(record, "偏离范围", "主要功能不属于本轮十二个小分类。"))
                continue
            if repo == "YujxZJCN/teaching-skills-codex" and path == "skills/teaching-suite/SKILL.md":
                exclusions.append(
                    exclusion(
                        record,
                        "实质重复",
                        "这是十五个原始教学技能的合并构建产物；正式库保留各原始技能，不把合并包再计一次。",
                        "https://github.com/YujxZJCN/teaching-skills",
                    )
                )
                continue
            github_jobs.append((record, repo, commit, path))
            continue
        if record["source_path"] == "huggingface_space":
            candidate, failed = pin_huggingface(record)
            if candidate:
                candidates.append(candidate)
            if failed:
                exclusions.append(failed)
            continue
        if record["source_path"] == "clawhub_skill":
            candidate, failed = pin_clawhub(record)
            if candidate:
                candidates.append(candidate)
            if failed:
                exclusions.append(failed)
            continue
        exclusion_type, reason = non_github_reason(record)
        exclusions.append(exclusion(record, exclusion_type, reason))

    def prepare(job: tuple[dict, str, str, str]) -> tuple[dict, dict | None]:
        record, repo, commit, path = job
        try:
            text = fetch_text(raw_github_url(repo, commit, path))
        except Exception as exc:  # noqa: BLE001 - recorded as evidence failure
            return {}, exclusion(
                record,
                "证据不足",
                f"固定版本技能入口读取失败：{type(exc).__name__}。",
            )
        normalized = normalize_text(text)
        candidate = {
            "candidate_id": None,
            "name": record["title"],
            "primary_subcategory": record["proposed_subcategory"],
            "secondary_tags": [],
            "canonical_url": record["discovery_url"],
            "source_kind": "github",
            "repository": repo,
            "skill_path": path,
            "source_shape": record.get("source_shape", "agent_skill"),
            "additional_paths": record.get("additional_paths", []),
            "fixed_version": commit,
            "content_sha256": sha256(normalized),
            "body_sha256": sha256(body_text(normalized)),
            "claimed_function": record["claimed_function"],
            "discovery_query": record["query"],
            "alternate_sources": [],
            "dedup_note": "固定版本技能入口已读取；等待许可证和静态安全审查。",
        }
        return candidate, None

    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = [pool.submit(prepare, job) for job in github_jobs]
        for future in as_completed(futures):
            candidate, failed = future.result()
            if candidate:
                candidates.append(candidate)
            if failed:
                exclusions.append(failed)

    grouped: dict[str, list[dict]] = {}
    unique_without_hash: list[dict] = []
    for candidate in candidates:
        if candidate["body_sha256"]:
            grouped.setdefault(logical_group_key(candidate), []).append(candidate)
        else:
            unique_without_hash.append(candidate)

    deduplicated: list[dict] = []
    for group in grouped.values():
        preferred = max(group, key=source_priority)
        alternates = [item for item in group if item is not preferred]
        preferred["alternate_sources"] = sorted(item["canonical_url"] for item in alternates)
        preferred["_identity_aliases"] = [source_identity(item) for item in alternates]
        if alternates:
            same_body = len({item["body_sha256"] for item in group}) == 1
            if same_body:
                preferred["dedup_note"] = f"与 {len(alternates)} 个固定版本入口正文相同；保留较接近原始上游的入口。"
            else:
                preferred["dedup_note"] = f"与 {len(alternates)} 个入口属于同一技能的合作发布、生态适配或市场转载；保留较接近原始上游的入口。"
        deduplicated.append(preferred)
        for duplicate in alternates:
            record = {
                "title": duplicate["name"],
                "discovery_url": duplicate["canonical_url"],
                "proposed_subcategory": duplicate["primary_subcategory"],
                "evidence_level": "fixed_version_content_match",
            }
            exclusions.append(
                exclusion(
                    record,
                    "实质重复",
                    "该入口与保留对象属于同一技能的相同正文、合作发布、生态适配或市场转载，只保留较接近原始上游的入口。",
                    preferred["canonical_url"],
                )
            )

    deduplicated.extend(unique_without_hash)
    previous_ids: dict[str, str] = {}
    anchor_path = PRIOR_AUDIT if PRIOR_AUDIT.exists() else OUTPUT
    if anchor_path.exists():
        try:
            previous = json.loads(anchor_path.read_text(encoding="utf-8"))
            previous_ids = {source_identity(item): item["candidate_id"] for item in previous}
        except (json.JSONDecodeError, KeyError, TypeError):
            previous_ids = {}
    deduplicated.sort(key=lambda item: (item["primary_subcategory"], item["name"].casefold(), item["canonical_url"]))
    used_ids = set(previous_ids.values())
    next_number = max((int(value.rsplit("C", 1)[-1]) for value in used_ids), default=0) + 1
    for candidate in deduplicated:
        old_id = previous_ids.get(source_identity(candidate))
        if not old_id:
            old_id = next(
                (previous_ids[alias] for alias in candidate.get("_identity_aliases", []) if alias in previous_ids),
                None,
            )
        if old_id:
            candidate["candidate_id"] = old_id
            candidate.pop("_identity_aliases", None)
            continue
        while f"FD06-C{next_number:04d}" in used_ids:
            next_number += 1
        candidate["candidate_id"] = f"FD06-C{next_number:04d}"
        candidate.pop("_identity_aliases", None)
        used_ids.add(candidate["candidate_id"])
        next_number += 1

    exclusions.sort(key=lambda item: (item.get("primary_subcategory") or "99", item["name"].casefold(), item["discovery_url"]))
    OUTPUT.write_text(json.dumps(deduplicated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    EXCLUSIONS.write_text(json.dumps(exclusions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    INTERNAL_EXCLUSIONS_MD.write_text(
        internal_exclusions_markdown(exclusions), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "raw_records": len(records),
                "deduplicated_candidates": len(deduplicated),
                "excluded_or_merged": len(exclusions),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
