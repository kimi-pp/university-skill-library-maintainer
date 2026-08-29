"""Task 14: production discovery, trusted material review, and E2E acceptance."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from skill_maintainer import cli
from skill_maintainer.catalog import Catalog, CatalogRow, CatalogSourceStatus, TaskProfile, diff_catalog
from skill_maintainer.dedup import deduplicate
from skill_maintainer.import_existing import ImportInventory, ImportedRecord, build_initial_ledger
from skill_maintainer.ledger import LedgerStore
from skill_maintainer.ledger_schema import CURRENT_SKILL_COLUMNS
from skill_maintainer.reports import make_project_report_builder
from skill_maintainer.production import (
    MaterialReviewError,
    NetworkSmokeEntry,
    NetworkSmokeReport,
    ProductionDriver,
    build_production_driver,
    run_network_smoke,
)
from skill_maintainer.queries import PLATFORM_ORDER, QueryJob
from skill_maintainer.runner import RunCoordinator, RunRequest, SourceRun
from skill_maintainer.runner import ReviewApplySummary, RunSummary
from skill_maintainer.review import DerivedFields, ObservedFacts, ProjectJudgments, ReviewDecision, build_review_packet
from skill_maintainer.snapshots import SnapshotCandidate, build_snapshot
from skill_maintainer.sources.base import (
    DoctorSmokeResult,
    SearchBatch,
    SnapshotResult,
    SourceCandidate,
    SourceError,
    SourceRequestEvent,
    VersionObservation,
)


WORKFLOW = "07_自动维护工作流"
FIXTURES = Path(__file__).parent / "fixtures" / "e2e"


class _Adapter:
    """Complete offline source boundary; candidate package content is never executed."""

    def __init__(self, platform: str, candidates: tuple[SourceCandidate, ...], package: Path | None = None) -> None:
        self.platform = platform
        self.candidates = candidates
        self.package = package
        self.search_calls: list[tuple[QueryJob, object]] = []
        self.latest_calls: list[str] = []
        self.snapshot_calls: list[tuple[str, str | None, Path]] = []

    def search(self, job: QueryJob, watermark):
        self.search_calls.append((job, watermark))
        body = json.dumps({"platform": self.platform, "query": job.query}, ensure_ascii=False).encode()
        event = SourceRequestEvent(
            self.platform, job.query_id, f"https://fixture.invalid/{self.platform}/{len(self.search_calls)}",
            1, 200, 1, sha256(body).hexdigest(), body, True, None, True,
        )
        return SearchBatch(self.platform, job, "complete", self.candidates, (event,), ())

    def latest_version(self, identity: str):
        self.latest_calls.append(identity)
        return VersionObservation(self.platform, identity, "a" * 40, datetime(2026, 8, 29, tzinfo=timezone.utc), "b" * 64)

    def snapshot(self, identity: str, version: str | None, destination: Path):
        self.snapshot_calls.append((identity, version, destination))
        if self.package is None:
            return SnapshotResult(self.platform, identity, version, destination, None, error=object())
        shutil.make_archive(str(destination.with_suffix("")), "zip", self.package)
        archive = destination.with_suffix(".zip")
        return SnapshotResult(self.platform, identity, version, archive, sha256(archive.read_bytes()).hexdigest())


class _FailedSearchAdapter(_Adapter):
    def search(self, job: QueryJob, watermark):
        self.search_calls.append((job, watermark))
        return SearchBatch(self.platform, job, "failed", (), (), ())


class _DeletedGithubAdapter(_Adapter):
    def latest_version(self, identity: str):
        self.latest_calls.append(identity)
        return VersionObservation(
            self.platform, identity, None, datetime(2026, 8, 29, tzinfo=timezone.utc), None,
            SourceError(self.platform, "latest-version", "not found", 404, identity),
        )


class _ScenarioGithubAdapter(_Adapter):
    def __init__(self, candidates, package, versions, deleted):
        super().__init__("GitHub", candidates, package)
        self.versions = dict(versions)
        self.deleted = set(deleted)

    def latest_version(self, identity: str):
        self.latest_calls.append(identity)
        if identity in self.deleted:
            return VersionObservation(
                self.platform, identity, None, datetime(2026, 8, 29, tzinfo=timezone.utc), None,
                SourceError(self.platform, "latest-version", "not found", 404, identity),
            )
        return VersionObservation(
            self.platform, identity, self.versions[identity], datetime(2026, 8, 29, tzinfo=timezone.utc), "b" * 64,
        )


def _candidate(platform: str, native: str, discovery: str, canonical: str | None) -> SourceCandidate:
    return SourceCandidate(
        platform=platform,
        native_id=native,
        discovery_url=discovery,
        canonical_source_hint=canonical,
        version_hint=None,
        display_name="经济数据整理",
        publisher="fixture",
        updated_at="2026-08-29T00:00:00Z",
        popularity={},
        query_id="fixture-query",
        response_evidence_sha256="c" * 64,
    )


class ProductionDriverContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name) / "中文 项目"
        self.workflow = self.project / WORKFLOW
        self.workflow.mkdir(parents=True)
        self.settings = self.workflow / "workflow-settings.toml"
        self.settings.write_text(
            """config_version = 1
