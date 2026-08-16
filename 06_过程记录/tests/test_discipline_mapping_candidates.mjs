import assert from "node:assert/strict";
import fs from "node:fs/promises";

import { generateCandidates } from "../discipline_mapping/generate_mapping_candidates.mjs";
import { validateBundle } from "../discipline_mapping/mapping_schema.mjs";

const root = new URL("../discipline_mapping/", import.meta.url);
const undergraduate = JSON.parse(
  await fs.readFile(new URL("catalogs/undergraduate_2026.json", root), "utf8"),
).records;
const graduate = JSON.parse(
  await fs.readFile(new URL("catalogs/graduate_effective.json", root), "utf8"),
).records;
const classRules = JSON.parse(
  await fs.readFile(new URL("rules/professional_class_seed_rules.json", root), "utf8"),
);
const overrides = JSON.parse(
  await fs.readFile(new URL("rules/major_overrides.json", root), "utf8"),
);

const academicType = "学术学位一级学科";
const professionalType = "专业学位类别";
const approvedBases = new Set([
  "主要研究对象",
  "核心知识基础",
  "主要研究或实践方法",
  "关键技术体系",
  "典型职业或行业场景",
  "培养出口",
  "教育部目录或正式说明中的明确衔接",
  "跨学科应用关系",
]);
const graduateKeys = new Set(graduate.map((record) => `${record.object_type}|${record.object_code}`));
const actualClasses = new Map(
  undergraduate
    .filter((record) => record.class_code !== null)
    .map((record) => [record.class_code, record.class_name]),
);

assert.equal(actualClasses.size, 92);
assert.equal(classRules.class_rules.length, 92);
assert.equal(new Set(classRules.class_rules.map((rule) => rule.class_code)).size, 92);
assert.deepEqual(
  new Set(classRules.class_rules.map((rule) => rule.class_code)),
  new Set(actualClasses.keys()),
);

for (const rule of classRules.class_rules) {
  assert.equal(rule.class_name, actualClasses.get(rule.class_code));
  assert.ok(typeof rule.rationale === "string" && rule.rationale.trim().length > 0);
  assert.ok(Object.hasOwn(rule, "academic_primary"));
  assert.ok(Object.hasOwn(rule, "professional_primary"));
  assert.ok(Array.isArray(rule.other_targets));

  const targets = [
    ...(rule.academic_primary ? [{ ...rule.academic_primary, graduate_type: academicType }] : []),
    ...(rule.professional_primary ? [{ ...rule.professional_primary, graduate_type: professionalType }] : []),
    ...rule.other_targets,
  ];
  const endpoints = new Set();
  for (const target of targets) {
    assert.ok(graduateKeys.has(`${target.graduate_type}|${target.code}`));
    assert.ok(Array.isArray(target.basis) && target.basis.length > 0);
    assert.ok(target.basis.every((basis) => approvedBases.has(basis)));
    const endpoint = `${target.graduate_type}|${target.code}`;
    assert.ok(!endpoints.has(endpoint), `${rule.class_code} has duplicate target ${endpoint}`);
    endpoints.add(endpoint);
  }
}

const category14Majors = undergraduate.filter((record) => record.category_code === "14");
assert.equal(category14Majors.length, 15);
assert.ok(category14Majors.every((record) => record.class_code === null && record.class_name === null));
assert.deepEqual(
  new Set(Object.keys(overrides.major_overrides).filter((code) => code.startsWith("14"))),
  new Set(category14Majors.map((record) => record.major_code)),
);
for (const major of category14Majors) {
  const actions = overrides.major_overrides[major.major_code];
  assert.ok(Array.isArray(actions) && actions.length > 0);
  assert.ok(actions.some((action) => action.action === "add" || action.action === "confirmed_zero"));
}
assert.deepEqual(
  new Set(overrides.supported_actions),
  new Set(["add", "remove", "replace_primary", "downgrade", "confirmed_zero"]),
);

const candidates = generateCandidates({ undergraduate, graduate, classRules, overrides });
const candidatesAgain = generateCandidates({ undergraduate, graduate, classRules, overrides });
assert.deepEqual(candidatesAgain, candidates);
const artifact = JSON.parse(
  await fs.readFile(new URL("artifacts/mapping_candidates.json", root), "utf8"),
);
assert.equal(artifact.metadata.record_count, candidates.length);
assert.equal(artifact.metadata.class_rule_count, 92);
assert.deepEqual(artifact.records, candidates);
assert.equal(new Set(candidates.map((candidate) => candidate.mapping_id)).size, candidates.length);
assert.deepEqual(
  candidates.map((candidate) => candidate.mapping_id),
  [...candidates].sort((left, right) => left.mapping_id.localeCompare(right.mapping_id, "en")).map((candidate) => candidate.mapping_id),
);
assert.doesNotThrow(() => validateBundle({ undergraduate, graduate, mappings: candidates }));

function targets(majorName) {
  const code = undergraduate.find((record) => record.major_name === majorName).major_code;
  return candidates
    .filter((candidate) => candidate.undergraduate_code === code)
    .map((candidate) => `${candidate.graduate_type}|${candidate.graduate_code}|${candidate.relation_level}`);
}

assert.ok(targets("哲学").some((target) => target.startsWith(`${academicType}|0101|`)));
assert.ok(targets("法学").some((target) => target.startsWith(`${professionalType}|0351|`)));
assert.ok(targets("计算机科学与技术").some((target) => target.startsWith(`${academicType}|0812|`)));
assert.ok(targets("临床医学").some((target) => target.startsWith(`${professionalType}|1051|`)));
assert.ok(targets("艺术设计学").some((target) => target.includes("1403")));
assert.ok(candidates.every((candidate) => candidate.review_status !== "已依据规则复核"));
assert.ok(candidates.every((candidate) => graduateKeys.has(`${candidate.graduate_type}|${candidate.graduate_code}`)));
assert.ok(candidates.every((candidate) => candidate.mapping_id === `MAP-${candidate.undergraduate_code}-${candidate.graduate_type === academicType ? "A" : "P"}-${candidate.graduate_code}`));

