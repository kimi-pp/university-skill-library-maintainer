import fs from "node:fs/promises";
import path from "node:path";
import { deflateRawSync, inflateRawSync } from "node:zlib";
import { FileBlob, SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const DAILY_SHEETS = [
  "使用说明",
  "执行概览",
  "目录变化",
  "新增正式推荐",
  "版本更新",
  "发现更新未升级",
  "条件候选",
  "需适配候选",
  "去重与来源别名",
  "受影响专业类",
  "排除原因汇总",
  "来源请求审计",
];

const inputPath = process.argv[2];
const outputPath = process.argv[3];
const verifyFlag = process.argv[4];
const verifyDir = verifyFlag === "--verify-dir" ? process.argv[5] : null;
if (!inputPath || !outputPath) {
  throw new Error("usage: daily_xlsx_builder.mjs INPUT_JSON OUTPUT_XLSX [--verify-dir DIRECTORY]");
}

const payload = JSON.parse(await fs.readFile(inputPath, "utf8"));
const workbook = Workbook.create();
workbook.setColorScheme({
  name: "Skill Maintainer",
  themeColors: {
    accent1: "#2E74B5",
    accent2: "#1F4D78",
    accent3: "#4F7A66",
    dk1: "#1F2937",
    lt1: "#FFFFFF",
    lt2: "#F2F4F7",
    hlink: "#0563C1",
    folHlink: "#954F72",
  },
});
for (const name of DAILY_SHEETS) workbook.worksheets.add(name);

const asText = (value) => value === null || value === undefined ? "" : String(value);
const asDate = (value) => {
  if (!value) return null;
  const wallTime = String(value).match(/^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2}))?$/);
  if (wallTime) {
    return new Date(Date.UTC(
      Number(wallTime[1]), Number(wallTime[2]) - 1, Number(wallTime[3]),
      Number(wallTime[4]), Number(wallTime[5]), Number(wallTime[6] ?? 0),
    ));
  }
  const parsed = new Date(value);
  return Number.isNaN(parsed.valueOf()) ? null : parsed;
};
const tableNames = {
  "使用说明": "DailyInstructions",
  "执行概览": "DailyOverview",
  "目录变化": "DailyCatalogChanges",
  "新增正式推荐": "DailyFormalAdditions",
  "版本更新": "DailyVersionUpdates",
  "发现更新未升级": "DailyUpdatesNotApplied",
  "条件候选": "DailyConditionalCandidates",
  "需适配候选": "DailyAdaptationCandidates",
  "去重与来源别名": "DailySourceAliases",
  "受影响专业类": "DailyAffectedScopes",
  "排除原因汇总": "DailyExclusionReasons",
  "来源请求审计": "DailySourceAudit",
};
const hyperlinksBySheet = new Map();

function registerHyperlink(sheetName, cell, target) {
  if (!target) return;
  if (!hyperlinksBySheet.has(sheetName)) hyperlinksBySheet.set(sheetName, []);
  hyperlinksBySheet.get(sheetName).push({ cell, target });
}

function columnLetter(number) {
  let result = "";
  let current = number;
  while (current > 0) {
    const remainder = (current - 1) % 26;
    result = String.fromCharCode(65 + remainder) + result;
    current = Math.floor((current - 1) / 26);
  }
  return result;
}

const crcTable = (() => {
  const table = new Uint32Array(256);
  for (let index = 0; index < 256; index += 1) {
    let value = index;
    for (let bit = 0; bit < 8; bit += 1) value = (value & 1) ? (0xEDB88320 ^ (value >>> 1)) : (value >>> 1);
    table[index] = value >>> 0;
  }
  return table;
})();

function crc32(data) {
  let crc = 0xFFFFFFFF;
  for (const byte of data) crc = crcTable[(crc ^ byte) & 0xFF] ^ (crc >>> 8);
  return (crc ^ 0xFFFFFFFF) >>> 0;
}