[workflow]
enabled = false
timezone = "Asia/Shanghai"
[schedule]
mode = "manual"
start_time = "22:00"
weekdays = ["Monday"]
interval_days = 1
day_of_month = 1
[research]
incremental_search = true
full_recheck_interval_days = 7
check_existing_skill_updates = true
include_generic_skills = true
[delivery]
generate_word = true
generate_excel = true
only_refresh_affected_classes = true
notify_on_no_change = false
""",
            encoding="utf-8",
        )
        (self.workflow / "ledger").mkdir()
        ledger = LedgerStore.create(self.workflow / "ledger" / "Skills主台账.xlsx")
        ledger.append_rows("专业任务映射", [{
            "映射标识": "profile-0201", "内部标识": "PROFILE-0201", "专业代码": "0201", "专业名称": "经济学类",
            "专业任务": "整理经济统计数据", "输入": "公开统计表", "输出": "字段字典", "适用理由": "支持实证研究准备",
            "使用限制": "需要研究者复核", "相关度": 5, "专业别名": "economics", "核心课程": "计量经济学",
            "研究方法": "描述性统计", "工作任务": "数据清洗", "成果或数据对象": "统计表",
            "软件/数据库/流程": "R；Stata；数据质量检查",
        }])
        ledger.save_staged(self.workflow / "ledger" / "initial.xlsx")
        shutil.move(self.workflow / "ledger" / "initial.xlsx", self.workflow / "ledger" / "Skills主台账.xlsx")

    def _catalog(self) -> Catalog:
        row = CatalogRow("02", "经济学", "0201", "经济学类", "020101", "经济学")
        profile = TaskProfile(
            professional_aliases=("economics",), core_courses=("计量经济学",), methods=("描述性统计",),
            work_tasks=("数据清洗",), outputs_and_data=("统计表",), software_databases_processes=("Stata",),
        )
        return Catalog((row,), {"0201": profile, "99": profile})

    def _driver(self) -> tuple[ProductionDriver, dict[str, _Adapter]]:
        upstream = "https://github.com/example/economic-data-skill"
        adapters = {
            "SkillHub": _Adapter("SkillHub", (_candidate("SkillHub", "market-1", "https://skillhub.cn/skills/market-1", upstream),)),
            "ClawHub": _Adapter("ClawHub", (_candidate("ClawHub", "mirror-1", "https://clawhub.ai/skills/mirror-1", upstream),)),
            "GitHub": _Adapter("GitHub", (_candidate("GitHub", "example/economic-data-skill", upstream, upstream),), FIXTURES / "fixed-package"),
            "Hugging Face Spaces": _Adapter("Hugging Face Spaces", (_candidate("Hugging Face Spaces", "example/demo", "https://huggingface.co/spaces/example/demo", None),)),
        }
        return ProductionDriver(
            project_root=self.project,
            adapters=adapters,
            catalog_loader=self._catalog,
            now=lambda: datetime(2026, 8, 29, tzinfo=timezone.utc),
        ), adapters

    def _append_existing(self, *, canonical: str) -> None:
        ledger_path = self.workflow / "ledger" / "Skills主台账.xlsx"
        ledger = LedgerStore.load(ledger_path)
        row = {column: "已核验" for column in CURRENT_SKILL_COLUMNS}
        row.update({
            "内部标识": "SK-TRACKED", "Skill名称": "tracked", "规范名称": "已跟踪技能", "入库层级": "正式",
            "来源平台": "GitHub", "发现地址": canonical, "Canonical source": canonical,
            "上游项目地址": canonical, "Skill入口路径": "SKILL.md", "固定版本": "1" * 40,
            "固定版本内容指纹": "2" * 64, "许可证": "MIT", "外部联网/API 调用": "否",
            "远程服务端点": "", "安全等级": "SA", "验证状态": "全部通过（未实测）", "质量评分": 3,
        })
        ledger.append_rows("当前Skill", [row])
        staged = ledger_path.with_name("tracked-seed.xlsx")
        ledger.save_staged(staged)
        shutil.copyfile(staged, ledger_path)
        staged.unlink()

    def test_discovery_uses_six_dimensions_fixed_platform_order_and_one_global_identity(self):
        driver, adapters = self._driver()
        staging = self.workflow / ".runtime" / "staging" / "run-red"
        staging.mkdir(parents=True)
        request = RunRequest(settings_path=self.settings, catalog_loader=driver.load_catalog, discover=driver.discover)
        runs = tuple(driver.discover(request, staging))

        self.assertEqual(tuple(run.platform for run in runs), PLATFORM_ORDER)
        self.assertTrue(all(len(adapters[name].search_calls) == 12 for name in PLATFORM_ORDER))
        dimensions = {call[0].dimension for call in adapters["GitHub"].search_calls}
        self.assertEqual(dimensions, {
            "professional_alias", "core_course", "method", "work_task", "output_or_data", "software_database_or_process",
        })
        canonical_ids = {
            candidate["内部标识"]
            for run in runs for candidate in run.candidates
            if candidate.get("canonical_source") == "https://github.com/example/economic-data-skill"
        }
        self.assertEqual(len(canonical_ids), 1)
        self.assertEqual(len(driver.review_materials), 1)
        self.assertEqual(driver.review_materials[0].fixed_version, "a" * 40)
        self.assertTrue(driver.review_materials[0].snapshot_path.is_dir())
        self.assertTrue(any(item.reason_code == "fixed-package-unavailable" for item in driver.observations))
        self.assertEqual(len(adapters["GitHub"].snapshot_calls), 1, "cross-platform duplicate must snapshot one canonical upstream once")
        hf_candidate = next(candidate for run in runs if run.platform == "Hugging Face Spaces" for candidate in run.candidates)
        self.assertEqual(hf_candidate["observation_status"], "条件候选")
        self.assertEqual(hf_candidate["observation_reason_code"], "fixed-package-unavailable")
        github_run = next(run for run in runs if run.platform == "GitHub")
        self.assertTrue(any(path.suffix == ".zip" and path.is_file() for path in github_run.evidence_files))

    def test_material_gate_builds_trusted_packets_only_after_bound_observations(self):
        driver, _ = self._driver()
        staging = self.workflow / ".runtime" / "staging" / "run-material"
        staging.mkdir(parents=True)
        request = RunRequest(settings_path=self.settings, catalog_loader=driver.load_catalog, discover=driver.discover)
        runs = tuple(driver.discover(request, staging))
        prepared = type("Prepared", (), {"run_id": "run-material", "source_runs": runs})()

        output = io.StringIO()
        first = driver.material_review_frame(prepared)
        material = first["materials"][0]
        response = {
            "type": "material_observations", "run_id": "run-material", "observations": [{
                "candidate_id": material["candidate_id"], "fixed_version": material["fixed_version"],
                "fixed_content_hash": material["fixed_content_hash"], "canonical_source": material["canonical_source"],
                "license": "MIT", "security_grade": "SA",
            }],
        }
        packets = driver.apply_material_observations(prepared, response)
        self.assertEqual(set(packets), {material["candidate_id"]})
        self.assertEqual(packets[material["candidate_id"]].fixed_content_hash, material["fixed_content_hash"])
        with self.assertRaises(MaterialReviewError):
            driver.apply_material_observations(prepared, response)

    def test_one_failed_source_degrades_but_does_not_stop_later_sources(self):
        driver, adapters = self._driver()
        failed = _FailedSearchAdapter("SkillHub", ())
        driver.adapters["SkillHub"] = failed
        staging = self.workflow / ".runtime" / "staging" / "run-degraded"
        staging.mkdir(parents=True)
        request = RunRequest(settings_path=self.settings, catalog_loader=driver.load_catalog, discover=driver.discover)

        runs = tuple(driver.discover(request, staging))

        self.assertEqual([run.status for run in runs], ["failed", "complete", "complete", "complete"])
        self.assertEqual(len(adapters["GitHub"].search_calls), 12)
        self.assertEqual(len(driver.review_materials), 1)

    def test_existing_github_skill_is_checked_even_when_search_does_not_rediscover_it(self):
        canonical = "https://github.com/example/tracked"
        self._append_existing(canonical=canonical)
        adapters = {
            "SkillHub": _Adapter("SkillHub", ()),
            "ClawHub": _Adapter("ClawHub", ()),
            "GitHub": _DeletedGithubAdapter("GitHub", (), FIXTURES / "fixed-package"),
            "Hugging Face Spaces": _Adapter("Hugging Face Spaces", ()),
        }
        driver = ProductionDriver(
            project_root=self.project, adapters=adapters, catalog_loader=self._catalog,
            now=lambda: datetime(2026, 8, 29, tzinfo=timezone.utc),
        )
        staging = self.workflow / ".runtime" / "staging" / "run-deleted"
        staging.mkdir(parents=True)
        request = RunRequest(settings_path=self.settings, catalog_loader=driver.load_catalog, discover=driver.discover)

        runs = tuple(driver.discover(request, staging))

        self.assertEqual(adapters["GitHub"].latest_calls, [canonical])
        tracked = [candidate for run in runs for candidate in run.candidates if candidate.get("内部标识") == "SK-TRACKED"]
        self.assertEqual(len(tracked), 1)
        self.assertEqual(tracked[0]["observation_status"], "attention_required")
        self.assertEqual(tracked[0]["observation_reason_code"], "upstream-deleted")
        self.assertEqual(driver.review_materials, ())

    def test_production_factory_is_real_and_network_smoke_never_searches_or_writes(self):
        self.assertIs(cli.PRODUCTION_DRIVER_FACTORY, build_production_driver)
        calls: list[str] = []

        def smoke(platform: str) -> DoctorSmokeResult:
            calls.append(platform)
            return DoctorSmokeResult(platform, True, 1, 200)

        before = tuple(self.workflow.rglob("*"))
        result = run_network_smoke(
            platform_smoke=smoke,
            ministry_fetch=lambda url: (calls.append("教育部"), 200)[1],
            ministry_url="https://www.moe.gov.cn/catalog.pdf",
            now=lambda: datetime(2026, 8, 29, 1, 2, 3, tzinfo=timezone.utc),
        )
        self.assertEqual(calls, [*PLATFORM_ORDER, "教育部"])
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.checked_at, "2026-08-29T01:02:03+00:00")
        self.assertEqual(tuple(self.workflow.rglob("*")), before)

    def test_default_catalog_loader_verifies_official_bytes_against_excel_baseline(self):
        catalog_path = self.project / "06_过程记录" / "discipline_mapping" / "catalogs" / "undergraduate_2026.json"
        catalog_path.parent.mkdir(parents=True)
        shutil.copyfile(FIXTURES / "catalog.json", catalog_path)
        official = b"official-ministry-catalog-fixture"
        ledger_path = self.workflow / "ledger" / "Skills主台账.xlsx"
        ledger = LedgerStore.load(ledger_path)
        ledger.append_rows("目录基线", [{
            "目录版本": "2026", "目录名称": "本科专业目录", "公开地址": "https://www.moe.gov.cn/catalog.pdf",
            "SHA-256": sha256(official).hexdigest(), "发布日期": "2026-04-27", "访问日期": "2026-08-29",
        }])
        staged = ledger_path.with_name("catalog-baseline.xlsx")
        ledger.save_staged(staged)
        shutil.copyfile(staged, ledger_path)
        staged.unlink()
        fetched: list[str] = []
        driver = ProductionDriver(
            project_root=self.project,
            catalog_source_fetch=lambda url: (fetched.append(url), official)[1],
        )

        catalog = driver.load_catalog()

        self.assertEqual(fetched, ["https://www.moe.gov.cn/catalog.pdf"])
        self.assertIsNotNone(catalog.source_status)
        self.assertFalse(catalog.source_status.changed)
        self.assertEqual(catalog.source_status.actual_sha, sha256(official).hexdigest())


class _ProtocolMaterialReviewer:
    def __init__(self) -> None:
        self.applied = False

    def material_review_frame(self, prepared):
        return {
            "type": "material_review_required", "run_id": prepared.run_id,
            "materials": [], "observations": [{"candidate_id": "OBS-1", "reason_code": "fixed-package-unavailable"}],
        }

    def apply_material_observations(self, prepared, frame):
        if frame != {"type": "material_observations", "run_id": prepared.run_id, "observations": []}:
            raise AssertionError(frame)
        self.applied = True
        return {}


class _ProtocolCoordinator:
    def __init__(self) -> None:
        self.prepared = type("Prepared", (), {
            "run_id": "run-three-gate", "settings_sha256": "d" * 64,
            "source_runs": tuple(SourceRun(name, "complete") for name in PLATFORM_ORDER),
        })()
        self.bound = None
        self.abandoned = False

    def prepare(self, request):
        return self.prepared

    def bind_review_packets(self, prepared, packets):
        self.bound = dict(packets)

    def apply_reviews(self, prepared, decisions):
        return ReviewApplySummary(prepared.run_id, "e" * 64, 0, "f" * 64)

    def finalize(self, prepared, reviews):
        return RunSummary(prepared.run_id, False, {name: "complete" for name in PLATFORM_ORDER}, Path("ledger.xlsx"), Path("generation"))

    def abandon(self, prepared):
        self.abandoned = True


class _ThreeGateInput:
    def __init__(self, output: io.StringIO, *, eof_material: bool = False) -> None:
        self.output = output
        self.eof_material = eof_material

    def readline(self) -> str:
        frame = json.loads(self.output.getvalue().splitlines()[-1])
        if frame["type"] == "material_review_required":
            if self.eof_material:
                return ""
            return json.dumps({"type": "material_observations", "run_id": frame["run_id"], "observations": []}) + "\n"
        if frame["type"] == "review_required":
            return json.dumps({"type": "review_decisions", "run_id": frame["run_id"], "decisions": []}) + "\n"
        raise AssertionError(frame)


class ThreeGateProtocolTest(unittest.TestCase):
    def test_deployed_skill_and_prompt_describe_same_process_three_gate_contract(self):
        skill_root = Path(__file__).parents[1] / "skill" / "university-skill-library-maintainer"
        skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        contract = (skill_root / "references" / "project-contract.md").read_text(encoding="utf-8")
        prompt = (skill_root / "assets" / "automation-prompt.md").read_text(encoding="utf-8")
        for text_value in (skill, contract):
            self.assertIn("material_review_required", text_value)
            self.assertIn("material_observations", text_value)
            self.assertIn("同一长驻进程", text_value)
            self.assertIn("不得跨进程", text_value)
        self.assertIn("材料事实观察", prompt)
        self.assertIn("逐页视觉", prompt)
        self.assertNotIn("prepare` 只产生暂存台账、固定来源快照、评审包", contract)

    def test_protocol_binds_material_packets_before_project_decisions(self):
        coordinator = _ProtocolCoordinator()
        reviewer = _ProtocolMaterialReviewer()
        request = RunRequest(
            settings_path=Path("workflow-settings.toml"), catalog_loader=lambda: {}, material_reviewer=reviewer,
        )
        output = io.StringIO()
        code = cli.run_interactive_protocol(coordinator, request, input_stream=_ThreeGateInput(output), output_stream=output)
        self.assertEqual(code, 0, output.getvalue())
        self.assertTrue(reviewer.applied)
        self.assertEqual(coordinator.bound, {})
        self.assertEqual(
            [json.loads(line)["type"] for line in output.getvalue().splitlines()],
            ["material_review_required", "review_required", "run_complete"],
        )

    def test_protocol_eof_at_material_gate_abandons_live_capability(self):
        coordinator = _ProtocolCoordinator()
        request = RunRequest(
            settings_path=Path("workflow-settings.toml"), catalog_loader=lambda: {}, material_reviewer=_ProtocolMaterialReviewer(),
        )
        output = io.StringIO()
        code = cli.run_interactive_protocol(
            coordinator, request, input_stream=_ThreeGateInput(output, eof_material=True), output_stream=output,
        )
        self.assertEqual(code, 1)
        self.assertTrue(coordinator.abandoned)
        self.assertEqual(
            [json.loads(line)["type"] for line in output.getvalue().splitlines()],
            ["material_review_required", "run_failed"],
        )


class CliTask14BoundaryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name) / "CLI 中文 项目"
        self.workflow = self.project / WORKFLOW
        (self.workflow / "ledger").mkdir(parents=True)
        self.settings = self.workflow / "workflow-settings.toml"
        self.settings.write_text(
            """config_version = 1
