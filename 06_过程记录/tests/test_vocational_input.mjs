import assert from "node:assert/strict";
import fs from "node:fs/promises";

const payload = JSON.parse(
  await fs.readFile(
    "06_过程记录/vocational_undergraduate_mapping/catalogs/vocational_class_skills.json",
    "utf8",
  ),
);

assert.equal(payload.categories.length, 19);
assert.equal(payload.classes.length, 97);
assert.equal(new Set(payload.categories.map((row) => row.category_code)).size, 19);
assert.equal(new Set(payload.classes.map((row) => row.class_code)).size, 97);
assert.ok(payload.classes.every((row) => Array.isArray(row.skills_domains)));
assert.ok(payload.classes.every((row) => row.skills_domains.length > 0));
assert.ok(payload.classes.every((row) => row.source_sheet === "专业类-领域分类明细"));
assert.deepEqual(payload.source_ranges, {
  Skills领域分类总表: "A1:E61",
  "领域分类-专业反向索引": "A1:F15",
  "专业大类-领域分类矩阵": "A1:R20",
  "专业类-领域分类明细": "A1:F389",
});

console.log("vocational input classification: OK");
