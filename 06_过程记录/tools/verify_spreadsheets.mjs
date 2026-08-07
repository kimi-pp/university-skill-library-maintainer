import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";


const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(scriptDir, "..", "..");
const dataDir = path.join(projectRoot, "03_候选池", "deduplicated");
const outputDir = process.env.SKILL_RESEARCH_OUTPUT_DIR || path.join(projectRoot, "05_交付物");
const manifest = JSON.parse(await fs.readFile(path.join(dataDir, "manifest.json"), "utf8"));
const formulaErrors = new Set(["#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A"]);
const requestedCategories = process.argv.slice(2);
const knownCategories = [...new Set(manifest.map((item) => item.category))];
const verifyCategories = requestedCategories.length ? requestedCategories : knownCategories;
const invalidCategories = verifyCategories.filter((category) => !knownCategories.includes(category));
if (invalidCategories.length) {
  throw new Error(`未知分类：${invalidCategories.join(", ")}`);
}

for (const category of verifyCategories) {
  const payload = JSON.parse(await fs.readFile(path.join(dataDir, `category_${category}.json`), "utf8"));
  const expectedIds = payload.records.map((row) => row.id);
  const item = manifest.find((entry) => entry.category === category && entry.format === "xlsx");
  const filePath = path.join(outputDir, item.path);
  const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(filePath));

  const guide = workbook.worksheets.getItem("使用说明");
  const catalog = workbook.worksheets.getItem("Skill总表");
  const stats = workbook.worksheets.getItem("分类统计");
  const sources = workbook.worksheets.getItem("来源清单");
  assert.ok(guide && catalog && stats && sources, `${category}: 缺少规定工作表`);

  const lastRow = expectedIds.length + 4;
  const actualIds = catalog.getRange(`B5:B${lastRow}`).values.flat();
  assert.deepEqual(actualIds, expectedIds, `${category}: Skill ID 与规范数据不一致`);
  assert.equal(stats.getRange("B4").values[0][0], expectedIds.length, `${category}: 统计总数错误`);
  assert.match(stats.getRange("B4").formulas[0][0], /^=/, `${category}: 统计应由公式生成`);
  assert.match(sources.getRange("F5").formulas[0][0], /^=/, `${category}: 来源计数应由公式生成`);

  const checked = [
    ...catalog.getRange(`A1:V${lastRow}`).values.flat(),
    ...stats.getRange("A1:J30").values.flat(),
    ...sources.getUsedRange().values.flat(),
  ];
  assert.equal(checked.some((value) => formulaErrors.has(value)), false, `${category}: 发现公式错误值`);
  console.log(`${category}: workbook reopen OK; sheets=4; skill_ids=${actualIds.length}; formulas OK`);
}
