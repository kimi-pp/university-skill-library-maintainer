import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { validateBundle } from "./mapping_schema.mjs";

const BLOCKING = "阻断";
const REVIEW = "需复核";
const NOTICE = "提示";
const PENDING_REVIEW = "尚未完成复核";
const EXPERT_REVIEW = "存在歧义，建议学科专家复核";
const CATALOG_CONFLICT = "目录版本差异待处理";
const CONFIRMED_ZERO = "已确认无直接对应";

const SEVERITY_RANK = new Map([
  [BLOCKING, 0],
  [REVIEW, 1],
  [NOTICE, 2],
]);

export class MappingBundleBuildError extends Error {
  constructor(message, qaFindings, cause = undefined) {
    super(message, cause === undefined ? undefined : { cause });
    this.name = "MappingBundleBuildError";
    this.qa_findings = qaFindings;
  }
}

function fail(message) {
  throw new TypeError(`映射聚合输入无效：${message}`);
}

function requireObject(value, field) {
  if (!value || typeof value !== "object" || Array.isArray(value)) fail(`${field} 必须是对象`);
  return value;
}

function recordsOf(value, field) {
  if (Array.isArray(value)) return value;
  requireObject(value, field);
  if (!Array.isArray(value.records)) fail(`${field}.records 必须是数组`);
  return value.records;
}

function requireArray(value, field) {
  if (!Array.isArray(value)) fail(`${field} 必须是数组`);
  return value;
}

function compareText(left, right) {
  return String(left).localeCompare(String(right), "en");
}

function graduateKey(type, code) {
  return `${type}|${code}`;
}

function relationshipKey(mapping) {
  return `${mapping.undergraduate_code}|${mapping.graduate_type}|${mapping.graduate_code}`;
}

function countBy(records, field, preferredOrder = []) {
  const counts = new Map();
  for (const record of records) {
    const value = record[field];
    counts.set(value, (counts.get(value) ?? 0) + 1);
  }
  const rank = new Map(preferredOrder.map((value, index) => [value, index]));
  return Object.fromEntries(
    [...counts].sort(([left], [right]) =>
      (rank.get(left) ?? Number.MAX_SAFE_INTEGER) - (rank.get(right) ?? Number.MAX_SAFE_INTEGER)
      || compareText(left, right)
    ),
  );
}

function sameStringSet(left, right) {
  if (left.length !== right.length) return false;
  const leftSet = new Set(left);
  const rightSet = new Set(right);
  return leftSet.size === left.length
    && rightSet.size === right.length
    && [...leftSet].every((value) => rightSet.has(value));
}

function uniqueSorted(values, comparator = compareText) {
  return [...new Set(values)].sort(comparator);
}

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isMilitaryRestricted(graduate, policy) {
  if (!graduate) return false;
  return graduate.category_code === policy.military_category_code
    || policy.military_restricted_objects.some(
      (row) => row.graduate_type === graduate.object_type
        && row.graduate_code === graduate.object_code,
    );
}

function isConsumable(mapping) {
  return !mapping.military_restriction
    && mapping.skills_behavior !== "仅目录查看"
    && mapping.skills_behavior !== "无";
}

function makeFindingCollector() {
  const findings = [];
  return {
    add({ severity, checkCode, category, entityType, entityKey, message, details }) {
      const finding = {
        severity,
        check_code: checkCode,
        category,
        entity_type: entityType,
        entity_key: String(entityKey),
        message,
      };
      if (details !== undefined) finding.details = details;
      findings.push(finding);
    },
    finish() {
      return findings
        .sort((left, right) =>
          (SEVERITY_RANK.get(left.severity) ?? 99) - (SEVERITY_RANK.get(right.severity) ?? 99)
          || compareText(left.check_code, right.check_code)
          || compareText(left.entity_type, right.entity_type)
          || compareText(left.entity_key, right.entity_key)
          || compareText(left.message, right.message)
        )
        .map((finding, index) => ({
          finding_id: `QA-${String(index + 1).padStart(4, "0")}`,
          ...finding,
        }));
    },
  };
}

function cloneCatalogRecords(records) {
  return records.map((record) => structuredClone(record));
}

function readReviewRows(input, primaryName, fallbackNames) {
  if (input[primaryName] !== undefined) return recordsOf(input[primaryName], primaryName);
  for (const name of fallbackNames) {
    if (input[name] !== undefined) return recordsOf(input[name], name);
  }
  fail(`${primaryName} 缺失`);
}

