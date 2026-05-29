#!/usr/bin/env python3
"""
Analyze dominant hue of each image, classify into color categories,
generate thumbnails, and output a JSON manifest.
"""
import os, json, colorsys
from PIL import Image

IMAGES_DIR = "images"
THUMBS_DIR = "thumbs"
THUMB_SIZE = (400, 400)

os.makedirs(THUMBS_DIR, exist_ok=True)

def dominant_hue(img_path):
    """Return (h, s, v) of the most saturated cluster in the image."""
    img = Image.open(img_path).convert("RGB")
    # Downsample for speed
    img.thumbnail((100, 100))
    pixels = list(img.getdata())

    # Collect HSV values, ignore very dark/light/desaturated pixels
    hsv_pixels = []
    for r, g, b in pixels:
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        if s > 0.15 and 0.1 < v < 0.95:
            hsv_pixels.append((h, s, v))

    if not hsv_pixels:
        # Fallback: use average of all pixels
        avg_r = sum(p[0] for p in pixels) / len(pixels)
        avg_g = sum(p[1] for p in pixels) / len(pixels)
        avg_b = sum(p[2] for p in pixels) / len(pixels)
        h, s, v = colorsys.rgb_to_hsv(avg_r/255, avg_g/255, avg_b/255)
        return h, s, v

    # Weight by saturation — more saturated pixels dominate
    total_s = sum(p[1] for p in hsv_pixels)
    avg_h = sum(p[0] * p[1] for p in hsv_pixels) / total_s
    avg_s = total_s / len(hsv_pixels)
    avg_v = sum(p[2] for p in hsv_pixels) / len(hsv_pixels)
    return avg_h, avg_s, avg_v

def classify_hue(h, s, v):
    """Map hue (0-1) to color category name."""
    # Low saturation → gray/neutral, classify by brightness
    if s < 0.12:
        return "neutral"

    deg = h * 360
    if deg < 15 or deg >= 345:
        return "red"
    elif deg < 40:
        return "orange"
    elif deg < 70:
        return "yellow"
    elif deg < 150:
        return "green"
    elif deg < 195:
        return "cyan"
    elif deg < 255:
        return "blue"
    elif deg < 285:
        return "purple"
    elif deg < 345:
        return "pink"
    return "red"

results = []
files = sorted(f for f in os.listdir(IMAGES_DIR) if f.lower().endswith((".jpeg", ".jpg", ".png")))

for fname in files:
    fpath = os.path.join(IMAGES_DIR, fname)
    try:
        h, s, v = dominant_hue(fpath)
        cat = classify_hue(h, s, v)

        # Generate thumbnail
        thumb_name = fname
        thumb_path = os.path.join(THUMBS_DIR, thumb_name)
        if not os.path.exists(thumb_path):
            img = Image.open(fpath)
            img.thumbnail(THUMB_SIZE, Image.LANCZOS)
            img.save(thumb_path, "JPEG", quality=75, optimize=True)

        results.append({
            "file": fname,
            "cat": cat,
            "h": round(h * 360, 1),
            "s": round(s, 3),
            "v": round(v, 3),
        })
        print(f"{fname:60s}  {cat:8s}  h={h*360:5.1f}  s={s:.2f}  v={v:.2f}")
    except Exception as e:
        print(f"ERROR {fname}: {e}")

# Save manifest
with open("gallery_manifest.json", "w") as f:
    json.dump(results, f, indent=2)

# Print category summary
from collections import Counter
cats = Counter(r["cat"] for r in results)
print("\n=== Category Summary ===")
for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {cat:10s}: {count}")
print(f"\nTotal: {len(results)} images")
