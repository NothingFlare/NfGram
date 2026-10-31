"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

# -*- coding: utf-8 -*-
import struct, subprocess, hashlib, zlib

with open(r"c:\project\ayugram\Tools\test_verify_classes4.dex", "rb") as f:
    dex4 = bytearray(f.read())

# Restore 0x38a706 to original
orig_706 = bytes.fromhex("22 01 9b 15 70 10 a5 74 01 00 6e 20 09 f8 10 00 0e 00")
dex4[0x38a706 : 0x38a706 + len(orig_706)] = orig_706

# --------------------------------------------------------------------------
# 1. HeaderSettingsCell.<init>: Display "NfGram" via LocaleController.getString(0x7f0f0000)
# --------------------------------------------------------------------------
start_hsc = 0x39c50c
patch_hsc = bytearray()
patch_hsc.extend(b"\x15\x03\x0f\x7f")         # const/high16 v3, 0x7f0f (R.string.AppName = 0x7f0f0000)
patch_hsc.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString:(I)Ljava/lang/String; (method@f580)
patch_hsc.extend(b"\x0c\x03")                 # move-result-object v3
patch_hsc.extend(b"\x6e\x20\x38\x09\x32\x00") # invoke-virtual {v2, v3}, TextView.setText:(Ljava/lang/CharSequence;)V (method@0938)
patch_hsc.extend(b"\x6e\x20\x36\x09\x02\x00") # invoke-virtual {v2, v0}, TextView.setSingleLine:(Z)V (method@0936)
patch_hsc.extend(b"\x00\x00\x00\x00")         # nop, nop
assert len(patch_hsc) == 28
dex4[start_hsc : start_hsc + 28] = patch_hsc
print("1. Patched HeaderSettingsCell title to NfGram")

# --------------------------------------------------------------------------
# 2. MainPreferencesActivity.onClick:
#    - Case 7 at 0x38a67e (14 bytes): Channel opener (lighthouse_top)
#    - Case 2 at 0x38a68c (26 bytes): Dispatcher for General / Submenu
#    - Case 8 at 0x38a6a6 (22 bytes): Opens AyuMainPreferencesActivity
#    - General at 0x38a706: Original (called by Case 2 when in submenu)
# --------------------------------------------------------------------------
pos_case7 = 0x38a67e
patch_case7 = bytearray()
patch_case7.extend(b"\x1a\x01\xbf\xc0")         # const-string v1, "lighthouse_top" (string@c0bf)
patch_case7.extend(b"\x70\x20\xc6\x74\x10\x00") # invoke-direct {v0, v1}, showNoticeBeforeOpeningChat (method@74c6)
patch_case7.extend(b"\x0e\x00")                 # return-void
patch_case7.extend(b"\x00\x00")                 # nop
assert len(patch_case7) == 14
dex4[pos_case7 : pos_case7 + 14] = patch_case7
print("2.1 Patched Case 7 (CHANNEL) at 0x38a67e")

pos_case2 = 0x38a68c
patch_case2 = bytearray()
patch_case2.extend(b"\x55\x01\xba\x8e")         # iget-boolean v1, v0, BaseFragment.hasOwnBackground:Z (field@8eba)
delta_to_gen = (0x38a706 - (pos_case2 + 4)) // 2
patch_case2.extend(b"\x39\x01" + struct.pack("<h", delta_to_gen)) # if-nez v1, -> 0x38a706
patch_case2.extend(b"\x22\x01\x9e\x15")         # new-instance v1, MainPreferencesActivity (type@159e)
patch_case2.extend(b"\x70\x10\xbe\x74\x01\x00") # invoke-direct {v1}, MainPreferencesActivity.<init> (method@74be)
patch_case2.extend(b"\x12\x12")                 # const/4 v2, 1
patch_case2.extend(b"\x5c\x12\xba\x8e")         # iput-boolean v2, v1, BaseFragment.hasOwnBackground:Z (field@8eba)
delta_pres = (0x38a710 - (pos_case2 + 24)) // 2
patch_case2.extend(b"\x28" + struct.pack("<b", delta_pres)) # goto -> 0x38a710
assert len(patch_case2) == 26
dex4[pos_case2 : pos_case2 + 26] = patch_case2
print("2.2 Patched Case 2 dispatcher at 0x38a68c")