function buildUndergraduateIndex({ undergraduate, mappings, reviewByCode, graduateTypes, policy, qa }) {
  const mappingsByMajor = new Map(undergraduate.map((major) => [major.major_code, []]));
  for (const mapping of mappings) mappingsByMajor.get(mapping.undergraduate_code)?.push(mapping);

  return undergraduate.map((major) => {
    const review = reviewByCode.get(major.major_code);
    const rows = mappingsByMajor.get(major.major_code) ?? [];
    const directRows = rows.filter((row) => !row.military_restriction
      && (row.relation_level === policy.relation_levels[0]
        || row.relation_level === policy.relation_levels[1]));
    const directTypes = new Set(directRows.map((row) => row.graduate_type));
    const zeroMappingTypes = graduateTypes.filter((type) => !directTypes.has(type));
    const declaredZeroTypes = Array.isArray(review?.zero_mapping_types) ? review.zero_mapping_types : [];
    if (review && !sameStringSet(declaredZeroTypes, zeroMappingTypes)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "ZERO_MAPPING_CONFLICT",
        category: "零映射状态不一致",
        entityType: "undergraduate",
        entityKey: major.major_code,
        message: "本科复核台账的零映射类型与已接受关系不一致。",
        details: { declared: declaredZeroTypes, derived: zeroMappingTypes },
      });
    }

    if (review?.review_status === EXPERT_REVIEW) {
      qa.add({
        severity: REVIEW,
        checkCode: "EXPERT_REVIEW_REQUIRED",
        category: "建议专家复核",
        entityType: "undergraduate",
        entityKey: major.major_code,
        message: review.review_note,
      });
    }
    if (zeroMappingTypes.length === graduateTypes.length) {
      qa.add({
        severity: review?.review_status === EXPERT_REVIEW ? REVIEW : NOTICE,
        checkCode: "UNDERGRADUATE_ZERO_MAPPING",
        category: review?.review_status === CONFIRMED_ZERO ? "已确认无映射" : "本科零映射",
        entityType: "undergraduate",
        entityKey: major.major_code,
        message: review?.review_note ?? "未形成已接受的研究生目录对应关系。",
      });
    }

    const byLevel = (level) => rows.filter((row) => row.relation_level === level).map((row) => row.mapping_id);
    const academicType = graduateTypes[0];
    const professionalType = graduateTypes[1];
    return {
      undergraduate_code: major.major_code,
      undergraduate_name: major.major_name,
      category_code: major.category_code,
      category_name: major.category_name,
      class_code: major.class_code,
      class_name: major.class_name,
      review_status: review?.review_status ?? PENDING_REVIEW,
      review_note: review?.review_note ?? "",
      reviewed_at: review?.reviewed_at ?? null,
      mapping_count: rows.length,
      direct_mapping_count: directRows.length,
      mapping_ids: rows.map((row) => row.mapping_id),
      academic_mapping_ids: rows.filter((row) => row.graduate_type === academicType).map((row) => row.mapping_id),
      professional_mapping_ids: rows.filter((row) => row.graduate_type === professionalType).map((row) => row.mapping_id),
      primary_mapping_ids: rows.filter((row) => row.is_primary).map((row) => row.mapping_id),
      other_core_mapping_ids: byLevel(policy.relation_levels[1]),
      strong_mapping_ids: byLevel(policy.relation_levels[2]),
      extended_mapping_ids: byLevel(policy.relation_levels[3]),
      directory_reference_mapping_ids: byLevel(policy.relation_levels[4]),
      skills_behaviors: uniqueSorted(rows.map((row) => row.skills_behavior)),
      zero_mapping_types: zeroMappingTypes,
      zero_mapping_state: zeroMappingTypes.length === graduateTypes.length
        ? "无合适研究生直接对应"
        : zeroMappingTypes.length > 0 ? "部分类型无直接对应" : "两类均有直接对应",
      consumable_mapping_count: rows.filter(isConsumable).length,
      military_reference_count: rows.filter((row) => row.military_restriction).length,
    };
  });
}

function deriveGraduateState(graduate, mappings, policy) {
  if (isMilitaryRestricted(graduate, policy)) return "军事学限制，仅目录参考";
  if (mappings.length === 0) return "已确认无直接对应本科专业";
  if (mappings.some((row) => row.relation_level === policy.relation_levels[0]
      || row.relation_level === policy.relation_levels[1])) {
    return "有核心本科对应";
  }
  return "仅有强相关或延伸本科对应";
}

