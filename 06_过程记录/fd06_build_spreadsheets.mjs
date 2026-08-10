import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";


const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(scriptDir, "..");
const catalogPath = path.join(scriptDir, "fd06_catalog.json");
const deliveryRoot = path.join(projectRoot, "05_交付物", "06_课程设计、教学材料与教学评估_全网公开技能调研");
const renderRoot = path.join(scriptDir, "fd06_artifacts", "xlsx_renders");
await fs.mkdir(deliveryRoot, { recursive: true });
await fs.mkdir(renderRoot, { recursive: true });

const catalog = JSON.parse(await fs.readFile(catalogPath, "utf8"));
const categories = [
  ["06-01", "课程体系、目标与能力设计"],
  ["06-02", "教学大纲、教案与课时规划"],
  ["06-03", "讲义、课件与阅读材料"],
  ["06-04", "案例、实验、讨论与课堂活动"],
  ["06-05", "作业、测验与考试命题"],
  ["06-06", "作业批改与形成性反馈"],
  ["06-07", "评分量规与评价方案"],
  ["06-08", "考试评卷、成绩分析与学情诊断"],
  ["06-09", "个性化、无障碍与多语言教学适配"],
  ["06-10", "课程质量、教学反思与持续改进"],
  ["06-11", "课程论文与毕业论文评阅"],
  ["06-12", "期刊与会议论文同行评审"],
];
const categoryName = new Map(categories);

const palette = {
  navy: "#17324D",
  teal: "#187B80",
  paleTeal: "#DDEEEF",
  paleBlue: "#E8EEF5",
  paleGold: "#FFF3D6",
  paleRed: "#FBE5E1",
  paleGreen: "#E0F1E7",
  ink: "#22313F",
  muted: "#5B6872",
  white: "#FFFFFF",
  grid: "#C9D2DA",
};

const deliveries = [
  {
    key: "00",
    title: "课程设计、教学材料与教学评估｜大分类总览",
    records: catalog,
    outputPath: path.join(deliveryRoot, "00_大分类总览.xlsx"),
  },
  ...categories.map(([code, name]) => ({
    key: code,
    title: `${code} ${name}`,
    records: catalog.filter((item) => item.primary_subcategory === code),
    outputPath: path.join(deliveryRoot, `${code}_${name}`, `${code}_技能清单.xlsx`),
  })),
];

function unique(values) {
  return [...new Set(values)].sort((a, b) => String(a).localeCompare(String(b), "zh-CN"));
}

