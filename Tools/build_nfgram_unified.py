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
import xml.etree.ElementTree as ET

VANILLA_APK = r"c:\Users\styuk\Downloads\AyuGram Desktop\vanilla-AyuGram-full-20261005.apk"
EXTERA_APK = r"c:\Users\styuk\Downloads\AyuGram Desktop\exteraGram-full-universal-20261004.apk"

OUTPUT_APK_PROJECT = r"C:\project\ayugram\NfGram-12.10.6-universal.apk"
OUTPUT_APK_DESKTOP = r"C:\Users\styuk\Desktop\NfGram-12.10.6-universal.apk"
OUTPUT_APK_AYU_DIR = r"c:\Users\styuk\Downloads\AyuGram Desktop\NfGram-12.10.6-universal.apk"
OUTPUT_APK_AYU_ALT = r"c:\Users\styuk\Downloads\AyuGram Desktop\AyuGram-12.10.6-universal.apk"
OUTPUT_APK_DOWNLOADS = r"c:\Users\styuk\Downloads\NfGram-12.10.6-universal.apk"

KEYSTORE = r"C:\project\ayugram\Tools\nfgram_release.keystore"
ZIPALIGN = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\zipalign.exe"
APKSIGNER = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\apksigner.bat"
AAPT = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\aapt.exe"
DEXDUMP = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\dexdump.exe"

OLD_PACKAGE = "com.radolyn.ayugram"
NEW_PACKAGE = "com.red.nfgram.chat"
assert len(NEW_PACKAGE) == len(OLD_PACKAGE) == 19

print("=== STEP 1: Patch DEX files ===")
with zipfile.ZipFile(VANILLA_APK, "r") as z:
    dex1 = bytearray(z.read("classes.dex"))
    dex4 = bytearray(z.read("classes4.dex"))
    dex5 = bytearray(z.read("classes5.dex"))
    dex6 = bytearray(z.read("classes6.dex"))
    dex7 = bytearray(z.read("classes7.dex"))
    manifest = bytearray(z.read("AndroidManifest.xml"))
    arsc = bytearray(z.read("resources.arsc"))

# -------------------------------------------------------------
# 1. Patch classes.dex: parallel upload, package name, battery
# -------------------------------------------------------------
seq1 = b"\x52\xa3\x87\x31\x35\x23\x09\x00\xb0\x23\x59\xa3\x87\x31"
seq2 = b"\x52\xa3\x86\x31\x35\x23\x09\x00\xb0\x23\x59\xa3\x86\x31"
assert dex1.count(seq1) == 1 and dex1.count(seq2) == 1
idx1 = dex1.find(seq1)
idx2 = dex1.find(seq2)
dex1[idx1+4 : idx1+8] = b"\x00\x00\x00\x00"
dex1[idx2+4 : idx2+8] = b"\x00\x00\x00\x00"
print("Applied parallel upload patches in classes.dex")

# Battery Patch 1: Disable persistent file logging to disk (BuildVars.LOGS_ENABLED = false)
assert dex1[0x2905f4 : 0x2905f4 + 12] == bytes.fromhex("71 00 12 2f 00 00 0a 00 6a 00 35 2e".replace(" ", ""))
dex1[0x2905f4 : 0x2905f4 + 12] = bytes.fromhex("12 00 6a 00 35 2e 00 00 00 00 00 00".replace(" ", ""))
print("Applied Battery patch 1: LOGS_ENABLED disabled")

# Battery Patch 2: Disable Proximity sensor polling (raiseToListen) and GPU blur shaders in SharedConfig.<clinit>
assert dex1[0x3339b8 : 0x3339bc] == bytes.fromhex("6a 03 11 80".replace(" ", ""))
dex1[0x3339b8 : 0x3339bc] = bytes.fromhex("6a 02 11 80".replace(" ", "")) # photoViewerBlur = false

assert dex1[0x333a0c : 0x333a10] == bytes.fromhex("6a 03 1f 80".replace(" ", ""))
dex1[0x333a0c : 0x333a10] = bytes.fromhex("6a 02 1f 80".replace(" ", "")) # raiseToListen = false

