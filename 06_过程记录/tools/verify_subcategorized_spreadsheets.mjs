import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
import {
  CATALOG_HEADERS,
  PROJECT_ROOT,
  SHEET_NAMES,
  loadInputs,
  selectManifestItems,
} from "./build_subcategorized_spreadsheets.mjs";
import { unzipEntries } from "./xlsx_package_utils.mjs";

const FORMULA_ERROR = /#REF!|#DIV\/0!|#VALUE!|#NAME\?|#N\/A/;

function xmlDecode(value) {
  return value
    .replaceAll("&quot;", '"')
    .replaceAll("&apos;", "'")
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&amp;", "&");
}

function requireEntry(entries, name) {
  const value = entries.get(name);
  if (!value) throw new Error(`XLSX 缺少结构文件: ${name}`);
  return value.toString("utf8");
}

export async function inspectXlsxPackage(filePath) {
  const entries = unzipEntries(await fs.readFile(filePath));
  const workbookXml = requireEntry(entries, "xl/workbook.xml");
  const relationshipsXml = requireEntry(entries, "xl/_rels/workbook.xml.rels");
  const relationships = new Map(
    [...relationshipsXml.matchAll(/<(?:\w+:)?Relationship\b[^>]*\/?\s*>/g)].map((match) => {
      const attributes = Object.fromEntries([...match[0].matchAll(/([\w:]+)="([^"]*)"/g)].map((item) => [item[1], item[2]]));
      return [attributes.Id, attributes.Target];
    }),
  );
  const sheetDescriptors = [...workbookXml.matchAll(/<(?:\w+:)?sheet\b[^>]*\/?\s*>/g)].map((match) => {
    const attributes = Object.fromEntries([...match[0].matchAll(/([\w:]+)="([^"]*)"/g)].map((item) => [item[1], item[2]]));
    return { name: xmlDecode(attributes.name), relationshipId: attributes["r:id"] };
  });
  const sheetXml = new Map();
  for (const descriptor of sheetDescriptors) {
    const target = relationships.get(descriptor.relationshipId);
    if (!target) throw new Error(`工作表关系不存在: ${descriptor.name}`);
    const normalized = target.startsWith("/")
      ? target.slice(1)
      : path.posix.normalize(path.posix.join("xl", target));
    sheetXml.set(descriptor.name, requireEntry(entries, normalized));
  }
  const tableXml = [...entries.entries()]
    .filter(([name]) => /^xl\/tables\/table\d+\.xml$/.test(name))
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([, value]) => value.toString("utf8"));
  return {
    sheetNames: sheetDescriptors.map((descriptor) => descriptor.name),
    sheetXml,
    stylesXml: requireEntry(entries, "xl/styles.xml"),
    tableXml,
    entries,
  };
}

function expectedRecordsFor(item, records) {
  return [...records]
    .filter((record) => item.scope === "overview"
      ? record.cat === item.big_category_code
      : record.subcategory_code === item.subcategory_code)
    .sort((left, right) => left.id.localeCompare(right.id));
}

function usedValues(sheet) {
  const used = sheet.getUsedRange(true);
  return used ? used.values.flat() : [];
}

function usedFormulas(sheet) {
  const used = sheet.getUsedRange();
  return used ? used.formulas.flat().filter(Boolean) : [];
}

function formulaErrors(workbook) {
  const errors = [];
  for (const sheet of workbook.worksheets.items) {
    for (const value of usedValues(sheet)) {
      if (typeof value === "string" && FORMULA_ERROR.test(value)) errors.push(`${sheet.name}: ${value}`);
    }
  }
  return errors;
}

function assertPackageLayout(packageInfo, lastCatalogRow, item) {
  assert.deepEqual(packageInfo.sheetNames, SHEET_NAMES, `${item.key}: 工作表名称/顺序错误`);
  assert.match(packageInfo.stylesXml, /FF16324F/i, `${item.key}: 缺少深蓝标题样式`);
  assert.match(packageInfo.stylesXml, /FF1F7A8C/i, `${item.key}: 缺少蓝绿色表头样式`);
  for (const [sheetName, xml] of packageInfo.sheetXml) {
    assert.match(xml, /<(?:\w+:)?sheetView\b[^>]*showGridLines="0"/, `${item.key}/${sheetName}: 未隐藏网格线`);
  }
  const catalogXml = packageInfo.sheetXml.get("AI技能清单");
  assert.match(catalogXml, /<(?:\w+:)?pane\b(?=[^>]*xSplit="4")(?=[^>]*ySplit="4")[^>]*>/, `${item.key}: AI技能清单冻结位置错误`);
  assert.match(catalogXml, /<(?:\w+:)?cols>.*?<(?:\w+:)?col\b[^>]*min="1"[^>]*max="1"[^>]*width="[6-9](?:\.\d+)?"/s, `${item.key}: 列宽未写入`);
  assert.match(catalogXml, /<(?:\w+:)?row\b[^>]*r="1"[^>]*ht="(?:3[6-9]|4\d)(?:\.\d+)?"[^>]*customHeight="1"/, `${item.key}: 标题行高错误`);
  assert.match(catalogXml, /<(?:\w+:)?row\b[^>]*r="5"[^>]*ht="(?:[7-9]\d|1\d{2})(?:\.\d+)?"[^>]*customHeight="1"/, `${item.key}: 数据行高错误`);
  const aStyle = catalogXml.match(/<(?:\w+:)?c\b(?=[^>]*r="A5")(?=[^>]*s="(\d+)")[^>]*>/)?.[1];
  const mStyle = catalogXml.match(/<(?:\w+:)?c\b(?=[^>]*r="M5")(?=[^>]*s="(\d+)")[^>]*>/)?.[1];
  assert.ok(aStyle && mStyle && aStyle !== mStyle, `${item.key}: 用户区和追溯区样式未区分`);
  const conditionalRanges = [...catalogXml.matchAll(/<(?:\w+:)?conditionalFormatting\b[^>]*sqref="([^"]+)"/g)].map((match) => match[1]).sort();
  assert.deepEqual(conditionalRanges, [`I5:I${lastCatalogRow}`, `J5:J${lastCatalogRow}`], `${item.key}: 条件格式只能用于推荐程度和接入难度`);
  assert.ok(packageInfo.tableXml.some((xml) => new RegExp(`<(?:\\w+:)?autoFilter\\b[^>]*ref="A4:V${lastCatalogRow}"`).test(xml)), `${item.key}: AI技能清单筛选区域错误`);
}

export async function verifySpreadsheetFile(filePath, item, records, taxonomy) {
  const expectedRecords = expectedRecordsFor(item, records);
  if (!expectedRecords.length) throw new Error(`${item.key}: Skill ID 成员不一致，期望集合为空`);
  for (const record of expectedRecords) {
    const category = taxonomy.find((candidate) => candidate.code === record.subcategory_code);
    if (!category || category.name !== record.subcategory_name) throw new Error(`${item.key}: 小分类成员不一致 ${record.id}`);
  }
  let workbook;
  try {
    workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(filePath));
  } catch (error) {
    throw new Error(`${item.key}: XLSX 无法重新打开: ${error.message}`);
  }
  assert.deepEqual(workbook.worksheets.items.map((sheet) => sheet.name), SHEET_NAMES, `${item.key}: 缺少或多出工作表`);
  const catalog = workbook.worksheets.getItem("AI技能清单");
  const lastRow = expectedRecords.length + 4;
  assert.deepEqual(catalog.getRange("A4:V4").values[0], CATALOG_HEADERS, `${item.key}: 清单列顺序错误`);
  assert.deepEqual(catalog.getRange(`N5:N${lastRow}`).values.flat(), expectedRecords.map((record) => record.id), `${item.key}: Skill ID 顺序或成员不一致`);
  assert.deepEqual(catalog.getRange(`C5:C${lastRow}`).values.flat(), expectedRecords.map((record) => record.cn), `${item.key}: 中文名称事实漂移`);
  assert.deepEqual(catalog.getRange(`M5:M${lastRow}`).values.flat(), expectedRecords.map((record) => record.name), `${item.key}: 英文名称事实漂移`);
  assert.deepEqual(catalog.getRange(`R5:R${lastRow}`).values.flat(), expectedRecords.map((record) => record.license), `${item.key}: 许可证事实漂移`);
  for (const [column, field] of [["U", "skill_url"], ["V", "repo_url"]]) {
    const values = catalog.getRange(`${column}5:${column}${lastRow}`).values.flat();
    assert.deepEqual(values, expectedRecords.map((record) => record[field]), `${item.key}: ${column} URL 事实漂移`);
  }

  const stats = workbook.worksheets.getItem("分类统计");
  const statsFormulas = usedFormulas(stats);
  assert.ok(statsFormulas.length >= 4 && statsFormulas.every((formula) => formula.includes("'AI技能清单'!")), `${item.key}: 分类统计不是清单驱动公式`);
  const statsTotal = stats.getRange("B3");
  assert.match(statsTotal.formulas[0][0], /^=/, `${item.key}: 统计总数应为公式`);
  assert.equal(statsTotal.values[0][0], expectedRecords.length, `${item.key}: 统计总数错误`);

  const sources = workbook.worksheets.getItem("来源清单");
  const sourceFormulas = usedFormulas(sources).filter((formula) => formula.startsWith("=COUNTIF"));
  assert.ok(sourceFormulas.length >= 1 && sourceFormulas.every((formula) => formula.startsWith("=COUNTIF('AI技能清单'!")), `${item.key}: 来源数量不是公式`);
  const sourceTotal = sourceFormulas.reduce((total, formula) => {
    const cellMatch = formula.match(/,B(\d+)\)$/);
    if (!cellMatch) return total;
    const row = Number(cellMatch[1]);
    return total + Number(sources.getRange(`G${row}`).values[0][0]);
  }, 0);
  assert.equal(sourceTotal, expectedRecords.length, `${item.key}: 来源数量合计错误`);

  const errors = formulaErrors(workbook);
  assert.deepEqual(errors, [], `${item.key}: 发现公式错误值 ${errors.join("; ")}`);
  const packageInfo = await inspectXlsxPackage(filePath);
  assertPackageLayout(packageInfo, lastRow, item);
  const catalogXml = packageInfo.sheetXml.get("AI技能清单");
  const hyperlinkRefs = [...catalogXml.matchAll(/<(?:\w+:)?hyperlink\b[^>]*ref="([UV]\d+)"[^>]*\br:id="([^"]+)"/g)].map((match) => match[1]);
  assert.equal(hyperlinkRefs.length, expectedRecords.length * 2, `${item.key}: Skill/仓库真实超链接数量错误`);
  const catalogRels = packageInfo.entries.get("xl/worksheets/_rels/sheet2.xml.rels")?.toString("utf8") ?? "";
  for (const record of expectedRecords) {
    assert.ok(catalogRels.includes(`Target="${record.skill_url.replaceAll("&", "&amp;")}"`), `${item.key}: Skill 超链接目标错误 ${record.id}`);
    assert.ok(catalogRels.includes(`Target="${record.repo_url.replaceAll("&", "&amp;")}"`), `${item.key}: 仓库超链接目标错误 ${record.id}`);
  }
  return { key: item.key, skillCount: expectedRecords.length, sheetCount: SHEET_NAMES.length };
}

