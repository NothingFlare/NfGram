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

# -*- coding: utf-8 -*-
import sys

with open(r"c:\project\ayugram\Tools\build_nfgram_faceunlock.py", "r", encoding="utf-8") as f:
    code = f.read()

# --------------------------------------------------------------------------
# 1. Update classes4.dex patch
# --------------------------------------------------------------------------
old_dex4_block = """# -------------------------------------------------------------
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
print("Applied MainPreferencesActivity unified AyuGram settings patch in classes4.dex")"""

new_dex4_block = """# -------------------------------------------------------------
# 1.1 Patch classes4.dex: Unify Settings into NfGram (AyuGram & exteraGram)
# -------------------------------------------------------------
# 1. HeaderSettingsCell.<init>: Display "NfGram" via LocaleController.getString(0x7f0f0000)
start_hsc = 0x39c50c
patch_hsc = bytearray()
patch_hsc.extend(b"\\x15\\x03\\x0f\\x7f")         # const/high16 v3, 0x7f0f (R.string.AppName = 0x7f0f0000)
patch_hsc.extend(b"\\x71\\x10\\x80\\xf5\\x03\\x00") # invoke-static {v3}, LocaleController.getString:(I)Ljava/lang/String; (method@f580)
patch_hsc.extend(b"\\x0c\\x03")                 # move-result-object v3
patch_hsc.extend(b"\\x6e\\x20\\x38\\x09\\x32\\x00") # invoke-virtual {v2, v3}, TextView.setText:(Ljava/lang/CharSequence;)V (method@0938)
patch_hsc.extend(b"\\x6e\\x20\\x36\\x09\\x02\\x00") # invoke-virtual {v2, v0}, TextView.setSingleLine:(Z)V (method@0936)
patch_hsc.extend(b"\\x00\\x00\\x00\\x00")         # nop, nop
assert len(patch_hsc) == 28
dex4[start_hsc : start_hsc + 28] = patch_hsc
print("1. Patched HeaderSettingsCell title to NfGram in classes4.dex")

# 2. MainPreferencesActivity.onClick:
#    - Case 7 at 0x38a67e (14 bytes): Channel opener (lighthouse_top)
#    - Case 2 at 0x38a68c (26 bytes): Dispatcher for General / Submenu
#    - Case 8 at 0x38a6a6 (22 bytes): Opens AyuMainPreferencesActivity
#    - General at 0x38a706: Original (called by Case 2 when in submenu)
pos_case7 = 0x38a67e
patch_case7 = bytearray()
patch_case7.extend(b"\\x1a\\x01\\xbf\\xc0")         # const-string v1, "lighthouse_top" (string@c0bf)
patch_case7.extend(b"\\x70\\x20\\xc6\\x74\\x10\\x00") # invoke-direct {v0, v1}, showNoticeBeforeOpeningChat (method@74c6)
patch_case7.extend(b"\\x0e\\x00")                 # return-void
patch_case7.extend(b"\\x00\\x00")                 # nop
assert len(patch_case7) == 14
dex4[pos_case7 : pos_case7 + 14] = patch_case7

pos_case2 = 0x38a68c
patch_case2 = bytearray()
patch_case2.extend(b"\\x55\\x01\\xba\\x8e")         # iget-boolean v1, v0, BaseFragment.hasOwnBackground:Z (field@8eba)
delta_to_gen = (0x38a706 - (pos_case2 + 4)) // 2
patch_case2.extend(b"\\x39\\x01" + struct.pack("<h", delta_to_gen)) # if-nez v1, -> 0x38a706
patch_case2.extend(b"\\x22\\x01\\x9e\\x15")         # new-instance v1, MainPreferencesActivity (type@159e)
patch_case2.extend(b"\\x70\\x10\\xbe\\x74\\x01\\x00") # invoke-direct {v1}, MainPreferencesActivity.<init> (method@74be)
patch_case2.extend(b"\\x12\\x12")                 # const/4 v2, 1
patch_case2.extend(b"\\x5c\\x12\\xba\\x8e")         # iput-boolean v2, v1, BaseFragment.hasOwnBackground:Z (field@8eba)
delta_pres = (0x38a710 - (pos_case2 + 24)) // 2
patch_case2.extend(b"\\x28" + struct.pack("<b", delta_pres)) # goto -> 0x38a710
assert len(patch_case2) == 26
dex4[pos_case2 : pos_case2 + 26] = patch_case2

pos_case8 = 0x38a6a6
patch_case8 = bytearray()
patch_case8.extend(b"\\x1c\\x01\\x01\\x35")         # const-class v1, AyuMainPreferencesActivity (type@3501)
patch_case8.extend(b"\\x6e\\x10\\x01\\xee\\x01\\x00") # invoke-static {v1}, AyuFragmentUtils.getOrCreateInstance (method@ee01)
patch_case8.extend(b"\\x0c\\x01")                 # move-result-object v1
patch_case8.extend(b"\\x1f\\x01\\x58\\x39")         # check-cast v1, BaseFragment (type@3958)
patch_case8.extend(b"\\x6e\\x20\\x09\\xf8\\x10\\x00") # invoke-virtual {v0, v1}, BaseFragment.presentFragment (method@f809)
patch_case8.extend(b"\\x0e\\x00")                 # return-void
assert len(patch_case8) == 22
dex4[pos_case8 : pos_case8 + 22] = patch_case8

# Update switch table at 0x38a744
base_switch = 0x38a670
off_c2 = (pos_case2 - base_switch) // 2
dex4[0x38a74c + 1*4 : 0x38a74c + 2*4] = struct.pack("<i", off_c2)
off_c7 = (pos_case7 - base_switch) // 2
dex4[0x38a74c + 6*4 : 0x38a74c + 7*4] = struct.pack("<i", off_c7)
off_c8 = (pos_case8 - base_switch) // 2
dex4[0x38a74c + 7*4 : 0x38a74c + 8*4] = struct.pack("<i", off_c8)

# 3. MainPreferencesActivity.fillItems:
#    Build Root mode (2 items + 1 link) and Submenu mode (5 categories)
start_fi = 0x38a3d8
code_fi = bytearray()

# Prefix:
code_fi.extend(b"\\x08\\x00\\x11\\x00") # move-object/from16 v0, v17 (items ArrayList)
code_fi.extend(b"\\x08\\x01\\x10\\x00") # move-object/from16 v1, v16 (this MainPreferencesActivity)

# Add HEADER_CELL:
code_fi.extend(b"\\x54\\x12\\x90\\x3e") # iget-object v2, v1, headerSettingsCell (field@3e90)
code_fi.extend(b"\\x39\\x02\\x03\\x00") # if-nez v2, +3
code_fi.extend(b"\\x12\\x02")         # const/4 v2, 0
code_fi.extend(b"\\x13\\x03\\xc6\\x00") # const/16 v3, 198
code_fi.extend(b"\\x71\\x20\\xcd\\xfa\\x32\\x00") # invoke-static {v2, v3}, UItem.asCustomShadow (method@facd)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x62\\x03\\x8a\\x3e")         # sget-object v3, PreferenceItem.HEADER_CELL (field@3e8a)
code_fi.extend(b"\\x6e\\x10\\xba\\x74\\x03\\x00") # invoke-virtual {v3}, PreferenceItem.getId (method@74ba)
code_fi.extend(b"\\x0a\\x03")                 # move-result v3
code_fi.extend(b"\\x6e\\x20\\xe9\\xfa\\x32\\x00") # invoke-virtual {v2, v3}, UItem.setId (method@fae9)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Add Header: "Categories":
code_fi.extend(b"\\x60\\x02\\x50\\x8a")         # sget v2, R.string.Categories (field@8a50)
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x02\\x00") # invoke-static {v2}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x71\\x10\\xd1\\xfa\\x02\\x00") # invoke-static {v2}, UItem.asHeader (method@fad1)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Zero out common argument registers v5, v6, v7, v8, v10, v11, v12, v14
code_fi.extend(b"\\x12\\x05") # const/4 v5, 0
code_fi.extend(b"\\x12\\x06") # const/4 v6, 0
code_fi.extend(b"\\x12\\x07") # const/4 v7, 0
code_fi.extend(b"\\x12\\x08") # const/4 v8, 0
code_fi.extend(b"\\x12\\x0a") # const/4 v10, 0
code_fi.extend(b"\\x12\\x0b") # const/4 v11, 0
code_fi.extend(b"\\x12\\x0c") # const/4 v12, 0
code_fi.extend(b"\\x12\\x0e") # const/4 v14, 0
code_fi.extend(b"\\x13\\x0d\\x78\\x07") # const/16 v13, 1912 (default mask)

# Branch on hasOwnBackground
code_fi.extend(b"\\x55\\x12\\xba\\x8e") # iget-boolean v2, v1, BaseFragment.hasOwnBackground:Z (field@8eba)
branch_sub_ph = len(code_fi)
code_fi.extend(b"\\x39\\x02\\x00\\x00") # if-nez v2, -> :fill_submenu (placeholder)

# ---------------- ROOT MODE (hasOwnBackground == false) ----------------
# Item 1: AyuGram (FORUM)
code_fi.extend(b"\\x62\\x02\\x88\\x3e")         # sget-object v2, PreferenceItem.FORUM (field@3e88)
code_fi.extend(b"\\x1a\\x03\\x54\\x19")         # const-string v3, "AyuGram" (string@1954)
code_fi.extend(b"\\x60\\x04\\x09\\x89")         # sget v4, R.drawable.ayu_ghost (field@8909)
code_fi.extend(b"\\x1a\\x09\\x54\\x19")         # const-string v9, "AyuGram" (string@1954)
code_fi.extend(b"\\x77\\x0e\\x51\\x74\\x01\\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Item 2: exteraGram (GENERAL_CATEGORY)
code_fi.extend(b"\\x62\\x02\\x89\\x3e")         # sget-object v2, PreferenceItem.GENERAL_CATEGORY (field@3e89)
code_fi.extend(b"\\x1a\\x03\\xf7\\xa1")         # const-string v3, "exteraGram" (string@a1f7)
code_fi.extend(b"\\x60\\x04\\x20\\x89")         # sget v4, R.drawable.ic_foreground_extera (field@8920)
code_fi.extend(b"\\x1a\\x09\\xf7\\xa1")         # const-string v9, "exteraGram" (string@a1f7)
code_fi.extend(b"\\x77\\x0e\\x51\\x74\\x01\\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Header: "Links"
code_fi.extend(b"\\x60\\x02\\x2f\\x8b")         # sget v2, R.string.Links (field@8b2f)
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x02\\x00") # invoke-static {v2}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x71\\x10\\xd1\\xfa\\x02\\x00") # invoke-static {v2}, UItem.asHeader (method@fad1)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Item: Channel (CHANNEL)
code_fi.extend(b"\\x62\\x02\\x85\\x3e")         # sget-object v2, PreferenceItem.CHANNEL (field@3e85)
code_fi.extend(b"\\x60\\x03\\xc4\\x8b")         # sget v3, R.string.ProfileChannel (field@8bc4)
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x03\\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x03")                 # move-result-object v3
code_fi.extend(b"\\x60\\x04\\x4b\\x89")         # sget v4, R.drawable.msg_channel (field@894b)
code_fi.extend(b"\\x60\\x05\\x78\\x8a")         # sget v5, R.string.Crowdin (field@8a78 = "@lighthouse_top")
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x05\\x00") # invoke-static {v5}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x05")                 # move-result-object v5
code_fi.extend(b"\\x60\\x09\\x81\\x8c")         # sget v9, R.string.Website (field@8c81 = "lighthouse_top")
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x09\\x00") # invoke-static {v9}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x09")                 # move-result-object v9
code_fi.extend(b"\\x13\\x0d\\x70\\x07")         # const/16 v13, 1904 (mask with subtitle)
code_fi.extend(b"\\x77\\x0e\\x51\\x74\\x01\\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# End root mode: goto :finish_shadow
goto_finish_ph = len(code_fi)
code_fi.extend(b"\\x28\\x00") # goto -> :finish_shadow

# ---------------- SUBMENU MODE (hasOwnBackground == true) ----------------
pos_submenu = len(code_fi)
code_fi[branch_sub_ph + 2 : branch_sub_ph + 4] = struct.pack("<h", (pos_submenu - branch_sub_ph) // 2)

# Reset mask & subtitle
code_fi.extend(b"\\x12\\x05")         # const/4 v5, 0
code_fi.extend(b"\\x13\\x0d\\x78\\x07") # const/16 v13, 1912

# Submenu Category 1: General
code_fi.extend(b"\\x62\\x02\\x89\\x3e")         # sget-object v2, PreferenceItem.GENERAL_CATEGORY (field@3e89)
code_fi.extend(b"\\x60\\x03\\xed\\x8a")         # sget v3, R.string.General (field@8aed)
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x03\\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x03")                 # move-result-object v3
code_fi.extend(b"\\x60\\x04\\x6b\\x89")         # sget v4, R.drawable.msg_media (field@896b)
code_fi.extend(b"\\x1a\\x09\\xca\\xa5")         # const-string v9, "general" (string@a5ca)
code_fi.extend(b"\\x77\\x0e\\x51\\x74\\x01\\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Submenu Category 2: Appearance
code_fi.extend(b"\\x62\\x02\\x84\\x3e")         # sget-object v2, PreferenceItem.APPEARANCE_CATEGORY (field@3e84)
code_fi.extend(b"\\x60\\x03\\x23\\x8a")         # sget v3, R.string.Appearance (field@8a23)
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x03\\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x03")                 # move-result-object v3
code_fi.extend(b"\\x60\\x04\\x90\\x89")         # sget v4, R.drawable.msg_theme (field@8990)
code_fi.extend(b"\\x1a\\x09\\x30\\x8c")         # const-string v9, "appearance" (string@8c30)
code_fi.extend(b"\\x77\\x0e\\x51\\x74\\x01\\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Submenu Category 3: Chats
code_fi.extend(b"\\x62\\x02\\x86\\x3e")         # sget-object v2, PreferenceItem.CHATS_CATEGORY (field@3e86)
code_fi.extend(b"\\x60\\x03\\xf7\\x8b")         # sget v3, R.string.SearchAllChatsShort (field@8bf7)
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x03\\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x03")                 # move-result-object v3
code_fi.extend(b"\\x60\\x04\\x54\\x89")         # sget v4, R.drawable.msg_discussion (field@8954)
code_fi.extend(b"\\x1a\\x09\\xaa\\x96")         # const-string v9, "chats" (string@96aa)
code_fi.extend(b"\\x77\\x0e\\x51\\x74\\x01\\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Submenu Category 4: Plugins
code_fi.extend(b"\\x62\\x02\\x8c\\x3e")         # sget-object v2, PreferenceItem.PLUGINS_CATEGORY (field@3e8c)
code_fi.extend(b"\\x60\\x03\\x9b\\x8b")         # sget v3, R.string.Plugins (field@8b9b)
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x03\\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x03")                 # move-result-object v3
code_fi.extend(b"\\x60\\x04\\x78\\x89")         # sget v4, R.drawable.msg_openwith (field@8978)
code_fi.extend(b"\\x1a\\x09\\x2c\\xc6")         # const-string v9, "plugins" (string@c62c)
code_fi.extend(b"\\x77\\x0e\\x51\\x74\\x01\\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Submenu Category 5: Other
code_fi.extend(b"\\x62\\x02\\x8b\\x3e")         # sget-object v2, PreferenceItem.OTHER_CATEGORY (field@3e8b)
code_fi.extend(b"\\x60\\x03\\x34\\x8b")         # sget v3, R.string.LocalOther (field@8b34)
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x03\\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x03")                 # move-result-object v3
code_fi.extend(b"\\x60\\x04\\x58\\x89")         # sget v4, R.drawable.msg_settings (field@8958)
code_fi.extend(b"\\x1a\\x09\\x04\\xc2")         # const-string v9, "other" (string@c204)
code_fi.extend(b"\\x77\\x0e\\x51\\x74\\x01\\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# :finish_shadow
pos_finish = len(code_fi)
code_fi[goto_finish_ph + 1] = (pos_finish - goto_finish_ph) // 2
code_fi.extend(b"\\x71\\x00\\xd8\\xfa\\x00\\x00") # invoke-static {}, UItem.asShadow (method@fad8)
code_fi.extend(b"\\x0c\\x01")                 # move-result-object v1
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x10\\x00") # invoke-virtual {v0, v1}, ArrayList.add (method@f055)
code_fi.extend(b"\\x0e\\x00")                 # return-void

assert len(code_fi) <= 572
while len(code_fi) < 572:
    code_fi.extend(b"\\x00\\x00")
assert len(code_fi) == 572

dex4[start_fi : start_fi + 572] = code_fi
print("Patched MainPreferencesActivity (Root 2-item categories + single lighthouse_top link, Submenu 5 categories) in classes4.dex")

dex4[12:32] = hashlib.sha1(dex4[32:]).digest()
dex4[8:12] = struct.pack("<I", zlib.adler32(dex4[12:]) & 0xFFFFFFFF)"""