assert dex1[0x333a98 : 0x333a9c] == bytes.fromhex("6a 03 dc 7f".replace(" ", ""))
dex1[0x333a98 : 0x333a9c] = bytes.fromhex("6a 02 dc 7f".replace(" ", "")) # drawActionBarShadow = false
print("Applied Battery patch 2: SharedConfig sensor polling & blur defaults disabled")

# Battery Patch 3: Force disable real-time compute blur shaders (SharedConfig.useNewBlur = false)
assert dex1[0x3345c6 : 0x3345cc] == bytes.fromhex("0a 02 6a 02 46 80".replace(" ", ""))
dex1[0x3345c6 : 0x3345cc] = bytes.fromhex("12 02 6a 02 46 80".replace(" ", ""))
print("Applied Battery patch 3: useNewBlur disabled")

# Battery Patch 4: Disable persistent background WakeLock service (AyuConfig.keepAliveService = false)
assert dex1[0x24a674 : 0x24a67e] == bytes.fromhex("71 00 da 71 00 00 0a 03 b7 43".replace(" ", ""))
dex1[0x24a674 : 0x24a67e] = bytes.fromhex("12 03 00 00 00 00 00 00 00 00".replace(" ", ""))
print("Applied Battery patch 4: keepAliveService default set to false")

old_dir = b"/data/data/" + OLD_PACKAGE.encode("utf-8") + b"/files"
new_dir = b"/data/data/" + NEW_PACKAGE.encode("utf-8") + b"/files"
assert dex1.count(old_dir) == 1
idx_dir = dex1.find(old_dir)
dex1[idx_dir : idx_dir + len(old_dir)] = new_dir

string_ids_off1 = struct.unpack("<I", dex1[60:64])[0]
str56764_off = struct.unpack("<I", dex1[string_ids_off1 + 56764*4 : string_ids_off1 + 56765*4])[0]
expected_old_entry = b"\x13" + OLD_PACKAGE.encode("utf-8") + b"\x00"
new_entry = b"\x13" + NEW_PACKAGE.encode("utf-8") + b"\x00"
assert dex1[str56764_off : str56764_off + 21] == expected_old_entry
dex1[str56764_off : str56764_off + 21] = new_entry

dex1[12:32] = hashlib.sha1(dex1[32:]).digest()
dex1[8:12] = struct.pack("<I", zlib.adler32(dex1[12:]) & 0xFFFFFFFF)

# -------------------------------------------------------------
# 2. Patch classes4.dex: Merge AyuGram Preferences into MainPreferencesActivity
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
print("Applied MainPreferencesActivity unified AyuGram settings patch in classes4.dex")

# -------------------------------------------------------------
# 3. Patch classes5.dex: package name
# -------------------------------------------------------------
string_ids_off5 = struct.unpack("<I", dex5[60:64])[0]
str41733_off = struct.unpack("<I", dex5[string_ids_off5 + 41733*4 : string_ids_off5 + 41734*4])[0]
assert dex5[str41733_off : str41733_off + 21] == expected_old_entry
dex5[str41733_off : str41733_off + 21] = new_entry

dex5[12:32] = hashlib.sha1(dex5[32:]).digest()
dex5[8:12] = struct.pack("<I", zlib.adler32(dex5[12:]) & 0xFFFFFFFF)

# -------------------------------------------------------------
# 4. Patch classes6.dex: Face Unlock in Settings + Single Unified Settings Button
# -------------------------------------------------------------
# 4.1 updateRows: canAuthenticate 0x00FF and allocate +2 rows
assert dex6[0x52acee : 0x52acf2] == b"\x13\x01\x0f\x00"
dex6[0x52acee : 0x52acf2] = b"\x13\x01\xff\x00"
assert dex6[0x52ad0e : 0x52ad12] == b"\xd8\x01\x00\x01"
dex6[0x52ad0e : 0x52ad12] = b"\xd8\x01\x00\x02"

