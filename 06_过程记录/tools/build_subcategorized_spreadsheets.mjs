import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";
import { normalizeXlsxPackage, semanticXlsxDigest } from "./xlsx_package_utils.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
export const PROJECT_ROOT = path.resolve(scriptDir, "..", "..");
const PLAIN_CATALOG_FILE = path.join("03_候选池", "derived", "plain_language_catalog.json");
const ASSIGNMENT_FILE = path.join("03_候选池", "derived", "subcategory_assignments.json");
const MANIFEST_FILE = path.join("03_候选池", "derived", "subcategory_manifest.json");
const DELIVERY_ROOT = "05_交付物/通俗细分版_2026-08-07";
const DATA_DATE = "2026-08-07";

export const BIG_CATEGORY_NAMES = {
  "01": "学术写作、引用与出版",
  "02": "文档、表格、演示文稿与办公自动化",
  "03": "文献检索与学术研究",
  "04": "图书馆与信息素养",
  "05": "编程、数学、数据分析和可视化",
};

export const BIG_CATEGORY_DIRECTORIES = {
  "01": "01_学术写作引用与出版",
  "02": "02_文档表格演示文稿与办公自动化",
  "03": "03_文献检索与学术研究",
  "04": "04_图书馆与信息素养",
  "05": "05_编程数学数据分析和可视化",
};

export const SHEET_NAMES = ["使用说明", "AI技能清单", "分类统计", "来源清单"];
export const CATALOG_HEADERS = [
  "序号", "小分类", "中文名称", "主要用途", "适用人员", "典型场景", "使用前准备", "注意事项",
  "推荐程度", "接入难度", "接入建议", "本次核验", "英文名称", "内部编号", "功能标签", "原生生态",
  "来源形态", "许可证", "GitHub 关注数", "最近更新", "Skill 地址", "仓库地址",
];

export const PALETTE = {
  navy: "#16324F",
  teal: "#1F7A8C",
  paleBlue: "#EAF2F8",
  paleTeal: "#E7F3F4",
  paleTrace: "#F2F5F7",
  white: "#FFFFFF",
  ink: "#1F2933",
  muted: "#52606D",
  grid: "#CBD5E1",
  green: "#DDF3E4",
  greenInk: "#176B3A",
  amber: "#FFF0C7",
  amberInk: "#8A5A00",
  orange: "#FBE1D1",
  orangeInk: "#9A3412",
  red: "#FADBD8",
  redInk: "#8A1C1C",
};

const DIFFICULTY = {
  A: "A｜调整少",
  B: "B｜少量调整",
  C: "C｜较多调整",
  D: "D｜仅参考",
};

function sortRecords(records) {
  return [...records].sort((left, right) => left.id.localeCompare(right.id));
}

function taxonomyMap(taxonomy) {
  const result = new Map();
  for (const item of taxonomy) {
    if (!item || typeof item.code !== "string" || !/^\d{2}-\d{2}$/.test(item.code)) {
      throw new Error(`小分类代码格式错误: ${item?.code}`);
    }
    if (!BIG_CATEGORY_NAMES[item.code.slice(0, 2)]) throw new Error(`未知大分类: ${item.code}`);
    if (typeof item.name !== "string" || !item.name.trim()) throw new Error(`小分类名称不能为空: ${item.code}`);
    if (typeof item.inclusion_focus !== "string" || !item.inclusion_focus.trim()) throw new Error(`小分类收录重点不能为空: ${item.code}`);
    if (result.has(item.code)) throw new Error(`小分类代码重复: ${item.code}`);
    result.set(item.code, { ...item });
  }
  return result;
}

function manifestKey(item) {
  if (item.scope === "overview") return `${item.big_category_code}-overview`;
  if (item.scope === "subcategory") return String(item.subcategory_code);
  throw new Error(`未知 manifest scope: ${item.scope}`);
}

