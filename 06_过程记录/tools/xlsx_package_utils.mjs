import fs from "node:fs/promises";
import crypto from "node:crypto";
import { deflateRawSync, inflateRawSync } from "node:zlib";

function findEndOfCentralDirectory(buffer) {
  const minimum = Math.max(0, buffer.length - 65557);
  for (let offset = buffer.length - 22; offset >= minimum; offset -= 1) {
    if (buffer.readUInt32LE(offset) === 0x06054b50) return offset;
  }
  throw new Error("XLSX ZIP 末尾目录不存在");
}

export function unzipEntries(buffer) {
  const eocd = findEndOfCentralDirectory(buffer);
  const entryCount = buffer.readUInt16LE(eocd + 10);
  let cursor = buffer.readUInt32LE(eocd + 16);
  const entries = new Map();
  for (let index = 0; index < entryCount; index += 1) {
    if (buffer.readUInt32LE(cursor) !== 0x02014b50) throw new Error("XLSX ZIP 中央目录损坏");
    const method = buffer.readUInt16LE(cursor + 10);
    const compressedSize = buffer.readUInt32LE(cursor + 20);
    const uncompressedSize = buffer.readUInt32LE(cursor + 24);
    const nameLength = buffer.readUInt16LE(cursor + 28);
    const extraLength = buffer.readUInt16LE(cursor + 30);
    const commentLength = buffer.readUInt16LE(cursor + 32);
    const localOffset = buffer.readUInt32LE(cursor + 42);
    const name = buffer.subarray(cursor + 46, cursor + 46 + nameLength).toString("utf8").replaceAll("\\", "/");
    if (buffer.readUInt32LE(localOffset) !== 0x04034b50) throw new Error(`XLSX ZIP 本地目录损坏: ${name}`);
    const localNameLength = buffer.readUInt16LE(localOffset + 26);
    const localExtraLength = buffer.readUInt16LE(localOffset + 28);
    const dataOffset = localOffset + 30 + localNameLength + localExtraLength;
    const compressed = buffer.subarray(dataOffset, dataOffset + compressedSize);
    let content;
    if (method === 0) content = Buffer.from(compressed);
    else if (method === 8) content = inflateRawSync(compressed);
    else throw new Error(`XLSX ZIP 使用不支持的压缩方法 ${method}: ${name}`);
    if (content.length !== uncompressedSize) throw new Error(`XLSX ZIP 解压长度不符: ${name}`);
    entries.set(name, content);
    cursor += 46 + nameLength + extraLength + commentLength;
  }
  return entries;
}

let crcTable;
function makeCrcTable() {
  if (crcTable) return crcTable;
  crcTable = Array.from({ length: 256 }, (_, index) => {
    let value = index;
    for (let bit = 0; bit < 8; bit += 1) value = (value & 1) ? (0xedb88320 ^ (value >>> 1)) : (value >>> 1);
    return value >>> 0;
  });
  return crcTable;
}