# 4.2 isEnabled: allow click on fingerprintRow AND fingerprintRow + 1
code_enabled = bytearray()
code_enabled.extend(b"\x6e\x10\x4f\x07\x02\x00") # invoke-virtual {v2}, getAdapterPosition
code_enabled.extend(b"\x0a\x02")                 # move-result v2
checks_enabled = [
    (0x8a05, True),  # fingerprintRow (has +1 face row check)
    (0x89fc, False), # autoLockRow
    (0x89ff, False), # captureRow
    (0x8a00, False), # changePasscodeRow
    (0x8a04, False), # disablePasscodeRow
]
ret1_phs = []
for f_id, has_face in checks_enabled:
    code_enabled.extend(b"\x54\x10\xf8\x89") # iget-object v0, v1, this$0
    code_enabled.extend(b"\x52\x00" + struct.pack("<H", f_id)) # iget v0, v0, field
    ret1_phs.append(len(code_enabled))
    code_enabled.extend(b"\x32\x02\x00\x00") # if-eq v2, v0, -> return_1
    if has_face:
        code_enabled.extend(b"\xd8\x00\x00\x01") # add-int/lit8 v0, v0, 1
        ret1_phs.append(len(code_enabled))
        code_enabled.extend(b"\x32\x02\x00\x00") # if-eq v2, v0, -> return_1

code_enabled.extend(b"\x12\x01") # const/4 v1, 0
code_enabled.extend(b"\x0f\x01") # return v1

ret1_pos = len(code_enabled)
code_enabled.extend(b"\x12\x11") # const/4 v1, 1
code_enabled.extend(b"\x0f\x01") # return v1

for ph in ret1_phs:
    delta = (ret1_pos - ph) // 2
    code_enabled[ph+2:ph+4] = struct.pack("<h", delta)

while len(code_enabled) < 98:
    code_enabled.extend(b"\x00\x00")
assert len(code_enabled) == 98
dex6[0x527e7c : 0x527e7c + 98] = code_enabled

# 4.3 onBindViewHolder: shorten DisablePasscode to free 14 bytes and bind Face Unlock
assert dex6[0x528318:0x52831c] == b"\x60\x05\x5a\x40"
shortened_bind = bytearray()
shortened_bind.extend(b"\x71\x10\x4e\x3f\x05\x00") # invoke-static Theme.getColor
shortened_bind.extend(b"\x0a\x05")                 # move-result v5
shortened_bind.extend(b"\x6e\x20\x14\x64\x56\x00") # invoke-virtual TextSettingsCell.setTextColor
shortened_bind.extend(b"\x0e\x00")                 # return-void
assert len(shortened_bind) == 16
dex6[0x52831c : 0x52832c] = shortened_bind

# Update branch at 0x528006
delta_branch = (0x52832c - 0x528006) // 2
dex6[0x528008 : 0x52800a] = struct.pack("<h", delta_branch)

# Bind TextCheckCells from 0x52832c to 0x528392 (102 bytes)
code_bind = bytearray()
code_bind.extend(b"\x54\x66\x9f\x00") # iget-object v6, v6, ViewHolder.itemView
code_bind.extend(b"\x1f\x06\xe8\x17") # check-cast v6, TextCheckCell
code_bind.extend(b"\x12\x01")         # const/4 v1, 0
code_bind.extend(b"\x54\x50\xf8\x89") # iget-object v0, v5, ListAdapter.this$0
code_bind.extend(b"\x52\x00\x05\x8a") # iget v0, v0, PasscodeActivity.fingerprintRow

fp_ph = len(code_bind)
code_bind.extend(b"\x32\x07\x00\x00") # if-eq v7, v0, -> :is_fp
code_bind.extend(b"\xd8\x00\x00\x01") # add-int/lit8 v0, v0, 1
face_ph = len(code_bind)
code_bind.extend(b"\x32\x07\x00\x00") # if-eq v7, v0, -> :is_face

# Capture row:
code_bind.extend(b"\x60\x05\x3b\x13") # sget v5, R$string.ScreenCaptureShowContent
code_bind.extend(b"\x63\x07\x34\x17") # sget-boolean v7, SharedConfig.allowScreenCapture
load_str_ph = len(code_bind)
code_bind.extend(b"\x28\x00")         # goto -> :load_string_res

# :is_fp:
fp_pos = len(code_bind)
code_bind.extend(b"\x60\x05\x8d\x15") # sget v5, R$string.UnlockFingerprint
code_bind.extend(b"\x63\x07\x7d\x17") # sget-boolean v7, SharedConfig.useFingerprintLock

