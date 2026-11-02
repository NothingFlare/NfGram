import os
import sys
import io
import struct
import zlib
import hashlib
import zipfile
import subprocess
from PIL import Image, ImageDraw

NEW_CORE_APK = r"c:\Users\styuk\Desktop\exteraGram-full-universal-20261102.apk"
KEYSTORE = r"C:\project\ayugram\Tools\nfgram_release.keystore"
KEYSTORE_PASS = "nfgram"
KEY_ALIAS = "nfgram"

AAPT = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\36.0.0\aapt.exe"
ZIPALIGN = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\36.0.0\zipalign.exe"
APKSIGNER = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat"

OLD_PACKAGE = "com.exteragram.messenger"
NEW_PACKAGE = "com.red.nfgram.chat"

print("=== STEP 1: Reading base APK ===")
with zipfile.ZipFile(NEW_CORE_APK, "r") as z:
    manifest_raw = bytearray(z.read("AndroidManifest.xml"))
    arsc_raw = bytearray(z.read("resources.arsc"))
    dex1 = bytearray(z.read("classes.dex"))
    dex7 = bytearray(z.read("classes7.dex"))

# -----------------------------------------------------------------
# 1. AndroidManifest.xml: Rebuild StringPool
# -----------------------------------------------------------------
print("=== STEP 2: Patching AndroidManifest.xml StringPool ===")
sp_off = 8
sp_type, sp_hdr_size, sp_size = struct.unpack("<HHI", manifest_raw[sp_off : sp_off + 8])
str_count, style_count, flags, str_start, style_start = struct.unpack("<IIIII", manifest_raw[sp_off + 8 : sp_off + 28])
is_utf8 = bool(flags & (1 << 8))

str_offsets = list(struct.unpack(f"<{str_count}I", manifest_raw[sp_off + 28 : sp_off + 28 + str_count * 4]))
data_start = sp_off + str_start

strings = []
for i in range(str_count):
    p = data_start + str_offsets[i]
    if is_utf8:
        while manifest_raw[p] & 0x80: p += 1
        p += 1
        b_len = 0
        shift = 0
        while True:
            b = manifest_raw[p]
            p += 1
            b_len |= (b & 0x7F) << shift
            if not (b & 0x80): break
            shift += 7
        s = manifest_raw[p : p + b_len].decode("utf-8", errors="replace")
    else:
        u16_len = struct.unpack("<H", manifest_raw[p : p + 2])[0]
        p += 2
        s = manifest_raw[p : p + u16_len * 2].decode("utf-16le", errors="replace")
    strings.append(s)

# Replace OLD_PACKAGE -> NEW_PACKAGE in manifest strings
repl_count = 0
for i in range(len(strings)):
    if OLD_PACKAGE in strings[i]:
        strings[i] = strings[i].replace(OLD_PACKAGE, NEW_PACKAGE)
        repl_count += 1
print(f"Replaced {repl_count} occurrences of {OLD_PACKAGE} in AndroidManifest.xml")

# Re-encode manifest StringPool (UTF-8)
new_str_data = bytearray()
new_offsets = []
for s in strings:
    new_offsets.append(len(new_str_data))
    encoded = s.encode("utf-8")
    u16_len = len(s)
    # write char length uleb128
    if u16_len <= 0x7F:
        new_str_data.append(u16_len)
    else:
        new_str_data.append((u16_len & 0x7F) | 0x80)
        new_str_data.append((u16_len >> 7) & 0x7F)
    # write byte length uleb128
    b_len = len(encoded)
    if b_len <= 0x7F:
        new_str_data.append(b_len)
    else:
        new_str_data.append((b_len & 0x7F) | 0x80)
        new_str_data.append((b_len >> 7) & 0x7F)
    new_str_data.extend(encoded)
    new_str_data.append(0)

# Pad to 4 bytes
while len(new_str_data) % 4 != 0:
    new_str_data.append(0)

new_str_start = 28 + str_count * 4
new_sp_size = new_str_start + len(new_str_data)
new_sp_hdr = struct.pack("<HHI", 0x0001, 28, new_sp_size) + struct.pack("<IIIII", str_count, 0, 0x100, new_str_start, 0)
new_offsets_bytes = struct.pack(f"<{str_count}I", *new_offsets)

