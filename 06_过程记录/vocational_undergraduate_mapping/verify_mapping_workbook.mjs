import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

import { OUTPUT_PATH, SHEET_NAMES } from "./build_mapping_workbook.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const defaultRenderDir = path.join(scriptDir, "renders");
const formulaErrorTokens = new Set(["#REF!", "#DIV/0!", "#VALUE!", "#NAME?", "#N/A"]);
const renderSpecs = [
  ["使用说明与版本", "A1:H15"],
  ["高职专科专业目录", "A1:K24"],
  ["本科专业目录_2026", "A1:J24"],
  ["高职本科相关性映射主表", "A1:X18"],
  ["高职专业反向索引", "A1:N18"],
  ["本科专业反向索引", "A1:O18"],
  ["专业类映射汇总", "A1:L24"],
  ["规则与字段字典", "A1:D28"],
  ["来源台账", "A1:J14"],
  ["质量复核清单", "A1:F19"],
  ["统计总览", "A1:D18"],
];

function rows(sheet) {
  return sheet.getUsedRange().values.slice(4);
}

function sorted(values) {
  return [...values].sort((left, right) =>
    String(left).localeCompare(String(right), "zh-CN"),
  );
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
          findings.push({
            sheet: sheet.name,
            row: rowIndex + 1,
            column: columnIndex + 1,
            value,
          });
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
    const preview = await workbook.render({
      sheetName,
      range,
      scale: 1.05,
      format: "png",
    });
    const outputPath = path.join(
      renderDir,
      `${String(index + 1).padStart(2, "0")}_${sheetName}.png`,
    );
    await fs.writeFile(outputPath, new Uint8Array(await preview.arrayBuffer()));
    paths.push(outputPath);
  }
  return paths;
}

