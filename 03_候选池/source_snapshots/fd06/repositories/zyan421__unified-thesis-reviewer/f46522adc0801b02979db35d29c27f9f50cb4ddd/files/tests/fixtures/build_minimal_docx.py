#!/usr/bin/env python3
"""构造最小合法 docx 作为测试夹具。

要求（T4.2）：
- 至少 10 段正文
- 1 个 2x2 表格
- 至少 1 段含多 run（不同 rPr，比如加粗 + 斜体）
- 仅用 Python 3.8+ 标准库
"""
from __future__ import annotations

import zipfile
from pathlib import Path

OUT = Path(__file__).resolve().parent / "minimal.docx"

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

STYLES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:style w:type="character" w:styleId="CommentReference">
<w:name w:val="annotation reference"/>
<w:rPr><w:sz w:val="16"/></w:rPr>
</w:style>
</w:styles>"""

DOCUMENT_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
<w:p><w:r><w:t>第一章 引言</w:t></w:r></w:p>
<w:p><w:r><w:t xml:space="preserve">本文研究个人信息保护法下知情同意制度的完善。</w:t></w:r></w:p>
<w:p><w:r><w:t>1.1 研究背景</w:t></w:r></w:p>
<w:p><w:r><w:t xml:space="preserve">个人信息保护成为数字时代的重要议题。</w:t></w:r></w:p>
<w:p><w:r><w:t>第二章 知情同意的理论基础</w:t></w:r></w:p>
<w:p><w:r><w:t xml:space="preserve">§2.1 学说概览:</w:t></w:r><w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">Beauchamp</w:t></w:r><w:r><w:t xml:space="preserve">、</w:t></w:r><w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">Fischer</w:t></w:r><w:r><w:t xml:space="preserve">、Childress 三位学者均认为同意应具备充分知情。</w:t></w:r></w:p>
<w:p><w:r><w:t>§2.2 法理基础</w:t></w:r></w:p>
<w:p><w:r><w:t xml:space="preserve">知情同意的法理基础可从合同说、信义说、风险分担说三个维度展开。</w:t></w:r></w:p>
<w:p><w:r><w:t>第三章 样本分析</w:t></w:r></w:p>
<w:tbl>
<w:tblPr><w:tblW w:w="0" w:type="auto"/></w:tblPr>
<w:tblGrid><w:gridCol w:w="2500"/><w:gridCol w:w="2500"/></w:tblGrid>
<w:tr><w:tc><w:tcPr><w:tcW w:w="2500" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>平台</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w="2500" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>样本量</w:t></w:r></w:p></w:tc></w:tr>
<w:tr><w:tc><w:tcPr><w:tcW w:w="2500" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>头部平台</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:w="2500" w:type="dxa"/></w:tcPr><w:p><w:r><w:t xml:space="preserve">N=127</w:t></w:r></w:p></w:tc></w:tr>
</w:tbl>
<w:p><w:r><w:t>第四章 规范适用</w:t></w:r></w:p>
<w:p><w:r><w:t xml:space="preserve">§4.3.2 第 1 段讨论合法性基础。</w:t></w:r></w:p>
<w:p><w:r><w:t>第五章 对策建议</w:t></w:r></w:p>
<w:p><w:r><w:t xml:space="preserve">§5.1 语言规范:法治建设需要完善的法制作为支撑。</w:t></w:r></w:p>
<w:p><w:r><w:t>结语</w:t></w:r></w:p>
<w:p><w:r><w:t xml:space="preserve">本文研究尚有不足,期待后续完善。</w:t></w:r></w:p>
<w:sectPr><w:pgSz w:w="12240" w:h="15840"/></w:sectPr>
</w:body>
</w:document>"""

CORE_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:title>最小测试论文(含表格)</dc:title>
<dc:creator>unified-thesis-reviewer tests</dc:creator>
</cp:coreProperties>"""


def build(out_path: Path = OUT) -> Path:
    """生成 minimal.docx 并返回路径。"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("word/document.xml", DOCUMENT_XML)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES_XML)
        z.writestr("docProps/core.xml", CORE_XML)
    return out_path


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
