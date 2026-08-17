import assert from "node:assert/strict";

import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

import bundle from "../discipline_mapping/artifacts/mapping_bundle.json" with { type: "json" };
import sources from "../discipline_mapping/source_manifest.json" with { type: "json" };
import policy from "../discipline_mapping/rules/mapping_policy.json" with { type: "json" };
import { buildWorkbook, OUTPUT_PATH } from "../discipline_mapping/build_mapping_workbook.mjs";
import { verifyWorkbookFile } from "../discipline_mapping/verify_mapping_workbook.mjs";

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
assert.equal(
  workbook.worksheets.getItem("本科专业目录_2026").getRange("E5").format.numberFormat,
  "@",
  "本科专业代码应按文本格式保存",
);
assert.equal(
  workbook.worksheets.getItem("使用说明与版本").getRange("B14").format.numberFormat,
  "yyyy-mm-dd",
  "生成日期不应显示为 Excel 序列号",
);
assert.equal(
  workbook.worksheets.getItem("本科专业反向索引").getRange("I5").format.numberFormat,
  "yyyy-mm-dd",
  "本科复核日期不应显示为 Excel 序列号",
);
assert.equal(
  workbook.worksheets.getItem("研究生学科反向索引").getRange("H5").format.numberFormat,
  "yyyy-mm-dd",
  "研究生复核日期不应显示为 Excel 序列号",
);

const imported = await SpreadsheetFile.importXlsx(await FileBlob.load(OUTPUT_PATH));
assert.equal(
  imported.worksheets.getItem("本科专业目录_2026").getUsedRange().values.length - 4,
  883,
  "导出的工作簿应完整保留 883 个本科专业",
);
assert.equal(
  imported.worksheets.getItem("本科专业反向索引").getUsedRange().values.length - 4,
  883,
  "导出的本科反向索引应一专业一行",
);
for (const sheetName of expectedSheets) {
  const values = imported.worksheets.getItem(sheetName).getUsedRange().values.flat();
  assert.equal(
    values.some((value) => ["#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A"].includes(value)),
    false,
    `${sheetName} 不应包含公式错误`,
  );
}

const verification = await verifyWorkbookFile(OUTPUT_PATH, bundle, { renderDir: null });
assert.equal(verification.sheetCount, 10);
assert.equal(verification.mappingCount, 1915);
assert.equal(verification.formulaErrorCount, 0);

console.log("discipline mapping workbook structure: OK");
