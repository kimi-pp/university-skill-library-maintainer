from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "03_候选池" / "raw" / "2026-08-08-fd06-discovery.jsonl"
OUTPUT = ROOT / "03_候选池" / "deduplicated" / "fd06.json"
EXCLUSIONS = ROOT / "06_过程记录" / "fd06_dedup_exclusions.json"
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


def fetch_text(url: str) -> str:
    last_error: Exception | None = None
    for delay in (0.0, 0.5, 1.5, 3.0):
        if delay:
            time.sleep(delay)
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read().decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001 - retried and recorded by caller
            last_error = exc
    assert last_error is not None
    raise last_error


def normalize_text(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    return "\n".join(lines).strip() + "\n"


def body_text(text: str) -> str:
    normalized = normalize_text(text)
    return re.sub(r"\A---\s*\n.*?\n---\s*\n", "", normalized, flags=re.DOTALL).strip()


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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
        "fixed_version": commit,
        "content_sha256": None,
        "body_sha256": None,
        "claimed_function": record["claimed_function"],
        "discovery_query": record["query"],
        "alternate_sources": [],
        "dedup_note": "可改造的公开应用；尚未完成包内容和许可证审查。",
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
    deduplicated.sort(key=lambda item: (item["primary_subcategory"], item["name"].casefold(), item["canonical_url"]))
    for index, candidate in enumerate(deduplicated, start=1):
        candidate["candidate_id"] = f"FD06-C{index:04d}"

    exclusions.sort(key=lambda item: (item.get("primary_subcategory") or "99", item["name"].casefold(), item["discovery_url"]))
    OUTPUT.write_text(json.dumps(deduplicated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    EXCLUSIONS.write_text(json.dumps(exclusions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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
