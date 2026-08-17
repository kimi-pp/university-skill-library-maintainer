import policy from "./rules/mapping_policy.json" with { type: "json" };

export const RELATION_LEVELS = Object.freeze([...policy.relation_levels]);
export const SKILLS_BEHAVIORS = Object.freeze([...policy.skills_behaviors]);
export const REVIEW_STATUSES = Object.freeze([...policy.review_statuses]);
export const CONFIDENCE_LEVELS = Object.freeze([...policy.confidence_levels]);
export const RELATION_BASES = Object.freeze([...policy.relation_bases]);
export const SENSITIVE_RULE = Object.freeze({ ...policy.sensitive_rule });

const relationLevels = new Set(RELATION_LEVELS);
const skillsBehaviors = new Set(SKILLS_BEHAVIORS);
const reviewStatuses = new Set(REVIEW_STATUSES);
const confidenceLevels = new Set(CONFIDENCE_LEVELS);
const relationBases = new Set(RELATION_BASES);
const restrictedUndergraduateClasses = new Set(
  policy.restricted_undergraduate_class_codes,
);
const restrictedPattern = new RegExp(
  policy.restricted_object_keywords.map(escapeRegExp).join("|"),
);

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function fail(message) {
  throw new Error(`高职本科映射记录无效：${message}`);
}

function requireMap(value, field) {
  if (!(value instanceof Map)) fail(`${field} 必须是 Map`);
}

function requireNonEmptyString(value, field) {
  if (typeof value !== "string" || value.trim() === "") {
    fail(`${field} 必须为非空文本`);
  }
}

function requireEnum(value, allowed, field) {
  if (!allowed.has(value)) fail(`${field} 不是允许的枚举值：${String(value)}`);
}

function sameSensitiveTuple(record) {
  return Object.entries(SENSITIVE_RULE).every(
    ([field, expected]) => record[field] === expected,
  );
}

export function isRestrictedObject(vocational, undergraduate) {
  if (!vocational || !undergraduate) return false;
  if (restrictedUndergraduateClasses.has(undergraduate.class_code)) return true;
  return restrictedPattern.test(
    `${vocational.major_name ?? ""}|${undergraduate.major_name ?? ""}`,
  );
}

export function validateMappingRecord(
  record,
  vocationalByCode,
  undergraduateByCode,
) {
  if (!record || typeof record !== "object" || Array.isArray(record)) {
    fail("record 必须是对象");
  }
  requireMap(vocationalByCode, "vocationalByCode");
  requireMap(undergraduateByCode, "undergraduateByCode");
  for (const field of [
    "mapping_id",
    "vocational_code",
    "undergraduate_code",
    "rationale",
    "generation_method",
  ]) {
    requireNonEmptyString(record[field], field);
  }
  for (const field of ["is_primary", "sensitive_restriction", "consumable"]) {
    if (typeof record[field] !== "boolean") fail(`${field} 必须为布尔值`);
  }

  requireEnum(record.relation_level, relationLevels, "relation_level");
  requireEnum(record.skills_behavior, skillsBehaviors, "skills_behavior");
  requireEnum(record.review_status, reviewStatuses, "review_status");
  requireEnum(record.confidence, confidenceLevels, "confidence");

  const vocational = vocationalByCode.get(record.vocational_code);
  const undergraduate = undergraduateByCode.get(record.undergraduate_code);
  if (!vocational) fail(`高职专科目录中不存在代码 ${record.vocational_code}`);
  if (!undergraduate) fail(`本科目录中不存在代码 ${record.undergraduate_code}`);
  const expectedId = `VUG-${record.vocational_code}-${record.undergraduate_code}`;
  if (record.mapping_id !== expectedId) fail(`mapping_id 必须为 ${expectedId}`);

  if (!Array.isArray(record.relation_basis) || record.relation_basis.length === 0) {
    fail("relation_basis 至少需要一项关系依据");
  }
  const bases = new Set(record.relation_basis);
  if (bases.size !== record.relation_basis.length) fail("relation_basis 不能包含重复关系依据");
  for (const basis of record.relation_basis) {
    requireEnum(basis, relationBases, "relation_basis");
  }

  if (record.is_primary && record.relation_level !== "主映射/核心对应") {
    fail("只有主映射/核心对应可以标记 is_primary=true");
  }

  const restricted =
    isRestrictedObject(vocational, undergraduate) || record.sensitive_restriction;
  if (restricted && !sameSensitiveTuple(record)) {
    fail("敏感对象只能保留为目录参考，且必须非主映射、不可消费");
  }
  if (!restricted) {
    const expectedBehavior = policy.relation_behavior_rules[record.relation_level];
    if (record.skills_behavior !== expectedBehavior) {
      fail(`${record.relation_level} 必须使用 Skills 行为 ${expectedBehavior}`);
    }
    const expectedConsumable = record.relation_level !== "目录参考";
    if (record.consumable !== expectedConsumable) {
      fail(
        record.relation_level === "目录参考"
          ? "目录参考关系不得被 Skills 消费"
          : "非敏感正式映射必须可被 Skills 消费",
      );
    }
  }
  return record;
}

