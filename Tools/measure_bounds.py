"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

from PIL import Image

im = Image.open(r"C:\Users\styuk\.gemini\antigravity\brain\4c610949-e656-421a-ae6d-8aca6746124b\.user_uploaded\media_1792704435865_2bc3c290.png").convert("RGBA")
# find bounds of red pixels (r > 200, g < 100, b < 100)
min_x, min_y, max_x, max_y = 10000, 10000, 0, 0
for x in range(im.width):
    for y in range(im.height):
        r, g, b, a = im.getpixel((x, y))
        if r > 180 and g < 80 and b < 80:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

print(f"Ref red squircle bounds: x=[{min_x}, {max_x}], y=[{min_y}, {max_y}], w={max_x-min_x}, h={max_y-min_y}")

# In live preview:
im2 = Image.open(r"C:\Users\styuk\.gemini\antigravity\brain\4c610949-e656-421a-ae6d-8aca6746124b\screen_live_preview.png").convert("RGBA")
min_x2, min_y2, max_x2, max_y2 = 10000, 10000, 0, 0
for x in range(im2.width):
    for y in range(im2.height):
        r, g, b, a = im2.getpixel((x, y))
        if r > 180 and g < 80 and b < 80:
            min_x2 = min(min_x2, x)
            min_y2 = min(min_y2, y)
            max_x2 = max(max_x2, x)
            max_y2 = max(max_y2, y)

print(f"Live red squircle bounds: x=[{min_x2}, {max_x2}], y=[{min_y2}, {max_y2}], w={max_x2-min_x2}, h={max_y2-min_y2}")
