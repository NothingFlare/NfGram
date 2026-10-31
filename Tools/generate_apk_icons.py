"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

import os
from PIL import Image, ImageDraw

# Input assets
art_dir = r"C:\Users\styuk\.gemini\antigravity\brain\c9f23415-fe4c-4be9-8659-7a2e7d013102"
plane_path = os.path.join(art_dir, "plane_extracted.png")
comb_path = os.path.join(art_dir, "combined_icon.png")

plane = Image.open(plane_path).convert("RGBA")
# trim plane bounding box
plane_cropped = plane.crop(plane.getbbox())

bg_color = (44, 35, 67, 255) # #2c2343

out_dir = r"C:\project\ayugram\Tools\new_icons"
os.makedirs(out_dir, exist_ok=True)

# 1. Adaptive foregrounds: transparent background, plane centered in inner area (approx 44% of total canvas)
foreground_sizes = {
    "NtV.webp": 108,
    "133.webp": 162,
    "9Qo.webp": 216,
    "iE4.webp": 324,
    "5cm.webp": 432,
}

for fname, size in foreground_sizes.items():
    fg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    # scale plane to roughly 48% of total width/height
    target_h = int(size * 0.44)
    ratio = target_h / plane_cropped.height
    target_w = int(plane_cropped.width * ratio)
    p_scaled = plane_cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    x = (size - target_w) // 2
    y = (size - target_h) // 2
    fg.paste(p_scaled, (x, y), p_scaled)
    fg.save(os.path.join(out_dir, fname), "WEBP", quality=95)
    print(f"Saved foreground {fname} ({size}x{size})")

# 2. Legacy icons (squircle / rounded rect):
legacy_sizes = {
    "SnS.webp": 144,
    "sKa.webp": 192,
}

for fname, size in legacy_sizes.items():
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    # draw smooth squircle/rounded rect
    corner_r = int(size * 0.22)
    mask = Image.new("L", (size * 4, size * 4), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size * 4, size * 4], radius=corner_r * 4, fill=255)
    mask = mask.resize((size, size), Image.Resampling.LANCZOS)
    
    bg = Image.new("RGBA", (size, size), bg_color)
    im.paste(bg, (0, 0), mask)
    
    # paste plane in center
    target_h = int(size * 0.58)
    ratio = target_h / plane_cropped.height
    target_w = int(plane_cropped.width * ratio)
    p_scaled = plane_cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    x = (size - target_w) // 2
    y = (size - target_h) // 2
    im.paste(p_scaled, (x, y), p_scaled)
    im.save(os.path.join(out_dir, fname), "WEBP", quality=95)
    print(f"Saved legacy {fname} ({size}x{size})")

# 3. Round icons:
round_sizes = {
    "j_H.webp": 144,
    "-66.webp": 192,
}

for fname, size in round_sizes.items():
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mask = Image.new("L", (size * 4, size * 4), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([0, 0, size * 4, size * 4], fill=255)
    mask = mask.resize((size, size), Image.Resampling.LANCZOS)
    
    bg = Image.new("RGBA", (size, size), bg_color)
    im.paste(bg, (0, 0), mask)
    
    target_h = int(size * 0.54)
    ratio = target_h / plane_cropped.height
    target_w = int(plane_cropped.width * ratio)
    p_scaled = plane_cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    x = (size - target_w) // 2
    y = (size - target_h) // 2
    im.paste(p_scaled, (x, y), p_scaled)
    im.save(os.path.join(out_dir, fname), "WEBP", quality=95)
    print(f"Saved round {fname} ({size}x{size})")
