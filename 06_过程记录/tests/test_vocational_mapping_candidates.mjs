import assert from "node:assert/strict";
import fs from "node:fs/promises";

import {
  validateMappingRecord,
  validateReviewRow,
} from "../vocational_undergraduate_mapping/mapping_schema.mjs";

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
const overrides = JSON.parse(
  await fs.readFile(`${root}/rules/vocational_major_overrides.json`, "utf8"),
).records;
const candidates = JSON.parse(
  await fs.readFile(`${root}/artifacts/mapping_candidates.json`, "utf8"),
).records;
const ledger = JSON.parse(
  await fs.readFile(`${root}/review/vocational_review_ledger.json`, "utf8"),
);
const reverse = JSON.parse(
  await fs.readFile(`${root}/review/undergraduate_reverse_ledger.json`, "utf8"),
);

assert.deepEqual(
  new Set(seeds.map((row) => row.vocational_class_code)),
  new Set(vocational.map((row) => row.class_code)),
);
assert.equal(seeds.length, 97);
assert.equal(new Set(seeds.map((row) => row.vocational_class_code)).size, 97);
assert.equal(
  new Set(overrides.map((row) => row.vocational_code)).size,
  overrides.length,
);
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
assert.equal(byPair.has("460106|080205"), false);
assert.equal(byPair.get("460106|120701")?.relation_level, "主映射/核心对应");
assert.equal(byPair.get("430602|080407")?.relation_level, "主映射/核心对应");
assert.equal(byPair.get("430603|080408")?.relation_level, "主映射/核心对应");
assert.equal(byPair.has("430608|080405"), false);
assert.equal(byPair.get("440107|080906")?.relation_level, "主映射/核心对应");
assert.equal(byPair.has("440703|120216T"), false);
assert.equal(byPair.get("460405|081806T")?.relation_level, "主映射/核心对应");
assert.equal(byPair.has("480402|130513TK"), false);
assert.equal(byPair.has("490205|100805T"), false);
assert.equal(byPair.get("490205|090402")?.relation_level, "主映射/核心对应");
assert.equal(byPair.get("520409K|100501K")?.relation_level, "强相关");
assert.equal(byPair.get("520414|100802")?.relation_level, "主映射/核心对应");
assert.equal(byPair.get("550104|130504")?.relation_level, "主映射/核心对应");
assert.equal(byPair.has("550104|130510TK"), false);
assert.equal(byPair.get("550212|130215T")?.relation_level, "主映射/核心对应");
assert.equal(byPair.has("550212|130315TK"), false);
assert.equal(byPair.get("560203|080707T")?.relation_level, "主映射/核心对应");
assert.equal(byPair.get("570204|050209")?.relation_level, "主映射/核心对应");
assert.equal(byPair.has("570313|040210TK"), false);
assert.equal(byPair.get("580605K|071102")?.relation_level, "主映射/核心对应");
assert.equal(byPair.get("590202|120206")?.relation_level, "主映射/核心对应");

for (const rows of Map.groupBy(candidates, (row) => row.vocational_code).values()) {
  assert.ok(rows.filter((row) => row.is_primary).length <= 1);
}

for (const row of candidates.filter((candidate) => candidate.sensitive_restriction)) {
  assert.deepEqual(
    [row.relation_level, row.skills_behavior, row.is_primary, row.consumable],
    ["目录参考", "仅目录查看", false, false],
  );
}

const category4 = vocational.filter((row) => row.major_code.startsWith("4"));
assert.equal(category4.length, 381);
assert.equal(vocational.filter((row) => row.major_code.startsWith("5")).length, 430);
assert.equal(ledger.records.length, 811);
assert.equal(new Set(ledger.records.map((row) => row.vocational_code)).size, 811);
assert.equal(ledger.records.filter((row) => row.review_status === "尚未完成复核").length, 0);
assert.equal(
  ledger.records.filter(
    (row) => row.review_status === "存在歧义，建议学科专家复核",
  ).length,
  5,
);
for (const major of vocational) {
  const row = ledger.records.find(
    (record) => record.vocational_code === major.major_code,
  );
  assert.ok(row, `missing review ledger: ${major.major_code}`);
  assert.notEqual(row.review_status, "尚未完成复核");
  const all = candidates
    .filter((candidate) => candidate.vocational_code === major.major_code)
    .map((candidate) => candidate.mapping_id)
    .sort();
  validateReviewRow(row, all);
  assert.deepEqual(
    [...row.accepted_mapping_ids, ...row.rejected_mapping_ids].sort(),
    all,
  );
  assert.equal(
    new Set([...row.accepted_mapping_ids, ...row.rejected_mapping_ids]).size,
    all.length,
  );
}
const genericForeignLanguage = ledger.records.find(
  (row) => row.vocational_code === "570208",
);
assert.equal(genericForeignLanguage.zero_all, true);
assert.equal(genericForeignLanguage.review_status, "已确认无直接对应");

assert.equal(reverse.records.length, 883);
assert.deepEqual(
  new Set(reverse.records.map((row) => row.undergraduate_code)),
  new Set(undergraduate.map((row) => row.major_code)),
);
const reverseStates = new Set([
  "有核心高职专科对应",
  "仅有强相关或延伸高职专科对应",
  "无高职专科对应",
  "仅有敏感目录参考",
]);
const acceptedIds = new Set(ledger.records.flatMap((row) => row.accepted_mapping_ids));
for (const row of reverse.records) {
  assert.ok(reverseStates.has(row.coverage_state));
  assert.equal(typeof row.zero_accepted_consumable, "boolean");
  const grouped = Object.values(row.mapping_ids_by_level).flat();
  assert.equal(new Set(grouped).size, grouped.length);
  assert.ok(grouped.every((mappingId) => acceptedIds.has(mappingId)));
  assert.ok(
    grouped.every(
      (mappingId) =>
        candidates.find((candidate) => candidate.mapping_id === mappingId)
          ?.undergraduate_code === row.undergraduate_code,
    ),
  );
  const consumable = grouped
    .map((mappingId) => candidates.find((candidate) => candidate.mapping_id === mappingId))
    .filter((candidate) => candidate?.consumable);
  assert.equal(row.zero_accepted_consumable, consumable.length === 0);
}

console.log(`vocational mapping candidates: ${candidates.length} OK`);
