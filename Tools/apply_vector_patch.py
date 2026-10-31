"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

with open(r'c:\project\ayugram\Tools\build_nfgram_faceunlock.py', 'r', encoding='utf-8') as f:
    c = f.read()

target = '        icon_replacements[fn] = z_ext.read(fn)\n'
patch = '''        icon_replacements[fn] = z_ext.read(fn)

# Patch squircle vector icons size from 72dp to 24dp
val_72dp = struct.pack("<I", 0x4801)
val_24dp = struct.pack("<I", 0x1801)
with zipfile.ZipFile(VANILLA_APK, "r") as zin:
    for vname in ["res/qS4.xml", "res/8ZN.xml"]:
        icon_replacements[vname] = zin.read(vname).replace(val_72dp, val_24dp)
print("Patched squircle vector icons res/qS4.xml and res/8ZN.xml to 24dp")
'''

assert target in c
c = c.replace(target, patch, 1)

with open(r'c:\project\ayugram\Tools\build_nfgram_faceunlock.py', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated build_nfgram_faceunlock.py successfully!')