# :load_string_res:
load_str_pos = len(code_bind)
code_bind.extend(b"\x71\x10\x70\x0f\x05\x00") # invoke-static {v5}, LocaleController.getString(int)
code_bind.extend(b"\x0c\x05")                 # move-result-object v5
set_btn_ph = len(code_bind)
code_bind.extend(b"\x28\x00")                 # goto -> :set_button_and_return

# :is_face:
face_pos = len(code_bind)
code_bind.extend(b"\x1a\x05\xa4\x4c")         # const-string v5, "camera"
code_bind.extend(b"\x60\x05\x6a\x09")         # sget v5, R$string.camera
code_bind.extend(b"\x71\x10\x70\x0f\x05\x00") # invoke-static {v5}, LocaleController.getString(int)
code_bind.extend(b"\x0c\x05")                 # move-result-object v5
code_bind.extend(b"\x71\x00\xc0\x11\x00\x00") # invoke-static {}, MessagesController.getGlobalMainSettings()
code_bind.extend(b"\x0c\x07")                 # move-result-object v7
code_bind.extend(b"\x1a\x08\xa4\x4c")         # const-string v8, "camera"
code_bind.extend(b"\x12\x09")                 # const/4 v9, 0
code_bind.extend(b"\x6e\x30\x6d\x01\x87\x09") # invoke-interface {v7, v8, v9}, SharedPreferences.getBoolean
code_bind.extend(b"\x0a\x07")                 # move-result v7

# :set_button_and_return:
set_btn_pos = len(code_bind)
code_bind.extend(b"\x6e\x50\x29\x64\x46\x05\x70") # invoke-virtual {v6, v5, v7, v1}, TextCheckCell.setTextAndCheck
code_bind.extend(b"\x0e\x00")                     # return-void

delta_fp = (fp_pos - fp_ph) // 2
code_bind[fp_ph+2:fp_ph+4] = struct.pack("<h", delta_fp)
delta_face = (face_pos - face_ph) // 2
code_bind[face_ph+2:face_ph+4] = struct.pack("<h", delta_face)
delta_load = (load_str_pos - load_str_ph) // 2
code_bind[load_str_ph+1] = delta_load
delta_btn = (set_btn_pos - set_btn_ph) // 2
code_bind[set_btn_ph+1] = delta_btn

while len(code_bind) < 102:
    code_bind.extend(b"\x00\x00")
assert len(code_bind) == 102
dex6[0x52832c : 0x52832c + 102] = code_bind

# 4.4 onClick: Handle clicks on fingerprintRow, fingerprintRow + 1, and captureRow
code_click = bytearray()
code_click.extend(b"\x1f\x02\xb6\x37")         # check-cast v2, TextCheckCell
code_click.extend(b"\x6e\x10\x4f\x07\x04\x00") # invoke-virtual {v4}, getAdapterPosition
code_click.extend(b"\x0a\x04")                 # move-result v4
code_click.extend(b"\x54\x35\xf8\x89")         # iget-object v5, v3, this$0
code_click.extend(b"\x52\x55\xff\x89")         # iget v5, v5, captureRow

capture_ph = len(code_click)
code_click.extend(b"\x33\x54\x00\x00")         # if-ne v4, v5, -> :check_fingerprint
code_click.extend(b"\x63\x07\x34\x17")         # sget-boolean v7, SharedConfig.allowScreenCapture
code_click.extend(b"\x12\x16")                 # const/4 v6, 1
code_click.extend(b"\xb1\x67")                 # xor-int/2addr v7, v6
code_click.extend(b"\x6a\x07\x34\x17")         # sput-boolean v7, SharedConfig.allowScreenCapture
code_click.extend(b"\x6e\x20\x2a\x64\x72\x00") # invoke-virtual {v2, v7}, TextCheckCell.setChecked
code_click.extend(b"\x71\x00\xc0\x11\x00\x00") # invoke-static {}, MessagesController.getGlobalMainSettings()
code_click.extend(b"\x0c\x06")                 # move-result-object v6
code_click.extend(b"\x6e\x10\x77\x01\x06\x00") # invoke-interface {v6}, edit()
code_click.extend(b"\x0c\x06")                 # move-result-object v6
code_click.extend(b"\x1a\x07\xa2\x38")         # const-string v7, "fFingerprint"
code_click.extend(b"\x63\x08\x34\x17")         # sget-boolean v8, SharedConfig.allowScreenCapture
code_click.extend(b"\x6e\x30\x97\x01\x86\x07") # invoke-interface {v6, v7, v8}, putBoolean
code_click.extend(b"\x6e\x10\x69\x01\x06\x00") # invoke-interface {v6}, commit()
code_click.extend(b"\x0e\x00")                 # return-void

