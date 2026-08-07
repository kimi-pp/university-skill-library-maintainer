"""把 DOCX 逐页渲染图拼成带页码的 QA 总览。"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


project_root = Path(__file__).resolve().parents[2]
render_root = project_root / "06_过程记录" / "renders" / "docx_final"
font = ImageFont.load_default()

for category in ("01", "02", "03"):
    category_dir = render_root / category
    pages = sorted(
        category_dir.glob("page-*.png"),
        key=lambda item: int(item.stem.split("-")[-1]),
    )
    thumb_width = 260
    label_height = 26
    columns = 4
    first = Image.open(pages[0]).convert("RGB")
    thumb_height = round(first.height * thumb_width / first.width)
    rows = (len(pages) + columns - 1) // columns
    contact = Image.new("RGB", (columns * thumb_width, rows * (thumb_height + label_height)), "#D8DEE5")
    draw = ImageDraw.Draw(contact)
    for index, page_path in enumerate(pages):
        page = Image.open(page_path).convert("RGB")
        page.thumbnail((thumb_width, thumb_height))
        column = index % columns
        row = index // columns
        x = column * thumb_width + (thumb_width - page.width) // 2
        y = row * (thumb_height + label_height) + label_height
        contact.paste(page, (x, y))
        draw.rectangle((column * thumb_width, row * (thumb_height + label_height), (column + 1) * thumb_width, row * (thumb_height + label_height) + label_height), fill="#16324F")
        draw.text((column * thumb_width + 8, row * (thumb_height + label_height) + 7), f"Page {index + 1}", fill="white", font=font)
    contact.save(render_root / f"{category}_contact_sheet.png")
    print(f"{category}: {len(pages)} pages")
