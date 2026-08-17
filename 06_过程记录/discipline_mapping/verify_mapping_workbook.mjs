import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

import { OUTPUT_PATH, SHEET_NAMES } from "./build_mapping_workbook.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const defaultRenderDir = path.join(scriptDir, "renders");
const bundlePath = path.join(scriptDir, "artifacts", "mapping_bundle.json");
const formulaErrorTokens = new Set(["#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A"]);

const renderSpecs = [
  ["使用说明与版本", "A1:H14"],
  ["本科专业目录_2026", "A1:K24"],
  ["研究生学科目录", "A1:K24"],
  ["学科相关性映射主表", "A1:U18"],
  ["本科专业反向索引", "A1:W16"],
  ["研究生学科反向索引", "A1:R16"],
  ["规则与字段字典", "A1:D24"],
  ["来源台账", "A1:J7"],
  ["质量复核清单", "A1:H18"],
  ["统计总览", "A1:D25"],
];

function rows(sheet) {
  return sheet.getUsedRange().values.slice(4);
}

function sorted(values) {
  return [...values].sort((left, right) => String(left).localeCompare(String(right), "zh-CN"));
}

function assertExactMembers(actual, expected, message) {
  assert.deepEqual(sorted(actual), sorted(expected), message);
}

function scanFormulaErrors(workbook) {
  const findings = [];
  for (const sheet of workbook.worksheets.items) {
    const values = sheet.getUsedRange().values;
    for (let rowIndex = 0; rowIndex < values.length; rowIndex += 1) {
      for (let columnIndex = 0; columnIndex < values[rowIndex].length; columnIndex += 1) {
        const value = values[rowIndex][columnIndex];
        if (formulaErrorTokens.has(value)) {
          findings.push({ sheet: sheet.name, row: rowIndex + 1, column: columnIndex + 1, value });
        }
      }
    }
  }
  return findings;
}

async function renderPreviews(workbook, renderDir) {
  if (!renderDir) return [];
  await fs.mkdir(renderDir, { recursive: true });
  for (const name of await fs.readdir(renderDir)) {
    if (/^\d{2}_.+\.png$/u.test(name)) await fs.unlink(path.join(renderDir, name));
  }
  const paths = [];
  for (let index = 0; index < renderSpecs.length; index += 1) {
    const [sheetName, range] = renderSpecs[index];
    const preview = await workbook.render({ sheetName, range, scale: 1.15, format: "png" });
    const outputPath = path.join(renderDir, `${String(index + 1).padStart(2, "0")}_${sheetName}.png`);
    await fs.writeFile(outputPath, new Uint8Array(await preview.arrayBuffer()));
    paths.push(outputPath);
  }
  return paths;
}