export async function verifyWorkbookFile(filePath, bundle, qa, options = {}) {
  const renderDir = options.renderDir === undefined ? defaultRenderDir : options.renderDir;
  const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(filePath));
  assert.deepEqual(
    workbook.worksheets.items.map((sheet) => sheet.name),
    SHEET_NAMES,
    "工作表名称或顺序不符合交付约定",
  );

  const vocationalRows = rows(workbook.worksheets.getItem("高职专科专业目录"));
  const undergraduateRows = rows(workbook.worksheets.getItem("本科专业目录_2026"));
  const mappingRows = rows(workbook.worksheets.getItem("高职本科相关性映射主表"));
  const vocationalIndexRows = rows(workbook.worksheets.getItem("高职专业反向索引"));
  const undergraduateIndexRows = rows(workbook.worksheets.getItem("本科专业反向索引"));
  const classRows = rows(workbook.worksheets.getItem("专业类映射汇总"));
  const qaRows = rows(workbook.worksheets.getItem("质量复核清单"));

  assert.equal(vocationalRows.length, bundle.vocational_catalog.length, "高职目录行数不一致");
  assert.equal(undergraduateRows.length, bundle.undergraduate_catalog.length, "本科目录行数不一致");
  assert.equal(mappingRows.length, bundle.mappings.length, "映射主表行数不一致");
  assert.equal(vocationalIndexRows.length, bundle.vocational_index.length, "高职反向索引行数不一致");
  assert.equal(undergraduateIndexRows.length, bundle.undergraduate_index.length, "本科反向索引行数不一致");
  assert.equal(classRows.length, bundle.class_aggregation.length, "专业类汇总行数不一致");
  assert.equal(qaRows.length, qa.blocking.length + qa.review.length + qa.notice.length, "质量清单行数不一致");

  assertExactMembers(
    vocationalRows.map((row) => String(row[4])),
    bundle.vocational_catalog.map((row) => row.major_code),
    "高职专业代码集合不一致",
  );
  assertExactMembers(
    undergraduateRows.map((row) => String(row[4])),
    bundle.undergraduate_catalog.map((row) => row.major_code),
    "本科专业代码集合不一致",
  );
  assertExactMembers(
    mappingRows.map((row) => row[0]),
    bundle.mappings.map((row) => row.mapping_id),
    "映射ID集合不一致",
  );
  assertExactMembers(
    vocationalIndexRows.map((row) => String(row[0])),
    bundle.vocational_index.map((row) => row.vocational_code),
    "高职反向索引代码集合不一致",
  );
  assertExactMembers(
    undergraduateIndexRows.map((row) => String(row[0])),
    bundle.undergraduate_index.map((row) => row.undergraduate_code),
    "本科反向索引代码集合不一致",
  );
  assertExactMembers(
    classRows.map((row) => String(row[2])),
    bundle.class_aggregation.map((row) => row.class_code),
    "专业类代码集合不一致",
  );

  const restrictedRows = mappingRows.filter((row) => row[19] === "是");
  for (const row of restrictedRows) {
    assert.equal(row[13], "目录参考", `${row[0]} 的敏感关系等级不合规`);
    assert.equal(row[14], "否", `${row[0]} 不得为主映射`);
    assert.equal(row[17], "仅目录查看", `${row[0]} 不得进入 Skills 消费`);
    assert.equal(row[18], "否", `${row[0]} 必须不可消费`);
  }

  assertExactMembers(
    vocationalIndexRows.filter((row) => row[11] === "是").map((row) => String(row[0])),
    bundle.vocational_index.filter((row) => row.zero_all).map((row) => row.vocational_code),
    "高职零映射记录不一致",
  );
  assert.deepEqual(
    undergraduateIndexRows.map((row) => row[6]),
    bundle.undergraduate_index.map((row) => row.coverage_state),
    "本科覆盖状态不一致",
  );

  const summaryFormulas = workbook.worksheets
    .getItem("统计总览")
    .getRange("B5:B18")
    .formulas.flat();
  assert.equal(
    summaryFormulas.every((formula) => typeof formula === "string" && formula.startsWith("=")),
    true,
    "统计总览必须使用公式",
  );
  assert.equal(
    summaryFormulas.every((formula) => /'[^']+'!/u.test(formula)),
    true,
    "跨表公式必须显式引用工作表",
  );
  assert.equal(
    summaryFormulas.some((formula) => /\$[A-Z]+:\$[A-Z]+/u.test(formula)),
    false,
    "统计公式不得使用整列引用",
  );

  const formulaErrors = scanFormulaErrors(workbook);
  assert.equal(
    formulaErrors.length,
    0,
    `工作簿存在公式错误：${JSON.stringify(formulaErrors.slice(0, 5))}`,
  );
  const [summaryInspection, mappingInspection] = await Promise.all([
    workbook.inspect({
      kind: "region,formula",
      sheetId: "统计总览",
      range: "A1:D18",
      maxChars: 6000,
      options: { maxResults: 100 },
    }),
    workbook.inspect({
      kind: "region",
      sheetId: "高职本科相关性映射主表",
      range: "A1:X12",
      maxChars: 6000,
    }),
  ]);
  const renderPaths = await renderPreviews(workbook, renderDir);
  return {
    sheetCount: workbook.worksheets.items.length,
    vocationalCount: vocationalRows.length,
    undergraduateCount: undergraduateRows.length,
    mappingCount: mappingRows.length,
    vocationalIndexCount: vocationalIndexRows.length,
    undergraduateIndexCount: undergraduateIndexRows.length,
    classCount: classRows.length,
    qaFindingCount: qaRows.length,
    restrictedMappingCount: restrictedRows.length,
    formulaErrorCount: formulaErrors.length,
    inspectionChars:
      (summaryInspection.ndjson?.length ?? 0) +
      (mappingInspection.ndjson?.length ?? 0),
    renderPaths,
  };
}

async function main() {
  const [bundle, qa] = await Promise.all([
    fs.readFile(path.join(artifactDir(), "mapping_bundle.json"), "utf8").then(JSON.parse),
    fs.readFile(path.join(artifactDir(), "qa_findings.json"), "utf8").then(JSON.parse),
  ]);
  const report = await verifyWorkbookFile(OUTPUT_PATH, bundle, qa);
  console.log(JSON.stringify(report));
}

function artifactDir() {
  return path.join(scriptDir, "artifacts");
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url))) {
  await main();
}
