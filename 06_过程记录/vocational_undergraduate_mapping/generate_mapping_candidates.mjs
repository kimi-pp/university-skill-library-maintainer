import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import policy from "./rules/mapping_policy.json" with { type: "json" };
import {
  isRestrictedObject,
  validateMappingRecord,
} from "./mapping_schema.mjs";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const processRoot = path.dirname(scriptDir);
const undergraduatePath = path.join(
  processRoot,
  "discipline_mapping",
  "catalogs",
  "undergraduate_2026.json",
);
const vocationalPath = path.join(
  scriptDir,
  "catalogs",
  "vocational_effective_2026.json",
);
const seedPath = path.join(
  scriptDir,
  "rules",
  "vocational_class_seed_rules.json",
);
const overridePath = path.join(
  scriptDir,
  "rules",
  "vocational_major_overrides.json",
);
const outputPath = path.join(scriptDir, "artifacts", "mapping_candidates.json");

const relationRank = new Map([
  ["主映射/核心对应", 0],
  ["其他核心对应", 1],
  ["强相关", 2],
  ["延伸相关", 3],
  ["目录参考", 4],
]);

const aliases = new Map([
  ["计算机应用技术", "计算机科学与技术"],
  ["软件技术", "软件工程"],
  ["大数据技术", "数据科学与大数据技术"],
  ["云计算技术应用", "云计算"],
  ["人工智能技术应用", "人工智能"],
  ["物联网应用技术", "物联网工程"],
  ["信息安全技术应用", "信息安全"],
  ["区块链技术应用", "区块链工程"],
  ["现代通信技术", "通信工程"],
  ["护理", "护理学"],
  ["药学", "药学"],
  ["中药学", "中药学"],
]);

function canonicalName(value) {
  let result = aliases.get(value) ?? value;
  result = result
    .normalize("NFKC")
    .replace(/[\s·•（）()、，,／/\-—_]/g, "")
    .replace(/专业$/, "");
  const suffixes = [
    "服务与管理",
    "运营与管理",
    "设计与制作",
    "应用技术",
    "工程技术",
    "生产技术",
    "管理技术",
    "技术应用",
    "技术",
    "制作",
    "应用",
  ];
  for (const suffix of suffixes) {
    if (result.length > suffix.length + 1 && result.endsWith(suffix)) {
      result = result.slice(0, -suffix.length).replace(/与$/, "");
      break;
    }
  }
  if (result.length >= 3 && result.endsWith("学")) result = result.slice(0, -1);
  return result;
}

function bigrams(value) {
  if (value.length < 2) return new Set([value]);
  const result = new Set();
  for (let index = 0; index < value.length - 1; index += 1) {
    result.add(value.slice(index, index + 2));
  }
  return result;
}

function nameSimilarity(leftName, rightName) {
  const left = canonicalName(leftName);
  const right = canonicalName(rightName);
  if (!left || !right) return 0;
  if (left === right) return 1;
  if (
    Math.min(left.length, right.length) >= 2 &&
    (left.includes(right) || right.includes(left))
  ) {
    return 0.78 + 0.2 * (Math.min(left.length, right.length) / Math.max(left.length, right.length));
  }
  const leftPairs = bigrams(left);
  const rightPairs = bigrams(right);
  const intersection = [...leftPairs].filter((pair) => rightPairs.has(pair)).length;
  return (2 * intersection) / (leftPairs.size + rightPairs.size);
}

function relationFields(level) {
  return {
    relation_level: level,
    skills_behavior: policy.relation_behavior_rules[level],
    consumable: level !== "目录参考",
  };
}

function makeCandidate({
  vocational,
  undergraduate,
  level,
  basis,
  rationale,
  confidence,
  generationMethod,
  sourceRuleId,
  score,
}) {
  const restricted = isRestrictedObject(vocational, undergraduate);
  const relation = restricted
    ? {
        ...policy.sensitive_rule,
        confidence: "中",
      }
    : {
        ...relationFields(level),
        is_primary: false,
        sensitive_restriction: false,
        review_status: "高置信度候选",
        confidence,
      };
  return {
    mapping_id: `VUG-${vocational.major_code}-${undergraduate.major_code}`,
    vocational_code: vocational.major_code,
    undergraduate_code: undergraduate.major_code,
    ...relation,
    relation_basis: basis,
    rationale,
    generation_method: generationMethod,
    source_rule_id: sourceRuleId,
    candidate_score: Number(score.toFixed(4)),
  };
}

