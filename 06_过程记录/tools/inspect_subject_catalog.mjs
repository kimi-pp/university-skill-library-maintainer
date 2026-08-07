import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";


const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(scriptDir, "..", "..");
const sourcePath = path.resolve(projectRoot, "..", "国内大学本科专业目录.xlsx");
const outputPath = path.join(projectRoot, "06_过程记录", "2026-08-07-本科专业目录工作簿读取.json");

const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(sourcePath));
const sheetInspection = await workbook.inspect({
  kind: "workbook,sheet,table",
  include: "id,name",
  maxChars: 10000,
  tableMaxRows: 8,
  tableMaxCols: 12,
});

const sheetNames = [];
for (const line of (sheetInspection.ndjson ?? String(sheetInspection)).split(/\r?\n/)) {
  if (!line.trim()) continue;
  try {
    const item = JSON.parse(line);
    const name = item.name ?? item.sheetName;
    if (name && !sheetNames.includes(name)) sheetNames.push(name);
  } catch {
    // Keep inspection resilient to non-JSON status lines.
  }
}

const sheets = [];
for (const name of sheetNames) {
  const sheet = workbook.worksheets.getItem(name);
  const used = sheet.getUsedRange(true);
  sheets.push({
    name,
    row_count: used?.rowCount ?? 0,
    column_count: used?.columnCount ?? 0,
    address: used?.address ?? "",
    values: used?.values ?? [],
  });
}

await fs.writeFile(
  outputPath,
  JSON.stringify({ source: sourcePath, inspection: sheetInspection.ndjson ?? String(sheetInspection), sheets }, null, 2),
  "utf8",
);
console.log(`sheets=${sheetNames.length}; output=${outputPath}`);

