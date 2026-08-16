import assert from "node:assert/strict";

import {
  CONFIDENCE_LEVELS,
  GRADUATE_OBJECT_TYPES,
  MILITARY_RULE,
  RELATION_BASES,
  RELATION_LEVELS,
  REVIEW_STATUSES,
  SKILLS_BEHAVIORS,
  graduateKey,
  validateBundle,
  validateMappingRecord,
} from "../discipline_mapping/mapping_schema.mjs";

const undergraduateByCode = new Map([
  ["080901", { major_code: "080901", major_name: "计算机科学与技术" }],
]);
const graduateByKey = new Map([
  ["学术学位一级学科|0812", {
    object_code: "0812",
    object_name: "计算机科学与技术",
    object_type: "学术学位一级学科",
    category_code: "08",
  }],
  ["学术学位一级学科|0809", {
    object_code: "0809",
    object_name: "电子科学与技术",
    object_type: "学术学位一级学科",
    category_code: "08",
  }],
  ["专业学位类别|0854", {
    object_code: "0854",
    object_name: "电子信息",
    object_type: "专业学位类别",
    category_code: "08",
  }],
  ["学术学位一级学科|1105", {
    object_code: "1105",
    object_name: "军队指挥学",
    object_type: "学术学位一级学科",
    category_code: "11",
  }],
]);

const ordinaryMapping = Object.freeze({
  mapping_id: "MAP-080901-A-0812",
  undergraduate_code: "080901",
  graduate_type: "学术学位一级学科",
  graduate_code: "0812",
  relation_level: "主映射/核心对应",
  is_primary: true,
  relation_basis: ["核心知识基础"],
  rationale: "本科与研究生阶段均以计算机系统、软件与计算理论为核心。",
  skills_behavior: "默认标签",
  military_restriction: false,
  review_status: "已依据规则复核",
  confidence: "高",
});

const militaryMapping = Object.freeze({
  ...ordinaryMapping,
  mapping_id: "MAP-080901-A-1105",
  graduate_code: "1105",
  relation_level: "目录参考",
  is_primary: false,
  relation_basis: ["关键技术体系"],
  rationale: "保留目录关系记录，不参与 Skills 标签、检索或推荐。",
  skills_behavior: "仅目录查看",
  military_restriction: true,
  review_status: "军事学限制",
  confidence: "中",
});

assert.deepEqual(RELATION_LEVELS, ["主映射/核心对应", "其他核心对应", "强相关", "延伸相关", "目录参考"]);
assert.deepEqual(SKILLS_BEHAVIORS, ["默认标签", "默认辅助标签", "扩展检索", "跨学科召回", "仅目录查看", "无"]);
assert.deepEqual(REVIEW_STATUSES, ["已依据规则复核", "高置信度候选", "存在歧义，建议学科专家复核", "已确认无直接对应", "尚未完成复核", "军事学限制", "目录版本差异待处理"]);
assert.deepEqual(CONFIDENCE_LEVELS, ["高", "中", "低"]);
assert.deepEqual(RELATION_BASES, ["主要研究对象", "核心知识基础", "主要研究或实践方法", "关键技术体系", "典型职业或行业场景", "培养出口", "教育部目录或正式说明中的明确衔接", "跨学科应用关系"]);
assert.deepEqual(GRADUATE_OBJECT_TYPES, ["学术学位一级学科", "专业学位类别"]);
assert.deepEqual(MILITARY_RULE, {
  relation_level: "目录参考",
  is_primary: false,
  skills_behavior: "仅目录查看",
  military_restriction: true,
  review_status: "军事学限制",
});

assert.equal(graduateKey("学术学位一级学科", "0812"), "学术学位一级学科|0812");
assert.doesNotThrow(() => validateMappingRecord(ordinaryMapping, undergraduateByCode, graduateByKey));
assert.doesNotThrow(() => validateMappingRecord(militaryMapping, undergraduateByCode, graduateByKey));

assert.throws(
  () => validateMappingRecord({ ...ordinaryMapping, undergraduate_code: "999999" }, undergraduateByCode, graduateByKey),
  /本科.*目录|undergraduate/i,
);
assert.throws(
  () => validateMappingRecord({ ...ordinaryMapping, graduate_code: "9999" }, undergraduateByCode, graduateByKey),
  /研究生.*目录|graduate/i,
);
assert.throws(
  () => validateMappingRecord({ ...ordinaryMapping, rationale: "  " }, undergraduateByCode, graduateByKey),
  /理由|rationale/i,
);
assert.throws(
  () => validateMappingRecord({ ...ordinaryMapping, relation_level: "名称相似" }, undergraduateByCode, graduateByKey),
  /relation_level/,
);
assert.throws(
  () => validateMappingRecord({ ...ordinaryMapping, relation_basis: ["核心知识基础", "核心知识基础"] }, undergraduateByCode, graduateByKey),
  /重复|duplicate/i,
);
assert.throws(
  () => validateMappingRecord({ ...ordinaryMapping, relation_level: "强相关" }, undergraduateByCode, graduateByKey),
  /主映射|primary/i,
);
assert.throws(
  () => validateMappingRecord({ ...militaryMapping, skills_behavior: "扩展检索" }, undergraduateByCode, graduateByKey),
  /军事学/,
);
assert.throws(
  () => validateMappingRecord({ ...militaryMapping, military_restriction: false }, undergraduateByCode, graduateByKey),
  /军事学/,
);
assert.throws(
  () => validateMappingRecord({ ...ordinaryMapping, military_restriction: true }, undergraduateByCode, graduateByKey),
  /军事学/,
);

assert.doesNotThrow(() => validateBundle(bundleWithCatalogs([ordinaryMapping, militaryMapping])));
assert.throws(
  () => validateBundle(bundleWithCatalogs([ordinaryMapping, { ...ordinaryMapping, mapping_id: "MAP-DUPLICATE" }])),
  /重复|duplicate/i,
);
assert.throws(
  () => validateBundle(bundleWithCatalogs([ordinaryMapping, {
    ...ordinaryMapping,
    mapping_id: "MAP-080901-A-0812-SECOND",
    graduate_code: "0812",
    relation_basis: ["关键技术体系"],
  }])),
  /重复|duplicate/i,
);
assert.throws(
  () => validateBundle(bundleWithCatalogs([ordinaryMapping, {
    ...ordinaryMapping,
    mapping_id: "MAP-080901-A-0809",
    graduate_code: "0809",
    graduate_type: "学术学位一级学科",
  }])),
  /主映射|primary/i,
);
assert.throws(
  () => validateBundle(bundleWithCatalogs([{ ...ordinaryMapping, relation_level: "强相关" }])),
  /主映射|primary/i,
);
assert.throws(
  () => validateBundle(bundleWithCatalogs([{ ...militaryMapping, skills_behavior: "扩展检索" }])),
  /军事学/,
);

function bundleWithCatalogs(mappings) {
  return {
    undergraduate: [...undergraduateByCode.values()],
    graduate: [...graduateByKey.values()],
    mappings,
  };
}

console.log("discipline mapping schema tests passed");
