import io
import json
import tempfile
import unittest
import zipfile
from copy import copy
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from skill_maintainer.ledger import LedgerStore
from skill_maintainer.ledger_schema import CURRENT_SKILL_COLUMNS
from skill_maintainer import review as review_module
from skill_maintainer.snapshots import (
    SnapshotCandidate, SnapshotLimits, SnapshotManifest, archive_skill_entries,
    build_archive_entry_snapshot, build_archive_snapshot, build_snapshot,
)
from skill_maintainer.review import (
    AppliedReview,
    DerivedFields,
    ObservedFacts,
    ProjectJudgments,
    ReviewDecision,
    ReviewPacket,
    apply_reviews_from_stream,
    build_review_packet,
    score_quality,
    validate_applied_review,
    validate_review,
)


class SnapshotContractTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def _candidate(self, source, version="0123456789abcdef0123456789abcdef01234567"):
        return SnapshotCandidate("org/example", version, Path(source), ("https://evidence.example/commit",))

    def test_fixed_version_is_required_before_snapshotting(self):
        source = self.root / "candidate"
        source.mkdir()
        (source / "SKILL.md").write_text("# skill", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "固定版本"):
            build_snapshot(self._candidate(source, ""), self.root / "snapshot")

    def test_archive_path_traversal_is_rejected_without_writing_outside_destination(self):
        archive = self.root / "candidate.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("../escape.py", "raise RuntimeError")

        with self.assertRaisesRegex(ValueError, "路径穿越"):
            build_snapshot(self._candidate(archive), self.root / "snapshot")
        self.assertFalse((self.root / "escape.py").exists())

    def test_safe_nested_archive_file_is_snapshotted_inside_destination(self):
        archive = self.root / "candidate.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("instructions/SKILL.md", "# static instruction")

        manifest = build_snapshot(self._candidate(archive), self.root / "snapshot")

        self.assertEqual([entry.path for entry in manifest.files], ["instructions/SKILL.md"])
        self.assertTrue((self.root / "snapshot" / "instructions" / "SKILL.md").is_file())

    def test_linked_candidate_entries_are_rejected(self):
        source = self.root / "candidate"
        source.mkdir()
        (source / "SKILL.md").write_text("# skill", encoding="utf-8")
        linked = source / "outside"
        try:
            linked.symlink_to(self.root, target_is_directory=True)
        except OSError:
            self.skipTest("当前环境不允许创建符号链接安全回归夹具")

        with self.assertRaisesRegex(ValueError, "链接|重解析"):
            build_snapshot(self._candidate(source), self.root / "snapshot")

    def test_linked_destination_is_rejected_before_resolution_or_external_write(self):
        source = self.root / "candidate"
        source.mkdir()
        (source / "SKILL.md").write_text("# skill", encoding="utf-8")
        outside = self.root / "outside"
        outside.mkdir()
        linked = self.root / "linked-destination"
        try:
            linked.symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("当前环境不允许创建符号链接安全回归夹具")

        with self.assertRaisesRegex(ValueError, "链接|重解析"):
            build_snapshot(self._candidate(source), linked / "snapshot")
        self.assertFalse((outside / "snapshot").exists())

    def test_snapshot_enforces_file_count_total_and_single_file_bounds(self):
        source = self.root / "candidate"
        source.mkdir()
        (source / "one.md").write_text("one", encoding="utf-8")
        (source / "two.md").write_text("two", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "文件数量"):
            build_snapshot(self._candidate(source), self.root / "count", SnapshotLimits(max_files=1, max_total_bytes=10, max_file_bytes=10))
        with self.assertRaisesRegex(ValueError, "总字节"):
            build_snapshot(self._candidate(source), self.root / "total", SnapshotLimits(max_files=3, max_total_bytes=5, max_file_bytes=10))
        with self.assertRaisesRegex(ValueError, "单文件"):
            build_snapshot(self._candidate(source), self.root / "single", SnapshotLimits(max_files=3, max_total_bytes=10, max_file_bytes=2))

    def test_oversized_archive_member_is_rejected_before_its_content_is_read(self):
        archive = self.root / "candidate.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("payload.md", "too large")
        with patch.object(zipfile.ZipFile, "read", side_effect=AssertionError("oversized candidate must not be read")):
            with self.assertRaisesRegex(ValueError, "单文件"):
                build_snapshot(self._candidate(archive), self.root / "snapshot", SnapshotLimits(max_files=1, max_total_bytes=100, max_file_bytes=2))

    def test_compressed_archive_bytes_have_an_independent_hard_cap(self):
        with self.assertRaisesRegex(ValueError, "压缩字节"):
            build_archive_snapshot(
                candidate_id="org/example", fixed_version="a" * 40,
                archive_bytes=b"x" * 11, archive_name="candidate.zip",
                destination=self.root / "snapshot",
                limits=SnapshotLimits(max_files=10, max_total_bytes=100, max_file_bytes=100, max_archive_bytes=10),
            )

    def test_archive_rejects_ntfs_unsafe_names_and_case_collisions(self):
        unsafe_groups = (("repo/a:stream/SKILL.md",), ("repo/CON/SKILL.md",), ("repo/trailing./SKILL.md",),
                         ("repo/A/SKILL.md", "repo/a/skill.md"))
        for index, names in enumerate(unsafe_groups):
            with self.subTest(names=names):
                archive = self.root / f"unsafe-{index}.zip"
                with zipfile.ZipFile(archive, "w") as handle:
                    for name in names:
                        handle.writestr(name, "# static")
                with self.assertRaisesRegex(ValueError, "Windows|大小写"):
                    build_snapshot(self._candidate(archive), self.root / f"unsafe-out-{index}")

    def test_monorepo_entries_are_enumerated_and_snapshotted_independently(self):
        archive = self.root / "mono.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("repo-root/a/SKILL.md", "# A")
            handle.writestr("repo-root/a/helper.py", "A = 1")
            handle.writestr("repo-root/b/SKILL.md", "# B")
            handle.writestr("repo-root/LICENSE", "MIT")
        content = archive.read_bytes()

        self.assertEqual(archive_skill_entries(content, archive.name), ("a/SKILL.md", "b/SKILL.md"))
        first = build_archive_entry_snapshot(
            candidate_id="SK-A", fixed_version="a" * 40, archive_bytes=content, archive_name=archive.name,
            skill_entry_path="a/SKILL.md", destination=self.root / "entry-a",
        )
        self.assertEqual({item.path for item in first.files}, {"a/SKILL.md", "a/helper.py", "LICENSE"})
        self.assertNotIn("b/SKILL.md", {item.path for item in first.files})

    def test_root_skill_snapshot_includes_support_tree_but_excludes_nested_independent_skill(self):
        archive = self.root / "root-and-nested.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("repo-root/SKILL.md", "# root")
            handle.writestr("repo-root/scripts/install.ps1", "Write-Output root")
            handle.writestr("repo-root/assets/config.json", '{"enabled": false}')
            handle.writestr("repo-root/README.md", "root docs")
            handle.writestr("repo-root/nested/SKILL.md", "# independent nested")
            handle.writestr("repo-root/nested/scripts/run.py", "print('nested')")
        content = archive.read_bytes()

        root_manifest = build_archive_entry_snapshot(
            candidate_id="SK-ROOT", fixed_version="a" * 40,
            archive_bytes=content, archive_name=archive.name,
            skill_entry_path="SKILL.md", destination=self.root / "root-entry",
        )
        nested_manifest = build_archive_entry_snapshot(
            candidate_id="SK-NESTED", fixed_version="a" * 40,
            archive_bytes=content, archive_name=archive.name,
            skill_entry_path="nested/SKILL.md", destination=self.root / "nested-entry",
        )

        self.assertEqual(
            {item.path for item in root_manifest.files},
            {"SKILL.md", "scripts/install.ps1", "assets/config.json", "README.md"},
        )
        self.assertEqual(
            {item.path for item in nested_manifest.files},
            {"nested/SKILL.md", "nested/scripts/run.py"},
        )
        manifest_path = Path(root_manifest.manifest_evidence_path)
        self.assertTrue(manifest_path.is_file())
        persisted = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(persisted["fixed_content_hash"], root_manifest.fixed_content_hash)
        self.assertEqual({item["path"] for item in persisted["files"]}, {item.path for item in root_manifest.files})

    def test_static_snapshot_hashes_only_text_code_and_config_without_running_candidate(self):
        source = self.root / "candidate"
        source.mkdir()
        (source / "SKILL.md").write_text("# static only", encoding="utf-8")
        (source / "plugin.py").write_text("raise RuntimeError('must not run')", encoding="utf-8")
        (source / "settings.toml").write_text("enabled = false", encoding="utf-8")
        (source / "payload.bin").write_bytes(b"\x00\x01")

        with patch("subprocess.run", side_effect=AssertionError("candidate command must never run")):
            manifest = build_snapshot(self._candidate(source), self.root / "snapshot")

        entries = {entry.path: entry for entry in manifest.files}
        self.assertIsNotNone(entries["SKILL.md"].sha256)
        self.assertIsNotNone(entries["plugin.py"].sha256)
        self.assertIsNotNone(entries["settings.toml"].sha256)
        self.assertIsNone(entries["payload.bin"].sha256)
        self.assertFalse((self.root / "candidate-ran").exists())