export async function verifySelectedSpreadsheets(records, taxonomy, manifest, projectRoot, { only = null } = {}) {
  const results = [];
  for (const item of selectManifestItems(manifest, only)) {
    const filePath = path.resolve(projectRoot, ...item.path.split("/"));
    try {
      const stat = await fs.stat(filePath);
      if (!stat.isFile() || stat.size === 0) throw new Error("文件为空");
    } catch (error) {
      if (error.code === "ENOENT") throw new Error(`${item.key}: XLSX 不存在: ${filePath}`);
      throw error;
    }
    results.push(await verifySpreadsheetFile(filePath, item, records, taxonomy));
  }
  return results;
}

function parseOnly(argv) {
  const index = argv.indexOf("--only");
  if (index < 0) return null;
  const values = [];
  for (let cursor = index + 1; cursor < argv.length && !argv[cursor].startsWith("--"); cursor += 1) {
    values.push(...argv[cursor].split(",").map((value) => value.trim()).filter(Boolean));
  }
  return values;
}

export async function main(argv = process.argv.slice(2)) {
  const inputs = await loadInputs(PROJECT_ROOT);
  const results = await verifySelectedSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, PROJECT_ROOT, { only: parseOnly(argv) });
  console.log(`xlsx=${results.length} sheets=${results.reduce((sum, result) => sum + result.sheetCount, 0)} formulas=OK structure=OK`);
  return 0;
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) {
  main().catch((error) => {
    console.error(`XLSX 验证失败: ${error.message}`);
    process.exitCode = 1;
  });
}
