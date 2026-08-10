#!/usr/bin/env python3
"""构造最小合法 pdf 作为测试夹具。

要求（T4.3）：
- 2 页，每页 MediaBox = [0 0 612 792]（US Letter）
- 仅用 Python 3.8+ 标准库
"""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent / "minimal.pdf"


def build(out_path: Path = OUT) -> Path:
    """生成 minimal.pdf（2 页，US Letter）。"""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 对象编号与内容
    objs = {}
    objs[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    objs[2] = b"<< /Type /Pages /Kids [3 0 R 5 0 R] /Count 2 >>"
    objs[3] = (
        b"<< /Type /Page /Parent 2 0 R "
        b"/MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 7 0 R >> >> "
        b"/Contents 4 0 R >>"
    )
    stream1 = (
        b"BT\n/F1 12 Tf\n72 750 Td\n"
        b"(Page 1: Test PDF for XFDF fixtures) Tj\n"
        b"0 -20 Td\n(Line 2) Tj\nET\n"
    )
    objs[4] = b"<< /Length " + str(len(stream1)).encode() + b" >>\nstream\n" + stream1 + b"endstream"
    objs[5] = (
        b"<< /Type /Page /Parent 2 0 R "
        b"/MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 7 0 R >> >> "
        b"/Contents 6 0 R >>"
    )
    stream2 = b"BT\n/F1 12 Tf\n72 750 Td\n(Page 2) Tj\nET\n"
    objs[6] = b"<< /Length " + str(len(stream2)).encode() + b" >>\nstream\n" + stream2 + b"endstream"
    objs[7] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"

    # 拼装
    parts: list[bytes] = [b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"]
    offsets: list[int] = [0]
    for obj_id in sorted(objs.keys()):
        current_offset = sum(len(p) for p in parts)
        offsets.append(current_offset)
        parts.append(f"{obj_id} 0 obj\n".encode() + objs[obj_id] + b"\nendobj\n")

    xref_offset = sum(len(p) for p in parts)
    xref = f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n"
    for off in offsets[1:]:
        xref += f"{off:010d} 00000 n \n"

    parts.append(xref.encode())
    parts.append(
        f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode()
    )

    out_path.write_bytes(b"".join(parts))
    return out_path


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
