import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

import bundle from "../vocational_undergraduate_mapping/artifacts/mapping_bundle.json" with { type: "json" };
import policy from "../vocational_undergraduate_mapping/rules/mapping_policy.json" with { type: "json" };
import qa from "../vocational_undergraduate_mapping/artifacts/qa_findings.json" with { type: "json" };
import summary from "../vocational_undergraduate_mapping/artifacts/summary.json" with { type: "json" };
import sources from "../vocational_undergraduate_mapping/source_manifest.json" with { type: "json" };
import {
  buildWorkbook,
  exportWorkbook,
  OUTPUT_PATH,
  SHEET_NAMES,
} from "../vocational_undergraduate_mapping/build_mapping_workbook.mjs";
import { verifyWorkbookFile } from "../vocational_undergraduate_mapping/verify_mapping_workbook.mjs";

const expected = [
  "使用说明与版本",
  "高职专科专业目录",
  "本科专业目录_2026",
  "高职本科相关性映射主表",
  "高职专业反向索引",
  "本科专业反向索引",
  "专业类映射汇总",
  "规则与字段字典",
  "来源台账",
  "质量复核清单",
  "统计总览",
];
assert.deepEqual(SHEET_NAMES, expected);

const workbook = buildWorkbook(bundle, qa, summary, policy, sources);
assert.deepEqual(workbook.worksheets.items.map((sheet) => sheet.name), expected);
assert.equal(
  workbook.worksheets.getItem("高职专科专业目录").getUsedRange().values.length - 4,
  811,
);
assert.equal(
  workbook.worksheets.getItem("本科专业目录_2026").getUsedRange().values.length - 4,
  883,
);
assert.equal(
  workbook.worksheets.getItem("高职专业反向索引").getUsedRange().values.length - 4,
  811,
);
assert.equal(
  workbook.worksheets.getItem("本科专业反向索引").getUsedRange().values.length - 4,
  883,
);
assert.equal(
  workbook.worksheets.getItem("专业类映射汇总").getUsedRange().values.length - 4,
  97,
);
assert.match(workbook.worksheets.getItem("统计总览").getRange("B5").formulas[0][0], /^=/);
assert.equal(
  workbook.worksheets.getItem("高职专科专业目录").getRange("E5").format.numberFormat,
  "@",
);

const imported = await SpreadsheetFile.importXlsx(await FileBlob.load(OUTPUT_PATH));
assert.deepEqual(imported.worksheets.items.map((sheet) => sheet.name), expected);
assert.equal(
  imported.worksheets.getItem("高职本科相关性映射主表").getUsedRange().values.length - 4,
  bundle.mappings.length,
);
assert.equal(
  String(imported.worksheets.getItem("本科专业目录_2026").getRange("E5").values[0][0]),
  "010101",
  "本科专业代码必须保留前导零",
);
assert.equal(
  String(imported.worksheets.getItem("本科专业反向索引").getRange("A5").values[0][0]),
  "010101",
  "本科反向索引代码必须保留前导零",
);
for (const name of expected) {
  const values = imported.worksheets.getItem(name).getUsedRange().values.flat();
  assert.equal(
    values.some((value) => ["#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A"].includes(value)),
    false,
    `${name} has formula errors`,
  );
}

const verification = await verifyWorkbookFile(OUTPUT_PATH, bundle, qa, {
  renderDir: null,
});
assert.equal(verification.sheetCount, 11);
assert.equal(verification.vocationalCount, 811);
assert.equal(verification.undergraduateCount, 883);
assert.equal(verification.mappingCount, bundle.mappings.length);
assert.equal(verification.classCount, 97);
assert.equal(verification.formulaErrorCount, 0);

const temporaryDirectory = await fs.mkdtemp(
  path.join(os.tmpdir(), "vocational-workbook-determinism-"),
);
try {
  const temporaryOutput = path.join(temporaryDirectory, "mapping.xlsx");
  await exportWorkbook(buildWorkbook(bundle, qa, summary, policy, sources), temporaryOutput);
  const firstHash = crypto
    .createHash("sha256")
    .update(await fs.readFile(temporaryOutput))
    .digest("hex");
  await exportWorkbook(buildWorkbook(bundle, qa, summary, policy, sources), temporaryOutput);
  const secondHash = crypto
    .createHash("sha256")
    .update(await fs.readFile(temporaryOutput))
    .digest("hex");
  assert.equal(secondHash, firstHash, "重复导出必须保持工作簿字节稳定");
} finally {
  await fs.rm(temporaryDirectory, { recursive: true, force: true });
}

console.log("vocational mapping workbook structure: OK");