new_sp = new_sp_hdr + new_offsets_bytes + new_str_data
manifest_rest = manifest_raw[sp_off + sp_size :]
new_manifest_total_size = 8 + len(new_sp) + len(manifest_rest)
manifest_header = struct.pack("<HHI", 0x0003, 8, new_manifest_total_size)
final_manifest = manifest_header + new_sp + manifest_rest

# -----------------------------------------------------------------
# 2. resources.arsc: Package name & App Name & Adaptive Background
# -----------------------------------------------------------------
print("=== STEP 3: Patching resources.arsc ===")
old_pkg_u16 = OLD_PACKAGE.encode("utf-16le")
new_pkg_u16 = NEW_PACKAGE.encode("utf-16le").ljust(len(old_pkg_u16), b"\x00")
assert arsc_raw.count(old_pkg_u16) == 1
arsc_patched = arsc_raw.replace(old_pkg_u16, new_pkg_u16)

# Global StringPool in arsc
arsc_sp_off = 12
_, _, old_arsc_sp_size = struct.unpack("<HHI", arsc_patched[arsc_sp_off : arsc_sp_off + 8])
arsc_str_count, _, arsc_flags, arsc_str_start, _ = struct.unpack("<IIIII", arsc_patched[arsc_sp_off + 8 : arsc_sp_off + 28])
arsc_str_offsets = list(struct.unpack(f"<{arsc_str_count}I", arsc_patched[arsc_sp_off + 28 : arsc_sp_off + 28 + arsc_str_count * 4]))
arsc_data_start = arsc_sp_off + arsc_str_start

arsc_strings = []
for i in range(arsc_str_count):
    p = arsc_data_start + arsc_str_offsets[i]
    while arsc_patched[p] & 0x80: p += 1
    p += 1
    b_len = 0
    shift = 0
    while True:
        b = arsc_patched[p]
        p += 1
        b_len |= (b & 0x7F) << shift
        if not (b & 0x80): break
        shift += 7
    s = arsc_patched[p : p + b_len].decode("utf-8", errors="replace")
    arsc_strings.append(s)

# Replace exteraGram -> NfGram
arsc_repl = 0
for i in range(len(arsc_strings)):
    if arsc_strings[i] == "exteraGram":
        arsc_strings[i] = "NfGram"
        arsc_repl += 1
    elif arsc_strings[i] == OLD_PACKAGE:
        arsc_strings[i] = NEW_PACKAGE
        arsc_repl += 1
print(f"Replaced {arsc_repl} strings in resources.arsc (exteraGram -> NfGram)")

# Re-encode arsc StringPool
new_arsc_str_data = bytearray()
new_arsc_offsets = []
for s in arsc_strings:
    new_arsc_offsets.append(len(new_arsc_str_data))
    encoded = s.encode("utf-8")
    u16_len = len(s)
    if u16_len <= 0x7F:
        new_arsc_str_data.append(u16_len)
    else:
        new_arsc_str_data.append((u16_len & 0x7F) | 0x80)
        new_arsc_str_data.append((u16_len >> 7) & 0x7F)
    b_len = len(encoded)
    if b_len <= 0x7F:
        new_arsc_str_data.append(b_len)
    else:
        new_arsc_str_data.append((b_len & 0x7F) | 0x80)
        new_arsc_str_data.append((b_len >> 7) & 0x7F)
    new_arsc_str_data.extend(encoded)
    new_arsc_str_data.append(0)

while len(new_arsc_str_data) % 4 != 0:
    new_arsc_str_data.append(0)

new_arsc_str_start = 28 + arsc_str_count * 4
new_arsc_sp_size = new_arsc_str_start + len(new_arsc_str_data)
new_arsc_sp_hdr = struct.pack("<HHI", 0x0001, 28, new_arsc_sp_size) + struct.pack("<IIIII", arsc_str_count, 0, 0x100, new_arsc_str_start, 0)
new_arsc_offsets_bytes = struct.pack(f"<{arsc_str_count}I", *new_arsc_offsets)
new_arsc_sp = new_arsc_sp_hdr + new_arsc_offsets_bytes + new_arsc_str_data

arsc_rest = arsc_patched[arsc_sp_off + old_arsc_sp_size :]

# Replace adaptive icon background color 0xffe83030 -> 0xff2ecc71 (emerald green)
old_bg_color = bytes.fromhex("30 30 e8 ff")
new_bg_color = bytes.fromhex("71 cc 2e ff") # #ff2ecc71
arsc_rest = arsc_rest.replace(old_bg_color, new_bg_color)
print("Replaced ic_background color with #2ecc71 emerald green in resources.arsc")

