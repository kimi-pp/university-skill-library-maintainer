import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import policy from "./rules/mapping_policy.json" with { type: "json" };
import { graduateKey, isMilitaryRestrictedObject, validateBundle } from "./mapping_schema.mjs";

const ACADEMIC_TYPE = "学术学位一级学科";
const PROFESSIONAL_TYPE = "专业学位类别";
const MAIN_RELATION = "主映射/核心对应";
const OTHER_CORE_RELATION = "其他核心对应";
const AMBIGUOUS_REVIEW = "存在歧义，建议学科专家复核";
const HIGH_CONFIDENCE_REVIEW = "高置信度候选";
const CLASS_METHOD = "专业类规则继承";
const OVERRIDE_METHOD = "专业级例外";
const MILITARY_METHOD = "军事学目录参考";
const SUPPORTED_ACTIONS = new Set(["add", "remove", "replace_primary", "downgrade", "confirmed_zero"]);
const relationLevels = new Set(policy.relation_levels);
const relationBases = new Set(policy.relation_bases);
const graduateTypes = new Set(policy.graduate_object_types);

function fail(message) {
  throw new Error(`候选映射生成失败：${message}`);
}

function requireObject(value, field) {
  if (!value || typeof value !== "object" || Array.isArray(value)) fail(`${field} 必须是对象`);
}

function requireNonEmptyString(value, field) {
  if (typeof value !== "string" || value.trim() === "") fail(`${field} 必须是非空字符串`);
}

function requireArray(value, field) {
  if (!Array.isArray(value)) fail(`${field} 必须是数组`);
}

function endpoint(type, code) {
  return graduateKey(type, code);
}

function typeLetter(type) {
  if (type === ACADEMIC_TYPE) return "A";
  if (type === PROFESSIONAL_TYPE) return "P";
  fail(`未知研究生对象类型 ${String(type)}`);
}

function confidenceFor(relationLevel) {
  if (relationLevel === MAIN_RELATION) return "高";
  if (relationLevel === OTHER_CORE_RELATION || relationLevel === "强相关") return "中";
  return "低";
}

function reviewStatusFor(relationLevel) {
  return relationLevel === MAIN_RELATION || relationLevel === OTHER_CORE_RELATION
    ? HIGH_CONFIDENCE_REVIEW
    : AMBIGUOUS_REVIEW;
}

function validateBasis(basis, field) {
  requireArray(basis, field);
  if (basis.length === 0) fail(`${field} 至少需要一项关系依据`);
  if (new Set(basis).size !== basis.length) fail(`${field} 不能重复`);
  for (const value of basis) {
    if (!relationBases.has(value)) fail(`${field} 包含不允许的关系依据 ${String(value)}`);
  }
}

function validateTarget(target, field, graduateType, graduateByKey) {
  requireObject(target, field);
  requireNonEmptyString(graduateType, `${field}.graduate_type`);
  if (!graduateTypes.has(graduateType)) fail(`${field}.graduate_type 不在允许目录类型中`);
  requireNonEmptyString(target.code, `${field}.code`);
  requireNonEmptyString(target.level, `${field}.level`);
  if (!relationLevels.has(target.level)) fail(`${field}.level 不是允许的关系层级`);
  validateBasis(target.basis, `${field}.basis`);
  const key = endpoint(graduateType, target.code);
  if (!graduateByKey.has(key)) fail(`${field} 引用的研究生目录对象不存在：${key}`);
}

function makeWorkingCandidate({ undergraduateCode, graduateType, target, isPrimary, rationale, generationMethod }) {
  return {
    undergraduate_code: undergraduateCode,
    graduate_type: graduateType,
    graduate_code: target.code,
    relation_level: target.level,
    is_primary: isPrimary,
    relation_basis: [...target.basis],
    rationale,
    generation_method: generationMethod,
  };
}

function insertSeed(targets, candidate, context) {
  const key = endpoint(candidate.graduate_type, candidate.graduate_code);
  if (targets.has(key)) fail(`${context} 重复声明研究生目标 ${key}`);
  targets.set(key, candidate);
}

function setOverrideTarget(targets, candidate) {
  targets.set(endpoint(candidate.graduate_type, candidate.graduate_code), candidate);
}

function assertPrimaryCapacity(targets, majorCode) {
  for (const graduateType of [ACADEMIC_TYPE, PROFESSIONAL_TYPE]) {
    const primaries = [...targets.values()].filter(
      (candidate) => candidate.graduate_type === graduateType && candidate.is_primary,
    );
    if (primaries.length > 1) {
      fail(`${majorCode} 在 ${graduateType} 中产生多个主映射：${primaries.map((candidate) => candidate.graduate_code).join("、")}`);
    }
  }
}

