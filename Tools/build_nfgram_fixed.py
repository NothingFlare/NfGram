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
import zlib
import hashlib
import struct
import subprocess
import os
import shutil
from PIL import Image, ImageDraw
import io

VANILLA_APK = r"c:\Users\styuk\Downloads\AyuGram Desktop\vanilla-AyuGram-full-20261005.apk"
EXTERA_APK = r"c:\Users\styuk\Downloads\AyuGram Desktop\exteraGram-full-universal-20261004.apk"
OUTPUT_APK_NFGRAM = r"c:\Users\styuk\Downloads\AyuGram Desktop\NfGram-12.10.6-universal.apk"
OUTPUT_APK_AYU = r"c:\Users\styuk\Downloads\AyuGram Desktop\AyuGram-12.10.6-universal.apk"
OUTPUT_APK_PROJECT = r"C:\project\ayugram\NfGram-12.10.6-universal.apk"

KEYSTORE = r"C:\project\ayugram\Tools\nfgram_release.keystore"
ZIPALIGN = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\zipalign.exe"
APKSIGNER = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\apksigner.bat"
AAPT = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\aapt.exe"
DEXDUMP = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\dexdump.exe"

OLD_PACKAGE = "com.radolyn.ayugram"
NEW_PACKAGE = "com.red.nfgram.chat"
assert len(NEW_PACKAGE) == len(OLD_PACKAGE) == 19

print("=== STEP 1: Patch DEX files (Parallel upload + package rename) ===")
with zipfile.ZipFile(VANILLA_APK, "r") as z:
    dex1 = bytearray(z.read("classes.dex"))
    dex5 = bytearray(z.read("classes5.dex"))
    manifest = bytearray(z.read("AndroidManifest.xml"))
    arsc = bytearray(z.read("resources.arsc"))

# 1. Patch classes.dex: parallel upload
seq1 = b"\x52\xa3\x87\x31\x35\x23\x09\x00\xb0\x23\x59\xa3\x87\x31"
seq2 = b"\x52\xa3\x86\x31\x35\x23\x09\x00\xb0\x23\x59\xa3\x86\x31"
assert dex1.count(seq1) == 1 and dex1.count(seq2) == 1
idx1 = dex1.find(seq1)
idx2 = dex1.find(seq2)
dex1[idx1+4 : idx1+8] = b"\x00\x00\x00\x00"
dex1[idx2+4 : idx2+8] = b"\x00\x00\x00\x00"
print("Applied parallel upload patches in classes.dex")

# 2. Patch classes.dex: replace #10097 and #56764 preserving Dalvik string ordering
# Replace string #10097: /data/data/com.radolyn.ayugram/files -> /data/data/com.red.nfgram.chat/files
old_dir = b"/data/data/" + OLD_PACKAGE.encode("utf-8") + b"/files"
new_dir = b"/data/data/" + NEW_PACKAGE.encode("utf-8") + b"/files"
assert dex1.count(old_dir) == 1
idx_dir = dex1.find(old_dir)
dex1[idx_dir : idx_dir + len(old_dir)] = new_dir
print(f"Patched data directory at {idx_dir}")

# Replace string #56764: com.radolyn.ayugram -> com.red.nfgram.chat
string_ids_off1 = struct.unpack("<I", dex1[60:64])[0]
str56764_off = struct.unpack("<I", dex1[string_ids_off1 + 56764*4 : string_ids_off1 + 56765*4])[0]
expected_old_entry = b"\x13" + OLD_PACKAGE.encode("utf-8") + b"\x00"
new_entry = b"\x13" + NEW_PACKAGE.encode("utf-8") + b"\x00"
assert dex1[str56764_off : str56764_off + 21] == expected_old_entry, f"Unexpected data at {str56764_off}"
dex1[str56764_off : str56764_off + 21] = new_entry
print(f"Patched classes.dex string #56764 at {str56764_off}")

# Recompute classes.dex hashes
dex1[12:32] = hashlib.sha1(dex1[32:]).digest()
dex1[8:12] = struct.pack("<I", zlib.adler32(dex1[12:]) & 0xFFFFFFFF)

# 3. Patch classes5.dex: replace string #41733
string_ids_off5 = struct.unpack("<I", dex5[60:64])[0]
str41733_off = struct.unpack("<I", dex5[string_ids_off5 + 41733*4 : string_ids_off5 + 41734*4])[0]
assert dex5[str41733_off : str41733_off + 21] == expected_old_entry, f"Unexpected data at {str41733_off}"
dex5[str41733_off : str41733_off + 21] = new_entry
print(f"Patched classes5.dex string #41733 at {str41733_off}")

# Recompute classes5.dex hashes
dex5[12:32] = hashlib.sha1(dex5[32:]).digest()
dex5[8:12] = struct.pack("<I", zlib.adler32(dex5[12:]) & 0xFFFFFFFF)

# Verify DEX checksums and Dalvik structure using dexdump
with open("Tools/temp_verify1.dex", "wb") as f: f.write(dex1)
with open("Tools/temp_verify5.dex", "wb") as f: f.write(dex5)

res1 = subprocess.run([DEXDUMP, "-c", "Tools/temp_verify1.dex"], capture_output=True, text=True)
if res1.returncode != 0:
    print("DEX verification failed for classes.dex:", res1.stderr or res1.stdout)
    exit(1)
print("classes.dex passed dexdump verification successfully!")

res5 = subprocess.run([DEXDUMP, "-c", "Tools/temp_verify5.dex"], capture_output=True, text=True)
if res5.returncode != 0:
    print("DEX verification failed for classes5.dex:", res5.stderr or res5.stdout)
    exit(1)
print("classes5.dex passed dexdump verification successfully!")

