import assert from "node:assert/strict";

import {
  isRestrictedObject,
  validateBundle,
  validateMappingRecord,
  validateReviewRow,
} from "../vocational_undergraduate_mapping/mapping_schema.mjs";

const vocationalRows = [
  { major_code: "510201", major_name: "计算机应用技术", class_code: "5102" },
  { major_code: "580101K", major_name: "治安管理", class_code: "5801" },
];
const undergraduateRows = [
  { major_code: "080901", major_name: "计算机科学与技术", class_code: "0809" },
  { major_code: "082101", major_name: "武器系统与工程", class_code: "0821" },
  { major_code: "030601K", major_name: "治安学", class_code: "0306" },
];
const vocational = new Map(vocationalRows.map((row) => [row.major_code, row]));
const undergraduate = new Map(
  undergraduateRows.map((row) => [row.major_code, row]),
);

const valid = {
  mapping_id: "VUG-510201-080901",
  vocational_code: "510201",
  undergraduate_code: "080901",
  relation_level: "主映射/核心对应",
  is_primary: true,
  relation_basis: ["核心知识基础", "关键技术体系"],
  rationale: "均以计算机系统、软件和应用开发为核心技术体系。",
  skills_behavior: "默认标签",
  sensitive_restriction: false,
  consumable: true,
  review_status: "已依据规则复核",
  confidence: "高",
  generation_method: "专业名称与专业类规则",
};

assert.doesNotThrow(() =>
  validateMappingRecord(valid, vocational, undergraduate),
);

assert.equal(
  isRestrictedObject(vocational.get("510201"), undergraduate.get("082101")),
  true,
);
assert.equal(
  isRestrictedObject(vocational.get("580101K"), undergraduate.get("030601K")),
  false,
);

const wrongRestricted = {
  ...valid,
  mapping_id: "VUG-510201-082101",
  undergraduate_code: "082101",
  relation_level: "强相关",
  is_primary: false,
  skills_behavior: "扩展检索",
  sensitive_restriction: true,
  review_status: "敏感专业限制",
  confidence: "中",
};
assert.throws(
  () => validateMappingRecord(wrongRestricted, vocational, undergraduate),
  /敏感对象/,
);

const restricted = {
  ...wrongRestricted,
  relation_level: "目录参考",
  skills_behavior: "仅目录查看",
  consumable: false,
};
assert.doesNotThrow(() =>
  validateMappingRecord(restricted, vocational, undergraduate),
);
for (const mutation of [
  { relation_level: "强相关" },
  { is_primary: true },
  { skills_behavior: "扩展检索" },
  { sensitive_restriction: false },
  { consumable: true },
  { review_status: "已依据规则复核" },
]) {
  assert.throws(
    () =>
      validateMappingRecord(
        { ...restricted, ...mutation },
        vocational,
        undergraduate,
      ),
    /敏感对象|只有主映射/,
  );
}

assert.doesNotThrow(() =>
  validateMappingRecord(
    {
      ...valid,
      relation_level: "目录参考",
      is_primary: false,
      skills_behavior: "仅目录查看",
      consumable: false,
    },
    vocational,
    undergraduate,
  ),
);

assert.throws(
  () =>
    validateMappingRecord(
      { ...valid, relation_level: "强相关", is_primary: true },
      vocational,
      undergraduate,
    ),
  /只有主映射/,
);
assert.throws(
  () =>
    validateMappingRecord(
      { ...valid, relation_basis: ["核心知识基础", "核心知识基础"] },
      vocational,
      undergraduate,
    ),
  /重复/,
);

assert.doesNotThrow(() =>
  validateReviewRow(
    {
      vocational_code: "510201",
      accepted_mapping_ids: ["VUG-510201-080901"],
      rejected_mapping_ids: ["VUG-510201-082101"],
      zero_direct: false,
      zero_all: false,
      review_status: "已依据规则复核",
      review_note: "逐候选完成复核。",
      reviewed_at: "2026-08-17",
    },
    ["VUG-510201-080901", "VUG-510201-082101"],
  ),
);
assert.throws(
  () =>
    validateReviewRow(
      {
        vocational_code: "510201",
        accepted_mapping_ids: ["VUG-510201-080901"],
        rejected_mapping_ids: [],
        zero_direct: false,
        zero_all: false,
        review_status: "已依据规则复核",
        review_note: "候选分区不完整。",
        reviewed_at: "2026-08-17",
      },
      ["VUG-510201-080901", "VUG-510201-082101"],
    ),
  /穷尽/,
);

assert.doesNotThrow(() =>
  validateBundle({
    vocational_catalog: vocationalRows,
    undergraduate_catalog: undergraduateRows,
    mappings: [valid, restricted],
  }),
);

console.log("vocational mapping schema: OK");
