import importlib.util
import json
from pathlib import Path

import pytest


PROJECT = Path(__file__).resolve().parents[2]
RUN_ROOT = PROJECT / "06_过程记录" / "economics_2026-08-19"
CLIENTS_PATH = RUN_ROOT / "platform_clients.py"
DISCOVERY_PATH = RUN_ROOT / "discover_economics.py"
VERIFY_PATH = RUN_ROOT / "verify_discovery.py"


def load_module(path: Path, name: str):
    assert path.is_file(), f"missing implementation: {path.name}"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, payload, headers=None, status_code=200):
        self._payload = payload
        self.headers = headers or {}
        self.status_code = status_code
        self.content = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.urls = []

    def get(self, url, timeout=None, headers=None):
        self.urls.append(url)
        assert self.responses, "unexpected request"
        return self.responses.pop(0)


def test_skillhub_reads_until_reported_last_page():
    clients = load_module(CLIENTS_PATH, "economics_platform_clients")
    session = FakeSession(
        [
            FakeResponse({"code": 0, "data": {"total": 3, "skills": [{"id": 1}, {"id": 2}]}}),
            FakeResponse({"code": 0, "data": {"total": 3, "skills": [{"id": 3}]}}),
        ]
    )
    rows, ledger = clients.skillhub_search("econometrics skill", session, page_size=2)
    assert [row["id"] for row in rows] == [1, 2, 3]
    assert [row["page"] for row in ledger] == [1, 2]
    assert ledger[-1]["is_last_page"] is True
    assert all(row["response_sha256"] for row in ledger)


def test_clawhub_and_huggingface_preserve_pagination_metadata():
    clients = load_module(CLIENTS_PATH, "economics_platform_clients")
    claw_session = FakeSession([FakeResponse({"results": [{"slug": "macro-agent"}]})])
    claw_rows, claw_ledger = clients.clawhub_search("macroeconomics", claw_session)
    assert claw_rows[0]["slug"] == "macro-agent"
    assert claw_ledger[0]["page"] == 1
    assert claw_ledger[0]["item_count"] == 1
    assert claw_ledger[0]["is_last_page"] is True

    hf_session = FakeSession(
        [
            FakeResponse([{"id": "one"}, {"id": "two"}]),
            FakeResponse([{"id": "three"}]),
        ]
    )
    hf_rows, hf_ledger = clients.huggingface_search("economic analysis", hf_session, page_size=2)
    assert [row["id"] for row in hf_rows] == ["one", "two", "three"]
    assert [row["page"] for row in hf_ledger] == [1, 2]
    assert "skip=2" in hf_session.urls[-1]


def test_github_uses_whole_encoded_query_as_one_argument_and_paginates():
    clients = load_module(CLIENTS_PATH, "economics_platform_clients")
    calls = []

    class Run:
        def __init__(self, payload):
            self.returncode = 0
            self.stdout = json.dumps(payload)
            self.stderr = ""

    payloads = [
        {"total_count": 2, "incomplete_results": False, "items": [{"path": "a/SKILL.md"}]},
        {"total_count": 2, "incomplete_results": False, "items": [{"path": "b/SKILL.md"}]},
    ]

    def runner(args):
        calls.append(args)
        return Run(payloads.pop(0))

    rows, ledger = clients.github_search("filename:SKILL.md 计量经济学", runner, page_size=1)
    assert len(rows) == 2
    assert len(ledger) == 2
    assert all(call[:4] == ["gh", "api", "--method", "GET"] for call in calls)
    assert all(len(call) == 5 for call in calls)
    assert "%E8%AE%A1" in calls[0][4]


def small_matrix():
    return {
        "jobs": [
            {
                "query_id": "ECON-020101-SH-R1-0001",
                "major_code": "020101",
                "major_name": "经济学",
                "class_code": "0201",
                "class_name": "经济学类",
                "platform": "SkillHub",
                "round": 1,
                "query": "economics skill",
                "term_types": ["structure"],
            }
        ]
    }


def test_discovery_resume_skips_only_successful_query_ids(tmp_path):
    discovery = load_module(DISCOVERY_PATH, "discover_economics")
    calls = []

    def fake_client(query):
        calls.append(query)
        return ([{"id": "candidate-1", "name": "Economics Helper"}], [{
            "page": 1,
            "item_count": 1,
            "is_last_page": True,
            "response_sha256": "a" * 64,
            "response_bytes": b"{}",
            "request_url": "https://example.test/search",
        }])

    clients = {"SkillHub": fake_client}
    first = discovery.run_discovery(small_matrix(), tmp_path, clients=clients)
    second = discovery.run_discovery(small_matrix(), tmp_path, clients=clients)
    assert first["network_calls"] == 1
    assert second["network_calls"] == 0
    assert calls == ["economics skill"]
    assert discovery.completed_query_ids(tmp_path / "query_ledger.jsonl") == {
        "ECON-020101-SH-R1-0001"
    }


def test_failed_query_is_recorded_as_failure_not_zero_results(tmp_path):
    discovery = load_module(DISCOVERY_PATH, "discover_economics")

    def failing_client(query):
        raise RuntimeError("query parsing fatal")

    summary = discovery.run_discovery(
        small_matrix(), tmp_path, clients={"SkillHub": failing_client}
    )
    assert summary["failed_jobs"] == 1
    ledger = [
        json.loads(line)
        for line in (tmp_path / "query_ledger.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    terminal = [row for row in ledger if row["event_type"] == "terminal"]
    assert terminal[0]["status"] == "failed"
    assert terminal[0]["complete"] is False
    assert terminal[0]["result_count"] is None
    assert "query parsing fatal" in terminal[0]["error"]


def test_verifier_accepts_complete_latest_terminal_and_response_hashes(tmp_path):
    discovery = load_module(DISCOVERY_PATH, "discover_economics")
    verifier = load_module(VERIFY_PATH, "verify_economics_discovery")

    def fake_client(query):
        return ([{"id": "candidate-1"}], [{
            "page": 1,
            "item_count": 1,
            "is_last_page": True,
            "response_sha256": "ignored",
            "response_bytes": b'{"ok":true}',
            "request_url": "https://example.test/search",
        }])

    matrix = small_matrix()
    discovery.run_discovery(matrix, tmp_path, clients={"SkillHub": fake_client})
    result = verifier.verify_discovery(matrix, tmp_path)
    assert result["errors"] == []
    assert result["latest_success_count"] == 1
    assert result["historical_failed_attempts"] == 0


def test_verifier_rejects_missing_saved_response(tmp_path):
    discovery = load_module(DISCOVERY_PATH, "discover_economics")
    verifier = load_module(VERIFY_PATH, "verify_economics_discovery")

    def fake_client(query):
        return ([], [{
            "page": 1,
            "item_count": 0,
            "is_last_page": True,
            "response_sha256": "ignored",
            "response_bytes": b'{}',
            "request_url": "https://example.test/search",
        }])

    matrix = small_matrix()
    discovery.run_discovery(matrix, tmp_path, clients={"SkillHub": fake_client})
    response = next((tmp_path / "raw_responses").rglob("page_*.json"))
    response.unlink()
    result = verifier.verify_discovery(matrix, tmp_path)
    assert any("响应文件缺失" in error for error in result["errors"])