export function validateReviewRow(row, candidateIds) {
  if (!row || typeof row !== "object" || Array.isArray(row)) fail("复核记录必须是对象");
  requireNonEmptyString(row.vocational_code, "vocational_code");
  requireNonEmptyString(row.review_note, "review_note");
  requireEnum(row.review_status, reviewStatuses, "review_status");
  if (!/^\d{4}-\d{2}-\d{2}$/.test(row.reviewed_at)) {
    fail("reviewed_at 必须为 YYYY-MM-DD");
  }
  if (typeof row.zero_direct !== "boolean" || typeof row.zero_all !== "boolean") {
    fail("zero_direct 和 zero_all 必须为布尔值");
  }
  if (!Array.isArray(row.accepted_mapping_ids) || !Array.isArray(row.rejected_mapping_ids)) {
    fail("接受和拒绝候选必须为数组");
  }
  const accepted = new Set(row.accepted_mapping_ids);
  const rejected = new Set(row.rejected_mapping_ids);
  if (accepted.size !== row.accepted_mapping_ids.length) fail("接受候选不能重复");
  if (rejected.size !== row.rejected_mapping_ids.length) fail("拒绝候选不能重复");
  for (const mappingId of accepted) {
    if (rejected.has(mappingId)) fail(`候选不能同时接受和拒绝：${mappingId}`);
  }
  const expected = new Set(candidateIds);
  const actual = new Set([...accepted, ...rejected]);
  if (
    expected.size !== actual.size ||
    [...expected].some((mappingId) => !actual.has(mappingId))
  ) {
    fail("接受和拒绝集合必须穷尽全部候选");
  }
  return row;
}

export function validateBundle(bundle) {
  if (!bundle || typeof bundle !== "object" || Array.isArray(bundle)) {
    fail("bundle 必须是对象");
  }
  if (!Array.isArray(bundle.vocational_catalog)) fail("vocational_catalog 必须是数组");
  if (!Array.isArray(bundle.undergraduate_catalog)) fail("undergraduate_catalog 必须是数组");
  if (!Array.isArray(bundle.mappings)) fail("mappings 必须是数组");

  const vocationalByCode = new Map(
    bundle.vocational_catalog.map((row) => [row.major_code, row]),
  );
  const undergraduateByCode = new Map(
    bundle.undergraduate_catalog.map((row) => [row.major_code, row]),
  );
  const mappingIds = new Set();
  const endpointPairs = new Set();
  const primaryVocationalCodes = new Set();

  for (const record of bundle.mappings) {
    validateMappingRecord(record, vocationalByCode, undergraduateByCode);
    if (mappingIds.has(record.mapping_id)) fail(`mapping_id 重复：${record.mapping_id}`);
    mappingIds.add(record.mapping_id);
    const pair = `${record.vocational_code}|${record.undergraduate_code}`;
    if (endpointPairs.has(pair)) fail(`关系重复：${pair}`);
    endpointPairs.add(pair);
    if (record.is_primary) {
      if (primaryVocationalCodes.has(record.vocational_code)) {
        fail(`每个高职专科专业最多一个主映射：${record.vocational_code}`);
      }
      primaryVocationalCodes.add(record.vocational_code);
    }
  }
  return bundle;
}
