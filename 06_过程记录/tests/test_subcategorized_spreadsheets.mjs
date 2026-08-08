import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
import {
  CATALOG_HEADERS,
  SHEET_NAMES,
  buildWorkbook,
  generateSpreadsheets,
  loadInputs,
  selectManifestItems,
  validateInputContracts,
} from "../tools/build_subcategorized_spreadsheets.mjs";
import {
  inspectXlsxPackage,
  verifySpreadsheetFile,
} from "../tools/verify_subcategorized_spreadsheets.mjs";
import { renderSpreadsheetFile } from "../tools/render_subcategorized_spreadsheets.mjs";
import {
  normalizeXlsxPackage,
  semanticXlsxDigest,
  unzipEntries,
  zipEntries,
} from "../tools/xlsx_package_utils.mjs";

const testDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(testDir, "..", "..");
const SAMPLE_KEYS = ["05-overview", "02-08", "01-01", "05-05"];

async function sha256(filePath) {
  return crypto.createHash("sha256").update(await fs.readFile(filePath)).digest("hex");
}

async function withTempDir(fn) {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), "subcategory-xlsx-"));
  try {
    return await fn(directory);
  } finally {
    await fs.rm(directory, { recursive: true, force: true });
  }
}

function xlsxPathFor(root, item) {
  return path.join(root, ...item.path.split("/"));
}

async function rewriteEntry(filePath, entryName, transform) {
  const entries = unzipEntries(await fs.readFile(filePath));
  const before = entries.get(entryName);
  assert.ok(before, `missing XLSX entry ${entryName}`);
  entries.set(entryName, Buffer.from(transform(before.toString("utf8")), "utf8"));
  await fs.writeFile(filePath, zipEntries(entries));
}

function replaceCachedValue(xml, reference, replacement) {
  const pattern = new RegExp(`(<x:c\\b(?=[^>]*\\br="${reference}")[^>]*>.*?<x:v>)(.*?)(</x:v>.*?</x:c>)`, "s");
  assert.match(xml, pattern, `missing cached value for ${reference}`);
  return xml.replace(pattern, `$1${replacement}$3`);
}

function mutateRecords(records, id, field, value) {
  return records.map((record) => record.id === id ? { ...record, [field]: value } : { ...record });
}

async function copyAndMutate(originalPath, root, name, mutation) {
  const copyPath = path.join(root, name);
  await fs.copyFile(originalPath, copyPath);
  await mutation(copyPath);
  return copyPath;
}

const OFFICE_RELATIONSHIP_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships";
const PACKAGE_RELATIONSHIP_NS = "http://schemas.openxmlformats.org/package/2006/relationships";

function semanticFixture({ relationships, references, ordinaryText = "rId1", ordinaryAttribute = "ordinary-rId1" }) {
  const relationshipXml = relationships.map(({ id, type, target, targetMode = null }) => {
    const mode = targetMode ? ` TargetMode="${targetMode}"` : "";
    return `<Relationship Id="${id}" Type="${OFFICE_RELATIONSHIP_NS}/${type}" Target="${target}"${mode} />`;
  }).join("");
  const referenceXml = references.map(({ attribute, id }, index) => `<x:item n="${index + 1}" ${attribute}="${id}" />`).join("");
  const entries = new Map([
    ["xl/workbook.xml", Buffer.from(`<?xml version="1.0" encoding="utf-8"?><x:workbook xmlns:x="urn:test" xmlns:r="${OFFICE_RELATIONSHIP_NS}" xmlns:foo-r="urn:foo-hyphen" xmlns:foo.r="urn:foo-dot" xmlns:my_r="urn:foo-underscore"><x:items>${referenceXml}</x:items><x:note label="${ordinaryAttribute}">${ordinaryText}</x:note></x:workbook>`, "utf8")],
    ["xl/_rels/workbook.xml.rels", Buffer.from(`<?xml version="1.0" encoding="utf-8"?><Relationships xmlns="${PACKAGE_RELATIONSHIP_NS}">${relationshipXml}</Relationships>`, "utf8")],
  ]);
  return zipEntries(entries);
}