const category14Codes = new Set(category14Majors.map((record) => record.major_code));
assert.ok(
  candidates
    .filter((candidate) => category14Codes.has(candidate.undergraduate_code))
    .every((candidate) => candidate.generation_method === "专业级例外" || candidate.generation_method === "军事学目录参考"),
);

for (const candidate of candidates) {
  const graduateRecord = graduate.find(
    (record) => record.object_type === candidate.graduate_type && record.object_code === candidate.graduate_code,
  );
  if (graduateRecord.category_code === "11") {
    assert.deepEqual(
      {
        relation_level: candidate.relation_level,
        is_primary: candidate.is_primary,
        skills_behavior: candidate.skills_behavior,
        military_restriction: candidate.military_restriction,
        review_status: candidate.review_status,
        generation_method: candidate.generation_method,
      },
      {
        relation_level: "目录参考",
        is_primary: false,
        skills_behavior: "仅目录查看",
        military_restriction: true,
        review_status: "军事学限制",
        generation_method: "军事学目录参考",
      },
    );
  }
}

const syntheticGraduate = [
  graduateRecord(academicType, "0101", "哲学", "01"),
  graduateRecord(academicType, "0201", "理论经济学", "02"),
  graduateRecord(academicType, "0301", "法学", "03"),
  graduateRecord(academicType, "1105", "军队指挥学", "11"),
  graduateRecord(professionalType, "0251", "金融", "02"),
];
const syntheticClassRules = {
  class_rules: [{
    class_code: "X001",
    class_name: "测试类",
    academic_primary: target("0101", "主映射/核心对应"),
    professional_primary: target("0251", "主映射/核心对应"),
    other_targets: [
      { ...target("0201", "强相关"), graduate_type: academicType },
      { ...target("1105", "强相关"), graduate_type: academicType },
    ],
    rationale: "用于验证专业级动作的确定顺序。",
  }],
};
const syntheticUndergraduate = [
  undergraduateRecord("X00101", "动作专业", "X001"),
  undergraduateRecord("X00102", "零映射专业", "X001"),
];
const syntheticOverrides = {
  supported_actions: ["add", "remove", "replace_primary", "downgrade", "confirmed_zero"],
  major_overrides: {
    X00101: [
      { action: "remove", graduate_type: academicType, graduate_code: "0201", rationale: "排除不适用目标。" },
      {
        action: "replace_primary",
        graduate_type: academicType,
        target: { ...target("0301", "主映射/核心对应"), rationale: "以专业级主映射替换类级主映射。" },
      },
      {
        action: "downgrade",
        graduate_type: professionalType,
        graduate_code: "0251",
        relation_level: "强相关",
        rationale: "该专业只与金融形成强相关关系。",
      },
      {
        action: "add",
        target: {
          ...target("0201", "延伸相关"),
          graduate_type: academicType,
          rationale: "移除类级关系后以专业级跨学科关系重新加入。",
        },
      },
    ],
    X00102: [{ action: "confirmed_zero", rationale: "明确确认无直接对应。" }],
  },
};
const syntheticCandidates = generateCandidates({
  undergraduate: syntheticUndergraduate,
  graduate: syntheticGraduate,
  classRules: syntheticClassRules,
  overrides: syntheticOverrides,
});
assert.deepEqual(
  syntheticCandidates.map((candidate) => [
    candidate.mapping_id,
    candidate.relation_level,
    candidate.is_primary,
    candidate.generation_method,
  ]),
  [
    ["MAP-X00101-A-0201", "延伸相关", false, "专业级例外"],
    ["MAP-X00101-A-0301", "主映射/核心对应", true, "专业级例外"],
    ["MAP-X00101-A-1105", "目录参考", false, "军事学目录参考"],
    ["MAP-X00101-P-0251", "强相关", false, "专业级例外"],
  ],
);
assert.equal(syntheticCandidates.some((candidate) => candidate.undergraduate_code === "X00102"), false);

assert.throws(
  () => generateCandidates({
    undergraduate: [undergraduateRecord("X00103", "无效规则专业", "X001")],
    graduate: syntheticGraduate,
    classRules: {
      class_rules: [{
        ...syntheticClassRules.class_rules[0],
        academic_primary: target("9999", "主映射/核心对应"),
        professional_primary: null,
        other_targets: [],
      }],
    },
    overrides: { supported_actions: syntheticOverrides.supported_actions, major_overrides: {} },
  }),
  /9999|研究生目录|graduate/i,
);

function target(code, level) {
  return { code, level, basis: ["核心知识基础"] };
}

function graduateRecord(objectType, objectCode, objectName, categoryCode) {
  return {
    category_code: categoryCode,
    category_name: "测试门类",
    degree_levels: ["硕士"],
    notes: [],
    object_code: objectCode,
    object_name: objectName,
    object_type: objectType,
    previous_names: [],
    source_ids: ["test"],
    status: "current",
  };
}

function undergraduateRecord(majorCode, majorName, classCode) {
  return {
    attributes: [],
    category_code: "X0",
    category_name: "测试门类",
    class_code: classCode,
    class_name: "测试类",
    degree_categories: ["测试"],
    duration: null,
    major_code: majorCode,
    major_name: majorName,
    source_id: "test",
  };
}

console.log("discipline mapping candidate tests passed");
