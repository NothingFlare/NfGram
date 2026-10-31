"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

from PIL import Image

im_ref = Image.open(r"C:\Users\styuk\.gemini\antigravity\brain\4c610949-e656-421a-ae6d-8aca6746124b\.user_uploaded\media_1792704435865_2bc3c290.png")
im_live = Image.open(r"C:\Users\styuk\.gemini\antigravity\brain\4c610949-e656-421a-ae6d-8aca6746124b\screen_live_preview.png")

print("Ref size:", im_ref.size)
print("Live size:", im_live.size)