async function cycleWorkbookRelationshipIds(filePath) {
  const entries = unzipEntries(await fs.readFile(filePath));
  const relationshipPath = "xl/_rels/workbook.xml.rels";
  const sourcePath = "xl/workbook.xml";
  let relationshipsXml = entries.get(relationshipPath).toString("utf8");
  const elements = [...relationshipsXml.matchAll(/<Relationship\b[^>]*\/?\s*>/g)].map((match) => match[0]);
  const rows = elements.map((element) => {
    const attributes = Object.fromEntries([...element.matchAll(/([A-Za-z:]+)="([^"]*)"/g)].map((match) => [match[1], match[2]]));
    return { element, attributes };
  }).sort((left, right) => `${left.attributes.Type}|${left.attributes.Target}|${left.attributes.TargetMode ?? ""}`.localeCompare(`${right.attributes.Type}|${right.attributes.Target}|${right.attributes.TargetMode ?? ""}`));
  const sourceBefore = entries.get(sourcePath).toString("utf8");
  const referencedIds = new Set([...sourceBefore.matchAll(/\br:(?:id|embed|link)="([^"]+)"/g)].map((match) => match[1]));
  const referencedIndexes = rows.map((row, index) => referencedIds.has(row.attributes.Id) ? index : -1).filter((index) => index >= 0);
  assert.ok(referencedIndexes.length >= 2, "fixture needs two referenced workbook relationships");
  const assignedIds = rows.map((_, index) => `rId${index + 1}`);
  [assignedIds[referencedIndexes[0]], assignedIds[referencedIndexes[1]]] = [assignedIds[referencedIndexes[1]], assignedIds[referencedIndexes[0]]];
  const mapping = new Map(rows.map((row, index) => [row.attributes.Id, assignedIds[index]]));
  relationshipsXml = relationshipsXml.replace(/<Relationship\b[^>]*\/?\s*>/g, (element) => element.replace(/\bId="([^"]+)"/, (match, id) => `Id="${mapping.get(id)}"`));
  const sourceXml = sourceBefore.replace(/\b(r:(?:id|embed|link))="([^"]+)"/g, (match, attribute, id) => {
    const replacement = mapping.get(id);
    return replacement ? `${attribute}="${replacement}"` : match;
  });
  entries.set(relationshipPath, Buffer.from(relationshipsXml, "utf8"));
  entries.set(sourcePath, Buffer.from(sourceXml, "utf8"));
  await fs.writeFile(filePath, zipEntries(entries));
}

test("manifest selection is safe, unique, scope-aware, and stably ordered", async () => {
  const { manifest } = await loadInputs(projectRoot);
  const selected = selectManifestItems([...manifest].reverse(), ["05-05", "05-overview", "01-01"]);
  assert.deepEqual(selected.map((item) => item.key), ["01-01", "05-overview", "05-05"]);

  const duplicate = [...manifest, { ...manifest.find((item) => item.format === "xlsx" && item.subcategory_code === "05-05") }];
  assert.throws(() => selectManifestItems(duplicate), /重复.*manifest.*键/i);

  const unsafe = manifest.map((item) => ({ ...item }));
  const target = unsafe.find((item) => item.format === "xlsx" && item.scope === "overview");
  target.path = "../越界.xlsx";
  assert.throws(() => selectManifestItems(unsafe), /不安全.*路径/i);
  assert.throws(() => selectManifestItems(manifest, ["99-99"]), /未知.*only/i);
});

test("input validation rejects duplicate IDs and subcategory member drift", async () => {
  const { records, taxonomy, manifest } = await loadInputs(projectRoot);
  assert.doesNotThrow(() => validateInputContracts(records, taxonomy, manifest));
  assert.throws(
    () => validateInputContracts([...records, { ...records[0] }], taxonomy, manifest),
    /重复.*Skill ID/i,
  );
  const moved = records.map((record) => ({ ...record }));
  moved.find((record) => record.id === "GH-05-0003").subcategory_code = "05-01";
  assert.throws(() => validateInputContracts(moved, taxonomy, manifest), /成员.*错配|小分类.*不一致/i);
});

