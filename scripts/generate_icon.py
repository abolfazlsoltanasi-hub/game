"""Generate the transparent high-resolution Word Guess app icon."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

SIZE = 1024
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "icon.png"

base = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
cx = cy = SIZE // 2

glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for radius, color, width in (
    (358, (168, 85, 247, 80), 52),
    (263, (6, 182, 212, 62), 48),
    (166, (196, 181, 253, 56), 43),
):
    gd.ellipse(
        (cx-radius, cy-radius, cx+radius, cy+radius),
        outline=color,
        width=width,
    )
base = Image.alpha_composite(base, glow.filter(ImageFilter.GaussianBlur(28)))

d = ImageDraw.Draw(base)
d.ellipse((cx-350, cy-350, cx+350, cy+350), outline=(184, 138, 255, 245), width=42)
d.ellipse((cx-252, cy-252, cx+252, cy+252), outline=(94, 231, 245, 245), width=38)
d.ellipse((cx-155, cy-155, cx+155, cy+155), outline=(244, 241, 255, 248), width=34)
d.ellipse((cx-68, cy-68, cx+68, cy+68), fill=(255, 209, 102, 255))
d.ellipse((cx-27, cy-27, cx+27, cy+27), fill=(255, 250, 230, 255))

dart_glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
ImageDraw.Draw(dart_glow).line([(650, 350), (546, 454)], fill=(94, 231, 245, 180), width=35)
base = Image.alpha_composite(base, dart_glow.filter(ImageFilter.GaussianBlur(18)))
d = ImageDraw.Draw(base)
d.line([(650, 350), (546, 454)], fill=(245, 247, 255, 255), width=24)
d.polygon([(680, 310), (638, 330), (665, 360)], fill=(255, 209, 102, 255))
d.polygon([(638, 330), (610, 338), (636, 355)], fill=(168, 85, 247, 255))
d.ellipse((260, 274, 278, 292), fill=(255, 255, 255, 210))
d.ellipse((730, 600, 742, 612), fill=(94, 231, 245, 220))

base.save(OUT, format="PNG", optimize=True)
print(f"Generated {OUT} ({OUT.stat().st_size} bytes)")