# :check_fingerprint:
capture_next = len(code_click)
delta_cap = (capture_next - capture_ph) // 2
code_click[capture_ph+2:capture_ph+4] = struct.pack("<h", delta_cap)

code_click.extend(b"\x54\x35\xf8\x89")         # iget-object v5, v3, this$0
code_click.extend(b"\x52\x55\x05\x8a")         # iget v5, v5, fingerprintRow

fp_click_ph = len(code_click)
code_click.extend(b"\x33\x54\x00\x00")         # if-ne v4, v5, -> :check_face
code_click.extend(b"\x63\x07\x7d\x17")         # sget-boolean v7, SharedConfig.useFingerprintLock
code_click.extend(b"\x12\x16")                 # const/4 v6, 1
code_click.extend(b"\xb1\x67")                 # xor-int/2addr v7, v6
code_click.extend(b"\x6a\x07\x7d\x17")         # sput-boolean v7, SharedConfig.useFingerprintLock
code_click.extend(b"\x6e\x20\x2a\x64\x72\x00") # invoke-virtual {v2, v7}, TextCheckCell.setChecked
code_click.extend(b"\x71\x00\xc0\x11\x00\x00") # invoke-static {}, MessagesController.getGlobalMainSettings()
code_click.extend(b"\x0c\x06")                 # move-result-object v6
code_click.extend(b"\x6e\x10\x77\x01\x06\x00") # invoke-interface {v6}, edit()
code_click.extend(b"\x0c\x06")                 # move-result-object v6
code_click.extend(b"\x1a\x07\xad\x3c")         # const-string v7, "useFingerprintLock"
code_click.extend(b"\x63\x08\x7d\x17")         # sget-boolean v8, SharedConfig.useFingerprintLock
code_click.extend(b"\x6e\x30\x97\x01\x86\x07") # invoke-interface {v6, v7, v8}, putBoolean
code_click.extend(b"\x6e\x10\x69\x01\x06\x00") # invoke-interface {v6}, commit()
code_click.extend(b"\x0e\x00")                 # return-void

# :check_face:
fp_click_next = len(code_click)
delta_fp_c = (fp_click_next - fp_click_ph) // 2
code_click[fp_click_ph+2:fp_click_ph+4] = struct.pack("<h", delta_fp_c)

code_click.extend(b"\xd8\x05\x05\x01")         # add-int/lit8 v5, v5, 1
face_click_ph = len(code_click)
code_click.extend(b"\x33\x54\x00\x00")         # if-ne v4, v5, -> :exit
code_click.extend(b"\x71\x00\xc0\x11\x00\x00") # invoke-static {}, MessagesController.getGlobalMainSettings()
code_click.extend(b"\x0c\x06")                 # move-result-object v6
code_click.extend(b"\x1a\x07\xa4\x4c")         # const-string v7, "camera"
code_click.extend(b"\x12\x08")                 # const/4 v8, 0
code_click.extend(b"\x6e\x30\x6d\x01\x86\x07") # invoke-interface {v6, v7, v8}, getBoolean
code_click.extend(b"\x0a\x08")                 # move-result v8
code_click.extend(b"\x12\x17")                 # const/4 v7, 1
code_click.extend(b"\xb1\x78")                 # xor-int/2addr v8, v7
code_click.extend(b"\x6e\x20\x2a\x64\x82\x00") # invoke-virtual {v2, v8}, TextCheckCell.setChecked
code_click.extend(b"\x6e\x10\x77\x01\x06\x00") # invoke-interface {v6}, edit()
code_click.extend(b"\x0c\x06")                 # move-result-object v6
code_click.extend(b"\x1a\x07\xa4\x4c")         # const-string v7, "camera"
code_click.extend(b"\x6e\x30\x97\x01\x86\x07") # invoke-interface {v6, v7, v8}, putBoolean
code_click.extend(b"\x6e\x10\x69\x01\x06\x00") # invoke-interface {v6}, commit()
code_click.extend(b"\x0e\x00")                 # return-void

