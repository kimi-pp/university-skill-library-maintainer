import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";


const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(scriptDir, "..", "..");
const dataDir = path.join(projectRoot, "03_候选池", "deduplicated");
const outputDir = process.env.SKILL_RESEARCH_OUTPUT_DIR || path.join(projectRoot, "05_交付物");
const renderDir = path.join(projectRoot, "06_过程记录", "renders", "xlsx");
await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(renderDir, { recursive: true });

const palette = {
  navy: "#16324F",
  teal: "#1F6F8B",
  lightTeal: "#DCEAF0",
  pale: "#F4F7F9",
  gold: "#D59A32",
  ink: "#1F2933",
  muted: "#52606D",
  white: "#FFFFFF",
  grid: "#CBD5E1",
  green: "#DDF3E4",
  amber: "#FFF0C7",
  red: "#FADBD8",
};

const manifest = JSON.parse(await fs.readFile(path.join(dataDir, "manifest.json"), "utf8"));
const requestedCategories = process.argv.slice(2);
const knownCategories = [...new Set(manifest.map((item) => item.category))];
const buildCategories = requestedCategories.length ? requestedCategories : knownCategories;
const invalidCategories = buildCategories.filter((category) => !knownCategories.includes(category));
if (invalidCategories.length) {
  throw new Error(`未知分类：${invalidCategories.join(", ")}`);
}