function buildGraduateIndex({ graduate, mappings, reviewByKey, policy, qa, overBroadThreshold }) {
  const mappingsByGraduate = new Map(
    graduate.map((record) => [graduateKey(record.object_type, record.object_code), []]),
  );
  for (const mapping of mappings) {
    mappingsByGraduate.get(graduateKey(mapping.graduate_type, mapping.graduate_code))?.push(mapping);
  }

  return graduate.map((record) => {
    const key = graduateKey(record.object_type, record.object_code);
    const rows = mappingsByGraduate.get(key) ?? [];
    const review = reviewByKey.get(key);
    const reverseState = deriveGraduateState(record, rows, policy);
    const expectedIds = rows.map((row) => row.mapping_id);
    const declaredIds = Array.isArray(review?.accepted_mapping_ids) ? review.accepted_mapping_ids : [];
    if (review && !sameStringSet(declaredIds, expectedIds)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "REVERSE_INDEX_CONFLICT",
        category: "双向复核不一致",
        entityType: "graduate",
        entityKey: key,
        message: "研究生反向复核台账与本科端已接受关系不一致。",
        details: { declared: declaredIds, derived: expectedIds },
      });
    }
    if (review && review.reverse_state !== reverseState) {
      qa.add({
        severity: BLOCKING,
        checkCode: "REVERSE_STATE_CONFLICT",
        category: "反向状态不一致",
        entityType: "graduate",
        entityKey: key,
        message: "研究生复核台账状态与已接受关系推导状态不一致。",
        details: { declared: review.reverse_state, derived: reverseState },
      });
    }
    if (!isMilitaryRestricted(record, policy) && rows.length > overBroadThreshold) {
      qa.add({
        severity: REVIEW,
        checkCode: "OVER_BROAD_GRADUATE_COVERAGE",
        category: "研究生覆盖范围过宽",
        entityType: "graduate",
        entityKey: key,
        message: `${record.object_name} 对应 ${rows.length} 个本科专业，建议抽查是否存在过宽规则。`,
        details: { mapping_count: rows.length, review_threshold: overBroadThreshold },
      });
    }
    if (!isMilitaryRestricted(record, policy) && rows.length === 0) {
      qa.add({
        severity: NOTICE,
        checkCode: "GRADUATE_ZERO_MAPPING",
        category: "研究生零映射",
        entityType: "graduate",
        entityKey: key,
        message: review?.review_note ?? "未形成已接受的本科专业对应关系。",
      });
    } else if (!isMilitaryRestricted(record, policy)
        && rows.length > 0
        && !rows.some((row) => row.relation_level === policy.relation_levels[0]
          || row.relation_level === policy.relation_levels[1])) {
      qa.add({
        severity: REVIEW,
        checkCode: "MISSING_CORE_MAPPING",
        category: "缺少核心映射",
        entityType: "graduate",
        entityKey: key,
        message: "该研究生对象仅有强相关或延伸关系，未形成核心本科对应。",
      });
    }

    return {
      graduate_type: record.object_type,
      graduate_code: record.object_code,
      graduate_name: record.object_name,
      category_code: record.category_code,
      category_name: record.category_name,
      reverse_state: reverseState,
      review_note: review?.review_note ?? "",
      reviewed_at: review?.reviewed_at ?? null,
      mapping_count: rows.length,
      mapping_ids: expectedIds,
      undergraduate_codes: uniqueSorted(rows.map((row) => row.undergraduate_code)),
      primary_mapping_ids: rows.filter((row) => row.is_primary).map((row) => row.mapping_id),
      core_mapping_ids: rows.filter((row) => row.relation_level === policy.relation_levels[0]
        || row.relation_level === policy.relation_levels[1]).map((row) => row.mapping_id),
      strong_mapping_ids: rows.filter((row) => row.relation_level === policy.relation_levels[2]).map((row) => row.mapping_id),
      extended_mapping_ids: rows.filter((row) => row.relation_level === policy.relation_levels[3]).map((row) => row.mapping_id),
      directory_reference_mapping_ids: rows.filter(
        (row) => row.relation_level === policy.relation_levels[4],
      ).map((row) => row.mapping_id),
      consumable_mapping_count: rows.filter(isConsumable).length,
      military_reference_count: rows.filter((row) => row.military_restriction).length,
    };
  });
}

