"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

import re
import struct

new_onclick_and_fillitems = """# 2. MainPreferencesActivity.onClick:
#    - Case 7 at 0x38a67e (20 bytes): Channel opener (lighthouse_top via showNoticeBeforeOpeningChat)
#    - Case 8 at 0x38a692 (18 bytes): Opens AyuMainPreferencesActivity
#    - Case 2 at 0x38a6a4 (26 bytes): Dispatcher for General / Submenu
#    - General at 0x38a706: Original (called by Case 2 when in submenu)
pos_case7 = 0x38a67e
patch_case7 = bytearray()
patch_case7.extend(b"\\x60\\x01\\x81\\x8c")         # sget v1, R.string.Website (field@8c81 = "lighthouse_top")
patch_case7.extend(b"\\x71\\x10\\x80\\xf5\\x01\\x00") # invoke-static {v1}, LocaleController.getString (method@f580)
patch_case7.extend(b"\\x0c\\x01")                 # move-result-object v1
patch_case7.extend(b"\\x70\\x20\\xc6\\x74\\x10\\x00") # invoke-direct {v0, v1}, showNoticeBeforeOpeningChat (method@74c6)
patch_case7.extend(b"\\x0e\\x00")                 # return-void
assert len(patch_case7) == 20
dex4[pos_case7 : pos_case7 + 20] = patch_case7

pos_case8 = 0x38a692
patch_case8 = bytearray()
patch_case8.extend(b"\\x1c\\x01\\x01\\x35")         # const-class v1, AyuMainPreferencesActivity (type@3501)
patch_case8.extend(b"\\x6e\\x10\\x01\\xee\\x01\\x00") # invoke-static {v1}, AyuFragmentUtils.getOrCreateInstance (method@ee01)
patch_case8.extend(b"\\x0c\\x01")                 # move-result-object v1
patch_case8.extend(b"\\x1f\\x01\\x58\\x39")         # check-cast v1, BaseFragment (type@3958)
delta_pres8 = (0x38a710 - (pos_case8 + 16)) // 2
patch_case8.extend(b"\\x28" + struct.pack("<b", delta_pres8)) # goto -> 0x38a710
assert len(patch_case8) == 18
dex4[pos_case8 : pos_case8 + 18] = patch_case8

pos_case2 = 0x38a6a4
patch_case2 = bytearray()
patch_case2.extend(b"\\x55\\x01\\xba\\x8e")         # iget-boolean v1, v0, BaseFragment.hasOwnBackground:Z (field@8eba)
delta_to_gen = (0x38a706 - (pos_case2 + 4)) // 2
patch_case2.extend(b"\\x39\\x01" + struct.pack("<h", delta_to_gen)) # if-nez v1, -> 0x38a706
patch_case2.extend(b"\\x22\\x01\\x9e\\x15")         # new-instance v1, MainPreferencesActivity (type@159e)
patch_case2.extend(b"\\x70\\x10\\xbe\\x74\\x01\\x00") # invoke-direct {v1}, MainPreferencesActivity.<init> (method@74be)
patch_case2.extend(b"\\x12\\x12")                 # const/4 v2, 1
patch_case2.extend(b"\\x5c\\x12\\xba\\x8e")         # iput-boolean v2, v1, BaseFragment.hasOwnBackground:Z (field@8eba)
delta_pres2 = (0x38a710 - (pos_case2 + 24)) // 2
patch_case2.extend(b"\\x28" + struct.pack("<b", delta_pres2)) # goto -> 0x38a710
assert len(patch_case2) == 26
dex4[pos_case2 : pos_case2 + 26] = patch_case2

# Fill remaining bytes between 0x38a6be and 0x38a706 with NOPs
dex4[0x38a6be : 0x38a706] = b"\\x00\\x00" * 36

# Update switch table at 0x38a744
base_switch = 0x38a670
off_c2 = (pos_case2 - base_switch) // 2
dex4[0x38a74c + 1*4 : 0x38a74c + 2*4] = struct.pack("<i", off_c2)
off_c7 = (pos_case7 - base_switch) // 2
dex4[0x38a74c + 6*4 : 0x38a74c + 7*4] = struct.pack("<i", off_c7)
off_c8 = (pos_case8 - base_switch) // 2
dex4[0x38a74c + 7*4 : 0x38a74c + 8*4] = struct.pack("<i", off_c8)
# Index 8 & 9 (Crowdin & Website - point to pos_case7)
dex4[0x38a74c + 8*4 : 0x38a74c + 9*4] = struct.pack("<i", off_c7)
dex4[0x38a74c + 9*4 : 0x38a74c + 10*4] = struct.pack("<i", off_c7)

# 3. MainPreferencesActivity.fillItems:
#    Build Root mode (2 items + card shadow + 1 channel link + card shadow) and Submenu mode (5 categories)
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
# Item 1: exteraGram (GENERAL_CATEGORY, 0x7f080326 ic_foreground_solid, red #ffe83030 squircle, title SupportDevelopment = "Настройки exteraGram")
code_fi.extend(b"\\x62\\x02\\x89\\x3e")         # sget-object v2, PreferenceItem.GENERAL_CATEGORY (field@3e89)
code_fi.extend(b"\\x14\\x03\\xc0\\xd2\\x0f\\x7f") # const v3, 0x7f0fd2c0 (SupportDevelopment)
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x03\\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x03")                 # move-result-object v3
code_fi.extend(b"\\x14\\x04\\x26\\x03\\x08\\x7f") # const v4, 0x7f080326 (ic_foreground_solid)
code_fi.extend(b"\\x1a\\x09\\xca\\xa5")         # const-string v9, "general" (string@a5ca)
code_fi.extend(b"\\x77\\x0e\\x51\\x74\\x01\\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x14\\x03\\x30\\x30\\xe8\\xff") # const v3, 0xffe83030 (Red squircle color)
code_fi.extend(b"\\x6e\\x30\\xe6\\xfa\\x42\\x03") # invoke-virtual {v2, v4, v3}, UItem.setColorfulIcon (method@fae6)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Item 2: AyuGram (FORUM, 0x7f080327 ic_foreground_solid_ayu, purple #ff9570ff squircle, title AyuPreferences = "Настройки AyuGram")
code_fi.extend(b"\\x62\\x02\\x88\\x3e")         # sget-object v2, PreferenceItem.FORUM (field@3e88)
code_fi.extend(b"\\x14\\x03\\xa3\\xfa\\x0f\\x7f") # const v3, 0x7f0ffaa3 (AyuPreferences)
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x03\\x00") # invoke-static {v3}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x03")                 # move-result-object v3
code_fi.extend(b"\\x14\\x04\\x27\\x03\\x08\\x7f") # const v4, 0x7f080327 (ic_foreground_solid_ayu)
code_fi.extend(b"\\x1a\\x09\\x54\\x19")         # const-string v9, "AyuGram" (string@1954)
code_fi.extend(b"\\x77\\x0e\\x51\\x74\\x01\\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x14\\x03\\xff\\x70\\x95\\xff") # const v3, 0xff9570ff (Purple squircle color)
code_fi.extend(b"\\x6e\\x30\\xe6\\xfa\\x42\\x03") # invoke-virtual {v2, v4, v3}, UItem.setColorfulIcon (method@fae6)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Card 1 Closer (Categories shadow):
code_fi.extend(b"\\x71\\x00\\xd8\\xfa\\x00\\x00") # invoke-static {}, UItem.asShadow (method@fad8)
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
code_fi.extend(b"\\x60\\x05\\x71\\x8a")         # sget v5, R.string.Crowdin (field@8a71 = "@lighthouse_top")
code_fi.extend(b"\\x71\\x10\\x80\\xf5\\x05\\x00") # invoke-static {v5}, LocaleController.getString (method@f580)
code_fi.extend(b"\\x0c\\x05")                 # move-result-object v5
code_fi.extend(b"\\x1a\\x09\\xd1\\x93")         # const-string v9, "channel" (string@93d1)
code_fi.extend(b"\\x13\\x0d\\x70\\x07")         # const/16 v13, 1904 (mask with subtitle)
code_fi.extend(b"\\x77\\x0e\\x51\\x74\\x01\\x00") # invoke-static/range {v1..v14}, uButton (method@7451)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)

# Card 2 Closer (Links shadow):
code_fi.extend(b"\\x71\\x00\\xd8\\xfa\\x00\\x00") # invoke-static {}, UItem.asShadow (method@fad8)
code_fi.extend(b"\\x0c\\x02")                 # move-result-object v2
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x20\\x00") # invoke-virtual {v0, v2}, ArrayList.add (method@f055)
code_fi.extend(b"\\x0e\\x00")                 # return-void

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

# Submenu shadow & return:
code_fi.extend(b"\\x71\\x00\\xd8\\xfa\\x00\\x00") # invoke-static {}, UItem.asShadow (method@fad8)
code_fi.extend(b"\\x0c\\x01")                 # move-result-object v1
code_fi.extend(b"\\x6e\\x20\\x55\\xf0\\x10\\x00") # invoke-virtual {v0, v1}, ArrayList.add (method@f055)
code_fi.extend(b"\\x0e\\x00")                 # return-void

assert len(code_fi) <= 572
while len(code_fi) < 572:
    code_fi.extend(b"\\x00\\x00")
assert len(code_fi) == 572

dex4[start_fi : start_fi + 572] = code_fi
print("Patched MainPreferencesActivity (Root 2-item categories + single lighthouse_top link, Submenu 5 categories) in classes4.dex")"""

