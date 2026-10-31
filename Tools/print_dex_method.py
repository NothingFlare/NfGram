"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

import subprocess

res = subprocess.run([
    r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\dexdump.exe",
    "-d", "temp_classes.dex"
], capture_output=True, text=True, errors="ignore")

lines = res.stdout.splitlines()
for i, line in enumerate(lines):
    if "4eb888" in line:
        start = max(0, i - 40)
        end = min(len(lines), i + 60)
        for j in range(start, end):
            print(lines[j])
        break