# Normalize CRLF vs LF
code_norm = code.replace("\r\n", "\n")
old_dex4_norm = old_dex4_block.replace("\r\n", "\n")
assert old_dex4_norm in code_norm, "old_dex4_block not found in code!"
code_norm = code_norm.replace(old_dex4_norm, new_dex4_block)

# --------------------------------------------------------------------------
# 2. Update replacements in resources.arsc
# --------------------------------------------------------------------------
old_rep_block = """replacements = {
    8559: "NfGram",
    8560: "NfGram Alt",
    9497: "NfGram",
    9593: "Update NfGram",
    9635: "Welcome to the NfGram Desktop. Make Telegram your own."
}"""

new_rep_block = """replacements = {
    8559: "NfGram",
    8560: "NfGram Alt",
    9497: "NfGram",
    9554: "@lighthouse_top",
    9593: "Update NfGram",
    9634: "lighthouse_top",
    9635: "Welcome to the NfGram Desktop. Make Telegram your own."
}"""

old_rep_norm = old_rep_block.replace("\r\n", "\n")
assert old_rep_norm in code_norm, "old_rep_block not found in code!"
code_norm = code_norm.replace(old_rep_norm, new_rep_block)

# --------------------------------------------------------------------------
# 3. Update STEP 5: Patch Locales
# --------------------------------------------------------------------------
old_step5_block = """print("=== STEP 5: Patch Locales (Face Unlock strings) ===")
xml_replacements = {}
with zipfile.ZipFile(VANILLA_APK, "r") as zin:
    for xml_path, string_val in [
        ("assets/ayu_locales/values-ru/ayu.xml", "\\u0420\\u0430\\u0437\\u0431\\u043b\\u043e\\u043a\\u0438\\u0440\\u043e\\u0432\\u043a\\u0430 \\u043b\\u0438\\u0446\\u043e\\u043c"),
        ("assets/extera_locales/values-ru/extera.xml", "\\u0420\\u0430\\u0437\\u0431\\u043b\\u043e\\u043a\\u0438\\u0440\\u043e\\u0432\\u043a\\u0430 \\u043b\\u0438\\u0446\\u043e\\u043c"),
        ("assets/ayu_locales/values/ayu.xml", "Face Unlock"),
        ("assets/extera_locales/values/extera.xml", "Face Unlock"),
    ]:
        xml_text = zin.read(xml_path).decode("utf-8")
        insert_line = f'  <string name="camera">{string_val}</string>\\n</resources>'
        new_xml_text = xml_text.replace("</resources>", insert_line)
        # Verify valid XML
        ET.fromstring(new_xml_text)
        xml_replacements[xml_path] = new_xml_text.encode("utf-8")
        print(f"Patched locale XML: {xml_path}")"""

