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

import os

script_path = r"C:\project\ayugram\Tools\build_nfgram_faceunlock.py"
with open(script_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Read classes4.dex
target1 = '    dex1 = bytearray(z.read("classes.dex"))\n    dex5 = bytearray(z.read("classes5.dex"))'
replace1 = '    dex1 = bytearray(z.read("classes.dex"))\n    dex4 = bytearray(z.read("classes4.dex"))\n    dex5 = bytearray(z.read("classes5.dex"))'
assert target1 in content, "target1 not found"
content = content.replace(target1, replace1, 1)

# 2. Patch classes4.dex
target2 = 'dex1[8:12] = struct.pack("<I", zlib.adler32(dex1[12:]) & 0xFFFFFFFF)'
replace2 = '''dex1[8:12] = struct.pack("<I", zlib.adler32(dex1[12:]) & 0xFFFFFFFF)

# -------------------------------------------------------------
# 1.1 Patch classes4.dex: Merge AyuGram into MainPreferencesActivity
# -------------------------------------------------------------
assert dex4[0x38a576 : 0x38a576 + 9] == bytes.fromhex("60 01 f7 8b 71 10 80 f5 01")
dex4[0x38a576 : 0x38a576 + 9] = bytes.fromhex("1a 03 54 19 00 00 00 00 00")
dex4[0x38a580 : 0x38a582] = bytes.fromhex("00 00")
dex4[0x38a584] = 0x09
dex4[0x38a588 : 0x38a58a] = bytes.fromhex("00 00")
dex4[0x38a58c : 0x38a58e] = bytes.fromhex("54 19")

dex4[0x38a6a6] = 0x1c
dex4[0x38a6a8 : 0x38a6af] = bytes.fromhex("01 35 6e 10 01 ee 01")
dex4[0x38a6b0 : 0x38a6b3] = bytes.fromhex("0c 01 1f")
dex4[0x38a6b4 : 0x38a6b7] = bytes.fromhex("58 39 6e")
dex4[0x38a6b8 : 0x38a6ba] = bytes.fromhex("09 f8")
dex4[0x38a764] = 0x11

dex4[12:32] = hashlib.sha1(dex4[32:]).digest()
dex4[8:12] = struct.pack("<I", zlib.adler32(dex4[12:]) & 0xFFFFFFFF)
print("Applied MainPreferencesActivity unified AyuGram settings patch in classes4.dex")'''
assert target2 in content, "target2 not found"
content = content.replace(target2, replace2, 1)

# 3. Patch classes6.dex for unified settings buttons
target3 = 'dex6[12:32] = hashlib.sha1(dex6[32:]).digest()'
replace3 = '''# 3.5 Unify Settings Buttons in ProfileActivity and SettingsActivity
# 1) ProfileActivity.updateRows: unify to 1 row
assert dex6[0x5e607c] == 8
dex6[0x5e607c] = 7

orig_rows = bytes.fromhex("d8 07 04 02 59 06 3c 9a d8 06 04 03 59 07 df 99 d8 07 04 04 59 06 10 9a d8 06 04 05 59 07 dd 9a d8 07 04 06 59 06 a8 9a d8 06 04 07 59 07 26 9a")
new_rows  = bytes.fromhex("12 f7 59 06 3c 9a 59 07 df 99 d8 06 04 02 59 06 10 9a d8 07 04 03 59 07 dd 9a d8 06 04 04 59 06 a8 9a d8 07 04 05 59 07 26 9a d8 06 04 06 00 00")
assert dex6[0x5e625e : 0x5e625e + len(orig_rows)] == orig_rows
dex6[0x5e625e : 0x5e625e + len(orig_rows)] = new_rows
print("Applied ProfileActivity unified settings row patch in classes6.dex")

# 2) SettingsActivity.fillItems: green color and remove second row
assert dex6[0x62e4f0 : 0x62e4f6] == bytes.fromhex("14 06 30 30 e8 ff")
dex6[0x62e4f0 : 0x62e4f6] = bytes.fromhex("14 06 71 cc 2e ff") # #ff2ecc71 Green

orig_ayu_row = bytes.fromhex("60 02 8a 04 60 03 b7 08 71 10 70 0f 03 00 0c 03 12 e5 14 06 ff 70 95 ff 71 53 d6 e6 65 26 0c 02 6e 20 c0 0a 21 00")
assert dex6[0x62e504 : 0x62e504 + len(orig_ayu_row)] == orig_ayu_row
dex6[0x62e504 : 0x62e504 + len(orig_ayu_row)] = b"\\x00" * len(orig_ayu_row) # 19 NOPs
print("Applied SettingsActivity single green button patch in classes6.dex")

dex6[12:32] = hashlib.sha1(dex6[32:]).digest()'''
assert target3 in content, "target3 not found"
content = content.replace(target3, replace3, 1)

# 4. Verify classes4.dex too
target4 = 'for name, dex_data in [("classes.dex", dex1), ("classes5.dex", dex5), ("classes6.dex", dex6), ("classes7.dex", dex7)]:'
replace4 = 'for name, dex_data in [("classes.dex", dex1), ("classes4.dex", dex4), ("classes5.dex", dex5), ("classes6.dex", dex6), ("classes7.dex", dex7)]:'
assert target4 in content, "target4 not found"
content = content.replace(target4, replace4, 1)

# 5. Patch resources.arsc color #ffe83030 -> #ff2ecc71
target5 = 'arsc = arsc.replace(old_pkg_u16, new_pkg_u16)'
replace5 = '''arsc = arsc.replace(old_pkg_u16, new_pkg_u16)

# Patch Accent Color: #ffe83030 (red) -> #ff2ecc71 (green)
old_color_pattern = b"\\x08\\x00\\x00\\x1d\\x30\\x30\\xe8\\xff"
new_color_pattern = b"\\x08\\x00\\x00\\x1d\\x71\\xcc\\x2e\\xff"
assert arsc.count(old_color_pattern) == 1
arsc = arsc.replace(old_color_pattern, new_color_pattern)
print("Replaced red color #ffe83030 with green #ff2ecc71 in resources.arsc")'''
assert target5 in content, "target5 not found"
content = content.replace(target5, replace5, 1)

# 6. Green icons
target6 = '''RED_COLOR = (232, 48, 48, 255)
bg_sizes = {
    "res/AtC.webp": (108, 108),
    "res/4kp.webp": (162, 162),
    "res/ByQ.webp": (216, 216),
    "res/BZn.webp": (324, 324),
    "res/gSt.webp": (432, 432)
}
for fn, size in bg_sizes.items():
    img = Image.new("RGBA", size, RED_COLOR)
    buf = io.BytesIO()
    img.save(buf, format="WEBP")
    icon_replacements[fn] = buf.getvalue()

fg_432 = Image.open(io.BytesIO(icon_replacements["res/5cm.webp"])).convert("RGBA")

def make_composite(size, round_shape=False):
    base = Image.new("RGBA", (432, 432), RED_COLOR)
    comp = Image.alpha_composite(base, fg_432)
    if round_shape:
        mask = Image.new("L", (432, 432), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 432, 432), fill=255)
        rounded = Image.new("RGBA", (432, 432), (0, 0, 0, 0))
        rounded.paste(comp, (0, 0), mask=mask)
        comp = rounded
    resized = comp.resize((size, size), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    resized.save(buf, format="WEBP")
    return buf.getvalue()

icon_replacements["res/sKa.webp"] = make_composite(192, round_shape=False)
icon_replacements["res/SnS.webp"] = make_composite(144, round_shape=False)
icon_replacements["res/j_H.webp"] = make_composite(192, round_shape=True)
icon_replacements["res/-66.webp"] = make_composite(144, round_shape=True)'''

replace6 = '''GREEN_COLOR = (46, 204, 113, 255) # #2ecc71 emerald green
bg_sizes = {
    "res/AtC.webp": (108, 108),
    "res/4kp.webp": (162, 162),
    "res/ByQ.webp": (216, 216),
    "res/BZn.webp": (324, 324),
    "res/gSt.webp": (432, 432)
}
for fn, size in bg_sizes.items():
    img = Image.new("RGBA", size, GREEN_COLOR)
    buf = io.BytesIO()
    img.save(buf, format="WEBP")
    icon_replacements[fn] = buf.getvalue()

fg_432 = Image.open(io.BytesIO(icon_replacements["res/5cm.webp"])).convert("RGBA")

def make_composite(size, round_shape=False):
    base = Image.new("RGBA", (432, 432), GREEN_COLOR)
    comp = Image.alpha_composite(base, fg_432)
    if round_shape:
        mask = Image.new("L", (432, 432), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 432, 432), fill=255)
        rounded = Image.new("RGBA", (432, 432), (0, 0, 0, 0))
        rounded.paste(comp, (0, 0), mask=mask)
        comp = rounded
    resized = comp.resize((size, size), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    resized.save(buf, format="WEBP")
    return buf.getvalue()

icon_replacements["res/sKa.webp"] = make_composite(192, round_shape=False)
icon_replacements["res/SnS.webp"] = make_composite(144, round_shape=False)
icon_replacements["res/j_H.webp"] = make_composite(192, round_shape=True)
icon_replacements["res/-66.webp"] = make_composite(144, round_shape=True)

# Settings menu row icons (all densities) replaced with green icons
settings_icons = {
    "res/3_C.png": r"C:\project\ayugram\Tools\res_3_C.png",
    "res/3Ul.png": r"C:\project\ayugram\Tools\res_3Ul.png",
    "res/gtN.png": r"C:\project\ayugram\Tools\res_gtN.png",
    "res/9501.png": r"C:\project\ayugram\Tools\res_9501.png",
}
for res_name, file_path in settings_icons.items():
    with open(file_path, "rb") as f:
        icon_replacements[res_name] = f.read()'''

assert target6 in content, "target6 not found"
content = content.replace(target6, replace6, 1)

# 7. Repack classes4.dex
target7 = '        if item.filename == "classes.dex":\n            zout.writestr(item, dex1)'
replace7 = '        if item.filename == "classes.dex":\n            zout.writestr(item, dex1)\n        elif item.filename == "classes4.dex":\n            zout.writestr(item, dex4)'
assert target7 in content, "target7 not found"
content = content.replace(target7, replace7, 1)

# 8. Deploy destinations
target8 = '''shutil.copy2(aligned_apk, OUTPUT_APK_NFGRAM)
shutil.copy2(aligned_apk, OUTPUT_APK_DESKTOP)
shutil.copy2(aligned_apk, OUTPUT_APK_PROJECT)'''
replace8 = '''destinations = [
    OUTPUT_APK_PROJECT,
    OUTPUT_APK_DESKTOP,
    OUTPUT_APK_NFGRAM,
    r"c:\\Users\\styuk\\Downloads\\AyuGram Desktop\\AyuGram-12.10.6-universal.apk",
    r"c:\\Users\\styuk\\Downloads\\NfGram-12.10.6-universal.apk",
]
for dst in destinations:
    try:
        dst_dir = os.path.dirname(dst)
        if os.path.exists(dst_dir):
            shutil.copy2(aligned_apk, dst)
            print(f"Deployed: {dst}")
    except Exception as e:
        print(f"Warning deploying to {dst}: {e}")'''
assert target8 in content, "target8 not found"
content = content.replace(target8, replace8, 1)

with open(script_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Successfully updated Tools/build_nfgram_faceunlock.py!")
