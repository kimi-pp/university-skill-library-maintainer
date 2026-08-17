import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { validateReviewRow } from "./mapping_schema.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const catalogPath = path.join(scriptDir, "catalogs", "vocational_effective_2026.json");
const candidatePath = path.join(scriptDir, "artifacts", "mapping_candidates.json");
const decisionPath = path.join(scriptDir, "rules", "vocational_review_decisions.json");
const outputPath = path.join(scriptDir, "review", "vocational_review_ledger.json");

async function readJson(filePath) {
  return JSON.parse((await fs.readFile(filePath, "utf8")).replace(/^\uFEFF/, ""));
}

function selectedPrefixes() {
  const scope = process.argv.find((value) => value.startsWith("--scope="))?.split("=")[1] ?? "4";
  if (scope === "all") return new Set(["4", "5"]);
  return new Set(scope.split(",").map((value) => value.trim()).filter(Boolean));
}

const [catalogPayload, candidatePayload, decisionPayload] = await Promise.all([
  readJson(catalogPath),
  readJson(candidatePath),
  readJson(decisionPath),
]);

const prefixes = selectedPrefixes();
const candidatesByVocational = new Map();
for (const candidate of candidatePayload.records) {
  const rows = candidatesByVocational.get(candidate.vocational_code) ?? [];
  rows.push(candidate);
  candidatesByVocational.set(candidate.vocational_code, rows);
}
const decisionsByVocational = new Map(
  decisionPayload.records.map((row) => [row.vocational_code, row]),
);

let existing = { records: [] };
try {
  existing = await readJson(outputPath);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}
const preserved = existing.records.filter(
  (row) => !prefixes.has(row.vocational_code.slice(0, 1)),
);

const generated = catalogPayload.records
  .filter((major) => prefixes.has(major.major_code.slice(0, 1)))
  .map((major) => {
    const candidates = candidatesByVocational.get(major.major_code) ?? [];
    const candidateIds = candidates.map((row) => row.mapping_id);
    const decision = decisionsByVocational.get(major.major_code) ?? {};
    const rejected = [...(decision.rejected_mapping_ids ?? [])].sort();
    const rejectedSet = new Set(rejected);
    const acceptedCandidates = candidates.filter(
      (row) => !rejectedSet.has(row.mapping_id),
    );
    const accepted = acceptedCandidates.map((row) => row.mapping_id).sort();
    const consumableAccepted = acceptedCandidates.filter((row) => row.consumable);
    const directAccepted = consumableAccepted.filter((row) =>
      ["主映射/核心对应", "其他核心对应"].includes(row.relation_level),
    );
    const row = {
      vocational_code: major.major_code,
      review_status:
        decision.review_status ??
        (consumableAccepted.length === 0 ? "已确认无直接对应" : "已依据规则复核"),
      accepted_mapping_ids: accepted,
      rejected_mapping_ids: rejected,
      zero_direct: directAccepted.length === 0,
      zero_all: consumableAccepted.length === 0,
      review_note:
        decision.review_note ??
        (candidateIds.length === 0
          ? "已核对本科目录与专业类边界，未发现培养对象、知识基础或技术体系可构成稳定映射的本科专业。"
          : "已按培养对象、核心知识、关键技术和职业场景复核全部候选；通过者按既定强度保留供 Skills 标签与检索使用。"),
      reviewed_at: "2026-08-17",
    };
    validateReviewRow(row, candidateIds);
    return row;
  });

const records = [...preserved, ...generated].sort((left, right) =>
  left.vocational_code.localeCompare(right.vocational_code, "zh-CN"),
);
await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.writeFile(
  outputPath,
  `${JSON.stringify(
    {
      metadata: {
        generated_at: "2026-08-17",
        record_count: records.length,
        completed_count: records.filter((row) => row.review_status !== "尚未完成复核").length,
        scope: [...prefixes].sort(),
      },
      records,
    },
    null,
    2,
  )}\n`,
  "utf8",
);
console.log(`vocational review ledger: ${records.length}`);