for (const category of buildCategories) {
  const payload = JSON.parse(await fs.readFile(path.join(dataDir, `category_${category}.json`), "utf8"));
  const records = payload.records;
  const workbook = Workbook.create();
  const guide = workbook.worksheets.add("使用说明");
  const catalog = workbook.worksheets.add("Skill总表");
  const stats = workbook.worksheets.add("分类统计");
  const sources = workbook.worksheets.add("来源清单");
  for (const sheet of [guide, catalog, stats, sources]) {
    sheet.showGridLines = false;
  }

  guide.getRange("A1:H1").merge();
  guide.getRange("A1").values = [[`${payload.category_name}｜GitHub Skill 调研`]];
  guide.getRange("A1:H1").format = {
    fill: palette.navy,
    font: { bold: true, color: palette.white, size: 20 },
    verticalAlignment: "center",
  };
  guide.getRange("A1:H1").format.rowHeight = 38;
  guide.getRange("A2:H2").merge();
  guide.getRange("A2").values = [["独立分类交付物｜仅含入选项｜数据日期 2026-08-06"]];
  guide.getRange("A2:H2").format = {
    fill: palette.lightTeal,
    font: { color: palette.navy, italic: true },
    verticalAlignment: "center",
  };
  guide.getRange("A4:B10").values = [
    ["项目", "说明"],
    ["调研范围", "仅 GitHub；其他平台与市场不在本轮交付范围"],
    ["分类", payload.category_name],
    ["入选数量", records.length],
    ["内容验证", "读取 SKILL.md/README；部分候选进一步检查脚本、references、assets 和仓库结构"],
    ["运行验证", "未安装、未执行；仅在用户另行指令后开展"],
    ["排除项", "不进入本表；仅保存在项目内部归档"],
  ];
  guide.getRange("A4:B4").format = {
    fill: palette.teal,
    font: { bold: true, color: palette.white },
  };
  guide.getRange("A4:B10").format.borders = { preset: "all", style: "thin", color: palette.grid };
  guide.getRange("A5:A10").format = { fill: palette.pale, font: { bold: true, color: palette.navy } };
  guide.getRange("B5:B10").format.wrapText = true;
  guide.getRange("A12:H12").merge();
  guide.getRange("A12").values = [["兼容等级释义"]];
  guide.getRange("A12:H12").format = { fill: palette.navy, font: { bold: true, color: palette.white } };
  guide.getRange("A13:D17").values = [
    ["等级", "含义", "建议", "备注"],
    ["A", "可直接按 Agent Skill/Codex skill 结构使用", "优先试点", "仍需按本校工具和制度补充配置"],
    ["B", "核心工作流可移植，需要替换工具或路径", "列入适配队列", "通常依赖外部 API、脚本或相邻 skill"],
    ["C", "可借鉴，但需明显重写或部署配套服务", "场景验证后再建设", "关注维护、权限与部署成本"],
    ["D", "主要作为方法或模板参考", "按需吸收", "不建议原样接入"],
  ];
  guide.getRange("A13:D13").format = { fill: palette.teal, font: { bold: true, color: palette.white } };
  guide.getRange("A13:D17").format.borders = { preset: "all", style: "thin", color: palette.grid };
  guide.getRange("A13:D17").format.wrapText = true;
  guide.getRange("A:A").format.columnWidth = 18;
  guide.getRange("B:B").format.columnWidth = 72;
  guide.getRange("C:D").format.columnWidth = 28;
  guide.freezePanes.freezeRows(2);

  const headers = [
    "序号", "Skill ID", "Skill名称", "中文定位", "简略功能", "Skill地址", "GitHub仓库", "仓库地址",
    "生态", "来源形态", "功能标签", "适用角色", "典型场景", "兼容等级", "适配建议", "依赖条件",
    "风险与边界", "验证层级", "优先级", "Stars", "最近推送", "许可证",
  ];
  const rows = records.map((row, index) => [
    index + 1, row.id, row.name, row.cn, row.summary, row.skill_url, row.repo, row.repo_url,
    row.ecosystem, row.form, row.tags, row.roles, row.scenario, row.compat, row.adapt, row.deps,
    row.risk, row.verify, row.priority, row.stars, row.repo_pushed, row.license,
  ]);
  const lastCatalogRow = rows.length + 4;
  catalog.getRange("A1:V1").merge();
  catalog.getRange("A1").values = [[`${payload.category_name}｜入选 Skill 总表`]];
  catalog.getRange("A1:V1").format = { fill: palette.navy, font: { bold: true, color: palette.white, size: 18 } };
  catalog.getRange("A1:V1").format.rowHeight = 34;
  catalog.getRange("A2:V2").merge();
  catalog.getRange("A2").values = [[`共 ${records.length} 项；地址为纯文本 GitHub URL；验证不含安装或运行。`]];
  catalog.getRange("A2:V2").format = { fill: palette.lightTeal, font: { color: palette.navy, italic: true } };
  catalog.getRange("A4:V4").values = [headers];
  catalog.getRange(`A5:V${lastCatalogRow}`).values = rows;
  catalog.getRange("A4:V4").format = { fill: palette.teal, font: { bold: true, color: palette.white }, wrapText: true };
  catalog.getRange(`A4:V${lastCatalogRow}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
  catalog.getRange(`A5:V${lastCatalogRow}`).format.verticalAlignment = "top";
  catalog.getRange(`C5:S${lastCatalogRow}`).format.wrapText = true;
  catalog.getRange("A:A").format.columnWidth = 7;
  catalog.getRange("B:B").format.columnWidth = 13;
  catalog.getRange("C:C").format.columnWidth = 22;
  catalog.getRange("D:D").format.columnWidth = 24;
  catalog.getRange("E:E").format.columnWidth = 42;
  catalog.getRange("F:F").format.columnWidth = 55;
  catalog.getRange("G:G").format.columnWidth = 37;
  catalog.getRange("H:H").format.columnWidth = 46;
  catalog.getRange("I:J").format.columnWidth = 30;
  catalog.getRange("K:Q").format.columnWidth = 34;
  catalog.getRange("R:S").format.columnWidth = 15;
  catalog.getRange("T:T").format.columnWidth = 11;
  catalog.getRange("U:U").format.columnWidth = 14;
  catalog.getRange("V:V").format.columnWidth = 20;
  catalog.getRange(`A5:B${lastCatalogRow}`).format.horizontalAlignment = "center";
  catalog.getRange(`N5:N${lastCatalogRow}`).format.horizontalAlignment = "center";
  catalog.getRange(`R5:U${lastCatalogRow}`).format.horizontalAlignment = "center";
  catalog.getRange(`A5:V${lastCatalogRow}`).format.rowHeight = 58;
  catalog.getRange("A4:V4").format.rowHeight = 32;
  catalog.freezePanes.freezeRows(4);
  catalog.freezePanes.freezeColumns(4);
  catalog.tables.add(`A4:V${lastCatalogRow}`, true, `SkillTable${category}`);
  catalog.getRange(`N5:N${lastCatalogRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"A"', format: { fill: palette.green, font: { bold: true, color: palette.navy } } });
  catalog.getRange(`N5:N${lastCatalogRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"B"', format: { fill: palette.lightTeal } });
  catalog.getRange(`N5:N${lastCatalogRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"C"', format: { fill: palette.amber } });
  catalog.getRange(`S5:S${lastCatalogRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"高"', format: { fill: palette.green, font: { bold: true } } });

  const uniqueRepos = [...new Set(records.map((row) => row.repo))].sort();
  const repoRows = uniqueRepos.map((repo) => {
    const sample = records.find((row) => row.repo === repo);
    return [repo, sample.repo_url, sample.stars, sample.repo_pushed, sample.license, null, sample.form];
  });
  const lastSourceRow = repoRows.length + 4;
  sources.getRange("A1:G1").merge();
  sources.getRange("A1").values = [[`${payload.category_name}｜GitHub 来源清单`]];
  sources.getRange("A1:G1").format = { fill: palette.navy, font: { bold: true, color: palette.white, size: 18 } };
  sources.getRange("A2:G2").merge();
  sources.getRange("A2").values = [["同一仓库可能包含多个入选 skill；许可证需以具体目录和当前仓库文件为准。"]];
  sources.getRange("A2:G2").format = { fill: palette.lightTeal, font: { color: palette.navy, italic: true } };
  sources.getRange("A4:G4").values = [["GitHub仓库", "仓库地址", "Stars", "最近推送", "许可证", "入选Skill数", "来源形态"]];
  sources.getRange(`A5:G${lastSourceRow}`).values = repoRows;
  const sourceFormulas = uniqueRepos.map((_, index) => [`=COUNTIF('Skill总表'!$G$5:$G$${lastCatalogRow},A${index + 5})`]);
  sources.getRange(`F5:F${lastSourceRow}`).formulas = sourceFormulas;
  sources.getRange("A4:G4").format = { fill: palette.teal, font: { bold: true, color: palette.white }, wrapText: true };
  sources.getRange(`A4:G${lastSourceRow}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
  sources.getRange(`A5:G${lastSourceRow}`).format.wrapText = true;
  sources.getRange(`A5:G${lastSourceRow}`).format.verticalAlignment = "top";
  sources.getRange("A:A").format.columnWidth = 40;
  sources.getRange("B:B").format.columnWidth = 50;
  sources.getRange("C:C").format.columnWidth = 12;
  sources.getRange("D:D").format.columnWidth = 15;
  sources.getRange("E:E").format.columnWidth = 22;
  sources.getRange("F:F").format.columnWidth = 14;
  sources.getRange("G:G").format.columnWidth = 34;
  sources.freezePanes.freezeRows(4);
  sources.tables.add(`A4:G${lastSourceRow}`, true, `SourceTable${category}`);

  const ecosystems = [...new Set(records.map((row) => row.ecosystem))].sort();
  stats.getRange("A1:J1").merge();
  stats.getRange("A1").values = [[`${payload.category_name}｜结构统计`]];
  stats.getRange("A1:J1").format = { fill: palette.navy, font: { bold: true, color: palette.white, size: 18 } };
  stats.getRange("A3:B3").values = [["核心指标", "数量"]];
  stats.getRange("A4:A9").values = [["入选Skill"], ["优先级：高"], ["优先级：中"], ["二级包内容验证"], ["说明已核验"], ["独立仓库"]];
  stats.getRange("B4:B9").formulas = [
    [`=COUNTA('Skill总表'!$B$5:$B$${lastCatalogRow})`],
    [`=COUNTIF('Skill总表'!$S$5:$S$${lastCatalogRow},"高")`],
    [`=COUNTIF('Skill总表'!$S$5:$S$${lastCatalogRow},"中")`],
    [`=COUNTIF('Skill总表'!$R$5:$R$${lastCatalogRow},"二级包内容验证")`],
    [`=COUNTIF('Skill总表'!$R$5:$R$${lastCatalogRow},"说明已核验")`],
    [`=COUNTA('来源清单'!$A$5:$A$${lastSourceRow})`],
  ];
  stats.getRange("A12:B12").values = [["兼容等级", "数量"]];
  stats.getRange("A13:A16").values = [["A"], ["B"], ["C"], ["D"]];
  stats.getRange("B13:B16").formulas = ["A", "B", "C", "D"].map((grade) => [`=COUNTIF('Skill总表'!$N$5:$N$${lastCatalogRow},"${grade}")`]);
  stats.getRange("F3:G3").values = [["独立标注的生态", "数量"]];
  stats.getRange(`F4:F${ecosystems.length + 3}`).values = ecosystems.map((item) => [item]);
  stats.getRange(`G4:G${ecosystems.length + 3}`).formulas = ecosystems.map((_, index) => [`=COUNTIF('Skill总表'!$I$5:$I$${lastCatalogRow},F${index + 4})`]);
  for (const headerRange of ["A3:B3", "A12:B12", "F3:G3"]) {
    stats.getRange(headerRange).format = { fill: palette.teal, font: { bold: true, color: palette.white } };
  }
  stats.getRange("A3:B9").format.borders = { preset: "all", style: "thin", color: palette.grid };
  stats.getRange("A12:B16").format.borders = { preset: "all", style: "thin", color: palette.grid };
  stats.getRange(`F3:G${ecosystems.length + 3}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
  stats.getRange(`F3:G${ecosystems.length + 3}`).format.wrapText = true;
  stats.getRange("A:A").format.columnWidth = 27;
  stats.getRange("B:B").format.columnWidth = 12;
  stats.getRange("F:F").format.columnWidth = 60;
  stats.getRange("G:G").format.columnWidth = 12;
  stats.getRange("B4:B16").format.numberFormat = "0";
  stats.getRange(`G4:G${ecosystems.length + 3}`).format.numberFormat = "0";
  const chart = stats.charts.add("bar", stats.getRange("A12:B16"));
  chart.title = "兼容等级分布";
  chart.hasLegend = false;
  const chartStartRow = Math.max(11, ecosystems.length + 5);
  chart.setPosition(`D${chartStartRow}`, `J${chartStartRow + 14}`);
  stats.freezePanes.freezeRows(1);

  const outputItem = manifest.find((item) => item.category === category && item.format === "xlsx");
  const outputPath = path.join(outputDir, outputItem.path);
  const xlsx = await SpreadsheetFile.exportXlsx(workbook);
  await xlsx.save(outputPath);

  const sheetNames = ["使用说明", "Skill总表", "分类统计", "来源清单"];
  for (const sheetName of sheetNames) {
    const preview = await workbook.render({ sheetName, autoCrop: "all", scale: sheetName === "Skill总表" ? 0.65 : 1, format: "png" });
    await fs.writeFile(path.join(renderDir, `${category}_${sheetName}.png`), new Uint8Array(await preview.arrayBuffer()));
  }

  const inspect = await workbook.inspect({
    kind: "formula,region",
    sheetId: "分类统计",
    range: "A1:J30",
    maxChars: 6000,
    options: { maxResults: 100 },
  });
  await fs.writeFile(path.join(renderDir, `${category}_inspect.ndjson`), inspect.ndjson ?? String(inspect), "utf8");
  console.log(`${category}: ${records.length} skills -> ${outputPath}`);
}
