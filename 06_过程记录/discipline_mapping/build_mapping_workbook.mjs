import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

export const OUTPUT_PATH =
  "D:/高校AI工作台/outputs/01a004e5-65dc-7c52-bd8c-7e29e9e058bc/研究生学科与本科专业Skills相关性映射.xlsx";

export const SHEET_NAMES = [
  "使用说明与版本",
  "本科专业目录_2026",
  "研究生学科目录",
  "学科相关性映射主表",
  "本科专业反向索引",
  "研究生学科反向索引",
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
  muted: "#5B6872",
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
  if (Array.isArray(value)) {
    return value
      .map((item) => (typeof item === "object" ? JSON.stringify(item) : String(item)))
      .join("；");
  }
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
  for (const index of textColumns) {
    const letter = columnName(index);
    sheet.getRange(`${letter}5:${letter}${lastRow}`).format.numberFormat = "@";
  }
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

function assertBundle(bundle, sources, policy) {
  if (!bundle || !Array.isArray(bundle.undergraduate) || !Array.isArray(bundle.graduate)) {
    throw new TypeError("mapping bundle is missing catalog arrays");
  }
  if (!Array.isArray(bundle.mappings) || !Array.isArray(bundle.undergraduate_index) || !Array.isArray(bundle.graduate_index)) {
    throw new TypeError("mapping bundle is missing mapping arrays");
  }
  if (!sources || !Array.isArray(sources.sources)) throw new TypeError("source manifest is invalid");
  if (!policy || !Array.isArray(policy.relation_levels)) throw new TypeError("mapping policy is invalid");
}

export function buildWorkbook(bundle, sources, policy) {
  assertBundle(bundle, sources, policy);

  const workbook = Workbook.create();
  const sheets = new Map(SHEET_NAMES.map((name) => [name, workbook.worksheets.add(name)]));
  for (const sheet of sheets.values()) sheet.showGridLines = false;

  const sourceById = new Map(sources.sources.map((source) => [source.id, source]));
  const undergraduateByCode = new Map(bundle.undergraduate.map((item) => [item.major_code, item]));
  const graduateByKey = new Map(bundle.graduate.map((item) => [`${item.object_type}|${item.object_code}`, item]));

  const guide = sheets.get("使用说明与版本");
  styleTitle(
    guide,
    "研究生学科与本科专业 Skills 相关性映射｜使用说明与版本",
    "H",
    "覆盖教育部现行本科专业与研究生学科专业目录；面向 Skills 标签和检索，不构成官方升学、报考或培养对应关系。",
  );
  guide.getRange("A4:B14").values = [
    ["项目", "说明"],
    ["用途", "为高校 AI Skills 提供本科专业与研究生学科的标签、辅助标签、扩展检索和跨学科召回依据。"],
    ["本科范围", `${bundle.summary.undergraduate_count} 种本科专业，来源为《普通高等学校本科专业目录（2026年）》。`],
    ["研究生范围", `${bundle.summary.graduate_count} 个研究生目录对象，包括一级学科和专业学位类别。`],
    ["正式映射", `${bundle.summary.mapping_count} 条已接受关系；候选关系必须经规则复核后才进入主表。`],
    ["零映射保留", "本科与研究生两端均保留没有直接对应的目录对象，零映射不是遗漏。"],
    ["军事学边界", "军事学及明确受限对象只保留目录参考，不进入 Skills 标签、检索或推荐。"],
    ["关系等级", policy.relation_levels.join("、")],
    ["Skills 行为", policy.skills_behaviors.join("、")],
    ["版本", bundle.metadata.schema_version],
    ["生成时间", bundle.metadata.generated_at],
  ];
  guide.getRange("A4:B4").format = { fill: palette.teal, font: { bold: true, color: palette.white } };
  guide.getRange("A4:B14").format.borders = { preset: "all", style: "thin", color: palette.grid };
  guide.getRange("A5:A14").format = { fill: palette.paleBlue, font: { bold: true, color: palette.navy } };
  guide.getRange("B5:B14").format.wrapText = true;
  guide.getRange("A4:A14").format.columnWidth = 22;
  guide.getRange("B4:B14").format.columnWidth = 92;
  guide.getRange("A5:B14").format.rowHeight = 38;
  guide.freezePanes.freezeRows(2);

  const undergraduateRows = bundle.undergraduate.map((item) => {
    const source = sourceById.get(item.source_id);
    return [
      item.category_code,
      item.category_name,
      item.class_code,
      item.class_name,
      item.major_code,
      item.major_name,
      stringify(item.attributes),
      stringify(item.degree_categories),
      item.duration,
      item.source_id,
      source?.url ?? "",
    ];
  });
  writeTableSheet(sheets.get("本科专业目录_2026"), {
    title: "普通高等学校本科专业目录（2026年）",
    note: "完整保留 883 种本科专业；代码按文本保存，来源网址为教育部官方文件。",
    headers: ["门类代码", "门类名称", "专业类代码", "专业类名称", "专业代码", "专业名称", "专业属性", "授予学位门类", "学制", "来源ID", "官方来源网址"],
    rows: undergraduateRows,
    tableName: "UndergraduateCatalog2026",
    widths: [12, 18, 14, 24, 16, 28, 18, 22, 10, 26, 66],
    textColumns: [0, 2, 4],
    wrapColumns: [3, 5, 6, 7, 10],
    centeredColumns: [0, 2, 4, 8],
    freezeColumns: 6,
    rowHeight: 30,
  });

  const graduateRows = bundle.graduate.map((item) => [
    item.category_code,
    item.category_name,
    item.object_type,
    item.object_code,
    item.object_name,
    stringify(item.degree_levels),
    item.status,
    stringify(item.previous_names),
    stringify(item.notes),
    stringify(item.source_ids),
    item.source_ids.map((id) => sourceById.get(id)?.url ?? "").filter(Boolean).join("；"),
  ]);
  writeTableSheet(sheets.get("研究生学科目录"), {
    title: "研究生教育学科专业目录（现行基础与沿革）",
    note: "2022 年目录为现行基础；2025 年对应关系只记录沿革，不反向覆盖现行代码和名称。",
    headers: ["门类代码", "门类名称", "对象类型", "对象代码", "对象名称", "学位层次", "状态", "历史名称与代码", "备注", "来源ID", "官方来源网址"],
    rows: graduateRows,
    tableName: "GraduateCatalogEffective",
    widths: [12, 18, 24, 14, 28, 18, 14, 38, 38, 34, 66],
    textColumns: [0, 3],
    wrapColumns: [2, 4, 5, 7, 8, 9, 10],
    centeredColumns: [0, 3, 6],
    freezeColumns: 5,
    rowHeight: 38,
  });

  const mappingRows = bundle.mappings.map((mapping) => {
    const undergraduate = undergraduateByCode.get(mapping.undergraduate_code);
    const graduate = graduateByKey.get(`${mapping.graduate_type}|${mapping.graduate_code}`);
    return [
      mapping.mapping_id,
      undergraduate.category_code,
      undergraduate.category_name,
      undergraduate.class_code,
      undergraduate.class_name,
      undergraduate.major_code,
      undergraduate.major_name,
      mapping.graduate_type,
      graduate.category_code,
      graduate.category_name,
      mapping.graduate_code,
      graduate.object_name,
      mapping.relation_level,
      mapping.is_primary ? "是" : "否",
      stringify(mapping.relation_basis),
      mapping.rationale,
      mapping.skills_behavior,
      mapping.military_restriction ? "是" : "否",
      mapping.review_status,
      mapping.confidence,
      mapping.generation_method,
    ];
  });
  const mappingRange = writeTableSheet(sheets.get("学科相关性映射主表"), {
    title: "本科专业—研究生学科相关性映射主表",
    note: "仅包含复核后接受的关系；每行保留关系等级、依据、理由、Skills 行为和军事限制等审计字段。",
    headers: ["映射ID", "本科门类代码", "本科门类名称", "本科专业类代码", "本科专业类名称", "本科专业代码", "本科专业名称", "研究生对象类型", "研究生门类代码", "研究生门类名称", "研究生对象代码", "研究生对象名称", "关系等级", "是否主映射", "关系依据", "映射理由", "Skills行为", "军事限制", "复核状态", "置信度", "生成方式"],
    rows: mappingRows,
    tableName: "DisciplineMappings",
    widths: [27, 13, 17, 15, 23, 16, 27, 24, 14, 18, 15, 28, 20, 14, 28, 62, 18, 13, 27, 12, 22],
    textColumns: [0, 1, 3, 5, 8, 10],
    wrapColumns: [4, 6, 7, 11, 12, 14, 15, 16, 18, 20],
    centeredColumns: [1, 3, 5, 8, 10, 13, 17, 19],
    freezeColumns: 7,
    rowHeight: 52,
  });
  const mappingSheet = sheets.get("学科相关性映射主表");
  mappingSheet.getRange(`M5:M${mappingRange.lastRow}`).dataValidation = { rule: { type: "list", values: policy.relation_levels } };
  mappingSheet.getRange(`Q5:Q${mappingRange.lastRow}`).dataValidation = { rule: { type: "list", values: policy.skills_behaviors } };
  mappingSheet.getRange(`S5:S${mappingRange.lastRow}`).dataValidation = { rule: { type: "list", values: policy.review_statuses } };
  mappingSheet.getRange(`T5:T${mappingRange.lastRow}`).dataValidation = { rule: { type: "list", values: policy.confidence_levels } };
  addEqualsFormatting(mappingSheet.getRange(`M5:M${mappingRange.lastRow}`), "主映射/核心对应", { fill: palette.paleGreen, font: { bold: true, color: palette.navy } });
  addEqualsFormatting(mappingSheet.getRange(`M5:M${mappingRange.lastRow}`), "其他核心对应", { fill: palette.paleBlue, font: { bold: true } });
  addEqualsFormatting(mappingSheet.getRange(`M5:M${mappingRange.lastRow}`), "强相关", { fill: palette.paleGold });
  addEqualsFormatting(mappingSheet.getRange(`M5:M${mappingRange.lastRow}`), "延伸相关", { fill: palette.paleGray });
  addEqualsFormatting(mappingSheet.getRange(`M5:M${mappingRange.lastRow}`), "目录参考", { fill: palette.paleRed, font: { bold: true } });
  addEqualsFormatting(mappingSheet.getRange(`S5:S${mappingRange.lastRow}`), "存在歧义，建议学科专家复核", { fill: palette.paleGold, font: { bold: true } });
  addEqualsFormatting(mappingSheet.getRange(`S5:S${mappingRange.lastRow}`), "军事学限制", { fill: palette.paleRed, font: { bold: true } });

  const undergraduateIndexRows = bundle.undergraduate_index.map((item) => [
    item.undergraduate_code,
    item.undergraduate_name,
    item.category_code,
    item.category_name,
    item.class_code,
    item.class_name,
    item.review_status,
    item.review_note,
    item.reviewed_at,
    item.mapping_count,
    item.direct_mapping_count,
    stringify(item.academic_mapping_ids),
    stringify(item.professional_mapping_ids),
    stringify(item.primary_mapping_ids),
    stringify(item.other_core_mapping_ids),
    stringify(item.strong_mapping_ids),
    stringify(item.extended_mapping_ids),
    stringify(item.directory_reference_mapping_ids),
    stringify(item.skills_behaviors),
    stringify(item.zero_mapping_types),
    item.zero_mapping_state,
    item.consumable_mapping_count,
    item.military_reference_count,
  ]);
  const ugIndexRange = writeTableSheet(sheets.get("本科专业反向索引"), {
    title: "本科专业反向索引",
    note: "每个本科专业一行；显式保留两类均有对应、部分类型无直接对应和完全无直接对应状态。",
    headers: ["本科专业代码", "本科专业名称", "门类代码", "门类名称", "专业类代码", "专业类名称", "复核状态", "复核说明", "复核时间", "映射总数", "直接映射数", "学术映射IDs", "专业学位映射IDs", "主映射IDs", "其他核心IDs", "强相关IDs", "延伸相关IDs", "目录参考IDs", "Skills行为", "零映射类型", "零映射状态", "可消费映射数", "军事目录参考数"],
    rows: undergraduateIndexRows,
    tableName: "UndergraduateReverseIndex",
    widths: [16, 28, 12, 18, 15, 24, 27, 68, 25, 12, 13, 48, 48, 48, 38, 42, 38, 42, 24, 24, 25, 16, 17],
    textColumns: [0, 2, 4],
    wrapColumns: [1, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    centeredColumns: [0, 2, 4, 9, 10, 21, 22],
    freezeColumns: 6,
    rowHeight: 48,
  });
  const ugIndexSheet = sheets.get("本科专业反向索引");
  ugIndexSheet.getRange(`G5:G${ugIndexRange.lastRow}`).dataValidation = { rule: { type: "list", values: policy.review_statuses } };
  addEqualsFormatting(ugIndexSheet.getRange(`U5:U${ugIndexRange.lastRow}`), "无合适研究生直接对应", { fill: palette.paleRed, font: { bold: true } });
  addEqualsFormatting(ugIndexSheet.getRange(`U5:U${ugIndexRange.lastRow}`), "部分类型无直接对应", { fill: palette.paleGold });
  addEqualsFormatting(ugIndexSheet.getRange(`G5:G${ugIndexRange.lastRow}`), "存在歧义，建议学科专家复核", { fill: palette.paleGold, font: { bold: true } });

  const graduateIndexRows = bundle.graduate_index.map((item) => [
    item.graduate_type,
    item.graduate_code,
    item.graduate_name,
    item.category_code,
    item.category_name,
    item.reverse_state,
    item.review_note,
    item.reviewed_at,
    item.mapping_count,
    stringify(item.mapping_ids),
    stringify(item.undergraduate_codes),
    stringify(item.primary_mapping_ids),
    stringify(item.core_mapping_ids),
    stringify(item.strong_mapping_ids),
    stringify(item.extended_mapping_ids),
    stringify(item.directory_reference_mapping_ids),
    item.consumable_mapping_count,
    item.military_reference_count,
  ]);
  const gradIndexRange = writeTableSheet(sheets.get("研究生学科反向索引"), {
    title: "研究生学科反向索引",
    note: "每个一级学科或专业学位类别一行；没有本科直接对应的研究生对象仍保留并标注状态。",
    headers: ["研究生对象类型", "对象代码", "对象名称", "门类代码", "门类名称", "反向覆盖状态", "复核说明", "复核时间", "映射总数", "映射IDs", "本科专业代码", "主映射IDs", "核心映射IDs", "强相关IDs", "延伸相关IDs", "目录参考IDs", "可消费映射数", "军事目录参考数"],
    rows: graduateIndexRows,
    tableName: "GraduateReverseIndex",
    widths: [24, 14, 28, 12, 18, 30, 68, 25, 12, 58, 58, 48, 48, 48, 42, 48, 16, 17],
    textColumns: [1, 3],
    wrapColumns: [0, 2, 5, 6, 9, 10, 11, 12, 13, 14, 15],
    centeredColumns: [1, 3, 8, 16, 17],
    freezeColumns: 5,
    rowHeight: 48,
  });
  const gradIndexSheet = sheets.get("研究生学科反向索引");
  addEqualsFormatting(gradIndexSheet.getRange(`F5:F${gradIndexRange.lastRow}`), "已确认无直接对应本科专业", { fill: palette.paleGold, font: { bold: true } });
  addEqualsFormatting(gradIndexSheet.getRange(`F5:F${gradIndexRange.lastRow}`), "军事学限制，仅目录参考", { fill: palette.paleRed, font: { bold: true } });

  const ruleRows = [];
  for (const level of policy.relation_levels) ruleRows.push(["关系等级", level, policy.relation_behavior_rules[level], "关系等级与 Skills 行为的固定对应"]);
  for (const behavior of policy.skills_behaviors) ruleRows.push(["Skills行为", behavior, behavior, "允许的 Skills 消费行为"]);
  for (const status of policy.review_statuses) ruleRows.push(["复核状态", status, status, "允许的复核状态"]);
  for (const confidence of policy.confidence_levels) ruleRows.push(["置信度", confidence, confidence, "允许的置信度"]);
  for (const basis of policy.relation_bases) ruleRows.push(["关系依据", basis, basis, "允许的映射判断依据"]);
  for (const type of policy.graduate_object_types) ruleRows.push(["研究生对象类型", type, type, "研究生目录对象类型"]);
  ruleRows.push(["军事限制", "军事学门类代码", policy.military_category_code, "该门类仅可目录查看"]);
  for (const item of policy.military_restricted_objects ?? []) ruleRows.push(["军事限制", `${item.graduate_type}|${item.graduate_code}`, "显式受限", "跨门类但按军事对象边界处理"]);
  for (const [key, value] of Object.entries(policy.military_rule)) ruleRows.push(["军事限制规则", key, stringify(value), "强制覆盖普通映射行为"]);
  writeTableSheet(sheets.get("规则与字段字典"), {
    title: "映射规则与字段字典",
    note: "公开关系枚举、Skills 行为、复核状态以及军事学安全边界，便于审计和后续维护。",
    headers: ["规则分组", "字段或枚举", "取值或行为", "说明"],
    rows: ruleRows,
    tableName: "MappingPolicyDictionary",
    widths: [24, 38, 34, 62],
    wrapColumns: [0, 1, 2, 3],
    freezeColumns: 1,
    rowHeight: 34,
  });

  const sourceRows = sources.sources.map((source) => [
    source.id,
    source.kind,
    source.title,
    source.publisher,
    source.publication_date,
    source.accessed_at,
    source.url,
    source.local_path,
    source.sha256,
    source.applies_to,
  ]);
  writeTableSheet(sheets.get("来源台账"), {
    title: "官方来源与文件校验台账",
    note: "网址以纯文本保留；SHA-256 对应仓库中的固定快照，用于复核来源完整性。",
    headers: ["来源ID", "类型", "标题", "发布单位", "发布日期", "访问日期", "官方网址", "本地快照", "SHA-256", "适用范围"],
    rows: sourceRows,
    tableName: "OfficialSourceLedger",
    widths: [30, 12, 46, 28, 16, 16, 72, 48, 68, 40],
    wrapColumns: [0, 2, 3, 6, 7, 8, 9],
    centeredColumns: [1, 4, 5],
    freezeColumns: 3,
    rowHeight: 52,
  });

  const qaRows = bundle.qa_findings.map((finding) => [
    finding.finding_id,
    finding.severity,
    finding.check_code,
    finding.category,
    finding.entity_type,
    finding.entity_key,
    finding.message,
    stringify(finding.details),
  ]);
  const qaRange = writeTableSheet(sheets.get("质量复核清单"), {
    title: "质量复核清单",
    note: "包含全部结构化质量发现；当前无阻断项，需复核与提示项继续保留供领域专家审阅。",
    headers: ["发现ID", "严重度", "检查代码", "类别", "对象类型", "对象键", "说明", "详细信息"],
    rows: qaRows,
    tableName: "MappingQaFindings",
    widths: [15, 14, 34, 24, 20, 20, 78, 46],
    textColumns: [5],
    wrapColumns: [2, 3, 4, 6, 7],
    centeredColumns: [0, 1, 5],
    freezeColumns: 2,
    rowHeight: 58,
  });
  const qaSheet = sheets.get("质量复核清单");
  qaSheet.getRange(`B5:B${qaRange.lastRow}`).dataValidation = { rule: { type: "list", values: ["阻断", "需复核", "提示"] } };
  addEqualsFormatting(qaSheet.getRange(`B5:B${qaRange.lastRow}`), "阻断", { fill: palette.paleRed, font: { bold: true, color: "#9C0006" } });
  addEqualsFormatting(qaSheet.getRange(`B5:B${qaRange.lastRow}`), "需复核", { fill: palette.paleGold, font: { bold: true } });
  addEqualsFormatting(qaSheet.getRange(`B5:B${qaRange.lastRow}`), "提示", { fill: palette.paleBlue });

  const summarySheet = sheets.get("统计总览");
  styleTitle(
    summarySheet,
    "研究生学科与本科专业 Skills 映射｜统计总览",
    "D",
    "工作簿公式值与聚合器基准并列展示；公式均使用有限范围并显式引用工作表。",
  );
  const ugLast = bundle.undergraduate.length + 4;
  const gradLast = bundle.graduate.length + 4;
  const mappingLast = bundle.mappings.length + 4;
  const ugIndexLast = bundle.undergraduate_index.length + 4;
  const gradIndexLast = bundle.graduate_index.length + 4;
  const qaLast = bundle.qa_findings.length + 4;
  const summaryRows = [
    ["本科专业数", `=COUNTA('本科专业目录_2026'!$E$5:$E$${ugLast})`, bundle.summary.undergraduate_count, "应完整覆盖 883 种本科专业"],
    ["研究生目录对象数", `=COUNTA('研究生学科目录'!$D$5:$D$${gradLast})`, bundle.summary.graduate_count, "一级学科与专业学位类别合计"],
    ["学术学位一级学科数", `=COUNTIF('研究生学科目录'!$C$5:$C$${gradLast},\"学术学位一级学科\")`, 117, "研究生基础目录基线"],
    ["专业学位类别数", `=COUNTIF('研究生学科目录'!$C$5:$C$${gradLast},\"专业学位类别\")`, 67, "研究生基础目录基线"],
    ["已接受映射数", `=COUNTA('学科相关性映射主表'!$A$5:$A$${mappingLast})`, bundle.summary.mapping_count, "主表仅保留已接受关系"],
    ["本科完全零映射数", `=COUNTIF('本科专业反向索引'!$U$5:$U$${ugIndexLast},\"无合适研究生直接对应\")`, bundle.summary.undergraduate_zero_mapping_count, "两类研究生对象均无直接对应"],
    ["本科无任何已接受关系数", `=COUNTIF('本科专业反向索引'!$J$5:$J$${ugIndexLast},0)`, bundle.summary.undergraduate_no_accepted_mapping_count, "映射总数为零"],
    ["本科部分类型零映射数", `=COUNTIF('本科专业反向索引'!$U$5:$U$${ugIndexLast},\"部分类型无直接对应\")`, bundle.summary.undergraduate_partial_zero_mapping_count, "学术或专业学位一类为空"],
    ["研究生确认零映射数", `=COUNTIF('研究生学科反向索引'!$F$5:$F$${gradIndexLast},\"已确认无直接对应本科专业\")`, bundle.summary.graduate_zero_mapping_count, "明确确认无直接本科对应"],
    ["研究生无已接受关系数", `=COUNTIF('研究生学科反向索引'!$I$5:$I$${gradIndexLast},0)`, bundle.summary.graduate_no_accepted_mapping_count, "映射总数为零，包含受限目录对象"],
    ["军事目录参考关系数", `=COUNTIF('学科相关性映射主表'!$R$5:$R$${mappingLast},\"是\")`, bundle.summary.military_mapping_count, "不得进入 Skills 消费"],
    ["可供 Skills 消费关系数", `=COUNTIF('学科相关性映射主表'!$R$5:$R$${mappingLast},\"否\")`, bundle.summary.consumable_mapping_count, "排除军事目录参考"],
    ["质量发现总数", `=COUNTA('质量复核清单'!$A$5:$A$${qaLast})`, bundle.summary.qa_finding_count, "结构化 QA 发现"],
    ["阻断发现数", `=COUNTIF('质量复核清单'!$B$5:$B$${qaLast},\"阻断\")`, bundle.summary.blocking_finding_count, "必须为零才能交付"],
    ["需复核发现数", `=COUNTIF('质量复核清单'!$B$5:$B$${qaLast},\"需复核\")`, bundle.summary.review_finding_count, "建议领域专家继续审阅"],
    ["提示发现数", `=COUNTIF('质量复核清单'!$B$5:$B$${qaLast},\"提示\")`, bundle.summary.notice_finding_count, "非阻断性说明"],
    ["主映射/核心对应", `=COUNTIF('学科相关性映射主表'!$M$5:$M$${mappingLast},\"主映射/核心对应\")`, bundle.summary.relation_level_counts["主映射/核心对应"], "默认标签"],
    ["其他核心对应", `=COUNTIF('学科相关性映射主表'!$M$5:$M$${mappingLast},\"其他核心对应\")`, bundle.summary.relation_level_counts["其他核心对应"], "默认辅助标签"],
    ["强相关", `=COUNTIF('学科相关性映射主表'!$M$5:$M$${mappingLast},\"强相关\")`, bundle.summary.relation_level_counts["强相关"], "扩展检索"],
    ["延伸相关", `=COUNTIF('学科相关性映射主表'!$M$5:$M$${mappingLast},\"延伸相关\")`, bundle.summary.relation_level_counts["延伸相关"], "跨学科召回"],
    ["目录参考", `=COUNTIF('学科相关性映射主表'!$M$5:$M$${mappingLast},\"目录参考\")`, bundle.summary.relation_level_counts["目录参考"], "仅目录查看"],
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
  summarySheet.getRange("A1:A25").format.columnWidth = 34;
  summarySheet.getRange("B1:C25").format.columnWidth = 18;
  summarySheet.getRange("D1:D25").format.columnWidth = 48;
  summarySheet.getRange(`A5:D${summaryRows.length + 4}`).format.rowHeight = 30;
  summarySheet.freezePanes.freezeRows(4);
  summarySheet.tables.add(`A4:D${summaryRows.length + 4}`, true, "MappingSummary");
  addEqualsFormatting(summarySheet.getRange("B18:B18"), 0, { fill: palette.paleGreen, font: { bold: true, color: palette.navy } });
  summarySheet.getRange("B5").format = { fill: palette.paleGreen, font: { bold: true, color: palette.navy, size: 14 } };

  return workbook;
}

export async function exportWorkbook(workbook, outputPath = OUTPUT_PATH) {
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  const output = await SpreadsheetFile.exportXlsx(workbook);
  await output.save(outputPath);
}

async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, "utf8"));
}

async function main() {
  const [bundle, summary, qaFindings, sources, policy] = await Promise.all([
    readJson(path.join(artifactDir, "mapping_bundle.json")),
    readJson(path.join(artifactDir, "summary.json")),
    readJson(path.join(artifactDir, "qa_findings.json")),
    readJson(path.join(scriptDir, "source_manifest.json")),
    readJson(path.join(scriptDir, "rules", "mapping_policy.json")),
  ]);
  if (JSON.stringify(bundle.summary) !== JSON.stringify(summary)) throw new Error("summary.json does not match mapping_bundle.json");
  if (JSON.stringify(bundle.qa_findings) !== JSON.stringify(qaFindings)) throw new Error("qa_findings.json does not match mapping_bundle.json");
  const workbook = buildWorkbook(bundle, sources, policy);
  await exportWorkbook(workbook, OUTPUT_PATH);
  console.log(JSON.stringify({ output: OUTPUT_PATH, sheets: SHEET_NAMES.length, mappings: bundle.mappings.length }));
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url))) {
  await main();
}
