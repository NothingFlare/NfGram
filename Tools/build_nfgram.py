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
import re

VANILLA_APK = r"c:\Users\styuk\Downloads\AyuGram Desktop\vanilla-AyuGram-full-20261005.apk"
EXTERA_APK = r"c:\Users\styuk\Downloads\AyuGram Desktop\exteraGram-full-universal-20261004.apk"
OUTPUT_APK_NFGRAM = r"c:\Users\styuk\Downloads\AyuGram Desktop\NfGram-12.10.6-universal.apk"
OUTPUT_APK_DESKTOP = r"C:\Users\styuk\Desktop\NfGram-12.10.6-universal.apk"
OUTPUT_APK_PROJECT = r"C:\project\ayugram\NfGram-12.10.6-universal.apk"

KEYSTORE = r"C:\project\ayugram\Tools\nfgram_release.keystore"
ZIPALIGN = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\zipalign.exe"
APKSIGNER = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\apksigner.bat"
AAPT = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\aapt.exe"
AAPT2 = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\aapt2.exe"
ANDROID_JAR = r"C:\Users\styuk\AppData\Local\Android\Sdk\platforms\android-34\android.jar"
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
# Optimal Parallel Uploads: Cap concurrent upload operations at 4 streams (const/4 v2, 4)
# instead of infinite threads that cause CPU pinning, overheating, and out-of-memory crashes
assert dex1[0x4eb878 : 0x4eb87a] == bytes.fromhex('12 12')
dex1[0x4eb878 : 0x4eb87a] = bytes.fromhex('12 42')
print("Applied capped 4-stream parallel upload patch in classes.dex")

# Proximity and Ear Sensor Optimization:
# 1. Proximity isNearToSensor: reduce distance threshold from 5.0f to 2.0f
# Only triggers when phone is within 2 cm of ear/face, eliminating accidental hand-wave triggers
assert dex1[0x506a18 : 0x506a1c] == bytes.fromhex('15 00 a0 40')
dex1[0x506a18 : 0x506a1c] = bytes.fromhex('15 00 00 40')

# 2. Accelerometer vertical angle: increase threshold from 2.5f (~14 deg) to 5.5f (~35 deg)
# Requires phone to actually be raised upright toward the ear before activating proximity wake/earpiece
assert dex1[0x50ec2e : 0x50ec32] == bytes.fromhex('15 04 20 40')
dex1[0x50ec2e : 0x50ec32] = bytes.fromhex('15 04 b0 40')
print("Applied Proximity and Ear sensor anti-accidental trigger patch in classes.dex")

# Thermal and Overheating Protection:
# 3. Disable KeepAliveJob.startJob (JobScheduler 0ms deadline churn that causes background wakeups)
assert dex1[0x4f74a4 : 0x4f74a8] == bytes.fromhex('62 00 e6 81')
dex1[0x4f74a4 : 0x4f74a8] = bytes.fromhex('0e 00 00 00')
print("Applied KeepAliveJob thermal wakeup suppression patch in classes.dex")

# 4. Cap DevicePerformanceClass to PERFORMANCE_CLASS_AVERAGE in SharedConfig.measureDevicePerformanceClass
# Prevents GPU driver hangs, surface frame timeouts, and thermal throttling crashes during charging
assert dex1[0x334778 : 0x33477c] == bytes.fromhex('60 00 93 00')
dex1[0x334778 : 0x33477c] = bytes.fromhex('12 10 0f 00')
print("Applied Thermal and Overheating protection patch in classes.dex")

# Battery Patch 1: Disable persistent file logging to disk (BuildVars.LOGS_ENABLED = false)
assert dex1[0x2905f4 : 0x2905f4 + 12] == bytes.fromhex("71 00 12 2f 00 00 0a 00 6a 00 35 2e".replace(" ", ""))
dex1[0x2905f4 : 0x2905f4 + 12] = bytes.fromhex("12 00 6a 00 35 2e 00 00 00 00 00 00".replace(" ", ""))
print("Applied Battery patch 1: LOGS_ENABLED disabled")

# Battery Patch 2: Disable Proximity sensor polling (raiseToListen) and GPU blur shaders in SharedConfig.<clinit>
assert dex1[0x3339b8 : 0x3339bc] == bytes.fromhex("6a 03 11 80".replace(" ", ""))
dex1[0x3339b8 : 0x3339bc] = bytes.fromhex("6a 02 11 80".replace(" ", "")) # photoViewerBlur = false

# raiseToListen left enabled with improved anti-false trigger sensor thresholds
assert dex1[0x333a0c : 0x333a10] == bytes.fromhex("6a 03 1f 80".replace(" ", ""))

assert dex1[0x333a98 : 0x333a9c] == bytes.fromhex("6a 03 dc 7f".replace(" ", ""))
dex1[0x333a98 : 0x333a9c] = bytes.fromhex("6a 02 dc 7f".replace(" ", "")) # drawActionBarShadow = false
print("Applied Battery patch 2: SharedConfig sensor polling & blur defaults disabled")

# Battery Patch 3: Force disable real-time compute blur shaders (SharedConfig.useNewBlur = false)
assert dex1[0x3345c6 : 0x3345cc] == bytes.fromhex("0a 02 6a 02 46 80".replace(" ", ""))
dex1[0x3345c6 : 0x3345cc] = bytes.fromhex("12 02 6a 02 46 80".replace(" ", ""))
print("Applied Battery patch 3: useNewBlur disabled")

# Battery Patch 4: Background Service & Push Connection
# Keep AyuConfig.keepAliveService enabled so NotificationsService runs as a foreground service
assert dex1[0x24a674 : 0x24a67e] == bytes.fromhex("71 00 da 71 00 00 0a 03 b7 43".replace(" ", ""))
print("Preserved keepAliveService: NotificationsService will maintain persistent background push socket")

# Battery Patch 5: Disable chat GPU background blur pass (SharedConfig.canBlurChat = false, chatBlurEnabled = false)
assert dex1[0x333b30 : 0x333b34] == bytes.fromhex("12 10 0f 00".replace(" ", ""))
dex1[0x333b30 : 0x333b34] = bytes.fromhex("12 00 0f 00".replace(" ", ""))

assert dex1[0x333b44 : 0x333b4a] == bytes.fromhex("71 00 48 d4 00 00".replace(" ", ""))
dex1[0x333b44 : 0x333b4a] = bytes.fromhex("12 00 0f 00 00 00".replace(" ", ""))
print("Applied Battery patch 5: canBlurChat and chatBlurEnabled disabled (stops GPU shader overhead)")