class ReviewContractTest(unittest.TestCase):
    def _decision(self, **observed_overrides):
        facts = {
            "fixed_version": "0123456789abcdef0123456789abcdef01234567",
            "entry_description_complete": True,
            "prerequisites_clear_and_available": True,
            "license": "MIT",
            "canonical_source": "https://github.com/org/example",
            "evidence_paths": ("evidence/SKILL.md",),
            "remote_api_call": "否",
            "remote_endpoints": (),
            "local_professional_software": "Abaqus，实操时需要",
            "local_script_plugin_interface": "按需使用",
            "security_grade": "SA",
            "verification_status": "全部通过（未实测）",
        }
        facts.update(observed_overrides)
        observed = ObservedFacts(**facts)
        judgments = ProjectJudgments(
            record_tier="正式推荐",
            display_in_product=True,
            direct_deployable=True,
            relevance_score=4,
            quality_bonus_flags=(True, True, True, True, True),
        )
        return ReviewDecision(observed, judgments, DerivedFields(), "org/example")

    def _packet(
        self, decision, *, fixed_version=None, candidate_id="org/example",
        approved_scopes=(), skill_entry_path="SKILL.md",
    ):
        facts = decision.observed_facts
        version = fixed_version or facts.fixed_version
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "candidate"
            source.mkdir()
            (source / "SKILL.md").write_text("# review evidence", encoding="utf-8")
            snapshot = build_snapshot(SnapshotCandidate(candidate_id, version, source, facts.evidence_paths), root / "snapshot")
            return build_review_packet(
                {
                    "id": candidate_id, "canonical_source": facts.canonical_source, "license": facts.license,
                    "security_grade": facts.security_grade, "approved_scopes": approved_scopes,
                    "upstream_repository": facts.canonical_source, "skill_entry_path": skill_entry_path,
                },
                snapshot,
            )

    @staticmethod
    def _payload(decision, *, ledger_row=None):
        facts = decision.observed_facts
        judgments = decision.project_judgments
        return {
            "candidate_id": "org/example",
            "observed_facts": {
                "fixed_version": facts.fixed_version,
                "entry_description_complete": facts.entry_description_complete,
                "prerequisites_clear_and_available": facts.prerequisites_clear_and_available,
                "license": facts.license,
                "canonical_source": facts.canonical_source,
                "evidence_paths": list(facts.evidence_paths),
                "remote_api_call": facts.remote_api_call,
                "remote_endpoints": list(facts.remote_endpoints),
                "local_professional_software": facts.local_professional_software,
                "local_script_plugin_interface": facts.local_script_plugin_interface,
                "security_grade": facts.security_grade,
                "verification_status": facts.verification_status,
            },
            "project_judgments": {
                "record_tier": judgments.record_tier,
                "display_in_product": judgments.display_in_product,
                "direct_deployable": judgments.direct_deployable,
                "relevance_score": judgments.relevance_score,
                "quality_bonus_flags": list(judgments.quality_bonus_flags),
                "outcome": judgments.outcome,
                "exclusion_reason_code": judgments.exclusion_reason_code,
                "exclusion_reason": judgments.exclusion_reason,
            },
            "derived_fields": {"ledger_row": ledger_row} if ledger_row is not None else {},
        }

    @staticmethod
    def _formal_row(decision, packet, *, stable_id="org/example"):
        facts = decision.observed_facts
        row = {column: "已填" for column in CURRENT_SKILL_COLUMNS}
        row.update({
            "内部标识": stable_id, "入库层级": "正式", "来源平台": "GitHub",
            "固定版本": facts.fixed_version, "固定版本内容指纹": packet.fixed_content_hash,
            "Canonical source": facts.canonical_source, "许可证": facts.license,
            "安全等级": facts.security_grade, "质量评分": score_quality(decision),
            "验证状态": facts.verification_status, "验证证据位置": "；".join(facts.evidence_paths),
            "外部联网/API 调用": facts.remote_api_call, "远程服务端点": "",
            "本地专业软件或运行时依赖": facts.local_professional_software,
            "本地脚本/插件接口": facts.local_script_plugin_interface,
            "上游项目地址": packet.upstream_repository,
            "Skill入口路径": packet.skill_entry_path,
        })
        return row

    def test_packet_carries_rule_versions_and_snapshot_evidence_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "candidate"
            source.mkdir()
            (source / "SKILL.md").write_text("# example", encoding="utf-8")
            snapshot = build_snapshot(SnapshotCandidate("org/example", "a" * 40, source, ("https://source.example/a",)), Path(temporary) / "snapshot")
            packet = build_review_packet({
                "id": "org/example", "canonical_source": "https://github.com/org/example", "license": "MIT",
                "security_grade": "SA",
            }, snapshot)

        self.assertIn("SKILL_RESEARCH_WORKFLOW", packet.rule_versions)
        self.assertIn("VALIDATION_PROTOCOL", packet.rule_versions)
        self.assertIn("snapshot/SKILL.md", packet.evidence_paths)
        self.assertRegex(packet.fixed_content_hash, r"^[0-9a-f]{64}$")

    def test_abaqus_markdown_is_local_boundary_not_remote_api(self):
        self.assertEqual(validate_review(self._decision()), ())

    def test_review_packet_binds_version_source_license_security_and_evidence(self):
        decision = self._decision()
        packet = self._packet(decision, fixed_version="b" * 40)
        errors = validate_review(decision, packet)
        self.assertIn("observed_facts.fixed_version: 与审查包固定版本不一致", errors)

    def test_candidate_id_is_required_for_parsed_direct_and_packet_build_paths(self):
        decision = self._decision()
        payload = self._payload(decision)
        payload.pop("candidate_id")
        packet = self._packet(decision)
        empty_identity_packet = self._packet(decision, candidate_id="different/candidate")
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            body = json.dumps({"decisions": [payload]}, ensure_ascii=False).encode("utf-8")
            with self.assertRaisesRegex(ValueError, "review_decision.candidate_id: 必须提供非空候选标识"):
                apply_reviews_from_stream(io.BytesIO(body), store, {"": empty_identity_packet})
        direct = ReviewDecision(decision.observed_facts, decision.project_judgments, candidate_id="")
        self.assertIn(
            "review_decision.candidate_id: 必须提供非空候选标识",
            validate_review(direct, packet),
        )
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "candidate"
            source.mkdir()
            (source / "SKILL.md").write_text("# example", encoding="utf-8")
            snapshot = build_snapshot(SnapshotCandidate("", "a" * 40, source), Path(temporary) / "snapshot")
            with self.assertRaisesRegex(ValueError, "candidate_id"):
                build_review_packet({
                    "canonical_source": decision.observed_facts.canonical_source,
                    "license": decision.observed_facts.license,
                    "security_grade": decision.observed_facts.security_grade,
                }, snapshot)

    def test_apply_review_rejects_missing_packet_and_tampered_ledger_row(self):
        decision = self._decision()
        tampered_row = {"内部标识": "GH-01-0001", "固定版本": "attacker-version"}
        body = json.dumps({"decisions": [self._payload(decision, ledger_row=tampered_row)]}, ensure_ascii=False).encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            with self.assertRaisesRegex(ValueError, "审查包"):
                apply_reviews_from_stream(io.BytesIO(body), store, {})
            with self.assertRaisesRegex(ValueError, "derived_fields.ledger_row.固定版本"):
                apply_reviews_from_stream(io.BytesIO(body), store, {"org/example": self._packet(decision)})
            attacker = self._decision(fixed_version="attacker-version")
            attacker_body = json.dumps({"decisions": [self._payload(attacker)]}, ensure_ascii=False).encode("utf-8")
            with self.assertRaisesRegex(ValueError, "observed_facts.fixed_version: 与审查包固定版本不一致"):
                apply_reviews_from_stream(io.BytesIO(attacker_body), store, {"org/example": self._packet(decision)})
            wrong_identity_packet = self._packet(decision, candidate_id="other/candidate")
            untampered_body = json.dumps({"decisions": [self._payload(decision)]}, ensure_ascii=False).encode("utf-8")
            with self.assertRaisesRegex(ValueError, "review_packet.candidate_id: 与审查决定候选标识不一致"):
                apply_reviews_from_stream(io.BytesIO(untampered_body), store, {"org/example": wrong_identity_packet})
            self.assertEqual(store.rows("当前Skill"), [])

    def test_review_facts_cannot_borrow_another_candidates_archive_evidence(self):
        decision = self._decision()
        packet = self._packet(decision)
        borrowed = replace(
            decision.observed_facts,
            evidence_paths=(*decision.observed_facts.evidence_paths, "other-candidate/archive.zip#sha256=" + "f" * 64),
        )
        attack = ReviewDecision(borrowed, decision.project_judgments, decision.derived_fields, decision.candidate_id)
        self.assertIn(
            "observed_facts.evidence_paths: 未全部包含在审查包证据路径中",
            validate_review(attack, packet),
        )

    def test_formal_ledger_row_cannot_overwrite_another_candidate_identity(self):
        decision = self._decision()
        packet = self._packet(decision)
        victim = self._formal_row(decision, packet, stable_id="other/candidate")
        victim["Skill名称"] = "victim before review"
        attack = dict(victim)
        attack["Skill名称"] = "attacker overwrite"
        body = json.dumps({"decisions": [self._payload(decision, ledger_row=attack)]}, ensure_ascii=False).encode("utf-8")

        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            store.upsert_skill(victim)
            with self.assertRaisesRegex(ValueError, "derived_fields.ledger_row.内部标识"):
                apply_reviews_from_stream(io.BytesIO(body), store, {"org/example": packet})
            self.assertEqual(store.rows("当前Skill")[0]["Skill名称"], "victim before review")

    def test_formal_ledger_row_cannot_forge_the_fixed_package_content_hash(self):
        decision = self._decision()
        packet = self._packet(decision)
        attack = self._formal_row(decision, packet)
        attack["固定版本内容指纹"] = "f" * 64
        body = json.dumps({"decisions": [self._payload(decision, ledger_row=attack)]}, ensure_ascii=False).encode("utf-8")

        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            with self.assertRaisesRegex(ValueError, "derived_fields.ledger_row.固定版本内容指纹"):
                apply_reviews_from_stream(io.BytesIO(body), store, {"org/example": packet})
            self.assertEqual(store.rows("当前Skill"), [])

    def test_nonformal_ledger_row_cannot_overwrite_another_candidate_observation(self):
        base = self._decision()
        for tier in ("条件候选", "需适配候选"):
            with self.subTest(tier=tier), tempfile.TemporaryDirectory() as temporary:
                decision = ReviewDecision(
                    base.observed_facts,
                    ProjectJudgments(tier, True, False, 4, ()),
                    candidate_id=base.candidate_id,
                )
                packet = self._packet(decision)
                victim_id = f"OBS-other/candidate-{tier}"
                victim = {
                    "观察标识": victim_id, "候选名称": "victim before review",
                    "Canonical source": decision.observed_facts.canonical_source,
                    "观察状态": tier, "许可证": decision.observed_facts.license,
                    "记录日期": "2026-08-29", "原因": "victim record",
                }
                attack = {**victim, "候选名称": "attacker overwrite"}
                body = json.dumps(
                    {"decisions": [self._payload(decision, ledger_row=attack)]}, ensure_ascii=False,
                ).encode("utf-8")
                store = LedgerStore.create(Path(temporary) / "source.xlsx")
                store.upsert_candidate_observation(victim)

                with self.assertRaisesRegex(ValueError, "derived_fields.ledger_row.观察标识"):
                    apply_reviews_from_stream(io.BytesIO(body), store, {"org/example": packet})
                self.assertEqual(store.rows("候选观察")[0]["候选名称"], "victim before review")

    def test_scoped_review_writes_human_mapping_for_each_display_tier(self):
        base = self._decision()
        approved_scopes = (("0201", "经济学类"),)
        for tier in ("正式推荐", "条件候选", "需适配候选"):
            with self.subTest(tier=tier), tempfile.TemporaryDirectory() as temporary:
                decision = ReviewDecision(
                    base.observed_facts,
                    ProjectJudgments(tier, True, tier == "正式推荐", 4, (True,) if tier == "正式推荐" else ()),
                    candidate_id=base.candidate_id,
                )
                packet = self._packet(decision, approved_scopes=approved_scopes)
                if tier == "正式推荐":
                    row = self._formal_row(decision, packet)
                else:
                    row = {
                        "观察标识": f"OBS-org/example-{tier}", "内部标识": "org/example", "候选名称": "example",
                        "Canonical source": decision.observed_facts.canonical_source,
                        "Skill入口路径": packet.skill_entry_path,
                        "观察状态": tier, "许可证": "MIT", "记录日期": "2026-08-29", "原因": "人工确认候选层级",
                        "固定版本": decision.observed_facts.fixed_version,
                        "固定版本内容指纹": packet.fixed_content_hash,
                        "验证证据位置": "；".join(decision.observed_facts.evidence_paths),
                        "显示层级": tier,
                    }
                mapping = {
                    "映射标识": "MAP-org/example-0201", "内部标识": "org/example",
                    "专业代码": "0201", "专业名称": "经济学类", "专业任务": "整理统计数据",
                    "输入": "公开统计表", "输出": "字段字典", "适用理由": "支持实证研究准备",
                    "使用限制": "研究者复核", "相关度": 4,
                }
                payload = self._payload(decision, ledger_row=row)
                payload["derived_fields"]["scope_mappings"] = [mapping]
                store = LedgerStore.create(Path(temporary) / "source.xlsx")

                apply_reviews_from_stream(
                    io.BytesIO(json.dumps({"decisions": [payload]}, ensure_ascii=False).encode("utf-8")),
                    store, {"org/example": packet},
                )

                self.assertEqual(store.rows("专业任务映射")[0]["映射标识"], "MAP-org/example-0201")

    def test_scoped_review_rejects_missing_foreign_military_or_candidate_tampered_mapping(self):
        decision = self._decision()
        packet = self._packet(decision, approved_scopes=(("0201", "经济学类"),))
        formal = self._formal_row(decision, packet)
        valid = {
            "映射标识": "MAP-org/example-0201", "内部标识": "org/example",
            "专业代码": "0201", "专业名称": "经济学类", "专业任务": "整理统计数据",
            "输入": "公开统计表", "输出": "字段字典", "适用理由": "支持实证研究准备",
            "使用限制": "研究者复核", "相关度": 4,
        }
        attacks = (
            ([], "scope_mappings"),
            ([{**valid, "专业代码": "0301", "专业名称": "法学类", "映射标识": "MAP-org/example-0301"}], "专业代码"),
            ([{**valid, "专业代码": "1101", "专业名称": "军事学类", "映射标识": "MAP-org/example-1101"}], "专业代码"),
            ([{**valid, "内部标识": "other/candidate"}], "内部标识"),
        )
        for mappings, expected in attacks:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as temporary:
                payload = self._payload(decision, ledger_row=formal)
                payload["derived_fields"]["scope_mappings"] = mappings
                store = LedgerStore.create(Path(temporary) / "source.xlsx")
                with self.assertRaisesRegex(ValueError, expected):
                    apply_reviews_from_stream(
                        io.BytesIO(json.dumps({"decisions": [payload]}, ensure_ascii=False).encode("utf-8")),
                        store, {"org/example": packet},
                    )
                self.assertEqual(store.rows("当前Skill"), [])
                self.assertEqual(store.rows("专业任务映射"), [])

    def test_exclusion_is_a_non_display_outcome_with_structured_chinese_reason_and_no_name(self):
        base = self._decision(security_grade="X", license="unknown")
        decision = ReviewDecision(
            base.observed_facts,
            ProjectJudgments("条件候选", False, False, 1, (), "exclude", "security_rejected", "发现禁止性安全行为"),
            candidate_id=base.candidate_id,
        )
        packet = self._packet(decision, approved_scopes=(("0201", "经济学类"),))
        payload = self._payload(decision)
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            apply_reviews_from_stream(
                io.BytesIO(json.dumps({"decisions": [payload]}, ensure_ascii=False).encode("utf-8")),
                store, {decision.candidate_id: packet},
            )
            row = store.rows("候选观察")[0]
            self.assertEqual((row["内部标识"], row["候选名称"], row["观察状态"], row["显示层级"]),
                             (decision.candidate_id, "", "排除", "不展示"))
            self.assertEqual(store.rows("当前Skill"), [])
            self.assertEqual(store.rows("专业任务映射"), [])

    def test_prohibited_or_irrelevant_items_cannot_be_smuggled_as_display_candidates(self):
        base = self._decision()
        prohibited = ReviewDecision(
            replace(base.observed_facts, security_grade="X"),
            ProjectJudgments("条件候选", True, False, 4), candidate_id=base.candidate_id,
        )
        irrelevant = ReviewDecision(
            base.observed_facts, ProjectJudgments("条件候选", True, False, 2), candidate_id=base.candidate_id,
        )
        self.assertTrue(any("X/禁止风险" in error for error in validate_review(prohibited)))
        self.assertTrue(any("相关度低于" in error for error in validate_review(irrelevant)))

    def test_parser_normalizes_legacy_formal_only_at_the_boundary_and_rejects_unknown_tier(self):
        payload = self._payload(self._decision())
        payload["project_judgments"]["record_tier"] = "正式"
        parsed = ReviewDecision.from_mapping(payload)
        self.assertEqual(parsed.project_judgments.record_tier, "正式推荐")
        unknown = ProjectJudgments("未知层级", True, True, 4, ())
        self.assertIn(
            "project_judgments.record_tier: 只能为正式推荐、条件候选或需适配候选",
            validate_review(ReviewDecision(parsed.observed_facts, unknown, candidate_id=parsed.candidate_id)),
        )

    def test_conditional_and_adaptation_cannot_be_directly_deployed(self):
        decision = self._decision()
        for tier in ("条件候选", "需适配候选"):
            with self.subTest(tier=tier):
                judgments = ProjectJudgments(tier, True, True, 4, ())
                self.assertIn(
                    "project_judgments.direct_deployable: 条件候选和需适配候选不得直接部署",
                    validate_review(ReviewDecision(decision.observed_facts, judgments, candidate_id=decision.candidate_id)),
                )

    def test_include_must_be_displayable_and_direct_use_must_match_tier(self):
        base = self._decision()
        hidden = ReviewDecision(
            base.observed_facts,
            ProjectJudgments("条件候选", False, False, 4),
            candidate_id=base.candidate_id,
        )
        formal_not_direct = ReviewDecision(
            base.observed_facts,
            ProjectJudgments("正式推荐", True, False, 4),
            candidate_id=base.candidate_id,
        )
        self.assertTrue(any("display_in_product" in item for item in validate_review(hidden)))
        self.assertTrue(any("direct_deployable" in item for item in validate_review(formal_not_direct)))

    def test_display_candidate_row_requires_name_reason_and_iso_record_date(self):
        base = self._decision()
        decision = ReviewDecision(
            base.observed_facts, ProjectJudgments("条件候选", True, False, 4),
            candidate_id=base.candidate_id,
        )
        packet = self._packet(decision)
        row = {
            "观察标识": "OBS-org/example-条件候选", "内部标识": "org/example",
            "候选名称": "", "Canonical source": decision.observed_facts.canonical_source,
            "Skill入口路径": packet.skill_entry_path, "观察状态": "条件候选", "许可证": "MIT",
            "记录日期": "not-a-date", "原因": "", "固定版本": decision.observed_facts.fixed_version,
            "固定版本内容指纹": packet.fixed_content_hash,
            "验证证据位置": "；".join(decision.observed_facts.evidence_paths), "显示层级": "条件候选",
        }
        payload = self._payload(decision, ledger_row=row)
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            with self.assertRaisesRegex(ValueError, "候选名称|记录日期|原因"):
                apply_reviews_from_stream(
                    io.BytesIO(json.dumps({"decisions": [payload]}, ensure_ascii=False).encode("utf-8")),
                    store, {decision.candidate_id: packet},
                )

    def test_application_routes_conditional_candidate_to_observations_not_current_skill(self):
        decision = self._decision()
        judgments = ProjectJudgments("条件候选", True, False, 4, ())
        decision = ReviewDecision(decision.observed_facts, judgments, candidate_id=decision.candidate_id)
        packet = self._packet(decision)
        observation = {
            "观察标识": "OBS-org/example-条件候选", "内部标识": "org/example", "候选名称": "example", "Canonical source": decision.observed_facts.canonical_source,
            "Skill入口路径": packet.skill_entry_path,
            "观察状态": "条件候选", "许可证": decision.observed_facts.license,
            "记录日期": "2026-08-27", "原因": "仍待人工条件复核",
            "固定版本": decision.observed_facts.fixed_version,
            "固定版本内容指纹": packet.fixed_content_hash,
            "验证证据位置": "；".join(decision.observed_facts.evidence_paths), "显示层级": "条件候选",
        }
        body = json.dumps({"decisions": [self._payload(decision, ledger_row=observation)]}, ensure_ascii=False).encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            apply_reviews_from_stream(io.BytesIO(body), store, {"org/example": packet})
            self.assertEqual(store.rows("当前Skill"), [])
            self.assertEqual(store.rows("候选观察")[0]["观察状态"], "条件候选")

    def test_application_routes_formal_recommendation_to_current_skill_only(self):
        decision = self._decision()
        packet = self._packet(decision)
        formal_row = self._formal_row(decision, packet)
        body = json.dumps({"decisions": [self._payload(decision, ledger_row=formal_row)]}, ensure_ascii=False).encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            apply_reviews_from_stream(io.BytesIO(body), store, {"org/example": packet})
            self.assertEqual(store.rows("当前Skill")[0]["内部标识"], "org/example")
            self.assertEqual(store.rows("候选观察"), [])
            self.assertEqual(store.validate(), [])

    def test_remote_endpoint_and_remote_api_flag_must_not_conflict(self):
        errors = validate_review(self._decision(remote_endpoints=("https://api.example",)))
        self.assertIn("observed_facts.remote_endpoints: remote API 标记为否时不得填写远程端点", errors)

    def test_unknown_license_cannot_be_formal(self):
        errors = validate_review(self._decision(license="unknown"))
        self.assertIn("observed_facts.license: 正式条目许可证未明确", errors)

    def test_sb_a_cannot_be_directly_deployed(self):
        errors = validate_review(self._decision(security_grade="SB-A"))
        self.assertIn("project_judgments.direct_deployable: SB-A 原包不得直接部署", errors)

    def test_relevance_two_is_not_product_displayable(self):
        decision = self._decision()
        decision = ReviewDecision(decision.observed_facts, ProjectJudgments("正式推荐", True, True, 2, ()), decision.derived_fields, decision.candidate_id)
        errors = validate_review(decision)
        self.assertIn("project_judgments.display_in_product: 相关度低于 3/5 不得展示", errors)

    def test_pending_verification_cannot_receive_sa_or_sb(self):
        errors = validate_review(self._decision(verification_status="待核验", security_grade="SA"))
        self.assertIn("observed_facts.security_grade: 待核验不得给出 SA/SB 正式等级", errors)

    def test_formal_requires_at_least_all_passed_not_tested(self):
        errors = validate_review(self._decision(verification_status="前两步通过"))
        self.assertIn("observed_facts.verification_status: 正式条目最低为全部通过（未实测）", errors)

    def test_quality_score_needs_exactly_all_four_admission_conditions_then_caps_bonuses_at_five(self):
        complete = self._decision()
        self.assertEqual(score_quality(complete), 5)
        missing = self._decision(entry_description_complete=False)
        self.assertEqual(score_quality(missing), 0)

    def test_derived_quality_score_cannot_override_observed_facts_or_project_judgments(self):
        decision = self._decision()
        decision = ReviewDecision(decision.observed_facts, decision.project_judgments, DerivedFields(quality_score=4), decision.candidate_id)
        self.assertIn(
            "derived_fields.quality_score: 必须由事实和项目判断重新计算",
            validate_review(decision),
        )

    def test_quality_score_is_zero_when_safety_license_or_traceability_fails_regardless_of_popularity(self):
        for decision in (
            self._decision(security_grade="SC"),
            self._decision(license="unknown"),
            self._decision(canonical_source="", evidence_paths=()),
        ):
            with self.subTest(decision=decision):
                self.assertEqual(score_quality(decision), 0)

    def test_review_stdin_is_decoded_in_memory_validated_and_applied_to_staged_ledger(self):
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            stream = io.BytesIO(json.dumps({"decisions": []}, ensure_ascii=False).encode("utf-8"))
            self.assertEqual(apply_reviews_from_stream(stream, store, {}), ())
            self.assertEqual(store.rows("当前Skill"), [])
            self.assertEqual(list(Path(temporary).glob("*.json")), [])

    def test_formal_applied_review_issues_a_registry_backed_content_bound_receipt(self):
        decision = self._decision()
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            packet = self._packet(decision)
            body = json.dumps({"decisions": [self._payload(decision, ledger_row=self._formal_row(decision, packet))]}, ensure_ascii=False).encode("utf-8")
            receipt, = apply_reviews_from_stream(io.BytesIO(body), store, {"org/example": packet})

        self.assertEqual(receipt.candidate_id, "org/example")
        self.assertEqual(receipt.fixed_content_hash, packet.fixed_content_hash)
        self.assertIs(validate_applied_review(receipt), receipt)
        fake = AppliedReview(
            receipt.candidate_id, receipt.fixed_version, receipt.canonical_source, receipt.license,
            receipt.security_grade, receipt.evidence_paths, receipt.fixed_content_hash,
        )
        with self.assertRaisesRegex(ValueError, "receipt"):
            validate_applied_review(fake)

    def test_self_constructed_packet_cannot_be_used_to_issue_a_receipt(self):
        decision = self._decision()
        packet = ReviewPacket(
            "org/example", decision.observed_facts.fixed_version, decision.observed_facts.canonical_source,
            decision.observed_facts.license, decision.observed_facts.security_grade,
            {"SKILL_RESEARCH_WORKFLOW": "1.4"}, decision.observed_facts.evidence_paths, ("SKILL.md",), "d" * 64,
        )
        body = json.dumps({"decisions": [self._payload(decision)]}, ensure_ascii=False).encode("utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            with self.assertRaisesRegex(ValueError, "受信"):
                apply_reviews_from_stream(io.BytesIO(body), store, {"org/example": packet})

    def test_self_constructed_snapshot_manifest_cannot_register_a_review_packet(self):
        decision = self._decision()
        forged_manifest = SnapshotManifest(
            "org/example", decision.observed_facts.fixed_version, Path("."), decision.observed_facts.evidence_paths,
            (), (), 0, "d" * 64,
        )

        with self.assertRaisesRegex(ValueError, "快照"):
            build_review_packet({
                "id": "org/example", "canonical_source": decision.observed_facts.canonical_source,
                "license": decision.observed_facts.license, "security_grade": decision.observed_facts.security_grade,
            }, forged_manifest)

    def test_copied_replaced_or_mutated_snapshot_manifest_cannot_register_a_review_packet(self):
        decision = self._decision()
        candidate = {
            "id": "org/example", "canonical_source": decision.observed_facts.canonical_source,
            "license": decision.observed_facts.license, "security_grade": decision.observed_facts.security_grade,
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "candidate"
            source.mkdir()
            (source / "SKILL.md").write_text("# evidence", encoding="utf-8")
            manifest = build_snapshot(SnapshotCandidate("org/example", decision.observed_facts.fixed_version, source, decision.observed_facts.evidence_paths), root / "snapshot")
            for forged in (copy(manifest), replace(manifest, fixed_content_hash="a" * 64)):
                with self.subTest(kind=type(forged).__name__):
                    with self.assertRaisesRegex(ValueError, "快照"):
                        build_review_packet(candidate, forged)
            object.__setattr__(manifest, "fixed_version", "attacker-version")
            with self.assertRaisesRegex(ValueError, "快照"):
                build_review_packet(candidate, manifest)

    def test_clear_review_run_state_releases_packets_and_unconsumed_receipts(self):
        decision = self._decision()
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            packet = self._packet(decision)
            body = json.dumps({"decisions": [self._payload(decision, ledger_row=self._formal_row(decision, packet))]}, ensure_ascii=False).encode("utf-8")
            receipt, = apply_reviews_from_stream(io.BytesIO(body), store, {"org/example": packet})
            self.assertIs(validate_applied_review(receipt), receipt)
            review_module.clear_review_run_state()
            with self.assertRaisesRegex(ValueError, "receipt"):
                validate_applied_review(receipt)
            with self.assertRaisesRegex(ValueError, "受信"):
                apply_reviews_from_stream(io.BytesIO(body), store, {"org/example": packet})

    def test_review_stdin_rejects_string_booleans_instead_of_treating_them_as_true(self):
        with tempfile.TemporaryDirectory() as temporary:
            store = LedgerStore.create(Path(temporary) / "source.xlsx")
            payload = {
                "decisions": [{
                    "candidate_id": "org/example",
                    "observed_facts": {
                        "fixed_version": "a" * 40,
                        "entry_description_complete": "false",
                        "prerequisites_clear_and_available": True,
                        "license": "MIT",
                        "canonical_source": "https://github.com/org/example",
                        "evidence_paths": ["evidence/SKILL.md"],
                        "remote_api_call": "否",
                        "remote_endpoints": [],
                        "local_professional_software": "无",
                        "local_script_plugin_interface": "不使用",
                        "security_grade": "SA",
                        "verification_status": "全部通过（未实测）",
                    },
                    "project_judgments": {
                        "record_tier": "正式", "display_in_product": True, "direct_deployable": True,
                        "relevance_score": 4, "quality_bonus_flags": [],
                    },
                    "derived_fields": {},
                }]
            }
            with self.assertRaisesRegex(ValueError, "布尔"):
                apply_reviews_from_stream(io.BytesIO(json.dumps(payload).encode("utf-8")), store, {})


if __name__ == "__main__":
    unittest.main()
