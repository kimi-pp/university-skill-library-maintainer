from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class MonkeyPatch:
    """Small standard-library replacement for the fixture this module needs."""

    def __init__(self):
        self._changes: list[tuple[object, str, object]] = []

    def setattr(self, target: object, name: str, value: object) -> None:
        self._changes.append((target, name, getattr(target, name)))
        setattr(target, name, value)

    def undo(self) -> None:
        for target, name, original in reversed(self._changes):
            setattr(target, name, original)


def _run_function_test(function) -> None:
    patcher = MonkeyPatch()
    try:
        with tempfile.TemporaryDirectory() as temporary:
            fixtures = {"monkeypatch": patcher, "tmp_path": Path(temporary)}
            kwargs = {
                name: fixtures[name]
                for name in inspect.signature(function).parameters
            }
            function(**kwargs)
    finally:
        patcher.undo()


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            suite.addTest(unittest.FunctionTestCase(
                lambda function=function: _run_function_test(function),
                description=name,
            ))
    return suite


def load_script(name: str):
    path = ROOT / "06_过程记录" / name
    spec = importlib.util.spec_from_file_location(name.removesuffix(".py"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def version_payload(files: list[dict], license_name: str = "MIT-0") -> dict:
    return {
        "skill": {"slug": "uplo-education", "displayName": "Uplo Education"},
        "version": {
            "version": "1.0.0",
            "license": license_name,
            "files": files,
        },
    }


def test_pin_clawhub_uses_declared_version_and_skill_body_hash(monkeypatch):
    # Break caught: accepting a mutable latest page instead of the requested version,
    # or failing to bind deduplication to the exact SKILL.md body.
    module = load_script("fd06_deduplicate.py")
    skill = b"---\nname: uplo-education\n---\n\n# Uplo Education\nFixed body.\n"
    files = [
        {
            "path": "SKILL.md",
            "size": len(skill),
            "sha256": hashlib.sha256(skill).hexdigest(),
            "contentType": "text/markdown",
        }
    ]

    def fake_fetch(url: str) -> str:
        if url.endswith("/api/v1/skills/uplo-education/versions/1.0.0"):
            return json.dumps(version_payload(files))
        raise AssertionError(f"unexpected URL: {url}")

    def fake_bytes(url: str) -> bytes:
        assert "preview=" not in url
        if (
            "/api/v1/skills/uplo-education/file?" in url
            and "path=SKILL.md" in url
            and "version=1.0.0" in url
        ):
            return skill
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(module, "fetch_text", fake_fetch)
    monkeypatch.setattr(module, "fetch_bytes", fake_bytes)
    record = {
        "title": "Uplo Education",
        "proposed_subcategory": "06-10",
        "claimed_function": "课程质量与机构知识审查。",
        "query": "public versioned education skill registry",
        "discovery_url": "https://hub.openclaw.ai/roojenkins/skills/uplo-education",
        "source_path": "clawhub_skill",
        "fixed_version_hint": "1.0.0",
        "owner_hint": "roojenkins",
    }

    candidate, failed = module.pin_clawhub(record)

    assert failed is None
    assert candidate["source_kind"] == "clawhub_registry"
    assert candidate["repository"] == "clawhub.ai/roojenkins/uplo-education"
    assert candidate["fixed_version"] == "1.0.0"
    assert candidate["body_sha256"] == hashlib.sha256(b"# Uplo Education\nFixed body.").hexdigest()
    assert candidate["declared_license"] == "MIT-0"


def test_pin_clawhub_hashes_exact_utf8_bom_and_crlf_bytes(monkeypatch):
    # Break caught: a valid registry file being rejected because the downloader
    # decoded UTF-8 BOM/CRLF text and then re-encoded changed bytes for hashing.
    module = load_script("fd06_deduplicate.py")
    skill = b"\xef\xbb\xbf---\r\nname: thesis-review\r\n---\r\n\r\n# Thesis Review\r\n"
    files = [
        {
            "path": "SKILL.md",
            "size": len(skill),
            "sha256": hashlib.sha256(skill).hexdigest(),
            "contentType": "text/markdown",
        }
    ]

    monkeypatch.setattr(
        module,
        "fetch_text",
        lambda url: json.dumps(
            {
                "skill": {"slug": "thesis-review", "displayName": "Thesis Review"},
                "version": {"version": "2.1.0", "license": "MIT-0", "files": files},
            }
        ),
    )
    def exact_bytes(url: str) -> bytes:
        assert "preview=" not in url
        return skill

    monkeypatch.setattr(module, "fetch_bytes", exact_bytes)
    record = {
        "title": "Thesis Review",
        "proposed_subcategory": "06-11",
        "claimed_function": "高校学位论文评审。",
        "query": "thesis review",
        "discovery_url": "https://clawhub.ai/paudyyin/skills/thesis-review",
        "source_path": "clawhub_skill",
        "fixed_version_hint": "2.1.0",
        "owner_hint": "paudyyin",
    }

    candidate, failed = module.pin_clawhub(record)

    assert failed is None
    assert candidate["fixed_version"] == "2.1.0"
    assert candidate["content_sha256"] == hashlib.sha256(
        b"---\nname: thesis-review\n---\n\n# Thesis Review\n"
    ).hexdigest()


def test_clawhub_snapshot_reads_every_declared_file_and_checks_hashes(monkeypatch, tmp_path):
    # Break caught: scanning only the visible SKILL.md while ignoring a manifest file,
    # or saving content whose digest does not match the versioned registry declaration.
    module = load_script("fd06_snapshot_and_audit.py")
    skill = b"---\nname: uplo-education\n---\n# Uplo\n"
    manifest = b'{"endpoint":"https://approved.example/mcp"}\n'
    files = [
        {"path": "SKILL.md", "size": len(skill), "sha256": hashlib.sha256(skill).hexdigest(), "contentType": "text/markdown"},
        {"path": "skill.json", "size": len(manifest), "sha256": hashlib.sha256(manifest).hexdigest(), "contentType": "application/json"},
    ]

    def fake_bytes(url: str, allow_missing: bool = False):
        if url.endswith("/api/v1/skills/uplo-education/versions/1.0.0"):
            return json.dumps(version_payload(files)).encode()
        if "/api/v1/skills/uplo-education/file?" not in url:
            raise AssertionError(f"unexpected URL: {url}")
        assert "preview=" not in url
        if "path=SKILL.md" in url:
            return skill
        if "path=skill.json" in url:
            return manifest
        raise AssertionError(f"unexpected URL: {url}")

    snapshot_root = tmp_path / "snapshots"
    monkeypatch.setattr(module, "url_bytes", fake_bytes)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "SNAPSHOT_ROOT", snapshot_root)
    candidate = {
        "candidate_id": "FD06-C9999",
        "name": "Uplo Education",
        "repository": "clawhub.ai/roojenkins/uplo-education",
        "registry_owner": "roojenkins",
        "registry_slug": "uplo-education",
        "fixed_version": "1.0.0",
        "skill_path": "SKILL.md",
    }

    metadata, downloaded, package_manifest, license_info = module.clawhub_skill_snapshot(candidate)

    assert metadata["version"]["version"] == "1.0.0"
    assert [item.path for item in downloaded] == ["SKILL.md", "skill.json"]
    assert [item["path"] for item in package_manifest] == ["SKILL.md", "skill.json"]
    assert license_info == {
        "name": "MIT-0",
        "usable": True,
        "evidence_paths": [
            "snapshots/repositories/clawhub__roojenkins__uplo-education/1.0.0/version_metadata.json"
        ],
    }


def test_clawhub_snapshot_rejects_content_that_breaks_declared_hash(monkeypatch, tmp_path):
    # Break caught: treating a registry response as fixed-version evidence even when
    # the downloaded bytes do not match the registry's declared SHA-256.
    module = load_script("fd06_snapshot_and_audit.py")
    declared = b"expected\n"
    files = [
        {"path": "SKILL.md", "size": len(declared), "sha256": hashlib.sha256(declared).hexdigest(), "contentType": "text/markdown"}
    ]

    def fake_bytes(url: str, allow_missing: bool = False):
        if url.endswith("/api/v1/skills/uplo-education/versions/1.0.0"):
            return json.dumps(version_payload(files)).encode()
        return b"tampered\n"

    monkeypatch.setattr(module, "url_bytes", fake_bytes)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "SNAPSHOT_ROOT", tmp_path / "snapshots")
    candidate = {
        "candidate_id": "FD06-C9999",
        "name": "Uplo Education",
        "repository": "clawhub.ai/roojenkins/uplo-education",
        "registry_owner": "roojenkins",
        "registry_slug": "uplo-education",
        "fixed_version": "1.0.0",
        "skill_path": "SKILL.md",
    }

    with unittest.TestCase().assertRaisesRegex(ValueError, "SHA-256"):
        module.clawhub_skill_snapshot(candidate)