function safeRelativeXlsxPath(value) {
  if (typeof value !== "string" || !value) throw new Error("不安全的 manifest 路径: 空路径");
  if (value.includes("\\") || path.posix.isAbsolute(value) || path.win32.isAbsolute(value)) throw new Error(`不安全的 manifest 路径: ${value}`);
  const parts = value.split("/");
  if (parts.includes("..") || parts.includes(".") || parts.some((part) => !part || /[<>:"|?*\\]/.test(part))) {
    throw new Error(`不安全的 manifest 路径: ${value}`);
  }
  if (parts[0] !== "05_交付物" || !value.startsWith(`${DELIVERY_ROOT}/`) || path.posix.extname(value).toLowerCase() !== ".xlsx") {
    throw new Error(`不安全的 manifest 路径: ${value}`);
  }
  return parts;
}

function expectedManifestPath(item, taxonomyByCode) {
  const directory = BIG_CATEGORY_DIRECTORIES[item.big_category_code];
  if (item.scope === "overview") return `${DELIVERY_ROOT}/${directory}/00_大分类总览.xlsx`;
  const category = taxonomyByCode.get(item.subcategory_code);
  if (!category) throw new Error(`manifest 使用未知小分类: ${item.subcategory_code}`);
  const stem = `${item.subcategory_code}_${category.name}`;
  return `${DELIVERY_ROOT}/${directory}/${stem}/${stem}_GitHub技能调研.xlsx`;
}

function validateManifestContract(manifest, taxonomy) {
  const taxonomyByCode = taxonomyMap(taxonomy);
  const seenPaths = new Set();
  const seenKeys = new Set();
  for (const original of manifest) {
    if (original.format !== "xlsx") continue;
    const item = { ...original };
    if (!BIG_CATEGORY_NAMES[item.big_category_code]) throw new Error(`manifest 大分类错误: ${item.big_category_code}`);
    safeRelativeXlsxPath(item.path);
    const key = manifestKey(item);
    if (seenKeys.has(key)) throw new Error(`重复 XLSX manifest 键: ${key}`);
    if (seenPaths.has(item.path)) throw new Error(`重复 manifest 路径: ${item.path}`);
    seenKeys.add(key);
    seenPaths.add(item.path);
    if (item.scope === "subcategory") {
      const category = taxonomyByCode.get(item.subcategory_code);
      if (!category || item.subcategory_code.slice(0, 2) !== item.big_category_code) throw new Error(`小分类与大分类代码归属不一致: ${item.subcategory_code}`);
      if (item.subcategory_name !== category.name) throw new Error(`manifest 小分类名称不一致: ${item.subcategory_code}`);
    }
    const expected = expectedManifestPath(item, taxonomyByCode);
    if (item.path !== expected) throw new Error(`manifest 路径与元数据不一致: expected=${expected} actual=${item.path}`);
  }
  const expectedKeys = new Set([
    ...Object.keys(BIG_CATEGORY_NAMES).map((code) => `${code}-overview`),
    ...taxonomyByCode.keys(),
  ]);
  if (seenKeys.size !== expectedKeys.size || [...expectedKeys].some((key) => !seenKeys.has(key))) {
    throw new Error("manifest 未完整覆盖五个概览和 61 个小分类 XLSX");
  }
}

export function selectManifestItems(manifest, only = null) {
  const items = [];
  const seenKeys = new Set();
  for (const original of manifest) {
    if (original.format !== "xlsx") continue;
    const item = { ...original };
    safeRelativeXlsxPath(item.path);
    const key = manifestKey(item);
    if (seenKeys.has(key)) throw new Error(`重复 XLSX manifest 键: ${key}`);
    seenKeys.add(key);
    items.push({ ...item, key });
  }
  if (only?.length) {
    const requested = new Set(only);
    const unknown = [...requested].filter((key) => !seenKeys.has(key)).sort();
    if (unknown.length) throw new Error(`未知 --only 选择项: ${unknown.join(", ")}`);
    return items
      .filter((item) => requested.has(item.key))
      .sort((left, right) => left.big_category_code.localeCompare(right.big_category_code)
        || Number(left.scope !== "overview") - Number(right.scope !== "overview")
        || (left.subcategory_code ?? "").localeCompare(right.subcategory_code ?? ""));
  }
  return items.sort((left, right) => left.big_category_code.localeCompare(right.big_category_code)
    || Number(left.scope !== "overview") - Number(right.scope !== "overview")
    || (left.subcategory_code ?? "").localeCompare(right.subcategory_code ?? ""));
}

export function validateInputContracts(records, taxonomy, manifest, assignments = null) {
  if (!Array.isArray(records) || !Array.isArray(taxonomy) || !Array.isArray(manifest)) throw new Error("XLSX 输入数据格式错误");
  const taxonomyByCode = taxonomyMap(taxonomy);
  validateManifestContract(manifest, taxonomy);
  const seenIds = new Set();
  const groups = new Map([...taxonomyByCode.keys()].map((code) => [code, []]));
  for (const record of records) {
    if (seenIds.has(record.id)) throw new Error(`重复 Skill ID: ${record.id}`);
    seenIds.add(record.id);
    const category = taxonomyByCode.get(record.subcategory_code);
    if (!category || record.cat !== record.subcategory_code.slice(0, 2)) throw new Error(`小分类成员错配: ${record.id}`);
    if (record.subcategory_name !== category.name) throw new Error(`小分类名称不一致: ${record.id}`);
    if (assignments && assignments[record.id] !== record.subcategory_code) throw new Error(`归属台账成员错配: ${record.id}`);
    groups.get(record.subcategory_code).push(record.id);
  }
  if (assignments) {
    const assignmentIds = Object.keys(assignments);
    if (assignmentIds.length !== seenIds.size || assignmentIds.some((id) => !seenIds.has(id))) throw new Error("归属台账与通俗目录成员不一致");
  }
  for (const [code, ids] of groups) if (!ids.length) throw new Error(`空小分类: ${code}`);
}

async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

export async function loadInputs(projectRoot = PROJECT_ROOT) {
  const [records, assignment, manifest] = await Promise.all([
    readJson(path.join(projectRoot, PLAIN_CATALOG_FILE)),
    readJson(path.join(projectRoot, ASSIGNMENT_FILE)),
    readJson(path.join(projectRoot, MANIFEST_FILE)),
  ]);
  if (!assignment || !Array.isArray(assignment.taxonomy) || typeof assignment.assignments !== "object") throw new Error("小分类归属数据格式错误");
  validateInputContracts(records, assignment.taxonomy, manifest, assignment.assignments);
  if (records.length !== 157) throw new Error(`通俗目录成员总数错误: expected=157 actual=${records.length}`);
  return { records, taxonomy: assignment.taxonomy, assignments: assignment.assignments, manifest };
}

function scopeRecords(item, records) {
  const selected = sortRecords(records.filter((record) => item.scope === "overview"
    ? record.cat === item.big_category_code
    : record.subcategory_code === item.subcategory_code));
  if (!selected.length) throw new Error(`空小分类或空概览: ${item.key ?? manifestKey(item)}`);
  if (item.scope === "subcategory" && selected.some((record) => record.subcategory_code !== item.subcategory_code)) throw new Error(`小分类成员错配: ${item.subcategory_code}`);
  return selected;
}

function titleFor(item, taxonomyByCode) {
  if (item.scope === "overview") return `${BIG_CATEGORY_NAMES[item.big_category_code]}｜大分类总览`;
  return `${item.subcategory_code} ${taxonomyByCode.get(item.subcategory_code).name}｜小分类清单`;
}

function styleTitle(sheet, range, title, subtitle) {
  sheet.getRange(range).merge();
  sheet.getRange(range.split(":")[0]).values = [[title]];
  sheet.getRange(range).format = {
    fill: PALETTE.navy,
    font: { bold: true, color: PALETTE.white, size: 19, name: "Microsoft YaHei" },
    verticalAlignment: "center",
  };
  sheet.getRange(range).format.rowHeight = 40;
  const columns = range.split(":")[1].replace(/\d+/g, "");
  sheet.getRange(`A2:${columns}2`).merge();
  sheet.getRange("A2").values = [[subtitle]];
  sheet.getRange(`A2:${columns}2`).format = {
    fill: PALETTE.paleTeal,
    font: { color: PALETTE.navy, italic: true, name: "Microsoft YaHei" },
    wrapText: true,
    verticalAlignment: "center",
  };
  sheet.getRange(`A2:${columns}2`).format.rowHeight = 28;
}

function styleTable(sheet, range, headerRange) {
  sheet.getRange(headerRange).format = {
    fill: PALETTE.teal,
    font: { bold: true, color: PALETTE.white, name: "Microsoft YaHei" },
    wrapText: true,
    horizontalAlignment: "center",
    verticalAlignment: "center",
  };
  sheet.getRange(range).format.borders = { preset: "all", style: "thin", color: PALETTE.grid };
}

function subcategoryLabel(record) {
  return `${record.subcategory_code} ${record.subcategory_name}`;
}

function dateValue(value) {
  return new Date(`${value}T00:00:00Z`);
}

function createGuide(workbook, item, records, taxonomyByCode) {
  const sheet = workbook.worksheets.add("使用说明");
  sheet.showGridLines = false;
  styleTitle(sheet, "A1:D1", titleFor(item, taxonomyByCode), `通俗细分版｜数据日期 ${DATA_DATE}｜收录 ${records.length} 项｜本次未安装、未运行`);
  sheet.getRange("A4:B10").values = [
    ["阅读项目", "通俗说明"],
    ["什么是 Skill", "Skill 是一套告诉 AI 怎样完成某类任务的说明、步骤或配套文件；本表不把候选 Skill 写成已部署工具。"],
    ["先看什么", "先看“主要用途、适用人员、典型场景”，判断是否与自己的工作相符；再看准备事项、注意事项和接入建议。"],
    ["接入难度", "A 表示调整少；B 表示少量调整；C 表示较多调整；D 表示主要用于参考方法或模板。"],
    ["核验边界", "“说明已核验”或“包内容已核验”只代表已阅读公开资料或包内文件；本次未安装、未运行，不能据此判断实际效果。"],
    ["怎样筛选", "打开“AI技能清单”表，使用表头筛选按钮；可先按推荐程度和接入难度缩小范围，再按小分类或适用人员查看。"],
    ["怎样追溯", "用户字段位于左侧，技术追溯字段位于右侧；Skill 地址和仓库地址保留原始链接，许可证等事实保持原样。"],
  ];
  styleTable(sheet, "A4:B10", "A4:B4");
  sheet.getRange("A5:A10").format = { fill: PALETTE.paleBlue, font: { bold: true, color: PALETTE.navy } };
  sheet.getRange("B5:B10").format = { fill: PALETTE.white, wrapText: true, verticalAlignment: "top" };
  sheet.getRange("A4:B4").format.rowHeight = 28;
  sheet.getRange("A5:B10").format.rowHeight = 52;
  sheet.getRange("A:A").format.columnWidth = 20;
  sheet.getRange("B:B").format.columnWidth = 88;

  sheet.getRange("A12:D12").merge();
  sheet.getRange("A12").values = [["接入难度速查"]];
  sheet.getRange("A12:D12").format = { fill: PALETTE.navy, font: { bold: true, color: PALETTE.white } };
  sheet.getRange("A13:D17").values = [
    ["等级", "读法", "通常意味着", "建议"],
    ["A", "调整少", "基本结构可直接使用，仍需按本校制度和工具设置复核", "优先小范围试用"],
    ["B", "少量调整", "常需更换工具、路径、账号或权限设置", "列入适配队列"],
    ["C", "较多调整", "常需改写流程或增加配套服务", "先做场景验证"],
    ["D", "仅参考", "更适合吸收方法或模板，不建议原样接入", "按需摘取方法"],
  ];
  styleTable(sheet, "A13:D17", "A13:D13");
  sheet.getRange("A14:D17").format = { fill: PALETTE.paleTrace, wrapText: true, verticalAlignment: "top" };
  sheet.getRange("A14:A17").format.horizontalAlignment = "center";
  sheet.getRange("A13:D13").format.rowHeight = 28;
  sheet.getRange("A14:D17").format.rowHeight = 44;
  sheet.getRange("C:D").format.columnWidth = 34;
  sheet.freezePanes.freezeRows(2);
  return sheet;
}

function createCatalog(workbook, item, records, taxonomyByCode) {
  const sheet = workbook.worksheets.add("AI技能清单");
  sheet.showGridLines = false;
  styleTitle(sheet, "A1:V1", titleFor(item, taxonomyByCode), `用户字段在前，技术追溯字段在后｜共 ${records.length} 项｜地址可点击｜本次未安装、未运行`);
  sheet.getRange("A3:L3").merge();
  sheet.getRange("A3").values = [["面向使用者的信息"]];
  sheet.getRange("A3:L3").format = { fill: PALETTE.paleBlue, font: { bold: true, color: PALETTE.navy }, horizontalAlignment: "center" };
  sheet.getRange("M3:V3").merge();
  sheet.getRange("M3").values = [["技术追溯信息"]];
  sheet.getRange("M3:V3").format = { fill: PALETTE.paleTrace, font: { bold: true, color: PALETTE.muted }, horizontalAlignment: "center" };
  sheet.getRange("A4:V4").values = [CATALOG_HEADERS];

  const values = records.map((record, index) => [
    index + 1,
    subcategoryLabel(record),
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
    dateValue(record.repo_pushed),
    record.skill_url,
    record.repo_url,
  ]);
  const lastRow = records.length + 4;
  sheet.getRange(`A5:V${lastRow}`).values = values;
  styleTable(sheet, `A4:V${lastRow}`, "A4:V4");
  sheet.getRange(`A5:L${lastRow}`).format = { fill: PALETTE.white, font: { color: PALETTE.ink, name: "Microsoft YaHei" }, verticalAlignment: "top" };
  sheet.getRange(`M5:V${lastRow}`).format = { fill: PALETTE.paleTrace, font: { color: PALETTE.muted, name: "Microsoft YaHei" }, verticalAlignment: "top" };
  sheet.getRange(`B5:H${lastRow}`).format.wrapText = true;
  sheet.getRange(`K5:R${lastRow}`).format.wrapText = true;
  sheet.getRange(`U5:V${lastRow}`).format.wrapText = true;
  sheet.getRange(`A5:C${lastRow}`).format.horizontalAlignment = "center";
  sheet.getRange(`I5:J${lastRow}`).format.horizontalAlignment = "center";
  sheet.getRange(`M5:N${lastRow}`).format.horizontalAlignment = "center";
  sheet.getRange(`R5:T${lastRow}`).format.horizontalAlignment = "center";
  sheet.getRange(`S5:S${lastRow}`).format.numberFormat = "#,##0";
  sheet.getRange(`T5:T${lastRow}`).format.numberFormat = "yyyy-mm-dd";
  sheet.getRange("A4:V4").format.rowHeight = 38;
  sheet.getRange(`A5:V${lastRow}`).format.rowHeight = 92;

  const widths = {
    A: 7, B: 24, C: 24, D: 40, E: 28, F: 40, G: 40, H: 42, I: 13, J: 18, K: 44,
    L: 46, M: 26, N: 18, O: 34, P: 28, Q: 28, R: 18, S: 16, T: 16, U: 58, V: 58,
  };
  for (const [column, width] of Object.entries(widths)) sheet.getRange(`${column}:${column}`).format.columnWidth = width;
  sheet.freezePanes.freezeRows(4);
  sheet.freezePanes.freezeColumns(4);
  const table = sheet.tables.add(`A4:V${lastRow}`, true, `SkillTable${item.key.replaceAll("-", "")}`);
  table.style = "TableStyleMedium2";
  table.showFilterButton = true;
  table.showBandedRows = false;

  const priorityRange = sheet.getRange(`I5:I${lastRow}`);
  priorityRange.conditionalFormats.add("cellIs", { operator: "equal", formula: '"高"', format: { fill: PALETTE.green, font: { bold: true, color: PALETTE.greenInk } } });
  priorityRange.conditionalFormats.add("cellIs", { operator: "equal", formula: '"中"', format: { fill: PALETTE.amber, font: { color: PALETTE.amberInk } } });
  const difficultyRange = sheet.getRange(`J5:J${lastRow}`);
  difficultyRange.conditionalFormats.add("beginsWith", { text: "A", format: { fill: PALETTE.green, font: { bold: true, color: PALETTE.greenInk } } });
  difficultyRange.conditionalFormats.add("beginsWith", { text: "B", format: { fill: PALETTE.paleTeal, font: { bold: true, color: PALETTE.navy } } });
  difficultyRange.conditionalFormats.add("beginsWith", { text: "C", format: { fill: PALETTE.amber, font: { color: PALETTE.amberInk } } });
  difficultyRange.conditionalFormats.add("beginsWith", { text: "D", format: { fill: PALETTE.red, font: { color: PALETTE.redInk } } });
  return sheet;
}

function formulaCount(range, criteriaCell) {
  return `=COUNTIF('AI技能清单'!${range},${criteriaCell})`;
}

function createStats(workbook, item, records, taxonomyByCode) {
  const sheet = workbook.worksheets.add("分类统计");
  sheet.showGridLines = false;
  styleTitle(sheet, "A1:H1", `${titleFor(item, taxonomyByCode)}｜分类统计`, "数量均由“AI技能清单”公式计算，可随清单更新；不把统计结果写死。" );
  const lastCatalogRow = records.length + 4;
  sheet.getRange("A3:B3").values = [["收录 Skill", null]];
  sheet.getRange("B3").formulas = [[`=COUNTA('AI技能清单'!$N$5:$N$${lastCatalogRow})`]];
  sheet.getRange("A3:B3").format = { fill: PALETTE.paleBlue, font: { bold: true, color: PALETTE.navy }, horizontalAlignment: "center" };
  sheet.getRange("A3:B3").format.borders = { preset: "all", style: "thin", color: PALETTE.grid };

  let maxRow = 8;
  if (item.scope === "overview") {
    const categories = [...taxonomyByCode.values()].filter((category) => category.code.startsWith(`${item.big_category_code}-`)).sort((a, b) => a.code.localeCompare(b.code));
    sheet.getRange(`A5:B${categories.length + 5}`).values = [
      ["小分类", "数量"],
      ...categories.map((category) => [`${category.code} ${category.name}`, null]),
    ];
    sheet.getRange(`B6:B${categories.length + 5}`).formulas = categories.map((_, index) => [formulaCount(`$B$5:$B$${lastCatalogRow}`, `A${index + 6}`)]);
    styleTable(sheet, `A5:B${categories.length + 5}`, "A5:B5");
    maxRow = Math.max(maxRow, categories.length + 5);
  }

  const priorityColumn = item.scope === "overview" ? "D" : "A";
  const priorityValueColumn = item.scope === "overview" ? "E" : "B";
  sheet.getRange(`${priorityColumn}5:${priorityValueColumn}8`).values = [
    ["推荐程度", "数量"], ["高", null], ["中", null], ["其他", null],
  ];
  sheet.getRange(`${priorityValueColumn}6:${priorityValueColumn}7`).formulas = [
    [formulaCount(`$I$5:$I$${lastCatalogRow}`, `${priorityColumn}6`)],
    [formulaCount(`$I$5:$I$${lastCatalogRow}`, `${priorityColumn}7`)],
  ];
  sheet.getRange(`${priorityValueColumn}8`).formulas = [[`=COUNTIF('AI技能清单'!$I$5:$I$${lastCatalogRow},"<>高")-COUNTIF('AI技能清单'!$I$5:$I$${lastCatalogRow},"中")`]];
  styleTable(sheet, `${priorityColumn}5:${priorityValueColumn}8`, `${priorityColumn}5:${priorityValueColumn}5`);

  const difficultyColumn = item.scope === "overview" ? "G" : "D";
  const difficultyValueColumn = item.scope === "overview" ? "H" : "E";
  const levels = Object.values(DIFFICULTY);
  sheet.getRange(`${difficultyColumn}5:${difficultyValueColumn}9`).values = [
    ["接入难度", "数量"], ...levels.map((level) => [level, null]),
  ];
  sheet.getRange(`${difficultyValueColumn}6:${difficultyValueColumn}9`).formulas = levels.map((_, index) => [formulaCount(`$J$5:$J$${lastCatalogRow}`, `${difficultyColumn}${index + 6}`)]);
  styleTable(sheet, `${difficultyColumn}5:${difficultyValueColumn}9`, `${difficultyColumn}5:${difficultyValueColumn}5`);

  for (const columns of item.scope === "overview" ? ["A", "D", "G"] : ["A", "D"]) {
    sheet.getRange(`${columns}:${columns}`).format.columnWidth = columns === "A" && item.scope === "overview" ? 38 : 24;
  }
  for (const columns of item.scope === "overview" ? ["B", "E", "H"] : ["B", "E"]) sheet.getRange(`${columns}:${columns}`).format.columnWidth = 12;
  sheet.getRange(`A5:H${maxRow}`).format.wrapText = true;
  sheet.getRange(`A5:H${maxRow}`).format.verticalAlignment = "center";
  sheet.getRange(`B3:H${maxRow}`).format.numberFormat = "#,##0";
  sheet.freezePanes.freezeRows(4);
  return sheet;
}

function createSources(workbook, item, records, taxonomyByCode) {
  const sheet = workbook.worksheets.add("来源清单");
  sheet.showGridLines = false;
  styleTitle(sheet, "A1:G1", `${titleFor(item, taxonomyByCode)}｜来源清单`, "每个仓库只列一次；入选数量由“AI技能清单”的仓库地址公式计算。许可证以具体目录和当前仓库文件为准。" );
  const repositories = [...new Set(records.map((record) => record.repo))].sort();
  const rows = repositories.map((repository) => {
    const record = records.find((candidate) => candidate.repo === repository);
    return [repository, record.repo_url, record.form, record.license, Number(record.stars), dateValue(record.repo_pushed), null];
  });
  const lastRow = rows.length + 4;
  const lastCatalogRow = records.length + 4;
  sheet.getRange("A4:G4").values = [["仓库名称", "仓库地址", "来源形态", "许可证", "GitHub 关注数", "最近更新", "入选数量"]];
  sheet.getRange(`A5:G${lastRow}`).values = rows;
  sheet.getRange(`G5:G${lastRow}`).formulas = repositories.map((_, index) => [`=COUNTIF('AI技能清单'!$V$5:$V$${lastCatalogRow},B${index + 5})`]);
  styleTable(sheet, `A4:G${lastRow}`, "A4:G4");
  sheet.getRange(`A5:G${lastRow}`).format = { fill: PALETTE.white, font: { color: PALETTE.ink, name: "Microsoft YaHei" }, wrapText: true, verticalAlignment: "top" };
  sheet.getRange(`E5:E${lastRow}`).format.numberFormat = "#,##0";
  sheet.getRange(`F5:F${lastRow}`).format.numberFormat = "yyyy-mm-dd";
  sheet.getRange(`E5:G${lastRow}`).format.horizontalAlignment = "center";
  sheet.getRange("A4:G4").format.rowHeight = 34;
  sheet.getRange(`A5:G${lastRow}`).format.rowHeight = 68;
  const widths = { A: 38, B: 58, C: 32, D: 20, E: 18, F: 16, G: 14 };
  for (const [column, width] of Object.entries(widths)) sheet.getRange(`${column}:${column}`).format.columnWidth = width;
  sheet.freezePanes.freezeRows(4);
  sheet.freezePanes.freezeColumns(1);
  const table = sheet.tables.add(`A4:G${lastRow}`, true, `SourceTable${item.key.replaceAll("-", "")}`);
  table.style = "TableStyleMedium2";
  table.showFilterButton = true;
  table.showBandedRows = false;
  return sheet;
}

export function buildWorkbook(scope, records, taxonomy) {
  const item = { ...scope, key: scope.key ?? manifestKey(scope) };
  const taxonomyByCode = taxonomyMap(taxonomy);
  const selected = scopeRecords(item, records);
  const ids = selected.map((record) => record.id);
  if (new Set(ids).size !== ids.length) throw new Error(`重复 Skill ID: ${ids.find((id, index) => ids.indexOf(id) !== index)}`);
  for (const record of selected) {
    const category = taxonomyByCode.get(record.subcategory_code);
    if (!category || category.name !== record.subcategory_name) throw new Error(`小分类成员错配: ${record.id}`);
  }
  const workbook = Workbook.create();
  createGuide(workbook, item, selected, taxonomyByCode);
  createCatalog(workbook, item, selected, taxonomyByCode);
  createStats(workbook, item, selected, taxonomyByCode);
  createSources(workbook, item, selected, taxonomyByCode);
  return workbook;
}

export async function generateSpreadsheets(records, taxonomy, manifest, projectRoot, { only = null, assignments = null } = {}) {
  validateInputContracts(records, taxonomy, manifest, assignments);
  const root = path.resolve(projectRoot);
  const written = [];
  for (const item of selectManifestItems(manifest, only)) {
    const relativeParts = safeRelativeXlsxPath(item.path);
    const outputPath = path.resolve(root, ...relativeParts);
    const prefix = `${root}${path.sep}`.toLowerCase();
    if (!outputPath.toLowerCase().startsWith(prefix)) throw new Error(`不安全的输出路径: ${item.path}`);
    const selectedRecords = scopeRecords(item, records);
    await fs.mkdir(path.dirname(outputPath), { recursive: true });
    const candidatePath = `${outputPath}.task5-candidate`;
    await fs.rm(candidatePath, { force: true });
    const workbook = buildWorkbook(item, selectedRecords, taxonomy);
    const blob = await SpreadsheetFile.exportXlsx(workbook);
    const originalLog = console.log;
    try {
      console.log = () => {};
      await blob.save(candidatePath);
    } finally {
      console.log = originalLog;
    }
    const repositories = [...new Set(selectedRecords.map((record) => record.repo))].sort();
    await normalizeXlsxPackage(
      candidatePath,
      [
        {
          sheetPath: "xl/worksheets/sheet2.xml",
          links: selectedRecords.flatMap((record, index) => [
            { ref: `U${index + 5}`, target: record.skill_url },
            { ref: `V${index + 5}`, target: record.repo_url },
          ]),
        },
        {
          sheetPath: "xl/worksheets/sheet4.xml",
          links: repositories.map((repository, index) => ({
            ref: `B${index + 5}`,
            target: selectedRecords.find((record) => record.repo === repository).repo_url,
          })),
        },
      ],
      [
        { sheetPath: "xl/worksheets/sheet1.xml", ySplit: 2, topLeftCell: "A3", activePane: "bottomLeft" },
        { sheetPath: "xl/worksheets/sheet2.xml", xSplit: 4, ySplit: 4, topLeftCell: "E5", activePane: "bottomRight" },
        { sheetPath: "xl/worksheets/sheet3.xml", ySplit: 4, topLeftCell: "A5", activePane: "bottomLeft" },
        { sheetPath: "xl/worksheets/sheet4.xml", xSplit: 1, ySplit: 4, topLeftCell: "B5", activePane: "bottomRight" },
      ],
    );
    let keepExisting = false;
    try {
      const [existing, candidate] = await Promise.all([fs.readFile(outputPath), fs.readFile(candidatePath)]);
      keepExisting = semanticXlsxDigest(existing) === semanticXlsxDigest(candidate);
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    if (!keepExisting) await fs.copyFile(candidatePath, outputPath);
    await fs.rm(candidatePath, { force: true });
    await fs.rm(`${candidatePath}.inspect.ndjson`, { force: true });
    await fs.rm(`${outputPath}.inspect.ndjson`, { force: true });
    written.push({ item, outputPath });
  }
  return written;
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
  const only = parseOnly(argv);
  const inputs = await loadInputs(PROJECT_ROOT);
  const written = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, PROJECT_ROOT, { only, assignments: inputs.assignments });
  console.log(`xlsx=${written.length} keys=${written.map(({ item }) => item.key).join(",")}`);
  return 0;
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) {
  main().catch((error) => {
    console.error(`XLSX 生成失败: ${error.message}`);
    process.exitCode = 1;
  });
}