function crc32(buffer) {
  const table = makeCrcTable();
  let crc = 0xffffffff;
  for (const byte of buffer) crc = table[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  return (crc ^ 0xffffffff) >>> 0;
}

export function zipEntries(entries) {
  const localParts = [];
  const centralParts = [];
  let offset = 0;
  const names = [...entries.keys()].sort((left, right) => left.localeCompare(right));
  const dosTime = 0;
  const dosDate = ((2026 - 1980) << 9) | (8 << 5) | 7;
  for (const name of names) {
    const data = Buffer.from(entries.get(name));
    const compressed = deflateRawSync(data, { level: 9 });
    const nameBytes = Buffer.from(name, "utf8");
    const checksum = crc32(data);
    const local = Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(20, 4);
    local.writeUInt16LE(0x0800, 6);
    local.writeUInt16LE(8, 8);
    local.writeUInt16LE(dosTime, 10);
    local.writeUInt16LE(dosDate, 12);
    local.writeUInt32LE(checksum, 14);
    local.writeUInt32LE(compressed.length, 18);
    local.writeUInt32LE(data.length, 22);
    local.writeUInt16LE(nameBytes.length, 26);
    local.writeUInt16LE(0, 28);
    localParts.push(local, nameBytes, compressed);

    const central = Buffer.alloc(46);
    central.writeUInt32LE(0x02014b50, 0);
    central.writeUInt16LE(20, 4);
    central.writeUInt16LE(20, 6);
    central.writeUInt16LE(0x0800, 8);
    central.writeUInt16LE(8, 10);
    central.writeUInt16LE(dosTime, 12);
    central.writeUInt16LE(dosDate, 14);
    central.writeUInt32LE(checksum, 16);
    central.writeUInt32LE(compressed.length, 20);
    central.writeUInt32LE(data.length, 24);
    central.writeUInt16LE(nameBytes.length, 28);
    central.writeUInt16LE(0, 30);
    central.writeUInt16LE(0, 32);
    central.writeUInt16LE(0, 34);
    central.writeUInt16LE(0, 36);
    central.writeUInt32LE(0, 38);
    central.writeUInt32LE(offset, 42);
    centralParts.push(central, nameBytes);
    offset += local.length + nameBytes.length + compressed.length;
  }
  const centralDirectory = Buffer.concat(centralParts);
  const eocd = Buffer.alloc(22);
  eocd.writeUInt32LE(0x06054b50, 0);
  eocd.writeUInt16LE(0, 4);
  eocd.writeUInt16LE(0, 6);
  eocd.writeUInt16LE(names.length, 8);
  eocd.writeUInt16LE(names.length, 10);
  eocd.writeUInt32LE(centralDirectory.length, 12);
  eocd.writeUInt32LE(offset, 16);
  eocd.writeUInt16LE(0, 20);
  return Buffer.concat([...localParts, centralDirectory, eocd]);
}

function xmlEscape(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll('"', "&quot;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function relationshipSourcePath(relationshipPath) {
  if (relationshipPath === "_rels/.rels") return null;
  const match = relationshipPath.match(/^(.*)\/_rels\/([^/]+)\.rels$/);
  return match ? `${match[1]}/${match[2]}` : null;
}

function canonicalizeRelationshipsForComparison(entries) {
  for (const relationshipPath of [...entries.keys()].filter((name) => name.endsWith(".rels")).sort()) {
    let xml = entries.get(relationshipPath).toString("utf8");
    const elements = [...xml.matchAll(/<Relationship\b[^>]*\/?\s*>/g)].map((match) => match[0]);
    if (!elements.length) continue;
    const parsed = elements.map((element) => {
      const attributes = Object.fromEntries([...element.matchAll(/([A-Za-z:]+)="([^"]*)"/g)].map((match) => [match[1], match[2]]));
      if (!attributes.Id || !attributes.Type || !attributes.Target) throw new Error(`XLSX 关系缺少 Id/Type/Target: ${relationshipPath}`);
      return { attributes };
    }).sort((left, right) => `${left.attributes.Type}|${left.attributes.Target}|${left.attributes.TargetMode ?? ""}`.localeCompare(`${right.attributes.Type}|${right.attributes.Target}|${right.attributes.TargetMode ?? ""}`));
    const mapping = new Map();
    for (let index = 0; index < parsed.length; index += 1) {
      const oldId = parsed[index].attributes.Id;
      if (mapping.has(oldId)) throw new Error(`XLSX 关系 ID 重复: ${relationshipPath}#${oldId}`);
      mapping.set(oldId, `rId${index + 1}`);
    }
    const rebuilt = parsed.map((item, index) => {
      const targetMode = item.attributes.TargetMode ? ` TargetMode="${item.attributes.TargetMode}"` : "";
      return `<Relationship Id="rId${index + 1}" Type="${item.attributes.Type}" Target="${item.attributes.Target}"${targetMode} />`;
    }).join("");
    xml = xml.replace(/<Relationship\b[^>]*\/?\s*>/g, "").replace(/<\/Relationships>/, `${rebuilt}</Relationships>`);
    entries.set(relationshipPath, Buffer.from(xml, "utf8"));
    const sourcePath = relationshipSourcePath(relationshipPath);
    if (sourcePath && entries.has(sourcePath)) {
      const sourceXml = entries.get(sourcePath).toString("utf8").replace(
        /\b(r:(?:id|embed|link))="([^"]+)"/g,
        (match, attribute, oldId) => mapping.has(oldId) ? `${attribute}="${mapping.get(oldId)}"` : match,
      );
      entries.set(sourcePath, Buffer.from(sourceXml, "utf8"));
    }
  }
}

export function semanticXlsxDigest(buffer) {
  const entries = new Map([...unzipEntries(buffer)].map(([name, bytes]) => [name, Buffer.from(bytes)]));
  canonicalizeRelationshipsForComparison(entries);
  return crypto.createHash("sha256").update(zipEntries(entries)).digest("hex");
}

function addHyperlinks(entries, sheetPath, links) {
  if (!links.length) return;
  let sheetXml = entries.get(sheetPath)?.toString("utf8");
  if (!sheetXml) throw new Error(`XLSX 缺少超链接目标工作表: ${sheetPath}`);
  sheetXml = sheetXml.replace(/<x:worksheet\b([^>]*)>/, (match, attributes) => attributes.includes("xmlns:r=")
    ? match
    : `<x:worksheet${attributes} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">`);
  sheetXml = sheetXml.replace(/<x:hyperlinks>.*?<\/x:hyperlinks>/s, "");
  const relationshipPath = sheetPath.replace(/^(.*)\/([^/]+)$/, "$1/_rels/$2.rels");
  let relationshipsXml = entries.get(relationshipPath)?.toString("utf8")
    ?? '<?xml version="1.0" encoding="utf-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>';
  relationshipsXml = relationshipsXml.replace(
    /<Relationship\b(?=[^>]*\bType="[^"]*\/hyperlink")[^>]*\/?\s*>/g,
    "",
  );
  const existingIds = new Set([...relationshipsXml.matchAll(/\bId="([^"]+)"/g)].map((match) => match[1]));
  const hyperlinkXml = [];
  for (let index = 0; index < links.length; index += 1) {
    let relationshipId = `rIdHyperlink${index + 1}`;
    let suffix = 1;
    while (existingIds.has(relationshipId)) {
      relationshipId = `rIdHyperlink${index + 1}_${suffix}`;
      suffix += 1;
    }
    existingIds.add(relationshipId);
    hyperlinkXml.push(`<x:hyperlink ref="${xmlEscape(links[index].ref)}" r:id="${relationshipId}" />`);
    relationshipsXml = relationshipsXml.replace(
      /<\/Relationships>/,
      `<Relationship Id="${relationshipId}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="${xmlEscape(links[index].target)}" TargetMode="External" /></Relationships>`,
    );
  }
  const block = `<x:hyperlinks>${hyperlinkXml.join("")}</x:hyperlinks>`;
  if (/<x:tableParts\b/.test(sheetXml)) sheetXml = sheetXml.replace(/<x:tableParts\b/, `${block}<x:tableParts`);
  else sheetXml = sheetXml.replace(/<\/x:worksheet>/, `${block}</x:worksheet>`);
  entries.set(sheetPath, Buffer.from(sheetXml, "utf8"));
  entries.set(relationshipPath, Buffer.from(relationshipsXml, "utf8"));
}

function addFreezePane(entries, sheetPath, freeze) {
  let sheetXml = entries.get(sheetPath)?.toString("utf8");
  if (!sheetXml) throw new Error(`XLSX 缺少冻结窗格目标工作表: ${sheetPath}`);
  sheetXml = sheetXml.replace(/<x:pane\b[^>]*\/?\s*>/g, "");
  const attributes = [
    freeze.xSplit ? `xSplit="${freeze.xSplit}"` : "",
    freeze.ySplit ? `ySplit="${freeze.ySplit}"` : "",
    `topLeftCell="${freeze.topLeftCell}"`,
    `activePane="${freeze.activePane}"`,
    'state="frozen"',
  ].filter(Boolean).join(" ");
  const pane = `<x:pane ${attributes} />`;
  sheetXml = sheetXml.replace(/<x:sheetView\b([^>]*)>(.*?)<\/x:sheetView>/s, `<x:sheetView$1>${pane}$2</x:sheetView>`);
  if (!sheetXml.includes(pane)) {
    sheetXml = sheetXml.replace(/<x:sheetView\b([^>]*)\/>/, `<x:sheetView$1>${pane}</x:sheetView>`);
  }
  if (!sheetXml.includes(pane)) throw new Error(`XLSX 无法写入冻结窗格: ${sheetPath}`);
  entries.set(sheetPath, Buffer.from(sheetXml, "utf8"));
}

export async function normalizeXlsxPackage(filePath, hyperlinkPlan = [], freezePlan = []) {
  const entries = unzipEntries(await fs.readFile(filePath));
  for (const plan of hyperlinkPlan) addHyperlinks(entries, plan.sheetPath, plan.links);
  for (const plan of freezePlan) addFreezePane(entries, plan.sheetPath, plan);
  await fs.writeFile(filePath, zipEntries(entries));
}