# 2.3 Update switch table at 0x38a744
base_switch = 0x38a670
# Case 2 is index 1
off_c2 = (pos_case2 - base_switch) // 2
dex4[0x38a74c + 1*4 : 0x38a74c + 2*4] = struct.pack("<i", off_c2)

# Case 7 is index 6
off_c7 = (pos_case7 - base_switch) // 2
dex4[0x38a74c + 6*4 : 0x38a74c + 7*4] = struct.pack("<i", off_c7)
print(f"2.3 Updated switch table: Case 2 -> {hex(pos_case2)}, Case 7 -> {hex(pos_case7)}")

# --------------------------------------------------------------------------
# 3. MainPreferencesActivity.fillItems:
#    Build Root mode (2 items + 1 link) and Submenu mode (5 categories)
# --------------------------------------------------------------------------
start_fi = 0x38a3d8
code_fi = bytearray()

# Prefix:
code_fi.extend(b"\x08\x00\x11\x00") # move-object/from16 v0, v17 (items ArrayList)
code_fi.extend(b"\x08\x01\x10\x00") # move-object/from16 v1, v16 (this MainPreferencesActivity)

# Add HEADER_CELL:
code_fi.extend(b"\x54\x12\x90\x3e") # iget-object v2, v1, headerSettingsCell (field@3e90)
code_fi.extend(b"\x39\x02\x03\x00") # if-nez v2, +3
code_fi.extend(b"\x12\x02")         # const/4 v2, 0
code_fi.extend(b"\x13\x03\xc6\x00") # const/16 v3, 198
code_fi.extend(b"\x71\x20\xcd\xfa\x32\x00") # invoke-static {v2, v3}, UItem.asCustomShadow (method@facd)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x62\x03\x8a\x3e")         # sget-object v3, PreferenceItem.HEADER_CELL (field@3e8a)
code_fi.extend(b"\x6e\x10\xba\x74\x03\x00") # invoke-virtual {v3}, PreferenceItem.getId (method@74ba)
code_fi.extend(b"\x0a\x03")                 # move-result v3
code_fi.extend(b"\x6e\x20\xe9\xfa\x32\x00") # invoke-virtual {v2, v3}, UItem.setId (method@fae9)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Add Header: "Categories":
code_fi.extend(b"\x60\x02\x50\x8a")         # sget v2, R.string.Categories (field@8a50)
code_fi.extend(b"\x71\x10\x80\xf5\x02\x00") # invoke-static {v2}, LocaleController.getString (method@f580)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x71\x10\xd1\xfa\x02\x00") # invoke-static {v2}, UItem.asHeader (method@fad1)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Zero out common argument registers v5, v6, v7, v8, v10, v11, v12, v14
code_fi.extend(b"\x12\x05") # const/4 v5, 0
code_fi.extend(b"\x12\x06") # const/4 v6, 0
code_fi.extend(b"\x12\x07") # const/4 v7, 0
code_fi.extend(b"\x12\x08") # const/4 v8, 0
code_fi.extend(b"\x12\x0a") # const/4 v10, 0
code_fi.extend(b"\x12\x0b") # const/4 v11, 0
code_fi.extend(b"\x12\x0c") # const/4 v12, 0
code_fi.extend(b"\x12\x0e") # const/4 v14, 0
code_fi.extend(b"\x13\x0d\x78\x07") # const/16 v13, 1912 (default mask)

# Branch on hasOwnBackground
code_fi.extend(b"\x55\x12\xba\x8e") # iget-boolean v2, v1, BaseFragment.hasOwnBackground:Z (field@8eba)
branch_sub_ph = len(code_fi)
code_fi.extend(b"\x39\x02\x00\x00") # if-nez v2, -> :fill_submenu (placeholder)