function buildSummary({
  undergraduateIndex,
  graduateIndex,
  mappings,
  qaFindings,
  policy,
  graduateTypeCount,
  overBroadThreshold,
}) {
  return {
    undergraduate_count: undergraduateIndex.length,
    graduate_count: graduateIndex.length,
    mapping_count: mappings.length,
    undergraduate_index_count: undergraduateIndex.length,
    graduate_index_count: graduateIndex.length,
    undergraduate_zero_mapping_count: undergraduateIndex.filter(
      (row) => row.zero_mapping_types.length === graduateTypeCount,
    ).length,
    undergraduate_no_accepted_mapping_count: undergraduateIndex.filter((row) => row.mapping_count === 0).length,
    undergraduate_partial_zero_mapping_count: undergraduateIndex.filter(
      (row) => row.zero_mapping_types.length > 0
        && row.zero_mapping_types.length < graduateTypeCount,
    ).length,
    graduate_zero_mapping_count: graduateIndex.filter(
      (row) => row.reverse_state === "已确认无直接对应本科专业",
    ).length,
    graduate_no_accepted_mapping_count: graduateIndex.filter((row) => row.mapping_count === 0).length,
    military_mapping_count: mappings.filter((row) => row.military_restriction).length,
    consumable_mapping_count: mappings.filter(isConsumable).length,
    qa_finding_count: qaFindings.length,
    blocking_finding_count: qaFindings.filter((row) => row.severity === BLOCKING).length,
    review_finding_count: qaFindings.filter((row) => row.severity === REVIEW).length,
    notice_finding_count: qaFindings.filter((row) => row.severity === NOTICE).length,
    over_broad_review_threshold: overBroadThreshold,
    relation_level_counts: countBy(mappings, "relation_level", policy.relation_levels),
    skills_behavior_counts: countBy(mappings, "skills_behavior", policy.skills_behaviors),
    mapping_review_status_counts: countBy(mappings, "review_status", policy.review_statuses),
    undergraduate_review_status_counts: countBy(
      undergraduateIndex,
      "review_status",
      policy.review_statuses,
    ),
    graduate_reverse_state_counts: countBy(graduateIndex, "reverse_state"),
    qa_severity_counts: countBy(qaFindings, "severity", [BLOCKING, REVIEW, NOTICE]),
    qa_check_counts: countBy(qaFindings, "check_code"),
  };
}

/**
 * Reconciles the two reviewed ledgers into one deterministic, safety-gated bundle.
 * Only undergraduate-ledger accepted IDs can enter the formal mapping table.
 */