test("overview and contrasting subcategory samples reopen with exact values, formulas, and hyperlinks", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const written = await generateSpreadsheets(
      inputs.records,
      inputs.taxonomy,
      inputs.manifest,
      root,
      { only: SAMPLE_KEYS },
    );
    assert.equal(written.length, SAMPLE_KEYS.length);

    for (const { item, outputPath } of written) {
      const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(outputPath));
      assert.deepEqual(workbook.worksheets.items.map((sheet) => sheet.name), SHEET_NAMES);
      const expectedRecords = inputs.records
        .filter((record) => item.scope === "overview"
          ? record.cat === item.big_category_code
          : record.subcategory_code === item.subcategory_code)
        .sort((left, right) => left.id.localeCompare(right.id));
      const catalog = workbook.worksheets.getItem("AI技能清单");
      assert.deepEqual(catalog.getRange("A4:V4").values[0], CATALOG_HEADERS);
      assert.deepEqual(
        catalog.getRange(`N5:N${expectedRecords.length + 4}`).values.flat(),
        expectedRecords.map((record) => record.id),
      );
      assert.deepEqual(
        catalog.getRange(`C5:C${expectedRecords.length + 4}`).values.flat(),
        expectedRecords.map((record) => record.cn),
      );
      assert.deepEqual(catalog.getRange(`U5:U${expectedRecords.length + 4}`).values.flat(), expectedRecords.map((record) => record.skill_url));
      assert.deepEqual(catalog.getRange(`V5:V${expectedRecords.length + 4}`).values.flat(), expectedRecords.map((record) => record.repo_url));
      const packageInfo = await inspectXlsxPackage(outputPath);
      assert.doesNotMatch(packageInfo.sheetXml.get("使用说明"), /<(?:\w+:)?mergeCell\b[^>]*ref="A[12]:H[12]"/, `${item.key}: 使用说明不应保留空白尾列`);
      const catalogXml = packageInfo.sheetXml.get("AI技能清单");
      assert.equal([...catalogXml.matchAll(/<(?:\w+:)?hyperlink\b[^>]*ref="[UV]\d+"[^>]*\br:id="[^"]+"/g)].length, expectedRecords.length * 2);

      const stats = workbook.worksheets.getItem("分类统计");
      const statsFormulas = stats.getUsedRange().formulas.flat().filter(Boolean);
      assert.ok(statsFormulas.length >= 4, `${item.key}: 分类统计缺少公式`);
      assert.ok(statsFormulas.every((formula) => formula.includes("'AI技能清单'!")), `${item.key}: 跨表公式必须引用清单页`);
      const sources = workbook.worksheets.getItem("来源清单");
      const sourceFormulas = sources.getUsedRange().formulas.flat().filter(Boolean);
      assert.ok(sourceFormulas.length >= 1, `${item.key}: 来源清单计数必须是公式`);
      assert.ok(sourceFormulas.every((formula) => /^=COUNTIF\('AI技能清单'!/.test(formula)));
    }
  });
});