function sourceRows(records) {
  const groups = new Map();
  for (const item of records) {
    const key = `${item.repository}\u0000${item.source_label}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(item);
  }
  return [...groups.values()]
    .sort((a, b) => a[0].repository.localeCompare(b[0].repository, "en"))
    .map((items) => {
      const sample = items[0];
      const grades = unique(items.map((item) => item.security_grade)).join("、");
      return [
        sample.repository,
        sample.source_label,
        sample.maintainer,
        unique(items.map((item) => item.license)).join("、"),
        unique(items.map((item) => item.fixed_version)).length,
        null,
        grades,
        sample.canonical_url,
      ];
    });
}

function styleTitle(sheet, title, columns) {
  sheet.getRange(`A1:${columns}1`).merge();
  sheet.getRange("A1").values = [[title]];
  sheet.getRange(`A1:${columns}1`).format = {
    fill: palette.navy,
    font: { bold: true, color: palette.white, size: 18 },
    verticalAlignment: "center",
  };
  sheet.getRange(`A1:${columns}1`).format.rowHeight = 36;
}

async function buildWorkbook(delivery) {
  const records = delivery.records;
  const workbook = Workbook.create();
  const guide = workbook.worksheets.add("使用说明");
  const skills = workbook.worksheets.add("AI技能清单");
  const stats = workbook.worksheets.add("分类统计");
  const sources = workbook.worksheets.add("来源清单");
  for (const sheet of [guide, skills, stats, sources]) sheet.showGridLines = false;

  styleTitle(guide, `${delivery.title}｜使用说明`, "H");
  guide.getRange("A2:H2").merge();
  guide.getRange("A2").values = [["全网公开来源｜仅含通过静态安全准入的正式技能｜核验日期截至 2026-08-09"]];
  guide.getRange("A2:H2").format = { fill: palette.paleTeal, font: { color: palette.navy, italic: true } };
  guide.getRange("A4:B12").values = [
    ["项目", "通俗说明"],
    ["本表用途", "帮助教师、助教、教学管理人员、导师和评审人员按实际任务筛选可参考的 AI 技能。"],
    ["正式数量", records.length],
    ["收录范围", delivery.key === "00" ? "FD06 大分类的十二个小分类。" : delivery.title],
    ["来源范围", "全网公开来源，包括 GitHub、Hugging Face Space、ClawHub 等公开平台。"],
    ["安全检查", "逐项固定版本读取说明、许可证和包内文件，并做静态安全审查。"],
    ["运行状态", "未安装、未运行；只有用户另行明确指令后才可开展运行验证。"],
    ["不含内容", "落选、重复、SC 和 SX 条目不进入本工作簿。"],
    ["重要边界", "涉及成绩、学生权益、未公开论文、个人信息或最终评价决定时，必须由有权限人员复核。"],
  ];
  guide.getRange("A4:B4").format = { fill: palette.teal, font: { bold: true, color: palette.white } };
  guide.getRange("A4:B12").format.borders = { preset: "all", style: "thin", color: palette.grid };
  guide.getRange("A5:A12").format = { fill: palette.paleBlue, font: { bold: true, color: palette.navy } };
  guide.getRange("B5:B12").format.wrapText = true;
  guide.getRange("A14:H14").merge();
  guide.getRange("A14").values = [["安全等级与采用建议"]];
  guide.getRange("A14:H14").format = { fill: palette.navy, font: { bold: true, color: palette.white } };
  guide.getRange("A15:D18").values = [
    ["等级", "本次建议", "通俗含义", "使用前应做什么"],
    ["SA", "可直接使用", "静态检查未发现阻断性问题。", "仍需按本校制度和实际任务复核输出。"],
    ["SB", "需要少量调整", "基本可用，但要替换少量工具、路径、模板或规则。", "完成列出的调整并进行人工复核。"],
    ["SB-A", "需要重新改造", "原项目不能直接接入学校环境。", "先删除或改写高风险步骤，再单独测试和审批。"],
  ];
  guide.getRange("A15:D15").format = { fill: palette.teal, font: { bold: true, color: palette.white } };
  guide.getRange("A15:D18").format.borders = { preset: "all", style: "thin", color: palette.grid };
  guide.getRange("A15:D18").format.wrapText = true;
  guide.getRange("A:A").format.columnWidth = 19;
  guide.getRange("B:B").format.columnWidth = 78;
  guide.getRange("C:D").format.columnWidth = 32;
  guide.freezePanes.freezeRows(2);

  const headers = [
    "序号", "Skill ID", "Skill名称", "主要小分类", "简略功能", "适用对象", "典型场景", "需要准备", "可得到",
    "采用建议", "安全等级", "安全说明", "许可证", "来源平台", "维护者", "仓库或项目", "固定版本", "核验日期", "地址",
  ];
  const rows = records.map((item, index) => [
    index + 1,
    item.skill_id,
    item.name,
    `${item.primary_subcategory} ${item.subcategory_name}`,
    item.plain_function,
    item.audience.join("、"),
    item.when_to_use,
    item.inputs,
    item.outputs,
    item.adoption_level,
    item.security_grade,
    item.security_plain,
    item.license,
    item.source_label,
    item.maintainer,
    item.repository,
    item.fixed_version,
    item.verified_at,
    item.canonical_url,
  ]);
  const lastSkillRow = rows.length + 4;
  styleTitle(skills, `${delivery.title}｜正式 AI 技能清单`, "S");
  skills.getRange("A2:S2").merge();
  skills.getRange("A2").values = [[`共 ${records.length} 项；所有功能说明均采用非计算机背景用户可直接理解的表述。`]];
  skills.getRange("A2:S2").format = { fill: palette.paleTeal, font: { color: palette.navy, italic: true } };
  skills.getRange("A4:S4").values = [headers];
  skills.getRange(`A5:S${lastSkillRow}`).values = rows;
  skills.getRange("A4:S4").format = { fill: palette.teal, font: { bold: true, color: palette.white }, wrapText: true };
  skills.getRange(`A4:S${lastSkillRow}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
  skills.getRange(`A5:S${lastSkillRow}`).format.verticalAlignment = "top";
  skills.getRange(`C5:S${lastSkillRow}`).format.wrapText = true;
  skills.getRange(`A5:B${lastSkillRow}`).format.horizontalAlignment = "center";
  skills.getRange(`J5:K${lastSkillRow}`).format.horizontalAlignment = "center";
  skills.getRange(`Q5:R${lastSkillRow}`).format.horizontalAlignment = "center";
  skills.getRange(`A5:S${lastSkillRow}`).format.rowHeight = 64;
  skills.getRange("A4:S4").format.rowHeight = 34;
  const widths = [7, 14, 25, 28, 48, 25, 46, 38, 38, 16, 12, 48, 18, 28, 22, 32, 24, 14, 58];
  widths.forEach((width, index) => {
    const letter = String.fromCharCode(65 + index);
    skills.getRange(`${letter}:${letter}`).format.columnWidth = width;
  });
  skills.freezePanes.freezeRows(4);
  skills.freezePanes.freezeColumns(3);
  const tableSuffix = delivery.key.replace(/\D/g, "") || "00";
  skills.tables.add(`A4:S${lastSkillRow}`, true, `FD06Skills${tableSuffix}`);
  skills.getRange(`K5:K${lastSkillRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"SA"', format: { fill: palette.paleGreen, font: { bold: true } } });
  skills.getRange(`K5:K${lastSkillRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"SB"', format: { fill: palette.paleGold, font: { bold: true } } });
  skills.getRange(`K5:K${lastSkillRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"SB-A"', format: { fill: palette.paleRed, font: { bold: true } } });

  const repos = sourceRows(records);
  const lastSourceRow = repos.length + 4;
  styleTitle(sources, `${delivery.title}｜公开来源清单`, "H");
  sources.getRange("A2:H2").merge();
  sources.getRange("A2").values = [["同一来源可能包含多个技能；正式技能数由 AI技能清单自动统计。"]];
  sources.getRange("A2:H2").format = { fill: palette.paleTeal, font: { color: palette.navy, italic: true } };
  sources.getRange("A4:H4").values = [["来源项目", "来源平台", "维护者", "许可证", "固定版本数", "正式技能数", "安全等级", "示例地址"]];
  sources.getRange(`A5:H${lastSourceRow}`).values = repos;
  sources.getRange(`F5:F${lastSourceRow}`).formulas = repos.map((_, index) => [`=COUNTIF('AI技能清单'!$P$5:$P$${lastSkillRow},A${index + 5})`]);
  sources.getRange("A4:H4").format = { fill: palette.teal, font: { bold: true, color: palette.white }, wrapText: true };
  sources.getRange(`A4:H${lastSourceRow}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
  sources.getRange(`A5:H${lastSourceRow}`).format.wrapText = true;
  sources.getRange(`A5:H${lastSourceRow}`).format.verticalAlignment = "top";
  [38, 27, 22, 22, 15, 15, 18, 58].forEach((width, index) => {
    const letter = String.fromCharCode(65 + index);
    sources.getRange(`${letter}:${letter}`).format.columnWidth = width;
  });
  sources.getRange(`E5:G${lastSourceRow}`).format.horizontalAlignment = "center";
  sources.freezePanes.freezeRows(4);
  sources.tables.add(`A4:H${lastSourceRow}`, true, `FD06Sources${tableSuffix}`);

  const categoryRows = delivery.key === "00" ? categories : categories.filter(([code]) => code === delivery.key);
  const platforms = unique(records.map((item) => item.source_label));
  const licenses = unique(records.map((item) => item.license));
  styleTitle(stats, `${delivery.title}｜分类统计`, "K");
  stats.getRange("A3:B3").values = [["核心指标", "数量"]];
  stats.getRange("A4:A10").values = [["正式技能总数"], ["安全等级 SA"], ["安全等级 SB"], ["安全等级 SB-A"], ["可直接使用"], ["需要少量调整"], ["需要重新改造"]];
  stats.getRange("B4:B10").formulas = [
    [`=COUNTA('AI技能清单'!$B$5:$B$${lastSkillRow})`],
    [`=COUNTIF('AI技能清单'!$K$5:$K$${lastSkillRow},"SA")`],
    [`=COUNTIF('AI技能清单'!$K$5:$K$${lastSkillRow},"SB")`],
    [`=COUNTIF('AI技能清单'!$K$5:$K$${lastSkillRow},"SB-A")`],
    [`=COUNTIF('AI技能清单'!$J$5:$J$${lastSkillRow},"可直接使用")`],
    [`=COUNTIF('AI技能清单'!$J$5:$J$${lastSkillRow},"需要少量调整")`],
    [`=COUNTIF('AI技能清单'!$J$5:$J$${lastSkillRow},"需要重新改造")`],
  ];
  stats.getRange("D3:E3").values = [["主要小分类", "数量"]];
  stats.getRange(`D4:D${categoryRows.length + 3}`).values = categoryRows.map(([code, name]) => [`${code} ${name}`]);
  stats.getRange(`E4:E${categoryRows.length + 3}`).formulas = categoryRows.map((_, index) => [`=COUNTIF('AI技能清单'!$D$5:$D$${lastSkillRow},D${index + 4})`]);
  stats.getRange("G3:H3").values = [["来源平台", "数量"]];
  stats.getRange(`G4:G${platforms.length + 3}`).values = platforms.map((item) => [item]);
  stats.getRange(`H4:H${platforms.length + 3}`).formulas = platforms.map((_, index) => [`=COUNTIF('AI技能清单'!$N$5:$N$${lastSkillRow},G${index + 4})`]);
  stats.getRange("J3:K3").values = [["许可证", "数量"]];
  stats.getRange(`J4:J${licenses.length + 3}`).values = licenses.map((item) => [item]);
  stats.getRange(`K4:K${licenses.length + 3}`).formulas = licenses.map((_, index) => [`=COUNTIF('AI技能清单'!$M$5:$M$${lastSkillRow},J${index + 4})`]);
  for (const range of ["A3:B3", "D3:E3", "G3:H3", "J3:K3"]) stats.getRange(range).format = { fill: palette.teal, font: { bold: true, color: palette.white } };
  stats.getRange("A3:B10").format.borders = { preset: "all", style: "thin", color: palette.grid };
  stats.getRange(`D3:E${categoryRows.length + 3}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
  stats.getRange(`G3:H${platforms.length + 3}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
  stats.getRange(`J3:K${licenses.length + 3}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
  stats.getRange("A:A").format.columnWidth = 25;
  stats.getRange("B:B").format.columnWidth = 12;
  stats.getRange("D:D").format.columnWidth = 44;
  stats.getRange("E:E").format.columnWidth = 12;
  stats.getRange("G:G").format.columnWidth = 33;
  stats.getRange("H:H").format.columnWidth = 12;
  stats.getRange("J:J").format.columnWidth = 28;
  stats.getRange("K:K").format.columnWidth = 12;
  stats.freezePanes.freezeRows(1);

  await fs.mkdir(path.dirname(delivery.outputPath), { recursive: true });
  const xlsx = await SpreadsheetFile.exportXlsx(workbook);
  await xlsx.save(delivery.outputPath);

  const renderPrefix = delivery.key.replace("-", "_");
  for (const sheetName of ["使用说明", "AI技能清单", "分类统计", "来源清单"]) {
    const preview = await workbook.render({
      sheetName,
      autoCrop: "all",
      scale: sheetName === "AI技能清单" ? (delivery.key === "00" ? 0.42 : 0.58) : 0.85,
      format: "png",
    });
    await fs.writeFile(path.join(renderRoot, `${renderPrefix}_${sheetName}.png`), new Uint8Array(await preview.arrayBuffer()));
  }

  const inspection = await workbook.inspect({
    kind: "formula,region",
    sheetId: "分类统计",
    range: "A1:K30",
    maxChars: 8000,
    options: { maxResults: 200 },
  });
  await fs.writeFile(path.join(renderRoot, `${renderPrefix}_inspect.ndjson`), inspection.ndjson ?? String(inspection), "utf8");
  const automaticInspection = `${delivery.outputPath}.inspect.ndjson`;
  try {
    await fs.rename(automaticInspection, path.join(renderRoot, `${renderPrefix}_export.inspect.ndjson`));
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
  console.log(`${delivery.key}: ${records.length} skills -> ${delivery.outputPath}`);
}

for (const delivery of deliveries) await buildWorkbook(delivery);

await fs.writeFile(
  path.join(deliveryRoot, "MANIFEST.json"),
  JSON.stringify(deliveries.map((item) => ({ key: item.key, title: item.title, count: item.records.length, path: item.outputPath })), null, 2) + "\n",
  "utf8",
);
