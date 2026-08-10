#!/usr/bin/env python3
"""
extract-pdf-text.py —— v2.0.0 新增

从 pdf 中提取文本 + 页面/段落/行级别的精确坐标，输出结构化 JSON。
Agent 在生成 issues.json 的 anchor_text 和 bbox 字段时可消费此脚本产物。

用法：
    python3 extract-pdf-text.py <input.pdf> <output.positions.json>

输出 JSON 结构：
{
  "schema_version": "1.0",
  "pdf_path": "...",
  "page_count": N,
  "pages": [
    {
      "page": 1,                       // 1-based
      "width": 595.28,                  // page width in points
      "height": 841.89,
      "blocks": [
        {
          "block_index": 0,
          "bbox": [x0, y0, x1, y1],     // 左下原点，y 向上
          "text": "...",
          "lines": [
            {"text": "...", "bbox": [...]}
          ]
        }
      ],
      "plain_text": "整页连接后的纯文本"
    }
  ],
  "full_text": "全书连接后的纯文本"
}

依赖：PyMuPDF
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    print("error: PyMuPDF is required. pip install --user PyMuPDF", file=sys.stderr)
    sys.exit(10)


def extract(pdf_path: Path) -> dict:
    doc = fitz.open(pdf_path)
    out = {
        "schema_version": "1.0",
        "pdf_path": str(pdf_path),
        "page_count": doc.page_count,
        "pages": [],
    }
    all_text: list[str] = []

    for page_idx in range(doc.page_count):
        page = doc[page_idx]
        page_h = page.rect.height

        page_record = {
            "page": page_idx + 1,
            "width": round(page.rect.width, 2),
            "height": round(page_h, 2),
            "blocks": [],
            "plain_text": "",
        }

        # 用 get_text("dict") 取结构化数据
        text_dict = page.get_text("dict")
        for b_idx, block in enumerate(text_dict.get("blocks", [])):
            if block.get("type", 0) != 0:
                continue  # 非文本块（图片等）跳过
            x0, y0, x1, y1 = block["bbox"]
            # 坐标系：PyMuPDF 是左上原点 y 向下；转为我们约定的左下原点 y 向上
            bbox_converted = [
                round(x0, 2),
                round(page_h - y1, 2),
                round(x1, 2),
                round(page_h - y0, 2),
            ]

            lines_data = []
            block_text_parts = []
            for line in block.get("lines", []):
                line_text = "".join(span.get("text", "") for span in line.get("spans", []))
                if line_text.strip():
                    lx0, ly0, lx1, ly1 = line["bbox"]
                    lines_data.append({
                        "text": line_text,
                        "bbox": [
                            round(lx0, 2),
                            round(page_h - ly1, 2),
                            round(lx1, 2),
                            round(page_h - ly0, 2),
                        ],
                    })
                    block_text_parts.append(line_text)

            block_text = "\n".join(block_text_parts)
            if block_text.strip():
                page_record["blocks"].append({
                    "block_index": b_idx,
                    "bbox": bbox_converted,
                    "text": block_text,
                    "lines": lines_data,
                })

        # plain_text：页面纯文本（与 PyMuPDF 的默认 get_text 一致）
        page_plain = page.get_text()
        page_record["plain_text"] = page_plain
        all_text.append(page_plain)

        out["pages"].append(page_record)

    out["full_text"] = "\n".join(all_text)
    doc.close()
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="extract-pdf-text",
        description="Extract pdf text with positional metadata (v2.0.0).",
    )
    ap.add_argument("src_pdf", type=Path)
    ap.add_argument("out_json", type=Path)
    args = ap.parse_args(argv if argv is not None else sys.argv[1:])

    if not args.src_pdf.is_file():
        print(f"error: pdf not found: {args.src_pdf}", file=sys.stderr)
        return 2

    data = extract(args.src_pdf)
    args.out_json.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"[extract-pdf-text] wrote {args.out_json} "
        f"(pages={data['page_count']}, full_text={len(data['full_text'])} chars)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