test("real XLSX package preserves title styling, user/trace grouping, freeze panes, filters, widths, heights, and limited conditional formatting", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [{ item, outputPath }] = await generateSpreadsheets(
      inputs.records,
      inputs.taxonomy,
      inputs.manifest,
      root,
      { only: ["05-05"] },
    );
    const packageInfo = await inspectXlsxPackage(outputPath);
    assert.deepEqual(packageInfo.sheetNames, SHEET_NAMES);
    assert.match(packageInfo.stylesXml, /FF16324F/i, `${item.key}: 标题深蓝色未写入样式表`);
    assert.match(packageInfo.stylesXml, /FF1F7A8C/i, `${item.key}: 表头蓝绿色未写入样式表`);

    const catalogXml = packageInfo.sheetXml.get("AI技能清单");
    assert.match(catalogXml, /<(?:\w+:)?pane\b[^>]*xSplit="4"[^>]*ySplit="4"|<(?:\w+:)?pane\b[^>]*ySplit="4"[^>]*xSplit="4"/);
    assert.match(catalogXml, /<(?:\w+:)?cols>.*?<(?:\w+:)?col\b[^>]*min="1"[^>]*max="1"[^>]*width="[6-9](?:\.\d+)?"/s);
    assert.match(catalogXml, /<(?:\w+:)?row\b[^>]*r="1"[^>]*ht="(?:3[6-9]|4\d)(?:\.\d+)?"[^>]*customHeight="1"/);
    assert.match(catalogXml, /<(?:\w+:)?row\b[^>]*r="5"[^>]*ht="(?:[7-9]\d|1\d{2})(?:\.\d+)?"[^>]*customHeight="1"/);
    const aStyle = catalogXml.match(/<(?:\w+:)?c\b[^>]*r="A5"[^>]*s="(\d+)"/)[1];
    const mStyle = catalogXml.match(/<(?:\w+:)?c\b[^>]*r="M5"[^>]*s="(\d+)"/)[1];
    assert.notEqual(aStyle, mStyle, "用户字段区和技术追溯区必须使用不同样式");
    const conditionalRanges = [...catalogXml.matchAll(/<(?:\w+:)?conditionalFormatting\b[^>]*sqref="([^"]+)"/g)].map((match) => match[1]);
    assert.deepEqual(conditionalRanges.sort(), ["I5:I9", "J5:J9"]);
    assert.ok(packageInfo.tableXml.some((xml) => /<(?:\w+:)?autoFilter\b[^>]*ref="A4:V9"/.test(xml)), "AI技能清单必须启用筛选");
    for (const xml of packageInfo.sheetXml.values()) assert.doesNotMatch(xml, /showGridLines="1"/);
  });
});

test("verifier checks a real XLSX and rejects expected-member mismatch", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [written] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, root, { only: ["02-08"] });
    const ok = await verifySpreadsheetFile(written.outputPath, written.item, inputs.records, inputs.taxonomy);
    assert.equal(ok.skillCount, 1);
    const missing = inputs.records.filter((record) => record.id !== "GH-02-0016");
    await assert.rejects(
      verifySpreadsheetFile(written.outputPath, written.item, missing, inputs.taxonomy),
      /成员.*不一致|Skill ID.*不一致/i,
    );
  });
});

test("generation is byte-idempotent despite reversed input ordering", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [first] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, root, { only: ["01-01"] });
    const firstHash = await sha256(first.outputPath);
    const [second] = await generateSpreadsheets(
      [...inputs.records].reverse(),
      [...inputs.taxonomy].reverse(),
      [...inputs.manifest].reverse(),
      root,
      { only: ["01-01"] },
    );
    assert.equal(await sha256(second.outputPath), firstHash);
  });
});

test("renderer reopens one XLSX and emits one nonblank PNG per worksheet", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [written] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, root, { only: ["02-08"] });
    const renderDir = path.join(root, "renders");
    const rendered = await renderSpreadsheetFile(written.outputPath, renderDir, written.item.key);
    assert.equal(rendered.length, 4);
    for (const renderedPath of rendered) {
      const bytes = await fs.readFile(renderedPath);
      assert.ok(bytes.length > 5000, `${renderedPath}: PNG 体积异常`);
      assert.deepEqual([...bytes.subarray(0, 8)], [137, 80, 78, 71, 13, 10, 26, 10]);
      assert.ok(bytes.readUInt32BE(16) >= 600, `${renderedPath}: PNG 宽度异常`);
      assert.ok(bytes.readUInt32BE(20) >= 180, `${renderedPath}: PNG 高度异常`);
    }
  });
});