# :exit:
face_click_next = len(code_click)
delta_face_c = (face_click_next - face_click_ph) // 2
code_click[face_click_ph+2:face_click_ph+4] = struct.pack("<h", delta_face_c)

while len(code_click) < 216:
    code_click.extend(b"\x00\x00")
assert len(code_click) == 216
dex6[0x52857e : 0x52857e + 216] = code_click

# 4.5 Unify Settings Buttons in ProfileActivity and SettingsActivity
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
dex6[0x62e504 : 0x62e504 + len(orig_ayu_row)] = b"\x00" * len(orig_ayu_row) # 19 NOPs
print("Applied SettingsActivity single green button patch in classes6.dex")

dex6[12:32] = hashlib.sha1(dex6[32:]).digest()
dex6[8:12] = struct.pack("<I", zlib.adler32(dex6[12:]) & 0xFFFFFFFF)

# -------------------------------------------------------------
# 5. Patch classes7.dex: Face Unlock in PasscodeView
# -------------------------------------------------------------
# 5.1 checkFingerprintButton: canAuthenticate 0x00FF
assert dex7[0x37e28e : 0x37e292] == b"\x13\x01\x0f\x00"
dex7[0x37e28e : 0x37e292] = b"\x13\x01\xff\x00"

# checkFingerprintButton: check face unlock preference
start_pos_btn = 0x37e2b4
target_5a = 0x37e33e
target_6a = 0x37e34c

code_btn = bytearray()
code_btn.extend(b"\x63\x02\x7d\x18")                             # sget-boolean v2, SharedConfig.useFingerprintLock
code_btn.extend(b"\x39\x02\x08\x00")                             # if-nez v2, -> target_5a
code_btn.extend(b"\x71\x00\x75\x12\x00\x00")                     # invoke-static {}, MessagesController.getGlobalMainSettings()
code_btn.extend(b"\x0c\x02")                                     # move-result-object v2
code_btn.extend(b"\x1a\x03\x99\x4d")                             # const-string v3, "camera"
code_btn.extend(b"\x12\x04")                                     # const/4 v4, 0
code_btn.extend(b"\x6e\x30\x67\x01\x82\x04")                     # invoke-interface {v2, v3, v4}, SharedPreferences.getBoolean
code_btn.extend(b"\x0a\x02")                                     # move-result v2

cur_pos = start_pos_btn + len(code_btn)
delta_5a = (target_5a - cur_pos) // 2
code_btn.extend(b"\x39\x02" + struct.pack("<h", delta_5a))       # if-nez v2, -> target_5a
cur_pos = start_pos_btn + len(code_btn)
delta_6a = (target_6a - cur_pos) // 2
code_btn.extend(b"\x28" + struct.pack("<b", delta_6a))           # goto -> target_6a

while len(code_btn) < 68:
    code_btn.extend(b"\x00\x00")
assert len(code_btn) == 68
dex7[start_pos_btn : start_pos_btn + 68] = code_btn

# 5.2 hasFingerprint: canAuthenticate 0x00FF and check face unlock preference
assert dex7[0x37e61a : 0x37e61e] == b"\x13\x01\x0f\x00"
dex7[0x37e61a : 0x37e61e] = b"\x13\x01\xff\x00"

start_pos_hf = 0x37e640
target_5a = 0x37e684
target_6a = 0x37e692

code_hf = bytearray()
code_hf.extend(b"\x63\x02\x7d\x18")                              # sget-boolean v2, SharedConfig.useFingerprintLock
code_hf.extend(b"\x39\x02\x08\x00")                              # if-nez v2, -> target_5a
code_hf.extend(b"\x71\x00\x75\x12\x00\x00")                      # invoke-static {}, MessagesController.getGlobalMainSettings()
code_hf.extend(b"\x0c\x02")                                      # move-result-object v2
code_hf.extend(b"\x1a\x03\x99\x4d")                              # const-string v3, "camera"
code_hf.extend(b"\x12\x04")                                      # const/4 v4, 0
code_hf.extend(b"\x6e\x30\x67\x01\x82\x04")                      # invoke-interface {v2, v3, v4}, SharedPreferences.getBoolean
code_hf.extend(b"\x0a\x02")                                      # move-result v2