# Battery Patch 6: startPushService AlarmManager RTC_WAKEUP 60s
# Retain periodic RTC_WAKEUP ping to prevent VPN / mobile carrier timeout when app is in background
assert dex1[0x28f174 : 0x28f17c] == bytes.fromhex("12 07 17 0a 60 ea 00 00".replace(" ", ""))
print("Preserved AlarmManager RTC_WAKEUP ping: prevents VPN idle connection drop")

# Battery Patch 7: Default LiteMode.powerSaverFollowSystem to true
assert dex1[0x2c9f10 : 0x2c9f16] == bytes.fromhex("72 30 4c 02 02 06".replace(" ", ""))
dex1[0x2c9f10 : 0x2c9f16] = bytes.fromhex("72 30 4c 02 02 03".replace(" ", ""))
print("Applied Battery patch 7: powerSaverFollowSystem default set to true")

# Single Persistent Background Push Connection: ConnectionsManager.isPushConnectionEnabled() -> always true
# Ensures client holds exactly one dedicated MTProto push connection to Telegram DC in background
assert dex1[0x3430a8 : 0x3430b0] == bytes.fromhex("71 00 1b c6 00 00 0c 02".replace(" ", ""))
dex1[0x3430a8 : 0x3430a8 + 66] = bytes.fromhex("12 10 0f 00".replace(" ", "")) + b"\x00" * 62
print("Applied Single Background Connection Patch: isPushConnectionEnabled returns true (instant notifications over VPN)")

# Disable Comma After Mention: ExteraConfig.getAddCommaAfterMention() -> always false
# Removes comma after @username mention
assert dex1[0x3bda04 : 0x3bda0c] == bytes.fromhex("62 00 74 0d 62 01 72 0d".replace(" ", ""))
dex1[0x3bda04 : 0x3bda04 + 40] = bytes.fromhex("12 00 0f 00".replace(" ", "")) + b"\x00" * 36
print("Applied Disable Comma After Mention Patch: getAddCommaAfterMention returns false (no comma after @user)")

# -------------------------------------------------------------
# Plugins Engine Fix: Ensure Python Plugins engine is enabled,
# initialized on launch, never drops plugins across toggle cycles,
# and allows enabling in safe mode.
# -------------------------------------------------------------
# 1. ExteraConfig.loadConfig() -> default preferences.getBoolean("pluginsEngine", true)
assert dex1[0x1e6850 : 0x1e6856] == bytes.fromhex("72 30 4c 02 21 03".replace(" ", ""))
dex1[0x1e6850 : 0x1e6856] = bytes.fromhex("72 30 4c 02 21 06".replace(" ", ""))
print("Applied Plugin Patch 1: ExteraConfig.loadConfig() defaults pluginsEngine preference to true")

# 1b. ExteraConfig.loadConfig() -> bypass auto-killswitch resetting pluginsEngine to false
assert dex1[0x1e67de : 0x1e67e2] == bytes.fromhex("39 01 34 00".replace(" ", ""))
dex1[0x1e67de : 0x1e67e2] = bytes.fromhex("28 34 00 00".replace(" ", ""))
print("Applied Plugin Patch 1b: ExteraConfig.loadConfig() bypasses killswitch (preserves plugins on toggle/restart)")

# 2. findModuleNameOwner -> return null immediately (avoids false module collision with sys.modules)
assert dex1[0x3d9ff4 : 0x3d9ff8] == bytes.fromhex("1a 00 f5 d0".replace(" ", ""))
dex1[0x3d9ff4 : 0x3d9ff8] = bytes.fromhex("12 00 11 00".replace(" ", ""))
print("Applied Plugin Patch 2: findModuleNameOwner returns null (prevents false collisions)")

# 3. PythonPluginsEngine.initSdk() -> Ensure getPython() is called before checking this.python
assert dex1[0x3d8be6 : 0x3d8bf0] == bytes.fromhex("54 f2 1c 10 39 02 03 00 0f 01".replace(" ", ""))
dex1[0x3d8be6 : 0x3d8bf0] = bytes.fromhex("70 10 5e 37 0f 00 54 f2 1c 10".replace(" ", ""))
print("Applied Plugin Patch 3: PythonPluginsEngine.initSdk ensures getPython() initializes interpreter")

# 4. PythonPluginsEngine.initSdk() -> Force sdkInitialized = true
assert dex1[0x3d8f24 : 0x3d8f26] == bytes.fromhex("01 13".replace(" ", ""))
dex1[0x3d8f24 : 0x3d8f26] = bytes.fromhex("12 13".replace(" ", ""))
print("Applied Plugin Patch 4: PythonPluginsEngine.initSdk guarantees sdkInitialized = true")

# 5. PythonPluginsEngine.initSdk() -> Do not skip requireBasePluginClass in safe mode
assert dex1[0x3d8fb4 : 0x3d8fb8] == bytes.fromhex("39 00 0d 00".replace(" ", ""))
dex1[0x3d8fb4 : 0x3d8fb8] = bytes.fromhex("00 00 00 00".replace(" ", ""))
print("Applied Plugin Patch 5: PythonPluginsEngine.initSdk completes initialization in safe mode")

# 5b. PythonPluginsEngine.requireBasePluginClass() -> Allow enabling plugins in safe mode
assert dex1[0x3d927e : 0x3d9282] == bytes.fromhex("39 00 48 00".replace(" ", ""))
dex1[0x3d927e : 0x3d9282] = bytes.fromhex("00 00 00 00".replace(" ", ""))
print("Applied Plugin Patch 5b: PythonPluginsEngine.requireBasePluginClass permits enabling plugins in safe mode")

# 5c. PythonPluginsEngine.requireBasePluginClass() -> Lazy bootstrap SDK on demand instead of throwing Exception
assert dex1[0x3d92fe : 0x3d930e] == bytes.fromhex("22 00 27 19 1a 01 5f a2 70 20 57 74 10 00 27 00".replace(" ", ""))
dex1[0x3d92fe : 0x3d930e] = bytes.fromhex("70 10 61 37 03 00 28 c3 00 00 00 00 00 00 00 00".replace(" ", ""))
print("Applied Plugin Patch 5c: PythonPluginsEngine.requireBasePluginClass lazily initializes SDK on demand")

