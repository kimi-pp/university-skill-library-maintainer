import assert from "node:assert/strict";
import fs from "node:fs/promises";

import { validateBundle } from "../vocational_undergraduate_mapping/mapping_schema.mjs";

const root = "06_过程记录/vocational_undergraduate_mapping";
const bundle = JSON.parse(
  await fs.readFile(`${root}/artifacts/mapping_bundle.json`, "utf8"),
);
const ledger = JSON.parse(
  await fs.readFile(`${root}/review/vocational_review_ledger.json`, "utf8"),
);
const reverseLedger = JSON.parse(
  await fs.readFile(`${root}/review/undergraduate_reverse_ledger.json`, "utf8"),
);
const qa = JSON.parse(await fs.readFile(`${root}/artifacts/qa_findings.json`, "utf8"));
const summary = JSON.parse(await fs.readFile(`${root}/artifacts/summary.json`, "utf8"));

validateBundle(bundle);
assert.equal(bundle.vocational_catalog.length, 811);
assert.equal(bundle.undergraduate_catalog.length, 883);
assert.equal(bundle.vocational_index.length, 811);
assert.equal(bundle.undergraduate_index.length, 883);
assert.equal(bundle.class_aggregation.length, 97);
assert.equal(new Set(bundle.mappings.map((row) => row.mapping_id)).size, bundle.mappings.length);

const accepted = new Set(ledger.records.flatMap((row) => row.accepted_mapping_ids));
assert.deepEqual(new Set(bundle.mappings.map((row) => row.mapping_id)), accepted);
assert.deepEqual(
  new Set(bundle.vocational_index.map((row) => row.vocational_code)),
  new Set(bundle.vocational_catalog.map((row) => row.major_code)),
);
assert.deepEqual(
  new Set(bundle.undergraduate_index.map((row) => row.undergraduate_code)),
  new Set(bundle.undergraduate_catalog.map((row) => row.major_code)),
);
assert.deepEqual(
  bundle.undergraduate_index.map((row) => row.coverage_state),
  reverseLedger.records.map((row) => row.coverage_state),
);
for (const row of bundle.mappings.filter((mapping) => mapping.sensitive_restriction)) {
  assert.deepEqual(
    [row.relation_level, row.skills_behavior, row.is_primary, row.consumable],
    ["目录参考", "仅目录查看", false, false],
  );
}
for (const row of bundle.vocational_index) {
  const expected = ledger.records.find(
    (ledgerRow) => ledgerRow.vocational_code === row.vocational_code,
  );
  assert.deepEqual(row.mapping_ids, expected.accepted_mapping_ids);
  assert.equal(row.zero_direct, expected.zero_direct);
  assert.equal(row.zero_all, expected.zero_all);
}
assert.equal(qa.blocking.length, 0);
assert.equal(qa.review.length, 5);
assert.equal(qa.notice.length, 10);
assert.equal(summary.vocational_count, 811);
assert.equal(summary.undergraduate_count, 883);
assert.equal(summary.class_count, 97);
assert.equal(summary.mapping_count, bundle.mappings.length);
assert.equal(summary.blocking_count, 0);
assert.equal(summary.expert_review_count, 5);
assert.ok(
  bundle.sources.official_sources.some((source) => source.id === "undergraduate_2026_pdf"),
);
assert.equal(
  summary.vocational_zero_all,
  bundle.vocational_index.filter((row) => row.zero_all).length,
);

console.log(`vocational mapping bundle: ${bundle.mappings.length} OK`);