def test_audit_main_accepts_clawhub_registry_candidate(monkeypatch, tmp_path):
    # Break caught: a correctly pinned registry candidate being rejected by the
    # audit dispatcher or omitted from the final audit JSON.
    module = load_script("fd06_snapshot_and_audit.py")
    candidate = {
        "candidate_id": "FD06-C9999",
        "name": "Uplo Education",
        "primary_subcategory": "06-10",
        "source_kind": "clawhub_registry",
        "source_shape": "registry_skill",
        "repository": "clawhub.ai/roojenkins/uplo-education",
        "registry_owner": "roojenkins",
        "registry_slug": "uplo-education",
        "skill_path": "SKILL.md",
        "fixed_version": "1.0.0",
        "canonical_url": "https://clawhub.ai/roojenkins/skills/uplo-education?version=1.0.0",
        "declared_license": "MIT-0",
    }
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps([candidate]), encoding="utf-8")
    entry_path = tmp_path / "source" / "SKILL.md"
    entry_path.parent.mkdir(parents=True)
    entry_path.write_text("# Uplo\nUse a remote API token for student records.\n", encoding="utf-8")
    downloaded = [
        module.DownloadedFile(
            path="SKILL.md",
            size=entry_path.stat().st_size,
            local_path=entry_path,
            text=entry_path.read_text(encoding="utf-8"),
        )
    ]

    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "INPUT", input_path)
    monkeypatch.setattr(module, "SNAPSHOT_ROOT", tmp_path / "snapshots")
    monkeypatch.setattr(module, "AUDIT_DIR", tmp_path / "audit")
    monkeypatch.setattr(module, "AUDIT_JSON", tmp_path / "audit" / "audit.json")
    monkeypatch.setattr(module, "AUDIT_MD", tmp_path / "audit" / "audit.md")
    monkeypatch.setattr(module, "AUDIT_EXCLUSIONS_MD", tmp_path / "audit" / "excluded.md")
    monkeypatch.setattr(module, "INDEX_MD", tmp_path / "index" / "index.md")
    monkeypatch.setattr(module, "OVERRIDES", tmp_path / "missing-overrides.json")
    monkeypatch.setattr(
        module,
        "clawhub_skill_snapshot",
        lambda item: (
            {"skill": {"displayName": "Uplo Education"}, "version": {"createdAt": 1}},
            downloaded,
            [{"path": "SKILL.md", "size": entry_path.stat().st_size}],
            {"name": "MIT-0", "usable": True, "evidence_paths": ["source/version_metadata.json"]},
        ),
    )

    assert module.main() == 0
    records = json.loads(module.AUDIT_JSON.read_text(encoding="utf-8"))
    assert len(records) == 1
    assert records[0]["candidate_id"] == "FD06-C9999"
    assert records[0]["source_kind"] == "clawhub_registry"
    assert records[0]["license"] == "MIT-0"
    assert records[0]["read_errors"] == []