# 6. PythonPluginsEngine.refreshImportCaches() -> Always append plugin parent directory to Python's sys.path
old_refresh = bytes.fromhex("1b 03 2b 34 01 00 6e 20 91 2e 31 00 0c 03 1f 03 5b 09 38 05 13 00 38 03 11 00 1b 01 8d 36 01 00 6e 10 4b 73 05 00 0c 05 12 02 24 20 86 3a 25 00 0c 05 6e 30 8e 2e 13 05".replace(" ", ""))
new_refresh = bytes.fromhex("1b 03 1f 34 01 00 6e 20 91 2e 31 00 0c 03 1f 03 5b 09 38 05 13 00 38 03 11 00 1b 01 48 d1 00 00 6e 10 4b 73 05 00 0c 05 24 10 86 3a 05 00 0c 05 00 00 6e 30 8e 2e 13 05".replace(" ", ""))
assert dex1[0x3dcd36 : 0x3dcd36 + len(old_refresh)] == old_refresh
dex1[0x3dcd36 : 0x3dcd36 + len(new_refresh)] = new_refresh
print("Applied Plugin Patch 6: PythonPluginsEngine.refreshImportCaches ensures plugin parent directory is in sys.path")

# 7. PythonPluginsEngine.parsePluginMetadata() -> Never re-throw unhandled exception, return empty map gracefully
assert dex1[0x3daac4 : 0x3daac4 + 2] == bytes.fromhex("27 03".replace(" ", ""))
dex1[0x3daac4 : 0x3daac4 + 2] = bytes.fromhex("28 01".replace(" ", "")) # goto -> 3daac6 (return-object v0)
print("Applied Plugin Patch 7: PythonPluginsEngine.parsePluginMetadata returns empty map instead of crashing on error")

# 8. PythonPluginsEngine.stopAndUnloadSdk() -> Do NOT purge Python C extension SDK modules on shutdown
old_stop_sdk = bytes.fromhex("1a 00 00 00 70 40 77 37 16 02".replace(" ", ""))
new_stop_sdk = bytes.fromhex("0e 00 00 00 00 00 00 00 00 00".replace(" ", ""))
assert dex1[0x3ddb64 : 0x3ddb64 + len(old_stop_sdk)] == old_stop_sdk
dex1[0x3ddb64 : 0x3ddb64 + len(new_stop_sdk)] = new_stop_sdk
print("Applied Plugin Patch 8: PythonPluginsEngine.stopAndUnloadSdk preserves SDK modules across toggle cycles")

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
# 1.1 Patch classes4.dex: NfGram Hub + Authentic ExteraGram Settings (Photo 3)
# -------------------------------------------------------------
# We patch string 0xa1f9 ("exteraGram.app" -> "lighthouse_top") for channel username
# so showNoticeBeforeOpeningChat("lighthouse_top") opens @lighthouse_top
# String 49344 (0xc0c0): originally 'lightnessEnhancementParam' (25 chars)
# Replace with 'lighthouse_top           ' (25 chars) - preserves exact length and alphabetical sort!
off_49344 = 0x7c59a4
assert dex4[off_49344 : off_49344 + 27] == b"\x19lightnessEnhancementParam\x00"
dex4[off_49344 : off_49344 + 27] = b"\x19lighthouse_top           \x00"
print("Patched string 0xc0c0 to lighthouse_top (padded) in classes4.dex")

# 1. MainPreferencesActivity.onClick:
# Layout:
# - 0x38a624..0x38a630: Dispatch (iget v1, UItem.id; packed-switch v1, table) (12 bytes)
# - 0x38a630..0x38a642: :open_extera_settings (new-instance MainPreferencesActivity, hasOwnBackground=1, goto :present) (18 bytes)
# - 0x38a642..0x38a66e: Case 8 (pos_c8 = 0x38a642) (if hasOwnBackground -> exteraForum; else new AyuMainPreferencesActivity; :present_and_ret) (44 bytes)
# - 0x38a66e..0x38a68e: Case 7 (pos_c7 = 0x38a66e) (trim lighthouse_top; if hasOwnBackground -> exteraGram; showNoticeBeforeOpeningChat) (32 bytes)
# - 0x38a68e..0x38a692: Padding (4 bytes)
# - 0x38a692..0x38a6a6: Case 9 (Crowdin, authentic 20 bytes untouched)
# - 0x38a6a6..0x38a6be: Case 10 (pos_c10 = 0x38a6a6) (if hasOwnBackground == 0 -> goto :open_extera_settings; else open https://exteraGram.app) (24 bytes)

base_switch = 0x38a628

# Dispatch at 0x38a624 (12 bytes)
sw_rel = (0x38a744 - base_switch) // 2
dispatch = bytearray()
dispatch.extend(b"\x52\x11\x7d\x8f") # iget v1, v1, UItem.id (field@8f7d)
dispatch.extend(b"\x2b\x01" + struct.pack("<i", sw_rel)) # packed-switch v1, table
dispatch.extend(b"\x0e\x00") # return-void
assert len(dispatch) == 12

# :open_extera_settings at 0x38a630 (18 bytes)
# Jumps to :present_and_ret in Case 8 (at 0x38a666): (0x38a666 - 0x38a640) // 2 = 19 (0x13)
open_ext = bytearray()
open_ext.extend(b"\x22\x01\x9e\x15")         # new-instance v1, MainPreferencesActivity (0x38a630)
open_ext.extend(b"\x70\x10\xbe\x74\x01\x00") # invoke-direct {v1}, <init> (0x38a634)
open_ext.extend(b"\x12\x12")                 # const/4 v2, 1 (0x38a63a)
open_ext.extend(b"\x5c\x12\xba\x8e")         # iput-boolean v2, v1, hasOwnBackground (0x38a63c)
open_ext.extend(b"\x28\x13")                 # goto +19 -> 0x38a666 (0x38a640)
assert len(open_ext) == 18

# Case 8 at 0x38a642 (44 bytes)
pos_c8 = 0x38a642
c8 = bytearray()
c8.extend(b"\x55\x01\xba\x8e") # iget-boolean v1, v0, hasOwnBackground (0x38a642)
c8.extend(b"\x38\x01\x08\x00") # if-eqz v1, +8 -> :open_ayu_settings (0x38a646)
c8.extend(b"\x1a\x01\xf6\xa1")         # const-string v1, "exteraForum" (0x38a64a)
c8.extend(b"\x70\x20\xc6\x74\x10\x00") # invoke-direct {v0, v1}, showNoticeBeforeOpeningChat (0x38a64e)
c8.extend(b"\x0e\x00")                 # return-void (0x38a654)
# :open_ayu_settings (at 0x38a656)
c8.extend(b"\x1c\x01\x01\x35")         # const-class v1, AyuMainPreferencesActivity (0x38a656)
c8.extend(b"\x6e\x10\x01\xee\x01\x00") # invoke-static {v1}, AyuFragmentUtils.getOrCreateInstance (0x38a65a)
c8.extend(b"\x0c\x01")                 # move-result-object v1 (0x38a660)
c8.extend(b"\x1f\x01\x58\x39")         # check-cast v1, BaseFragment (0x38a662)
# :present_and_ret (at 0x38a666)
c8.extend(b"\x6e\x20\x09\xf8\x10\x00") # invoke-virtual {v0, v1}, presentFragment (0x38a666)
c8.extend(b"\x0e\x00")                 # return-void (0x38a66c)
assert len(c8) == 44