[workflow]
enabled = false
timezone = "Asia/Shanghai"
[schedule]
mode = "manual"
start_time = "22:00"
weekdays = ["Monday"]
interval_days = 7
day_of_month = 1
[research]
incremental_search = true
full_recheck_interval_days = 7
check_existing_skill_updates = true
include_generic_skills = true
[delivery]
generate_word = true
generate_excel = true
only_refresh_affected_classes = true
notify_on_no_change = false
""",
            encoding="utf-8",
        )
        ledger = LedgerStore.create(self.workflow / "ledger" / "Skills主台账.xlsx")
        ledger.append_rows("目录基线", [{
            "目录版本": "2026", "目录名称": "本科专业目录", "公开地址": "https://www.moe.gov.cn/catalog.pdf",
            "SHA-256": "a" * 64, "发布日期": "2026-04-27", "访问日期": "2026-08-29",
        }])
        staged = self.workflow / "ledger" / "cli-seed.xlsx"
        ledger.save_staged(staged)
        shutil.copyfile(staged, self.workflow / "ledger" / "Skills主台账.xlsx")
        staged.unlink()

    def test_disabled_manual_scheduled_run_stops_before_factory_or_network(self):
        factory = unittest.mock.Mock(side_effect=AssertionError("factory must not run"))
        output = io.StringIO()
        with patch.object(cli, "PRODUCTION_DRIVER_FACTORY", factory), patch("sys.stdout", output):
            code = cli.main([
                "scheduled-run", "--project-root", str(self.project),
                "--expected-config-sha", sha256(self.settings.read_bytes()).hexdigest(),
            ])
        self.assertEqual(code, cli.SAFE_NOOP)
        self.assertEqual(factory.call_count, 0)
        self.assertEqual(json.loads(output.getvalue())["type"], "run_noop")

    def test_missing_loader_and_mismatched_scheduled_hash_stop_before_factory(self):
        factory = unittest.mock.Mock(side_effect=AssertionError("factory must not run"))
        output = io.StringIO()
        with patch.object(cli, "PRODUCTION_DRIVER_FACTORY", factory), patch("sys.stdout", output):
            run_now = cli.main(["run-now", "--project-root", str(self.project)])
            scheduled = cli.main([
                "scheduled-run", "--project-root", str(self.project),
                "--loader-output", "{}", "--expected-config-sha", "0" * 64,
            ])
        self.assertEqual((run_now, scheduled), (cli.OPERATIONAL_FAILURE, cli.INVALID_INPUT))
        self.assertEqual(factory.call_count, 0)

    def test_interval_dispatcher_not_due_stops_before_factory(self):
        text_value = self.settings.read_text(encoding="utf-8").replace("enabled = false", "enabled = true").replace('mode = "manual"', 'mode = "interval"')
        self.settings.write_text(text_value, encoding="utf-8")
        ledger_path = self.workflow / "ledger" / "Skills主台账.xlsx"
        ledger = LedgerStore.load(ledger_path)
        ledger.append_rows("运行记录", [{
            "运行标识": "run-recent-success", "运行类型": "维护",
            "开始时间": datetime.now(), "成功完成时间": datetime.now(),
            "状态": "成功", "摘要": "interval fixture", "快照SHA-256": "f" * 64,
        }])
        staged = ledger_path.with_name("interval-seed.xlsx")
        ledger.save_staged(staged)
        shutil.copyfile(staged, ledger_path)
        staged.unlink()
        factory = unittest.mock.Mock(side_effect=AssertionError("factory must not run"))
        output = io.StringIO()
        with patch.object(cli, "PRODUCTION_DRIVER_FACTORY", factory), patch("sys.stdout", output):
            code = cli.main([
                "scheduled-run", "--project-root", str(self.project), "--loader-output", "{}",
                "--expected-config-sha", sha256(self.settings.read_bytes()).hexdigest(),
            ])
        self.assertEqual(code, cli.SAFE_NOOP)
        self.assertIn("尚未到期", json.loads(output.getvalue())["reason"])
        self.assertEqual(factory.call_count, 0)

    def test_doctor_network_wires_five_read_only_probes_and_reports_partial_truthfully(self):
        local = cli.DoctorReport(cli.SUCCESS, True, {"local": "PASS"}, (), ())
        smoke = NetworkSmokeReport(
            "2026-08-29T01:02:03+00:00", "PARTIAL",
            (NetworkSmokeEntry("SkillHub", False, 1, 503, "http-503"),),
        )
        output = io.StringIO()
        with patch.object(cli, "doctor_project", return_value=local), \
             patch.object(cli, "run_network_smoke", return_value=smoke) as probe, \
             patch("sys.stdout", output):
            code = cli.main(["doctor", "--project-root", str(self.project), "--network"])
        self.assertEqual(code, cli.OPERATIONAL_FAILURE)
        probe.assert_called_once_with(ministry_url="https://www.moe.gov.cn/catalog.pdf")
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["network"]["status"], "PARTIAL")
        self.assertEqual(payload["network"]["entries"][0]["pages_checked"], 1)


class RunnerTask14RoutingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "路由 项目"
        self.root.mkdir()
        self.settings = self.root / "workflow-settings.toml"
        self.settings.write_text(
            """config_version = 1