function locateEndOfCentralDirectory(buffer) {
  const minimum = Math.max(0, buffer.length - 65557);
  for (let offset = buffer.length - 22; offset >= minimum; offset -= 1) {
    if (buffer.readUInt32LE(offset) === 0x06054B50) return offset;
  }
  throw new Error("artifact-tool output is not a readable ZIP container");
}

function readZipEntries(buffer) {
  const end = locateEndOfCentralDirectory(buffer);
  const count = buffer.readUInt16LE(end + 10);
  let cursor = buffer.readUInt32LE(end + 16);
  const entries = [];
  for (let index = 0; index < count; index += 1) {
    if (buffer.readUInt32LE(cursor) !== 0x02014B50) throw new Error("invalid ZIP central-directory entry");
    const method = buffer.readUInt16LE(cursor + 10);
    const compressedSize = buffer.readUInt32LE(cursor + 20);
    const nameLength = buffer.readUInt16LE(cursor + 28);
    const extraLength = buffer.readUInt16LE(cursor + 30);
    const commentLength = buffer.readUInt16LE(cursor + 32);
    const localOffset = buffer.readUInt32LE(cursor + 42);
    const name = buffer.subarray(cursor + 46, cursor + 46 + nameLength).toString("utf8");
    if (buffer.readUInt32LE(localOffset) !== 0x04034B50) throw new Error(`invalid ZIP local header: ${name}`);
    const localNameLength = buffer.readUInt16LE(localOffset + 26);
    const localExtraLength = buffer.readUInt16LE(localOffset + 28);
    const dataOffset = localOffset + 30 + localNameLength + localExtraLength;
    const compressed = buffer.subarray(dataOffset, dataOffset + compressedSize);
    let data;
    if (method === 0) data = Buffer.from(compressed);
    else if (method === 8) data = inflateRawSync(compressed);
    else throw new Error(`unsupported ZIP compression method ${method}: ${name}`);
    entries.push({
      name,
      data,
      modTime: buffer.readUInt16LE(cursor + 12),
      modDate: buffer.readUInt16LE(cursor + 14),
      externalAttributes: buffer.readUInt32LE(cursor + 38),
    });
    cursor += 46 + nameLength + extraLength + commentLength;
  }
  return entries;
}

function writeZipEntries(entries) {
  const localParts = [];
  const centralParts = [];
  let localOffset = 0;
  for (const entry of entries) {
    const name = Buffer.from(entry.name, "utf8");
    const compressed = entry.data.length ? deflateRawSync(entry.data, { level: 6 }) : Buffer.alloc(0);
    const method = entry.data.length ? 8 : 0;
    const checksum = crc32(entry.data);
    const local = Buffer.alloc(30);
    local.writeUInt32LE(0x04034B50, 0);
    local.writeUInt16LE(20, 4);
    local.writeUInt16LE(0x0800, 6);
    local.writeUInt16LE(method, 8);
    local.writeUInt16LE(entry.modTime, 10);
    local.writeUInt16LE(entry.modDate, 12);
    local.writeUInt32LE(checksum, 14);
    local.writeUInt32LE(compressed.length, 18);
    local.writeUInt32LE(entry.data.length, 22);
    local.writeUInt16LE(name.length, 26);
    local.writeUInt16LE(0, 28);
    localParts.push(local, name, compressed);

    const central = Buffer.alloc(46);
    central.writeUInt32LE(0x02014B50, 0);
    central.writeUInt16LE(20, 4);
    central.writeUInt16LE(20, 6);
    central.writeUInt16LE(0x0800, 8);
    central.writeUInt16LE(method, 10);
    central.writeUInt16LE(entry.modTime, 12);
    central.writeUInt16LE(entry.modDate, 14);
    central.writeUInt32LE(checksum, 16);
    central.writeUInt32LE(compressed.length, 20);
    central.writeUInt32LE(entry.data.length, 24);
    central.writeUInt16LE(name.length, 28);
    central.writeUInt16LE(0, 30);
    central.writeUInt16LE(0, 32);
    central.writeUInt16LE(0, 34);
    central.writeUInt16LE(0, 36);
    central.writeUInt32LE(entry.externalAttributes, 38);
    central.writeUInt32LE(localOffset, 42);
    centralParts.push(central, name);
    localOffset += local.length + name.length + compressed.length;
  }
  const centralDirectory = Buffer.concat(centralParts);
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054B50, 0);
  end.writeUInt16LE(0, 4);
  end.writeUInt16LE(0, 6);
  end.writeUInt16LE(entries.length, 8);
  end.writeUInt16LE(entries.length, 10);
  end.writeUInt32LE(centralDirectory.length, 12);
  end.writeUInt32LE(localOffset, 16);
  end.writeUInt16LE(0, 20);
  return Buffer.concat([...localParts, centralDirectory, end]);
}