new_arsc_total_size = 12 + len(new_arsc_sp) + len(arsc_rest)
arsc_header = struct.pack("<HHI", 0x0002, 12, new_arsc_total_size) + arsc_patched[8:12]
final_arsc = arsc_header + new_arsc_sp + arsc_rest

# -----------------------------------------------------------------
# 3. Patch classes.dex: All Features & Plugins Engine Fixes
# -----------------------------------------------------------------
print("=== STEP 4: Patching classes.dex ===")

# Patch 1: getAddCommaAfterMention:()Z -> return false
off_comma = 0x3b3eec
assert dex1[off_comma : off_comma + 4] == bytes.fromhex("62 00 9f 13")
dex1[off_comma : off_comma + 20] = bytes.fromhex("12 00 0f 00") + b"\x00" * 16
print("Patched getAddCommaAfterMention -> returns false (no comma after @user)")

# Patch 2: isPushConnectionEnabled:()Z -> return true
off_push = 0x32ee64
assert dex1[off_push : off_push + 6] == bytes.fromhex("71 00 e3 bc 00 00")
dex1[off_push : off_push + 22] = bytes.fromhex("12 10 0f 00") + b"\x00" * 18
print("Patched isPushConnectionEnabled -> returns true (RF VPN background push kept alive)")

# Patch 3: MediaController.isNearToSensor -> 2.0f threshold
off_sensor1 = 0x4dcfd0
assert dex1[off_sensor1 : off_sensor1 + 4] == bytes.fromhex("15 00 a0 40")
dex1[off_sensor1 : off_sensor1 + 4] = bytes.fromhex("15 00 00 40")
print("Patched MediaController.isNearToSensor -> 2.0f threshold (calibrated ear sensor)")

# Patch 4: SharedConfig.canBlurChat -> return false
off_blur = 0x3225a0
assert dex1[off_blur : off_blur + 4] == bytes.fromhex("12 10 0f 00")
dex1[off_blur : off_blur + 4] = bytes.fromhex("12 00 0f 00")
print("Patched SharedConfig.canBlurChat -> returns false (disables GPU compute blurs, stops overheating)")

# Patch 5: SharedConfig.loadConfig -> force useNewBlur and photoViewerBlur to false
off_unb = 0x3230b0
assert dex1[off_unb : off_unb + 4] == bytes.fromhex("6a 02 80 81")
dex1[off_unb : off_unb + 4] = bytes.fromhex("12 02 6a 02") # const/4 v2, 0; sput-boolean v2, useNewBlur:Z (at 3230b4: 80 81)
off_pvb = 0x323126
assert dex1[off_pvb : off_pvb + 4] == bytes.fromhex("6a 02 4b 81")
dex1[off_pvb : off_pvb + 4] = bytes.fromhex("12 02 6a 02")
print("Patched SharedConfig.loadConfig -> useNewBlur & photoViewerBlur disabled")

# Patch 6: Neutralize NativeCrashHandler in Java
off_nch_call = 0x296820
assert dex1[off_nch_call : off_nch_call + 6] == bytes.fromhex("71 00 f4 46 00 00")
dex1[off_nch_call : off_nch_call + 14] = b"\x00" * 14
off_nch_chk = 0x228760
assert dex1[off_nch_chk : off_nch_chk + 4] == bytes.fromhex("22 00 37 16")
dex1[off_nch_chk : off_nch_chk + 2] = bytes.fromhex("0e 00") # return-void
print("Patched NativeCrashHandler -> suppressed init & checkAndHandleNativeCrash (eliminates SIGSEGV loop)")

# Patch 7: ExteraConfig.getPluginsEngine:()Z -> return true
off_pe = 0x21327c
assert dex1[off_pe : off_pe + 6] == bytes.fromhex("63 00 02 14 0f 00")
dex1[off_pe : off_pe + 6] = bytes.fromhex("12 10 0f 00 00 00")
print("Patched ExteraConfig.getPluginsEngine -> returns true (plugins enabled by default)")