def test_static_scan_recognizes_remote_mcp_config_and_governance_writebacks():
    # Break caught: treating an MCP package as offline/read-only when its JSON
    # explicitly declares HTTP transport, one-shot npx installation, and tools
    # that change institutional knowledge-governance state.
    module = load_script("fd06_snapshot_and_audit.py")
    text = """
    {
      "command": "npx",
      "args": ["-y", "@agentdocs1/mcp-server", "--http"],
      "transport": "http",
      "url": "${config.agentdocs_url}/mcp",
      "tools": ["propose_update", "flag_outdated", "log_conversation"]
    }
    """

    hits = module.match_patterns(text)

    assert "network" in hits
    assert "remote_install" in hits
    assert "external_write" in hits


def test_package_frontmatter_license_is_evidence_when_repository_license_is_unknown(monkeypatch, tmp_path):
    # Break caught: excluding a self-contained skill whose SKILL.md explicitly
    # declares a supported SPDX license merely because the repository-level API
    # cannot identify a license for the wider collection.
    module = load_script("fd06_snapshot_and_audit.py")
    entry_path = tmp_path / "SKILL.md"
    text = "---\nname: learning-analytics\nlicense: \"MIT\"\n---\n# Learning analytics\n"
    entry_path.write_text(text, encoding="utf-8")
    downloaded = [
        module.DownloadedFile(
            path="SKILL.md",
            size=entry_path.stat().st_size,
            local_path=entry_path,
            text=text,
        )
    ]
    monkeypatch.setattr(module, "ROOT", tmp_path)
    repo_license = {
        "name": "未声明或无法确认",
        "usable": False,
        "evidence_paths": ["repository/license_api.json"],
    }

    result = module.resolve_package_license(repo_license, downloaded)

    assert result == {
        "name": "MIT",
        "usable": True,
        "evidence_paths": ["SKILL.md", "repository/license_api.json"],
    }


def test_license_display_names_normalize_to_supported_spdx():
    module = load_script("fd06_snapshot_and_audit.py")
    for declared, expected in (
        ("MIT license", "MIT"),
        (
            "Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)",
            "CC-BY-NC-4.0",
        ),
    ):
        assert module.normalize_license_id(declared) == expected
        assert module.license_is_usable(module.normalize_license_id(declared))