function addFrozenHeaderView(xml, sheetName) {
  if (/<(?:\w+:)?pane\b/.test(xml)) return xml;
  const pane = '<x:pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen" />';
  const selfClosing = /<x:sheetView([^>]*)\/>/;
  if (selfClosing.test(xml)) return xml.replace(selfClosing, `<x:sheetView$1>${pane}</x:sheetView>`);
  const opening = /<x:sheetView([^>]*)>/;
  if (opening.test(xml)) return xml.replace(opening, `<x:sheetView$1>${pane}`);
  throw new Error(`worksheet has no sheetView to freeze: ${sheetName}`);
}

function xmlAttribute(value) {
  return String(value).replaceAll("&", "&amp;").replaceAll('"', "&quot;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
}

function addWorksheetHyperlinks(xml, links, relationIds) {
  if (!links.length) return xml;
  xml = xml.replace(/<x:worksheet([^>]*)>/, (match, attributes) => attributes.includes("xmlns:r=")
    ? match
    : `<x:worksheet${attributes} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">`);
  const nodes = links.map((link, index) => `<x:hyperlink ref="${xmlAttribute(link.cell)}" r:id="${relationIds[index]}" />`).join("");
  const block = `<x:hyperlinks>${nodes}</x:hyperlinks>`;
  const insertion = xml.search(/<x:(?:printOptions|pageMargins|pageSetup|headerFooter|drawing|legacyDrawing|tableParts)\b/);
  if (insertion >= 0) return xml.slice(0, insertion) + block + xml.slice(insertion);
  return xml.replace("</x:worksheet>", `${block}</x:worksheet>`);
}

function addHyperlinkRelationships(xml, links) {
  const ids = [...xml.matchAll(/\bId="rId(\d+)"/g)].map((match) => Number(match[1]));
  let nextId = Math.max(0, ...ids) + 1;
  const relationIds = [];
  const relations = [];
  for (const link of links) {
    const id = `rId${nextId++}`;
    relationIds.push(id);
    relations.push(`<Relationship Id="${id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="${xmlAttribute(link.target)}" TargetMode="External" />`);
  }
  if (/\/>\s*$/.test(xml) && /<Relationships\b/.test(xml)) {
    xml = xml.replace(/\s*\/>\s*$/, `>${relations.join("")}</Relationships>`);
  } else {
    xml = xml.replace("</Relationships>", `${relations.join("")}</Relationships>`);
  }
  return { xml, relationIds };
}

async function persistWorkbookCompatibility(xlsxPath) {
  const entries = readZipEntries(await fs.readFile(xlsxPath));
  const byName = new Map(entries.map((entry) => [entry.name, entry]));
  let patched = 0;
  for (let index = 0; index < DAILY_SHEETS.length; index += 1) {
    const sheetNumber = index + 1;
    const sheetPath = `xl/worksheets/sheet${sheetNumber}.xml`;
    const entry = byName.get(sheetPath);
    if (!entry) throw new Error(`missing worksheet part: ${sheetPath}`);
    let xml = addFrozenHeaderView(entry.data.toString("utf8"), entry.name);
    const links = hyperlinksBySheet.get(DAILY_SHEETS[index]) ?? [];
    if (links.length) {
      const relPath = `xl/worksheets/_rels/sheet${sheetNumber}.xml.rels`;
      let relEntry = byName.get(relPath);
      if (!relEntry) {
        relEntry = {
          name: relPath,
          data: Buffer.from('<?xml version="1.0" encoding="utf-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>', "utf8"),
          modTime: entry.modTime,
          modDate: entry.modDate,
          externalAttributes: 0,
        };
        entries.push(relEntry);
        byName.set(relPath, relEntry);
      }
      const relationships = addHyperlinkRelationships(relEntry.data.toString("utf8"), links);
      relEntry.data = Buffer.from(relationships.xml, "utf8");
      xml = addWorksheetHyperlinks(xml, links, relationships.relationIds);
    }
    entry.data = Buffer.from(xml, "utf8");
    patched += 1;
  }
  if (patched !== DAILY_SHEETS.length) throw new Error(`expected ${DAILY_SHEETS.length} worksheet views, patched ${patched}`);
  await fs.writeFile(xlsxPath, writeZipEntries(entries));
}

function writeSheet(name, headers, dataRows, options = {}) {
  const sheet = workbook.worksheets.getItem(name);
  sheet.showGridLines = false;
  const rows = dataRows.length ? dataRows : [headers.map(() => "")];
  const matrix = [headers, ...rows];
  const lastColumn = columnLetter(headers.length);
  const lastRow = matrix.length;
  sheet.getRange(`A1:${lastColumn}${lastRow}`).values = matrix;
  const header = sheet.getRange(`A1:${lastColumn}1`);
  header.format = {
    fill: "#2E74B5",
    font: { bold: true, color: "#FFFFFF", size: 11 },
    wrapText: true,
    verticalAlignment: "center",
    borders: { preset: "outside", style: "thin", color: "#1F4D78" },
  };
  header.format.rowHeight = 30;
  const body = sheet.getRange(`A2:${lastColumn}${lastRow}`);
  body.format = {
    font: { color: "#1F2937", size: 10 },
    verticalAlignment: "top",
    wrapText: true,
    borders: {
      insideHorizontal: { style: "thin", color: "#E4E7EC" },
      bottom: { style: "thin", color: "#D0D5DD" },
    },
  };
  body.format.rowHeight = 36;
  const table = sheet.tables.add(`A1:${lastColumn}${lastRow}`, true, tableNames[name]);
  table.style = "TableStyleMedium2";
  table.showHeaders = true;
  table.showFilterButton = true;
  table.showBandedRows = true;
  sheet.freezePanes.freezeRows(1);
  for (let index = 0; index < headers.length; index += 1) {
    const letter = columnLetter(index + 1);
    sheet.getRange(`${letter}:${letter}`).format.columnWidth = options.widths?.[index] ?? 18;
  }
  if (options.dateColumns) {
    for (const index of options.dateColumns) {
      const letter = columnLetter(index + 1);
      sheet.getRange(`${letter}2:${letter}${lastRow}`).format.numberFormat = "yyyy-mm-dd";
    }
  }
  if (options.centerColumns) {
    for (const index of options.centerColumns) {
      const letter = columnLetter(index + 1);
      sheet.getRange(`${letter}2:${letter}${lastRow}`).format.horizontalAlignment = "center";
    }
  }
  return { sheet, lastRow, lastColumn };
}

const instructions = [
  ["报告用途", "记录本轮高校专业 Skill 库静态查验结果、变化边界与人工复核事项。"],
  ["统计口径", "正式推荐、条件候选、需适配候选分别统计；条件候选和需适配候选不计入正式推荐。"],
  ["输入", "固定版本、来源快照、许可证、安全证据、专业任务映射和目录基线。"],
  ["输出", "中文日报、12 张查验工作表与受影响专业类副本。"],
  ["限制", "不列排除项名称；候选未安装、未运行；不上传真实教学或科研数据。"],
  ["可移植性", "工作簿由项目运行时通过 @oai/artifact-tool 生成，不依赖用户目录内的固定路径。"],
];
writeSheet("使用说明", ["项目", "说明"], instructions, { widths: [18, 90] });

const formalCount = payload.formal_additions.length;
const conditionalCount = payload.conditional_candidates.length;
const adaptationCount = payload.adaptation_candidates.length;
const formalLastRow = Math.max(2, formalCount + 1);
const overview = [
  ["运行标识", asText(payload.run_id)],
  ["生成时间", asDate(payload.generated_at)],
  ["运行状态", payload.blocked ? "阻断" : "完成"],
  ["新增正式推荐", formalCount],
  ["版本更新", payload.version_updates.length],
  ["条件候选", conditionalCount],
  ["需适配候选", adaptationCount],
  ["受影响专业类", payload.affected_scopes.length],
  ["正式推荐行数复核", null],
];
const overviewResult = writeSheet("执行概览", ["指标", "值"], overview, { widths: [28, 58] });
overviewResult.sheet.getRange("B10").formulas = [[`=COUNTA('新增正式推荐'!$A$2:$A$${formalLastRow})`]];
overviewResult.sheet.getRange("B3").format.numberFormat = "yyyy-mm-dd hh:mm";
overviewResult.sheet.getRange("B5:B10").format.numberFormat = "#,##0";

const catalogRows = payload.catalog_changes.map((row) => [
  asText(row["专业类"] ?? row.scope),
  asText(row["变化"] ?? row.change ?? row["说明"]),
]);
writeSheet("目录变化", ["专业类", "变化说明"], catalogRows, { widths: [28, 70] });

const skillHeaders = [
  "内部标识", "英文原名", "规范名称", "固定版本", "许可证", "来源平台", "Canonical source",
  "中文用途与功能", "适用人员", "输入", "输出", "限制", "专业类", "收集日期",
];
function skillMatrix(rows) {
  return rows.map((row) => [
    asText(row["内部标识"]),
    asText(row["Skill名称"] ?? row["英文原名"]),
    asText(row["规范名称"]),
    asText(row["固定版本"] ?? row["新版本"] ?? row["发现版本"]),
    asText(row["许可证"]),
    asText(row["来源平台"]),
    asText(row["Canonical source"] ?? row["来源地址"] ?? row["发现地址"]),
    asText(row["用途"] ?? row["简要功能"] ?? row["详细功能摘要"]),
    asText(row["适用人员"] ?? row["适用用户角色"]),
    asText(row["输入"]),
    asText(row["输出"]),
    asText(row["使用限制"] ?? row["安全限制条件"] ?? row["适配建议"]),
    asText(row["专业类"]),
    asDate(row["收集日期"] ?? row["记录日期"]),
  ]);
}
function writeSkillSheet(name, rows) {
  writeSheet(name, skillHeaders, skillMatrix(rows), {
    widths: [16, 26, 28, 14, 16, 18, 48, 48, 28, 34, 34, 48, 24, 14],
    dateColumns: [13],
    centerColumns: [0, 3, 4, 5, 13],
  });
  rows.forEach((row, index) => {
    const url = asText(row["Canonical source"] ?? row["来源地址"] ?? row["发现地址"]);
    registerHyperlink(name, `G${index + 2}`, url);
  });
}
writeSkillSheet("新增正式推荐", payload.formal_additions);
writeSkillSheet("版本更新", payload.version_updates);
writeSkillSheet("发现更新未升级", payload.updates_not_applied);
writeSkillSheet("条件候选", payload.conditional_candidates);
writeSkillSheet("需适配候选", payload.adaptation_candidates);

const aliasRows = payload.aliases.map((row) => [
  asText(row["内部标识"]),
  asText(row["来源平台"]),
  asText(row["来源地址"]),
  asText(row["Canonical source"]),
  asText(row["关系类型"] ?? "来源别名"),
  asText(row["去重依据"]),
  asDate(row["记录日期"]),
]);
writeSheet(
  "去重与来源别名",
  ["内部标识", "来源平台", "来源地址", "Canonical source", "关系类型", "去重依据", "记录日期"],
  aliasRows,
  { widths: [18, 18, 48, 48, 18, 42, 14], dateColumns: [6] },
);
payload.aliases.forEach((row, index) => {
  for (const [column, key] of [["C", "来源地址"], ["D", "Canonical source"]]) {
    const url = asText(row[key]);
    registerHyperlink("去重与来源别名", `${column}${index + 2}`, url);
  }
});

writeSheet("受影响专业类", ["专业类", "刷新说明"], payload.affected_scopes.map((scope) => [asText(scope), "存在实质变化，刷新本专业类 Word/Excel。"]), { widths: [30, 70] });

const reasonCounts = new Map();
for (const row of payload.exclusions) {
  const reason = asText(row["原因"] || "未分类原因");
  reasonCounts.set(reason, (reasonCounts.get(reason) ?? 0) + 1);
}
writeSheet("排除原因汇总", ["排除原因", "数量"], [...reasonCounts.entries()], { widths: [70, 16], centerColumns: [1] });

const requestRows = payload.source_requests.map((row) => [
  asText(row["来源平台"]),
  asText(row["请求地址"] ?? row.url),
  asText(row["状态"] ?? row.status),
  asDate(row["请求时间"] ?? row.requested_at),
]);
writeSheet("来源请求审计", ["来源平台", "请求地址", "状态", "请求时间"], requestRows, { widths: [22, 72, 16, 20], dateColumns: [3] });
payload.source_requests.forEach((row, index) => {
  const url = asText(row["请求地址"] ?? row.url);
  registerHyperlink("来源请求审计", `B${index + 2}`, url);
});

// Apply view state after all range/table mutations so later writes cannot replace it.
for (const name of DAILY_SHEETS) workbook.worksheets.getItem(name).freezePanes.freezeRows(1);

const overviewCheck = await workbook.inspect({
  kind: "table",
  range: "执行概览!A1:B10",
  include: "values,formulas",
  tableMaxRows: 12,
  tableMaxCols: 4,
  maxChars: 4000,
});
console.log(overviewCheck.ndjson);
const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
  maxChars: 4000,
});
console.log(formulaErrors.ndjson);

