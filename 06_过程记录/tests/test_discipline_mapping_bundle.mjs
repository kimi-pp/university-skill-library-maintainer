import assert from "node:assert/strict";
import fs from "node:fs/promises";

import {
  MappingBundleBuildError,
  buildMappingBundle,
} from "../discipline_mapping/build_mapping_bundle.mjs";

const root = new URL("../discipline_mapping/", import.meta.url);
const bundle = JSON.parse(
  await fs.readFile(new URL("artifacts/mapping_bundle.json", root), "utf8"),
);
const qaArtifact = JSON.parse(
  await fs.readFile(new URL("artifacts/qa_findings.json", root), "utf8"),
);
const summaryArtifact = JSON.parse(
  await fs.readFile(new URL("artifacts/summary.json", root), "utf8"),
);
const undergraduatePayload = JSON.parse(
  await fs.readFile(new URL("catalogs/undergraduate_2026.json", root), "utf8"),
);
const graduatePayload = JSON.parse(
  await fs.readFile(new URL("catalogs/graduate_effective.json", root), "utf8"),
);
const candidatesPayload = JSON.parse(
  await fs.readFile(new URL("artifacts/mapping_candidates.json", root), "utf8"),
);
const overrides = JSON.parse(
  await fs.readFile(new URL("rules/major_overrides.json", root), "utf8"),
);
const policy = JSON.parse(
  await fs.readFile(new URL("rules/mapping_policy.json", root), "utf8"),
);
const undergraduateReview = JSON.parse(
  await fs.readFile(new URL("review/major_review_ledger.json", root), "utf8"),
);
const graduateReview = JSON.parse(
  await fs.readFile(new URL("review/graduate_review_ledger.json", root), "utf8"),
);

const inputs = {
  undergraduate: undergraduatePayload,
  graduate: graduatePayload,
  candidates: candidatesPayload,
  overrides,
  policy,
  undergraduateReview,
  graduateReview,
};

assert.equal(bundle.undergraduate.length, 883);
assert.equal(bundle.undergraduate_index.length, 883);
assert.equal(bundle.graduate.length, 184);
assert.equal(bundle.graduate_index.length, bundle.graduate.length);
assert.equal(new Set(bundle.mappings.map((row) => row.mapping_id)).size, bundle.mappings.length);
assert.equal(bundle.qa_findings.filter((row) => row.severity === "阻断").length, 0);
assert.deepEqual(qaArtifact, bundle.qa_findings);
assert.deepEqual(summaryArtifact, bundle.summary);

for (const major of bundle.undergraduate) {
  assert.ok(
    bundle.undergraduate_index.some((row) => row.undergraduate_code === major.major_code),
    `missing undergraduate index row: ${major.major_code}`,
  );
}

for (const object of bundle.graduate) {
  assert.ok(
    bundle.graduate_index.some(
      (row) => row.graduate_type === object.object_type && row.graduate_code === object.object_code,
    ),
    `missing graduate index row: ${object.object_type}|${object.object_code}`,
  );
}

for (const row of bundle.mappings.filter((mapping) => mapping.military_restriction)) {
  assert.equal(row.relation_level, "目录参考");
  assert.equal(row.skills_behavior, "仅目录查看");
  assert.equal(row.is_primary, false);
}

const undergraduateZeroRows = bundle.undergraduate_index.filter((row) => row.mapping_count === 0);
const graduateZeroRows = bundle.graduate_index.filter((row) => row.mapping_count === 0);
assert.equal(bundle.summary.undergraduate_no_accepted_mapping_count, undergraduateZeroRows.length);
assert.equal(bundle.summary.graduate_no_accepted_mapping_count, graduateZeroRows.length);
assert.equal(
  bundle.summary.undergraduate_zero_mapping_count,
  bundle.undergraduate_index.filter((row) => row.zero_mapping_types.length === policy.graduate_object_types.length).length,
);
assert.equal(
  bundle.summary.undergraduate_partial_zero_mapping_count,
  bundle.undergraduate_index.filter(
    (row) => row.zero_mapping_types.length > 0
      && row.zero_mapping_types.length < policy.graduate_object_types.length,
  ).length,
);
assert.equal(
  bundle.summary.graduate_zero_mapping_count,
  bundle.graduate_index.filter((row) => row.reverse_state === "已确认无直接对应本科专业").length,
);
assert.equal(bundle.summary.military_mapping_count, bundle.mappings.filter((row) => row.military_restriction).length);
assert.equal(bundle.summary.blocking_finding_count, 0);

const rebuilt = buildMappingBundle(inputs);
assert.deepEqual(rebuilt, bundle);

const acceptedMappingIds = new Set(
  undergraduateReview.records.flatMap((row) => row.accepted_mapping_ids),
);
assert.deepEqual(new Set(bundle.mappings.map((row) => row.mapping_id)), acceptedMappingIds);
assert.ok(bundle.undergraduate_index.some((row) => row.mapping_count === 0));
assert.ok(bundle.graduate_index.some((row) => row.mapping_count === 0));
assert.equal(new Set(bundle.qa_findings.map((row) => row.finding_id)).size, bundle.qa_findings.length);
assert.ok(bundle.qa_findings.some((row) => row.check_code === "EXPERT_REVIEW_REQUIRED"));
assert.ok(bundle.qa_findings.some((row) => row.check_code === "OVER_BROAD_GRADUATE_COVERAGE"));
assert.ok(bundle.qa_findings.every((row) => row.check_code !== "EXPERT_REVIEW_REQUIRED" || row.severity !== "阻断"));