function mergeCandidate(candidateMap, candidate) {
  const existing = candidateMap.get(candidate.undergraduate_code);
  if (!existing) {
    candidateMap.set(candidate.undergraduate_code, candidate);
    return;
  }
  const candidateRank = relationRank.get(candidate.relation_level);
  const existingRank = relationRank.get(existing.relation_level);
  if (
    candidateRank < existingRank ||
    (candidateRank === existingRank && candidate.candidate_score > existing.candidate_score)
  ) {
    candidateMap.set(candidate.undergraduate_code, candidate);
  }
}

function applySensitiveTuple(candidate) {
  return {
    ...candidate,
    ...policy.sensitive_rule,
    confidence: candidate.confidence === "低" ? "低" : "中",
  };
}

function applyOverrides(candidateMap, vocational, undergraduateByCode, override) {
  if (!override) return;
  for (const operation of override.operations) {
    if (operation.action === "remove") {
      candidateMap.delete(operation.undergraduate_code);
      continue;
    }
    if (operation.action === "replace") {
      candidateMap.clear();
      for (const target of operation.targets) {
        const undergraduate = undergraduateByCode.get(target.undergraduate_code);
        if (!undergraduate) throw new Error(`override target missing: ${target.undergraduate_code}`);
        mergeCandidate(
          candidateMap,
          makeCandidate({
            vocational,
            undergraduate,
            level: target.relation_level,
            basis: target.relation_basis,
            rationale: target.rationale,
            confidence: target.confidence,
            generationMethod: "专业级覆盖规则",
            sourceRuleId: override.rule_id,
            score: target.candidate_score ?? 1,
          }),
        );
      }
      continue;
    }
    if (operation.action === "add") {
      const undergraduate = undergraduateByCode.get(operation.undergraduate_code);
      if (!undergraduate) throw new Error(`override target missing: ${operation.undergraduate_code}`);
      mergeCandidate(
        candidateMap,
        makeCandidate({
          vocational,
          undergraduate,
          level: operation.relation_level,
          basis: operation.relation_basis,
          rationale: operation.rationale,
          confidence: operation.confidence,
          generationMethod: "专业级覆盖规则",
          sourceRuleId: override.rule_id,
          score: operation.candidate_score ?? 1,
        }),
      );
      continue;
    }
    const current = candidateMap.get(operation.undergraduate_code);
    if (!current) throw new Error(`override candidate missing: ${operation.undergraduate_code}`);
    if (operation.action === "set_level") {
      candidateMap.set(operation.undergraduate_code, {
        ...current,
        ...relationFields(operation.relation_level),
        relation_basis: operation.relation_basis ?? current.relation_basis,
        rationale: operation.rationale ?? current.rationale,
        confidence: operation.confidence ?? current.confidence,
        is_primary: false,
        generation_method: "专业级覆盖规则",
        source_rule_id: override.rule_id,
      });
    } else if (operation.action === "set_primary") {
      candidateMap.set(operation.undergraduate_code, {
        ...current,
        ...relationFields("主映射/核心对应"),
        is_primary: true,
        rationale: operation.rationale ?? current.rationale,
        generation_method: "专业级覆盖规则",
        source_rule_id: override.rule_id,
      });
    } else if (operation.action === "restrict") {
      candidateMap.set(operation.undergraduate_code, applySensitiveTuple(current));
    } else {
      throw new Error(`unsupported override action: ${operation.action}`);
    }
  }
}

function finalizePrimary(candidates) {
  const eligible = candidates
    .filter(
      (row) =>
        !row.sensitive_restriction &&
        (row.is_primary || row.relation_level === "主映射/核心对应"),
    )
    .sort(
      (left, right) =>
        Number(right.is_primary) - Number(left.is_primary) ||
        right.candidate_score - left.candidate_score ||
        left.undergraduate_code.localeCompare(right.undergraduate_code, "zh-CN"),
    );
  const primaryCode = eligible[0]?.undergraduate_code;
  return candidates.map((row) => {
    if (row.sensitive_restriction) return applySensitiveTuple(row);
    if (row.undergraduate_code === primaryCode) {
      return {
        ...row,
        ...relationFields("主映射/核心对应"),
        is_primary: true,
      };
    }
    if (row.relation_level === "主映射/核心对应") {
      return {
        ...row,
        ...relationFields("其他核心对应"),
        is_primary: false,
      };
    }
    return { ...row, is_primary: false };
  });
}