# Patch 8: PythonPluginsEngine.initSdk:()Z -> ensure getPython() is invoked
off_init_py = 0x223d0a
assert dex1[off_init_py : off_init_py + 10] == bytes.fromhex("54 f2 95 18 39 02 03 00 0f 01")
# invoke-direct {v15}, getPython() [70 10 ac 43 0f 00] + iget-object v2, v15, python [54 f2 95 18]
dex1[off_init_py : off_init_py + 10] = bytes.fromhex("70 10 ac 43 0f 00 54 f2 95 18")
print("Patched PythonPluginsEngine.initSdk -> ensures getPython() initializes Chaquopy runtime")

# Patch 9: PythonPluginsEngine.initSdk:()Z -> force sdkInitialized = true
off_force_sdk = 0x224048
assert dex1[off_force_sdk : off_force_sdk + 2] == bytes.fromhex("01 13")
dex1[off_force_sdk : off_force_sdk + 2] = bytes.fromhex("12 13") # const/4 v3, 1
print("Patched PythonPluginsEngine.initSdk -> forces sdkInitialized = true")

# Patch 10: PythonPluginsEngine.initSdk:()Z -> do not skip requireBasePluginClass in safe mode
off_skip_sm = 0x2240d8
assert dex1[off_skip_sm : off_skip_sm + 4] == bytes.fromhex("39 00 0d 00")
dex1[off_skip_sm : off_skip_sm + 4] = bytes.fromhex("00 00 00 00")
print("Patched PythonPluginsEngine.initSdk -> loads BasePlugin in safe mode")

# Patch 11: PythonPluginsEngine.requireBasePluginClass() -> Lazy bootstrap SDK on demand
off_rbp_sm = 0x224eea
assert dex1[off_rbp_sm : off_rbp_sm + 4] == bytes.fromhex("39 00 48 00")
dex1[off_rbp_sm : off_rbp_sm + 4] = bytes.fromhex("00 00 00 00")

off_rbp_throw = 0x224f6a
assert dex1[off_rbp_throw : off_rbp_throw + 16] == bytes.fromhex("22 00 69 16 1a 01 21 a3 70 20 3f 6a 10 00 27 00")
# invoke-direct {v3}, initSdk:()Z (70 10 af 43 03 00)
# goto 000b / 224ef6 (28 c3)
# nop padding (00 00 00 00 00 00 00 00)
dex1[off_rbp_throw : off_rbp_throw + 16] = bytes.fromhex("70 10 af 43 03 00 28 c3 00 00 00 00 00 00 00 00")
print("Patched PythonPluginsEngine.requireBasePluginClass -> lazily bootstraps SDK on demand (FIXES CRASH)")

# Patch 12: PythonPluginsEngine.findModuleNameOwner -> return null immediately
off_fmno = 0x223728
assert dex1[off_fmno : off_fmno + 4] == bytes.fromhex("1a 00 30 d9")
dex1[off_fmno : off_fmno + 4] = bytes.fromhex("12 00 11 00") # const/4 v0, 0; return-object v0
print("Patched PythonPluginsEngine.findModuleNameOwner -> returns null (prevents false collisions)")

# Patch 13: PythonPluginsEngine.createPluginInstance -> bypass false module conflict check
off_cpi = 0x22304a
assert dex1[off_cpi : off_cpi + 4] == bytes.fromhex("39 07 27 00")
dex1[off_cpi : off_cpi + 4] = bytes.fromhex("28 27 00 00") # goto 0094
print("Patched PythonPluginsEngine.createPluginInstance -> bypasses false module collision error")

# Patch 14: PythonPluginsEngine.stopAndUnloadSdk -> return-void immediately
off_stop = 0x3dce74
assert dex1[off_stop : off_stop + 4] == bytes.fromhex("54 60 95 18")
dex1[off_stop : off_stop + 4] = bytes.fromhex("0e 00 00 00") # return-void; nop
print("Patched PythonPluginsEngine.stopAndUnloadSdk -> preserves C extension modules across toggle")

# Patch 15: PythonPluginsEngine.parsePluginMetadata -> return empty map on error
off_ppm = 0x224964
assert dex1[off_ppm : off_ppm + 2] == bytes.fromhex("27 03")
dex1[off_ppm : off_ppm + 2] = bytes.fromhex("28 01") # goto +1 -> return-object v0
print("Patched PythonPluginsEngine.parsePluginMetadata -> returns gracefully on metadata error")

