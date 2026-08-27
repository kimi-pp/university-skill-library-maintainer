import hashlib
import json
import unittest
from pathlib import Path

from skill_maintainer.catalog import (
    Catalog,
    CatalogRow,
    CatalogSourceChangedError,
    CatalogSourceStatus,
    TaskProfile,
    build_scopes,
    diff_catalog,
    load_catalog,
    verify_catalog_source,
)
from skill_maintainer.queries import PLATFORM_ORDER, build_queries


WORKTREE = Path(__file__).resolve().parents[2]
FIXTURE_PATH = WORKTREE / "06_过程记录" / "discipline_mapping" / "catalogs" / "undergraduate_2026.json"


def row(**changes):
    values = {
        "category_code": "08",
        "category_name": "工学",
        "class_code": "0818",
        "class_name": "交通运输类",
        "major_code": "081801",
        "major_name": "交通运输",
    }
    values.update(changes)
    return CatalogRow(**values)


class CatalogScopeTest(unittest.TestCase):
    def test_current_fixture_builds_the_frozen_13_category_research_scope(self):
        catalog = load_catalog(FIXTURE_PATH)

        scopes = build_scopes(catalog)

        self.assertEqual(len(catalog.rows), 883)
        self.assertEqual(len({item.major_code for item in catalog.rows}), 883)
        self.assertNotIn("11", {scope.category_code for scope in scopes})
        self.assertEqual(sum(scope.scope_kind == "professional_class" for scope in scopes), 92)
        self.assertEqual(sum(scope.scope_kind == "interdisciplinary_major" for scope in scopes), 15)
        self.assertEqual(sum(scope.scope_kind == "generic" for scope in scopes), 1)
        self.assertEqual(scopes[-1].scope_id, "99")
        self.assertEqual(scopes[-1].scope_name, "跨学科通用")

    def test_changed_source_blocks_scope_building_until_snapshot_and_record_diff_are_staged(self):
        changed = CatalogSourceStatus(
            url="https://catalog.example/undergraduate.pdf",
            expected_sha="a" * 64,
            actual_sha="b" * 64,
            changed=True,
        )
        catalog = Catalog(rows=(row(),), source_status=changed)

        with self.assertRaises(CatalogSourceChangedError):
            build_scopes(catalog)

        with self.assertRaises(CatalogSourceChangedError):
            build_scopes(catalog.stage_new_snapshot())

        staged = catalog.stage_new_snapshot().stage_record_diff(diff_catalog((row(),), (row(),)))
        self.assertEqual(build_scopes(staged)[0].scope_id, "0818")

    def test_injected_fetch_hash_gate_reports_content_change_without_claiming_official_unchanged(self):
        expected = hashlib.sha256(b"old catalog bytes").hexdigest()

        status = verify_catalog_source(
            "https://catalog.example/undergraduate.pdf",
            expected,
            fetch=lambda _url: b"new catalog bytes",
        )

        self.assertTrue(status.changed)
        self.assertEqual(status.actual_sha, hashlib.sha256(b"new catalog bytes").hexdigest())


class CatalogDiffTest(unittest.TestCase):
    def test_diff_catalog_keeps_all_six_record_change_types_separate(self):
        unchanged = row()
        old_rows = (
            unchanged,
            row(major_code="080001", major_name="旧专业"),
            row(major_code="080002", major_name="保留代码旧名称"),
            row(major_code="080003", major_name="代码迁移专业"),
            row(major_code="080004", major_name="专业类迁移专业", class_code="0801", class_name="力学类"),
            row(major_code="080005", major_name="门类迁移专业", category_code="07", category_name="理学", class_code="0701", class_name="数学类"),
        )
        new_rows = (
            unchanged,
            row(major_code="080006", major_name="新增专业"),
            row(major_code="080002", major_name="保留代码新名称"),
            row(major_code="080007", major_name="代码迁移专业"),
            row(major_code="080004", major_name="专业类迁移专业", class_code="0802", class_name="机械类"),
            row(major_code="080005", major_name="门类迁移专业", category_code="08", category_name="工学", class_code="0805", class_name="能源动力类"),
        )

        diff = diff_catalog(old_rows, new_rows)

        self.assertEqual([item.major_code for item in diff.added], ["080006"])
        self.assertEqual([item.major_code for item in diff.removed], ["080001"])
        self.assertEqual([(item.old.major_code, item.new.major_name) for item in diff.renamed], [("080002", "保留代码新名称")])
        self.assertEqual([(item.old.major_code, item.new.major_code) for item in diff.major_code_changes], [("080003", "080007")])
        self.assertEqual([(item.old.class_code, item.new.class_code) for item in diff.class_moves], [("0801", "0802")])
        self.assertEqual([(item.old.category_code, item.new.category_code) for item in diff.category_moves], [("07", "08")])
        self.assertTrue(diff.has_record_changes)


class SixDimensionQueryTest(unittest.TestCase):
    def test_transport_scope_emits_every_dimension_for_each_fixed_platform_with_stable_ids(self):
        profile = TaskProfile(
            professional_aliases=("交通运输", "transportation engineering"),
            core_courses=("交通工程学",),
            methods=("traffic flow prediction",),
            work_tasks=("route optimisation",),
            outputs_and_data=("OD matrix",),
            software_databases_processes=("SUMO traffic simulation",),
        )
        catalog = Catalog(rows=(row(),), task_profiles={"0818": profile})
        transport_scope = build_scopes(catalog)[0]

        jobs = build_queries(transport_scope)
        rerun_jobs = build_queries(transport_scope)

        self.assertEqual(PLATFORM_ORDER, ("SkillHub", "ClawHub", "GitHub", "Hugging Face Spaces"))
        self.assertEqual({job.platform for job in jobs}, set(PLATFORM_ORDER))
        self.assertEqual(
            {job.dimension for job in jobs},
            {"professional_alias", "core_course", "method", "work_task", "output_or_data", "software_database_or_process"},
        )
        self.assertEqual(len({job.query_id for job in jobs}), len(jobs))
        self.assertEqual([job.query_id for job in jobs], [job.query_id for job in rerun_jobs])
        method_and_task_queries = [job.query for job in jobs if job.dimension in {"method", "work_task"}]
        self.assertTrue(any("交通运输" not in query for query in method_and_task_queries))
        self.assertTrue(any("traffic flow prediction" in query for query in method_and_task_queries))
        self.assertTrue(any("route optimisation" in query for query in method_and_task_queries))


if __name__ == "__main__":
    unittest.main()
