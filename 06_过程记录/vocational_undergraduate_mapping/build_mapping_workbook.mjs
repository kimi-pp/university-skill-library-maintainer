import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";
import {
  normalizeXlsxPackage,
  semanticXlsxDigest,
} from "../tools/xlsx_package_utils.mjs";

export const OUTPUT_PATH =
  "D:/高校AI工作台/outputs/01a004e5-65dc-7c52-bd8c-7e29e9e058bc/高职专科专业与本科专业Skills相关性映射.xlsx";

export const SHEET_NAMES = [
  "使用说明与版本",
  "高职专科专业目录",
  "本科专业目录_2026",
  "高职本科相关性映射主表",
  "高职专业反向索引",
  "本科专业反向索引",
  "专业类映射汇总",
  "规则与字段字典",
  "来源台账",
  "质量复核清单",
  "统计总览",
];

const palette = {
  navy: "#17324D",
  teal: "#187B80",
  paleTeal: "#DDEEEF",
  paleBlue: "#E8EEF5",
  paleGold: "#FFF3D6",
  paleRed: "#FBE5E1",
  paleGreen: "#E0F1E7",
  paleGray: "#EEF2F5",
  ink: "#22313F",
  white: "#FFFFFF",
  grid: "#C9D2DA",
};

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const artifactDir = path.join(scriptDir, "artifacts");

function columnName(index) {
  let value = index + 1;
  let result = "";
  while (value > 0) {
    value -= 1;
    result = String.fromCharCode(65 + (value % 26)) + result;
    value = Math.floor(value / 26);
  }
  return result;
}

function stringify(value) {
  if (value === null || value === undefined) return "";
  if (Array.isArray(value)) return value.join("；");
  if (typeof value === "object") return JSON.stringify(value);
  return value;
}

function styleTitle(sheet, title, lastColumn, note) {
  sheet.getRange(`A1:${lastColumn}1`).merge();
  sheet.getRange("A1").values = [[title]];
  sheet.getRange(`A1:${lastColumn}1`).format = {
    fill: palette.navy,
    font: { bold: true, color: palette.white, size: 18 },
    verticalAlignment: "center",
  };
  sheet.getRange(`A1:${lastColumn}1`).format.rowHeight = 36;
  sheet.getRange(`A2:${lastColumn}2`).merge();
  sheet.getRange("A2").values = [[note]];
  sheet.getRange(`A2:${lastColumn}2`).format = {
    fill: palette.paleTeal,
    font: { color: palette.navy, italic: true },
    verticalAlignment: "center",
    wrapText: true,
  };
  sheet.getRange(`A2:${lastColumn}2`).format.rowHeight = 30;
}

function writeTableSheet(sheet, config) {
  const {
    title,
    note,
    headers,
    rows,
    tableName,
    widths,
    textColumns = [],
    wrapColumns = [],
    centeredColumns = [],
    freezeColumns = 0,
    rowHeight = 30,
  } = config;
  const lastColumn = columnName(headers.length - 1);
  const lastRow = rows.length + 4;
  styleTitle(sheet, title, lastColumn, note);
  sheet.getRange(`A4:${lastColumn}4`).values = [headers];
  for (const index of textColumns) {
    const letter = columnName(index);
    sheet.getRange(`${letter}5:${letter}${lastRow}`).format.numberFormat = "@";
  }
  if (rows.length > 0) sheet.getRange(`A5:${lastColumn}${lastRow}`).values = rows;
  sheet.getRange(`A4:${lastColumn}4`).format = {
    fill: palette.teal,
    font: { bold: true, color: palette.white },
    horizontalAlignment: "center",
    verticalAlignment: "center",
    wrapText: true,
  };
  sheet.getRange(`A4:${lastColumn}4`).format.rowHeight = 36;
  sheet.getRange(`A4:${lastColumn}${lastRow}`).format.borders = {
    preset: "all",
    style: "thin",
    color: palette.grid,
  };
  if (rows.length > 0) {
    sheet.getRange(`A5:${lastColumn}${lastRow}`).format = {
      font: { color: palette.ink, size: 10 },
      verticalAlignment: "top",
    };
    sheet.getRange(`A5:${lastColumn}${lastRow}`).format.rowHeight = rowHeight;
  }
  widths.forEach((width, index) => {
    const letter = columnName(index);
    sheet.getRange(`${letter}1:${letter}${lastRow}`).format.columnWidth = width;
  });
  for (const index of wrapColumns) {
    const letter = columnName(index);
    sheet.getRange(`${letter}5:${letter}${lastRow}`).format.wrapText = true;
  }
  for (const index of centeredColumns) {
    const letter = columnName(index);
    sheet.getRange(`${letter}5:${letter}${lastRow}`).format.horizontalAlignment = "center";
  }
  sheet.freezePanes.freezeRows(4);
  if (freezeColumns > 0) sheet.freezePanes.freezeColumns(freezeColumns);
  sheet.tables.add(`A4:${lastColumn}${lastRow}`, true, tableName);
  return { lastColumn, lastRow };
}