export function buildMappingBundle(input) {
  requireObject(input, "inputs");
  const policy = requireObject(input.policy, "policy");
  const graduateTypes = requireArray(policy.graduate_object_types, "policy.graduate_object_types");
  requireArray(policy.relation_levels, "policy.relation_levels");
  requireArray(policy.skills_behaviors, "policy.skills_behaviors");
  requireArray(policy.review_statuses, "policy.review_statuses");
  requireArray(policy.military_restricted_objects, "policy.military_restricted_objects");
  requireObject(policy.military_rule, "policy.military_rule");

  const undergraduateInput = recordsOf(input.undergraduate, "undergraduate");
  const graduateInput = recordsOf(input.graduate, "graduate");
  const candidateInput = recordsOf(input.candidates, "candidates");
  const undergraduateReviewRows = readReviewRows(
    input,
    "undergraduateReview",
    ["majorReview", "undergraduate_review", "major_review"],
  );
  const graduateReviewRows = readReviewRows(
    input,
    "graduateReview",
    ["graduate_review"],
  );
  const overrides = requireObject(input.overrides, "overrides");
  requireObject(overrides.major_overrides, "overrides.major_overrides");

  const undergraduate = cloneCatalogRecords(undergraduateInput)
    .sort((left, right) => compareText(left.major_code, right.major_code));
  const typeRank = new Map(graduateTypes.map((value, index) => [value, index]));
  const graduate = cloneCatalogRecords(graduateInput)
    .sort((left, right) =>
      (typeRank.get(left.object_type) ?? Number.MAX_SAFE_INTEGER)
      - (typeRank.get(right.object_type) ?? Number.MAX_SAFE_INTEGER)
      || compareText(left.object_code, right.object_code)
    );
  const qa = makeFindingCollector();

  const undergraduateByCode = new Map();
  for (const major of undergraduate) {
    if (!isNonEmptyString(major.major_code)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "INVALID_REFERENCE",
        category: "本科目录代码无效",
        entityType: "undergraduate",
        entityKey: major.major_code ?? "(missing)",
        message: "本科目录记录缺少有效专业代码。",
      });
      continue;
    }
    if (undergraduateByCode.has(major.major_code)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "DUPLICATE_RELATIONSHIP",
        category: "本科目录代码重复",
        entityType: "undergraduate",
        entityKey: major.major_code,
        message: "本科目录存在重复专业代码。",
      });
    } else undergraduateByCode.set(major.major_code, major);
  }

  const graduateByKey = new Map();
  for (const record of graduate) {
    const key = graduateKey(record.object_type, record.object_code);
    if (!graduateTypes.includes(record.object_type) || !isNonEmptyString(record.object_code)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "INVALID_REFERENCE",
        category: "研究生目录代码无效",
        entityType: "graduate",
        entityKey: key,
        message: "研究生目录记录缺少有效对象类型或代码。",
      });
      continue;
    }
    if (graduateByKey.has(key)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "DUPLICATE_RELATIONSHIP",
        category: "研究生目录对象重复",
        entityType: "graduate",
        entityKey: key,
        message: "研究生目录存在重复对象。",
      });
    } else graduateByKey.set(key, record);
  }

  for (const majorCode of Object.keys(overrides.major_overrides)) {
    if (!undergraduateByCode.has(majorCode)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "INVALID_REFERENCE",
        category: "专业例外引用无效",
        entityType: "override",
        entityKey: majorCode,
        message: "专业级例外引用了本科目录中不存在的代码。",
      });
    }
  }

  const candidatesById = new Map();
  const duplicateCandidateIds = new Set();
  for (const candidate of candidateInput) {
    if (!isNonEmptyString(candidate.mapping_id)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "INVALID_REFERENCE",
        category: "候选映射标识无效",
        entityType: "mapping",
        entityKey: candidate.mapping_id ?? "(missing)",
        message: "候选映射缺少有效 mapping_id。",
      });
      continue;
    }
    if (candidatesById.has(candidate.mapping_id)) duplicateCandidateIds.add(candidate.mapping_id);
    else candidatesById.set(candidate.mapping_id, candidate);
    if (!undergraduateByCode.has(candidate.undergraduate_code)
        || !graduateByKey.has(graduateKey(candidate.graduate_type, candidate.graduate_code))) {
      qa.add({
        severity: BLOCKING,
        checkCode: "INVALID_REFERENCE",
        category: "候选目录引用无效",
        entityType: "mapping",
        entityKey: candidate.mapping_id,
        message: "候选映射引用了不存在的本科或研究生目录对象。",
      });
    }
  }
  for (const mappingId of duplicateCandidateIds) {
    qa.add({
      severity: BLOCKING,
      checkCode: "DUPLICATE_RELATIONSHIP",
      category: "候选映射标识重复",
      entityType: "mapping",
      entityKey: mappingId,
      message: "候选映射中存在重复 mapping_id。",
    });
  }

  const reviewByCode = new Map();
  for (const review of undergraduateReviewRows) {
    const code = review.undergraduate_code;
    if (!undergraduateByCode.has(code)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "INVALID_REFERENCE",
        category: "本科复核引用无效",
        entityType: "undergraduate_review",
        entityKey: code ?? "(missing)",
        message: "本科复核台账引用了目录中不存在的专业。",
      });
      continue;
    }
    if (reviewByCode.has(code)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "DUPLICATE_RELATIONSHIP",
        category: "本科复核记录重复",
        entityType: "undergraduate_review",
        entityKey: code,
        message: "同一本科专业存在重复复核记录。",
      });
      continue;
    }
    reviewByCode.set(code, review);
  }

  for (const major of undergraduate) {
    const review = reviewByCode.get(major.major_code);
    if (!review || review.review_status === PENDING_REVIEW || !isNonEmptyString(review.reviewed_at)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "UNREVIEWED_RECORD",
        category: "本科记录尚未复核",
        entityType: "undergraduate",
        entityKey: major.major_code,
        message: review ? "本科复核状态尚未完成。" : "本科专业缺少逐项复核记录。",
      });
    }
    if (review && !policy.review_statuses.includes(review.review_status)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "UNREVIEWED_RECORD",
        category: "本科复核状态无效",
        entityType: "undergraduate",
        entityKey: major.major_code,
        message: `本科复核状态不在政策枚举中：${String(review.review_status)}`,
      });
    }
    if (review?.review_status === CATALOG_CONFLICT) {
      qa.add({
        severity: BLOCKING,
        checkCode: "CATALOG_VERSION_CONFLICT",
        category: "目录版本冲突",
        entityType: "undergraduate",
        entityKey: major.major_code,
        message: review.review_note ?? "本科复核记录存在待处理目录版本差异。",
      });
    }
  }

  const acceptedMembership = new Map();
  const rejectedMembership = new Map();
  const acceptedMappings = [];
  for (const [code, review] of reviewByCode) {
    const acceptedIds = Array.isArray(review.accepted_mapping_ids) ? review.accepted_mapping_ids : [];
    const rejectedIds = Array.isArray(review.rejected_mapping_ids) ? review.rejected_mapping_ids : [];
    if (!Array.isArray(review.accepted_mapping_ids) || !Array.isArray(review.rejected_mapping_ids)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "UNREVIEWED_RECORD",
        category: "本科复核决定不完整",
        entityType: "undergraduate",
        entityKey: code,
        message: "accepted_mapping_ids 与 rejected_mapping_ids 必须显式记录。",
      });
    }
    for (const mappingId of acceptedIds) {
      if (acceptedMembership.has(mappingId) || acceptedIds.indexOf(mappingId) !== acceptedIds.lastIndexOf(mappingId)) {
        qa.add({
          severity: BLOCKING,
          checkCode: "DUPLICATE_RELATIONSHIP",
          category: "接受决定重复",
          entityType: "mapping",
          entityKey: mappingId,
          message: "同一映射被重复接受或被多个本科复核记录接受。",
        });
      }
      acceptedMembership.set(mappingId, code);
      const candidate = candidatesById.get(mappingId);
      if (!candidate || candidate.undergraduate_code !== code) {
        qa.add({
          severity: BLOCKING,
          checkCode: "INVALID_REFERENCE",
          category: "接受映射引用无效",
          entityType: "mapping",
          entityKey: mappingId,
          message: candidate
            ? "接受映射不属于当前本科专业。"
            : "接受映射未出现在候选清单中。",
        });
        continue;
      }
      const mapping = structuredClone(candidate);
      const graduateRecord = graduateByKey.get(graduateKey(mapping.graduate_type, mapping.graduate_code));
      const restricted = isMilitaryRestricted(graduateRecord, policy);
      if (!restricted) mapping.review_status = review.review_status;

      if (!isNonEmptyString(mapping.rationale)) {
        qa.add({
          severity: BLOCKING,
          checkCode: "MISSING_RATIONALE",
          category: "映射理由缺失",
          entityType: "mapping",
          entityKey: mapping.mapping_id,
          message: "正式映射必须保留非空映射理由。",
        });
      }
      if (mapping.review_status === PENDING_REVIEW) {
        qa.add({
          severity: BLOCKING,
          checkCode: "UNREVIEWED_RECORD",
          category: "映射尚未复核",
          entityType: "mapping",
          entityKey: mapping.mapping_id,
          message: "尚未完成复核的关系不得进入正式映射。",
        });
      }
      if (mapping.review_status === CATALOG_CONFLICT) {
        qa.add({
          severity: BLOCKING,
          checkCode: "CATALOG_VERSION_CONFLICT",
          category: "目录版本冲突",
          entityType: "mapping",
          entityKey: mapping.mapping_id,
          message: "存在待处理目录版本差异的关系不得进入正式映射。",
        });
      }
      const militaryTupleValid = mapping.relation_level === policy.military_rule.relation_level
        && mapping.is_primary === policy.military_rule.is_primary
        && mapping.skills_behavior === policy.military_rule.skills_behavior
        && mapping.military_restriction === policy.military_rule.military_restriction
        && mapping.review_status === policy.military_rule.review_status;
      if ((restricted && !militaryTupleValid) || (!restricted && mapping.military_restriction)) {
        qa.add({
          severity: BLOCKING,
          checkCode: "MILITARY_LEAKAGE",
          category: "军事学 Skills 行为泄漏",
          entityType: "mapping",
          entityKey: mapping.mapping_id,
          message: restricted
            ? "受限目录关系必须保持目录参考、非主映射且不可消费。"
            : "非受限目录关系不得伪标为军事学限制。",
        });
      }
      acceptedMappings.push(mapping);
    }
    for (const mappingId of rejectedIds) {
      if (rejectedMembership.has(mappingId) || rejectedIds.indexOf(mappingId) !== rejectedIds.lastIndexOf(mappingId)) {
        qa.add({
          severity: BLOCKING,
          checkCode: "DUPLICATE_RELATIONSHIP",
          category: "拒绝决定重复",
          entityType: "mapping",
          entityKey: mappingId,
          message: "同一映射被重复拒绝或被多个本科复核记录拒绝。",
        });
      }
      rejectedMembership.set(mappingId, code);
      const candidate = candidatesById.get(mappingId);
      if (!candidate || candidate.undergraduate_code !== code) {
        qa.add({
          severity: BLOCKING,
          checkCode: "INVALID_REFERENCE",
          category: "拒绝映射引用无效",
          entityType: "mapping",
          entityKey: mappingId,
          message: candidate
            ? "拒绝映射不属于当前本科专业。"
            : "拒绝映射未出现在候选清单中。",
        });
      }
    }
  }

  for (const candidate of candidateInput) {
    const acceptedBy = acceptedMembership.get(candidate.mapping_id);
    const rejectedBy = rejectedMembership.get(candidate.mapping_id);
    if (acceptedBy && rejectedBy) {
      qa.add({
        severity: BLOCKING,
        checkCode: "UNREVIEWED_RECORD",
        category: "复核决定冲突",
        entityType: "mapping",
        entityKey: candidate.mapping_id,
        message: "候选映射同时被接受和拒绝。",
      });
    } else if (!acceptedBy && !rejectedBy) {
      qa.add({
        severity: BLOCKING,
        checkCode: "UNREVIEWED_RECORD",
        category: "候选映射尚未决定",
        entityType: "mapping",
        entityKey: candidate.mapping_id,
        message: "候选映射未在本科复核台账中明确接受或拒绝。",
      });
    }
  }

  const relationRank = new Map(policy.relation_levels.map((value, index) => [value, index]));
  acceptedMappings.sort((left, right) =>
    compareText(left.undergraduate_code, right.undergraduate_code)
    || (typeRank.get(left.graduate_type) ?? Number.MAX_SAFE_INTEGER)
      - (typeRank.get(right.graduate_type) ?? Number.MAX_SAFE_INTEGER)
    || (relationRank.get(left.relation_level) ?? Number.MAX_SAFE_INTEGER)
      - (relationRank.get(right.relation_level) ?? Number.MAX_SAFE_INTEGER)
    || compareText(left.graduate_code, right.graduate_code)
    || compareText(left.mapping_id, right.mapping_id)
  );

  const mappingIds = new Set();
  const relationshipKeys = new Set();
  const primaryKeys = new Set();
  for (const mapping of acceptedMappings) {
    if (mappingIds.has(mapping.mapping_id)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "DUPLICATE_RELATIONSHIP",
        category: "正式映射标识重复",
        entityType: "mapping",
        entityKey: mapping.mapping_id,
        message: "正式映射中存在重复 mapping_id。",
      });
    }
    mappingIds.add(mapping.mapping_id);
    const relationKey = relationshipKey(mapping);
    if (relationshipKeys.has(relationKey)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "DUPLICATE_RELATIONSHIP",
        category: "正式关系重复",
        entityType: "relationship",
        entityKey: relationKey,
        message: "同一本科专业与研究生对象之间存在重复关系。",
      });
    }
    relationshipKeys.add(relationKey);
    if (mapping.is_primary) {
      const primaryKey = `${mapping.undergraduate_code}|${mapping.graduate_type}`;
      if (primaryKeys.has(primaryKey)) {
        qa.add({
          severity: BLOCKING,
          checkCode: "PRIMARY_OVERFLOW",
          category: "主映射超限",
          entityType: "undergraduate",
          entityKey: primaryKey,
          message: "同一本科专业在同一研究生对象类型下存在多个主映射。",
        });
      }
      primaryKeys.add(primaryKey);
    }
  }

  const graduateReviewByKey = new Map();
  for (const review of graduateReviewRows) {
    const key = graduateKey(review.graduate_type, review.graduate_code);
    if (!graduateByKey.has(key)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "INVALID_REFERENCE",
        category: "研究生复核引用无效",
        entityType: "graduate_review",
        entityKey: key,
        message: "研究生复核台账引用了目录中不存在的对象。",
      });
      continue;
    }
    if (graduateReviewByKey.has(key)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "DUPLICATE_RELATIONSHIP",
        category: "研究生复核记录重复",
        entityType: "graduate_review",
        entityKey: key,
        message: "同一研究生目录对象存在重复复核记录。",
      });
      continue;
    }
    graduateReviewByKey.set(key, review);
    if (!Array.isArray(review.accepted_mapping_ids)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "UNREVIEWED_RECORD",
        category: "研究生复核决定不完整",
        entityType: "graduate",
        entityKey: key,
        message: "accepted_mapping_ids 必须显式记录。",
      });
    } else {
      for (const mappingId of review.accepted_mapping_ids) {
        const candidate = candidatesById.get(mappingId);
        if (!candidate
            || graduateKey(candidate.graduate_type, candidate.graduate_code) !== key) {
          qa.add({
            severity: BLOCKING,
            checkCode: "INVALID_REFERENCE",
            category: "研究生反向映射引用无效",
            entityType: "mapping",
            entityKey: mappingId,
            message: candidate
              ? "研究生反向复核映射不属于当前目录对象。"
              : "研究生反向复核映射未出现在候选清单中。",
          });
        }
      }
    }
    if (!isNonEmptyString(review.reviewed_at) || review.reverse_state === PENDING_REVIEW) {
      qa.add({
        severity: BLOCKING,
        checkCode: "UNREVIEWED_RECORD",
        category: "研究生记录尚未复核",
        entityType: "graduate",
        entityKey: key,
        message: "研究生反向覆盖记录尚未完成复核。",
      });
    }
    if (review.reverse_state === CATALOG_CONFLICT) {
      qa.add({
        severity: BLOCKING,
        checkCode: "CATALOG_VERSION_CONFLICT",
        category: "目录版本冲突",
        entityType: "graduate",
        entityKey: key,
        message: review.review_note ?? "研究生反向复核记录存在待处理目录版本差异。",
      });
    }
  }
  for (const record of graduate) {
    const key = graduateKey(record.object_type, record.object_code);
    if (!graduateReviewByKey.has(key)) {
      qa.add({
        severity: BLOCKING,
        checkCode: "UNREVIEWED_RECORD",
        category: "研究生记录尚未复核",
        entityType: "graduate",
        entityKey: key,
        message: "研究生目录对象缺少逐项反向复核记录。",
      });
    }
  }

  const overBroadThreshold = Number.isInteger(policy.over_broad_graduate_coverage_threshold)
    && policy.over_broad_graduate_coverage_threshold > 0
    ? policy.over_broad_graduate_coverage_threshold
    : Math.max(50, Math.ceil(undergraduate.length * 0.05));
  const undergraduateIndex = buildUndergraduateIndex({
    undergraduate,
    mappings: acceptedMappings,
    reviewByCode,
    graduateTypes,
    policy,
    qa,
  });
  const graduateIndex = buildGraduateIndex({
    graduate,
    mappings: acceptedMappings,
    reviewByKey: graduateReviewByKey,
    policy,
    qa,
    overBroadThreshold,
  });

  let validationError;
  try {
    validateBundle({ undergraduate, graduate, mappings: acceptedMappings });
  } catch (error) {
    validationError = error;
    qa.add({
      severity: BLOCKING,
      checkCode: "SCHEMA_VALIDATION_FAILURE",
      category: "映射安全校验失败",
      entityType: "bundle",
      entityKey: "mapping_bundle",
      message: error instanceof Error ? error.message : String(error),
    });
  }

  const qaFindings = qa.finish();
  const summary = buildSummary({
    undergraduateIndex,
    graduateIndex,
    mappings: acceptedMappings,
    qaFindings,
    policy,
    graduateTypeCount: graduateTypes.length,
    overBroadThreshold,
  });
  const reviewedAtValues = [
    ...undergraduateReviewRows.map((row) => row.reviewed_at),
    ...graduateReviewRows.map((row) => row.reviewed_at),
  ].filter(isNonEmptyString).sort(compareText);
  const metadata = {
    schema_version: "1.0.0",
    generated_at: reviewedAtValues.at(-1) ?? null,
    undergraduate_catalog_count: undergraduate.length,
    graduate_catalog_count: graduate.length,
    candidate_mapping_count: candidateInput.length,
    accepted_mapping_count: acceptedMappings.length,
    rejected_mapping_count: rejectedMembership.size,
    undergraduate_review_count: undergraduateReviewRows.length,
    graduate_review_count: graduateReviewRows.length,
    override_major_count: Object.keys(overrides.major_overrides).length,
    sort_order: ["undergraduate_code", "graduate_type", "relation_rank", "graduate_code"],
  };
  const bundle = {
    metadata,
    undergraduate,
    graduate,
    mappings: acceptedMappings,
    undergraduate_index: undergraduateIndex,
    graduate_index: graduateIndex,
    qa_findings: qaFindings,
    summary,
  };

  if (summary.blocking_finding_count > 0) {
    throw new MappingBundleBuildError(
      `映射聚合被 ${summary.blocking_finding_count} 条阻断质量发现拒绝。`,
      qaFindings,
      validationError,
    );
  }
  return bundle;
}

