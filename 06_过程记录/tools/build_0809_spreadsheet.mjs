import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(scriptDir, "..", "..");
const dataPath = path.join(projectRoot, "03_候选池", "deduplicated", "0809_computer_science.json");
const outputDir = path.join(projectRoot, "05_交付物");
const renderDir = path.join(projectRoot, "06_过程记录", "renders", "0809_xlsx");
await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(renderDir, { recursive: true });

const payload = JSON.parse(await fs.readFile(dataPath, "utf8"));
const records = payload.records;
const majors = [
  ["080901K", "计算机科学与技术"], ["080902", "软件工程"], ["080903", "网络工程"],
  ["080904K", "信息安全"], ["080905T", "物联网工程"], ["080906T", "数字媒体技术"],
  ["080907T", "智能科学与技术"], ["080908T", "空间信息与数字技术"],
  ["080909T", "电子与计算机工程"], ["080910T", "数据科学与大数据技术"],
  ["080911T", "网络空间安全"], ["080912T", "新媒体技术"], ["080913T", "电影制作"],
  ["080914T", "保密管理"],
];
const groups = ["A 计算基础", "B 软件工程", "C 网络安全", "D 物联网", "E AI与数据", "F 空间信息", "G 数字媒体", "H 保密治理"];
const platforms = [...new Set(records.map((row) => row.platform))].sort();
const repositories = [...new Set(records.map((row) => row.repo))].sort();

const palette = {
  navy: "#18324A", teal: "#167D89", blue: "#2E74B5", paleBlue: "#EAF2F8", paleTeal: "#E8F3F4",
  pale: "#F6F8FA", ink: "#18212B", muted: "#536273", white: "#FFFFFF", grid: "#C9D3DC",
  green: "#DDF3E4", greenInk: "#176B3A", amber: "#FFF0C7", amberInk: "#8A5A00",
  orange: "#FBE1D1", orangeInk: "#9A3412", red: "#FADBD8", gray: "#E5E7EB",
};

const workbook = Workbook.create();
const overview = workbook.worksheets.add("总览");
const catalog = workbook.worksheets.add("技能清单");
const coverage = workbook.worksheets.add("专业覆盖");
const mapping = workbook.worksheets.add("专业映射");
const sources = workbook.worksheets.add("来源仓库");
const rules = workbook.worksheets.add("规则与说明");
for (const sheet of [overview, catalog, coverage, mapping, sources, rules]) sheet.showGridLines = false;

const headers = [
  "序号", "Skill ID", "能力群", "中文名称", "英文名称", "来源平台", "来源仓库", "Skill地址",
  "简略功能", "覆盖专业", "覆盖类型", "安全等级", "准入形式", "执行行为", "网络与数据行为",
  "安全限制", "适配保留", "适配剥离", "优先级", "许可证", "审查提交", "提交日期", "审查日期",
  "包文件数", "脚本数", "静态验证结论",
];
const rows = records.map((row, index) => [
  index + 1, row.id, row.primary_group, row.cn_name, row.name, row.platform, row.repo, row.skill_url,
  row.summary, row.majors.join("、"), row.coverage_type, row.security_grade, row.admission_form,
  row.executable_behavior, row.network_data_behavior, row.security_restrictions, row.adapt_keep, row.adapt_strip,
  row.priority, row.license, row.review_commit, row.review_commit_date, row.review_date, row.package_files,
  row.script_files, row.verification,
]);
const lastCatalogRow = rows.length + 4;