function addEqualsFormatting(range, value, format) {
  range.conditionalFormats.add("cellIs", {
    operator: "equal",
    formula: `"${value}"`,
    format,
  });
}

function assertInputs(bundle, qa, summary, policy, sources) {
  if (!Array.isArray(bundle?.vocational_catalog) || !Array.isArray(bundle?.undergraduate_catalog)) {
    throw new TypeError("mapping bundle is missing catalog arrays");
  }
  if (!Array.isArray(bundle.mappings) || !Array.isArray(bundle.vocational_index)) {
    throw new TypeError("mapping bundle is missing mapping arrays");
  }
  if (!Array.isArray(qa?.blocking) || !Array.isArray(qa?.review) || !Array.isArray(qa?.notice)) {
    throw new TypeError("QA payload is invalid");
  }
  if (summary?.vocational_count !== 811 || summary?.undergraduate_count !== 883) {
    throw new TypeError("summary payload is invalid");
  }
  if (!Array.isArray(policy?.relation_levels)) throw new TypeError("mapping policy is invalid");
  if (!Array.isArray(sources?.sources)) throw new TypeError("source manifest is invalid");
}

export function buildWorkbook(bundle, qa, summary, policy, sources) {
  assertInputs(bundle, qa, summary, policy, sources);
  const workbook = Workbook.create();
  const sheets = new Map(SHEET_NAMES.map((name) => [name, workbook.worksheets.add(name)]));
  for (const sheet of sheets.values()) sheet.showGridLines = false;

  const vocationalByCode = new Map(
    bundle.vocational_catalog.map((row) => [row.major_code, row]),
  );
  const undergraduateByCode = new Map(
    bundle.undergraduate_catalog.map((row) => [row.major_code, row]),
  );

  const guide = sheets.get("使用说明与版本");
  styleTitle(
    guide,
    "高职专科专业与本科专业 Skills 相关性映射｜使用说明与版本",
    "H",
    "覆盖教育部截至2026年7月的811个高职专科专业与《普通高等学校本科专业目录（2026年）》883个本科专业。",
  );
  guide.getRange("A4:B15").values = [
    ["项目", "说明"],
    ["用途", "服务高校 AI Skills 的学科标签与检索：主映射用于默认标签，其他核心用于辅助标签，强相关用于扩展检索，延伸相关用于跨学科召回。"],
    ["高职范围", `${summary.vocational_count} 个现行高职专科专业，含49个国控专业代码；9个2026年增补专业标注为自2027年起招生。`],
    ["本科范围", `${summary.undergraduate_count} 个本科专业，完整保留没有高职对应的本科专业。`],
    ["正式关系", `${summary.mapping_count} 条已复核接受关系，候选关系未通过复核不得进入本表。`],
    ["零映射保留", "高职与本科两端均保留无直接对应对象；“无直接对应”是审查结果，不是数据遗漏。"],
    ["敏感边界", "受限对象只能保留目录参考，且不可用于标签、检索或推荐；本批数据未生成此类正式关系。"],
    ["资格边界", "专业相关性不代表学历等同、专升本对应、招生报考资格、执业资格或职业准入结论。"],
    ["关系等级", policy.relation_levels.join("、")],
    ["质量状态", `阻断 ${qa.blocking.length}；建议专家复核 ${qa.review.length}；提示 ${qa.notice.length}。`],
    ["目录版本", bundle.metadata.catalog_version],
    ["生成日期", bundle.metadata.generated_at],
  ];
  guide.getRange("A4:B4").format = {
    fill: palette.teal,
    font: { bold: true, color: palette.white },
  };
  guide.getRange("A4:B15").format.borders = {
    preset: "all",
    style: "thin",
    color: palette.grid,
  };
  guide.getRange("A5:A15").format = {
    fill: palette.paleBlue,
    font: { bold: true, color: palette.navy },
  };
  guide.getRange("B5:B15").format.wrapText = true;
  guide.getRange("A4:A15").format.columnWidth = 22;
  guide.getRange("B4:B15").format.columnWidth = 96;
  guide.getRange("A5:B15").format.rowHeight = 40;
  guide.getRange("B15").format.numberFormat = "yyyy-mm-dd";
  guide.freezePanes.freezeRows(2);

  writeTableSheet(sheets.get("高职专科专业目录"), {
    title: "高等职业教育专科专业目录（截至2026年7月）",
    note: "完整保留811个专业、19个专业大类、97个专业类；K后缀按原代码保存。",
    headers: ["专业大类代码", "专业大类名称", "专业类代码", "专业类名称", "专业代码", "专业名称", "是否国控", "目录状态", "目录版本", "招生执行", "来源ID"],
    rows: bundle.vocational_catalog.map((row) => [
      row.category_code,
      row.category_name,
      row.class_code,
      row.class_name,
      row.major_code,
      row.major_name,
      row.is_national_control ? "是" : "否",
      row.catalog_status,
      row.catalog_version,
      row.enrollment_effective,
      stringify(row.source_ids),
    ]),
    tableName: "VocationalCatalog2026",
    widths: [14, 22, 14, 25, 16, 34, 12, 14, 42, 16, 30],
    textColumns: [0, 2, 4],
    wrapColumns: [1, 3, 5, 8, 10],
    centeredColumns: [0, 2, 4, 6, 7, 9],
    freezeColumns: 6,
    rowHeight: 34,
  });

  writeTableSheet(sheets.get("本科专业目录_2026"), {
    title: "普通高等学校本科专业目录（2026年）",
    note: "完整保留883个本科专业；代码按文本保存，未映射专业仍在目录和反向索引中保留。",
    headers: ["门类代码", "门类名称", "专业类代码", "专业类名称", "专业代码", "专业名称", "专业属性", "授予学位门类", "学制", "来源ID"],
    rows: bundle.undergraduate_catalog.map((row) => [
      row.category_code,
      row.category_name,
      row.class_code,
      row.class_name,
      row.major_code,
      row.major_name,
      stringify(row.attributes),
      stringify(row.degree_categories),
      row.duration,
      row.source_id,
    ]),
    tableName: "UndergraduateCatalog2026",
    widths: [12, 18, 14, 24, 16, 32, 20, 24, 10, 28],
    textColumns: [0, 2, 4],
    wrapColumns: [3, 5, 6, 7, 9],
    centeredColumns: [0, 2, 4, 8],
    freezeColumns: 6,
    rowHeight: 32,
  });

  const mappingRows = bundle.mappings.map((mapping) => {
    const vocational = vocationalByCode.get(mapping.vocational_code);
    const undergraduate = undergraduateByCode.get(mapping.undergraduate_code);
    return [
      mapping.mapping_id,
      vocational.category_code,
      vocational.category_name,
      vocational.class_code,
      vocational.class_name,
      vocational.major_code,
      vocational.major_name,
      undergraduate.category_code,
      undergraduate.category_name,
      undergraduate.class_code,
      undergraduate.class_name,
      undergraduate.major_code,
      undergraduate.major_name,
      mapping.relation_level,
      mapping.is_primary ? "是" : "否",
      stringify(mapping.relation_basis),
      mapping.rationale,
      mapping.skills_behavior,
      mapping.consumable ? "是" : "否",
      mapping.sensitive_restriction ? "是" : "否",
      mapping.review_status,
      mapping.confidence,
      mapping.generation_method,
      mapping.source_rule_id,
    ];
  });
  const mappingRange = writeTableSheet(sheets.get("高职本科相关性映射主表"), {
    title: "高职专科—本科专业相关性映射主表",
    note: "仅包含逐专业复核后接受的关系；关系等级直接控制 Skills 标签与检索行为。",
    headers: ["映射ID", "高职大类代码", "高职大类名称", "高职专业类代码", "高职专业类名称", "高职专业代码", "高职专业名称", "本科门类代码", "本科门类名称", "本科专业类代码", "本科专业类名称", "本科专业代码", "本科专业名称", "关系等级", "是否主映射", "关系依据", "映射理由", "Skills行为", "可供消费", "敏感限制", "复核状态", "置信度", "生成方式", "规则ID"],
    rows: mappingRows,
    tableName: "VocationalUndergraduateMappings",
    widths: [30, 14, 20, 15, 24, 16, 32, 13, 18, 15, 24, 16, 32, 20, 14, 30, 66, 18, 13, 13, 28, 12, 22, 24],
    textColumns: [0, 1, 3, 5, 7, 9, 11],
    wrapColumns: [2, 4, 6, 8, 10, 12, 13, 15, 16, 17, 20, 22, 23],
    centeredColumns: [1, 3, 5, 7, 9, 11, 14, 18, 19, 21],
    freezeColumns: 7,
    rowHeight: 54,
  });
  const mappingSheet = sheets.get("高职本科相关性映射主表");
  mappingSheet.getRange(`N5:N${mappingRange.lastRow}`).dataValidation = {
    rule: { type: "list", values: policy.relation_levels },
  };
  mappingSheet.getRange(`R5:R${mappingRange.lastRow}`).dataValidation = {
    rule: { type: "list", values: policy.skills_behaviors },
  };
  addEqualsFormatting(mappingSheet.getRange(`N5:N${mappingRange.lastRow}`), "主映射/核心对应", { fill: palette.paleGreen, font: { bold: true, color: palette.navy } });
  addEqualsFormatting(mappingSheet.getRange(`N5:N${mappingRange.lastRow}`), "其他核心对应", { fill: palette.paleBlue, font: { bold: true } });
  addEqualsFormatting(mappingSheet.getRange(`N5:N${mappingRange.lastRow}`), "强相关", { fill: palette.paleGold });
  addEqualsFormatting(mappingSheet.getRange(`N5:N${mappingRange.lastRow}`), "延伸相关", { fill: palette.paleGray });
  addEqualsFormatting(mappingSheet.getRange(`N5:N${mappingRange.lastRow}`), "目录参考", { fill: palette.paleRed, font: { bold: true } });

  writeTableSheet(sheets.get("高职专业反向索引"), {
    title: "高职专科专业反向索引",
    note: "每个高职专业恰好一行；无直接对应和无任何关系均保留显式标注。",
    headers: ["高职专业代码", "高职专业名称", "大类代码", "大类名称", "专业类代码", "专业类名称", "主映射本科代码", "主映射本科名称", "已接受关系数", "映射ID", "无核心直接对应", "无任何可消费关系", "复核状态", "复核说明"],
    rows: bundle.vocational_index.map((row) => [
      row.vocational_code,
      row.vocational_name,
      row.category_code,
      row.category_name,
      row.class_code,
      row.class_name,
      row.primary_undergraduate_code ?? "",
      undergraduateByCode.get(row.primary_undergraduate_code)?.major_name ?? "",
      row.accepted_consumable_count,
      stringify(row.mapping_ids),
      row.zero_direct ? "是" : "否",
      row.zero_all ? "是" : "否",
      row.review_status,
      row.review_note,
    ]),
    tableName: "VocationalReverseIndex",
    widths: [16, 32, 12, 20, 14, 25, 18, 32, 14, 54, 18, 18, 28, 66],
    textColumns: [0, 2, 4, 6],
    wrapColumns: [1, 3, 5, 7, 9, 12, 13],
    centeredColumns: [0, 2, 4, 6, 8, 10, 11],
    freezeColumns: 8,
    rowHeight: 48,
  });

  writeTableSheet(sheets.get("本科专业反向索引"), {
    title: "本科专业反向索引",
    note: "每个本科专业恰好一行；没有高职专科对应的本科专业完整保留并明确标注。",
    headers: ["本科专业代码", "本科专业名称", "门类代码", "门类名称", "专业类代码", "专业类名称", "覆盖状态", "主映射ID", "其他核心ID", "强相关ID", "延伸相关ID", "目录参考ID", "高职专业代码", "关系总数", "无可消费关系"],
    rows: bundle.undergraduate_index.map((row) => [
      row.undergraduate_code,
      row.undergraduate_name,
      row.category_code,
      row.category_name,
      row.class_code,
      row.class_name,
      row.coverage_state,
      stringify(row.mapping_ids_by_level["主映射/核心对应"]),
      stringify(row.mapping_ids_by_level["其他核心对应"]),
      stringify(row.mapping_ids_by_level["强相关"]),
      stringify(row.mapping_ids_by_level["延伸相关"]),
      stringify(row.mapping_ids_by_level["目录参考"]),
      stringify(row.vocational_codes),
      row.mapping_count,
      row.zero_accepted_consumable ? "是" : "否",
    ]),
    tableName: "UndergraduateReverseIndex",
    widths: [16, 32, 12, 18, 14, 25, 30, 48, 48, 56, 44, 40, 42, 13, 16],
    textColumns: [0, 2, 4],
    wrapColumns: [1, 3, 5, 6, 7, 8, 9, 10, 11, 12],
    centeredColumns: [0, 2, 4, 13, 14],
    freezeColumns: 7,
    rowHeight: 50,
  });

  writeTableSheet(sheets.get("专业类映射汇总"), {
    title: "97个高职专科专业类映射汇总",
    note: "专业类统计由811个高职专业的已接受映射重算；Skills领域只作为检索上下文，不作为相关性证据。",
    headers: ["大类代码", "大类名称", "专业类代码", "专业类名称", "高职专业数", "已接受关系数", "可消费关系数", "核心关系数", "关联本科专业数", "无核心专业数", "无任何关系专业数", "Skills领域"],
    rows: bundle.class_aggregation.map((row) => [
      row.category_code,
      row.category_name,
      row.class_code,
      row.class_name,
      row.vocational_major_count,
      row.accepted_mapping_count,
      row.consumable_mapping_count,
      row.core_mapping_count,
      row.distinct_undergraduate_count,
      row.zero_direct_major_count,
      row.zero_all_major_count,
      stringify(row.skills_domains),
    ]),
    tableName: "VocationalClassAggregation",
    widths: [12, 20, 14, 26, 14, 16, 16, 14, 18, 16, 18, 66],
    textColumns: [0, 2],
    wrapColumns: [1, 3, 11],
    centeredColumns: [0, 2, 4, 5, 6, 7, 8, 9, 10],
    freezeColumns: 4,
    rowHeight: 44,
  });

  const ruleRows = [
    ...policy.relation_levels.map((level) => ["关系等级", level, policy.relation_behavior_rules[level], level === "目录参考" ? "不可供 Skills 消费" : "可供 Skills 消费"]),
    ...policy.review_statuses.map((status) => ["复核状态", status, "记录复核结论或待办", "高职专业反向索引与质量清单"]),
    ...policy.relation_bases.map((basis) => ["关系依据", basis, "至少一项，用于解释映射为何成立", "不能仅依据 Skills 领域名称"]),
    ["零映射", "无核心直接对应", "无主映射/其他核心对应，但可保留强相关或延伸相关", "高职专业仍完整保留"],
    ["零映射", "无任何可消费关系", "没有已接受且可消费的关系", "高职专业仍完整保留"],
    ["边界", "专业相关性", "只用于 Skills 标签与检索", "不代表学历、升学、招生或职业资格对应"],
  ];
  writeTableSheet(sheets.get("规则与字段字典"), {
    title: "映射规则与字段字典",
    note: "关系证据以培养对象、知识基础、实践方法、关键技术和职业场景为核心；Skills领域不能单独证明专业相关。",
    headers: ["类型", "字段或取值", "定义", "使用说明"],
    rows: ruleRows,
    tableName: "MappingRuleDictionary",
    widths: [18, 34, 62, 58],
    wrapColumns: [1, 2, 3],
    centeredColumns: [0],
    freezeColumns: 2,
    rowHeight: 44,
  });

  const sourceRows = [
    ...bundle.sources.official_sources.map((source) => [
      source.id,
      source.kind,
      source.title,
      source.publisher,
      source.publication_date,
      source.accessed_at ?? sources.accessed_at,
      source.url,
      source.local_path,
      source.sha256,
      source.applies_to,
    ]),
    [
      "vocational_skills_input",
      "xlsx",
      "高职高专Skills领域分类表",
      "项目输入",
      "",
      bundle.sources.input_manifest.accessed_at,
      "",
      bundle.sources.input_manifest.absolute_path,
      bundle.sources.input_manifest.sha256,
      "高职专业类Skills领域上下文，不作为专业相关性单独证据",
    ],
  ];
  const sourceRange = writeTableSheet(sheets.get("来源台账"), {
    title: "官方目录与输入文件来源台账",
    note: "官方网址、固定快照与SHA-256用于复核来源完整性；本科与高职目录均来自教育部。",
    headers: ["来源ID", "类型", "标题", "发布单位", "发布日期", "访问日期", "官方网址", "本地文件", "SHA-256", "适用范围"],
    rows: sourceRows,
    tableName: "VocationalSourceLedger",
    widths: [30, 12, 48, 28, 16, 16, 72, 58, 68, 48],
    wrapColumns: [0, 2, 3, 6, 7, 8, 9],
    centeredColumns: [1, 4, 5],
    freezeColumns: 3,
    rowHeight: 54,
  });
  sheets.get("来源台账").getRange(`E5:F${sourceRange.lastRow}`).format.numberFormat = "yyyy-mm-dd";

  const qaRows = [
    ...qa.blocking.map((row, index) => [`B-${String(index + 1).padStart(3, "0")}`, "阻断", row.code, row.vocational_code ?? "", row.vocational_name ?? "", row.message]),
    ...qa.review.map((row, index) => [`R-${String(index + 1).padStart(3, "0")}`, "需复核", row.code, row.vocational_code ?? "", row.vocational_name ?? "", row.message]),
    ...qa.notice.map((row, index) => [`N-${String(index + 1).padStart(3, "0")}`, "提示", row.code, row.vocational_code ?? "", row.vocational_name ?? "", row.message]),
  ];
  const qaRange = writeTableSheet(sheets.get("质量复核清单"), {
    title: "质量复核清单",
    note: "阻断项必须为0；需复核与提示项保留给领域专家和后续目录更新使用。",
    headers: ["发现ID", "严重度", "检查代码", "高职专业代码", "高职专业名称", "说明"],
    rows: qaRows,
    tableName: "VocationalMappingQa",
    widths: [14, 14, 34, 18, 34, 92],
    textColumns: [3],
    wrapColumns: [2, 4, 5],
    centeredColumns: [0, 1, 3],
    freezeColumns: 2,
    rowHeight: 54,
  });
  const qaSheet = sheets.get("质量复核清单");
  addEqualsFormatting(qaSheet.getRange(`B5:B${qaRange.lastRow}`), "阻断", { fill: palette.paleRed, font: { bold: true } });
  addEqualsFormatting(qaSheet.getRange(`B5:B${qaRange.lastRow}`), "需复核", { fill: palette.paleGold, font: { bold: true } });
  addEqualsFormatting(qaSheet.getRange(`B5:B${qaRange.lastRow}`), "提示", { fill: palette.paleBlue });

  const summarySheet = sheets.get("统计总览");
  styleTitle(
    summarySheet,
    "高职专科—本科专业 Skills 映射｜统计总览",
    "D",
    "工作簿公式值与聚合器基准并列展示；公式使用有限范围并显式引用工作表。",
  );
  const vocationalLast = bundle.vocational_catalog.length + 4;
  const undergraduateLast = bundle.undergraduate_catalog.length + 4;
  const mappingLast = bundle.mappings.length + 4;
  const vocationalIndexLast = bundle.vocational_index.length + 4;
  const undergraduateIndexLast = bundle.undergraduate_index.length + 4;
  const classLast = bundle.class_aggregation.length + 4;
  const qaLast = qaRows.length + 4;
  const summaryRows = [
    ["高职专科专业数", `=COUNTA('高职专科专业目录'!$E$5:$E$${vocationalLast})`, summary.vocational_count, "完整覆盖811个专业"],
    ["本科专业数", `=COUNTA('本科专业目录_2026'!$E$5:$E$${undergraduateLast})`, summary.undergraduate_count, "完整覆盖883个专业"],
    ["高职专业类数", `=COUNTA('专业类映射汇总'!$C$5:$C$${classLast})`, summary.class_count, "完整覆盖97个专业类"],
    ["正式映射数", `=COUNTA('高职本科相关性映射主表'!$A$5:$A$${mappingLast})`, summary.mapping_count, "只含已接受关系"],
    ["主映射数", `=COUNTIF('高职本科相关性映射主表'!$N$5:$N$${mappingLast},"主映射/核心对应")`, summary.primary_mapping_count, "默认标签"],
    ["其他核心对应", `=COUNTIF('高职本科相关性映射主表'!$N$5:$N$${mappingLast},"其他核心对应")`, summary.relation_level_counts["其他核心对应"], "默认辅助标签"],
    ["强相关", `=COUNTIF('高职本科相关性映射主表'!$N$5:$N$${mappingLast},"强相关")`, summary.relation_level_counts["强相关"], "扩展检索"],
    ["延伸相关", `=COUNTIF('高职本科相关性映射主表'!$N$5:$N$${mappingLast},"延伸相关")`, summary.relation_level_counts["延伸相关"], "跨学科召回"],
    ["高职无核心直接对应", `=COUNTIF('高职专业反向索引'!$K$5:$K$${vocationalIndexLast},"是")`, summary.vocational_zero_direct, "仍可保留强相关/延伸关系"],
    ["高职无任何关系", `=COUNTIF('高职专业反向索引'!$L$5:$L$${vocationalIndexLast},"是")`, summary.vocational_zero_all, "明确保留零映射"],
    ["本科无高职可消费关系", `=COUNTIF('本科专业反向索引'!$O$5:$O$${undergraduateIndexLast},"是")`, summary.undergraduate_zero_consumable, "本科端零映射保留"],
    ["阻断项", `=COUNTIF('质量复核清单'!$B$5:$B$${qaLast},"阻断")`, summary.blocking_count, "交付必须为0"],
    ["专家复核项", `=COUNTIF('质量复核清单'!$B$5:$B$${qaLast},"需复核")`, summary.expert_review_count, "非阻断，保留专家审阅"],
    ["提示项", `=COUNTIF('质量复核清单'!$B$5:$B$${qaLast},"提示")`, summary.notice_count, "目录版本或零映射提示"],
  ];
  summarySheet.getRange("A4:D4").values = [["指标", "工作簿公式值", "聚合器基准", "口径说明"]];
  summarySheet.getRange(`A5:A${summaryRows.length + 4}`).values = summaryRows.map((row) => [row[0]]);
  summarySheet.getRange(`B5:B${summaryRows.length + 4}`).formulas = summaryRows.map((row) => [row[1]]);
  summarySheet.getRange(`C5:D${summaryRows.length + 4}`).values = summaryRows.map((row) => [row[2], row[3]]);
  summarySheet.getRange("A4:D4").format = { fill: palette.teal, font: { bold: true, color: palette.white }, horizontalAlignment: "center" };
  summarySheet.getRange(`A4:D${summaryRows.length + 4}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
  summarySheet.getRange(`A5:A${summaryRows.length + 4}`).format = { fill: palette.paleBlue, font: { bold: true, color: palette.navy } };
  summarySheet.getRange(`B5:C${summaryRows.length + 4}`).format.numberFormat = "#,##0";
  summarySheet.getRange(`B5:C${summaryRows.length + 4}`).format.horizontalAlignment = "right";
  summarySheet.getRange(`D5:D${summaryRows.length + 4}`).format.wrapText = true;
  summarySheet.getRange("A1:A20").format.columnWidth = 34;
  summarySheet.getRange("B1:C20").format.columnWidth = 18;
  summarySheet.getRange("D1:D20").format.columnWidth = 48;
  summarySheet.getRange(`A5:D${summaryRows.length + 4}`).format.rowHeight = 32;
  summarySheet.freezePanes.freezeRows(4);
  summarySheet.tables.add(`A4:D${summaryRows.length + 4}`, true, "VocationalMappingSummary");
  summarySheet.getRange("B5").format = { fill: palette.paleGreen, font: { bold: true, color: palette.navy, size: 14 } };

  return workbook;
}

export async function exportWorkbook(workbook, outputPath = OUTPUT_PATH) {
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  const candidatePath = `${outputPath}.candidate`;
  await fs.rm(candidatePath, { force: true });
  const output = await SpreadsheetFile.exportXlsx(workbook);
  const originalLog = console.log;
  try {
    console.log = () => {};
    await output.save(candidatePath);
  } finally {
    console.log = originalLog;
  }
  await normalizeXlsxPackage(candidatePath);
  let keepExisting = false;
  try {
    const [existing, candidate] = await Promise.all([
      fs.readFile(outputPath),
      fs.readFile(candidatePath),
    ]);
    keepExisting = semanticXlsxDigest(existing) === semanticXlsxDigest(candidate);
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
  if (!keepExisting) await fs.copyFile(candidatePath, outputPath);
  await fs.rm(candidatePath, { force: true });
  await fs.rm(`${candidatePath}.inspect.ndjson`, { force: true });
  await fs.rm(`${outputPath}.inspect.ndjson`, { force: true });
}

async function readJson(filePath) {
  return JSON.parse((await fs.readFile(filePath, "utf8")).replace(/^\uFEFF/, ""));
}

async function main() {
  const [bundle, qa, summary, policy, sources] = await Promise.all([
    readJson(path.join(artifactDir, "mapping_bundle.json")),
    readJson(path.join(artifactDir, "qa_findings.json")),
    readJson(path.join(artifactDir, "summary.json")),
    readJson(path.join(scriptDir, "rules", "mapping_policy.json")),
    readJson(path.join(scriptDir, "source_manifest.json")),
  ]);
  const workbook = buildWorkbook(bundle, qa, summary, policy, sources);
  await exportWorkbook(workbook, OUTPUT_PATH);
  console.log(JSON.stringify({ output: OUTPUT_PATH, sheets: SHEET_NAMES.length, mappings: bundle.mappings.length }));
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url))) {
  await main();
}