os.remove("Tools/temp_verify1.dex")
os.remove("Tools/temp_verify5.dex")

print("=== STEP 2: Patch AndroidManifest.xml ===")
old_pkg_u16 = OLD_PACKAGE.encode("utf-16le")
new_pkg_u16 = NEW_PACKAGE.encode("utf-16le")
manifest_count = manifest.count(old_pkg_u16)
assert manifest_count == 12, f"Expected 12 occurrences in manifest, found {manifest_count}"
manifest = manifest.replace(old_pkg_u16, new_pkg_u16)
print(f"AndroidManifest.xml: successfully replaced all {manifest_count} package occurrences.")

print("=== STEP 3: Patch resources.arsc ===")
arsc_pkg_count = arsc.count(old_pkg_u16)
assert arsc_pkg_count == 1, f"Expected 1 package occurrence in arsc, found {arsc_pkg_count}"
arsc = arsc.replace(old_pkg_u16, new_pkg_u16)
print("resources.arsc: package name replaced.")

# Rebuild StringPool in resources.arsc for app labels
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
    8559: "NfGram",
    8560: "NfGram Alt",
    9497: "NfGram",
    9593: "Update NfGram",
    9635: "Welcome to the NfGram Desktop. Make Telegram your own."
}

for idx, rep in replacements.items():
    raw_entries[idx] = make_entry(rep)

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
final_arsc = new_header + new_sp + rest
print(f"Patched resources.arsc size: {len(final_arsc)} bytes")

print("=== STEP 4: Prepare exteraGram Icons ===")
icon_replacements = {}
with zipfile.ZipFile(EXTERA_APK, "r") as z_ext:
    # Foreground webps (white paper plane)
    fg_names = ["res/NtV.webp", "res/133.webp", "res/9Qo.webp", "res/iE4.webp", "res/5cm.webp"]
    for fn in fg_names:
        icon_replacements[fn] = z_ext.read(fn)

# Background webps (solid red #E83030)
RED_COLOR = (232, 48, 48, 255)
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

# Legacy composite icons
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
icon_replacements["res/-66.webp"] = make_composite(144, round_shape=True)
print(f"Prepared {len(icon_replacements)} icon replacements.")

print("=== STEP 5: Repack APK ===")
unaligned_apk = "Tools/nfgram_fixed_unaligned.apk"
if os.path.exists(unaligned_apk):
    os.remove(unaligned_apk)

with zipfile.ZipFile(VANILLA_APK, "r") as zin, zipfile.ZipFile(unaligned_apk, "w") as zout:
    for item in zin.infolist():
        # Discard old signatures
        if item.filename.startswith("META-INF/") and (item.filename.endswith(".SF") or item.filename.endswith(".RSA") or item.filename.endswith(".MF")):
            continue
        if item.filename == "classes.dex":
            zout.writestr(item, dex1)
        elif item.filename == "classes5.dex":
            zout.writestr(item, dex5)
        elif item.filename == "AndroidManifest.xml":
            zout.writestr(item, manifest)
        elif item.filename == "resources.arsc":
            zout.writestr(item, final_arsc)
        elif item.filename in icon_replacements:
            zout.writestr(item, icon_replacements[item.filename])
        else:
            data = zin.read(item.filename)
            zout.writestr(item, data, compress_type=item.compress_type)

print(f"Created unaligned APK: {unaligned_apk} ({os.path.getsize(unaligned_apk)} bytes)")

print("=== STEP 6: Zipalign APK ===")
aligned_apk = "Tools/nfgram_fixed_aligned.apk"
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)

res = subprocess.run([ZIPALIGN, "-p", "-f", "4", unaligned_apk, aligned_apk], capture_output=True, text=True)
if res.returncode != 0:
    print("Zipalign error:", res.stderr)
    exit(1)
print(f"Zipalign succeeded: {aligned_apk} ({os.path.getsize(aligned_apk)} bytes)")

print("=== STEP 7: Sign APK with NfGram Keystore ===")
cmd_sign = [
    APKSIGNER, "sign",
    "--ks", KEYSTORE,
    "--ks-pass", "pass:nfgram",
    "--key-pass", "pass:nfgram",
    "--ks-key-alias", "nfgram",
    "--v1-signing-enabled", "true",
    "--v2-signing-enabled", "true",
    "--v3-signing-enabled", "true",
    aligned_apk
]
res = subprocess.run(cmd_sign, capture_output=True, text=True)
if res.returncode != 0:
    print("Apksigner error:", res.stderr)
    exit(1)
print("Apksigner signing succeeded!")

print("=== STEP 8: Verify Signature and Badging ===")
res_sig = subprocess.run([APKSIGNER, "verify", "--verbose", "--print-certs", aligned_apk], capture_output=True, text=True)
print("Signature verification:")
for l in res_sig.stdout.splitlines():
    if "Verified" in l or "Signer #1 certificate DN" in l:
        print("  ", l)

res_badge = subprocess.run([AAPT, "dump", "badging", aligned_apk], capture_output=True, text=True)
print("Badging verification:")
for l in res_badge.stdout.splitlines():
    if "package:" in l or "application-label:" in l or "application-icon" in l:
        print("  ", l)

print("=== STEP 9: Deploy to destination paths ===")
shutil.copy2(aligned_apk, OUTPUT_APK_NFGRAM)
shutil.copy2(aligned_apk, OUTPUT_APK_AYU)
shutil.copy2(aligned_apk, OUTPUT_APK_PROJECT)
print(f"Deployed: {OUTPUT_APK_NFGRAM}")
print(f"Deployed: {OUTPUT_APK_AYU}")
print(f"Deployed: {OUTPUT_APK_PROJECT}")
print("BUILD COMPLETED 100% SUCCESSFULLY!")