# Patch 16: ApplicationLoader.getFilesDirFixed fallback string
old_data_str = b")/data/data/" + OLD_PACKAGE.encode("utf-8") + b"/files\x00"
new_data_str = b")/data/data/" + NEW_PACKAGE.encode("utf-8") + b"/files/////\x00"
assert len(old_data_str) == len(new_data_str) == 43
assert dex1.count(old_data_str) == 1
idx_ds = dex1.find(old_data_str)
dex1[idx_ds : idx_ds + len(new_data_str)] = new_data_str
print("Patched ApplicationLoader.getFilesDirFixed fallback path -> points to com.red.nfgram.chat")

# Update DEX1 checksums
dex1[12:32] = hashlib.sha1(dex1[32:]).digest()
dex1[8:12] = struct.pack("<I", zlib.adler32(dex1[12:]) & 0xFFFFFFFF)
print("Updated classes.dex SHA-1 and Adler32 checksums.")

# -----------------------------------------------------------------
# 4. Patch classes7.dex: EarListener.isNearToSensor
# -----------------------------------------------------------------
print("=== STEP 5: Patching classes7.dex ===")
off_sensor2 = 0x314084
assert dex7[off_sensor2 : off_sensor2 + 4] == bytes.fromhex("15 00 a0 40")
dex7[off_sensor2 : off_sensor2 + 4] = bytes.fromhex("15 00 00 40")
print("Patched EarListener.isNearToSensor in classes7.dex -> 2.0f threshold")

dex7[12:32] = hashlib.sha1(dex7[32:]).digest()
dex7[8:12] = struct.pack("<I", zlib.adler32(dex7[12:]) & 0xFFFFFFFF)
print("Updated classes7.dex SHA-1 and Adler32 checksums.")

# -----------------------------------------------------------------
# 5. Native libraries (libtmessages.49.so in arm64-v8a & armeabi-v7a)
# -----------------------------------------------------------------
print("=== STEP 6: Patching Native Libraries ===")
so_patches = {}
with zipfile.ZipFile(NEW_CORE_APK, "r") as z:
    # arm64-v8a
    so64 = bytearray(z.read("lib/arm64-v8a/libtmessages.49.so"))
    assert so64[0x62fe28 : 0x62fe2c] == bytes.fromhex("ff c3 01 d1")
    so64[0x62fe28 : 0x62fe2c] = bytes.fromhex("c0 03 5f d6") # ret
    so_patches["lib/arm64-v8a/libtmessages.49.so"] = so64
    print("Patched lib/arm64-v8a/libtmessages.49.so (NativeCrashHandler neutralized with ret)")
    
    # armeabi-v7a
    so32 = bytearray(z.read("lib/armeabi-v7a/libtmessages.49.so"))
    assert so32[0x3236c0 : 0x3236c4] == bytes.fromhex("f0 4f 2d e9")
    so32[0x3236c0 : 0x3236c4] = bytes.fromhex("1e ff 2f e1") # bx lr
    so_patches["lib/armeabi-v7a/libtmessages.49.so"] = so32
    print("Patched lib/armeabi-v7a/libtmessages.49.so (NativeCrashHandler neutralized with bx lr)")

# -----------------------------------------------------------------
# 6. Icons and Splash Drawables
# -----------------------------------------------------------------
print("=== STEP 7: Preparing Emerald Green Branding Icons ===")
icon_replacements = {}
GREEN_COLOR = (46, 204, 113, 255) # #2ecc71 emerald green

with zipfile.ZipFile(NEW_CORE_APK, "r") as z:
    fg_5cm_bytes = z.read("res/5cm.webp")
    fg_432 = Image.open(io.BytesIO(fg_5cm_bytes)).convert("RGBA")

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

# Patch res/Twu.xml
with zipfile.ZipFile(NEW_CORE_APK, "r") as z:
    twu_raw = bytearray(z.read("res/Twu.xml"))

# Replace circle color (@0x7f060088) with emerald green #ff2ecc71
# Replace plane color (@0x7f06008a) with pure white #ffffffff
old_circle_ref = bytes.fromhex("08 00 00 01 88 00 06 7f")
new_circle_col = bytes.fromhex("08 00 00 1d 71 cc 2e ff")
old_plane_ref  = bytes.fromhex("08 00 00 01 8a 00 06 7f")
new_plane_col  = bytes.fromhex("08 00 00 1d ff ff ff ff")