cur_pos = start_pos_hf + len(code_hf)
delta_5a = (target_5a - cur_pos) // 2
code_hf.extend(b"\x39\x02" + struct.pack("<h", delta_5a))       # if-nez v2, -> target_5a
cur_pos = start_pos_hf + len(code_hf)
delta_6a = (target_6a - cur_pos) // 2
code_hf.extend(b"\x28" + struct.pack("<b", delta_6a))           # goto -> target_6a

while len(code_hf) < 64:
    code_hf.extend(b"\x00\x00")
assert len(code_hf) == 64
dex7[start_pos_hf : start_pos_hf + 64] = code_hf

dex7[12:32] = hashlib.sha1(dex7[32:]).digest()
dex7[8:12] = struct.pack("<I", zlib.adler32(dex7[12:]) & 0xFFFFFFFF)

# -------------------------------------------------------------
# Verify all DEX files using dexdump -c
# -------------------------------------------------------------
dex_list = [
    ("classes.dex", dex1),
    ("classes4.dex", dex4),
    ("classes5.dex", dex5),
    ("classes6.dex", dex6),
    ("classes7.dex", dex7)
]
for name, dex_data in dex_list:
    tmp_path = f"tmp_{name}"
    with open(tmp_path, "wb") as f: f.write(dex_data)
    res = subprocess.run([DEXDUMP, "-c", tmp_path], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"DEX verification failed for {name}:", res.stderr or res.stdout)
        exit(1)
    print(f"{name} passed dexdump verification successfully!")
    os.remove(tmp_path)

print("=== STEP 2: Patch AndroidManifest.xml ===")
old_pkg_u16 = OLD_PACKAGE.encode("utf-16le")
new_pkg_u16 = NEW_PACKAGE.encode("utf-16le")
manifest_count = manifest.count(old_pkg_u16)
assert manifest_count == 12
manifest = manifest.replace(old_pkg_u16, new_pkg_u16)
print(f"AndroidManifest.xml: successfully replaced all {manifest_count} package occurrences.")

print("=== STEP 3: Patch resources.arsc ===")
arsc_pkg_count = arsc.count(old_pkg_u16)
assert arsc_pkg_count == 1
arsc = arsc.replace(old_pkg_u16, new_pkg_u16)

# Patch Accent Color: #ffe83030 (red) -> #ff2ecc71 (green)
old_color_pattern = b"\x08\x00\x00\x1d\x30\x30\xe8\xff"
new_color_pattern = b"\x08\x00\x00\x1d\x71\xcc\x2e\xff"
assert arsc.count(old_color_pattern) == 1
arsc = arsc.replace(old_color_pattern, new_color_pattern)
print("Replaced red color #ffe83030 with green #ff2ecc71 in resources.arsc")

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

print("=== STEP 4: Prepare Green Icons ===")
icon_replacements = {}
with zipfile.ZipFile(EXTERA_APK, "r") as z_ext:
    fg_names = ["res/NtV.webp", "res/133.webp", "res/9Qo.webp", "res/iE4.webp", "res/5cm.webp"]
    for fn in fg_names:
        icon_replacements[fn] = z_ext.read(fn)

GREEN_COLOR = (46, 204, 113, 255) # #2ecc71 emerald green
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
        icon_replacements[res_name] = f.read()

print(f"Prepared {len(icon_replacements)} icon replacements (all green).")

print("=== STEP 5: Patch Locales (Face Unlock strings) ===")
xml_replacements = {}
with zipfile.ZipFile(VANILLA_APK, "r") as zin:
    for xml_path, string_val in [
        ("assets/ayu_locales/values-ru/ayu.xml", "Разблокировка по лицу"),
        ("assets/extera_locales/values-ru/extera.xml", "Разблокировка по лицу"),
        ("assets/ayu_locales/values/ayu.xml", "Face Unlock"),
        ("assets/extera_locales/values/extera.xml", "Face Unlock"),
    ]:
        xml_text = zin.read(xml_path).decode("utf-8")
        insert_line = f'  <string name="camera">{string_val}</string>\n</resources>'
        new_xml_text = xml_text.replace("</resources>", insert_line)
        ET.fromstring(new_xml_text)
        xml_replacements[xml_path] = new_xml_text.encode("utf-8")
        print(f"Patched locale XML: {xml_path}")

