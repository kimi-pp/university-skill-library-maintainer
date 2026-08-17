import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const inputManifestPath = path.join(scriptDir, "input_manifest.json");
const outputPath = path.join(scriptDir, "catalogs", "vocational_class_skills.json");

const expectedRanges = {
  Skills领域分类总表: "A1:E61",
  "领域分类-专业反向索引": "A1:F15",
  "专业大类-领域分类矩阵": "A1:R20",
  "专业类-领域分类明细": "A1:F389",
};

function text(value) {
  return value === null || value === undefined ? "" : String(value).trim();
}

export async function extractInputClassification() {
  const manifestText = await fs.readFile(inputManifestPath, "utf8");
  const manifest = JSON.parse(manifestText.replace(/^\uFEFF/, ""));
  const workbook = await SpreadsheetFile.importXlsx(
    await FileBlob.load(manifest.absolute_path),
  );

  const actualNames = workbook.worksheets.items.map((sheet) => sheet.name);
  for (const name of Object.keys(expectedRanges)) {
    if (!actualNames.includes(name)) throw new Error(`missing source sheet: ${name}`);
    const sheet = workbook.worksheets.getItem(name);
    if (sheet.getUsedRange().address !== expectedRanges[name]) {
      throw new Error(
        `unexpected used range for ${name}: ${sheet.getUsedRange().address}`,
      );
    }
  }

  const domainRows = workbook.worksheets
    .getItem("Skills领域分类总表")
    .getUsedRange().values.slice(1);
  const domainOrder = [];
  const domainDescriptions = new Map();
  for (const row of domainRows) {
    const domain = text(row[1]);
    if (!domain) continue;
    domainOrder.push(domain);
    domainDescriptions.set(domain, text(row[2]));
  }

  const detailRows = workbook.worksheets
    .getItem("专业类-领域分类明细")
    .getUsedRange().values.slice(1);
  const categories = new Map();
  const classes = new Map();
  let currentCategoryCode = "";
  let currentCategoryName = "";
  let currentClassCode = "";
  let currentClassName = "";

  for (const row of detailRows) {
    if (text(row[0])) currentCategoryCode = text(row[0]);
    if (text(row[1])) currentCategoryName = text(row[1]);
    if (text(row[2])) currentClassCode = text(row[2]);
    if (text(row[3])) currentClassName = text(row[3]);
    const domain = text(row[4]);

    if (!currentCategoryCode || !currentCategoryName || !currentClassCode || !currentClassName || !domain) {
      throw new Error(`incomplete classification row: ${JSON.stringify(row)}`);
    }
    if (!domainDescriptions.has(domain)) {
      throw new Error(`unknown Skills domain: ${domain}`);
    }

    categories.set(currentCategoryCode, {
      category_code: currentCategoryCode,
      category_name: currentCategoryName,
    });
    const current = classes.get(currentClassCode) ?? {
      category_code: currentCategoryCode,
      category_name: currentCategoryName,
      class_code: currentClassCode,
      class_name: currentClassName,
      skills_domains: [],
      domain_descriptions: {},
      source_sheet: "专业类-领域分类明细",
    };
    if (!current.skills_domains.includes(domain)) current.skills_domains.push(domain);
    current.domain_descriptions[domain] = domainDescriptions.get(domain);
    classes.set(currentClassCode, current);
  }

  const orderIndex = new Map(domainOrder.map((domain, index) => [domain, index]));
  for (const row of classes.values()) {
    row.skills_domains.sort((left, right) => orderIndex.get(left) - orderIndex.get(right));
  }

  return {
    metadata: {
      purpose: "Skills辅助分类上下文，不作为专业相关性单独证据",
      input_sha256: manifest.sha256,
      extracted_at: "2026-08-17",
    },
    source_ranges: expectedRanges,
    domains: domainOrder.map((domain, index) => ({
      domain_order: index + 1,
      domain_name: domain,
      domain_description: domainDescriptions.get(domain),
    })),
    categories: [...categories.values()].sort((a, b) =>
      a.category_code.localeCompare(b.category_code, "zh-CN"),
    ),
    classes: [...classes.values()].sort((a, b) =>
      a.class_code.localeCompare(b.class_code, "zh-CN"),
    ),
  };
}

async function main() {
  const payload = await extractInputClassification();
  if (payload.categories.length !== 19 || payload.classes.length !== 97) {
    throw new Error(
      `classification coverage mismatch: ${payload.categories.length}/${payload.classes.length}`,
    );
  }
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  console.log(
    `vocational input classification: categories=${payload.categories.length} classes=${payload.classes.length}`,
  );
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await main();
}