const reviewByMajor = new Map(
  undergraduateReview.records.map((row) => [row.undergraduate_code, row]),
);
for (const mapping of bundle.mappings.filter((row) => !row.military_restriction)) {
  assert.equal(mapping.review_status, reviewByMajor.get(mapping.undergraduate_code).review_status);
}

const relationRank = new Map(policy.relation_levels.map((value, index) => [value, index]));
const graduateTypeRank = new Map(policy.graduate_object_types.map((value, index) => [value, index]));
const expectedMappingOrder = [...bundle.mappings].sort((left, right) =>
  left.undergraduate_code.localeCompare(right.undergraduate_code, "en")
  || graduateTypeRank.get(left.graduate_type) - graduateTypeRank.get(right.graduate_type)
  || relationRank.get(left.relation_level) - relationRank.get(right.relation_level)
  || left.graduate_code.localeCompare(right.graduate_code, "en")
  || left.mapping_id.localeCompare(right.mapping_id, "en")
);
assert.deepEqual(bundle.mappings, expectedMappingOrder);

for (const row of bundle.mappings) {
  const graduate = bundle.graduate.find(
    (object) => object.object_type === row.graduate_type && object.object_code === row.graduate_code,
  );
  if (graduate.category_code === policy.military_category_code
      || policy.military_restricted_objects.some(
        (object) => object.graduate_type === row.graduate_type && object.graduate_code === row.graduate_code,
      )) {
    assert.equal(row.military_restriction, true);
    assert.equal(row.relation_level, policy.military_rule.relation_level);
    assert.equal(row.skills_behavior, policy.military_rule.skills_behavior);
    assert.equal(row.is_primary, policy.military_rule.is_primary);
  }
}
for (const row of bundle.graduate_index.filter((entry) => entry.reverse_state === "军事学限制，仅目录参考")) {
  assert.equal(row.consumable_mapping_count, 0);
  assert.ok(row.primary_mapping_ids.length === 0);
}

function expectBlockingFailure(mutator, checkCode) {
  const changed = structuredClone(inputs);
  mutator(changed);
  assert.throws(
    () => buildMappingBundle(changed),
    (error) => error instanceof MappingBundleBuildError
      && error.qa_findings.some(
        (row) => row.severity === "阻断" && row.check_code === checkCode,
      ),
    `expected blocking ${checkCode} finding`,
  );
}

expectBlockingFailure((changed) => {
  changed.undergraduateReview.records[0].accepted_mapping_ids = ["MAP-NOT-IN-CANDIDATES"];
}, "INVALID_REFERENCE");

expectBlockingFailure((changed) => {
  changed.graduateReview.records[0].accepted_mapping_ids.push("MAP-NOT-IN-CANDIDATES");
}, "INVALID_REFERENCE");

expectBlockingFailure((changed) => {
  changed.undergraduateReview.records[0].review_status = "尚未完成复核";
}, "UNREVIEWED_RECORD");

expectBlockingFailure((changed) => {
  const acceptedId = changed.undergraduateReview.records[0].accepted_mapping_ids[0];
  changed.candidates.records.find((row) => row.mapping_id === acceptedId).rationale = "";
}, "MISSING_RATIONALE");

expectBlockingFailure((changed) => {
  changed.undergraduateReview.records[0].review_status = "目录版本差异待处理";
}, "CATALOG_VERSION_CONFLICT");

expectBlockingFailure((changed) => {
  const review = changed.graduateReview.records.find(
    (row) => row.reverse_state !== "军事学限制，仅目录参考",
  );
  review.reverse_state = "目录版本差异待处理";
}, "CATALOG_VERSION_CONFLICT");

expectBlockingFailure((changed) => {
  const restricted = changed.candidates.records.find((row) => row.military_restriction);
  restricted.skills_behavior = "扩展检索";
}, "MILITARY_LEAKAGE");

expectBlockingFailure((changed) => {
  const ledger = changed.undergraduateReview.records.find((row) => row.accepted_mapping_ids.length > 0);
  const original = changed.candidates.records.find((row) => row.mapping_id === ledger.accepted_mapping_ids[0]);
  const duplicate = { ...original, mapping_id: `${original.mapping_id}-DUPLICATE` };
  changed.candidates.records.push(duplicate);
  ledger.accepted_mapping_ids.push(duplicate.mapping_id);
}, "DUPLICATE_RELATIONSHIP");

expectBlockingFailure((changed) => {
  const ledger = changed.undergraduateReview.records.find((row) => {
    const accepted = row.accepted_mapping_ids.map(
      (id) => changed.candidates.records.find((candidate) => candidate.mapping_id === id),
    );
    return accepted.some((candidate) => candidate?.graduate_type === "学术学位一级学科" && candidate.is_primary);
  });
  const original = changed.candidates.records.find(
    (row) => ledger.accepted_mapping_ids.includes(row.mapping_id)
      && row.graduate_type === "学术学位一级学科" && row.is_primary,
  );
  const secondGraduate = changed.graduate.records.find(
    (row) => row.object_type === original.graduate_type
      && row.object_code !== original.graduate_code
      && row.category_code !== changed.policy.military_category_code
      && !changed.policy.military_restricted_objects.some(
        (object) => object.graduate_type === row.object_type && object.graduate_code === row.object_code,
      ),
  );
  const overflow = {
    ...original,
    mapping_id: `${original.mapping_id}-PRIMARY-OVERFLOW`,
    graduate_code: secondGraduate.object_code,
  };
  changed.candidates.records.push(overflow);
  ledger.accepted_mapping_ids.push(overflow.mapping_id);
}, "PRIMARY_OVERFLOW");

console.log("discipline mapping bundle reconciliation tests passed");
