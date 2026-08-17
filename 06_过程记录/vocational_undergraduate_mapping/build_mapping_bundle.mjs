import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { validateBundle } from "./mapping_schema.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const processRoot = path.dirname(scriptDir);

async function readJson(filePath) {
  return JSON.parse((await fs.readFile(filePath, "utf8")).replace(/^\uFEFF/, ""));
}

export async function buildMappingBundle() {
  const [
    vocationalPayload,
    undergraduatePayload,
    classSkillsPayload,
    candidatePayload,
    ledgerPayload,
    reversePayload,
    sourceManifest,
    inputManifest,
  ] = await Promise.all([
    readJson(path.join(scriptDir, "catalogs", "vocational_effective_2026.json")),
    readJson(
      path.join(processRoot, "discipline_mapping", "catalogs", "undergraduate_2026.json"),
    ),
    readJson(path.join(scriptDir, "catalogs", "vocational_class_skills.json")),
    readJson(path.join(scriptDir, "artifacts", "mapping_candidates.json")),
    readJson(path.join(scriptDir, "review", "vocational_review_ledger.json")),
    readJson(path.join(scriptDir, "review", "undergraduate_reverse_ledger.json")),
    readJson(path.join(scriptDir, "source_manifest.json")),
    readJson(path.join(scriptDir, "input_manifest.json")),
  ]);

  const candidateById = new Map(
    candidatePayload.records.map((row) => [row.mapping_id, row]),
  );
  const acceptedIds = new Set(
    ledgerPayload.records.flatMap((row) => row.accepted_mapping_ids),
  );
  const mappings = [...acceptedIds]
    .map((mappingId) => {
      const mapping = candidateById.get(mappingId);
      if (!mapping) throw new Error(`accepted mapping missing from candidates: ${mappingId}`);
      return mapping;
    })
    .sort(
      (left, right) =>
        left.vocational_code.localeCompare(right.vocational_code, "zh-CN") ||
        left.undergraduate_code.localeCompare(right.undergraduate_code, "zh-CN"),
    );

  const vocationalByCode = new Map(
    vocationalPayload.records.map((row) => [row.major_code, row]),
  );
  const undergraduateByCode = new Map(
    undergraduatePayload.records.map((row) => [row.major_code, row]),
  );
  const mappingsByVocational = Map.groupBy(mappings, (row) => row.vocational_code);
  const mappingsByUndergraduate = Map.groupBy(mappings, (row) => row.undergraduate_code);
  const ledgerByVocational = new Map(
    ledgerPayload.records.map((row) => [row.vocational_code, row]),
  );

  const vocationalIndex = vocationalPayload.records.map((major) => {
    const ledger = ledgerByVocational.get(major.major_code);
    if (!ledger) throw new Error(`missing vocational ledger: ${major.major_code}`);
    const accepted = mappingsByVocational.get(major.major_code) ?? [];
    return {
      vocational_code: major.major_code,
      vocational_name: major.major_name,
      category_code: major.category_code,
      category_name: major.category_name,
      class_code: major.class_code,
      class_name: major.class_name,
      mapping_ids: [...ledger.accepted_mapping_ids],
      primary_undergraduate_code:
        accepted.find((row) => row.is_primary)?.undergraduate_code ?? null,
      accepted_consumable_count: accepted.filter((row) => row.consumable).length,
      zero_direct: ledger.zero_direct,
      zero_all: ledger.zero_all,
      review_status: ledger.review_status,
      review_note: ledger.review_note,
    };
  });

  const reverseByCode = new Map(
    reversePayload.records.map((row) => [row.undergraduate_code, row]),
  );
  const undergraduateIndex = undergraduatePayload.records.map((major) => {
    const reverse = reverseByCode.get(major.major_code);
    if (!reverse) throw new Error(`missing undergraduate reverse ledger: ${major.major_code}`);
    const accepted = mappingsByUndergraduate.get(major.major_code) ?? [];
    return {
      undergraduate_code: major.major_code,
      undergraduate_name: major.major_name,
      category_code: major.category_code,
      category_name: major.category_name,
      class_code: major.class_code,
      class_name: major.class_name,
      coverage_state: reverse.coverage_state,
      mapping_ids_by_level: reverse.mapping_ids_by_level,
      mapping_count: accepted.length,
      vocational_codes: [...new Set(accepted.map((row) => row.vocational_code))].sort(),
      zero_accepted_consumable: reverse.zero_accepted_consumable,
    };
  });

  const classAggregation = classSkillsPayload.classes.map((classRow) => {
    const majors = vocationalPayload.records.filter(
      (major) => major.class_code === classRow.class_code,
    );
    const classMappings = mappings.filter((mapping) =>
      majors.some((major) => major.major_code === mapping.vocational_code),
    );
    return {
      category_code: classRow.category_code,
      category_name: classRow.category_name,
      class_code: classRow.class_code,
      class_name: classRow.class_name,
      vocational_major_count: majors.length,
      accepted_mapping_count: classMappings.length,
      consumable_mapping_count: classMappings.filter((row) => row.consumable).length,
      core_mapping_count: classMappings.filter((row) =>
        ["主映射/核心对应", "其他核心对应"].includes(row.relation_level),
      ).length,
      distinct_undergraduate_count: new Set(
        classMappings.map((row) => row.undergraduate_code),
      ).size,
      zero_direct_major_count: majors.filter(
        (major) => ledgerByVocational.get(major.major_code)?.zero_direct,
      ).length,
      zero_all_major_count: majors.filter(
        (major) => ledgerByVocational.get(major.major_code)?.zero_all,
      ).length,
      skills_domains: classRow.skills_domains,
    };
  });

  const blocking = [];
  if (vocationalIndex.length !== vocationalPayload.records.length) {
    blocking.push({ code: "VOCATIONAL_INDEX_INCOMPLETE", message: "高职反向索引不完整" });
  }
  if (undergraduateIndex.length !== undergraduatePayload.records.length) {
    blocking.push({ code: "UNDERGRADUATE_INDEX_INCOMPLETE", message: "本科反向索引不完整" });
  }
  if (classAggregation.length !== classSkillsPayload.classes.length) {
    blocking.push({ code: "CLASS_AGGREGATION_INCOMPLETE", message: "专业类聚合不完整" });
  }
  const review = ledgerPayload.records
    .filter((row) => row.review_status === "存在歧义，建议学科专家复核")
    .map((row) => ({
      code: "EXPERT_REVIEW_RECOMMENDED",
      vocational_code: row.vocational_code,
      vocational_name: vocationalByCode.get(row.vocational_code)?.major_name,
      message: row.review_note,
    }));
  const notice = [
    ...ledgerPayload.records
      .filter((row) => row.zero_all)
      .map((row) => ({
        code: "CONFIRMED_NO_MAPPING",
        vocational_code: row.vocational_code,
        vocational_name: vocationalByCode.get(row.vocational_code)?.major_name,
        message: row.review_note,
      })),
    ...vocationalPayload.records
      .filter((row) => row.enrollment_effective === "2027")
      .map((row) => ({
        code: "ENROLLMENT_EFFECTIVE_2027",
        vocational_code: row.major_code,
        vocational_name: row.major_name,
        message: "该专业列入2026年目录增补，自2027年起执行招生。",
      })),
  ];
  const qa = { blocking, review, notice };

  const bundle = {
    metadata: {
      generated_at: "2026-08-17",
      catalog_version: "2026-07",
      purpose: "高职专科专业与本科专业相关性映射，用于 Skills 学科标签与检索",
      mapping_count: mappings.length,
      policy_note: "专业映射不代表学历等同、升学资格或职业资格准入。",
    },
    vocational_catalog: vocationalPayload.records,
    undergraduate_catalog: undergraduatePayload.records,
    mappings,
    vocational_index: vocationalIndex,
    undergraduate_index: undergraduateIndex,
    class_aggregation: classAggregation,
    sources: {
      official_sources: sourceManifest.sources,
      input_manifest: inputManifest,
    },
    qa,
  };
  validateBundle(bundle);
  if (blocking.length > 0) throw new Error(`blocking QA findings: ${blocking.length}`);

  const summary = {
    generated_at: "2026-08-17",
    vocational_count: vocationalPayload.records.length,
    undergraduate_count: undergraduatePayload.records.length,
    class_count: classAggregation.length,
    mapping_count: mappings.length,
    consumable_mapping_count: mappings.filter((row) => row.consumable).length,
    primary_mapping_count: mappings.filter((row) => row.is_primary).length,
    vocational_zero_direct: vocationalIndex.filter((row) => row.zero_direct).length,
    vocational_zero_all: vocationalIndex.filter((row) => row.zero_all).length,
    undergraduate_zero_consumable: undergraduateIndex.filter(
      (row) => row.zero_accepted_consumable,
    ).length,
    expert_review_count: review.length,
    notice_count: notice.length,
    blocking_count: blocking.length,
    relation_level_counts: Object.fromEntries(
      ["主映射/核心对应", "其他核心对应", "强相关", "延伸相关", "目录参考"].map(
        (level) => [level, mappings.filter((row) => row.relation_level === level).length],
      ),
    ),
  };
  return { bundle, qa, summary };
}

async function main() {
  const { bundle, qa, summary } = await buildMappingBundle();
  const artifactDir = path.join(scriptDir, "artifacts");
  await Promise.all([
    fs.writeFile(
      path.join(artifactDir, "mapping_bundle.json"),
      `${JSON.stringify(bundle, null, 2)}\n`,
      "utf8",
    ),
    fs.writeFile(
      path.join(artifactDir, "qa_findings.json"),
      `${JSON.stringify(qa, null, 2)}\n`,
      "utf8",
    ),
    fs.writeFile(
      path.join(artifactDir, "summary.json"),
      `${JSON.stringify(summary, null, 2)}\n`,
      "utf8",
    ),
  ]);
  console.log(
    `mapping bundle: ${bundle.mappings.length}; blocking=${qa.blocking.length}; review=${qa.review.length}; notice=${qa.notice.length}`,
  );
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await main();
}
