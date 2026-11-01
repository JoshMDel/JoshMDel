"""One-off image preparation: resizes/compresses source photos into web assets.
Usage: python3 tools/prepare_images.py <uploads_dir>
"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
U = lambda n: os.path.join(SRC, n)

def save_variants(im, name, widths, q=78):
    for w in widths:
        r = im.copy()
        if r.width > w:
            r = r.resize((w, round(r.height * w / r.width)), Image.LANCZOS)
        r.save(os.path.join(OUT, f"{name}-{w}.webp"), "WEBP", quality=q, method=6)
        r.convert("RGB").save(os.path.join(OUT, f"{name}-{w}.jpg"), "JPEG", quality=q, optimize=True, progressive=True)

# --- Logo: circle version + white-on-transparent version ---
logo = Image.open(U("a7d50f8e-image.jpg")).convert("L")
W, H = logo.size
mask = Image.new("L", logo.size, 0)
ImageDraw.Draw(mask).ellipse((40, 40, W - 40, H - 40), fill=255)
# white text on transparent (for dark UI)
alpha = ImageOps.invert(logo)
textbox = Image.new("L", logo.size, 0)
ImageDraw.Draw(textbox).rectangle((120, 430, 975, 790), fill=255)
alpha = Image.composite(alpha, Image.new("L", logo.size, 0), textbox)
alpha = alpha.point(lambda p: 0 if p < 40 else min(255, int(p * 1.15)))
white = Image.new("RGBA", logo.size, (255, 255, 255, 0))
white.putalpha(alpha)
bbox = alpha.getbbox()
white = white.crop((bbox[0] - 6, bbox[1] - 6, bbox[2] + 6, bbox[3] + 6))
for w in (240, 480):
    r = white.resize((w, round(white.height * w / white.width)), Image.LANCZOS)
    r.save(os.path.join(OUT, f"radc-logo-white-{w}.png"), optimize=True)
    r.save(os.path.join(OUT, f"radc-logo-white-{w}.webp"), "WEBP", quality=90)
# circle logo (for schema logo, favicon, social)
circ = Image.open(U("a7d50f8e-image.jpg")).convert("RGB")
c = Image.new("RGBA", circ.size, (0, 0, 0, 0))
m2 = Image.new("L", circ.size, 0)
ImageDraw.Draw(m2).ellipse((38, 38, W - 38, H - 38), fill=255)
c.paste(circ, (0, 0), m2)
c = c.crop((30, 30, W - 30, H - 30))
c.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT, "radc-logo-512.png"), optimize=True)
c.resize((192, 192), Image.LANCZOS).save(os.path.join(OUT, "radc-logo-192.png"), optimize=True)
c.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)
c.resize((48, 48), Image.LANCZOS).save(os.path.join(OUT, "..", "..", "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

# --- Photos ---
civic_front = Image.open(U("2830bbd8-image.webp")).convert("RGB")   # headlight close-up 1080x1620
civic_night = Image.open(U("fbcf92ba-image.webp")).convert("RGB")   # full car at night 1080x1440
headlight_before = Image.open(U("49cdb304-image.jpg")).convert("RGB")  # oxidised headlight 860x460

save_variants(civic_front, "honda-civic-headlight-detail-oudtshoorn", (480, 800, 1080))
save_variants(civic_night, "honda-civic-paint-correction-gloss", (480, 800, 1080))
save_variants(headlight_before, "oxidised-headlight-before-restoration", (430, 860))

# Hero: landscape crop of night shot
hero = civic_night.crop((0, 380, 1080, 1188))  # 1080x808
save_variants(hero, "radc-hero-civic-gloss", (640, 1080))

# --- Open Graph image 1200x630 ---
og = Image.new("RGB", (1200, 630), (6, 9, 16))
bg = civic_night.crop((0, 420, 1080, 987)).resize((1200, 630), Image.LANCZOS)
og.paste(bg, (0, 0))
grad = Image.new("L", (1200, 630))
gd = ImageDraw.Draw(grad)
for x in range(1200):
    gd.line([(x, 0), (x, 630)], fill=int(max(0, 235 - x * 0.28)))
og.paste(Image.new("RGB", (1200, 630), (6, 9, 16)), (0, 0), grad)
lw = white.resize((340, round(white.height * 380 / white.width)), Image.LANCZOS)
og.paste(lw, (60, 70), lw)
f_big = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf", 54)
f_sm = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBoldItalic.otf", 28)
d = ImageDraw.Draw(og)
y = 70 + lw.height + 40
d.text((60, y), "Car Detailing in", font=f_big, fill=(255, 255, 255))
d.text((60, y + 64), "Oudtshoorn", font=f_big, fill=(30, 144, 255))
d.text((60, y + 146), "Ceramic coating · Paint correction · Valets", font=f_sm, fill=(210, 220, 235))
d.text((60, y + 184), "Garden Route & Karoo · 081 087 6539", font=f_sm, fill=(210, 220, 235))
og.save(os.path.join(OUT, "og-radc-car-detailing-oudtshoorn.jpg"), "JPEG", quality=85, optimize=True)
print("done")
