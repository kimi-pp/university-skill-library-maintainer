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
    const preview = await workbook.render({ sheetName, autoCrop: "all", scale, format: "png" });
    const bytes = Buffer.from(await preview.arrayBuffer());
    if (bytes.length < 5000 || bytes.readUInt32BE(0) !== 0x89504e47 || bytes.readUInt32BE(4) !== 0x0d0a1a0a) {
      throw new Error(`${key}/${sheetName}: 渲染结果为空或不是 PNG`);
    }
    const width = bytes.readUInt32BE(16);
    const height = bytes.readUInt32BE(20);
    if (width < 600 || height < 180) throw new Error(`${key}/${sheetName}: 渲染尺寸异常 ${width}x${height}`);
    const outputPath = path.join(outputDir, `${index + 1}_${safeFileName(sheetName)}.png`);
    await fs.writeFile(outputPath, bytes);
    written.push(outputPath);
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