new_step5_block = """print("=== STEP 5: Patch Locales (Face Unlock & NfGram Preferences strings) ===")
xml_replacements = {}
with zipfile.ZipFile(VANILLA_APK, "r") as zin:
    for item in zin.infolist():
        if item.filename.startswith("assets/extera_locales/") and item.filename.endswith("extera.xml"):
            xml_text = zin.read(item.filename).decode("utf-8")
            # Rename exteraGram to NfGram across all extera locales (Preferences -> Настройки NfGram / NfGram Preferences)
            new_xml = xml_text.replace("exteraGram", "NfGram").replace("ExteraGram", "NfGram")
            xml_replacements[item.filename] = new_xml

    camera_strings = {
        "assets/ayu_locales/values-ru/ayu.xml": "\\u0420\\u0430\\u0437\\u0431\\u043b\\u043e\\u043a\\u0438\\u0440\\u043e\\u0432\\u043a\\u0430 \\u043b\\u0438\\u0446\\u043e\\u043c",
        "assets/extera_locales/values-ru/extera.xml": "\\u0420\\u0430\\u0437\\u0431\\u043b\\u043e\\u043a\\u0438\\u0440\\u043e\\u0432\\u043a\\u0430 \\u043b\\u0438\\u0446\\u043e\\u043c",
        "assets/ayu_locales/values/ayu.xml": "Face Unlock",
        "assets/extera_locales/values/extera.xml": "Face Unlock",
    }
    for xml_path, string_val in camera_strings.items():
        if xml_path in xml_replacements:
            base_text = xml_replacements[xml_path]
        else:
            base_text = zin.read(xml_path).decode("utf-8")
        insert_line = f'  <string name="camera">{string_val}</string>\\n</resources>'
        new_text = base_text.replace("</resources>", insert_line)
        ET.fromstring(new_text)
        xml_replacements[xml_path] = new_text

    for k in list(xml_replacements.keys()):
        xml_replacements[k] = xml_replacements[k].encode("utf-8")
        print(f"Patched locale XML: {k}")"""

old_step5_norm = old_step5_block.replace("\r\n", "\n")
assert old_step5_norm in code_norm, "old_step5_block not found in code!"
code_norm = code_norm.replace(old_step5_norm, new_step5_block)

with open(r"c:\project\ayugram\Tools\build_nfgram_faceunlock.py", "w", encoding="utf-8", newline="\r\n") as f:
    f.write(code_norm)

print("build_nfgram_faceunlock.py successfully updated!")