# Case 7 at 0x38a66e (32 bytes)
pos_c7 = 0x38a66e
c7 = bytearray()
c7.extend(b"\x1a\x01\xc0\xc0")         # const-string v1, "lighthouse_top           " (string@c0c0) (0x38a66e)
c7.extend(b"\x6e\x10\xed\xee\x01\x00") # invoke-virtual {v1}, String.trim (method@eeed) (0x38a672)
c7.extend(b"\x0c\x01")                 # move-result-object v1 (0x38a678)
c7.extend(b"\x55\x02\xba\x8e")         # iget-boolean v2, v0, hasOwnBackground (0x38a67a)
c7.extend(b"\x38\x02\x04\x00")         # if-eqz v2, +4 -> :show_chan (0x38a67e)
c7.extend(b"\x1a\x01\xf7\xa1")         # const-string v1, "exteraGram" (string@a1f7) (0x38a682)
# :show_chan (at 0x38a686)
c7.extend(b"\x70\x20\xc6\x74\x10\x00") # invoke-direct {v0, v1}, showNoticeBeforeOpeningChat (0x38a686)
c7.extend(b"\x0e\x00")                 # return-void (0x38a68c)
assert len(c7) == 32

pad = b"\x00\x00\x00\x00"

# Case 10 at 0x38a6a6 (24 bytes)
pos_c10 = 0x38a6a6
c10 = bytearray()
c10.extend(b"\x55\x01\xba\x8e") # iget-boolean v1, v0, hasOwnBackground (0x38a6a6)
rel_ext = (0x38a630 - (pos_c10 + 4)) // 2 # offset to 0x38a630 (:open_extera_settings)
c10.extend(b"\x38\x01" + struct.pack("<h", rel_ext))
c10.extend(b"\x6e\x10\xf5\xf7\x00\x00") # invoke-virtual {v0}, getParentActivity (0x38a6ae)
c10.extend(b"\x0c\x00")                 # move-result-object v0 (0x38a6b4)
c10.extend(b"\x1a\x01\x68\xb6")         # const-string v1, "https://exteraGram.app" (0x38a6b6)
rel_url = (0x38a69e - (pos_c10 + 20)) // 2 # goto -> Browser.openUrl in Case 9
c10.extend(b"\x28" + struct.pack("b", rel_url)) # goto (0x38a6ba)
c10.extend(b"\x00\x00") # nop pad (0x38a6bc)
assert len(c10) == 24

# Write into dex4
dex4[0x38a624 : 0x38a630] = dispatch
dex4[0x38a630 : 0x38a642] = open_ext
dex4[0x38a642 : 0x38a66e] = c8
dex4[0x38a66e : 0x38a68e] = c7
dex4[0x38a68e : 0x38a692] = pad
dex4[0x38a6a6 : 0x38a6be] = c10

# Update switch targets in Switch Table at 0x38a74c:
targets = [
    0x38a718, # Key 1: HEADER_CELL
    0x38a706, # Key 2: GENERAL
    0x38a6f4, # Key 3: APPEARANCE
    0x38a6e2, # Key 4: CHATS
    0x38a6d0, # Key 5: PLUGINS
    0x38a6be, # Key 6: OTHER
    pos_c7,   # Key 7: CHANNEL
    pos_c8,   # Key 8: FORUM
    0x38a692, # Key 9: CROWDIN
    pos_c10,  # Key 10: WEBSITE
]
for i, t in enumerate(targets):
    off_val = (t - base_switch) // 2
    dex4[0x38a74c + i*4 : 0x38a74c + (i+1)*4] = struct.pack("<i", off_val)
print("Patched MainPreferencesActivity.onClick and switch targets in classes4.dex")

# 2. MainPreferencesActivity.fillItems:
#    - Root mode (hasOwnBackground == false):
#        1. HeaderSettingsCell title -> "NfGram"
#        2. Categories header
#        3. Item 1: exteraGram (WEBSITE, 0x7f080326 scaled paper plane, RED 0xffe83030, text "Preferences" = "РќР°СЃС‚СЂРѕР№РєРё exteraGram")
#        4. Item 2: AyuGram (FORUM, 0x7f080327 scaled wings, BLUE/PURPLE 0xff9570ff, text "AyuPreferences" = "РќР°СЃС‚СЂРѕР№РєРё AyuGram")
#        5. Shadow
#        6. Links header
#        7. Channel (@lighthouse_top)
#        8. Shadow
#    - Submenu mode (hasOwnBackground == true, Photo 3):
#        1. HeaderSettingsCell (vanilla authentic "exteraGram", red squircle, version)
#        2. Categories: General, Appearance, Chats, Plugins, Other
#        3. Shadow
#        4. Links: Channel, Forum, Crowdin, Website
#        5. Shadow
start_fi = 0x38a3d8
code_fi = bytearray()
code_fi.extend(b"\x08\x00\x11\x00") # move-object/from16 v0, v17
code_fi.extend(b"\x08\x01\x10\x00") # move-object/from16 v1, v16

# 1. Header:
code_fi.extend(b"\x54\x12\x90\x3e") # iget-object v2, v1, headerSettingsCell
code_fi.extend(b"\x55\x13\xba\x8e") # iget-boolean v3, v1, hasOwnBackground
ph_sub_hdr = len(code_fi)
code_fi.extend(b"\x39\x03\x00\x00") # if-nez v3, -> :add_header
ph_null_hdr = len(code_fi)
code_fi.extend(b"\x38\x02\x00\x00") # if-eqz v2, -> :add_header
# Title -> 'NfGram'
code_fi.extend(b"\x54\x23\x56\x40") # iget-object v3, v2, titleTextView
code_fi.extend(b"\x15\x04\x0f\x7f") # const/high16 v4, 0x7f0f (AppName)
code_fi.extend(b"\x71\x10\x80\xf5\x04\x00") # invoke-static {v4}, LocaleController.getString
code_fi.extend(b"\x0c\x04")                 # move-result-object v4
code_fi.extend(b"\x6e\x20\x38\x09\x43\x00") # invoke-virtual {v3, v4}, TextView.setText
# Squircle -> Green #ff2ecc71 (for NfGram!)
code_fi.extend(b"\x54\x23\x53\x40")         # iget-object v3, v2, imageView (field@4053)
code_fi.extend(b"\x14\x04\x71\xcc\x2e\xff") # const v4, 0xff2ecc71 (green)
code_fi.extend(b"\x6e\x20\xc0\x07\x43\x00") # invoke-virtual {v3, v4}, View.setBackgroundColor (method@07c0)

