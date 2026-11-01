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

import zipfile, struct, os, subprocess, shutil

src_apk = r"c:\Users\styuk\Downloads\AyuGram Desktop\exteraGram-full-universal-20261004.apk"
unaligned_apk = r"C:\project\ayugram\Tools\ayugram_unaligned.apk"
aligned_apk = r"C:\project\ayugram\AyuGram-12.10.6-universal.apk"
keystore_path = r"C:\project\ayugram\TMessagesProj\config\release.keystore"
zipalign_bin = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\zipalign.exe"
apksigner_bin = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\apksigner.bat"
new_icons_dir = r"C:\project\ayugram\Tools\new_icons"

# 1. Read and patch resources.arsc
with zipfile.ZipFile(src_apk, "r") as z:
    arsc = bytearray(z.read("resources.arsc"))

# Replace color pattern #ffe83030 with #ff2c2343
old_color_pattern = b"\x08\x00\x00\x1d\x30\x30\xe8\xff"
new_color_pattern = b"\x08\x00\x00\x1d\x43\x23\x2c\xff"
assert arsc.count(old_color_pattern) == 1
idx = arsc.index(old_color_pattern)
arsc[idx : idx + len(old_color_pattern)] = new_color_pattern

# Rebuild StringPool
sp_offset = 12
sp_type, sp_header_size, old_sp_size = struct.unpack("<HHI", arsc[sp_offset : sp_offset + 8])
string_count, style_count, flags, strings_start, styles_start = struct.unpack("<IIIII", arsc[sp_offset + 8 : sp_offset + 28])
old_offsets = struct.unpack(f"<{string_count}I", arsc[sp_offset + 28 : sp_offset + 28 + string_count * 4])

style_offset_start = sp_offset + 28 + string_count * 4
style_offsets = arsc[style_offset_start : style_offset_start + style_count * 4]

data_start = sp_offset + strings_start
old_styles_data = arsc[sp_offset + styles_start : sp_offset + old_sp_size]

raw_entries = []
for i in range(string_count):
    p = data_start + old_offsets[i]
    start = p
    b1 = arsc[p]; p += 1
    if b1 & 0x80: p += 1
    b2 = arsc[p]; p += 1
    if b2 & 0x80:
        b2 = ((b2 & 0x7f) << 8) | arsc[p]; p += 1
    end = p + b2 + 1
    raw_entries.append(bytes(arsc[start:end]))

def make_entry(text):
    b = text.encode("utf-8")
    char_len = len(text)
    byte_len = len(b)
    res = bytearray()
    if char_len > 0x7f:
        res.append(0x80 | ((char_len >> 8) & 0x7f))
        res.append(char_len & 0xff)
    else:
        res.append(char_len)
    if byte_len > 0x7f:
        res.append(0x80 | ((byte_len >> 8) & 0x7f))
        res.append(byte_len & 0xff)
    else:
        res.append(byte_len)
    res.extend(b)
    res.append(0)
    return bytes(res)

replacements = {
    9027: "AyuGram",
    9205: "AyuGram",
    9206: "AyuGram Preferences"
}

for i, rep in replacements.items():
    raw_entries[i] = make_entry(rep)

new_offsets = []
new_data = bytearray()
for entry in raw_entries:
    new_offsets.append(len(new_data))
    new_data.extend(entry)

while len(new_data) % 4 != 0:
    new_data.append(0)

new_strings_start = 28 + string_count * 4 + style_count * 4
while new_strings_start % 4 != 0:
    new_strings_start += 1

new_styles_start = new_strings_start + len(new_data)
new_sp_size = new_styles_start + len(old_styles_data)
while new_sp_size % 4 != 0:
    new_sp_size += 1

new_sp = bytearray()
new_sp.extend(struct.pack("<HHI", sp_type, sp_header_size, new_sp_size))
new_sp.extend(struct.pack("<IIIII", string_count, style_count, flags, new_strings_start, new_styles_start))
for off in new_offsets:
    new_sp.extend(struct.pack("<I", off))