[workflow]
enabled = false
timezone = "Asia/Shanghai"
[schedule]
mode = "manual"
start_time = "22:00"
weekdays = ["Monday"]
interval_days = 1
day_of_month = 1
[research]
incremental_search = true
full_recheck_interval_days = 7
check_existing_skill_updates = true
include_generic_skills = true
[delivery]
generate_word = true
generate_excel = true
only_refresh_affected_classes = true
notify_on_no_change = false
""",
            encoding="utf-8",
        )
        ledger_path = self.root / "ledger" / "Skills主台账.xlsx"
        ledger = LedgerStore.create(ledger_path)
        row = {column: "已核验" for column in CURRENT_SKILL_COLUMNS}
        row.update({
            "内部标识": "SK-EXISTING", "Skill名称": "existing", "规范名称": "既有技能", "入库层级": "正式",
            "来源平台": "GitHub", "发现地址": "https://github.com/example/existing", "Canonical source": "https://github.com/example/existing",
            "上游项目地址": "https://github.com/example/existing", "Skill入口路径": "SKILL.md", "固定版本": "1" * 40,
            "固定版本内容指纹": "2" * 64, "许可证": "MIT", "外部联网/API 调用": "否", "远程服务端点": "",
            "安全等级": "SA", "验证状态": "全部通过（未实测）", "质量评分": 3,
        })
        ledger.append_rows("当前Skill", [row])
        candidate = self.root / "candidate"
        shutil.copytree(FIXTURES / "fixed-package", candidate)
        snapshot = build_snapshot(SnapshotCandidate("SK-EXISTING", "3" * 40, candidate, ("evidence/SKILL.md",)), self.root / "snapshot")
        self.packet = build_review_packet({
            "candidate_id": "SK-EXISTING", "canonical_source": "https://github.com/example/existing",
            "license": "MIT", "security_grade": "SB-A",
        }, snapshot)
        staged = self.root / "ledger" / "seed.xlsx"
        ledger.save_staged(staged)
        shutil.copyfile(staged, ledger_path)
        staged.unlink()

    def test_existing_version_routed_to_condition_observation_is_not_lost_in_shadow_workbook(self):
        coordinator = RunCoordinator(
            root=self.root,
            discover=lambda request, staging: tuple(SourceRun(name, "complete") for name in PLATFORM_ORDER),
            report_builder=lambda prepared, staging: (),
            office_verifier=lambda prepared, paths: None,
        )
        request = RunRequest(
            settings_path=self.settings, catalog_loader=lambda: {"catalog": "fixed"},
            review_packets={"SK-EXISTING": self.packet}, requested_run_id="run-existing-condition",
        )
        prepared = coordinator.prepare(request)
        observation = {
            "观察标识": "OBS-REJECTED-VERSION", "候选名称": "existing", "Canonical source": "https://github.com/example/existing",
            "观察状态": "条件候选", "许可证": "MIT", "记录日期": "2026-08-29",
            "原因": "发现新版本但许可证范围需要复核；保留旧固定版本。",
        }
        decision = ReviewDecision(
            ObservedFacts(
                "3" * 40, True, True, "MIT", "https://github.com/example/existing", ("evidence/SKILL.md",),
                "否", (), "无", "不使用", "SB-A", "前两步通过",
            ),
            ProjectJudgments("条件候选", True, False, 4),
            DerivedFields(quality_score=0, ledger_row=observation),
            "SK-EXISTING",
        )
        coordinator.apply_reviews(prepared, (decision,))
        staged_ledger = LedgerStore.load(prepared.staging_ledger)
        try:
            rows = staged_ledger.rows("候选观察")
            current = staged_ledger.rows("当前Skill")
        finally:
            staged_ledger.workbook.close()
            coordinator.abandon(prepared)
        self.assertEqual([row["观察标识"] for row in rows], ["OBS-REJECTED-VERSION"])
        self.assertEqual(current[0]["固定版本"], "1" * 40)

    def test_discovered_existing_formal_skill_does_not_gain_a_false_pending_observation(self):
        ledger = LedgerStore.load(self.root / "ledger" / "Skills主台账.xlsx")
        coordinator = RunCoordinator(root=self.root)
        candidate = {
            "内部标识": "SK-EXISTING", "platform": "GitHub", "name": "existing",
            "source_url": "https://github.com/example/existing", "canonical_source": "https://github.com/example/existing",
        }
        coordinator._apply_dedup_and_watermarks(
            ledger,
            (SourceRun("GitHub", "complete", candidates=(candidate,)),),
        )
        try:
            self.assertEqual(ledger.rows("候选观察"), [])
        finally:
            ledger.workbook.close()

    def test_no_fixed_package_reason_is_persisted_instead_of_generic_pending_text(self):
        ledger = LedgerStore.load(self.root / "ledger" / "Skills主台账.xlsx")
        coordinator = RunCoordinator(root=self.root)
        candidate = {
            "内部标识": "SK-NO-PACKAGE", "platform": "Hugging Face Spaces", "name": "metadata only",
            "source_url": "https://huggingface.co/spaces/example/demo", "canonical_source": "",
            "observation_status": "条件候选", "observation_reason_code": "fixed-package-unavailable",
            "observation_reason": "当前接口只返回元数据，无法取得完整固定包；不得进入正式评审。",
        }
        coordinator._apply_dedup_and_watermarks(
            ledger,
            (SourceRun("Hugging Face Spaces", "complete", candidates=(candidate,)),),
        )
        try:
            rows = ledger.rows("候选观察")
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["观察状态"], "条件候选")
            self.assertIn("无法取得完整固定包", rows[0]["原因"])
            self.assertNotIn("Task 7", rows[0]["原因"])
        finally:
            ledger.workbook.close()

    def test_deleted_upstream_is_attention_observation_and_keeps_current_row(self):
        ledger = LedgerStore.load(self.root / "ledger" / "Skills主台账.xlsx")
        coordinator = RunCoordinator(root=self.root)
        candidate = {
            "内部标识": "SK-EXISTING", "platform": "GitHub", "name": "existing",
            "source_url": "https://github.com/example/existing", "canonical_source": "https://github.com/example/existing",
            "observation_status": "attention_required", "observation_reason_code": "upstream-deleted",
            "observation_reason": "上游已删除或不可用；保留既有当前版本和固定快照。",
        }
        coordinator._apply_dedup_and_watermarks(ledger, (SourceRun("GitHub", "complete", candidates=(candidate,)),))
        try:
            self.assertEqual(len(ledger.rows("当前Skill")), 1)
            observations = ledger.rows("候选观察")
            self.assertEqual(len(observations), 1)
            self.assertEqual(observations[0]["观察状态"], "attention_required")
        finally:
            ledger.workbook.close()

    def test_empty_material_packet_binding_is_still_one_time(self):
        coordinator = RunCoordinator(
            root=self.root,
            discover=lambda request, staging: tuple(SourceRun(name, "complete") for name in PLATFORM_ORDER),
        )
        prepared = coordinator.prepare(RunRequest(
            settings_path=self.settings, catalog_loader=lambda: {"catalog": "fixed"},
            requested_run_id="run-bind-empty",
        ))
        try:
            coordinator.bind_review_packets(prepared, {})
            with self.assertRaisesRegex(Exception, "不得替换"):
                coordinator.bind_review_packets(prepared, {})
        finally:
            coordinator.abandon(prepared)


class OfflineWorkflowEndToEndTest(unittest.TestCase):
    """A complete file-only release rehearsal; candidate fixture content is never executed."""

    def setUp(self) -> None:
        if not os.environ.get("SKILL_MAINTAINER_NODE") or not os.environ.get("SKILL_MAINTAINER_NODE_MODULES"):
            self.skipTest("offline E2E requires explicitly loader-bound Node runtime")
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name) / "便携 中文 项目"
        self.project.mkdir()
        (self.project / "AGENTS.md").write_text("# E2E fixture authority\n", encoding="utf-8")
        rules = self.project / "01_规则"
        rules.mkdir()
        for name in cli.REQUIRED_RULES:
            (rules / name).write_text(f"# {name}\nE2E fixture rule.\n", encoding="utf-8")
        self.skills_root = Path(self.temporary.name) / "Codex Skills"
        source_workflow = Path(__file__).parents[1]
        result = cli.setup_project(
            self.project, source_workflow=source_workflow, codex_skills_root=self.skills_root,
        )
        self.assertEqual(result.exit_code, 0, result)
        self.workflow = self.project / WORKFLOW
        self._import_520_rows()
        self.old_catalog, self.changed_catalog, self.current_catalog = self._catalogs()
        self.ids = self._seed_profiles_and_mappings()

    @staticmethod
    def _formal_row(stable_id: str, canonical: str, version: str, content_hash: str) -> dict[str, object]:
        row = {column: "已核验" for column in CURRENT_SKILL_COLUMNS}
        row.update({
            "内部标识": stable_id, "Skill名称": stable_id, "规范名称": stable_id, "入库层级": "正式",
            "功能一级分类": "经济学", "功能二级标签": "0201 经济学类", "关联分类": "经济统计",
            "原生生态": "Codex Skill", "来源形态": "公开社区", "来源平台": "GitHub",
            "发现地址": canonical, "收集日期": "2026-08-29", "Canonical source": canonical,
            "上游项目地址": canonical, "Skill入口路径": "SKILL.md", "发布者": "fixture",
            "固定版本": version, "固定版本内容指纹": content_hash, "许可证": "MIT", "简要功能": "整理研究资料",
            "详细功能摘要": "以只读静态流程整理公开研究资料。", "适用用户角色": "高校技术人员",
            "典型高校场景": "经济学研究", "Codex兼容等级": "可直接使用", "适配建议": "人工复核结果",
            "关联资源类型": "本地文件", "关联资源地址": "无", "外部依赖": "无",
            "外部联网/API 调用": "否", "远程服务端点": "", "本地专业软件或运行时依赖": "无",
            "本地脚本/插件接口": "不使用", "可执行行为": "无", "网络与数据行为": "无",
            "凭据行为": "无", "文件行为": "只读", "安全等级": "SA", "安全限制条件": "静态检查通过",
            "最近更新": "2026-08-29", "维护状态": "活跃", "风险提示": "固定版本", "替代方案": "无",
            "验证级别": "静态", "验证状态": "全部通过（未实测）", "验证证据位置": "fixture/SKILL.md",
            "最近核验日期": "2026-08-29", "推荐优先级": "高", "接入难度": "低", "实施准备度": "高",
            "质量评分": 3, "重复或关联条目": "无", "备注": "E2E fixture",
        })
        return row

    def _import_520_rows(self) -> None:
        source = FIXTURES / "fixed-package" / "SKILL.md"
        rows: list[ImportedRecord] = []
        for index in range(517):
            stable = f"SK-FILLER-{index:04d}"
            historical = self._formal_row(stable, f"https://fixture.invalid/skills/{index:04d}", "1" * 40, f"{index + 1:064x}")
            historical["质量评分"] = "3"
            rows.append(ImportedRecord(
                source, index + 2,
                historical,
            ))
        specials = (
            ("SK-UPGRADE", "https://github.com/e2e/accepted-upgrade", "1" * 40, "a" * 64),
            ("SK-REJECT", "https://github.com/e2e/rejected-upgrade", "2" * 40, "b" * 64),
            ("SK-DELETED", "https://github.com/e2e/deleted-upstream", "3" * 40, "c" * 64),
        )
        for offset, values in enumerate(specials, start=519):
            historical = self._formal_row(*values)
            historical["质量评分"] = "3"
            rows.append(ImportedRecord(source, offset, historical))
        inventory = ImportInventory(
            root=FIXTURES, records=tuple(rows), source_hashes={}, excel_files=(), word_files=(),
            excel_skill_count=520, word_skill_count=520, duplicate_group_count=0,
            ambiguous_record_count=0, word_excel_count_mismatch=False,
        )
        staging = self.workflow / "ledger" / "staging"
        staging.mkdir()
        imported = staging / "initial-import.xlsx"
        summary = build_initial_ledger(inventory, imported)
        self.assertEqual(summary.current_skill_count, 520)
        shutil.copyfile(imported, self.workflow / "ledger" / "Skills主台账.xlsx")

    @staticmethod
    def _catalogs():
        profile = TaskProfile(
            professional_aliases=("economics",), core_courses=("计量经济学",), methods=("描述性统计",),
            work_tasks=("数据清洗",), outputs_and_data=("统计表",), software_databases_processes=("Stata",),
        )
        old = CatalogRow("02", "经济学", "0201", "经济学类", "020101", "经济学")
        new = CatalogRow("02", "经济学", "0201", "经济学类", "020101", "经济学（数字经济方向）")
        status = CatalogSourceStatus("https://www.moe.gov.cn/catalog.pdf", "d" * 64, "e" * 64, True)
        base = Catalog((old,), {"0201": profile, "99": profile}, status)
        changed = base.stage_new_snapshot((new,), snapshot_sha="e" * 64).stage_record_diff(diff_catalog((old,), (new,)))
        return Catalog((old,), {"0201": profile, "99": profile}), changed, Catalog((new,), {"0201": profile, "99": profile})

    def _stable_for(self, canonical: str) -> str:
        ledger = LedgerStore.load(self.workflow / "ledger" / "Skills主台账.xlsx")
        try:
            result = deduplicate([{
                "platform": "GitHub", "source_url": canonical, "canonical_source": canonical, "name": canonical.rsplit("/", 1)[-1],
            }], ledger)
        finally:
            ledger.workbook.close()
        return result.skills[0]["内部标识"]

    def _seed_profiles_and_mappings(self) -> dict[str, str]:
        ids = {
            "formal": self._stable_for("https://github.com/e2e/new-formal"),
            "condition": self._stable_for("https://github.com/e2e/new-condition"),
            "adaptation": self._stable_for("https://github.com/e2e/new-adaptation"),
            "upgrade": "SK-UPGRADE", "reject": "SK-REJECT", "deleted": "SK-DELETED",
        }
        ledger_path = self.workflow / "ledger" / "Skills主台账.xlsx"
        ledger = LedgerStore.load(ledger_path)
        profile = {
            "映射标识": "PROFILE-0201", "内部标识": "PROFILE-0201", "专业代码": "0201", "专业名称": "经济学类",
            "专业任务": "整理经济统计数据", "输入": "公开统计表", "输出": "字段字典", "适用理由": "支持实证研究准备",
            "使用限制": "需要研究者复核", "相关度": 5, "专业别名": "economics", "核心课程": "计量经济学",
            "研究方法": "描述性统计", "工作任务": "数据清洗", "成果或数据对象": "统计表",
            "软件/数据库/流程": "Stata；数据质量检查",
        }
        mappings = [profile]
        for label, stable in ids.items():
            mappings.append({
                "映射标识": f"MAP-{label}", "内部标识": stable, "专业代码": "0201", "专业名称": "经济学类",
                "专业任务": "整理经济统计数据", "输入": "公开统计表", "输出": "查验结果", "适用理由": "支持核心研究任务",
                "使用限制": "人工复核", "相关度": 5,
            })
        ledger.append_rows("专业任务映射", mappings)
        ledger.append_rows("目录基线", [{
            "目录版本": "2026", "目录名称": "本科专业目录", "公开地址": "https://www.moe.gov.cn/catalog.pdf",
            "SHA-256": "d" * 64, "发布日期": "2026-04-27", "访问日期": "2026-08-29",
        }])
        staged = self.workflow / "ledger" / "mapped.xlsx"
        ledger.save_staged(staged)
        shutil.copyfile(staged, ledger_path)
        staged.unlink()
        return ids

    def _driver(self, catalog: Catalog) -> ProductionDriver:
        canonicals = {
            "formal": "https://github.com/e2e/new-formal",
            "condition": "https://github.com/e2e/new-condition",
            "adaptation": "https://github.com/e2e/new-adaptation",
            "upgrade": "https://github.com/e2e/accepted-upgrade",
            "reject": "https://github.com/e2e/rejected-upgrade",
        }
        github_candidates = tuple(
            _candidate("GitHub", canonical.rsplit("github.com/", 1)[-1], canonical, canonical)
            for canonical in canonicals.values()
        )
        versions = {canonical: f"{index:x}" * 40 for index, canonical in enumerate(canonicals.values(), start=4)}
        versions["https://github.com/e2e/deleted-upstream"] = "9" * 40
        duplicate = _candidate("SkillHub", "formal-market", "https://skillhub.cn/formal", canonicals["formal"])
        adapters = {
            "SkillHub": _Adapter("SkillHub", (duplicate,)),
            "ClawHub": _Adapter("ClawHub", (_candidate("ClawHub", "formal-mirror", "https://clawhub.ai/formal", canonicals["formal"]),)),
            "GitHub": _ScenarioGithubAdapter(
                github_candidates, FIXTURES / "fixed-package", versions,
                {"https://github.com/e2e/deleted-upstream"},
            ),
            "Hugging Face Spaces": _Adapter(
                "Hugging Face Spaces", (_candidate("Hugging Face Spaces", "metadata-only", "https://huggingface.co/spaces/e2e/only", None),),
            ),
        }
        return ProductionDriver(
            project_root=self.project, adapters=adapters, catalog_loader=lambda: catalog,
            now=lambda: datetime(2026, 8, 29, tzinfo=timezone.utc),
        )

    @staticmethod
    def _unit_office_verifier(prepared, artifacts):
        from skill_maintainer.office import (
            OfficeEvidenceBundle, WordRenderDecision, bind_word_visual_decision, verify_excel, verify_word,
        )

        class Renderer:
            @staticmethod
            def render(pdf, output_dir):
                page = output_dir / "page-1.png"
                page.write_bytes(b"e2e-page-body")
                return (page,), (1,)

        checks = []
        for path in artifacts:
            path = Path(path).absolute()
            if path.suffix.casefold() == ".xlsx":
                role = "ledger" if path == prepared.staging_ledger.absolute() else "daily"
                result = {
                    "passed": True, "office_opened": True, "read_only": True,
                    "key_sheet": "运行记录" if role == "ledger" else "执行概览", "last_row": 522,
                    "last_column": 1, "last_value": "verified", "process_count_before": 0,
                    "process_count_after": 0, "error": None,
                }
                with patch("skill_maintainer.office._run_office", return_value=result):
                    checks.append(verify_excel(path, scope=prepared.office_scope, role=role))
            elif path.suffix.casefold() == ".docx":
                evidence = prepared.staging_dir / ".office-evidence"
                evidence.mkdir(exist_ok=True)
                render = evidence / sha256(str(path).encode()).hexdigest()[:16]

                def office_word(*arguments):
                    render_dir = Path(arguments[arguments.index("-RenderDirectory") + 1])
                    pdf = render_dir / f"{path.stem}.office.pdf"
                    pdf.write_bytes(b"e2e-pdf")
                    return {
                        "passed": True, "office_opened": True, "read_only": True,
                        "pdf_path": str(pdf), "page_count": 1, "process_count_before": 0,
                        "process_count_after": 0, "error": None,
                    }

                with patch("skill_maintainer.office._run_office", side_effect=office_word):
                    rendered = verify_word(path, render, renderer=Renderer(), scope=prepared.office_scope)
                checks.append(bind_word_visual_decision(
                    rendered, WordRenderDecision.from_check(rendered, approved=True, reviewer="offline E2E"),
                    scope=prepared.office_scope,
                ))
        return OfficeEvidenceBundle.from_checks(tuple(checks), scope=prepared.office_scope)

    def _decisions(self, driver: ProductionDriver, packets) -> tuple[ReviewDecision, ...]:
        decisions = []
        for material in driver.review_materials:
            canonical = material.canonical_source
            packet = packets[material.candidate_id]
            if canonical.endswith("new-formal") or canonical.endswith("accepted-upgrade"):
                tier, security, verification, bonuses = "正式推荐", "SA", "全部通过（未实测）", (True, True)
                row = self._formal_row(material.candidate_id, canonical, material.fixed_version, packet.fixed_content_hash)
                row["验证证据位置"] = "；".join(packet.evidence_paths)
            else:
                tier, security, verification, bonuses = (
                    ("需适配候选", "SB-A", "前两步通过", ()) if canonical.endswith("new-adaptation")
                    else ("条件候选", "SB-A", "前两步通过", ())
                )
                reason = "需封装本地流程后使用" if tier == "需适配候选" else "发现新版本但未升级；保留旧固定版本并待人工复核"
                row = {
                    "观察标识": f"OBS-{material.candidate_id}-{tier}", "候选名称": material.name,
                    "Canonical source": canonical, "观察状态": tier, "许可证": "MIT",
                    "记录日期": "2026-08-29", "原因": reason,
                }
            decisions.append(ReviewDecision(
                ObservedFacts(
                    material.fixed_version, True, True, "MIT", canonical, packet.evidence_paths,
                    "否", (), "无", "不使用", security, verification,
                ),
                ProjectJudgments(tier, True, tier == "正式推荐", 5, bonuses),
                DerivedFields(quality_score=3 if tier == "正式推荐" else 0, ledger_row=row),
                material.candidate_id,
            ))
        return tuple(decisions)

    def _run_once(self, run_id: str, catalog: Catalog):
        driver = self._driver(catalog)
        coordinator = RunCoordinator(
            root=self.workflow, discover=driver.discover,
            report_builder=make_project_report_builder(self.workflow),
            office_verifier=self._unit_office_verifier,
        )
        request = RunRequest(
            settings_path=self.workflow / "workflow-settings.toml", catalog_loader=driver.load_catalog,
            discover=driver.discover, requested_run_id=run_id, material_reviewer=driver,
        )
        prepared = coordinator.prepare(request)
        frame = driver.material_review_frame(prepared)
        observations = {
            "type": "material_observations", "run_id": run_id,
            "observations": [{
                "candidate_id": item["candidate_id"], "fixed_version": item["fixed_version"],
                "fixed_content_hash": item["fixed_content_hash"], "canonical_source": item["canonical_source"],
                "license": "MIT", "security_grade": "SA" if item["canonical_source"].endswith(("new-formal", "accepted-upgrade")) else "SB-A",
            } for item in frame["materials"]],
        }
        packets = driver.apply_material_observations(prepared, observations)
        coordinator.bind_review_packets(prepared, packets)
        reviews = coordinator.apply_reviews(prepared, self._decisions(driver, packets))
        return coordinator.finalize(prepared, reviews), driver

    def test_setup_import_three_gates_finalize_twice_is_file_only_and_idempotent(self):
        first, first_driver = self._run_once("run-e2e-first", self.changed_catalog)
        first_ledger = LedgerStore.load(first.published_ledger)
        try:
            first_counts = {sheet: len(first_ledger.rows(sheet)) for sheet in ("当前Skill", "候选观察", "来源别名", "版本历史")}
            current = {row["内部标识"]: row for row in first_ledger.rows("当前Skill")}
            aliases = [row for row in first_ledger.rows("来源别名") if row["内部标识"] == self.ids["formal"]]
        finally:
            first_ledger.workbook.close()
        self.assertEqual(first_counts["当前Skill"], 521)
        self.assertEqual(current["SK-UPGRADE"]["固定版本"], "7" * 40)
        self.assertEqual(current["SK-REJECT"]["固定版本"], "2" * 40)
        self.assertGreaterEqual(first_counts["候选观察"], 4)
        self.assertGreaterEqual(len(aliases), 3)
        self.assertTrue((first.output_generation / "受影响专业类").is_dir())
        self.assertTrue(any(item.reason_code == "upstream-deleted" for item in first_driver.observations))

        second, _ = self._run_once("run-e2e-second", self.current_catalog)
        second_ledger = LedgerStore.load(second.published_ledger)
        try:
            second_counts = {sheet: len(second_ledger.rows(sheet)) for sheet in first_counts}
        finally:
            second_ledger.workbook.close()
        self.assertEqual(second_counts, first_counts)
        self.assertFalse(any((second.output_generation / "受影响专业类").rglob("*.docx")))
        self.assertFalse(any((second.output_generation / "受影响专业类").rglob("*.xlsx")))
        self.assertFalse(any(path.suffix.casefold() in {".db", ".sqlite", ".duckdb"} for path in self.workflow.rglob("*")))

        authority_before = sha256((self.workflow / "ledger" / "Skills主台账.xlsx").read_bytes()).hexdigest()
        published_before = {
            path.relative_to(self.workflow / "output"): sha256(path.read_bytes()).hexdigest()
            for path in (self.workflow / "output").rglob("*") if path.is_file()
        }
        for point in ("report", "office", "before_commit"):
            coordinator = RunCoordinator(
                root=self.workflow,
                discover=lambda request, staging: tuple(SourceRun(name, "complete") for name in PLATFORM_ORDER),
                report_builder=make_project_report_builder(self.workflow), office_verifier=self._unit_office_verifier,
                fail_at=point,
            )
            prepared = coordinator.prepare(RunRequest(
                settings_path=self.workflow / "workflow-settings.toml", catalog_loader=lambda: self.current_catalog,
                requested_run_id=f"run-e2e-failure-{point}",
            ))
            reviews = coordinator.apply_reviews(prepared, ())
            with self.assertRaisesRegex(RuntimeError, "injected failure"):
                coordinator.finalize(prepared, reviews)
            self.assertEqual(sha256((self.workflow / "ledger" / "Skills主台账.xlsx").read_bytes()).hexdigest(), authority_before)
            self.assertEqual({
                path.relative_to(self.workflow / "output"): sha256(path.read_bytes()).hexdigest()
                for path in (self.workflow / "output").rglob("*") if path.is_file()
            }, published_before)

        export_text = os.environ.get("SKILL_MAINTAINER_E2E_EXPORT", "").strip()
        if export_text:
            export_root = Path(export_text).absolute()
            if export_root.exists() and any(export_root.iterdir()):
                self.fail("SKILL_MAINTAINER_E2E_EXPORT must name an absent or empty directory")
            export_root.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(second.published_ledger, export_root / "E2E_520行发布主台账.xlsx")
            for source in second.output_generation.rglob("*"):
                if not source.is_file() or source.suffix.casefold() not in {".docx", ".xlsx"}:
                    continue
                relative = source.relative_to(second.output_generation)
                destination = export_root / "generation" / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)


if __name__ == "__main__":
    unittest.main()