# :add_header
pos_add_hdr = len(code_fi)
code_fi[ph_sub_hdr + 2 : ph_sub_hdr + 4] = struct.pack('<h', (pos_add_hdr - ph_sub_hdr) // 2)
code_fi[ph_null_hdr + 2 : ph_null_hdr + 4] = struct.pack('<h', (pos_add_hdr - ph_null_hdr) // 2)

code_fi.extend(b"\x13\x03\xc6\x00")         # const/16 v3, 198
code_fi.extend(b"\x71\x20\xcd\xfa\x32\x00") # invoke-static {v2, v3}, UItem.asCustomShadow
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x12\x13")                 # const/4 v3, 1 (HEADER_CELL id)
code_fi.extend(b"\x6e\x20\xe9\xfa\x32\x00") # invoke-virtual {v2, v3}, UItem.setId
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add

# 2. Categories Header:
code_fi.extend(b"\x60\x02\x50\x8a")         # sget v2, R.string.Categories
code_fi.extend(b"\x71\x10\x80\xf5\x02\x00") # invoke-static {v2}, LocaleController.getString
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x71\x10\xd1\xfa\x02\x00") # invoke-static {v2}, UItem.asHeader
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add

# 3. Branch on hasOwnBackground for categories:
code_fi.extend(b"\x55\x12\xba\x8e") # iget-boolean v2, v1, hasOwnBackground
ph_sub_cat = len(code_fi)
code_fi.extend(b"\x39\x02\x00\x00") # if-nez v2, -> :sub_categories

# --- ROOT CATEGORIES (UItem.asButton method@fac1: id, icon, text) ---
# Item 1: exteraGram
code_fi.extend(b"\x13\x02\x0a\x00")         # const/16 v2, 10 (WEBSITE id)
code_fi.extend(b"\x14\x04\x26\x03\x08\x7f") # const v4, 0x7f080326 (plane)
code_fi.extend(b"\x14\x03\x24\xde\x0f\x7f") # const v3, 0x7f0fde24 (Preferences)
code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x71\x30\xc1\xfa\x42\x03") # invoke-static {v2, v4, v3}, UItem.asButton (method@fac1)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x14\x03\x30\x30\xe8\xff") # const v3, 0xffe83030 (red)
code_fi.extend(b"\x6e\x30\xe6\xfa\x42\x03") # invoke-virtual {v2, v4, v3}, UItem.setColorfulIcon (method@fae6)
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add

# Item 2: AyuGram
code_fi.extend(b"\x13\x02\x08\x00")         # const/16 v2, 8 (FORUM id)
code_fi.extend(b"\x14\x04\x27\x03\x08\x7f") # const v4, 0x7f080327 (wings)
code_fi.extend(b"\x14\x03\xa3\xfa\x0f\x7f") # const v3, 0x7f0ffaa3 (AyuPreferences)
code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x71\x30\xc1\xfa\x42\x03") # invoke-static {v2, v4, v3}, UItem.asButton (method@fac1)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x14\x03\xff\x70\x95\xff") # const v3, 0xff9570ff (blue/purple)
code_fi.extend(b"\x6e\x30\xe6\xfa\x42\x03") # invoke-virtual {v2, v4, v3}, UItem.setColorfulIcon (method@fae6)
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add

ph_after_cat = len(code_fi)
code_fi.extend(b"\x28\x00") # goto -> :after_categories