new_sp.extend(style_offsets)
while len(new_sp) < new_strings_start:
    new_sp.append(0)
new_sp.extend(new_data)
new_sp.extend(old_styles_data)
while len(new_sp) < new_sp_size:
    new_sp.append(0)

rest = arsc[sp_offset + old_sp_size :]
new_total_size = 12 + len(new_sp) + len(rest)
new_header = struct.pack("<HHI", 0x0002, 12, new_total_size) + arsc[8:12]
patched_arsc = new_header + new_sp + rest

# Map of new icon files
icon_replacements = {
    "res/NtV.webp": os.path.join(new_icons_dir, "NtV.webp"),
    "res/133.webp": os.path.join(new_icons_dir, "133.webp"),
    "res/9Qo.webp": os.path.join(new_icons_dir, "9Qo.webp"),
    "res/iE4.webp": os.path.join(new_icons_dir, "iE4.webp"),
    "res/5cm.webp": os.path.join(new_icons_dir, "5cm.webp"),
    "res/SnS.webp": os.path.join(new_icons_dir, "SnS.webp"),
    "res/sKa.webp": os.path.join(new_icons_dir, "sKa.webp"),
    "res/j_H.webp": os.path.join(new_icons_dir, "j_H.webp"),
    "res/-66.webp": os.path.join(new_icons_dir, "-66.webp"),
}

# 2. Write unaligned APK
print("Writing unaligned APK...")
if os.path.exists(unaligned_apk):
    os.remove(unaligned_apk)

with zipfile.ZipFile(src_apk, "r") as zin, zipfile.ZipFile(unaligned_apk, "w") as zout:
    for item in zin.infolist():
        # Skip old signatures
        if item.filename.startswith("META-INF/") and (
            item.filename.endswith(".SF")
            or item.filename.endswith(".RSA")
            or item.filename.endswith(".MF")
        ):
            continue

        new_info = zipfile.ZipInfo(item.filename)
        new_info.date_time = item.date_time
        new_info.compress_type = item.compress_type
        new_info.external_attr = item.external_attr

        if item.filename == "resources.arsc":
            zout.writestr(new_info, patched_arsc)
        elif item.filename in icon_replacements:
            with open(icon_replacements[item.filename], "rb") as f:
                zout.writestr(new_info, f.read())
        else:
            zout.writestr(new_info, zin.read(item.filename))

print("Unaligned APK written successfully.")

# 3. Zipalign
print("Running zipalign...")
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)

res = subprocess.run([zipalign_bin, "-p", "-f", "4", unaligned_apk, aligned_apk], capture_output=True, text=True)
if res.returncode != 0:
    print("Zipalign error:", res.stderr)
    exit(1)
print("Zipalign completed successfully.")

# 4. Sign with apksigner (v1, v2, v3)
print("Signing APK with apksigner...")
cmd = [
    apksigner_bin, "sign",
    "--ks", keystore_path,
    "--ks-pass", "pass:android",
    "--key-pass", "pass:android",
    "--v1-signing-enabled", "true",
    "--v2-signing-enabled", "true",
    "--v3-signing-enabled", "true",
    aligned_apk
]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Signing error:", res.stderr)
    exit(1)
print("APK signed successfully.")

# 5. Verify signature
print("Verifying signature...")
res = subprocess.run([apksigner_bin, "verify", "--verbose", aligned_apk], capture_output=True, text=True)
print(res.stdout)

# 6. Verify badging
print("Verifying badging...")
res = subprocess.run([r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\aapt.exe", "dump", "badging", aligned_apk], capture_output=True, text=True)
for line in res.stdout.splitlines():
    if "package:" in line or "application-label:" in line or "launchable-activity:" in line:
        print(line)

print("\nSUCCESS! Built and signed:", aligned_apk)