await fs.mkdir(path.dirname(outputPath), { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
// artifact-tool 2.8.6 drops freezeRows() panes and renders HYPERLINK formulas as
// implementation notices. Keep it as the sole content/style/formula author and
// repair only those two view/link packaging details in the emitted OOXML package.
await persistWorkbookCompatibility(outputPath);

if (verifyDir) {
  await fs.mkdir(verifyDir, { recursive: true });
  const imported = await SpreadsheetFile.importXlsx(await FileBlob.load(outputPath));
  const reread = await imported.inspect({
    kind: "table",
    range: `新增正式推荐!A1:N${formalLastRow}`,
    include: "values,formulas",
    tableMaxRows: 4,
    tableMaxCols: 14,
    maxChars: 5000,
  });
  console.log(reread.ndjson);
  const importedErrors = await imported.inspect({
    kind: "match",
    searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
    options: { useRegex: true, maxResults: 300 },
    summary: "reimported formula error scan",
    maxChars: 4000,
  });
  console.log(importedErrors.ndjson);
  for (const name of DAILY_SHEETS) {
    const sheet = imported.worksheets.getItem(name);
    const used = sheet.getUsedRange(true);
    const preview = await imported.render({
      sheetName: name,
      range: used ? used.address : "A1:B2",
      scale: 1,
      format: "png",
    });
    await fs.writeFile(path.join(verifyDir, `${String(DAILY_SHEETS.indexOf(name) + 1).padStart(2, "0")}-${name}.png`), new Uint8Array(await preview.arrayBuffer()));
  }
}
