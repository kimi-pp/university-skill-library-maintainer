"""只读抓取分类 04/05 候选的 GitHub 说明、仓库元数据和包结构摘要。"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "03_候选池" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


CANDIDATES = {
    "04": [
        ("Tibsfox/gsd-skill-creator", "examples/skills/reading/information-literacy/SKILL.md"),
        ("Tibsfox/gsd-skill-creator", "examples/skills/digital-literacy/information-evaluation/SKILL.md"),
        ("Tibsfox/gsd-skill-creator", "examples/skills/communication/media-literacy/SKILL.md"),
        ("Tibsfox/gsd-skill-creator", "examples/skills/history/source-analysis/SKILL.md"),
        ("AhmedAnwar-Gazy/latex_templet", ".agents/skills/research-information-literacy/SKILL.md"),
        ("lionelsimai/claude-skills-collection", "skills/digital-library-plan/SKILL.md"),
        ("lionelsimai/claude-skills-collection", "skills/library-outreach-plan/SKILL.md"),
        ("lionelsimai/claude-skills-collection", "skills/library-program-design/SKILL.md"),
        ("lionelsimai/claude-skills-collection", "skills/library-technology-plan/SKILL.md"),
        ("lionelsimai/claude-skills-collection", "skills/media-literacy-program/SKILL.md"),
        ("lionelsimai/claude-skills-collection", "skills/fact-checking-protocol/SKILL.md"),
        ("lionelsimai/claude-skills-collection", "skills/data-literacy-program/SKILL.md"),
        ("lionelsimai/claude-skills-collection", "skills/source-management/SKILL.md"),
        ("ASI2030/Fact-Check-X", "skills/fact-check-x-unified/SKILL.md"),
        ("ASI2030/Fact-Check-X", "skills/fact-check-x-authoritative-verify/SKILL.md"),
        ("SamaritanOC/fact-checker", "SKILL.md"),
        ("wentorai/research-plugins", "skills/literature/fulltext/institutional-repository-guide/SKILL.md"),
        ("wentorai/research-plugins", "skills/literature/search/worldcat-search-api/SKILL.md"),
        ("wentorai/research-plugins", "skills/research/funding/open-science-guide/SKILL.md"),
        ("wentorai/research-plugins", "skills/tools/scraping/repository-harvesting-guide/SKILL.md"),
        ("wentorai/research-plugins", "skills/research/funding/figshare-api/SKILL.md"),
        ("wentorai/research-plugins", "skills/literature/fulltext/pmc-oai-api/SKILL.md"),
        ("wu-yc/LabClaw", "skills/general/fair-data/SKILL.md"),
        ("scdenney/open-science-skills", "codex/fair-check/SKILL.md"),
        ("dandye/ai-runbooks", "skills/design-metadata-schema/SKILL.md"),
        ("Albert-Libra/nanobot-zotero-bridge", "SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/ontology-term-resolution/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/labarchive-integration/SKILL.md"),
        ("zotero/translators", ".agent/skills/develop-web-translator/SKILL.md"),
    ],
    "05": [
        ("K-Dense-AI/scientific-agent-skills", "skills/get-available-resources/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/exploratory-data-analysis/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/dask/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/polars/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/vaex/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/zarr-python/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/matplotlib/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/seaborn/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/scientific-visualization/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/networkx/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/geopandas/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/scikit-learn/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/statistical-analysis/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/statistical-power/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/statsmodels/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/pymc/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/sympy/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/uncertainty-and-units/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/shap/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/umap-learn/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/timesfm-forecasting/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/matlab/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/simpy/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/optimize-for-gpu/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/pymoo/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/pytorch-lightning/SKILL.md"),
        ("K-Dense-AI/scientific-agent-skills", "skills/transformers/SKILL.md"),
        ("obra/superpowers", "skills/systematic-debugging/SKILL.md"),
        ("obra/superpowers", "skills/test-driven-development/SKILL.md"),
        ("obra/superpowers", "skills/requesting-code-review/SKILL.md"),
        ("obra/superpowers", "skills/receiving-code-review/SKILL.md"),
        ("wshobson/agents", "plugins/business-analytics/skills/data-storytelling/SKILL.md"),
        ("wshobson/agents", "plugins/database-design/skills/postgresql/SKILL.md"),
        ("wshobson/agents", "plugins/data-engineering/skills/data-quality-frameworks/SKILL.md"),
        ("wshobson/agents", "plugins/data-engineering/skills/dbt-transformation-patterns/SKILL.md"),
        ("wshobson/agents", "plugins/data-engineering/skills/spark-optimization/SKILL.md"),
        ("wshobson/agents", "plugins/developer-essentials/skills/sql-optimization-patterns/SKILL.md"),
        ("wshobson/agents", "plugins/machine-learning-ops/skills/ml-pipeline-workflow/SKILL.md"),
        ("wshobson/agents", "plugins/python-development/skills/python-testing-patterns/SKILL.md"),
        ("wshobson/agents", "plugins/python-development/skills/python-code-style/SKILL.md"),
        ("wshobson/agents", "plugins/python-development/skills/python-error-handling/SKILL.md"),
        ("wshobson/agents", "plugins/python-development/skills/python-project-structure/SKILL.md"),
        ("wshobson/agents", "plugins/python-development/skills/python-performance-optimization/SKILL.md"),
        ("wshobson/agents", "plugins/python-development/skills/async-python-patterns/SKILL.md"),
        ("wshobson/agents", "plugins/javascript-typescript/skills/javascript-testing-patterns/SKILL.md"),
        ("markdown-viewer/skills", "data-analytics/SKILL.md"),
        ("markdown-viewer/skills", "vega/SKILL.md"),
        ("markdown-viewer/skills", "graphviz/SKILL.md"),
        ("leanprover/skills", "skills/lean-proof/SKILL.md"),
        ("leanprover/skills", "skills/mathlib-review/SKILL.md"),
        ("lyndonkl/claude", "skills/bayesian-reasoning-calibration/SKILL.md"),
        ("lyndonkl/claude", "skills/causal-inference-root-cause/SKILL.md"),
        ("lyndonkl/claude", "skills/design-of-experiments/SKILL.md"),
        ("lyndonkl/claude", "skills/visualization-choice-reporting/SKILL.md"),
        ("lyndonkl/claude", "skills/d3-visualization/SKILL.md"),
    ],
}


def run_gh(*args: str) -> str:
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False
    )
    if result.returncode:
        raise RuntimeError(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def parse_frontmatter(text: str) -> tuple[str, str]:
    name = ""
    description = ""
    match = re.match(r"^---\s*\n(.*?)\n---", text, flags=re.DOTALL)
    if match:
        block = match.group(1)
        name_match = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", block)
        description_match = re.search(r"(?ms)^description:\s*[|>]?\s*(.*?)(?=\n\w[\w-]*:\s|\Z)", block)
        if name_match:
            name = name_match.group(1).strip()
        if description_match:
            description = " ".join(description_match.group(1).split())
    return name, description


def main() -> None:
    repo_meta: dict[str, dict] = {}
    repo_trees: dict[str, list[dict]] = {}

    for category, candidates in CANDIDATES.items():
        records = []
        for repo, path in candidates:
            if repo not in repo_meta:
                meta = json.loads(run_gh("api", f"repos/{repo}"))
                branch = meta["default_branch"]
                tree = json.loads(run_gh("api", f"repos/{repo}/git/trees/{branch}?recursive=1"))["tree"]
                repo_meta[repo] = {
                    "stars": meta["stargazers_count"],
                    "pushed": meta["pushed_at"][:10],
                    "license": (meta.get("license") or {}).get("spdx_id") or "未明确",
                    "branch": branch,
                    "description": meta.get("description") or "",
                    "archived": bool(meta.get("archived")),
                }
                repo_trees[repo] = tree

            branch = repo_meta[repo]["branch"]
            encoded_path = quote(path, safe="/")
            text = run_gh(
                "api",
                f"repos/{repo}/contents/{encoded_path}?ref={branch}",
                "-H",
                "Accept: application/vnd.github.raw+json",
            )
            name, description = parse_frontmatter(text)
            prefix = path.rsplit("/", 1)[0] + "/" if "/" in path else ""
            files = [item["path"] for item in repo_trees[repo] if item.get("type") == "blob" and item["path"].startswith(prefix)]
            scoped_files = files if prefix else [item["path"] for item in repo_trees[repo] if item.get("type") == "blob"]
            records.append(
                {
                    "category": category,
                    "repo": repo,
                    "path": path,
                    "skill_url": f"https://github.com/{repo}/blob/{branch}/{path}",
                    "repo_url": f"https://github.com/{repo}",
                    "name": name or Path(path).parent.name or repo.rsplit("/", 1)[-1],
                    "description": description,
                    "line_count": len(text.splitlines()),
                    "char_count": len(text),
                    "headings": re.findall(r"(?m)^#{1,3}\s+(.+)$", text)[:20],
                    "package_files": len(scoped_files),
                    "script_files": sum("/scripts/" in f"/{item}" for item in scoped_files),
                    "reference_asset_files": sum(
                        any(part in f"/{item}" for part in ("/references/", "/assets/", "/templates/"))
                        for item in scoped_files
                    ),
                    **repo_meta[repo],
                }
            )

        output = RAW_DIR / f"2026-08-06-category-{category}-github.jsonl"
        output.write_text(
            "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records), encoding="utf-8"
        )
        print(f"category {category}: {len(records)} candidates -> {output}")

    (RAW_DIR / "2026-08-06-category-04-05-repositories.json").write_text(
        json.dumps(repo_meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"repositories: {len(repo_meta)}")


if __name__ == "__main__":
    main()