test("verifier rejects drift in verification, stars, and updated facts", async (t) => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [written] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, root, { only: ["05-05"] });
    const target = inputs.records.find((record) => record.subcategory_code === "05-05");
    const mutations = [
      ["本次核验", "plain_verification", `${target.plain_verification}（变异）`],
      ["GitHub 关注数", "stars", Number(target.stars) + 1],
      ["最近更新", "repo_pushed", "2000-01-01"],
    ];
    for (const [label, field, value] of mutations) {
      await t.test(label, async () => {
        await assert.rejects(
          verifySpreadsheetFile(
            written.outputPath,
            written.item,
            mutateRecords(inputs.records, target.id, field, value),
            inputs.taxonomy,
          ),
          new RegExp(`${label}|事实|22列`),
        );
      });
    }
  });
});

test("verifier rejects swapped per-category statistics even when the total is unchanged", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [written] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, root, { only: ["05-overview"] });
    const mutated = await copyAndMutate(written.outputPath, root, "swapped-stats.xlsx", async (filePath) => {
      await rewriteEntry(filePath, "xl/worksheets/sheet3.xml", (xml) => {
        const first = xml.match(/<x:c\b(?=[^>]*\br="B6")[^>]*>.*?<x:v>(.*?)<\/x:v>.*?<\/x:c>/s)?.[1];
        const second = xml.match(/<x:c\b(?=[^>]*\br="B7")[^>]*>.*?<x:v>(.*?)<\/x:v>.*?<\/x:c>/s)?.[1];
        assert.notEqual(first, second, "fixture must have unequal category counts");
        return replaceCachedValue(replaceCachedValue(xml, "B6", second), "B7", first);
      });
    });
    await assert.rejects(
      verifySpreadsheetFile(mutated, written.item, inputs.records, inputs.taxonomy),
      /小分类.*计数|分类统计.*逐项/,
    );
  });
});

test("verifier rejects wrong per-repository allocation even when the total is unchanged", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [written] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, root, { only: ["05-overview"] });
    const mutated = await copyAndMutate(written.outputPath, root, "swapped-sources.xlsx", async (filePath) => {
      await rewriteEntry(filePath, "xl/worksheets/sheet4.xml", (xml) => {
        const first = xml.match(/<x:c\b(?=[^>]*\br="G5")[^>]*>.*?<x:v>(.*?)<\/x:v>.*?<\/x:c>/s)?.[1];
        const second = xml.match(/<x:c\b(?=[^>]*\br="G6")[^>]*>.*?<x:v>(.*?)<\/x:v>.*?<\/x:c>/s)?.[1];
        assert.notEqual(first, second, "fixture must have unequal repository counts");
        return replaceCachedValue(replaceCachedValue(xml, "G5", second), "G6", first);
      });
    });
    await assert.rejects(
      verifySpreadsheetFile(mutated, written.item, inputs.records, inputs.taxonomy),
      /仓库.*计数|来源清单.*逐项/,
    );
  });
});

