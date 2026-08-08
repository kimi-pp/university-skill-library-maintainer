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
const DIFFICULTY = {
  A: "A｜调整少",
  B: "B｜少量调整",
  C: "C｜较多调整",
  D: "D｜仅参考",
};

function parseAttributes(element) {
  return Object.fromEntries([...element.matchAll(/([\w:]+)="([^"]*)"/g)].map((match) => [match[1], xmlDecode(match[2])]));
}

function relationshipPathFor(sourcePath) {
  return sourcePath.replace(/^(.*)\/([^/]+)$/, "$1/_rels/$2.rels");
}

function resolveTarget(sourcePath, target) {
  return target.startsWith("/")
    ? target.slice(1)
    : path.posix.normalize(path.posix.join(path.posix.dirname(sourcePath), target));
}

function relationshipsFor(packageInfo, sourcePath) {
  const xml = packageInfo.entries.get(relationshipPathFor(sourcePath))?.toString("utf8") ?? "";
  return [...xml.matchAll(/<(?:\w+:)?Relationship\b[^>]*\/?\s*>/g)].map((match) => parseAttributes(match[0]));
}

function normalizeCellValue(value, columnIndex) {
  if (columnIndex === 19) {
    if (value instanceof Date) return value.toISOString().slice(0, 10);
    if (typeof value === "number") {
      const milliseconds = Math.round((value - 25569) * 86400 * 1000);
      return new Date(milliseconds).toISOString().slice(0, 10);
    }
  }
  return value;
}

function expectedCatalogRows(records) {
  return records.map((record, index) => [
    index + 1,
    `${record.subcategory_code} ${record.subcategory_name}`,
    record.cn,
    record.plain_purpose,
    record.plain_audience,
    record.plain_when_to_use,
    record.plain_prerequisites,
    record.plain_limitations,
    record.priority,
    DIFFICULTY[record.compat] ?? record.compat,
    record.plain_integration,
    record.plain_verification,
    record.name,
    record.id,
    record.tags,
    record.ecosystem,
    record.form,
    record.license,
    Number(record.stars),
    record.repo_pushed,
    record.skill_url,
    record.repo_url,
  ]);
}

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
  const sheetPaths = new Map();
  for (const descriptor of sheetDescriptors) {
    const target = relationships.get(descriptor.relationshipId);
    if (!target) throw new Error(`工作表关系不存在: ${descriptor.name}`);
    const normalized = target.startsWith("/")
      ? target.slice(1)
      : path.posix.normalize(path.posix.join("xl", target));
    sheetXml.set(descriptor.name, requireEntry(entries, normalized));
    sheetPaths.set(descriptor.name, normalized);
  }
  const tableXmlByPath = new Map([...entries.entries()]
    .filter(([name]) => /^xl\/tables\/table\d+\.xml$/.test(name))
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([name, value]) => [name, value.toString("utf8")]));
  return {
    sheetNames: sheetDescriptors.map((descriptor) => descriptor.name),
    sheetXml,
    sheetPaths,
    stylesXml: requireEntry(entries, "xl/styles.xml"),
    tableXml: [...tableXmlByPath.values()],
    tableXmlByPath,
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

function assertFreezePane(packageInfo, item, sheetName, expected) {
  const xml = packageInfo.sheetXml.get(sheetName);
  const pane = xml.match(/<(?:\w+:)?pane\b[^>]*\/?\s*>/)?.[0];
  assert.ok(pane, `${item.key}/${sheetName}: 冻结位置缺失`);
  const actual = parseAttributes(pane);
  const selected = {
    xSplit: actual.xSplit ?? null,
    ySplit: actual.ySplit ?? null,
    topLeftCell: actual.topLeftCell,
    activePane: actual.activePane,
    state: actual.state,
  };
  assert.deepEqual(selected, { xSplit: null, ySplit: null, ...expected, state: "frozen" }, `${item.key}/${sheetName}: 冻结位置错误`);
}

function assertTableFilter(packageInfo, item, sheetName, expectedRange) {
  const sheetPath = packageInfo.sheetPaths.get(sheetName);
  const xml = packageInfo.sheetXml.get(sheetName);
  const tableIds = [...xml.matchAll(/<(?:\w+:)?tablePart\b[^>]*\br:id="([^"]+)"/g)].map((match) => match[1]);
  assert.equal(tableIds.length, 1, `${item.key}/${sheetName}: 筛选表数量错误`);
  const relationships = new Map(relationshipsFor(packageInfo, sheetPath).map((relationship) => [relationship.Id, relationship]));
  const relationship = relationships.get(tableIds[0]);
  assert.ok(relationship?.Type?.endsWith("/table"), `${item.key}/${sheetName}: 筛选表关系错误`);
  const tablePath = resolveTarget(sheetPath, relationship.Target);
  const tableXml = packageInfo.tableXmlByPath.get(tablePath);
  assert.ok(tableXml, `${item.key}/${sheetName}: 筛选表文件缺失`);
  assert.match(tableXml, new RegExp(`<(?:\\w+:)?table\\b[^>]*\\bref="${expectedRange}"`), `${item.key}/${sheetName}: 筛选区域错误`);
  assert.match(tableXml, new RegExp(`<(?:\\w+:)?autoFilter\\b[^>]*\\bref="${expectedRange}"`), `${item.key}/${sheetName}: 筛选区域错误`);
}

function assertHyperlinkPlan(packageInfo, item, sheetName, expectedLinks) {
  const sheetPath = packageInfo.sheetPaths.get(sheetName);
  const xml = packageInfo.sheetXml.get(sheetName);
  const nodes = [...xml.matchAll(/<(?:\w+:)?hyperlink\b[^>]*\/?\s*>/g)].map((match) => parseAttributes(match[0]));
  assert.equal(nodes.length, expectedLinks.length, `${item.key}/${sheetName}: 链接数量错误`);
  assert.equal(new Set(nodes.map((node) => node.ref)).size, nodes.length, `${item.key}/${sheetName}: 链接单元格重复`);
  assert.equal(new Set(nodes.map((node) => node["r:id"])).size, nodes.length, `${item.key}/${sheetName}: 链接关系重复`);
  const relationships = relationshipsFor(packageInfo, sheetPath);
  const hyperlinkRelationships = relationships.filter((relationship) => relationship.Type?.endsWith("/hyperlink"));
  assert.equal(hyperlinkRelationships.length, expectedLinks.length, `${item.key}/${sheetName}: 存在孤儿或重复链接关系`);
  const byId = new Map(hyperlinkRelationships.map((relationship) => [relationship.Id, relationship]));
  for (const expected of expectedLinks) {
    const node = nodes.find((candidate) => candidate.ref === expected.ref);
    assert.ok(node, `${item.key}/${sheetName}: 缺少链接 ${expected.ref}`);
    const relationship = byId.get(node["r:id"]);
    assert.ok(relationship, `${item.key}/${sheetName}: 链接关系孤儿 ${expected.ref}`);
    assert.equal(relationship.TargetMode, "External", `${item.key}/${sheetName}: 链接必须为 External ${expected.ref}`);
    assert.match(relationship.Target, /^https:\/\//, `${item.key}/${sheetName}: 链接必须为 HTTPS ${expected.ref}`);
    assert.equal(relationship.Target, expected.target, `${item.key}/${sheetName}: 链接目标错误 ${expected.ref}`);
  }
  const referencedIds = new Set(nodes.map((node) => node["r:id"]));
  assert.ok(hyperlinkRelationships.every((relationship) => referencedIds.has(relationship.Id)), `${item.key}/${sheetName}: 存在孤儿链接关系`);
}

function assertPackageLayout(packageInfo, lastCatalogRow, lastSourceRow, item) {
  assert.deepEqual(packageInfo.sheetNames, SHEET_NAMES, `${item.key}: 工作表名称/顺序错误`);
  assert.match(packageInfo.stylesXml, /FF16324F/i, `${item.key}: 缺少深蓝标题样式`);
  assert.match(packageInfo.stylesXml, /FF1F7A8C/i, `${item.key}: 缺少蓝绿色表头样式`);
  for (const [sheetName, xml] of packageInfo.sheetXml) {
    assert.match(xml, /<(?:\w+:)?sheetView\b[^>]*showGridLines="0"/, `${item.key}/${sheetName}: 未隐藏网格线`);
  }
  assertFreezePane(packageInfo, item, "使用说明", { ySplit: "2", topLeftCell: "A3", activePane: "bottomLeft" });
  assertFreezePane(packageInfo, item, "AI技能清单", { xSplit: "4", ySplit: "4", topLeftCell: "E5", activePane: "bottomRight" });
  assertFreezePane(packageInfo, item, "分类统计", { ySplit: "4", topLeftCell: "A5", activePane: "bottomLeft" });
  assertFreezePane(packageInfo, item, "来源清单", { xSplit: "1", ySplit: "4", topLeftCell: "B5", activePane: "bottomRight" });
  const catalogXml = packageInfo.sheetXml.get("AI技能清单");
  assert.match(catalogXml, /<(?:\w+:)?cols>.*?<(?:\w+:)?col\b[^>]*min="1"[^>]*max="1"[^>]*width="[6-9](?:\.\d+)?"/s, `${item.key}: 列宽未写入`);
  assert.match(catalogXml, /<(?:\w+:)?row\b[^>]*r="1"[^>]*ht="(?:3[6-9]|4\d)(?:\.\d+)?"[^>]*customHeight="1"/, `${item.key}: 标题行高错误`);
  assert.match(catalogXml, /<(?:\w+:)?row\b[^>]*r="5"[^>]*ht="(?:[7-9]\d|1\d{2})(?:\.\d+)?"[^>]*customHeight="1"/, `${item.key}: 数据行高错误`);
  const aStyle = catalogXml.match(/<(?:\w+:)?c\b(?=[^>]*r="A5")(?=[^>]*s="(\d+)")[^>]*>/)?.[1];
  const mStyle = catalogXml.match(/<(?:\w+:)?c\b(?=[^>]*r="M5")(?=[^>]*s="(\d+)")[^>]*>/)?.[1];
  assert.ok(aStyle && mStyle && aStyle !== mStyle, `${item.key}: 用户区和追溯区样式未区分`);
  const conditionalRanges = [...catalogXml.matchAll(/<(?:\w+:)?conditionalFormatting\b[^>]*sqref="([^"]+)"/g)].map((match) => match[1]).sort();
  assert.deepEqual(conditionalRanges, [`I5:I${lastCatalogRow}`, `J5:J${lastCatalogRow}`], `${item.key}: 条件格式只能用于推荐程度和接入难度`);
  assertTableFilter(packageInfo, item, "AI技能清单", `A4:V${lastCatalogRow}`);
  assertTableFilter(packageInfo, item, "来源清单", `A4:G${lastSourceRow}`);
}

function countBy(records, selector) {
  const counts = new Map();
  for (const record of records) {
    const key = selector(record);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return counts;
}

function assertCountCell(sheet, item, reference, expectedFormula, expectedValue, label) {
  const cell = sheet.getRange(reference);
  assert.equal(cell.formulas[0][0], expectedFormula, `${item.key}/${label}: 公式错误 ${reference}`);
  assert.equal(Number(cell.values[0][0]), expectedValue, `${item.key}/${label}: 逐项计数错误 ${reference}`);
}

function assertStatistics(sheet, item, records, taxonomy) {
  const lastCatalogRow = records.length + 4;
  assertCountCell(
    sheet,
    item,
    "B3",
    `=COUNTA('AI技能清单'!$N$5:$N$${lastCatalogRow})`,
    records.length,
    "分类统计总数",
  );
  if (item.scope === "overview") {
    const categories = taxonomy
      .filter((category) => category.code.startsWith(`${item.big_category_code}-`))
      .sort((left, right) => left.code.localeCompare(right.code));
    const counts = countBy(records, (record) => record.subcategory_code);
    assert.deepEqual(
      sheet.getRange(`A6:A${categories.length + 5}`).values.flat(),
      categories.map((category) => `${category.code} ${category.name}`),
      `${item.key}/分类统计: 小分类标签或顺序错误`,
    );
    for (let index = 0; index < categories.length; index += 1) {
      const row = index + 6;
      assertCountCell(
        sheet,
        item,
        `B${row}`,
        `=COUNTIF('AI技能清单'!$B$5:$B$${lastCatalogRow},A${row})`,
        counts.get(categories[index].code) ?? 0,
        `小分类 ${categories[index].code} 计数`,
      );
    }
  }

  const priorityColumn = item.scope === "overview" ? "D" : "A";
  const priorityValueColumn = item.scope === "overview" ? "E" : "B";
  const priorityCounts = countBy(records, (record) => record.priority);
  assert.deepEqual(sheet.getRange(`${priorityColumn}6:${priorityColumn}8`).values.flat(), ["高", "中", "其他"], `${item.key}/分类统计: 推荐等级顺序错误`);
  assertCountCell(sheet, item, `${priorityValueColumn}6`, `=COUNTIF('AI技能清单'!$I$5:$I$${lastCatalogRow},${priorityColumn}6)`, priorityCounts.get("高") ?? 0, "推荐等级 高");
  assertCountCell(sheet, item, `${priorityValueColumn}7`, `=COUNTIF('AI技能清单'!$I$5:$I$${lastCatalogRow},${priorityColumn}7)`, priorityCounts.get("中") ?? 0, "推荐等级 中");
  const otherPriority = records.filter((record) => !["高", "中"].includes(record.priority)).length;
  assertCountCell(
    sheet,
    item,
    `${priorityValueColumn}8`,
    `=COUNTIF('AI技能清单'!$I$5:$I$${lastCatalogRow},"<>高")-COUNTIF('AI技能清单'!$I$5:$I$${lastCatalogRow},"中")`,
    otherPriority,
    "推荐等级 其他",
  );

  const difficultyColumn = item.scope === "overview" ? "G" : "D";
  const difficultyValueColumn = item.scope === "overview" ? "H" : "E";
  const levels = Object.values(DIFFICULTY);
  const difficultyCounts = countBy(records, (record) => DIFFICULTY[record.compat] ?? record.compat);
  assert.deepEqual(sheet.getRange(`${difficultyColumn}6:${difficultyColumn}9`).values.flat(), levels, `${item.key}/分类统计: 难度等级顺序错误`);
  for (let index = 0; index < levels.length; index += 1) {
    const row = index + 6;
    assertCountCell(
      sheet,
      item,
      `${difficultyValueColumn}${row}`,
      `=COUNTIF('AI技能清单'!$J$5:$J$${lastCatalogRow},${difficultyColumn}${row})`,
      difficultyCounts.get(levels[index]) ?? 0,
      `难度等级 ${levels[index]}`,
    );
  }
}

function expectedRepositories(records) {
  return [...new Set(records.map((record) => record.repo))].sort().map((repository) => {
    const record = records.find((candidate) => candidate.repo === repository);
    return {
      repository,
      target: record.repo_url,
      row: [repository, record.repo_url, record.form, record.license, Number(record.stars), record.repo_pushed],
      count: records.filter((candidate) => candidate.repo === repository).length,
    };
  });
}

function assertSources(sheet, item, records) {
  const repositories = expectedRepositories(records);
  const lastCatalogRow = records.length + 4;
  const actualRows = sheet.getRange(`A5:F${repositories.length + 4}`).values
    .map((row) => row.map((value, columnIndex) => normalizeCellValue(value, columnIndex === 5 ? 19 : columnIndex)));
  assert.deepEqual(actualRows, repositories.map(({ row }) => row), `${item.key}/来源清单: 事实列逐项错误`);
  for (let index = 0; index < repositories.length; index += 1) {
    const row = index + 5;
    assertCountCell(
      sheet,
      item,
      `G${row}`,
      `=COUNTIF('AI技能清单'!$V$5:$V$${lastCatalogRow},B${row})`,
      repositories[index].count,
      `仓库 ${repositories[index].repository} 计数`,
    );
  }
  return repositories;
}

export async function verifySpreadsheetFile(filePath, item, records, taxonomy) {
  const expectedRecords = expectedRecordsFor(item, records);
  if (!expectedRecords.length) throw new Error(`${item.key}: Skill ID 成员不一致，期望集合为空`);
  for (const record of expectedRecords) {
    const category = taxonomy.find((candidate) => candidate.code === record.subcategory_code);
    if (!category || category.name !== record.subcategory_name) throw new Error(`${item.key}: 小分类成员不一致 ${record.id}`);
  }
  const packageInfo = await inspectXlsxPackage(filePath);
  const repositories = expectedRepositories(expectedRecords);
  const lastRow = expectedRecords.length + 4;
  const lastSourceRow = repositories.length + 4;
  assertPackageLayout(packageInfo, lastRow, lastSourceRow, item);
  const catalogLinks = expectedRecords.flatMap((record, index) => [
    { ref: `U${index + 5}`, target: record.skill_url },
    { ref: `V${index + 5}`, target: record.repo_url },
  ]);
  const sourceLinks = repositories.map((repository, index) => ({ ref: `B${index + 5}`, target: repository.target }));
  assertHyperlinkPlan(packageInfo, item, "AI技能清单", catalogLinks);
  assertHyperlinkPlan(packageInfo, item, "来源清单", sourceLinks);

  let workbook;
  try {
    workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(filePath));
  } catch (error) {
    throw new Error(`${item.key}: XLSX 无法重新打开: ${error.message}`);
  }
  assert.deepEqual(workbook.worksheets.items.map((sheet) => sheet.name), SHEET_NAMES, `${item.key}: 缺少或多出工作表`);
  const catalog = workbook.worksheets.getItem("AI技能清单");
  assert.deepEqual(catalog.getRange("A4:V4").values[0], CATALOG_HEADERS, `${item.key}: 清单列顺序错误`);
  const actualCatalogRows = catalog.getRange(`A5:V${lastRow}`).values
    .map((row) => row.map((value, columnIndex) => normalizeCellValue(value, columnIndex)));
  assert.deepEqual(actualCatalogRows, expectedCatalogRows(expectedRecords), `${item.key}: AI技能清单全部22列事实逐项不一致`);

  const stats = workbook.worksheets.getItem("分类统计");
  assertStatistics(stats, item, expectedRecords, taxonomy);

  const sources = workbook.worksheets.getItem("来源清单");
  assertSources(sources, item, expectedRecords);

  const errors = formulaErrors(workbook);
  assert.deepEqual(errors, [], `${item.key}: 发现公式错误值 ${errors.join("; ")}`);
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
  const outputRoot = process.env.SUBCATEGORY_OUTPUT_ROOT
    ? path.resolve(process.env.SUBCATEGORY_OUTPUT_ROOT)
    : PROJECT_ROOT;
  const results = await verifySelectedSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, outputRoot, { only: parseOnly(argv) });
  console.log(`xlsx=${results.length} sheets=${results.reduce((sum, result) => sum + result.sheetCount, 0)} formulas=OK structure=OK`);
  return 0;
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) {
  main().catch((error) => {
    console.error(`XLSX 验证失败: ${error.message}`);
    process.exitCode = 1;
  });
}