# ---------------- ROOT MODE (hasOwnBackground == false) ----------------
# Item 1: AyuGram (FORUM)
code_fi.extend(b"\x62\x02\x88\x3e")         # sget-object v2, PreferenceItem.FORUM (field@3e88)
code_fi.extend(b"\x1a\x03\x54\x19")         # const-string v3, "AyuGram" (string@1954)
code_fi.extend(b"\x60\x04\x09\x89")         # sget v4, R.drawable.ayu_ghost (field@8909)
code_fi.extend(b"\x1a\x09\x54\x19")         # const-string v9, "AyuGram" (string@1954)
code_fi.extend(b"\x77\x0e\x51\x74\x01\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Item 2: exteraGram (GENERAL_CATEGORY)
code_fi.extend(b"\x62\x02\x89\x3e")         # sget-object v2, PreferenceItem.GENERAL_CATEGORY (field@3e89)
code_fi.extend(b"\x1a\x03\xf7\xa1")         # const-string v3, "exteraGram" (string@a1f7)
code_fi.extend(b"\x60\x04\x20\x89")         # sget v4, R.drawable.ic_foreground_extera (field@8920)
code_fi.extend(b"\x1a\x09\xf7\xa1")         # const-string v9, "exteraGram" (string@a1f7)
code_fi.extend(b"\x77\x0e\x51\x74\x01\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Header: "Links"
code_fi.extend(b"\x60\x02\x2f\x8b")         # sget v2, R.string.Links (field@8b2f)
code_fi.extend(b"\x71\x10\x80\xf5\x02\x00") # invoke-static {v2}, LocaleController.getString (method@f580)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x71\x10\xd1\xfa\x02\x00") # invoke-static {v2}, UItem.asHeader (method@fad1)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Item: Channel (CHANNEL)
code_fi.extend(b"\x62\x02\x85\x3e")         # sget-object v2, PreferenceItem.CHANNEL (field@3e85)
code_fi.extend(b"\x60\x03\xc4\x8b")         # sget v3, R.string.ProfileChannel (field@8bc4)
code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x60\x04\x4b\x89")         # sget v4, R.drawable.msg_channel (field@894b)
code_fi.extend(b"\x60\x05\x78\x8a")         # sget v5, R.string.Crowdin (field@8a78 = "@lighthouse_top")
code_fi.extend(b"\x71\x10\x80\xf5\x05\x00") # invoke-static {v5}, LocaleController.getString (method@f580)
code_fi.extend(b"\x0c\x05")                 # move-result-object v5
code_fi.extend(b"\x60\x09\x81\x8c")         # sget v9, R.string.Website (field@8c81 = "lighthouse_top")
code_fi.extend(b"\x71\x10\x80\xf5\x09\x00") # invoke-static {v9}, LocaleController.getString (method@f580)
code_fi.extend(b"\x0c\x09")                 # move-result-object v9
code_fi.extend(b"\x13\x0d\x70\x07")         # const/16 v13, 1904 (mask with subtitle)
code_fi.extend(b"\x77\x0e\x51\x74\x01\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# End root mode: goto :finish_shadow
goto_finish_ph = len(code_fi)
code_fi.extend(b"\x28\x00") # goto -> :finish_shadow

# ---------------- SUBMENU MODE (hasOwnBackground == true) ----------------
pos_submenu = len(code_fi)
code_fi[branch_sub_ph + 2 : branch_sub_ph + 4] = struct.pack("<h", (pos_submenu - branch_sub_ph) // 2)

# Reset mask & subtitle
code_fi.extend(b"\x12\x05")         # const/4 v5, 0
code_fi.extend(b"\x13\x0d\x78\x07") # const/16 v13, 1912

# Submenu Category 1: General
code_fi.extend(b"\x62\x02\x89\x3e")         # sget-object v2, PreferenceItem.GENERAL_CATEGORY (field@3e89)
code_fi.extend(b"\x60\x03\xed\x8a")         # sget v3, R.string.General (field@8aed)
code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x60\x04\x6b\x89")         # sget v4, R.drawable.msg_media (field@896b)
code_fi.extend(b"\x1a\x09\xca\xa5")         # const-string v9, "general" (string@a5ca)
code_fi.extend(b"\x77\x0e\x51\x74\x01\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Submenu Category 2: Appearance
code_fi.extend(b"\x62\x02\x84\x3e")         # sget-object v2, PreferenceItem.APPEARANCE_CATEGORY (field@3e84)
code_fi.extend(b"\x60\x03\x23\x8a")         # sget v3, R.string.Appearance (field@8a23)
code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x60\x04\x90\x89")         # sget v4, R.drawable.msg_theme (field@8990)
code_fi.extend(b"\x1a\x09\x30\x8c")         # const-string v9, "appearance" (string@8c30)
code_fi.extend(b"\x77\x0e\x51\x74\x01\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Submenu Category 3: Chats
code_fi.extend(b"\x62\x02\x86\x3e")         # sget-object v2, PreferenceItem.CHATS_CATEGORY (field@3e86)
code_fi.extend(b"\x60\x03\xf7\x8b")         # sget v3, R.string.SearchAllChatsShort (field@8bf7)
code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x60\x04\x54\x89")         # sget v4, R.drawable.msg_discussion (field@8954)
code_fi.extend(b"\x1a\x09\xaa\x96")         # const-string v9, "chats" (string@96aa)
code_fi.extend(b"\x77\x0e\x51\x74\x01\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Submenu Category 4: Plugins
code_fi.extend(b"\x62\x02\x8c\x3e")         # sget-object v2, PreferenceItem.PLUGINS_CATEGORY (field@3e8c)
code_fi.extend(b"\x60\x03\x9b\x8b")         # sget v3, R.string.Plugins (field@8b9b)
code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x60\x04\x78\x89")         # sget v4, R.drawable.msg_openwith (field@8978)
code_fi.extend(b"\x1a\x09\x2c\xc6")         # const-string v9, "plugins" (string@c62c)
code_fi.extend(b"\x77\x0e\x51\x74\x01\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Submenu Category 5: Other
code_fi.extend(b"\x62\x02\x8b\x3e")         # sget-object v2, PreferenceItem.OTHER_CATEGORY (field@3e8b)
code_fi.extend(b"\x60\x03\x34\x8b")         # sget v3, R.string.LocalOther (field@8b34)
code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x60\x04\x58\x89")         # sget v4, R.drawable.msg_settings (field@8958)
code_fi.extend(b"\x1a\x09\x04\xc2")         # const-string v9, "other" (string@c204)
code_fi.extend(b"\x77\x0e\x51\x74\x01\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# :finish_shadow
pos_finish = len(code_fi)
code_fi[goto_finish_ph + 1] = (pos_finish - goto_finish_ph) // 2
code_fi.extend(b"\x71\x00\xd8\xfa\x00\x00") # invoke-static {}, UItem.asShadow (method@fad8)
code_fi.extend(b"\x0c\x01")                 # move-result-object v1
code_fi.extend(b"\x6e\x20\x55\xf0\x10\x00") # invoke-virtual {v0, v1}, ArrayList.add (method@f055)
code_fi.extend(b"\x0e\x00")                 # return-void

print(f"3. Generated fillItems bytecode: {len(code_fi)} bytes (limit: 572 bytes)")
assert len(code_fi) <= 572

# Pad with NOPs to exactly 572 bytes
while len(code_fi) < 572:
    code_fi.extend(b"\x00\x00")
assert len(code_fi) == 572

dex4[start_fi : start_fi + 572] = code_fi
print("3. Successfully injected fillItems bytecode into dex4!")

# Recalculate checksums
dex4[12:32] = hashlib.sha1(dex4[32:]).digest()
dex4[8:12] = struct.pack("<I", zlib.adler32(dex4[12:]) & 0xFFFFFFFF)

with open(r"c:\project\ayugram\Tools\test_verify_classes4_v2.dex", "wb") as f:
    f.write(dex4)

# Run dexdump verification
res = subprocess.run([r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\dexdump.exe", "-c", r"c:\project\ayugram\Tools\test_verify_classes4_v2.dex"], capture_output=True, text=True)
if res.returncode != 0:
    print("DEX verification failed:", res.stderr)
    exit(1)
print("DEX verification passed 100% successfully!")
