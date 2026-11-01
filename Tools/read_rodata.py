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

import zipfile

with zipfile.ZipFile(r"c:\Users\styuk\Downloads\AyuGram Desktop\vanilla-AyuGram-full-20261005.apk", "r") as z:
    d = z.read("lib/arm64-v8a/libtmessages.49.so")

# Search all strings within 2000 bytes of 0x13cd8f (rodata)
start = max(0, 0x13cd8f - 500)
end = min(len(d), 0x13cd8f + 500)
chunk = d[start:end]
for s in chunk.split(b"\x00"):
    if len(s) > 2:
        try:
            print(s.decode())
        except:
            pass