test("verifier checks every sheet freeze and the source filter and hyperlink", async (t) => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [written] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, root, { only: ["05-05"] });
    const freezeCases = [
      ["使用说明冻结", "xl/worksheets/sheet1.xml", 'ySplit="2"', 'ySplit="1"'],
      ["分类统计冻结", "xl/worksheets/sheet3.xml", 'ySplit="4"', 'ySplit="3"'],
      ["来源清单冻结", "xl/worksheets/sheet4.xml", 'ySplit="4"', 'ySplit="3"'],
    ];
    for (const [label, entryName, before, after] of freezeCases) {
      await t.test(label, async () => {
        const mutated = await copyAndMutate(written.outputPath, root, `${label}.xlsx`, async (filePath) => {
          await rewriteEntry(filePath, entryName, (xml) => {
            assert.ok(xml.includes(before));
            return xml.replace(before, after);
          });
        });
        await assert.rejects(verifySpreadsheetFile(mutated, written.item, inputs.records, inputs.taxonomy), /冻结位置/);
      });
    }
    await t.test("来源清单筛选", async () => {
      const mutated = await copyAndMutate(written.outputPath, root, "source-filter.xlsx", async (filePath) => {
        const entries = unzipEntries(await fs.readFile(filePath));
        const tableName = [...entries.keys()].find((name) => /^xl\/tables\/table\d+\.xml$/.test(name)
          && entries.get(name).toString("utf8").includes('ref="A4:G'));
        assert.ok(tableName);
        await rewriteEntry(filePath, tableName, (xml) => xml.replace(/ref="A4:G(\d+)"/g, 'ref="A4:F$1"'));
      });
      await assert.rejects(verifySpreadsheetFile(mutated, written.item, inputs.records, inputs.taxonomy), /来源清单.*筛选/);
    });
    await t.test("来源清单链接", async () => {
      const mutated = await copyAndMutate(written.outputPath, root, "source-link.xlsx", async (filePath) => {
        await rewriteEntry(filePath, "xl/worksheets/_rels/sheet4.xml.rels", (xml) => {
          assert.match(xml, /TargetMode="External"/);
          return xml.replace(/Target="https:\/\/github\.com\/[^"]+" TargetMode="External"/, 'Target="https://example.com/wrong-source" TargetMode="External"');
        });
      });
      await assert.rejects(verifySpreadsheetFile(mutated, written.item, inputs.records, inputs.taxonomy), /来源清单.*链接|HTTPS|External/);
    });
  });
});

test("OOXML normalization is scoped and idempotent when invoked twice on the same package", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const item = selectManifestItems(inputs.manifest, ["02-08"])[0];
    const records = inputs.records.filter((record) => record.subcategory_code === "02-08");
    const filePath = path.join(root, "raw.xlsx");
    const rawBlob = await SpreadsheetFile.exportXlsx(buildWorkbook(item, records, inputs.taxonomy));
    const originalLog = console.log;
    try {
      console.log = () => {};
      await rawBlob.save(filePath);
    } finally {
      console.log = originalLog;
    }
    const beforeEntries = unzipEntries(await fs.readFile(filePath));
    const links = [
      { sheetPath: "xl/worksheets/sheet2.xml", links: [
        { ref: "U5", target: records[0].skill_url },
        { ref: "V5", target: records[0].repo_url },
      ] },
      { sheetPath: "xl/worksheets/sheet4.xml", links: [{ ref: "B5", target: records[0].repo_url }] },
    ];
    const freezes = [
      { sheetPath: "xl/worksheets/sheet1.xml", ySplit: 2, topLeftCell: "A3", activePane: "bottomLeft" },
      { sheetPath: "xl/worksheets/sheet2.xml", xSplit: 4, ySplit: 4, topLeftCell: "E5", activePane: "bottomRight" },
      { sheetPath: "xl/worksheets/sheet3.xml", ySplit: 4, topLeftCell: "A5", activePane: "bottomLeft" },
      { sheetPath: "xl/worksheets/sheet4.xml", xSplit: 1, ySplit: 4, topLeftCell: "B5", activePane: "bottomRight" },
    ];
    await normalizeXlsxPackage(filePath, links, freezes);
    const onceHash = await sha256(filePath);
    const onceEntries = unzipEntries(await fs.readFile(filePath));
    const touched = new Set([
      ...freezes.map((plan) => plan.sheetPath),
      ...links.map((plan) => plan.sheetPath.replace(/^(.*)\/([^/]+)$/, "$1/_rels/$2.rels")),
    ]);
    for (const [name, bytes] of beforeEntries) {
      if (!touched.has(name)) assert.deepEqual(onceEntries.get(name), bytes, `unrelated entry changed: ${name}`);
    }
    await normalizeXlsxPackage(filePath, links, freezes);
    assert.equal(await sha256(filePath), onceHash, "second normalization must be byte-identical");

    const twiceEntries = unzipEntries(await fs.readFile(filePath));
    for (const plan of links) {
      const sheetXml = twiceEntries.get(plan.sheetPath).toString("utf8");
      const relationshipPath = plan.sheetPath.replace(/^(.*)\/([^/]+)$/, "$1/_rels/$2.rels");
      const relationshipsXml = twiceEntries.get(relationshipPath).toString("utf8");
      const nodeIds = [...sheetXml.matchAll(/<x:hyperlink\b[^>]*\br:id="([^"]+)"/g)].map((match) => match[1]);
      const relationshipRows = [...relationshipsXml.matchAll(/<Relationship\b[^>]*\bId="([^"]+)"[^>]*\bType="[^"]*\/hyperlink"[^>]*\bTarget="([^"]+)"[^>]*\bTargetMode="External"[^>]*\/?\s*>/g)]
        .map((match) => ({ id: match[1], target: match[2] }));
      assert.equal(nodeIds.length, plan.links.length);
      assert.equal(relationshipRows.length, plan.links.length);
      assert.deepEqual(new Set(nodeIds), new Set(relationshipRows.map(({ id }) => id)), "orphan hyperlink relationship");
      assert.equal(new Set(relationshipRows.map(({ target }) => target)).size, relationshipRows.length, "duplicate hyperlink target");
    }
  });
});

