import assert from "node:assert/strict";
import fs from "node:fs/promises";

import { validateMappingRecord } from "../vocational_undergraduate_mapping/mapping_schema.mjs";

const root = "06_过程记录/vocational_undergraduate_mapping";
const vocational = JSON.parse(
  await fs.readFile(`${root}/catalogs/vocational_effective_2026.json`, "utf8"),
).records;
const undergraduate = JSON.parse(
  await fs.readFile("06_过程记录/discipline_mapping/catalogs/undergraduate_2026.json", "utf8"),
).records;
const seeds = JSON.parse(
  await fs.readFile(`${root}/rules/vocational_class_seed_rules.json`, "utf8"),
).records;
const candidates = JSON.parse(
  await fs.readFile(`${root}/artifacts/mapping_candidates.json`, "utf8"),
).records;

assert.deepEqual(
  new Set(seeds.map((row) => row.vocational_class_code)),
  new Set(vocational.map((row) => row.class_code)),
);
assert.equal(seeds.length, 97);
assert.equal(new Set(seeds.map((row) => row.vocational_class_code)).size, 97);
assert.ok(
  seeds.every(
    (row) =>
      Array.isArray(row.undergraduate_class_codes) &&
      Array.isArray(row.default_targets) &&
      typeof row.rationale === "string" &&
      row.rationale.length >= 12,
  ),
);

assert.equal(new Set(candidates.map((row) => row.mapping_id)).size, candidates.length);
assert.ok(candidates.length > 0);
assert.ok(
  candidates.every(
    (row) =>
      row.mapping_id === `VUG-${row.vocational_code}-${row.undergraduate_code}`,
  ),
);
assert.ok(candidates.every((row) => row.relation_basis.length > 0));
assert.ok(candidates.every((row) => row.rationale.length >= 12));
assert.ok(candidates.every((row) => row.generation_method !== "skills-domain-only"));

const vocationalByCode = new Map(
  vocational.map((row) => [row.major_code, row]),
);
const undergraduateByCode = new Map(
  undergraduate.map((row) => [row.major_code, row]),
);
for (const row of candidates) {
  validateMappingRecord(row, vocationalByCode, undergraduateByCode);
}

const byPair = new Map(
  candidates.map((row) => [
    `${row.vocational_code}|${row.undergraduate_code}`,
    row,
  ]),
);
assert.equal(byPair.get("410105|090102")?.relation_level, "主映射/核心对应");
assert.equal(byPair.get("410105|090102")?.is_primary, true);
assert.equal(byPair.get("520101K|100201K")?.relation_level, "主映射/核心对应");
assert.equal(byPair.get("520102K|100301K")?.relation_level, "主映射/核心对应");
assert.equal(byPair.get("520201|101101K")?.relation_level, "主映射/核心对应");

for (const row of candidates.filter((candidate) => candidate.sensitive_restriction)) {
  assert.deepEqual(
    [row.relation_level, row.skills_behavior, row.is_primary, row.consumable],
    ["目录参考", "仅目录查看", false, false],
  );
}

console.log(`vocational mapping candidates: ${candidates.length} OK`);
