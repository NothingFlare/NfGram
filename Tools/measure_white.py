"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

from PIL import Image

im = Image.open(r"C:\Users\styuk\.gemini\antigravity\brain\4c610949-e656-421a-ae6d-8aca6746124b\.user_uploaded\media_1792704435865_2bc3c290.png").convert("RGBA")
# find bounds of white pixels (r > 240, g > 240, b > 240) in the first squircle (y between 40 and 130)
min_x, min_y, max_x, max_y = 10000, 10000, 0, 0
for x in range(60, 160):
    for y in range(40, 130):
        r, g, b, a = im.getpixel((x, y))
        if r > 240 and g > 240 and b > 240:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

print(f"White airplane in Photo 2: x=[{min_x}, {max_x}], y=[{min_y}, {max_y}], w={max_x-min_x}, h={max_y-min_y}")