export async function writeMappingArtifacts(bundle, rootUrl = new URL("./", import.meta.url)) {
  validateBundle(bundle);
  if (bundle.qa_findings.some((row) => row.severity === BLOCKING)) {
    throw new MappingBundleBuildError("包含阻断质量发现的映射包不得写入正式产物。", bundle.qa_findings);
  }
  const artifactsUrl = new URL("artifacts/", rootUrl);
  await fs.mkdir(artifactsUrl, { recursive: true });
  await Promise.all([
    fs.writeFile(new URL("mapping_bundle.json", artifactsUrl), `${JSON.stringify(bundle, null, 2)}\n`, "utf8"),
    fs.writeFile(new URL("qa_findings.json", artifactsUrl), `${JSON.stringify(bundle.qa_findings, null, 2)}\n`, "utf8"),
    fs.writeFile(new URL("summary.json", artifactsUrl), `${JSON.stringify(bundle.summary, null, 2)}\n`, "utf8"),
  ]);
}

async function buildArtifacts() {
  const root = new URL("./", import.meta.url);
  const readJson = async (relativePath) => JSON.parse(
    await fs.readFile(new URL(relativePath, root), "utf8"),
  );
  const bundle = buildMappingBundle({
    undergraduate: await readJson("catalogs/undergraduate_2026.json"),
    graduate: await readJson("catalogs/graduate_effective.json"),
    candidates: await readJson("artifacts/mapping_candidates.json"),
    overrides: await readJson("rules/major_overrides.json"),
    policy: await readJson("rules/mapping_policy.json"),
    undergraduateReview: await readJson("review/major_review_ledger.json"),
    graduateReview: await readJson("review/graduate_review_ledger.json"),
  });
  await writeMappingArtifacts(bundle, root);
  console.log(
    `generated mapping bundle: ${bundle.undergraduate_index.length} undergraduate index rows, `
    + `${bundle.graduate_index.length} graduate index rows, ${bundle.mappings.length} accepted mappings, `
    + `${bundle.summary.blocking_finding_count} blocking findings`,
  );
}

const invokedPath = process.argv[1] ? path.resolve(process.argv[1]) : null;
if (invokedPath === fileURLToPath(import.meta.url)) await buildArtifacts();
