import policy from "./rules/mapping_policy.json" with { type: "json" };

export const RELATION_LEVELS = Object.freeze([...policy.relation_levels]);
export const SKILLS_BEHAVIORS = Object.freeze([...policy.skills_behaviors]);
export const REVIEW_STATUSES = Object.freeze([...policy.review_statuses]);
export const CONFIDENCE_LEVELS = Object.freeze([...policy.confidence_levels]);
export const RELATION_BASES = Object.freeze([...policy.relation_bases]);
export const GRADUATE_OBJECT_TYPES = Object.freeze([...policy.graduate_object_types]);
export const MILITARY_RULE = Object.freeze({ ...policy.military_rule });

const relationLevels = new Set(RELATION_LEVELS);
const skillsBehaviors = new Set(SKILLS_BEHAVIORS);
const reviewStatuses = new Set(REVIEW_STATUSES);
const confidenceLevels = new Set(CONFIDENCE_LEVELS);
const relationBases = new Set(RELATION_BASES);
const graduateObjectTypes = new Set(GRADUATE_OBJECT_TYPES);

function fail(message) {
  throw new Error(`映射记录无效：${message}`);
}

function requireNonEmptyString(value, field) {
  if (typeof value !== "string" || value.trim() === "") fail(`${field} 必须为非空文本`);
}

function requireEnum(value, values, field) {
  if (!values.has(value)) fail(`${field} 不是允许的枚举值：${String(value)}`);
}

function requireMap(value, field) {
  if (!(value instanceof Map)) fail(`${field} 必须是 Map`);
}

function sameMilitaryTuple(record) {
  return Object.entries(MILITARY_RULE).every(([field, expected]) => record[field] === expected);
}

/** Returns a stable catalog key without changing the supplied code string. */
export function graduateKey(type, code) {
  return `${type}|${code}`;
}

/**
 * Validates one relationship against the normalized undergraduate and graduate catalogs.
 * Returns the original record so callers may validate inline without copying code fields.
 */
export function validateMappingRecord(record, ugByCode, gradByKey) {
  if (!record || typeof record !== "object" || Array.isArray(record)) fail("record 必须是对象");
  requireMap(ugByCode, "ugByCode");
  requireMap(gradByKey, "gradByKey");

  for (const field of ["mapping_id", "undergraduate_code", "graduate_type", "graduate_code", "rationale"]) {
    requireNonEmptyString(record[field], field);
  }
  if (typeof record.is_primary !== "boolean") fail("is_primary 必须为布尔值");
  if (typeof record.military_restriction !== "boolean") fail("military_restriction 必须为布尔值");

  requireEnum(record.graduate_type, graduateObjectTypes, "graduate_type");
  requireEnum(record.relation_level, relationLevels, "relation_level");
  requireEnum(record.skills_behavior, skillsBehaviors, "skills_behavior");
  requireEnum(record.review_status, reviewStatuses, "review_status");
  requireEnum(record.confidence, confidenceLevels, "confidence");

  if (!ugByCode.has(record.undergraduate_code)) fail(`本科目录中不存在代码 ${record.undergraduate_code}`);
  const graduateCatalogKey = graduateKey(record.graduate_type, record.graduate_code);
  const graduate = gradByKey.get(graduateCatalogKey);
  if (!graduate) fail(`研究生目录中不存在对象 ${graduateCatalogKey}`);
  if (graduate.object_type !== record.graduate_type || graduate.object_code !== record.graduate_code) {
    fail(`研究生目录对象与映射键不一致：${graduateCatalogKey}`);
  }

  if (!Array.isArray(record.relation_basis) || record.relation_basis.length === 0) {
    fail("relation_basis 至少需要一项关系依据");
  }
  const uniqueBases = new Set(record.relation_basis);
  if (uniqueBases.size !== record.relation_basis.length) fail("relation_basis 不能包含重复关系依据");
  for (const basis of record.relation_basis) requireEnum(basis, relationBases, "relation_basis");

  if (record.is_primary && record.relation_level !== "主映射/核心对应") {
    fail("只有主映射/核心对应可以标记 is_primary=true");
  }

  const militaryRelation = graduate.category_code === policy.military_category_code || record.military_restriction;
  if (militaryRelation && !sameMilitaryTuple(record)) {
    fail("军事学关系只能保留为目录参考，且不得产生 Skills 标签或检索行为");
  }
  if (!militaryRelation && record.skills_behavior !== policy.relation_behavior_rules[record.relation_level]) {
    fail(`${record.relation_level} 必须使用 Skills 行为 ${policy.relation_behavior_rules[record.relation_level]}`);
  }

  return record;
}

/**
 * Validates bundle-level uniqueness. Relationship identity is the pair of catalog
 * endpoints; relation level is an attribute of that relationship, not an extra key.
 */
export function validateBundle(bundle) {
  if (!bundle || typeof bundle !== "object" || Array.isArray(bundle)) fail("bundle 必须是对象");
  if (!Array.isArray(bundle.undergraduate)) fail("bundle.undergraduate 必须是数组");
  if (!Array.isArray(bundle.graduate)) fail("bundle.graduate 必须是数组");
  if (!Array.isArray(bundle.mappings)) fail("bundle.mappings 必须是数组");
  const ugByCode = new Map(bundle.undergraduate.map((record) => [record.major_code, record]));
  const gradByKey = new Map(bundle.graduate.map((record) => [graduateKey(record.object_type, record.object_code), record]));

  const mappingIds = new Set();
  const relationshipKeys = new Set();
  const primaryKeys = new Set();
  for (const record of bundle.mappings) {
    validateMappingRecord(record, ugByCode, gradByKey);

    if (mappingIds.has(record.mapping_id)) fail(`mapping_id 重复：${record.mapping_id}`);
    mappingIds.add(record.mapping_id);

    const relationshipKey = `${record.undergraduate_code}|${record.graduate_type}|${record.graduate_code}`;
    if (relationshipKeys.has(relationshipKey)) fail(`关系重复：${relationshipKey}`);
    relationshipKeys.add(relationshipKey);

    if (record.is_primary) {
      const primaryKey = `${record.undergraduate_code}|${record.graduate_type}`;
      if (primaryKeys.has(primaryKey)) fail(`同一本科专业和研究生对象类型只能有一个主映射：${primaryKey}`);
      primaryKeys.add(primaryKey);
    }
  }
  return bundle;
}