print("=== STEP 6: Repack APK ===")
unaligned_apk = r"C:\project\ayugram\Tools\nfgram_faceunlock_unaligned.apk"
if os.path.exists(unaligned_apk):
    os.remove(unaligned_apk)

with zipfile.ZipFile(VANILLA_APK, "r") as zin, zipfile.ZipFile(unaligned_apk, "w") as zout:
    for item in zin.infolist():
        if item.filename.startswith("META-INF/") and (item.filename.endswith(".SF") or item.filename.endswith(".RSA") or item.filename.endswith(".MF")):
            continue
        if item.filename == "classes.dex":
            zout.writestr(item, dex1)
        elif item.filename == "classes4.dex":
            zout.writestr(item, dex4)
        elif item.filename == "classes5.dex":
            zout.writestr(item, dex5)
        elif item.filename == "classes6.dex":
            zout.writestr(item, dex6)
        elif item.filename == "classes7.dex":
            zout.writestr(item, dex7)
        elif item.filename == "AndroidManifest.xml":
            zout.writestr(item, manifest)
        elif item.filename == "resources.arsc":
            zout.writestr(item, final_arsc)
        elif item.filename in icon_replacements:
            zout.writestr(item, icon_replacements[item.filename])
        elif item.filename in xml_replacements:
            zout.writestr(item, xml_replacements[item.filename])
        else:
            data = zin.read(item.filename)
            zout.writestr(item, data, compress_type=item.compress_type)

print(f"Created unaligned APK: {unaligned_apk} ({os.path.getsize(unaligned_apk)} bytes)")

print("=== STEP 7: Zipalign APK ===")
aligned_apk = r"C:\project\ayugram\Tools\nfgram_faceunlock_aligned.apk"
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)

res = subprocess.run([ZIPALIGN, "-p", "-f", "4", unaligned_apk, aligned_apk], capture_output=True, text=True)
if res.returncode != 0:
    print("Zipalign error:", res.stderr)
    exit(1)
print(f"Zipalign succeeded: {aligned_apk} ({os.path.getsize(aligned_apk)} bytes)")

print("=== STEP 8: Sign APK with NfGram Keystore ===")
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

print("=== STEP 9: Verify Signature and Badging ===")
res_sig = subprocess.run([APKSIGNER, "verify", "--verbose", "--print-certs", aligned_apk], capture_output=True, text=True)
for l in res_sig.stdout.splitlines():
    if "Verified" in l or "Signer #1 certificate DN" in l:
        print("  ", l)

res_badge = subprocess.run([AAPT, "dump", "badging", aligned_apk], capture_output=True, text=True)
for l in res_badge.stdout.splitlines():
    if "package:" in l or "application-label:" in l or "application-icon" in l:
        print("  ", l)

print("=== STEP 10: Deploy to destination paths ===")
destinations = [
    OUTPUT_APK_PROJECT,
    OUTPUT_APK_DESKTOP,
    OUTPUT_APK_AYU_DIR,
    OUTPUT_APK_AYU_ALT,
    OUTPUT_APK_DOWNLOADS,
]
for dst in destinations:
    try:
        dst_dir = os.path.dirname(dst)
        if os.path.exists(dst_dir):
            shutil.copy2(aligned_apk, dst)
            print(f"Deployed: {dst}")
    except Exception as e:
        print(f"Warning deploying to {dst}: {e}")

# Also update build_nfgram_faceunlock.py with this same working script
shutil.copy2(__file__, r"C:\project\ayugram\Tools\build_nfgram_faceunlock.py")
print("Updated Tools/build_nfgram_faceunlock.py")

print("\nALL DONE! GREEN ICON & UNIFIED SETTINGS BUILD COMPLETED 100% SUCCESSFULLY!")
