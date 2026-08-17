import assert from "node:assert/strict";

import bundle from "../discipline_mapping/artifacts/mapping_bundle.json" with { type: "json" };
import sources from "../discipline_mapping/source_manifest.json" with { type: "json" };
import policy from "../discipline_mapping/rules/mapping_policy.json" with { type: "json" };
import { buildWorkbook } from "../discipline_mapping/build_mapping_workbook.mjs";

const expectedSheets = [
  "使用说明与版本",
  "本科专业目录_2026",
  "研究生学科目录",
  "学科相关性映射主表",
  "本科专业反向索引",
  "研究生学科反向索引",
  "规则与字段字典",
  "来源台账",
  "质量复核清单",
  "统计总览",
];

const workbook = await buildWorkbook(bundle, sources, policy);

assert.deepEqual(
  workbook.worksheets.items.map((sheet) => sheet.name),
  expectedSheets,
  "工作簿应按约定顺序包含十个工作表",
);
assert.equal(
  workbook.worksheets.getItem("本科专业目录_2026").getUsedRange().values.length - 4,
  883,
  "本科目录应完整保留 883 个专业",
);
assert.match(
  workbook.worksheets.getItem("统计总览").getRange("B5").formulas[0][0],
  /^=/,
  "统计总览核心指标应由公式计算",
);

console.log("discipline mapping workbook structure: OK");