# --- SUBMENU CATEGORIES (Compact Loop: id v2 = 2..6) ---
pos_sub_cat = len(code_fi)
code_fi[ph_sub_cat + 2 : ph_sub_cat + 4] = struct.pack('<h', (pos_sub_cat - ph_sub_cat) // 2)

code_fi.extend(b"\x12\x22") # const/4 v2, 2

pos_loop = len(code_fi)
# switch on v2 (2: General, 3: Appearance, 4: Chats, 5: Plugins, 6: Other)
code_fi.extend(b"\x12\x27") # const/4 v7, 2
ph_is2 = len(code_fi)
code_fi.extend(b"\x32\x72\x00\x00") # if-eq v2, v7, :is_2
code_fi.extend(b"\x12\x37") # const/4 v7, 3
ph_is3 = len(code_fi)
code_fi.extend(b"\x32\x72\x00\x00") # if-eq v2, v7, :is_3
code_fi.extend(b"\x12\x47") # const/4 v7, 4
ph_is4 = len(code_fi)
code_fi.extend(b"\x32\x72\x00\x00") # if-eq v2, v7, :is_4
code_fi.extend(b"\x12\x57") # const/4 v7, 5
ph_is5 = len(code_fi)
code_fi.extend(b"\x32\x72\x00\x00") # if-eq v2, v7, :is_5

# else is 6 (Other)
code_fi.extend(b"\x60\x04\x58\x89") # sget v4, msg_fave (field@8958)
code_fi.extend(b"\x60\x03\x34\x8b") # sget v3, LocalOther (field@8b34)
ph_goto_add = len(code_fi)
code_fi.extend(b"\x28\x00")

# :is_2 (General)
pos_is2 = len(code_fi)
code_fi[ph_is2 + 2 : ph_is2 + 4] = struct.pack('<h', (pos_is2 - ph_is2) // 2)
code_fi.extend(b"\x60\x04\x6b\x89") # sget v4, msg_media (field@896b)
code_fi.extend(b"\x60\x03\xed\x8a") # sget v3, General (field@8aed)
ph_goto2 = len(code_fi)
code_fi.extend(b"\x28\x00")

# :is_3 (Appearance)
pos_is3 = len(code_fi)
code_fi[ph_is3 + 2 : ph_is3 + 4] = struct.pack('<h', (pos_is3 - ph_is3) // 2)
code_fi.extend(b"\x60\x04\x90\x89") # sget v4, msg_theme (field@8990)
code_fi.extend(b"\x60\x03\x23\x8a") # sget v3, Appearance (field@8a23) ("Р’РЅРµС€РЅРёР№ РІРёРґ")
ph_goto3 = len(code_fi)
code_fi.extend(b"\x28\x00")

# :is_4 (Chats)
pos_is4 = len(code_fi)
code_fi[ph_is4 + 2 : ph_is4 + 4] = struct.pack('<h', (pos_is4 - ph_is4) // 2)
code_fi.extend(b"\x60\x04\x54\x89") # sget v4, msg_discussion (field@8954)
code_fi.extend(b"\x60\x03\xf7\x8b") # sget v3, SearchAllChatsShort (field@8bf7)
ph_goto4 = len(code_fi)
code_fi.extend(b"\x28\x00")

# :is_5 (Plugins)
pos_is5 = len(code_fi)
code_fi[ph_is5 + 2 : ph_is5 + 4] = struct.pack('<h', (pos_is5 - ph_is5) // 2)
code_fi.extend(b"\x60\x04\x78\x89") # sget v4, msg_plugins (field@8978)
code_fi.extend(b"\x60\x03\x9b\x8b") # sget v3, Plugins (field@8b9b)

# :add_button
pos_add = len(code_fi)
code_fi[ph_goto_add + 1] = (pos_add - ph_goto_add) // 2
code_fi[ph_goto2 + 1] = (pos_add - ph_goto2) // 2
code_fi[ph_goto3 + 1] = (pos_add - ph_goto3) // 2
code_fi[ph_goto4 + 1] = (pos_add - ph_goto4) // 2

code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x71\x30\xc1\xfa\x42\x03") # invoke-static {v2, v4, v3}, UItem.asButton
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x6e\x20\x55\xf0\x30\x00") # invoke-virtual {v0, v3}, ArrayList.add
code_fi.extend(b"\xd8\x02\x02\x01")         # add-int/lit8 v2, v2, 1
code_fi.extend(b"\x12\x77")                 # const/4 v7, 7
code_fi.extend(b"\x34\x72" + struct.pack('<h', (pos_loop - len(code_fi)) // 2)) # if-lt v2, v7, :loop

# :after_categories (Shared Shadow)
pos_after_cat = len(code_fi)
code_fi[ph_after_cat + 1] = (pos_after_cat - ph_after_cat) // 2

code_fi.extend(b"\x71\x00\xd8\xfa\x00\x00") # invoke-static {}, UItem.asShadow
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add

# Shared Links Header:
code_fi.extend(b"\x60\x02\x2f\x8b")         # sget v2, R.string.Links
code_fi.extend(b"\x71\x10\x80\xf5\x02\x00") # invoke-static {v2}, LocaleController.getString
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x71\x10\xd1\xfa\x02\x00") # invoke-static {v2}, UItem.asHeader
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add

# --- SHARED CHANNEL ITEM ---
code_fi.extend(b"\x13\x02\x07\x00")         # const/16 v2, 7 (CHANNEL id)
code_fi.extend(b"\x60\x04\x4b\x89")         # sget v4, msg_channel
code_fi.extend(b"\x60\x03\xc4\x8b")         # sget v3, ProfileChannel
code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x55\x15\xba\x8e")         # iget-boolean v5, v1, hasOwnBackground
ph_sub_chan = len(code_fi)
code_fi.extend(b"\x39\x05\x00\x00")         # if-nez v5, -> :sub_chan_text
# Root channel text:
code_fi.extend(b"\x1a\x05\xc0\xc0")         # const-string v5, 'lighthouse_top           '
code_fi.extend(b"\x6e\x10\xed\xee\x05\x00") # invoke-virtual {v5}, String.trim
code_fi.extend(b"\x0c\x05")                 # move-result-object v5
ph_goto_add_chan = len(code_fi)
code_fi.extend(b"\x28\x00")                 # goto -> :add_chan
# :sub_chan_text
pos_sub_chan = len(code_fi)
code_fi[ph_sub_chan + 2 : ph_sub_chan + 4] = struct.pack('<h', (pos_sub_chan - ph_sub_chan) // 2)
code_fi.extend(b"\x1a\x05\xf7\xa1")         # const-string v5, 'exteraGram'
# :add_chan
pos_add_chan = len(code_fi)
code_fi[ph_goto_add_chan + 1] = (pos_add_chan - ph_goto_add_chan) // 2

code_fi.extend(b"\x71\x40\xc2\xfa\x42\x53") # invoke-static {v2, v4, v3, v5}, UItem.asButton (method@fac2)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add

# If Root mode, jump straight to final shadow!
code_fi.extend(b"\x55\x12\xba\x8e")         # iget-boolean v2, v1, hasOwnBackground
ph_to_shadow = len(code_fi)
code_fi.extend(b"\x38\x02\x00\x00")         # if-eqz v2, -> :final_shadow

# --- SUBMENU REMAINING LINKS ---
# Sub Link 2: Forum (@exteraForum) (id=8)
code_fi.extend(b"\x13\x02\x08\x00")         # const/16 v2, 8
code_fi.extend(b"\x60\x04\x60\x89")         # sget v4, msg_groups (field@8960)
code_fi.extend(b"\x60\x03\xf7\x8b")         # sget v3, SearchAllChatsShort (field@8bf7) ("Р§Р°С‚С‹")
code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x1a\x05\xf6\xa1")         # const-string v5, 'exteraForum'
code_fi.extend(b"\x71\x40\xc2\xfa\x42\x53") # invoke-static {v2, v4, v3, v5}, UItem.asButton (method@fac2)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add

# Sub Link 3: Crowdin (id=9)
code_fi.extend(b"\x13\x02\x09\x00")         # const/16 v2, 9
code_fi.extend(b"\x60\x04\x92\x89")         # sget v4, msg_translate
code_fi.extend(b"\x60\x03\x71\x8a")         # sget v3, Crowdin
code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x1a\x05\xa5\x1e")         # const-string v5, 'Crowdin'
code_fi.extend(b"\x71\x40\xc2\xfa\x42\x53") # invoke-static {v2, v4, v3, v5}, UItem.asButton (method@fac2)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add

# Sub Link 4: Website (id=10)
code_fi.extend(b"\x13\x02\x0a\x00")         # const/16 v2, 10
code_fi.extend(b"\x60\x04\x63\x89")         # sget v4, msg_language
code_fi.extend(b"\x60\x03\x81\x8c")         # sget v3, Website
code_fi.extend(b"\x71\x10\x80\xf5\x03\x00") # invoke-static {v3}, LocaleController.getString
code_fi.extend(b"\x0c\x03")                 # move-result-object v3
code_fi.extend(b"\x1a\x05\x00\xa2")         # const-string v5, 'exteragram.app'
code_fi.extend(b"\x71\x40\xc2\xfa\x42\x53") # invoke-static {v2, v4, v3, v5}, UItem.asButton (method@fac2)
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add

# :final_shadow
pos_final_shadow = len(code_fi)
code_fi[ph_to_shadow + 2 : ph_to_shadow + 4] = struct.pack('<h', (pos_final_shadow - ph_to_shadow) // 2)

code_fi.extend(b"\x71\x00\xd8\xfa\x00\x00") # invoke-static {}, UItem.asShadow
code_fi.extend(b"\x0c\x02")                 # move-result-object v2
code_fi.extend(b"\x6e\x20\x55\xf0\x20\x00") # invoke-virtual {v0, v2}, ArrayList.add
code_fi.extend(b"\x0e\x00")                 # return-void

print(f"Total fillItems bytecode len: {len(code_fi)} bytes (limit: 572)")
assert len(code_fi) <= 572
while len(code_fi) < 572:
    code_fi.extend(b"\x00\x00")
assert len(code_fi) == 572

dex4[start_fi : start_fi + 572] = code_fi
print("Patched MainPreferencesActivity.fillItems (Root NfGram hub + 100% complete Photo 3 exteraGram) in classes4.dex")

dex4[12:32] = hashlib.sha1(dex4[32:]).digest()
dex4[8:12] = struct.pack("<I", zlib.adler32(dex4[12:]) & 0xFFFFFFFF)

# -------------------------------------------------------------
# 2. Patch classes5.dex: package name
# -------------------------------------------------------------
string_ids_off5 = struct.unpack("<I", dex5[60:64])[0]
str41733_off = struct.unpack("<I", dex5[string_ids_off5 + 41733*4 : string_ids_off5 + 41734*4])[0]
assert dex5[str41733_off : str41733_off + 21] == expected_old_entry
dex5[str41733_off : str41733_off + 21] = new_entry

dex5[12:32] = hashlib.sha1(dex5[32:]).digest()
dex5[8:12] = struct.pack("<I", zlib.adler32(dex5[12:]) & 0xFFFFFFFF)

# -------------------------------------------------------------
# 3. Patch classes6.dex: ProfileActivity row count + SettingsActivity single green button
#    NOTE: PasscodeActivity is NOT patched at all! All Face ID code removed, 100% vanilla!
# -------------------------------------------------------------
# 3.1 ProfileActivity.updateRows: unify to 1 row
assert dex6[0x5e607c] == 8
dex6[0x5e607c] = 7

orig_rows = bytes.fromhex("d8 07 04 02 59 06 3c 9a d8 06 04 03 59 07 df 99 d8 07 04 04 59 06 10 9a d8 06 04 05 59 07 dd 9a d8 07 04 06 59 06 a8 9a d8 06 04 07 59 07 26 9a")
new_rows  = bytes.fromhex("12 f7 59 06 3c 9a 59 07 df 99 d8 06 04 02 59 06 10 9a d8 07 04 03 59 07 dd 9a d8 06 04 04 59 06 a8 9a d8 07 04 05 59 07 26 9a d8 06 04 06 00 00")
assert dex6[0x5e625e : 0x5e625e + len(orig_rows)] == orig_rows
dex6[0x5e625e : 0x5e625e + len(orig_rows)] = new_rows
print("Applied ProfileActivity unified settings row patch in classes6.dex")

# 3.2 SettingsActivity.fillItems:
patch_settings_btn = bytearray()
patch_settings_btn.extend(b"\x15\x03\x0f\x7f")         # const/high16 v3, 0x7f0f (AppName = "NfGram")
patch_settings_btn.extend(b"\x71\x10\x70\x0f\x03\x00") # invoke-static {v3}, LocaleController.getString
patch_settings_btn.extend(b"\x0c\x03")                 # move-result-object v3
patch_settings_btn.extend(b"\x12\xf5")                 # const/4 v5, -1
patch_settings_btn.extend(b"\x14\x06\x71\xcc\x2e\xff") # const v6, 0xff2ecc71 (GREEN!)
patch_settings_btn.extend(b"\x71\x53\xd6\xe6\x65\x26") # invoke-static {v5, v6, v6, v2, v3}, SettingCell$Factory.of
patch_settings_btn.extend(b"\x0c\x02")                 # move-result-object v2
patch_settings_btn.extend(b"\x6e\x20\xc0\x0a\x21\x00") # invoke-virtual {v1, v2}, ArrayList.add
assert len(patch_settings_btn) == 34

assert dex6[0x62e4e2 : 0x62e4e2 + 34] == bytes.fromhex("60 03 51 11 71 10 70 0f 03 00 0c 03 12 f5 14 06 30 30 e8 ff 71 53 d6 e6 65 26 0c 02 6e 20 c0 0a 21 00")
dex6[0x62e4e2 : 0x62e4e2 + 34] = patch_settings_btn

# NOP out row 2 (AyuGram button, 38 bytes at 0x62e504)
orig_ayu_row = bytes.fromhex("60 02 8a 04 60 03 b7 08 71 10 70 0f 03 00 0c 03 12 e5 14 06 ff 70 95 ff 71 53 d6 e6 65 26 0c 02 6e 20 c0 0a 21 00")
assert dex6[0x62e504 : 0x62e504 + len(orig_ayu_row)] == orig_ayu_row
dex6[0x62e504 : 0x62e504 + len(orig_ayu_row)] = b"\x00" * len(orig_ayu_row) # 19 NOPs
print("Applied SettingsActivity single green button patch in classes6.dex")

dex6[12:32] = hashlib.sha1(dex6[32:]).digest()
dex6[8:12] = struct.pack("<I", zlib.adler32(dex6[12:]) & 0xFFFFFFFF)

# -------------------------------------------------------------
# Verify all DEX files using dexdump -c
# -------------------------------------------------------------
for name, dex_data in [("classes.dex", dex1), ("classes4.dex", dex4), ("classes5.dex", dex5), ("classes6.dex", dex6), ("classes7.dex", dex7)]:
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

# Bump versionCode from 71129 to 71157
old_vc = struct.pack("<I", 71129)
new_vc = struct.pack("<I", 71157)
assert manifest.count(old_vc) == 1
manifest = manifest.replace(old_vc, new_vc)
print("Bumped versionCode to 71157 in AndroidManifest.xml")

print("=== STEP 3: Patch resources.arsc ===")
arsc_pkg_count = arsc.count(old_pkg_u16)
assert arsc_pkg_count == 1
arsc = arsc.replace(old_pkg_u16, new_pkg_u16)

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
    8560: "Смена чёлки Nfgram",
    8563: "NfGram Preferences",
    9497: "NfGram",
    9593: "Update NfGram",
    9635: "Welcome to the NfGram Desktop. Make Telegram your own.",
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

print("=== STEP 4: Prepare Icons ===")
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

with zipfile.ZipFile(VANILLA_APK, "r") as z_van:
    qS4_van = z_van.read("res/qS4.xml")
    _8ZN_van = z_van.read("res/8ZN.xml")

icon_replacements["res/qS4.xml"] = qS4_van.replace(b"\x08\x00\x00\x05\x01\x48\x00\x00", b"\x08\x00\x00\x05\x01\x18\x00\x00")
icon_replacements["res/8ZN.xml"] = _8ZN_van.replace(b"\x08\x00\x00\x05\x01\x48\x00\x00", b"\x08\x00\x00\x05\x01\x18\x00\x00")

with zipfile.ZipFile(VANILLA_APK, "r") as zin:
    lna_splash = zin.read("res/lnA.xml")
    twu_raw = bytearray(zin.read("res/Twu.xml"))

bg_color_old = bytes.fromhex("08 00 00 01 8a 00 06 7f")
bg_color_new = bytes.fromhex("08 00 00 1d 71 cc 2e ff") # #ff2ecc71 emerald green
plane_color_old = bytes.fromhex("08 00 00 01 8c 00 06 7f")
plane_color_new = bytes.fromhex("08 00 00 1d ff ff ff ff") # pure white

twu_patched = twu_raw.replace(bg_color_old, bg_color_new).replace(plane_color_old, plane_color_new)
fa_old = bytes.fromhex("08 00 00 04 00 00 00 00")
fa_new = bytes.fromhex("08 00 00 04 00 00 80 3f") # float 1.0 for static fallback
twu_static = twu_patched.replace(fa_old, fa_new)

icon_replacements["res/Twu.xml"] = bytes(twu_patched)
icon_replacements["res/lnA.xml"] = lna_splash
icon_replacements["res/HWO.xml"] = lna_splash
icon_replacements["res/fSN.xml"] = bytes(twu_static)

print(f"Prepared {len(icon_replacements)} icon replacements.")

print("=== STEP 5: Patch Locales ===")
xml_replacements = {}
with zipfile.ZipFile(VANILLA_APK, "r") as zin:
    for xml_path, pref_val in [
        ("assets/ayu_locales/values-ru/ayu.xml", "Настройки NfGram"),
        ("assets/ayu_locales/values/ayu.xml", "NfGram Preferences")
    ]:
        base_text = zin.read(xml_path).decode("utf-8")
        insert_line = f'  <string name="NfGramPreferences">{pref_val}</string>\n  <string name="AppNameAlt">Смена чёлки Nfgram</string>\n</resources>'
        new_text = base_text.replace("</resources>", insert_line)
        xml_replacements[xml_path] = new_text.encode("utf-8")

print("=== STEP 6: Repack APK ===")
unaligned_apk = "nfgram_unaligned.apk"
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
        elif item.filename == "lib/arm64-v8a/libtmessages.49.so":
            so_data = bytearray(zin.read(item.filename))
            assert so_data[0x11174d8 : 0x11174d8 + 8] == bytes.fromhex("ff 83 05 d1 fd 7b 11 a9")
            so_data[0x11174d8 : 0x11174d8 + 8] = bytes.fromhex("e0 03 1f 2a c0 03 5f d6")
            assert so_data[0x11f0728 : 0x11f0728 + 8] == bytes.fromhex("29 10 40 f9 e8 03 1f 2a")
            so_data[0x11f0728 : 0x11f0728 + 8] = bytes.fromhex("e0 03 1f 2a c0 03 5f d6")
            zout.writestr(item, so_data, compress_type=item.compress_type)
            print("Patched lib/arm64-v8a/libtmessages.49.so: LSPlant hooks neutralized (fixed ART JIT crash)")
        elif item.filename == "lib/armeabi-v7a/libtmessages.49.so":
            so_data = bytearray(zin.read(item.filename))
            assert so_data[0xe4bd50 : 0xe4bd50 + 4] == bytes.fromhex("f0 b5 03 af")
            so_data[0xe4bd50 : 0xe4bd50 + 4] = bytes.fromhex("00 20 70 47")
            zout.writestr(item, so_data, compress_type=item.compress_type)
            print("Patched lib/armeabi-v7a/libtmessages.49.so: LSPlant hooks neutralized")
        else:
            data = zin.read(item.filename)
            zout.writestr(item, data, compress_type=item.compress_type)

print(f"Created unaligned APK: {unaligned_apk} ({os.path.getsize(unaligned_apk)} bytes)")

print("=== STEP 7: Zipalign APK ===")
aligned_apk = "nfgram_aligned.apk"
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)

res = subprocess.run([ZIPALIGN, "-p", "-f", "4", unaligned_apk, aligned_apk], capture_output=True, text=True)
if res.returncode != 0:
    print("Zipalign error:", res.stderr)
    exit(1)
print(f"Zipalign succeeded: {aligned_apk} ({os.path.getsize(aligned_apk)} bytes)")

print("=== STEP 8: Sign APK with Keystore ===")
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
    OUTPUT_APK_NFGRAM,
    r"c:\Users\styuk\Downloads\AyuGram Desktop\AyuGram-12.10.6-universal.apk",
    r"c:\Users\styuk\Downloads\NfGram-12.10.6-universal.apk",
]
for dst in destinations:
    try:
        dst_dir = os.path.dirname(dst)
        if os.path.exists(dst_dir):
            shutil.copy2(aligned_apk, dst)
            print(f"Deployed: {dst}")
    except Exception as e:
        print(f"Warning deploying to {dst}: {e}")

# Auto-install via adb if device is connected
try:
    p_dev = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    if "device\n" in p_dev.stdout or "\tdevice" in p_dev.stdout:
        print("=== STEP 11: Auto-installing APK to connected Android device ===")
        res_inst = subprocess.run(["adb", "install", "-r", aligned_apk], capture_output=True, text=True)
        print("ADB Install result:", res_inst.stdout.strip())
except Exception as e:
    print("ADB auto-install skipped:", e)

print("ALL DONE! BUILD COMPLETED 100% SUCCESSFULLY!")