function seedFromClassRule(major, rule, graduateByKey) {
  const targets = new Map();
  const common = {
    undergraduateCode: major.major_code,
    rationale: rule.rationale,
    generationMethod: CLASS_METHOD,
  };

  if (rule.academic_primary !== null) {
    validateTarget(rule.academic_primary, `${rule.class_code}.academic_primary`, ACADEMIC_TYPE, graduateByKey);
    if (rule.academic_primary.level !== MAIN_RELATION) fail(`${rule.class_code}.academic_primary 必须使用主映射/核心对应`);
    insertSeed(targets, makeWorkingCandidate({
      ...common,
      graduateType: ACADEMIC_TYPE,
      target: rule.academic_primary,
      isPrimary: true,
    }), rule.class_code);
  }

  if (rule.professional_primary !== null) {
    validateTarget(rule.professional_primary, `${rule.class_code}.professional_primary`, PROFESSIONAL_TYPE, graduateByKey);
    if (rule.professional_primary.level !== MAIN_RELATION) fail(`${rule.class_code}.professional_primary 必须使用主映射/核心对应`);
    insertSeed(targets, makeWorkingCandidate({
      ...common,
      graduateType: PROFESSIONAL_TYPE,
      target: rule.professional_primary,
      isPrimary: true,
    }), rule.class_code);
  }

  for (const [index, target] of rule.other_targets.entries()) {
    validateTarget(target, `${rule.class_code}.other_targets[${index}]`, target.graduate_type, graduateByKey);
    if (target.level === MAIN_RELATION) fail(`${rule.class_code}.other_targets[${index}] 不能使用主映射/核心对应`);
    insertSeed(targets, makeWorkingCandidate({
      ...common,
      graduateType: target.graduate_type,
      target,
      isPrimary: false,
    }), rule.class_code);
  }

  return targets;
}

function validateOverrideActions(majorCode, actions) {
  requireArray(actions, `major_overrides.${majorCode}`);
  if (actions.length === 0) fail(`major_overrides.${majorCode} 不能为空`);
  for (const [index, action] of actions.entries()) {
    requireObject(action, `major_overrides.${majorCode}[${index}]`);
    if (!SUPPORTED_ACTIONS.has(action.action)) fail(`${majorCode} 使用未知动作 ${String(action.action)}`);
    requireNonEmptyString(action.rationale ?? action.target?.rationale, `${majorCode}.${action.action}.rationale`);
  }
  const zeroActions = actions.filter((action) => action.action === "confirmed_zero");
  if (zeroActions.length > 0 && actions.length !== 1) fail(`${majorCode} 的 confirmed_zero 不能与其他动作并用`);
}

