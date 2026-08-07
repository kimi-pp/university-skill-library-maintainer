import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(scriptDir, "..", "..");
const data = JSON.parse(await fs.readFile(path.join(projectRoot, "03_候选池", "deduplicated", "0809_computer_science.json"), "utf8"));
const filePath = path.join(projectRoot, "05_交付物", "0809_计算机类_跨平台技能调研.xlsx");
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(filePath));
const expectedSheets = ["总览", "技能清单", "专业覆盖", "专业映射", "来源仓库", "规则与说明"];
for (const name of expectedSheets) assert.ok(workbook.worksheets.getItem(name), `缺少工作表：${name}`);

const catalog = workbook.worksheets.getItem("技能清单");
const coverage = workbook.worksheets.getItem("专业覆盖");
const mapping = workbook.worksheets.getItem("专业映射");
const overview = workbook.worksheets.getItem("总览");
const lastRow = data.records.length + 4;
const expectedIds = data.records.map((row) => row.id);
assert.deepEqual(catalog.getRange(`B5:B${lastRow}`).values.flat(), expectedIds, "Skill ID 与规范数据不一致");
assert.equal(overview.getRange("A5").values[0][0], 88, "总览总数错误");
assert.equal(overview.getRange("C5").values[0][0], 27, "SA 数量错误");
assert.equal(overview.getRange("E5").values[0][0], 35, "SB 数量错误");
assert.equal(overview.getRange("G5").values[0][0], 26, "SB-A 数量错误");
for (const cell of ["A5", "C5", "E5", "G5"]) assert.match(overview.getRange(cell).formulas[0][0], /^=/, `${cell} 应由公式生成`);
assert.deepEqual(coverage.getRange("H5:H18").values.flat(), Array(14).fill("已覆盖"), "14 个专业未全部覆盖");
assert.match(coverage.getRange("C5").formulas[0][0], /^=/, "专业覆盖数量应由公式生成");
assert.ok(mapping.getUsedRange().values.length > 200, "专业映射明细不足");

const errors = new Set(["#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A"]);
for (const name of expectedSheets) {
  const values = workbook.worksheets.getItem(name).getUsedRange().values.flat();
  assert.equal(values.some((value) => errors.has(value)), false, `${name} 发现公式错误值`);
}
console.log(`XLSX reopen OK; sheets=${expectedSheets.length}; skills=${expectedIds.length}; formulas/coverage OK`);