catalog.getRange("A1:Z1").merge();
catalog.getRange("A1").values = [["0809 计算机类｜跨平台开源 Skill 正式清单"]];
catalog.getRange("A1:Z1").format = { fill: palette.navy, font: { bold: true, color: palette.white, size: 19 }, verticalAlignment: "center" };
catalog.getRange("A1:Z1").format.rowHeight = 38;
catalog.getRange("A2:Z2").merge();
catalog.getRange("A2").values = [["仅含通过静态准入的 88 项；原始包未安装、未运行。SB-A 只能采用剥离危险部分后的适配版。"]];
catalog.getRange("A2:Z2").format = { fill: palette.paleTeal, font: { color: palette.navy, italic: true }, verticalAlignment: "center" };
catalog.getRange("A4:Z4").values = [headers];
catalog.getRange(`A5:Z${lastCatalogRow}`).values = rows;
catalog.getRange("A4:Z4").format = { fill: palette.teal, font: { bold: true, color: palette.white }, wrapText: true, verticalAlignment: "center" };
catalog.getRange(`A4:Z${lastCatalogRow}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
catalog.getRange(`A5:Z${lastCatalogRow}`).format.verticalAlignment = "top";
catalog.getRange(`C5:Z${lastCatalogRow}`).format.wrapText = true;
catalog.getRange(`A5:B${lastCatalogRow}`).format.horizontalAlignment = "center";
catalog.getRange(`F5:F${lastCatalogRow}`).format.horizontalAlignment = "center";
catalog.getRange(`K5:M${lastCatalogRow}`).format.horizontalAlignment = "center";
catalog.getRange(`S5:Y${lastCatalogRow}`).format.horizontalAlignment = "center";
catalog.getRange(`A5:Z${lastCatalogRow}`).format.rowHeight = 74;
catalog.getRange("A4:Z4").format.rowHeight = 34;
const widths = {
  A: 7, B: 17, C: 18, D: 24, E: 28, F: 14, G: 32, H: 58, I: 42, J: 46, K: 22, L: 12, M: 17,
  N: 35, O: 42, P: 52, Q: 44, R: 47, S: 12, T: 16, U: 34, V: 14, W: 14, X: 11, Y: 9, Z: 34,
};
for (const [column, width] of Object.entries(widths)) catalog.getRange(`${column}:${column}`).format.columnWidth = width;
catalog.freezePanes.freezeRows(4);
catalog.freezePanes.freezeColumns(5);
catalog.tables.add(`A4:Z${lastCatalogRow}`, true, "ComputerScienceSkillTable");
catalog.getRange(`L5:L${lastCatalogRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"SA"', format: { fill: palette.green, font: { bold: true, color: palette.greenInk } } });
catalog.getRange(`L5:L${lastCatalogRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"SB"', format: { fill: palette.amber, font: { bold: true, color: palette.amberInk } } });
catalog.getRange(`L5:L${lastCatalogRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"SB-A"', format: { fill: palette.orange, font: { bold: true, color: palette.orangeInk } } });
catalog.getRange(`S5:S${lastCatalogRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"高"', format: { fill: palette.green, font: { bold: true, color: palette.greenInk } } });

const mappingRows = records.flatMap((row) => row.majors.map((major) => [row.id, major, row.priority, row.security_grade, row.cn_name, row.primary_group]));
const lastMappingRow = mappingRows.length + 4;
mapping.getRange("A1:F1").merge();
mapping.getRange("A1").values = [["0809 计算机类｜Skill—专业映射明细"]];
mapping.getRange("A1:F1").format = { fill: palette.navy, font: { bold: true, color: palette.white, size: 18 } };
mapping.getRange("A2:F2").merge();
mapping.getRange("A2").values = [["一项 Skill 可映射多个专业；本表为“专业覆盖”公式的可审计数据源。"]];
mapping.getRange("A2:F2").format = { fill: palette.paleTeal, font: { color: palette.navy, italic: true } };
mapping.getRange("A4:F4").values = [["Skill ID", "专业名称", "优先级", "安全等级", "Skill名称", "能力群"]];
mapping.getRange(`A5:F${lastMappingRow}`).values = mappingRows;
mapping.getRange("A4:F4").format = { fill: palette.teal, font: { bold: true, color: palette.white } };
mapping.getRange(`A4:F${lastMappingRow}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
mapping.getRange(`A5:F${lastMappingRow}`).format.wrapText = true;
mapping.getRange("A:A").format.columnWidth = 18; mapping.getRange("B:B").format.columnWidth = 31;
mapping.getRange("C:D").format.columnWidth = 13; mapping.getRange("E:E").format.columnWidth = 30; mapping.getRange("F:F").format.columnWidth = 20;
mapping.getRange(`D5:D${lastMappingRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"SA"', format: { fill: palette.green, font: { bold: true, color: palette.greenInk } } });
mapping.getRange(`D5:D${lastMappingRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"SB"', format: { fill: palette.amber, font: { bold: true, color: palette.amberInk } } });
mapping.getRange(`D5:D${lastMappingRow}`).conditionalFormats.add("cellIs", { operator: "equal", formula: '"SB-A"', format: { fill: palette.orange, font: { bold: true, color: palette.orangeInk } } });
mapping.freezePanes.freezeRows(4);
mapping.tables.add(`A4:F${lastMappingRow}`, true, "ComputerScienceMajorMappingTable");

overview.getRange("A1:J1").merge();
overview.getRange("A1").values = [["0809 计算机类｜跨平台开源 Skill 调研总览"]];
overview.getRange("A1:J1").format = { fill: palette.navy, font: { bold: true, color: palette.white, size: 21 }, verticalAlignment: "center" };
overview.getRange("A1:J1").format.rowHeight = 42;
overview.getRange("A2:J2").merge();
overview.getRange("A2").values = [["数据日期 2026-08-07｜范围：公开开源平台｜方法：说明读取、拆包与静态审查｜未做运行验证"]];
overview.getRange("A2:J2").format = { fill: palette.paleTeal, font: { color: palette.navy, italic: true }, verticalAlignment: "center" };
overview.getRange("A4:J4").merge();
overview.getRange("A4").values = [["核心指标"]];
overview.getRange("A4:J4").format = { fill: palette.teal, font: { bold: true, color: palette.white, size: 13 } };
overview.getRange("A5:B5").merge(); overview.getRange("C5:D5").merge(); overview.getRange("E5:F5").merge(); overview.getRange("G5:H5").merge(); overview.getRange("I5:J5").merge();
overview.getRange("A5").formulas = [[`=COUNTA('技能清单'!$B$5:$B$${lastCatalogRow})`]];
overview.getRange("C5").formulas = [[`=COUNTIF('技能清单'!$L$5:$L$${lastCatalogRow},"SA")`]];
overview.getRange("E5").formulas = [[`=COUNTIF('技能清单'!$L$5:$L$${lastCatalogRow},"SB")`]];
overview.getRange("G5").formulas = [[`=COUNTIF('技能清单'!$L$5:$L$${lastCatalogRow},"SB-A")`]];
overview.getRange("I5").formulas = [[`=COUNTA('专业覆盖'!$B$5:$B$18)`]];
overview.getRange("A6:B6").merge(); overview.getRange("C6:D6").merge(); overview.getRange("E6:F6").merge(); overview.getRange("G6:H6").merge(); overview.getRange("I6:J6").merge();
overview.getRange("A6").values = [["正式候选"]]; overview.getRange("C6").values = [["SA 低风险"]]; overview.getRange("E6").values = [["SB 限制使用"]]; overview.getRange("G6").values = [["SB-A 仅适配"]]; overview.getRange("I6").values = [["覆盖专业"]];
overview.getRange("A5:J5").format = { fill: palette.paleBlue, font: { bold: true, color: palette.navy, size: 22 }, horizontalAlignment: "center", verticalAlignment: "center" };
overview.getRange("A6:J6").format = { fill: palette.pale, font: { bold: true, color: palette.muted }, horizontalAlignment: "center" };
overview.getRange("A5:J6").format.borders = { preset: "all", style: "thin", color: palette.grid };
overview.getRange("A5:J5").format.rowHeight = 36;

overview.getRange("A9:B9").values = [["安全等级", "数量"]];
overview.getRange("A10:A12").values = [["SA"], ["SB"], ["SB-A"]];
overview.getRange("B10:B12").formulas = ["SA", "SB", "SB-A"].map((grade) => [`=COUNTIF('技能清单'!$L$5:$L$${lastCatalogRow},"${grade}")`]);
overview.getRange("D9:E9").values = [["来源平台", "数量"]];
overview.getRange(`D10:D${platforms.length + 9}`).values = platforms.map((item) => [item]);
overview.getRange(`E10:E${platforms.length + 9}`).formulas = platforms.map((_, index) => [`=COUNTIF('技能清单'!$F$5:$F$${lastCatalogRow},D${index + 10})`]);
overview.getRange("G9:H9").values = [["能力群", "数量"]];
overview.getRange("G10:G17").values = groups.map((item) => [item]);
overview.getRange("H10:H17").formulas = groups.map((_, index) => [`=COUNTIF('技能清单'!$C$5:$C$${lastCatalogRow},G${index + 10})`]);
for (const headerRange of ["A9:B9", "D9:E9", "G9:H9"]) overview.getRange(headerRange).format = { fill: palette.teal, font: { bold: true, color: palette.white } };
overview.getRange("A9:B12").format.borders = { preset: "all", style: "thin", color: palette.grid };
overview.getRange(`D9:E${platforms.length + 9}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
overview.getRange("G9:H17").format.borders = { preset: "all", style: "thin", color: palette.grid };
overview.getRange("A15:E15").merge(); overview.getRange("A15").values = [["准入解释"]];
overview.getRange("A15:E15").format = { fill: palette.navy, font: { bold: true, color: palette.white } };
overview.getRange("A16:E19").values = [
  ["等级", "原包是否可用", "网络/凭据", "外部状态", "高校落地要求"],
  ["SA", "可作为低风险知识包", "无必要敏感行为", "无自动外部写入", "仍按校内制度复核"],
  ["SB", "只在限制条件下使用", "默认断网或白名单", "状态改变需人工确认", "隔离目录、固定依赖"],
  ["SB-A", "原包不可直接接入", "剥离自动联网/凭据", "剥离上传、发布、部署", "仅交付静态适配版"],
];
overview.getRange("A16:E16").format = { fill: palette.teal, font: { bold: true, color: palette.white } };
overview.getRange("A16:E19").format.borders = { preset: "all", style: "thin", color: palette.grid };
overview.getRange("A16:E19").format.wrapText = true;
overview.getRange("A21:J22").merge();
overview.getRange("A21").values = [["安全边界：本表只说明“静态审查后的准入建议”，不构成可直接安装或运行的安全保证。任何部署仍需在隔离环境中复核依赖、权限、网络域名、数据流和外部状态改变。落选项未进入本工作簿。"]];
overview.getRange("A21:J22").format = { fill: palette.amber, font: { color: palette.amberInk, bold: true }, wrapText: true, verticalAlignment: "center" };
overview.getRange("A:A").format.columnWidth = 19; overview.getRange("B:B").format.columnWidth = 13;
overview.getRange("C:C").format.columnWidth = 19; overview.getRange("D:D").format.columnWidth = 21;
overview.getRange("E:E").format.columnWidth = 18; overview.getRange("F:F").format.columnWidth = 4;
overview.getRange("G:G").format.columnWidth = 27; overview.getRange("H:H").format.columnWidth = 13;
overview.getRange("I:I").format.columnWidth = 19; overview.getRange("J:J").format.columnWidth = 13;
const groupChart = overview.charts.add("bar", overview.getRange("G9:H17"));
groupChart.title = "候选数量（按能力群）";
groupChart.hasLegend = false;
groupChart.setPosition("J9", "P23");
overview.freezePanes.freezeRows(2);

coverage.getRange("A1:H1").merge();
coverage.getRange("A1").values = [["0809 计算机类｜14 个专业覆盖"]];
coverage.getRange("A1:H1").format = { fill: palette.navy, font: { bold: true, color: palette.white, size: 19 } };
coverage.getRange("A2:H2").merge();
coverage.getRange("A2").values = [["数量由“技能清单”的覆盖专业字段自动统计；一项 Skill 可覆盖多个专业，因此合计会高于 88。"]];
coverage.getRange("A2:H2").format = { fill: palette.paleTeal, font: { color: palette.navy, italic: true } };
coverage.getRange("A4:H4").values = [["专业代码", "专业名称", "候选数", "高优先级", "SA", "SB", "SB-A", "覆盖状态"]];
coverage.getRange("A5:B18").values = majors;
coverage.getRange("C5:C18").formulas = majors.map((_, index) => [`=COUNTIF('专业映射'!$B$5:$B$${lastMappingRow},B${index + 5})`]);
coverage.getRange("D5:D18").formulas = majors.map((_, index) => [`=COUNTIFS('专业映射'!$B$5:$B$${lastMappingRow},B${index + 5},'专业映射'!$C$5:$C$${lastMappingRow},"高")`]);
coverage.getRange("E5:E18").formulas = majors.map((_, index) => [`=COUNTIFS('专业映射'!$B$5:$B$${lastMappingRow},B${index + 5},'专业映射'!$D$5:$D$${lastMappingRow},"SA")`]);
coverage.getRange("F5:F18").formulas = majors.map((_, index) => [`=COUNTIFS('专业映射'!$B$5:$B$${lastMappingRow},B${index + 5},'专业映射'!$D$5:$D$${lastMappingRow},"SB")`]);
coverage.getRange("G5:G18").formulas = majors.map((_, index) => [`=COUNTIFS('专业映射'!$B$5:$B$${lastMappingRow},B${index + 5},'专业映射'!$D$5:$D$${lastMappingRow},"SB-A")`]);
coverage.getRange("H5:H18").formulas = majors.map((_, index) => [`=IF(C${index + 5}>0,"已覆盖","待补充")`]);
coverage.getRange("A4:H4").format = { fill: palette.teal, font: { bold: true, color: palette.white }, wrapText: true };
coverage.getRange("A4:H18").format.borders = { preset: "all", style: "thin", color: palette.grid };
coverage.getRange("A5:H18").format.verticalAlignment = "center";
coverage.getRange("A:A").format.columnWidth = 15; coverage.getRange("B:B").format.columnWidth = 30;
coverage.getRange("C:G").format.columnWidth = 14; coverage.getRange("H:H").format.columnWidth = 16;
coverage.getRange("C5:G18").format.horizontalAlignment = "center"; coverage.getRange("H5:H18").format.horizontalAlignment = "center";
coverage.getRange("H5:H18").conditionalFormats.add("cellIs", { operator: "equal", formula: '"已覆盖"', format: { fill: palette.green, font: { bold: true, color: palette.greenInk } } });
const coverageChart = coverage.charts.add("bar", coverage.getRange("B4:C18"));
coverageChart.title = "各专业候选覆盖量";
coverageChart.hasLegend = false;
coverageChart.setPosition("J4", "Q22");
coverage.freezePanes.freezeRows(4);

const sourceRows = repositories.map((repo) => {
  const sample = records.find((row) => row.repo === repo);
  return [sample.platform, repo, sample.repo_url, sample.license, sample.review_commit, sample.review_commit_date, null];
});
const lastSourceRow = sourceRows.length + 4;
sources.getRange("A1:G1").merge();
sources.getRange("A1").values = [["0809 计算机类｜正式来源仓库"]];
sources.getRange("A1:G1").format = { fill: palette.navy, font: { bold: true, color: palette.white, size: 19 } };
sources.getRange("A2:G2").merge();
sources.getRange("A2").values = [["仓库按审查提交固定；同一仓库可能贡献多个 Skill。许可证以对应提交与具体目录为准。"]];
sources.getRange("A2:G2").format = { fill: palette.paleTeal, font: { color: palette.navy, italic: true } };
sources.getRange("A4:G4").values = [["平台", "仓库", "仓库地址", "许可证", "审查提交", "提交日期", "正式候选数"]];
sources.getRange(`A5:G${lastSourceRow}`).values = sourceRows;
sources.getRange(`G5:G${lastSourceRow}`).formulas = repositories.map((_, index) => [`=COUNTIF('技能清单'!$G$5:$G$${lastCatalogRow},B${index + 5})`]);
sources.getRange("A4:G4").format = { fill: palette.teal, font: { bold: true, color: palette.white }, wrapText: true };
sources.getRange(`A4:G${lastSourceRow}`).format.borders = { preset: "all", style: "thin", color: palette.grid };
sources.getRange(`A5:G${lastSourceRow}`).format.wrapText = true;
sources.getRange("A:A").format.columnWidth = 19; sources.getRange("B:B").format.columnWidth = 38;
sources.getRange("C:C").format.columnWidth = 54; sources.getRange("D:D").format.columnWidth = 18;
sources.getRange("E:E").format.columnWidth = 42; sources.getRange("F:F").format.columnWidth = 15; sources.getRange("G:G").format.columnWidth = 16;
sources.freezePanes.freezeRows(4);
sources.tables.add(`A4:G${lastSourceRow}`, true, "ComputerScienceSourceTable");

rules.getRange("A1:F1").merge();
rules.getRange("A1").values = [["0809 计算机类｜范围、安全与使用规则"]];
rules.getRange("A1:F1").format = { fill: palette.navy, font: { bold: true, color: palette.white, size: 19 } };
rules.getRange("A3:B10").values = [
  ["项目", "规则"],
  ["调研对象", "0809 计算机类 14 个本科专业；本工作簿不延伸到其他一级学科。"],
  ["来源范围", "GitHub、GitLab、Gitee、Hugging Face 等公开开源平台；没有为平台多样性而降低准入标准。"],
  ["正式收录", "只保留通过静态审查的正式候选；落选项仅保存在内部过程记录，不进入 Excel 与 Word。"],
  ["验证方式", "读取入口说明、枚举包结构、检查脚本/依赖/网络/凭据/写入/删除/外部状态；未安装、未运行。"],
  ["SA", "静态观察为低风险知识/流程包；仍需按校内制度和具体版本复核。"],
  ["SB", "限制使用：隔离目录、最小权限、固定依赖、默认断网或白名单、状态改变前人工确认。"],
  ["SB-A", "仅适配后使用：原包不可直接安装或整体复制；仅保留已审知识和模板，剥离高风险执行路径。"],
];
rules.getRange("A3:B3").format = { fill: palette.teal, font: { bold: true, color: palette.white } };
rules.getRange("A3:B10").format.borders = { preset: "all", style: "thin", color: palette.grid };
rules.getRange("A4:A10").format = { fill: palette.pale, font: { bold: true, color: palette.navy } };
rules.getRange("A3:B10").format.wrapText = true;
rules.getRange("A:A").format.columnWidth = 20; rules.getRange("B:B").format.columnWidth = 100;
rules.getRange("A12:F12").merge(); rules.getRange("A12").values = [["SB-A 适配版最低要求"]];
rules.getRange("A12:F12").format = { fill: palette.navy, font: { bold: true, color: palette.white } };
rules.getRange("A13:B19").values = [
  ["控制项", "最低要求"],
  ["保留范围", "只保留 SKILL.md、说明性 references、非可执行模板以及逐文件复核后批准的脚本。"],
  ["依赖", "移除 curl|shell、未固定版本的 npx -y、下载后直接执行；依赖必须锁版本并记录哈希。"],
  ["凭据", "禁止自动搜索或读取 .env、令牌、密钥；由用户侧以最小权限按任务注入。"],
  ["网络", "默认断网；必要联网采用域名白名单，不发送学生、员工、科研或管理敏感数据。"],
  ["外部状态", "禁止自动上传、发布、推送、部署、评论、提交、付费训练或调用硬件执行。"],
  ["文件系统", "输出到显式指定的新目录，禁止静默覆盖、递归删除或访问无关目录。"],
];
rules.getRange("A13:B13").format = { fill: palette.teal, font: { bold: true, color: palette.white } };
rules.getRange("A13:B19").format.borders = { preset: "all", style: "thin", color: palette.grid };
rules.getRange("A14:A19").format = { fill: palette.pale, font: { bold: true, color: palette.navy } };
rules.getRange("A13:B19").format.wrapText = true;
rules.getRange("A21:F22").merge();
rules.getRange("A21").values = [["结论边界：静态审查只能降低已发现风险，不能证明运行时绝对安全。环境、依赖、上游版本、外部服务和输入数据变化后，原结论必须重新审查。"]];
rules.getRange("A21:F22").format = { fill: palette.amber, font: { bold: true, color: palette.amberInk }, wrapText: true, verticalAlignment: "center" };
rules.freezePanes.freezeRows(1);

const outputPath = path.join(outputDir, "0809_计算机类_跨平台技能调研.xlsx");
const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);

for (const [sheetName, scale] of [["总览", 1], ["技能清单", 0.62], ["专业覆盖", 0.9], ["专业映射", 0.72], ["来源仓库", 0.9], ["规则与说明", 1]]) {
  const preview = await workbook.render({ sheetName, autoCrop: "all", scale, format: "png" });
  await fs.writeFile(path.join(renderDir, `${sheetName}.png`), new Uint8Array(await preview.arrayBuffer()));
}

const inspections = {};
for (const [sheetName, range] of [["总览", "A1:P24"], ["技能清单", `A1:Z${lastCatalogRow}`], ["专业覆盖", "A1:Q22"], ["专业映射", `A1:F${lastMappingRow}`], ["来源仓库", `A1:G${lastSourceRow}`], ["规则与说明", "A1:F22"]]) {
  const result = await workbook.inspect({ kind: "formula,region", sheetId: sheetName, range, maxChars: 16000, options: { maxResults: 500 } });
  inspections[sheetName] = result.ndjson ?? String(result);
}
const errors = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 200 }, summary: "formula error scan" });
await fs.writeFile(path.join(renderDir, "inspect.json"), JSON.stringify({ inspections, errors: errors.ndjson ?? String(errors) }, null, 2), "utf8");
console.log(`${records.length} skills -> ${outputPath}`);