test("semantic digest is invariant to a two-way relationship ID swap", () => {
  const first = semanticFixture({
    relationships: [
      { id: "rId1", type: "worksheet", target: "worksheets/sheet1.xml" },
      { id: "rId2", type: "styles", target: "styles.xml" },
    ],
    references: [{ attribute: "r:id", id: "rId1" }, { attribute: "r:embed", id: "rId2" }],
  });
  const swapped = semanticFixture({
    relationships: [
      { id: "rId2", type: "worksheet", target: "worksheets/sheet1.xml" },
      { id: "rId1", type: "styles", target: "styles.xml" },
    ],
    references: [{ attribute: "r:id", id: "rId2" }, { attribute: "r:embed", id: "rId1" }],
  });
  assert.equal(semanticXlsxDigest(first), semanticXlsxDigest(swapped));
});

test("semantic digest is invariant to a three-way relationship ID cycle", () => {
  const first = semanticFixture({
    relationships: [
      { id: "rId1", type: "worksheet", target: "worksheets/sheet1.xml" },
      { id: "rId2", type: "styles", target: "styles.xml" },
      { id: "rId3", type: "theme", target: "theme/theme1.xml" },
    ],
    references: [
      { attribute: "r:id", id: "rId1" },
      { attribute: "r:embed", id: "rId2" },
      { attribute: "r:link", id: "rId3" },
    ],
  });
  const cycled = semanticFixture({
    relationships: [
      { id: "rId2", type: "worksheet", target: "worksheets/sheet1.xml" },
      { id: "rId3", type: "styles", target: "styles.xml" },
      { id: "rId1", type: "theme", target: "theme/theme1.xml" },
    ],
    references: [
      { attribute: "r:id", id: "rId2" },
      { attribute: "r:embed", id: "rId3" },
      { attribute: "r:link", id: "rId1" },
    ],
  });
  assert.equal(semanticXlsxDigest(first), semanticXlsxDigest(cycled));
});

test("semantic digest maps exact relationship QNames without touching QName suffixes, ordinary text, or ordinary attributes", () => {
  const first = semanticFixture({
    relationships: [
      { id: "rId1", type: "worksheet", target: "worksheets/sheet1.xml" },
      { id: "rId2", type: "styles", target: "styles.xml" },
      { id: "rId3", type: "theme", target: "theme/theme1.xml" },
    ],
    references: [
      { attribute: "r:id", id: "rId1" },
      { attribute: "r:embed", id: "rId2" },
      { attribute: "r:link", id: "rId3" },
      { attribute: "foo-r:id", id: "rId1" },
      { attribute: "foo.r:embed", id: "rId2" },
      { attribute: "my_r:link", id: "rId3" },
    ],
    ordinaryText: "rId1",
    ordinaryAttribute: "rId1",
  });
  const renamed = semanticFixture({
    relationships: [
      { id: "alpha", type: "worksheet", target: "worksheets/sheet1.xml" },
      { id: "beta", type: "styles", target: "styles.xml" },
      { id: "gamma", type: "theme", target: "theme/theme1.xml" },
    ],
    references: [
      { attribute: "r:id", id: "alpha" },
      { attribute: "r:embed", id: "beta" },
      { attribute: "r:link", id: "gamma" },
      { attribute: "foo-r:id", id: "rId1" },
      { attribute: "foo.r:embed", id: "rId2" },
      { attribute: "my_r:link", id: "rId3" },
    ],
    ordinaryText: "rId1",
    ordinaryAttribute: "rId1",
  });
  assert.equal(semanticXlsxDigest(first), semanticXlsxDigest(renamed));
});

