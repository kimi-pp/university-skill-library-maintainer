"""Microsoft Office read-only verification and hash-bound visual evidence."""

from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import threading
from typing import Any, Iterable
import weakref

from .paths import assert_ordinary_path, is_link_or_reparse


class OfficeVerificationError(RuntimeError):
    """Office or render evidence is missing, stale, or unsafe."""


@dataclass(frozen=True)
class RendererCommand:
    """Explicit loader-supplied PDF renderer command.

    The command receives ``--pdf ABSOLUTE`` and ``--output-dir ABSOLUTE`` and
    prints one JSON object with ordered page paths and body-pixel counts.
    """

    argv: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.argv or any(not str(part) for part in self.argv):
            raise OfficeVerificationError("PDF 渲染器命令不能为空。")

    def render(self, pdf: Path, output_dir: Path) -> tuple[tuple[Path, ...], tuple[int, ...]]:
        completed = subprocess.run(
            [*self.argv, "--pdf", str(pdf), "--output-dir", str(output_dir)],
            check=False, capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        stdout = completed.stdout.strip().lstrip("\ufeff")
        lines = [line for line in stdout.splitlines() if line.strip()]
        if completed.returncode != 0 or len(lines) != 1:
            detail = completed.stderr.strip() or stdout or f"exit={completed.returncode}"
            raise OfficeVerificationError(f"显式 PDF 渲染器失败：{detail}")
        try:
            payload = json.loads(lines[0])
        except json.JSONDecodeError as exc:
            raise OfficeVerificationError("显式 PDF 渲染器返回无效 JSON。") from exc
        rows = payload.get("pages") if isinstance(payload, dict) else None
        if not isinstance(rows, list) or not rows:
            raise OfficeVerificationError("显式 PDF 渲染器没有返回页面。")
        paths: list[Path] = []
        body_pixels: list[int] = []
        for index, row in enumerate(rows, start=1):
            if not isinstance(row, dict):
                raise OfficeVerificationError("显式 PDF 渲染器页面记录无效。")
            relative = Path(str(row.get("path") or ""))
            if relative.is_absolute() or relative.parts != (f"page-{index}.png",):
                raise OfficeVerificationError("显式 PDF 渲染器页面路径或顺序不符合契约。")
            page = output_dir / relative
            if not page.is_file() or is_link_or_reparse(page):
                raise OfficeVerificationError("显式 PDF 渲染器页面缺失或不是普通文件。")
            assert_ordinary_path(page)
            try:
                count = int(row["body_nonwhite_pixels"])
            except (KeyError, TypeError, ValueError) as exc:
                raise OfficeVerificationError("显式 PDF 渲染器缺少正文区域像素判定。") from exc
            if count < 0:
                raise OfficeVerificationError("显式 PDF 渲染器正文区域像素判定无效。")
            paths.append(page)
            body_pixels.append(count)
        return tuple(paths), tuple(body_pixels)


@dataclass(frozen=True)
class OfficeCheck:
    kind: str
    source_path: Path
    source_sha256: str
    passed: bool
    office_passed: bool
    office_opened: bool
    read_only: bool
    excel_role: str | None = None
    key_sheet: str | None = None
    last_row: int | None = None
    last_column: int | None = None
    last_value: str | None = None
    pdf_path: Path | None = None
    pdf_sha256: str | None = None
    page_paths: tuple[Path, ...] = ()
    page_sha256: tuple[str, ...] = ()
    body_nonwhite_pixels: tuple[int, ...] = ()
    blank_pages: tuple[int, ...] = ()
    visual_reviewed: bool = False
    page_approved: tuple[bool, ...] = ()
    visual_reviewer: str | None = None
    process_count_before: int = 0
    process_count_after: int = 0
    error: str | None = None

    def __bool__(self) -> bool:
        return self.passed


@dataclass(frozen=True)
class WordPageDecision:
    page_number: int
    sha256: str
    approved: bool


@dataclass(frozen=True)
class WordRenderDecision:
    source_sha256: str
    pdf_sha256: str
    pages: tuple[WordPageDecision, ...]
    reviewer: str

    @classmethod
    def from_check(
        cls,
        check: OfficeCheck,
        *,
        approved: bool,
        reviewer: str,
        rejected_pages: tuple[int, ...] = (),
    ) -> "WordRenderDecision":
        if check.kind != "word" or not check.pdf_sha256 or not check.page_sha256:
            raise OfficeVerificationError("Word 渲染证据不完整，不能形成视觉判定。")
        if not reviewer.strip():
            raise OfficeVerificationError("逐页视觉判定必须记录复核者。")
        rejected = set(rejected_pages)
        if any(page < 1 or page > len(check.page_sha256) for page in rejected):
            raise OfficeVerificationError("视觉驳回页码越出当前渲染范围。")
        return cls(
            check.source_sha256,
            check.pdf_sha256,
            tuple(
                WordPageDecision(index, digest, approved and index not in rejected)
                for index, digest in enumerate(check.page_sha256, start=1)
            ),
            reviewer.strip(),
        )


@dataclass(frozen=True)
class OfficeRunScope:
    """Verifier-issued, object-identity capability for one staging tree."""

    run_id: str
    project_root: Path
    staging_root: Path


@dataclass(frozen=True)
class OfficeEvidenceBundle:
    """Exact Office evidence for every Word/Excel artifact in a commit."""

    checks: tuple[OfficeCheck, ...]
    scope: OfficeRunScope
    sha256: str

    @property
    def run_id(self) -> str:
        return self.scope.run_id

    @classmethod
    def from_checks(
        cls,
        checks: Iterable[OfficeCheck],
        *,
        scope: OfficeRunScope,
    ) -> "OfficeEvidenceBundle":
        frozen = tuple(checks)
        with _OFFICE_REGISTRY_LOCK:
            _require_trusted_scope(scope)
            seen: set[Path] = set()
            records: list[_CheckRecord] = []
            for check in frozen:
                source = check.source_path.absolute()
                if source in seen:
                    raise OfficeVerificationError(f"Office 证据重复绑定同一文件：{source}")
                seen.add(source)
                _require_trusted_check(check, scope, final=True, issued=False)
                _validate_check(check)
                record = _TRUSTED_CHECKS[id(check)]
                _assert_check_within_scope(check, scope)
                records.append(record)
            if not records or any(record.scope_identity != id(scope) for record in records):
                raise OfficeVerificationError("同一 OfficeEvidenceBundle 的全部证据必须位于同一暂存作用域。")
            bundle = cls(frozen, scope, _evidence_digest(frozen, scope))
            try:
                _register_bundle(bundle, scope)
                for record in records:
                    record.issued = True
                return bundle
            except BaseException:
                _TRUSTED_BUNDLES.pop(id(bundle), None)
                for record in records:
                    record.issued = False
                raise

    def assert_covers(self, paths: Iterable[str | Path]) -> None:
        with _OFFICE_REGISTRY_LOCK:
            _require_trusted_bundle(self, self.scope)
            required = {
                Path(path).absolute()
                for path in paths
                if Path(path).suffix.casefold() in {".xlsx", ".docx"}
            }
            supplied = {check.source_path.absolute() for check in self.checks}
            if required != supplied:
                missing = sorted(str(path) for path in required - supplied)
                extra = sorted(str(path) for path in supplied - required)
                raise OfficeVerificationError(f"Office 证据未精确覆盖发布文件；缺失={missing}；多余={extra}")
            for check in self.checks:
                _validate_check(check)
                _assert_check_within_scope(check, self.scope)

    def assert_publication_roles(
        self,
        staged_ledger: str | Path,
        paths: Iterable[str | Path],
    ) -> None:
        """Bind each approved Office kind/role to its exact publication path."""

        ledger = Path(staged_ledger).absolute()
        supplied_paths = tuple(Path(path).absolute() for path in paths)
        with _OFFICE_REGISTRY_LOCK:
            self.assert_covers(supplied_paths)
            _assert_paths_within_scope(supplied_paths, self.scope)
            if ledger.parent.resolve(strict=True) != self.scope.staging_root:
                raise OfficeVerificationError("暂存主台账必须直接位于当前 verifier 暂存作用域根目录。")
            checks = {check.source_path.absolute(): check for check in self.checks}
            ledger_check = checks.get(ledger)
            if ledger_check is None or ledger_check.kind != "excel" or ledger_check.excel_role != "ledger":
                raise OfficeVerificationError("暂存主台账必须绑定 kind=excel、role=ledger 的受信证据。")
            for path in supplied_paths:
                if path == ledger:
                    continue
                check = checks.get(path)
                suffix = path.suffix.casefold()
                if suffix == ".xlsx" and (
                    check is None or check.kind != "excel" or check.excel_role != "daily"
                ):
                    raise OfficeVerificationError(f"交付 Excel 必须绑定 kind=excel、role=daily：{path}")
                if suffix == ".docx" and (check is None or check.kind != "word"):
                    raise OfficeVerificationError(f"交付 Word 必须绑定 kind=word：{path}")


@dataclass
class _CheckRecord:
    check: weakref.ReferenceType[OfficeCheck]
    scope: weakref.ReferenceType[OfficeRunScope]
    scope_identity: int
    final: bool
    facts: tuple[object, ...]
    issued: bool = False


@dataclass
class _BundleRecord:
    bundle: weakref.ReferenceType[OfficeEvidenceBundle]
    scope: weakref.ReferenceType[OfficeRunScope]
    scope_identity: int
    facts: tuple[object, ...]


@dataclass
class _ScopeRecord:
    scope: weakref.ReferenceType[OfficeRunScope]
    facts: tuple[object, ...]
    chain_identities: tuple[tuple[Path, tuple[int, int, int, int]], ...]
    active: bool = True


_TRUSTED_CHECKS: dict[int, _CheckRecord] = {}
_TRUSTED_BUNDLES: dict[int, _BundleRecord] = {}
_TRUSTED_SCOPES: dict[int, _ScopeRecord] = {}
_OFFICE_REGISTRY_LOCK = threading.RLock()


def assert_office_evidence_owner(
    bundle: object,
    *,
    scope: OfficeRunScope,
) -> OfficeEvidenceBundle:
    """Authenticate object ownership without accepting copied cross-scope inputs.

    This deliberately does not re-read artifact files or the staging chain.  A
    publication owner can therefore claim its exact registry objects first,
    then clear only that token if later hash/path validation fails.
    """

    with _OFFICE_REGISTRY_LOCK:
        scope_record = _owned_scope_record(scope)
        if not scope_record.active:
            raise OfficeVerificationError("OfficeRunScope 已清理，不能再次签发或消费证据。")
        record = _TRUSTED_BUNDLES.get(id(bundle))
        if (
            not isinstance(bundle, OfficeEvidenceBundle)
            or record is None
            or record.bundle() is not bundle
            or bundle.scope is not scope
            or record.scope() is not scope
            or record.scope_identity != id(scope)
            or record.facts != _bundle_facts(bundle)
        ):
            raise OfficeVerificationError("OfficeEvidenceBundle 不属于给定 OfficeRunScope token。")
        for check in bundle.checks:
            check_record = _TRUSTED_CHECKS.get(id(check))
            if (
                check_record is None
                or check_record.check() is not check
                or check_record.scope() is not scope
                or check_record.scope_identity != id(scope)
                or not check_record.final
                or not check_record.issued
                or check_record.facts != _check_facts(check)
            ):
                raise OfficeVerificationError("OfficeEvidenceBundle 包含非本 token 签发的 Check。")
        return bundle


def consume_office_evidence(
    bundle: object,
    *,
    scope: OfficeRunScope,
) -> OfficeEvidenceBundle:
    """Consume the exact token-bound evidence immediately before authority replace."""

    with _OFFICE_REGISTRY_LOCK:
        trusted = _require_trusted_bundle(bundle, scope)
        _TRUSTED_BUNDLES.pop(id(trusted), None)
        return trusted


def clear_office_run_state(
    *,
    scope: OfficeRunScope,
) -> None:
    """Release only the capabilities owned by one exact issued scope token."""

    with _OFFICE_REGISTRY_LOCK:
        _owned_scope_record(scope)
        scope_identity = id(scope)
        for identity, record in tuple(_TRUSTED_CHECKS.items()):
            if record.scope_identity == scope_identity:
                _TRUSTED_CHECKS.pop(identity, None)
        for identity, record in tuple(_TRUSTED_BUNDLES.items()):
            if record.scope_identity == scope_identity:
                _TRUSTED_BUNDLES.pop(identity, None)
        # Keep only the exact object-identity tombstone until the token itself
        # is collected.  This makes nested owners' finally cleanup idempotent
        # without making a copied/reconstructed token clearable.
        record = _TRUSTED_SCOPES[scope_identity]
        record.active = False


def _required_run_id(run_id: str) -> str:
    normalized = str(run_id).strip()
    if not normalized:
        raise OfficeVerificationError("Office verifier capability 必须绑定非空运行标识。")
    return normalized


def _ordinary_canonical_directory(path: str | Path, *, label: str) -> Path:
    supplied = Path(path).absolute()
    if not supplied.is_dir() or is_link_or_reparse(supplied):
        raise OfficeVerificationError(f"{label}必须是存在的普通目录：{supplied}")
    try:
        assert_ordinary_path(supplied, require_directory=True)
    except ValueError as exc:
        raise OfficeVerificationError(f"{label}不得包含链接或重解析点：{supplied}") from exc
    canonical = supplied.resolve(strict=True)
    if supplied != canonical:
        raise OfficeVerificationError(f"{label}必须使用规范路径，不接受别名或链接：{supplied}")
    return canonical


def _path_lstat_identity(path: Path) -> tuple[int, int, int, int]:
    result = path.lstat()
    return (
        getattr(result, "st_dev", 0), getattr(result, "st_ino", 0),
        result.st_mode, getattr(result, "st_file_attributes", 0),
    )


def _scope_chain(
    project_root: str | Path,
    staging_root: str | Path,
) -> tuple[Path, Path, tuple[tuple[Path, tuple[int, int, int, int]], ...]]:
    project = _ordinary_canonical_directory(project_root, label="Office 项目根目录")
    staging = _ordinary_canonical_directory(staging_root, label="Office 暂存根目录")
    try:
        relative = staging.relative_to(project)
    except ValueError as exc:
        raise OfficeVerificationError("Office 暂存根目录越出项目根目录。") from exc
    if not relative.parts:
        raise OfficeVerificationError("Office 暂存根目录不能等于项目根目录。")
    chain: list[Path] = [project]
    current = project
    for part in relative.parts:
        current = current / part
        if not current.is_dir() or is_link_or_reparse(current):
            raise OfficeVerificationError(f"Office 暂存父链必须是普通目录：{current}")
        chain.append(current)
    return project, staging, tuple((path, _path_lstat_identity(path)) for path in chain)


def _scope_facts(scope: object) -> tuple[object, ...]:
    if not isinstance(scope, OfficeRunScope):
        return ()
    return (scope.run_id, scope.project_root, scope.staging_root)


def issue_office_run_scope(
    *,
    run_id: str,
    staging_root: str | Path,
    project_root: str | Path,
) -> OfficeRunScope:
    """Issue one unique verifier capability for an ordinary contained staging tree."""

    normalized_run_id = _required_run_id(run_id)
    project, staging, identities = _scope_chain(project_root, staging_root)
    scope = OfficeRunScope(normalized_run_id, project, staging)
    identity = id(scope)

    def _discard(reference: weakref.ReferenceType[OfficeRunScope]) -> None:
        with _OFFICE_REGISTRY_LOCK:
            record = _TRUSTED_SCOPES.get(identity)
            if record is not None and record.scope is reference:
                for check_id, check_record in tuple(_TRUSTED_CHECKS.items()):
                    if check_record.scope_identity == identity:
                        _TRUSTED_CHECKS.pop(check_id, None)
                for bundle_id, bundle_record in tuple(_TRUSTED_BUNDLES.items()):
                    if bundle_record.scope_identity == identity:
                        _TRUSTED_BUNDLES.pop(bundle_id, None)
                _TRUSTED_SCOPES.pop(identity, None)

    with _OFFICE_REGISTRY_LOCK:
        _TRUSTED_SCOPES[identity] = _ScopeRecord(
            weakref.ref(scope, _discard), _scope_facts(scope), identities,
        )
    return scope


def _owned_scope_record(scope: object) -> _ScopeRecord:
    record = _TRUSTED_SCOPES.get(id(scope))
    if (
        not isinstance(scope, OfficeRunScope)
        or record is None
        or record.scope() is not scope
        or record.facts != _scope_facts(scope)
    ):
        raise OfficeVerificationError("OfficeRunScope 必须由当前 verifier 真实签发且未清理。")
    return record


def _require_trusted_scope(scope: object) -> OfficeRunScope:
    record = _owned_scope_record(scope)
    if not record.active:
        raise OfficeVerificationError("OfficeRunScope 已清理，不能再次签发或消费证据。")
    project, staging, identities = _scope_chain(scope.project_root, scope.staging_root)
    if project != scope.project_root or staging != scope.staging_root or identities != record.chain_identities:
        raise OfficeVerificationError("OfficeRunScope 的项目/暂存父链身份已变化。")
    return scope


def _assert_paths_within_scope(paths: Iterable[str | Path], scope: OfficeRunScope) -> None:
    _require_trusted_scope(scope)
    for value in paths:
        path = Path(value).absolute()
        if not path.is_file() or is_link_or_reparse(path):
            raise OfficeVerificationError(f"Office 证据作用域内必须是普通文件：{path}")
        try:
            assert_ordinary_path(path)
            path.resolve(strict=True).relative_to(scope.staging_root)
        except (OSError, ValueError) as exc:
            raise OfficeVerificationError(f"Office 证据越出当前暂存作用域：{path}") from exc


def _assert_check_within_scope(check: OfficeCheck, scope: OfficeRunScope) -> None:
    paths: tuple[Path, ...] = (
        check.source_path,
        *((check.pdf_path,) if check.pdf_path is not None else ()),
        *check.page_paths,
    )
    _assert_paths_within_scope(paths, scope)


def _register_check(check: OfficeCheck, scope: OfficeRunScope, *, final: bool) -> None:
    identity = id(check)
    _require_trusted_scope(scope)
    _assert_check_within_scope(check, scope)

    def _discard(reference: weakref.ReferenceType[OfficeCheck]) -> None:
        with _OFFICE_REGISTRY_LOCK:
            record = _TRUSTED_CHECKS.get(identity)
            if record is not None and record.check is reference:
                _TRUSTED_CHECKS.pop(identity, None)

    with _OFFICE_REGISTRY_LOCK:
        _TRUSTED_CHECKS[identity] = _CheckRecord(
            weakref.ref(check, _discard), weakref.ref(scope), id(scope), final, _check_facts(check),
        )


def _require_trusted_check(
    check: object,
    scope: OfficeRunScope,
    *,
    final: bool,
    issued: bool | None = None,
) -> OfficeCheck:
    _require_trusted_scope(scope)
    record = _TRUSTED_CHECKS.get(id(check))
    if (
        not isinstance(check, OfficeCheck)
        or record is None
        or record.check() is not check
        or record.scope() is not scope
        or record.scope_identity != id(scope)
        or record.final is not final
        or (issued is not None and record.issued is not issued)
        or record.facts != _check_facts(check)
    ):
        raise OfficeVerificationError("OfficeCheck 必须由当前运行的真实 verifier capability 单次签发且未篡改。")
    return check


def _register_bundle(bundle: OfficeEvidenceBundle, scope: OfficeRunScope) -> None:
    identity = id(bundle)

    def _discard(reference: weakref.ReferenceType[OfficeEvidenceBundle]) -> None:
        with _OFFICE_REGISTRY_LOCK:
            record = _TRUSTED_BUNDLES.get(identity)
            if record is not None and record.bundle is reference:
                _TRUSTED_BUNDLES.pop(identity, None)

    with _OFFICE_REGISTRY_LOCK:
        _TRUSTED_BUNDLES[identity] = _BundleRecord(
            weakref.ref(bundle, _discard), weakref.ref(scope), id(scope), _bundle_facts(bundle),
        )


def _require_trusted_bundle(bundle: object, scope: OfficeRunScope) -> OfficeEvidenceBundle:
    _require_trusted_scope(scope)
    record = _TRUSTED_BUNDLES.get(id(bundle))
    if (
        not isinstance(bundle, OfficeEvidenceBundle)
        or record is None
        or record.bundle() is not bundle
        or bundle.scope is not scope
        or record.scope() is not scope
        or record.scope_identity != id(scope)
        or record.facts != _bundle_facts(bundle)
    ):
        raise OfficeVerificationError("OfficeEvidenceBundle 不是当前运行真实签发且未消费的受信 capability。")
    for check in bundle.checks:
        _require_trusted_check(check, scope, final=True, issued=True)
        if _TRUSTED_CHECKS[id(check)].scope_identity != record.scope_identity:
            raise OfficeVerificationError("OfficeEvidenceBundle 的 Check 暂存作用域不一致。")
    return bundle


def _check_facts(check: object) -> tuple[object, ...]:
    if not isinstance(check, OfficeCheck):
        return ()
    return (
        check.kind, check.source_path.absolute(), check.source_sha256, check.passed,
        check.office_passed, check.office_opened, check.read_only, check.excel_role,
        check.key_sheet, check.last_row, check.last_column, check.last_value,
        check.pdf_path.absolute() if check.pdf_path else None, check.pdf_sha256,
        tuple(path.absolute() for path in check.page_paths), tuple(check.page_sha256),
        tuple(check.body_nonwhite_pixels), tuple(check.blank_pages), check.visual_reviewed,
        tuple(check.page_approved), check.visual_reviewer, check.process_count_before,
        check.process_count_after, check.error,
    )


def _evidence_digest(checks: tuple[OfficeCheck, ...], scope: OfficeRunScope) -> str:
    records = [{
        "run_id": scope.run_id,
        "project_root": str(scope.project_root),
        "staging_root": str(scope.staging_root),
        "kind": check.kind,
        "source_path": str(check.source_path.absolute()),
        "source_sha256": check.source_sha256,
        "passed": check.passed,
        "office_passed": check.office_passed,
        "office_opened": check.office_opened,
        "read_only": check.read_only,
        "excel_role": check.excel_role,
        "key_sheet": check.key_sheet,
        "last_row": check.last_row,
        "last_column": check.last_column,
        "last_value": check.last_value,
        "pdf_path": str(check.pdf_path.absolute()) if check.pdf_path else None,
        "pdf_sha256": check.pdf_sha256,
        "page_paths": [str(path.absolute()) for path in check.page_paths],
        "page_sha256": list(check.page_sha256),
        "body_nonwhite_pixels": list(check.body_nonwhite_pixels),
        "blank_pages": list(check.blank_pages),
        "visual_reviewed": check.visual_reviewed,
        "page_approved": list(check.page_approved),
        "visual_reviewer": check.visual_reviewer,
        "process_count_before": check.process_count_before,
        "process_count_after": check.process_count_after,
        "error": check.error,
    } for check in checks]
    encoded = json.dumps(records, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded).hexdigest()


def _bundle_facts(bundle: object) -> tuple[object, ...]:
    if not isinstance(bundle, OfficeEvidenceBundle):
        return ()
    return (
        id(bundle.scope), _scope_facts(bundle.scope), tuple(id(check) for check in bundle.checks),
        tuple(_check_facts(check) for check in bundle.checks), bundle.sha256,
        _evidence_digest(bundle.checks, bundle.scope),
    )


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_check(check: OfficeCheck) -> None:
    source = check.source_path.absolute()
    if check.kind not in {"excel", "word"}:
        raise OfficeVerificationError("Office 证据类型必须是 excel 或 word。")
    if not check.passed or not check.office_passed or not check.office_opened or not check.read_only:
        raise OfficeVerificationError(f"Office 证据未完整通过：{source}")
    if check.process_count_before != check.process_count_after:
        raise OfficeVerificationError(f"Office 进程未精确返回基线：{source}")
    if not source.is_file() or is_link_or_reparse(source) or _sha256(source) != check.source_sha256:
        raise OfficeVerificationError(f"Office 源文件缺失或哈希已变化：{source}")
    if check.kind == "excel":
        expected = {
            "ledger": {"当前Skill", "运行记录"},
            "daily": {"执行概览"},
        }
        if check.excel_role not in expected or check.key_sheet not in expected[check.excel_role]:
            raise OfficeVerificationError(f"Excel 关键工作表未绑定文件角色：{source}")
        if not check.last_row or check.last_row < 2 or not check.last_column or not (check.last_value or "").strip():
            raise OfficeVerificationError(f"Excel 关键工作表没有正式数据行：{source}")
    else:
        if not check.visual_reviewed or check.blank_pages:
            raise OfficeVerificationError(f"Word 未完成逐页视觉批准：{source}")
        if not check.pdf_path or not check.pdf_sha256 or not check.page_paths:
            raise OfficeVerificationError(f"Word PDF/逐页证据不完整：{source}")
        if not (
            len(check.page_paths)
            == len(check.page_sha256)
            == len(check.body_nonwhite_pixels)
        ):
            raise OfficeVerificationError(f"Word 逐页证据数量不一致：{source}")
        if any(count <= 0 for count in check.body_nonwhite_pixels):
            raise OfficeVerificationError(f"Word 逐页正文像素证据无效：{source}")
        if check.page_approved != (True,) * len(check.page_sha256) or not (check.visual_reviewer or "").strip():
            raise OfficeVerificationError(f"Word 逐页批准枚举或复核者证据不完整：{source}")
        evidence = ((check.pdf_path, check.pdf_sha256), *zip(check.page_paths, check.page_sha256))
        for path, digest in evidence:
            if not path.is_file() or is_link_or_reparse(path) or _sha256(path) != digest:
                raise OfficeVerificationError(f"Word PDF/逐页证据缺失或哈希已变化：{path}")


def _ordinary_file(path: str | Path, suffix: str) -> Path:
    target = Path(path).absolute()
    if target.suffix.casefold() != suffix or not target.is_file() or is_link_or_reparse(target):
        raise OfficeVerificationError(f"必须提供普通 {suffix} 文件：{target}")
    assert_ordinary_path(target)
    return target


def _powershell() -> str:
    executable = shutil.which("powershell.exe") or shutil.which("powershell")
    if not executable:
        raise OfficeVerificationError("未找到 Windows PowerShell，无法执行 Office COM 复读。")
    return executable


def _script_path() -> Path:
    path = Path(__file__).resolve().parents[2] / "verify_office.ps1"
    if not path.is_file():
        raise OfficeVerificationError(f"缺少 Office 验证脚本：{path}")
    return path


def _run_office(*arguments: str) -> dict[str, Any]:
    if os.name != "nt":
        raise OfficeVerificationError("Microsoft Office COM 验证只支持 Windows。")
    command = [
        _powershell(), "-NoLogo", "-NoProfile", "-NonInteractive",
        "-ExecutionPolicy", "Bypass", "-File", str(_script_path()), *arguments,
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8", errors="replace")
    stdout = completed.stdout.strip().lstrip("\ufeff")
    lines = [line for line in stdout.splitlines() if line.strip()]
    if completed.returncode != 0 or len(lines) != 1:
        detail = completed.stderr.strip() or stdout or f"exit={completed.returncode}"
        raise OfficeVerificationError(f"Office 验证脚本没有返回唯一 JSON 结果：{detail}")
    try:
        result = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise OfficeVerificationError("Office 验证脚本返回了无效 JSON。") from exc
    if not isinstance(result, dict):
        raise OfficeVerificationError("Office 验证脚本结果必须是对象。")
    return result


def verify_excel(
    path: str | Path,
    *,
    scope: OfficeRunScope | None = None,
    role: str = "ledger",
) -> OfficeCheck:
    source = _ordinary_file(path, ".xlsx")
    if role not in {"ledger", "daily"}:
        raise OfficeVerificationError("Excel 文件角色只能为 ledger 或 daily。")
    source_hash = _sha256(source)
    result = _run_office("-Excel", str(source), "-ExcelRole", role)
    before = int(result.get("process_count_before") or 0)
    after = int(result.get("process_count_after") or 0)
    exact_baseline = before == after
    key_sheet = _optional_text(result.get("key_sheet"))
    last_row = _optional_int(result.get("last_row"))
    last_column = _optional_int(result.get("last_column"))
    last_value = _optional_text(result.get("last_value"))
    expected_sheets = {"ledger": {"当前Skill", "运行记录"}, "daily": {"执行概览"}}
    role_bound = key_sheet in expected_sheets[role]
    populated = bool(last_row and last_row >= 2 and last_column and last_value)
    passed = bool(result.get("passed")) and exact_baseline and role_bound and populated
    error = _friendly_error(result.get("error"))
    if not exact_baseline:
        error = "Excel COM 进程未精确返回验证前基线。"
    elif not role_bound:
        error = "缺少与文件角色匹配的关键工作表。"
    elif not populated:
        error = "关键工作表没有非空数据行或末尾数据单元格为空。"
    check = OfficeCheck(
        kind="excel", source_path=source, source_sha256=source_hash,
        passed=passed, office_passed=passed,
        office_opened=bool(result.get("office_opened")), read_only=bool(result.get("read_only")),
        excel_role=role,
        key_sheet=key_sheet, last_row=last_row, last_column=last_column, last_value=last_value,
        process_count_before=before, process_count_after=after, error=error,
    )
    if scope is not None and check.passed:
        _register_check(check, scope, final=True)
    return check


def verify_word(
    path: str | Path,
    render_dir: str | Path,
    *,
    renderer: RendererCommand,
    scope: OfficeRunScope | None = None,
) -> OfficeCheck:
    source = _ordinary_file(path, ".docx")
    source_hash = _sha256(source)
    render = Path(render_dir).absolute()
    if render.exists():
        assert_ordinary_path(render, require_directory=True)
        if any(render.iterdir()):
            raise OfficeVerificationError("Word 逐页渲染目录必须是空目录，拒绝覆盖既有文件。")
    else:
        render.mkdir(parents=True, exist_ok=False)
        assert_ordinary_path(render, require_directory=True)
    result = _run_office("-Word", str(source), "-RenderDirectory", str(render))
    before = int(result.get("process_count_before") or 0)
    after = int(result.get("process_count_after") or 0)
    exact_baseline = before == after
    office_passed = bool(result.get("passed")) and exact_baseline
    pdf_text = _optional_text(result.get("pdf_path"))
    if not office_passed or not pdf_text:
        error = _friendly_error(result.get("error")) or "Word Office 复读失败。"
        if not exact_baseline:
            error = "Word COM 进程未精确返回验证前基线。"
        check = OfficeCheck(
            kind="word", source_path=source, source_sha256=source_hash,
            passed=False, office_passed=False, office_opened=bool(result.get("office_opened")),
            read_only=bool(result.get("read_only")), process_count_before=before,
            process_count_after=after, error=error,
        )
        return check
    pdf = Path(pdf_text).absolute()
    try:
        pdf.relative_to(render)
        if not pdf.is_file() or is_link_or_reparse(pdf):
            raise OfficeVerificationError("Word PDF 不是渲染目录内的普通文件。")
        pages, body_pixels = renderer.render(pdf, render)
        page_hashes = tuple(_sha256(page) for page in pages)
        blank_pages = tuple(index for index, count in enumerate(body_pixels, start=1) if count == 0)
        reported_pages = int(result.get("page_count") or 0)
        if not pages or (reported_pages and len(pages) != reported_pages):
            raise OfficeVerificationError("Word 报告页数与逐页图像不一致或没有页面。")
        error = "逐页图像已生成；必须绑定外部视觉复核通过判定后方可发布。"
        if blank_pages:
            error = f"逐页渲染检测到无正文页面：{','.join(map(str, blank_pages))}"
        check = OfficeCheck(
            kind="word", source_path=source, source_sha256=source_hash,
            passed=False, office_passed=True, office_opened=bool(result.get("office_opened")),
            read_only=bool(result.get("read_only")), pdf_path=pdf, pdf_sha256=_sha256(pdf),
            page_paths=pages, page_sha256=page_hashes, body_nonwhite_pixels=body_pixels,
            blank_pages=blank_pages, process_count_before=before, process_count_after=after,
            error=error,
        )
        if scope is not None and check.office_passed:
            _register_check(check, scope, final=False)
        return check
    except OfficeVerificationError as exc:
        return OfficeCheck(
            kind="word", source_path=source, source_sha256=source_hash,
            passed=False, office_passed=False, office_opened=bool(result.get("office_opened")),
            read_only=bool(result.get("read_only")), pdf_path=pdf if pdf.is_file() else None,
            pdf_sha256=_sha256(pdf) if pdf.is_file() else None,
            process_count_before=before, process_count_after=after, error=str(exc),
        )


def bind_word_visual_decision(
    check: OfficeCheck,
    decision: WordRenderDecision,
    *,
    scope: OfficeRunScope,
) -> OfficeCheck:
    if not isinstance(decision, WordRenderDecision):
        raise OfficeVerificationError("Word 视觉判定必须使用结构化逐页决定。")
    with _OFFICE_REGISTRY_LOCK:
        record = _TRUSTED_CHECKS.get(id(check))
        if record is None:
            raise OfficeVerificationError("Word OfficeCheck 必须由真实 verifier capability 签发后才能绑定视觉判定。")
        _require_trusted_check(check, scope, final=False, issued=False)
    if check.kind != "word" or not check.office_passed:
        raise OfficeVerificationError("只有完成 Word Office/PDF/逐页渲染的结果可以绑定视觉判定。")
    if check.process_count_before != check.process_count_after:
        raise OfficeVerificationError("Word COM 进程未精确返回验证前基线。")
    if check.blank_pages:
        raise OfficeVerificationError("Word 逐页图像包含空白正文页，不能批准发布。")
    if not check.pdf_path or not check.page_paths or len(check.page_paths) != len(check.page_sha256):
        raise OfficeVerificationError("Word PDF 或逐页图像证据缺失。")
    evidence_paths = (check.source_path, check.pdf_path, *check.page_paths)
    if any(not path.is_file() or is_link_or_reparse(path) for path in evidence_paths):
        raise OfficeVerificationError("Word 源文档、PDF 或逐页图像证据缺失。")
    if check.source_sha256 != _sha256(check.source_path):
        raise OfficeVerificationError("Word 源文档哈希已变化。")
    if check.pdf_sha256 != _sha256(check.pdf_path):
        raise OfficeVerificationError("Word PDF 哈希已变化。")
    current_page_hashes = tuple(_sha256(path) for path in check.page_paths)
    if current_page_hashes != check.page_sha256:
        raise OfficeVerificationError("Word 逐页图像哈希已变化。")
    expected = tuple((index, digest) for index, digest in enumerate(check.page_sha256, start=1))
    actual = tuple((page.page_number, page.sha256) for page in decision.pages)
    if decision.source_sha256 != check.source_sha256 or decision.pdf_sha256 != check.pdf_sha256:
        raise OfficeVerificationError("外部视觉判定未绑定当前 Word/PDF 哈希。")
    if actual != expected:
        raise OfficeVerificationError("外部视觉判定必须逐页枚举并绑定每一页精确哈希。")
    if not decision.reviewer.strip():
        raise OfficeVerificationError("外部逐页视觉判定必须绑定非空复核者。")
    approved = bool(decision.pages) and all(page.approved for page in decision.pages)
    approved_check = replace(
        check,
        passed=approved,
        visual_reviewed=True,
        page_approved=tuple(page.approved for page in decision.pages),
        visual_reviewer=decision.reviewer,
        error=None if approved else "外部逐页视觉复核未通过。",
    )
    with _OFFICE_REGISTRY_LOCK:
        _require_trusted_check(check, scope, final=False, issued=False)
        _TRUSTED_CHECKS.pop(id(check), None)
        if approved_check.passed:
            _register_check(approved_check, scope, final=True)
    return approved_check


def _optional_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    return int(value)


def _friendly_error(value: object) -> str | None:
    text = _optional_text(value)
    if text is None:
        return None
    messages = {
        "excel-not-read-only": "Excel 未以只读方式打开。",
        "excel-no-data-row": "关键工作表没有非空数据行或末尾数据单元格为空。",
        "excel-key-sheet-missing": "缺少与文件角色匹配的关键工作表。",
        "excel-process-leak": "Excel COM 进程未精确返回验证前基线。",
        "word-not-read-only": "Word 未以只读方式打开。",
        "word-pdf-empty-or-missing": "Word PDF 导出为空或缺失。",
        "word-pdf-stability-timeout": "Word PDF 导出后未在有界等待内稳定。",
        "word-pdf-target-exists": "Word PDF 目标在验证期间已存在，拒绝覆盖。",
        "word-process-leak": "Word COM 进程未精确返回验证前基线。",
    }
    return messages.get(text, text)
