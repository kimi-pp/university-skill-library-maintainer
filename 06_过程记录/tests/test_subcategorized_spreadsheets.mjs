import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
import {
  CATALOG_HEADERS,
  SHEET_NAMES,
  generateSpreadsheets,
  loadInputs,
  selectManifestItems,
  validateInputContracts,
} from "../tools/build_subcategorized_spreadsheets.mjs";
import {
  inspectXlsxPackage,
  verifySpreadsheetFile,
} from "../tools/verify_subcategorized_spreadsheets.mjs";
import { renderSpreadsheetFile } from "../tools/render_subcategorized_spreadsheets.mjs";

const testDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(testDir, "..", "..");
const SAMPLE_KEYS = ["05-overview", "02-08", "01-01", "05-05"];

async function sha256(filePath) {
  return crypto.createHash("sha256").update(await fs.readFile(filePath)).digest("hex");
}

async function withTempDir(fn) {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), "subcategory-xlsx-"));
  try {
    return await fn(directory);
  } finally {
    await fs.rm(directory, { recursive: true, force: true });
  }
}

function xlsxPathFor(root, item) {
  return path.join(root, ...item.path.split("/"));
}

test("manifest selection is safe, unique, scope-aware, and stably ordered", async () => {
  const { manifest } = await loadInputs(projectRoot);
  const selected = selectManifestItems([...manifest].reverse(), ["05-05", "05-overview", "01-01"]);
  assert.deepEqual(selected.map((item) => item.key), ["01-01", "05-overview", "05-05"]);

  const duplicate = [...manifest, { ...manifest.find((item) => item.format === "xlsx" && item.subcategory_code === "05-05") }];
  assert.throws(() => selectManifestItems(duplicate), /重复.*manifest.*键/i);

  const unsafe = manifest.map((item) => ({ ...item }));
  const target = unsafe.find((item) => item.format === "xlsx" && item.scope === "overview");
  target.path = "../越界.xlsx";
  assert.throws(() => selectManifestItems(unsafe), /不安全.*路径/i);
  assert.throws(() => selectManifestItems(manifest, ["99-99"]), /未知.*only/i);
});

test("input validation rejects duplicate IDs and subcategory member drift", async () => {
  const { records, taxonomy, manifest } = await loadInputs(projectRoot);
  assert.doesNotThrow(() => validateInputContracts(records, taxonomy, manifest));
  assert.throws(
    () => validateInputContracts([...records, { ...records[0] }], taxonomy, manifest),
    /重复.*Skill ID/i,
  );
  const moved = records.map((record) => ({ ...record }));
  moved.find((record) => record.id === "GH-05-0003").subcategory_code = "05-01";
  assert.throws(() => validateInputContracts(moved, taxonomy, manifest), /成员.*错配|小分类.*不一致/i);
});

test("overview and contrasting subcategory samples reopen with exact values, formulas, and hyperlinks", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const written = await generateSpreadsheets(
      inputs.records,
      inputs.taxonomy,
      inputs.manifest,
      root,
      { only: SAMPLE_KEYS },
    );
    assert.equal(written.length, SAMPLE_KEYS.length);

    for (const { item, outputPath } of written) {
      const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(outputPath));
      assert.deepEqual(workbook.worksheets.items.map((sheet) => sheet.name), SHEET_NAMES);
      const expectedRecords = inputs.records
        .filter((record) => item.scope === "overview"
          ? record.cat === item.big_category_code
          : record.subcategory_code === item.subcategory_code)
        .sort((left, right) => left.id.localeCompare(right.id));
      const catalog = workbook.worksheets.getItem("AI技能清单");
      assert.deepEqual(catalog.getRange("A4:V4").values[0], CATALOG_HEADERS);
      assert.deepEqual(
        catalog.getRange(`N5:N${expectedRecords.length + 4}`).values.flat(),
        expectedRecords.map((record) => record.id),
      );
      assert.deepEqual(
        catalog.getRange(`C5:C${expectedRecords.length + 4}`).values.flat(),
        expectedRecords.map((record) => record.cn),
      );
      assert.deepEqual(catalog.getRange(`U5:U${expectedRecords.length + 4}`).values.flat(), expectedRecords.map((record) => record.skill_url));
      assert.deepEqual(catalog.getRange(`V5:V${expectedRecords.length + 4}`).values.flat(), expectedRecords.map((record) => record.repo_url));
      const packageInfo = await inspectXlsxPackage(outputPath);
      assert.doesNotMatch(packageInfo.sheetXml.get("使用说明"), /<(?:\w+:)?mergeCell\b[^>]*ref="A[12]:H[12]"/, `${item.key}: 使用说明不应保留空白尾列`);
      const catalogXml = packageInfo.sheetXml.get("AI技能清单");
      assert.equal([...catalogXml.matchAll(/<(?:\w+:)?hyperlink\b[^>]*ref="[UV]\d+"[^>]*\br:id="[^"]+"/g)].length, expectedRecords.length * 2);

      const stats = workbook.worksheets.getItem("分类统计");
      const statsFormulas = stats.getUsedRange().formulas.flat().filter(Boolean);
      assert.ok(statsFormulas.length >= 4, `${item.key}: 分类统计缺少公式`);
      assert.ok(statsFormulas.every((formula) => formula.includes("'AI技能清单'!")), `${item.key}: 跨表公式必须引用清单页`);
      const sources = workbook.worksheets.getItem("来源清单");
      const sourceFormulas = sources.getUsedRange().formulas.flat().filter(Boolean);
      assert.ok(sourceFormulas.length >= 1, `${item.key}: 来源清单计数必须是公式`);
      assert.ok(sourceFormulas.every((formula) => /^=COUNTIF\('AI技能清单'!/.test(formula)));
    }
  });
});