new_replacements = """replacements = {
    8559: "NfGram",
    8560: "NfGram Alt",
    9464: "exteraGram Preferences",
    9497: "NfGram",
    9554: "@lighthouse_top",
    9593: "Update NfGram",
    9634: "lighthouse_top",
    9635: "Welcome to the NfGram Desktop. Make Telegram your own.",
    9720: "NfGram Preferences",
}"""

new_locales = """print("=== STEP 5: Patch Locales (Face Unlock & NfGram Preferences strings) ===")
import re

def patch_string_tag(xml, name, new_val):
    pattern = rf'(<string name="{name}">)(.*?)(</string>)'
    if re.search(pattern, xml):
        return re.sub(pattern, rf'\\g<1>{new_val}\\g<3>', xml)
    else:
        return xml.replace('</resources>', f'  <string name="{name}">{new_val}</string>\\n</resources>')

xml_replacements = {}
with zipfile.ZipFile(VANILLA_APK, "r") as zin:
    for item in zin.infolist():
        if item.filename.startswith("assets/extera_locales/") and item.filename.endswith("extera.xml"):
            xml_text = zin.read(item.filename).decode("utf-8")
            is_ru = "values-ru" in item.filename
            new_xml = xml_text.replace("exteraGram", "NfGram").replace("ExteraGram", "NfGram")
            new_xml = patch_string_tag(new_xml, "Preferences", "\\u041d\\u0430\\u0441\\u0442\\u0440\\u043e\\u0439\\u043a\\u0438 NfGram" if is_ru else "NfGram Preferences")
            new_xml = patch_string_tag(new_xml, "SupportDevelopment", "\\u041d\\u0430\\u0441\\u0442\\u0440\\u043e\\u0439\\u043a\\u0438 exteraGram" if is_ru else "exteraGram Preferences")
            new_xml = patch_string_tag(new_xml, "Crowdin", "@lighthouse_top")
            new_xml = patch_string_tag(new_xml, "Website", "lighthouse_top")
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

file_path = r"c:\project\ayugram\Tools\build_nfgram_faceunlock.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace block 1
target_block1 = content[content.find("# 2. MainPreferencesActivity.onClick:") : content.find("dex4[12:32] = hashlib.sha1(dex4[32:]).digest()")]
assert target_block1, "Could not find block 1"
content = content.replace(target_block1, new_onclick_and_fillitems + "\n\n")

# Replace block 2 (replacements)
target_block2 = content[content.find("replacements = {") : content.find("for idx, rep in replacements.items():")]
assert target_block2, "Could not find block 2"
content = content.replace(target_block2, new_replacements + "\n\n")

# Replace block 3 (locales)
target_block3 = content[content.find('print("=== STEP 5: Patch Locales') : content.find('print("=== STEP 6: Repack APK ===")')]
assert target_block3, "Could not find block 3"
content = content.replace(target_block3, new_locales + "\n\n")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated build_nfgram_faceunlock.py with colorful squircle icons successfully!")