test("semantic digest rejects an unmapped exact relationship QName", () => {
  const workbook = semanticFixture({
    relationships: [{ id: "known", type: "worksheet", target: "worksheets/sheet1.xml" }],
    references: [{ attribute: "r:id", id: "missing" }],
  });
  assert.throws(() => semanticXlsxDigest(workbook), /未映射.*关系引用.*r:id.*missing/);
});

test("semantic digest distinguishes a real relationship target change", () => {
  const first = semanticFixture({
    relationships: [{ id: "rId1", type: "worksheet", target: "worksheets/sheet1.xml" }],
    references: [{ attribute: "r:id", id: "rId1" }],
  });
  const changed = semanticFixture({
    relationships: [{ id: "different", type: "worksheet", target: "worksheets/sheet2.xml" }],
    references: [{ attribute: "r:id", id: "different" }],
  });
  assert.notEqual(semanticXlsxDigest(first), semanticXlsxDigest(changed));
});

test("generator preserves existing bytes for a relationship-ID-only fresh export and rewrites real content changes", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [first] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, root, { only: ["01-01"] });
    await cycleWorkbookRelationshipIds(first.outputPath);
    const permutedHash = await sha256(first.outputPath);

    const [equivalent] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, root, { only: ["01-01"] });
    assert.equal(await sha256(equivalent.outputPath), permutedHash, "relationship-ID-only fresh export must retain existing bytes");

    const target = inputs.records.find((record) => record.subcategory_code === "01-01");
    const changedRecords = mutateRecords(inputs.records, target.id, "plain_purpose", `${target.plain_purpose}（真实内容变化）`);
    const [changed] = await generateSpreadsheets(changedRecords, inputs.taxonomy, inputs.manifest, root, { only: ["01-01"] });
    assert.notEqual(await sha256(changed.outputPath), permutedHash, "real content changes must rewrite the workbook");
    await verifySpreadsheetFile(changed.outputPath, changed.item, changedRecords, inputs.taxonomy);
  });
});

test("large overview catalogs automatically emit readable high-scale key-range renders", async () => {
  await withTempDir(async (root) => {
    const inputs = await loadInputs(projectRoot);
    const [written] = await generateSpreadsheets(inputs.records, inputs.taxonomy, inputs.manifest, root, { only: ["05-overview"] });
    const rendered = await renderSpreadsheetFile(written.outputPath, path.join(root, "renders"), written.item.key);
    assert.equal(rendered.filter((renderPath) => !path.basename(renderPath).includes("segment")).length, 4);
    const segments = rendered.filter((renderPath) => path.basename(renderPath).includes("segment"));
    assert.ok(segments.length >= 4, "large catalog needs title/header, longest text, longest URL, and last-row segments");
    assert.ok(segments.some((renderPath) => path.basename(renderPath).includes("A1-V5")), "title and header range missing");
    assert.ok(segments.some((renderPath) => path.basename(renderPath).includes("last-row")), "last row range missing");
    for (const renderedPath of segments) {
      const bytes = await fs.readFile(renderedPath);
      assert.ok(bytes.length > 10000, `${renderedPath}: segmented PNG too small`);
      assert.ok(bytes.readUInt32BE(16) >= 2400, `${renderedPath}: segmented PNG not high scale`);
      assert.ok(bytes.readUInt32BE(20) >= 100, `${renderedPath}: segmented PNG height abnormal`);
    }
  });
});