test("real XLSX package preserves title styling, user/trace grouping, freeze panes, filters, widths, heights, and limited conditional formatting", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [{ item, outputPath }] = await generateSpreadsheets(
      inputs.records,
      inputs.taxonomy,
      inputs.manifest,
      root,
      { only: ["05-05"] },
    );
    const packageInfo = await inspectXlsxPackage(outputPath);
    assert.deepEqual(packageInfo.sheetNames, SHEET_NAMES);
    assert.match(packageInfo.stylesXml, /FF16324F/i, `${item.key}: 标题深蓝色未写入样式表`);
    assert.match(packageInfo.stylesXml, /FF1F7A8C/i, `${item.key}: 表头蓝绿色未写入样式表`);

    const catalogXml = packageInfo.sheetXml.get("AI技能清单");
    assert.match(catalogXml, /<(?:\w+:)?pane\b[^>]*xSplit="4"[^>]*ySplit="4"|<(?:\w+:)?pane\b[^>]*ySplit="4"[^>]*xSplit="4"/);
    assert.match(catalogXml, /<(?:\w+:)?cols>.*?<(?:\w+:)?col\b[^>]*min="1"[^>]*max="1"[^>]*width="[6-9](?:\.\d+)?"/s);
    assert.match(catalogXml, /<(?:\w+:)?row\b[^>]*r="1"[^>]*ht="(?:3[6-9]|4\d)(?:\.\d+)?"[^>]*customHeight="1"/);
    assert.match(catalogXml, /<(?:\w+:)?row\b[^>]*r="5"[^>]*ht="(?:[7-9]\d|1\d{2})(?:\.\d+)?"[^>]*customHeight="1"/);
    const aStyle = catalogXml.match(/<(?:\w+:)?c\b[^>]*r="A5"[^>]*s="(\d+)"/)[1];
    const mStyle = catalogXml.match(/<(?:\w+:)?c\b[^>]*r="M5"[^>]*s="(\d+)"/)[1];
    assert.notEqual(aStyle, mStyle, "用户字段区和技术追溯区必须使用不同样式");
    const conditionalRanges = [...catalogXml.matchAll(/<(?:\w+:)?conditionalFormatting\b[^>]*sqref="([^"]+)"/g)].map((match) => match[1]);
    assert.deepEqual(conditionalRanges.sort(), ["I5:I9", "J5:J9"]);
    assert.ok(packageInfo.tableXml.some((xml) => /<(?:\w+:)?autoFilter\b[^>]*ref="A4:V9"/.test(xml)), "AI技能清单必须启用筛选");
    for (const xml of packageInfo.sheetXml.values()) assert.doesNotMatch(xml, /showGridLines="1"/);
  });
});

test("verifier checks a real XLSX and rejects expected-member mismatch", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [written] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, root, { only: ["02-08"] });
    const ok = await verifySpreadsheetFile(written.outputPath, written.item, inputs.records, inputs.taxonomy);
    assert.equal(ok.skillCount, 1);
    const missing = inputs.records.filter((record) => record.id !== "GH-02-0016");
    await assert.rejects(
      verifySpreadsheetFile(written.outputPath, written.item, missing, inputs.taxonomy),
      /成员.*不一致|Skill ID.*不一致/i,
    );
  });
});

test("generation is byte-idempotent despite reversed input ordering", async () => {
  await withTempDir(async (firstRoot) => withTempDir(async (secondRoot) => {
    const inputs = await loadInputs(projectRoot);
    const [first] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, firstRoot, { only: ["01-01"] });
    const [second] = await generateSpreadsheets(
      [...inputs.records].reverse(),
      [...inputs.taxonomy].reverse(),
      [...inputs.manifest].reverse(),
      secondRoot,
      { only: ["01-01"] },
    );
    assert.equal(await sha256(first.outputPath), await sha256(second.outputPath));
  }));
});

test("renderer reopens one XLSX and emits one nonblank PNG per worksheet", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [written] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, root, { only: ["02-08"] });
    const renderDir = path.join(root, "renders");
    const rendered = await renderSpreadsheetFile(written.outputPath, renderDir, written.item.key);
    assert.equal(rendered.length, 4);
    for (const renderedPath of rendered) {
      const bytes = await fs.readFile(renderedPath);
      assert.ok(bytes.length > 5000, `${renderedPath}: PNG 体积异常`);
      assert.deepEqual([...bytes.subarray(0, 8)], [137, 80, 78, 71, 13, 10, 26, 10]);
      assert.ok(bytes.readUInt32BE(16) >= 600, `${renderedPath}: PNG 宽度异常`);
      assert.ok(bytes.readUInt32BE(20) >= 180, `${renderedPath}: PNG 高度异常`);
    }
  });
});