function applyOverrides({ major, targets, actions, graduateByKey, hasExplicitOverride }) {
  if (!hasExplicitOverride) return targets;
  validateOverrideActions(major.major_code, actions);
  if (actions[0].action === "confirmed_zero") return new Map();

  const removals = actions.filter((action) => action.action === "remove");
  const replacements = actions.filter((action) => action.action === "replace_primary");
  const downgrades = actions.filter((action) => action.action === "downgrade");
  const additions = actions.filter((action) => action.action === "add");

  for (const action of removals) {
    if (!graduateTypes.has(action.graduate_type)) fail(`${major.major_code}.remove 的 graduate_type 无效`);
    requireNonEmptyString(action.graduate_code, `${major.major_code}.remove.graduate_code`);
    const key = endpoint(action.graduate_type, action.graduate_code);
    if (!targets.delete(key)) fail(`${major.major_code}.remove 找不到继承目标 ${key}`);
  }

  for (const action of replacements) {
    if (!graduateTypes.has(action.graduate_type)) fail(`${major.major_code}.replace_primary 的 graduate_type 无效`);
    validateTarget(action.target, `${major.major_code}.replace_primary.target`, action.graduate_type, graduateByKey);
    if (action.target.level !== MAIN_RELATION) fail(`${major.major_code}.replace_primary 必须使用主映射/核心对应`);
    for (const [key, candidate] of targets) {
      if (candidate.graduate_type === action.graduate_type && candidate.is_primary) targets.delete(key);
    }
    setOverrideTarget(targets, makeWorkingCandidate({
      undergraduateCode: major.major_code,
      graduateType: action.graduate_type,
      target: action.target,
      isPrimary: true,
      rationale: action.target.rationale,
      generationMethod: OVERRIDE_METHOD,
    }));
  }

  for (const action of downgrades) {
    if (!graduateTypes.has(action.graduate_type)) fail(`${major.major_code}.downgrade 的 graduate_type 无效`);
    requireNonEmptyString(action.graduate_code, `${major.major_code}.downgrade.graduate_code`);
    if (!relationLevels.has(action.relation_level) || action.relation_level === MAIN_RELATION) {
      fail(`${major.major_code}.downgrade 必须指定非主映射关系层级`);
    }
    const key = endpoint(action.graduate_type, action.graduate_code);
    const inherited = targets.get(key);
    if (!inherited) fail(`${major.major_code}.downgrade 找不到继承目标 ${key}`);
    const replacesBasis = Object.hasOwn(action, "basis");
    if (replacesBasis) validateBasis(action.basis, `${major.major_code}.downgrade.basis`);
    targets.set(key, {
      ...inherited,
      relation_level: action.relation_level,
      is_primary: false,
      relation_basis: replacesBasis ? [...action.basis] : inherited.relation_basis,
      rationale: action.rationale,
      generation_method: OVERRIDE_METHOD,
    });
  }

  for (const action of additions) {
    const graduateType = action.target?.graduate_type;
    validateTarget(action.target, `${major.major_code}.add.target`, graduateType, graduateByKey);
    const key = endpoint(graduateType, action.target.code);
    if (targets.has(key)) {
      fail(`${major.major_code}.add 目标已存在 ${key}；请使用 replace_primary 或 downgrade 修改已有关系`);
    }
    const isPrimary = action.target.level === MAIN_RELATION;
    if (isPrimary) {
      const existingPrimary = [...targets.values()].find(
        (candidate) => candidate.graduate_type === graduateType && candidate.is_primary
          && candidate.graduate_code !== action.target.code,
      );
      if (existingPrimary) {
        fail(`${major.major_code}.add 会在 ${graduateType} 中产生第二个主映射；应使用 replace_primary`);
      }
    }
    setOverrideTarget(targets, makeWorkingCandidate({
      undergraduateCode: major.major_code,
      graduateType,
      target: action.target,
      isPrimary,
      rationale: action.target.rationale,
      generationMethod: OVERRIDE_METHOD,
    }));
  }

  assertPrimaryCapacity(targets, major.major_code);
  return targets;
}

function finalizeCandidate(candidate, graduateByKey) {
  const graduate = graduateByKey.get(endpoint(candidate.graduate_type, candidate.graduate_code));
  const isMilitary = isMilitaryRestrictedObject(graduate);
  const relationLevel = isMilitary ? policy.military_rule.relation_level : candidate.relation_level;
  const isPrimary = isMilitary ? policy.military_rule.is_primary : candidate.is_primary;
  const skillsBehavior = isMilitary
    ? policy.military_rule.skills_behavior
    : policy.relation_behavior_rules[relationLevel];
  const reviewStatus = isMilitary
    ? policy.military_rule.review_status
    : reviewStatusFor(relationLevel);

  return {
    mapping_id: `MAP-${candidate.undergraduate_code}-${typeLetter(candidate.graduate_type)}-${candidate.graduate_code}`,
    undergraduate_code: candidate.undergraduate_code,
    graduate_type: candidate.graduate_type,
    graduate_code: candidate.graduate_code,
    relation_level: relationLevel,
    is_primary: isPrimary,
    relation_basis: [...candidate.relation_basis],
    rationale: candidate.rationale,
    skills_behavior: skillsBehavior,
    military_restriction: isMilitary,
    review_status: reviewStatus,
    confidence: isMilitary ? "中" : confidenceFor(relationLevel),
    generation_method: isMilitary ? MILITARY_METHOD : candidate.generation_method,
  };
}

/**
 * Generate deterministic, schema-valid mapping candidates from class seeds and
 * explicit major-level decisions. Rules create candidates only; they never mark
 * a relationship as having completed human review.
 */
