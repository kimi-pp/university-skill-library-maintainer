import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
import {
  PROJECT_ROOT,
  SHEET_NAMES,
  loadInputs,
  selectManifestItems,
} from "./build_subcategorized_spreadsheets.mjs";

const DEFAULT_RENDER_ROOT = path.join(PROJECT_ROOT, "06_过程记录", "renders", "subcategorized_xlsx");

function safeFileName(value) {
  return value.replace(/[<>:"/\\|?*]/g, "_");
}

function assertPng(bytes, key, label, { minWidth = 600, minHeight = 180 } = {}) {
  if (bytes.length < 5000 || bytes.readUInt32BE(0) !== 0x89504e47 || bytes.readUInt32BE(4) !== 0x0d0a1a0a) {
    throw new Error(`${key}/${label}: 渲染结果为空或不是 PNG`);
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width < minWidth || height < minHeight) throw new Error(`${key}/${label}: 渲染尺寸异常 ${width}x${height}`);
  return { width, height };
}

async function renderToFile(workbook, outputDir, key, { sheetName, fileName, scale, range = null, minimum = {} }) {
  const preview = await workbook.render({ sheetName, ...(range ? { range } : { autoCrop: "all" }), scale, format: "png" });
  const bytes = Buffer.from(await preview.arrayBuffer());
  assertPng(bytes, key, range ? `${sheetName}/${range}` : sheetName, minimum);
  const outputPath = path.join(outputDir, fileName);
  await fs.writeFile(outputPath, bytes);
  return outputPath;
}

function keyCatalogRanges(sheet) {
  const values = sheet.getUsedRange(true).values;
  if (values.length <= 30) return [];
  const dataRows = values.slice(4);
  const longestRow = (columns) => dataRows.reduce((best, row, index) => {
    const length = columns.reduce((sum, column) => sum + String(row[column] ?? "").length, 0);
    return length > best.length ? { row: index + 5, length } : best;
  }, { row: 5, length: -1 }).row;
  const longestTextRow = longestRow([2, 3, 4, 5, 6, 7, 10, 11]);
  const longestUrlRow = longestRow([20, 21]);
  const lastRow = values.length;
  return [
    { label: "title-header", range: "A1:V5" },
    { label: "longest-text", range: `A${longestTextRow}:V${longestTextRow}` },
    { label: "longest-url", range: `A${longestUrlRow}:V${longestUrlRow}` },
    { label: "last-row", range: `A${lastRow}:V${lastRow}` },
  ];
}

export async function renderSpreadsheetFile(filePath, renderRoot, key) {
  const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(filePath));
  const actualNames = workbook.worksheets.items.map((sheet) => sheet.name);
  if (actualNames.join("\u0000") !== SHEET_NAMES.join("\u0000")) throw new Error(`${key}: 渲染前发现工作表名称/顺序错误`);
  const outputDir = path.join(renderRoot, safeFileName(key));
  await fs.mkdir(outputDir, { recursive: true });
  const written = [];
  for (let index = 0; index < SHEET_NAMES.length; index += 1) {
    const sheetName = SHEET_NAMES[index];
    const rowCount = workbook.worksheets.getItem(sheetName).getUsedRange(true).values.length;
    const scale = sheetName === "AI技能清单"
      ? rowCount <= 10 ? 0.65 : rowCount <= 20 ? 0.5 : 0.4
      : sheetName === "来源清单" ? 0.75 : 1;
    written.push(await renderToFile(workbook, outputDir, key, {
      sheetName,
      fileName: `${index + 1}_${safeFileName(sheetName)}.png`,
      scale,
    }));
    if (sheetName === "AI技能清单") {
      for (const segment of keyCatalogRanges(workbook.worksheets.getItem(sheetName))) {
        written.push(await renderToFile(workbook, outputDir, key, {
          sheetName,
          range: segment.range,
          fileName: `${index + 1}_${safeFileName(sheetName)}_segment_${segment.label}_${segment.range.replace(":", "-")}.png`,
          scale: 1.15,
          minimum: { minWidth: 2400, minHeight: 100 },
        }));
      }
    }
  }
  return written;
}

export async function renderSelectedSpreadsheets(manifest, projectRoot, renderRoot = DEFAULT_RENDER_ROOT, { only = null } = {}) {
  const rendered = [];
  for (const item of selectManifestItems(manifest, only)) {
    const filePath = path.resolve(projectRoot, ...item.path.split("/"));
    try {
      const stat = await fs.stat(filePath);
      if (!stat.isFile() || stat.size === 0) throw new Error("文件为空");
    } catch (error) {
      if (error.code === "ENOENT") throw new Error(`${item.key}: 待渲染 XLSX 不存在: ${filePath}`);
      throw error;
    }
    const paths = await renderSpreadsheetFile(filePath, renderRoot, item.key);
    rendered.push(...paths.map((renderPath) => ({ item, renderPath })));
  }
  return rendered;
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
  const { manifest } = await loadInputs(PROJECT_ROOT);
  const rendered = await renderSelectedSpreadsheets(manifest, PROJECT_ROOT, DEFAULT_RENDER_ROOT, { only: parseOnly(argv) });
  console.log(`xlsx_renders=${rendered.length} workbooks=${new Set(rendered.map(({ item }) => item.key)).size}`);
  return 0;
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) {
  main().catch((error) => {
    console.error(`XLSX 渲染失败: ${error.message}`);
    process.exitCode = 1;
  });
}