export async function verifyWorkbookFile(filePath, bundle, options = {}) {
  const renderDir = options.renderDir === undefined ? defaultRenderDir : options.renderDir;
  const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(filePath));

  assert.deepEqual(
    workbook.worksheets.items.map((sheet) => sheet.name),
    SHEET_NAMES,
    "工作表名称或顺序不符合交付约定",
  );

  const undergraduateRows = rows(workbook.worksheets.getItem("本科专业目录_2026"));
  const graduateRows = rows(workbook.worksheets.getItem("研究生学科目录"));
  const mappingRows = rows(workbook.worksheets.getItem("学科相关性映射主表"));
  const undergraduateIndexRows = rows(workbook.worksheets.getItem("本科专业反向索引"));
  const graduateIndexRows = rows(workbook.worksheets.getItem("研究生学科反向索引"));
  const qaRows = rows(workbook.worksheets.getItem("质量复核清单"));

  assert.equal(undergraduateRows.length, bundle.undergraduate.length, "本科目录行数不一致");
  assert.equal(graduateRows.length, bundle.graduate.length, "研究生目录行数不一致");
  assert.equal(mappingRows.length, bundle.mappings.length, "映射主表行数不一致");
  assert.equal(undergraduateIndexRows.length, bundle.undergraduate_index.length, "本科反向索引行数不一致");
  assert.equal(graduateIndexRows.length, bundle.graduate_index.length, "研究生反向索引行数不一致");
  assert.equal(qaRows.length, bundle.qa_findings.length, "质量发现行数不一致");

  assertExactMembers(
    undergraduateRows.map((row) => String(row[4])),
    bundle.undergraduate.map((item) => item.major_code),
    "本科专业代码集合不一致",
  );
  assertExactMembers(
    graduateRows.map((row) => `${row[2]}|${row[3]}`),
    bundle.graduate.map((item) => `${item.object_type}|${item.object_code}`),
    "研究生对象键集合不一致",
  );
  assertExactMembers(
    mappingRows.map((row) => row[0]),
    bundle.mappings.map((item) => item.mapping_id),
    "映射 ID 集合不一致",
  );
  assertExactMembers(
    undergraduateIndexRows.map((row) => String(row[0])),
    bundle.undergraduate_index.map((item) => item.undergraduate_code),
    "本科反向索引代码集合不一致",
  );
  assertExactMembers(
    graduateIndexRows.map((row) => `${row[0]}|${row[1]}`),
    bundle.graduate_index.map((item) => `${item.graduate_type}|${item.graduate_code}`),
    "研究生反向索引对象键集合不一致",
  );

  const militaryRows = mappingRows.filter((row) => row[17] === "是");
  assert.equal(militaryRows.length, bundle.summary.military_mapping_count, "军事目录参考关系数量不一致");
  for (const row of militaryRows) {
    assert.equal(row[12], "目录参考", `${row[0]} 的军事关系等级不合规`);
    assert.equal(row[13], "否", `${row[0]} 不得为主映射`);
    assert.equal(row[16], "仅目录查看", `${row[0]} 不得进入 Skills 消费`);
  }

  const undergraduateZeroCodes = undergraduateIndexRows
    .filter((row) => row[20] === "无合适研究生直接对应")
    .map((row) => String(row[0]));
  assertExactMembers(
    undergraduateZeroCodes,
    bundle.undergraduate_index
      .filter((item) => item.zero_mapping_state === "无合适研究生直接对应")
      .map((item) => item.undergraduate_code),
    "本科零映射记录不一致",
  );
  const graduateZeroKeys = graduateIndexRows
    .filter((row) => row[5] === "已确认无直接对应本科专业")
    .map((row) => `${row[0]}|${row[1]}`);
  assertExactMembers(
    graduateZeroKeys,
    bundle.graduate_index
      .filter((item) => item.reverse_state === "已确认无直接对应本科专业")
      .map((item) => `${item.graduate_type}|${item.graduate_code}`),
    "研究生零映射记录不一致",
  );

  const summarySheet = workbook.worksheets.getItem("统计总览");
  const summaryFormulas = summarySheet.getRange("B5:B25").formulas.flat();
  assert.equal(summaryFormulas.every((formula) => typeof formula === "string" && formula.startsWith("=")), true, "统计总览必须使用公式");
  assert.equal(summaryFormulas.every((formula) => /'[^']+'!/u.test(formula)), true, "跨表公式必须显式引用带引号的工作表名");
  assert.equal(summaryFormulas.some((formula) => /\$[A-Z]+:\$[A-Z]+/u.test(formula)), false, "统计公式不得使用整列引用");

  const formulaErrors = scanFormulaErrors(workbook);
  assert.equal(formulaErrors.length, 0, `工作簿存在公式错误：${JSON.stringify(formulaErrors.slice(0, 5))}`);

  const [summaryInspection, mappingInspection] = await Promise.all([
    workbook.inspect({ kind: "region,formula", sheetId: "统计总览", range: "A1:D25", maxChars: 6000, options: { maxResults: 100 } }),
    workbook.inspect({ kind: "region", sheetId: "学科相关性映射主表", range: "A1:U12", maxChars: 6000 }),
  ]);
  const renderPaths = await renderPreviews(workbook, renderDir);

  return {
    sheetCount: workbook.worksheets.items.length,
    undergraduateCount: undergraduateRows.length,
    graduateCount: graduateRows.length,
    mappingCount: mappingRows.length,
    undergraduateZeroCount: undergraduateZeroCodes.length,
    graduateZeroCount: graduateZeroKeys.length,
    militaryMappingCount: militaryRows.length,
    qaFindingCount: qaRows.length,
    formulaErrorCount: formulaErrors.length,
    inspectionChars: (summaryInspection.ndjson?.length ?? 0) + (mappingInspection.ndjson?.length ?? 0),
    renderPaths,
  };
}

async function main() {
  const bundle = JSON.parse(await fs.readFile(bundlePath, "utf8"));
  const report = await verifyWorkbookFile(OUTPUT_PATH, bundle);
  console.log(JSON.stringify(report));
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url))) {
  await main();
}
