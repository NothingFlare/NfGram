"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

import zipfile

with zipfile.ZipFile(r"c:\Users\styuk\Downloads\AyuGram Desktop\vanilla-AyuGram-full-20261005.apk", "r") as z:
    d = z.read("lib/arm64-v8a/libtmessages.49.so")

for off in [0x2cb156, 0x2cb1b6, 0x2cb206]:
    end = d.find(b"\x00", off)
    print(d[off:end].decode())