twu_patched = twu_raw.replace(old_circle_ref, new_circle_col).replace(old_plane_ref, new_plane_col)
icon_replacements["res/Twu.xml"] = bytes(twu_patched)
print("Prepared emerald green launcher icons & vector splash screen")

# -----------------------------------------------------------------
# 7. Repack Unaligned APK
# -----------------------------------------------------------------
print("=== STEP 8: Repacking Unaligned APK ===")
unaligned_apk = r"C:\project\ayugram\Tools\nfgram_13_unaligned.apk"
if os.path.exists(unaligned_apk):
    os.remove(unaligned_apk)

with zipfile.ZipFile(NEW_CORE_APK, "r") as zin, zipfile.ZipFile(unaligned_apk, "w") as zout:
    for item in zin.infolist():
        # Exclude old v1 signatures
        if item.filename.startswith("META-INF/") and (item.filename.endswith(".SF") or item.filename.endswith(".RSA") or item.filename.endswith(".MF")):
            continue
        
        if item.filename == "AndroidManifest.xml":
            zout.writestr(item, final_manifest)
        elif item.filename == "resources.arsc":
            zout.writestr(item, final_arsc)
        elif item.filename == "classes.dex":
            zout.writestr(item, dex1)
        elif item.filename == "classes7.dex":
            zout.writestr(item, dex7)
        elif item.filename in so_patches:
            zout.writestr(item, so_patches[item.filename], compress_type=item.compress_type)
        elif item.filename in icon_replacements:
            zout.writestr(item, icon_replacements[item.filename])
        else:
            data = zin.read(item.filename)
            zout.writestr(item, data, compress_type=item.compress_type)

print(f"Created unaligned APK: {unaligned_apk} ({os.path.getsize(unaligned_apk)} bytes)")

# -----------------------------------------------------------------
# 8. Zipalign APK
# -----------------------------------------------------------------
print("=== STEP 9: Zipalign APK ===")
aligned_apk = r"C:\project\ayugram\Tools\nfgram_13_aligned.apk"
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)

res = subprocess.run([ZIPALIGN, "-p", "-f", "4", unaligned_apk, aligned_apk], capture_output=True, text=True)
if res.returncode != 0:
    print("Zipalign error:", res.stderr)
    sys.exit(1)
print(f"Zipaligned APK: {aligned_apk}")

# -----------------------------------------------------------------
# 9. Sign APK
# -----------------------------------------------------------------
print("=== STEP 10: Sign APK with apksigner ===")
sign_cmd = [
    APKSIGNER, "sign",
    "--ks", KEYSTORE,
    "--ks-pass", f"pass:{KEYSTORE_PASS}",
    "--ks-key-alias", KEY_ALIAS,
    "--key-pass", f"pass:{KEYSTORE_PASS}",
    "--v1-signing-enabled", "true",
    "--v2-signing-enabled", "true",
    "--v3-signing-enabled", "true",
    aligned_apk
]
res = subprocess.run(sign_cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Apksigner error:", res.stderr)
    sys.exit(1)
print("Successfully signed APK with v2/v3 signatures!")

# -----------------------------------------------------------------
# 10. Verify APK
# -----------------------------------------------------------------
print("=== STEP 11: Verification ===")
verify_res = subprocess.run([APKSIGNER, "verify", "-v", aligned_apk], capture_output=True, text=True)
print("apksigner verify:\n", verify_res.stdout)

badging_res = subprocess.run([AAPT, "dump", "badging", aligned_apk], capture_output=True, text=True)
for line in badging_res.stdout.splitlines()[:5]:
    print("badging:", line)

# Deploy to target paths
TARGET_DESKTOP = r"C:\Users\styuk\Desktop\NfGram-13.1.1-universal.apk"
TARGET_DOWNLOADS = r"C:\Users\styuk\Downloads\NfGram-13.1.1-universal.apk"

with open(aligned_apk, "rb") as f_src:
    apk_bytes = f_src.read()

with open(TARGET_DESKTOP, "wb") as f_dst:
    f_dst.write(apk_bytes)
print(f"Deployed to {TARGET_DESKTOP} ({len(apk_bytes)} bytes)")

with open(TARGET_DOWNLOADS, "wb") as f_dst:
    f_dst.write(apk_bytes)
print(f"Deployed to {TARGET_DOWNLOADS} ({len(apk_bytes)} bytes)")
print("ALL DONE SUCCESSFULLY!")