export function generateCandidates({
  vocational,
  undergraduate,
  seeds,
  overrides,
}) {
  const undergraduateByCode = new Map(
    undergraduate.map((row) => [row.major_code, row]),
  );
  const undergraduateByClass = new Map();
  for (const row of undergraduate) {
    if (!row.class_code) continue;
    const rows = undergraduateByClass.get(row.class_code) ?? [];
    rows.push(row);
    undergraduateByClass.set(row.class_code, rows);
  }
  const seedByClass = new Map(
    seeds.map((row) => [row.vocational_class_code, row]),
  );
  const overrideByVocational = new Map(
    overrides.map((row) => [row.vocational_code, row]),
  );
  const records = [];

  for (const vocationalMajor of vocational) {
    const seed = seedByClass.get(vocationalMajor.class_code);
    if (!seed) throw new Error(`missing class seed: ${vocationalMajor.class_code}`);
    const candidateMap = new Map();

    for (const target of seed.default_targets) {
      const undergraduateMajor = undergraduateByCode.get(target.undergraduate_code);
      if (!undergraduateMajor) throw new Error(`default target missing: ${target.undergraduate_code}`);
      mergeCandidate(
        candidateMap,
        makeCandidate({
          vocational: vocationalMajor,
          undergraduate: undergraduateMajor,
          level: target.relation_level,
          basis: ["核心知识基础", "典型职业或行业场景"],
          rationale: `${seed.rationale} 对“${vocationalMajor.major_name}”先保留专业类层面的${target.relation_level}候选。`,
          confidence: "中",
          generationMethod: "专业类种子规则",
          sourceRuleId: seed.rule_id,
          score: 0.4,
        }),
      );
    }

    const allowedUndergraduate = seed.undergraduate_class_codes.flatMap(
      (classCode) => undergraduateByClass.get(classCode) ?? [],
    );
    const scored = allowedUndergraduate
      .map((undergraduateMajor) => ({
        undergraduateMajor,
        score: nameSimilarity(
          vocationalMajor.major_name,
          undergraduateMajor.major_name,
        ),
      }))
      .filter((row) => row.score >= 0.48)
      .sort(
        (left, right) =>
          right.score - left.score ||
          left.undergraduateMajor.major_code.localeCompare(
            right.undergraduateMajor.major_code,
            "zh-CN",
          ),
      )
      .slice(0, 3);

    for (const { undergraduateMajor, score } of scored) {
      const level =
        score >= 0.92
          ? "主映射/核心对应"
          : score >= 0.68
            ? "其他核心对应"
            : "强相关";
      mergeCandidate(
        candidateMap,
        makeCandidate({
          vocational: vocationalMajor,
          undergraduate: undergraduateMajor,
          level,
          basis:
            score >= 0.92
              ? ["主要培养或实践对象", "核心知识基础"]
              : ["核心知识基础", "关键技术体系"],
          rationale: `高职“${vocationalMajor.major_name}”与本科“${undergraduateMajor.major_name}”处于规则限定的对应专业类，并在专业名称指向的培养对象或关键技术上具有连续性。`,
          confidence: score >= 0.92 ? "高" : "中",
          generationMethod: "专业名称与专业类规则",
          sourceRuleId: seed.rule_id,
          score,
        }),
      );
    }

    applyOverrides(
      candidateMap,
      vocationalMajor,
      undergraduateByCode,
      overrideByVocational.get(vocationalMajor.major_code),
    );
    records.push(...finalizePrimary([...candidateMap.values()]));
  }

  const vocationalByCode = new Map(
    vocational.map((row) => [row.major_code, row]),
  );
  records.sort(
    (left, right) =>
      left.vocational_code.localeCompare(right.vocational_code, "zh-CN") ||
      relationRank.get(left.relation_level) - relationRank.get(right.relation_level) ||
      left.undergraduate_code.localeCompare(right.undergraduate_code, "zh-CN"),
  );
  for (const record of records) {
    validateMappingRecord(record, vocationalByCode, undergraduateByCode);
  }
  return records;
}

async function readJson(filePath) {
  return JSON.parse((await fs.readFile(filePath, "utf8")).replace(/^\uFEFF/, ""));
}

async function main() {
  const [vocationalPayload, undergraduatePayload, seedPayload, overridePayload] =
    await Promise.all([
      readJson(vocationalPath),
      readJson(undergraduatePath),
      readJson(seedPath),
      readJson(overridePath),
    ]);
  const records = generateCandidates({
    vocational: vocationalPayload.records,
    undergraduate: undergraduatePayload.records,
    seeds: seedPayload.records,
    overrides: overridePayload.records,
  });
  const payload = {
    metadata: {
      generated_at: "2026-08-17",
      mapping_id_format: "VUG-<vocational_code>-<undergraduate_code>",
      record_count: records.length,
      vocational_count: vocationalPayload.records.length,
      class_rule_count: seedPayload.records.length,
      method: "97个专业类保守种子＋专业名称约束＋专业级覆盖规则",
    },
    records,
  };
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  console.log(`vocational mapping candidates: ${records.length}`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await main();
}
