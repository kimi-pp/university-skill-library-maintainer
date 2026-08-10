import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";


const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(scriptDir, "..");
const deliveryRoot = path.join(projectRoot, "05_交付物", "06_课程设计、教学材料与教学评估_全网公开技能调研");
const catalog = JSON.parse(await fs.readFile(path.join(scriptDir, "fd06_catalog.json"), "utf8"));
const manifest = JSON.parse(await fs.readFile(path.join(deliveryRoot, "MANIFEST.json"), "utf8"));
const formulaErrors = new Set(["#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A"]);
const expectedSheets = ["使用说明", "AI技能清单", "分类统计", "来源清单"];

assert.equal(manifest.length, 13, "应有 13 个 Excel 清单");

for (const item of manifest) {
  const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(item.path));
  const names = workbook.worksheets.items.map((sheet) => sheet.name);
  assert.deepEqual(names, expectedSheets, `${item.key}: 工作表名称或顺序不正确`);
  const skills = workbook.worksheets.getItem("AI技能清单");
  const stats = workbook.worksheets.getItem("分类统计");
  const sources = workbook.worksheets.getItem("来源清单");
  const expected = item.key === "00" ? catalog : catalog.filter((row) => row.primary_subcategory === item.key);
  const lastSkillRow = expected.length + 4;
  const ids = skills.getRange(`B5:B${lastSkillRow}`).values.flat().filter(Boolean);
  assert.deepEqual(ids, expected.map((row) => row.skill_id), `${item.key}: Skill ID 与正式目录不一致`);
  const grades = skills.getRange(`K5:K${lastSkillRow}`).values.flat().filter(Boolean);
  assert.equal(grades.some((grade) => grade === "SC" || grade === "SX"), false, `${item.key}: 出现禁入等级`);
  assert.match(stats.getRange("B4").formulas[0][0], /^=/, `${item.key}: 总数必须由公式生成`);
  assert.match(sources.getRange("F5").formulas[0][0], /^=/, `${item.key}: 来源数量必须由公式生成`);
  const checked = [
    ...skills.getRange(`A1:S${lastSkillRow}`).values.flat(),
    ...stats.getRange("A1:K30").values.flat(),
    ...sources.getRange("A1:H200").values.flat(),
  ];
  assert.equal(checked.some((value) => formulaErrors.has(value)), false, `${item.key}: 发现公式错误值`);
  console.log(`${item.key}: reopen OK; sheets=4; skills=${ids.length}; formulas OK`);
}