export function generateCandidates({ undergraduate, graduate, classRules, overrides }) {
  requireArray(undergraduate, "undergraduate");
  requireArray(graduate, "graduate");
  requireObject(classRules, "classRules");
  requireArray(classRules.class_rules, "classRules.class_rules");
  requireObject(overrides, "overrides");
  requireObject(overrides.major_overrides, "overrides.major_overrides");

  const declaredActions = new Set(overrides.supported_actions ?? []);
  for (const action of SUPPORTED_ACTIONS) {
    if (!declaredActions.has(action)) fail(`overrides.supported_actions 缺少 ${action}`);
  }

  const undergraduateByCode = new Map();
  for (const major of undergraduate) {
    requireNonEmptyString(major.major_code, "undergraduate.major_code");
    if (undergraduateByCode.has(major.major_code)) fail(`本科专业代码重复：${major.major_code}`);
    undergraduateByCode.set(major.major_code, major);
  }
  for (const majorCode of Object.keys(overrides.major_overrides)) {
    if (!undergraduateByCode.has(majorCode)) fail(`专业级例外引用不存在的本科专业：${majorCode}`);
  }

  const graduateByKey = new Map();
  for (const record of graduate) {
    const key = endpoint(record.object_type, record.object_code);
    if (graduateByKey.has(key)) fail(`研究生目录对象重复：${key}`);
    graduateByKey.set(key, record);
  }

  const classRuleByCode = new Map();
  for (const rule of classRules.class_rules) {
    requireObject(rule, "classRules.class_rules[]");
    requireNonEmptyString(rule.class_code, "classRules.class_rules[].class_code");
    requireNonEmptyString(rule.class_name, `${rule.class_code}.class_name`);
    requireNonEmptyString(rule.rationale, `${rule.class_code}.rationale`);
    if (!Object.hasOwn(rule, "academic_primary") || !Object.hasOwn(rule, "professional_primary")) {
      fail(`${rule.class_code} 必须显式声明 academic_primary 和 professional_primary，可使用 null`);
    }
    requireArray(rule.other_targets, `${rule.class_code}.other_targets`);
    if (classRuleByCode.has(rule.class_code)) fail(`专业类规则重复：${rule.class_code}`);
    classRuleByCode.set(rule.class_code, rule);
  }

  const generated = [];
  for (const major of [...undergraduate].sort((left, right) => left.major_code.localeCompare(right.major_code, "en"))) {
    let targets = new Map();
    const hasExplicitOverride = Object.hasOwn(overrides.major_overrides, major.major_code);
    if (major.class_code !== null) {
      const rule = classRuleByCode.get(major.class_code);
      if (!rule) fail(`本科专业 ${major.major_code} 缺少专业类规则 ${major.class_code}`);
      if (rule.class_name !== major.class_name) fail(`${major.class_code} 的规则名称与本科目录不一致`);
      targets = seedFromClassRule(major, rule, graduateByKey);
    } else if (!hasExplicitOverride) {
      fail(`未设置专业类的本科专业 ${major.major_code} 必须提供显式专业级例外或零映射决定`);
    }

    targets = applyOverrides({
      major,
      targets,
      actions: overrides.major_overrides[major.major_code],
      graduateByKey,
      hasExplicitOverride,
    });
    assertPrimaryCapacity(targets, major.major_code);
    for (const candidate of targets.values()) generated.push(finalizeCandidate(candidate, graduateByKey));
  }

  generated.sort((left, right) => left.mapping_id.localeCompare(right.mapping_id, "en"));
  validateBundle({ undergraduate, graduate, mappings: generated });
  return generated;
}

function countBy(records, field) {
  return Object.fromEntries(
    [...new Set(records.map((record) => record[field]))]
      .sort((left, right) => left.localeCompare(right, "zh-CN"))
      .map((value) => [value, records.filter((record) => record[field] === value).length]),
  );
}

async function generateArtifact() {
  const root = new URL("./", import.meta.url);
  const undergraduatePayload = JSON.parse(
    await fs.readFile(new URL("catalogs/undergraduate_2026.json", root), "utf8"),
  );
  const graduatePayload = JSON.parse(
    await fs.readFile(new URL("catalogs/graduate_effective.json", root), "utf8"),
  );
  const classRules = JSON.parse(
    await fs.readFile(new URL("rules/professional_class_seed_rules.json", root), "utf8"),
  );
  const overrides = JSON.parse(
    await fs.readFile(new URL("rules/major_overrides.json", root), "utf8"),
  );
  const records = generateCandidates({
    undergraduate: undergraduatePayload.records,
    graduate: graduatePayload.records,
    classRules,
    overrides,
  });
  const payload = {
    metadata: {
      record_count: records.length,
      undergraduate_major_count: undergraduatePayload.records.length,
      class_rule_count: classRules.class_rules.length,
      override_major_count: Object.keys(overrides.major_overrides).length,
      generation_method_counts: countBy(records, "generation_method"),
      review_status_counts: countBy(records, "review_status"),
    },
    records,
  };
  const output = new URL("artifacts/mapping_candidates.json", root);
  await fs.mkdir(new URL("artifacts/", root), { recursive: true });
  await fs.writeFile(output, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  console.log(`generated ${records.length} mapping candidates: ${fileURLToPath(output)}`);
}

const invokedPath = process.argv[1] ? path.resolve(process.argv[1]) : null;
if (invokedPath === fileURLToPath(import.meta.url)) {
  await generateArtifact();
}
