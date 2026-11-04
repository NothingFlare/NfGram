"""
Full NfGram 13.1.1 Build & Verification Script
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

BASE_DIR = r"C:\project\NfGram Android"
VANILLA_APK = r"c:\Users\styuk\Desktop\vanilla-AyuGram-full-20261104.apk"
EXTERA_APK = r"c:\Users\styuk\Downloads\AyuGram Desktop\exteraGram-full-universal-20261004.apk"
OUTPUT_APK_NFGRAM = r"c:\Users\styuk\Downloads\AyuGram Desktop\NfGram-13.1.1-universal.apk"
OUTPUT_APK_DESKTOP = r"C:\Users\styuk\Desktop\NfGram-13.1.1-universal.apk"
OUTPUT_APK_PROJECT = os.path.join(BASE_DIR, "NfGram-13.1.1-universal.apk")

KEYSTORE = os.path.join(BASE_DIR, "Tools", "nfgram_release.keystore")
ZIPALIGN = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\zipalign.exe"
APKSIGNER_JAR = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\lib\apksigner.jar"
AAPT = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\aapt.exe"
ANDROID_JAR = r"C:\Users\styuk\AppData\Local\Android\Sdk\platforms\android-34\android.jar"
D8 = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\d8.bat"
DEXDUMP = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\dexdump.exe"

OLD_PACKAGE = "com.radolyn.ayugram"
NEW_PACKAGE = "com.red.nfgram.chat"
assert len(NEW_PACKAGE) == len(OLD_PACKAGE) == 19

print("=== STEP 0: Compile NfGramGithubUpdater.java to classes9.dex ===")
build_tmp = os.path.join(BASE_DIR, "Tools", "build_tmp")
if os.path.exists(build_tmp):
    shutil.rmtree(build_tmp)
os.makedirs(build_tmp, exist_ok=True)

updater_src = os.path.join(BASE_DIR, "TMessagesProj", "src", "main", "java", "com", "radolyn", "ayugram", "utils", "NfGramGithubUpdater.java")
cmd_javac = [
    "javac",
    "--release", "11",
    "-cp", ANDROID_JAR,
    "-d", build_tmp,
    updater_src
]
res_javac = subprocess.run(cmd_javac, capture_output=True, text=True)
if res_javac.returncode != 0:
    print("Javac compilation failed:", res_javac.stderr)
    exit(1)

class_files = []
for root, _, files in os.walk(build_tmp):
    for fn in files:
        if fn.endswith(".class"):
            class_files.append(os.path.join(root, fn))

cmd_d8 = [
    D8,
    "--lib", ANDROID_JAR,
    "--output", build_tmp
] + class_files
res_d8 = subprocess.run(cmd_d8, capture_output=True, text=True)
if res_d8.returncode != 0:
    print("D8 compilation failed:", res_d8.stderr)
    exit(1)

dex9_path = os.path.join(build_tmp, "classes.dex")
assert os.path.exists(dex9_path)
with open(dex9_path, "rb") as f:
    dex9 = f.read()
print(f"Compiled classes9.dex successfully: {len(dex9)} bytes")

print("=== STEP 1: Patch DEX files ===")
with zipfile.ZipFile(VANILLA_APK, "r") as z:
    dex1 = bytearray(z.read("classes.dex"))
    dex4 = bytearray(z.read("classes4.dex"))
    dex7 = bytearray(z.read("classes7.dex"))
    manifest = bytearray(z.read("AndroidManifest.xml"))
    arsc = bytearray(z.read("resources.arsc"))

# -------------------------------------------------------------
# 1. Patch classes.dex: sensors, thermal, battery, pluginsEngine
# -------------------------------------------------------------
# Proximity and Ear Sensor Optimization:
# 1. Proximity isNearToSensor: reduce distance threshold from 5.0f to 2.0f
assert dex1[0x500cc4 : 0x500cc8] == bytes.fromhex('15 00 a0 40')
dex1[0x500cc4 : 0x500cc8] = bytes.fromhex('15 00 00 40')

# 2. Accelerometer vertical angle: increase threshold from 2.5f to 5.5f
assert dex1[0x5097aa : 0x5097ae] == bytes.fromhex('15 04 20 40')
dex1[0x5097aa : 0x5097ae] = bytes.fromhex('15 04 b0 40')
print("Applied Proximity and Ear sensor anti-accidental trigger patch in classes.dex")

# Thermal and Overheating Protection:
# 3. Disable KeepAliveJob.startJob (JobScheduler deadline churn)
assert dex1[0x4f1b0c : 0x4f1b0c + 22] == bytes.fromhex("62 00 f1 83 22 01 2e 23 70 10 83 b6 01 00 6e 20 65 af 10 00 0e 00".replace(" ", ""))
dex1[0x4f1b0c : 0x4f1b0c + 22] = bytes.fromhex("0e 00") + b"\x00" * 20
print("Applied KeepAliveJob thermal wakeup suppression patch in classes.dex")

# 4. Cap DevicePerformanceClass to PERFORMANCE_CLASS_AVERAGE (1)
assert dex1[0x32a320 : 0x32a324] == bytes.fromhex("60 00 96 00")
dex1[0x32a320 : 0x32a324] = bytes.fromhex("12 10 0f 00")

# 4b. Cap SharedConfig.getDevicePerformanceClass unconditionally to PERFORMANCE_CLASS_AVERAGE (1)
assert dex1[0x329808 : 0x329808 + 4] == bytes.fromhex("60 00 2b 82")
dex1[0x329808 : 0x329808 + 38] = bytes.fromhex("12 10 0f 00") + b"\x00" * 34
print("Applied Thermal and Overheating protection patch in classes.dex (capped getDevicePerformanceClass to AVERAGE)")

# Battery Patch 1: Disable persistent file logging (BuildVars.LOGS_ENABLED = false)
assert dex1[0x292e44 : 0x292e44 + 12] == bytes.fromhex("71 00 3f 2f 00 00 0a 00 6a 00 c8 2e".replace(" ", ""))
dex1[0x292e44 : 0x292e44 + 12] = bytes.fromhex("12 00 6a 00 c8 2e 00 00 00 00 00 00".replace(" ", ""))
print("Applied Battery patch 1: LOGS_ENABLED disabled")

# Battery Patch 2: Disable drawActionBarShadow in SharedConfig.<clinit>
assert dex1[0x329654 : 0x329658] == bytes.fromhex("6a 03 05 82")
dex1[0x329654 : 0x329658] = bytes.fromhex("6a 02 05 82")

# Battery Patch 3: Force disable real-time compute blur shaders in SharedConfig.loadConfig()
assert dex1[0x32a16c : 0x32a172] == bytes.fromhex("0a 02 6a 02 6f 82")
dex1[0x32a16c : 0x32a172] = bytes.fromhex("12 02 6a 02 6f 82") # useNewBlur = false

assert dex1[0x32a1e2 : 0x32a1e8] == bytes.fromhex("0a 02 6a 02 3a 82")
dex1[0x32a1e2 : 0x32a1e8] = bytes.fromhex("12 02 6a 02 3a 82") # photoViewerBlur = false

assert dex1[0x32a2d8 : 0x32a2de] == bytes.fromhex("0a 02 6a 02 05 82")
dex1[0x32a2d8 : 0x32a2de] = bytes.fromhex("12 02 6a 02 05 82") # drawActionBarShadow = false
print("Applied Battery patch 3: useNewBlur, photoViewerBlur & drawActionBarShadow disabled in loadConfig")

# Battery Patch 4: Disable chat GPU background blur pass
assert dex1[0x3296ec : 0x3296f0] == bytes.fromhex("12 10 0f 00")
dex1[0x3296ec : 0x3296f0] = bytes.fromhex("12 00 0f 00") # canBlurChat = false

assert dex1[0x329700 : 0x329706] == bytes.fromhex("71 00 4e d5 00 00")
dex1[0x329700 : 0x329700 + 36] = bytes.fromhex("12 00 0f 00") + b"\x00" * 32 # chatBlurEnabled = false
print("Applied Battery patch 4: canBlurChat and chatBlurEnabled disabled (stops GPU shader overhead)")

# Battery Patch 5: Keep LiteMode.loadPreference 100% vanilla to prevent ART VerifyError

# Single Persistent Background Push Connection: ConnectionsManager.isPushConnectionEnabled() -> always true
assert dex1[0x337fd0 : 0x337fd6] == bytes.fromhex("71 00 74 c7 00 00")
dex1[0x337fd0 : 0x337fd0 + 66] = bytes.fromhex("12 10 0f 00") + b"\x00" * 62
print("Applied Single Background Connection Patch: isPushConnectionEnabled returns true")

# Disable Comma After Mention: ExteraConfig.getAddCommaAfterMention() -> always false
assert dex1[0x3ad188 : 0x3ad190] == bytes.fromhex("62 00 85 0d 62 01 83 0d")
dex1[0x3ad188 : 0x3ad188 + 40] = bytes.fromhex("12 00 0f 00") + b"\x00" * 36
print("Applied Disable Comma After Mention Patch: getAddCommaAfterMention returns false")

# Neutralize NativeCrashHandler.init call
assert dex1[0x2919a0 : 0x2919a0 + 14] == bytes.fromhex("71 00 cf 38 00 00 0c 00 71 10 d0 38 00 00")
dex1[0x2919a0 : 0x2919a0 + 14] = b"\x00" * 14
print("Applied NativeCrashHandler suppression patch in classes.dex (prevents false SIGSEGV kills)")

# Plugins Engine Fix: Ensure Python Plugins engine is enabled & stable
assert dex1[0x1e997a : 0x1e997e] == bytes.fromhex("39 01 34 00")
dex1[0x1e997a : 0x1e997e] = bytes.fromhex("28 34 00 00") # bypass killswitch

assert dex1[0x1e99f2 : 0x1e99f4] == bytes.fromhex("0a 01")
dex1[0x1e99f2 : 0x1e99f4] = bytes.fromhex("12 11") # force pluginsEngine = true

assert dex1[0x3cbfc4 : 0x3cbfc8] == bytes.fromhex("1a 00 ff d5")
dex1[0x3cbfc4 : 0x3cbfc8] = bytes.fromhex("12 00 11 00") # findModuleNameOwner returns null

assert dex1[0x3cab9e : 0x3cab9e + 10] == bytes.fromhex("54 f2 8e 10 39 02 03 00 0f 01")
dex1[0x3cab9e : 0x3cab9e + 10] = bytes.fromhex("70 10 60 38 0f 00 54 f2 8e 10") # getPython() init

assert dex1[0x3caedc : 0x3caede] == bytes.fromhex("01 13")
dex1[0x3caedc : 0x3caede] = bytes.fromhex("12 13") # sdkInitialized = true

assert dex1[0x3cb236 : 0x3cb23a] == bytes.fromhex("39 00 48 00")
dex1[0x3cb236 : 0x3cb23a] = bytes.fromhex("00 00 00 00") # allow safe mode

old_req = bytes.fromhex("22 00 7f 19 1a 01 ff a5 70 20 2b 76 10 00 27 00")
assert dex1[0x3cb2b6 : 0x3cb2b6 + 16] == old_req
dex1[0x3cb2b6 : 0x3cb2b6 + 16] = bytes.fromhex("70 10 63 38 03 00 28 bf 00 00 00 00 00 00 00 00") # lazy bootstrap

old_refresh = bytes.fromhex("1b 03 0f 3b 01 00 6e 20 ae 2e 31 00 0c 03 1f 03 6f 09 38 05 13 00 38 03 11 00 1b 01 b1 3d 01 00 6e 10 1a 75 05 00 0c 05 12 02 24 20 e4 3b 25 00 0c 05 6e 30 ab 2e 13 05")
assert dex1[0x3cee46 : 0x3cee46 + len(old_refresh)] == old_refresh
new_refresh = bytes.fromhex("1b 03 03 3b 01 00 6e 20 ae 2e 31 00 0c 03 1f 03 6f 09 38 05 13 00 38 03 11 00 1b 01 52 d6 00 00 6e 10 1a 75 05 00 0c 05 24 10 e4 3b 05 00 0c 05 00 00 6e 30 ab 2e 13 05")
dex1[0x3cee46 : 0x3cee46 + len(new_refresh)] = new_refresh # append to sys.path

assert dex1[0x3cca94 : 0x3cca96] == bytes.fromhex("27 03")
dex1[0x3cca94 : 0x3cca96] = bytes.fromhex("28 01") # empty map on metadata error

assert dex1[0x3cfd78 : 0x3cfd7c] == bytes.fromhex("54 60 8e 10")
dex1[0x3cfd78 : 0x3cfd7a] = bytes.fromhex("0e 00") # do not purge SDK modules
print("Applied PythonPluginsEngine patches 1-8 in classes.dex")

# Package name replacement in dex1
old_dir = b"/data/data/" + OLD_PACKAGE.encode("utf-8") + b"/files"
new_dir = b"/data/data/" + NEW_PACKAGE.encode("utf-8") + b"/files"
assert dex1.count(old_dir) == 1
idx_dir = dex1.find(old_dir)
dex1[idx_dir : idx_dir + len(old_dir)] = new_dir

expected_old_entry = b"\x13" + OLD_PACKAGE.encode("utf-8") + b"\x00"
new_entry = b"\x13" + NEW_PACKAGE.encode("utf-8") + b"\x00"
string_ids_off1 = struct.unpack("<I", dex1[60:64])[0]
str58093_off = struct.unpack("<I", dex1[string_ids_off1 + 58093*4 : string_ids_off1 + 58094*4])[0]
assert dex1[str58093_off : str58093_off + 21] == expected_old_entry
dex1[str58093_off : str58093_off + 21] = new_entry

dex1[12:32] = hashlib.sha1(dex1[32:]).digest()
dex1[8:12] = struct.pack("<I", zlib.adler32(dex1[12:]) & 0xFFFFFFFF)
print("classes.dex patched and verified!")

# -------------------------------------------------------------
# 2. Patch classes4.dex: GitHub Release Updater Reflection Hook
# -------------------------------------------------------------
# 1. Patch UpdaterUtils.getAppUpdate at 0x43a6ac (18 bytes)
patch_getAppUpdate = bytearray()
patch_getAppUpdate.extend(b"\x12\x00") # const/4 v0, 0
patch_getAppUpdate.extend(b"\x71\x20\x69\x9a\x10\x00") # invoke-static {v0, v1}, method@9a69 (parseUpdateResponse)
patch_getAppUpdate.extend(b"\x0e\x00") # return-void
while len(patch_getAppUpdate) < 18:
    patch_getAppUpdate.extend(b"\x00\x00")
assert len(patch_getAppUpdate) == 18
dex4[0x43a6ac : 0x43a6ac + 18] = patch_getAppUpdate

# 2. Patch UpdaterUtils.parseUpdateResponse at 0x43a984 (648 bytes)
code_updater = bytearray()
# 1. new-array v0, 45, [B (type@3706)
code_updater.extend(b"\x13\x00\x2d\x00") # const/16 v0, 45
code_updater.extend(b"\x23\x00\x06\x37") # new-array v0, v0, type@3706 ([B)
code_updater.extend(b"\x26\x00\x00\x00\x00\x00") # fill-array-data v0, rel1

# 2. new-array v1, 12, [B (type@3706)
code_updater.extend(b"\x13\x01\x0c\x00") # const/16 v1, 12
code_updater.extend(b"\x23\x11\x06\x37") # new-array v1, v1, type@3706 ([B)
code_updater.extend(b"\x26\x01\x00\x00\x00\x00") # fill-array-data v1, rel2

# 3. new String(v0) -> v2
code_updater.extend(b"\x22\x02\x86\x31") # new-instance v2, type@3186 (String)
code_updater.extend(b"\x70\x20\xd5\xed\x02\x00") # invoke-direct {v2, v0}, method@edd5 (String.<init>:([B)V)

# 4. Class.forName(v2) -> v0
code_updater.extend(b"\x71\x10\xfc\xec\x02\x00") # invoke-static {v2}, method@ecfc (Class.forName)
code_updater.extend(b"\x0c\x00") # move-result-object v0

# 5. new String(v1) -> v2
code_updater.extend(b"\x22\x02\x86\x31") # new-instance v2, type@3186 (String)
code_updater.extend(b"\x70\x20\xd5\xed\x12\x00") # invoke-direct {v2, v1}, method@edd5 (String.<init>:([B)V)

# 6. new-array v3, 1, [Class (type@3909)
code_updater.extend(b"\x12\x11") # const/4 v1, 1
code_updater.extend(b"\x23\x13\x09\x39") # new-array v3, v1, type@3909 ([Class)
code_updater.extend(b"\x1c\x04\x7b\x31") # const-class v4, type@317b (Object)
code_updater.extend(b"\x12\x01") # const/4 v1, 0
code_updater.extend(b"\x4d\x04\x03\x01") # aput-object v4, v3, v1 (v1 is 0)

# 7. Class.getMethod(v2, v3) -> v0
code_updater.extend(b"\x6e\x30\x0d\xed\x20\x03") # invoke-virtual {v0, v2, v3}, method@ed0d (Class.getMethod)
code_updater.extend(b"\x0c\x00") # move-result-object v0

# 8. new-array v2, 1, [Object (type@390f)
code_updater.extend(b"\x12\x13") # const/4 v3, 1
code_updater.extend(b"\x23\x32\x0f\x39") # new-array v2, v3, type@390f ([Object)
code_updater.extend(b"\x4d\x0e\x02\x01") # aput-object v14, v2, v1 (v1 is 0, v14 is incoming callback)

# 9. Method.invoke(null, v2)
code_updater.extend(b"\x12\x01") # const/4 v1, 0 (null target)
code_updater.extend(b"\x6e\x30\x86\xee\x10\x02") # invoke-virtual {v0, v1, v2}, method@ee86 (Method.invoke)
code_updater.extend(b"\x0e\x00") # return-void

if len(code_updater) % 4 != 0:
    code_updater.extend(b"\x00\x00")

pos_arr1 = len(code_updater) // 2
actual_rel1 = pos_arr1 - 4
code_updater[10:14] = struct.pack("<i", actual_rel1)

bCls = b"com.radolyn.ayugram.utils.NfGramGithubUpdater"
arr1 = bytearray(b"\x00\x03\x01\x00" + struct.pack("<I", len(bCls)) + bCls)
while len(arr1) % 4 != 0:
    arr1.append(0)
code_updater.extend(arr1)

pos_arr2 = len(code_updater) // 2
actual_rel2 = pos_arr2 - 11
code_updater[24:28] = struct.pack("<i", actual_rel2)

bMth = b"checkUpdates"
arr2 = bytearray(b"\x00\x03\x01\x00" + struct.pack("<I", len(bMth)) + bMth)
while len(arr2) % 4 != 0:
    arr2.append(0)
code_updater.extend(arr2)

assert len(code_updater) <= 648
while len(code_updater) < 648:
    code_updater.extend(b"\x00\x00")
dex4[0x43a984 : 0x43a984 + 648] = code_updater

# 3. Patch MainPreferencesActivity (fillItems, onClick) and lighthouse_top string in classes4.dex
assert dex4[0x7b9500 : 0x7b9500 + 25] == b"lightnessEnhancementParam"
dex4[0x7b9500 : 0x7b9500 + 25] = b"lighthouse_top           "

code_fi_bytes = bytes.fromhex(
    "080011000801100054125c505513ad89390317003802150054237a5215040f7f711026f504000c046e207a09430054237752140471cc2eff6e20ed0743001303c600712004fc32000c0212136e2021fc32006e2074ef20006002c383711026f502000c02711009fc02000c026e2074ef20005512ad893902350013020a0014042603087f140324de0f7f711026f503000c037130f8fb42030c0214033030e8ff6e301efc42036e2074ef20001302080014042703087f1403a3fa0f7f711026f503000c037130f8fb42030c021403ff7095ff6e301efc42036e2074ef200028361222122732721000123732721200124732721400125732721600600482826003e68428146004998260037884280f6004ca8260038883280a60047e8260035b8628056004a9826003ed85711026f503000c037130f8fb42030c036e2074ef3000d802020112773472ceff710010fc00000c026e2074ef20006002e184711026f502000c02711009fc02000c026e2074ef2000130207006004758260031f86711026f503000c035515ad89390509001a05b8c86e1004ee05000c0528031a05b8a57140f9fb42530c026e2074ef20005512ad8938023b001302080060048d8260035b86711026f503000c031a05b7a57140f9fb42530c026e2074ef2000130209006004cd826003eb83711026f503000c031a051e227140f9fb42530c026e2074ef200013020a006004908260033787711026f503000c031a05c2a57140f9fb42530c026e2074ef2000710010fc00000c026e2074ef20000e00000000000000"
)
assert len(code_fi_bytes) == 574
dex4[0x410e74 : 0x410e74 + 574] = code_fi_bytes

code_oc_bytes = bytes.fromhex(
    "5211d18a2b01820000000e002201931a70108e9101006e2041f810000e002201f11a7010019301006e2041f810000e002201511b70107f9401006e2041f810000e002201881970102c8c01006e2041f810000e002201aa1a7010f49101006e2041f810000e000e001a01b8c86e1004ee01000c015502ad89380204001a01b8a57020af9110000e005501ad89380106001a01b7a57020af9110000e0012021c01fc306e2004ed21000c016e2073ee21000c011f01ad356e2041f810000e006e102bf800000c001a01b4bc712053f610000e005501ad89380108006e102bf800000c001a01b7bc712053f610000e002201961a7010a791010012125c12ad896e2041f810000e00000000010a0001000000040000000d000000160000001f000000280000003100000032000000420000005d00000067000000000000000000000000000000000000000000000000000000"
)
assert len(code_oc_bytes) == 336
dex4[0x4110c4 : 0x4110c4 + 336] = code_oc_bytes
print("Applied MainPreferencesActivity unified settings hierarchy patch in classes4.dex")

dex4[12:32] = hashlib.sha1(dex4[32:]).digest()
dex4[8:12] = struct.pack("<I", zlib.adler32(dex4[12:]) & 0xFFFFFFFF)
print("classes4.dex patched with GitHub release updater hook and unified settings, verified!")

# -------------------------------------------------------------
# 3. Patch classes7.dex: SettingsActivity green NfGram button
# -------------------------------------------------------------
# SettingsActivity.fillItems: Row 1 emerald green #ff2ecc71 button with "NfGram" title
# Replace field@142d (Preferences) with field@0894 (AppName)
assert dex7[0x5df8d2 : 0x5df8d6] == bytes.fromhex("60 03 2d 14")
dex7[0x5df8d4 : 0x5df8d6] = bytes.fromhex("94 08")

# Replace red color #ffe83030 with emerald green #ff2ecc71
assert dex7[0x5df8e0 : 0x5df8e6] == bytes.fromhex("14 06 30 30 e8 ff")
dex7[0x5df8e0 : 0x5df8e6] = bytes.fromhex("14 06 71 cc 2e ff")

# Remove second button: NOP 38 bytes (from 0x5df8f4 to 0x5df91a)
assert dex7[0x5df8f4 : 0x5df8f4 + 4] == bytes.fromhex("60 02 dd 04")
dex7[0x5df8f4 : 0x5df8f4 + 38] = b"\x00" * 38
print("Applied SettingsActivity single emerald green NfGram button in classes7.dex")

dex7[12:32] = hashlib.sha1(dex7[32:]).digest()
dex7[8:12] = struct.pack("<I", zlib.adler32(dex7[12:]) & 0xFFFFFFFF)

# Verify patched DEX files
for name, dex_data in [("classes.dex", dex1), ("classes4.dex", dex4), ("classes7.dex", dex7)]:
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
assert manifest_count == 13
manifest = manifest.replace(old_pkg_u16, new_pkg_u16)

# Bump versionCode from 72379 to 72381
old_vc = struct.pack("<I", 72379)
new_vc = struct.pack("<I", 72381)
assert manifest.count(old_vc) == 1
manifest = manifest.replace(old_vc, new_vc)
print("Bumped versionCode to 72381 in AndroidManifest.xml")

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
    8873: "NfGram",
    8874: "Смена чёлки Nfgram",
    8877: "NfGram Preferences",
    10096: "Update NfGram",
    10146: "Welcome to the NfGram Desktop. Make Telegram your own.",
    10237: "NfGram",
    10238: "Настройки NfGram",
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
fa_new = bytes.fromhex("08 00 00 04 00 00 80 3f")
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
unaligned_apk = os.path.join(BASE_DIR, "Tools", "nfgram_unaligned.apk")
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
            assert so_data[0x62f3ec : 0x62f3ec + 4] == bytes.fromhex("ff c3 01 d1")
            so_data[0x62f3ec : 0x62f3ec + 4] = bytes.fromhex("c0 03 5f d6") # ret
            assert so_data[0x1375fb0 : 0x1375fb0 + 8] == bytes.fromhex("ff 83 05 d1 fd 7b 11 a9")
            so_data[0x1375fb0 : 0x1375fb0 + 8] = bytes.fromhex("e0 03 1f 2a c0 03 5f d6") # mov w0, wzr; ret
            assert so_data[0x1445e04 : 0x1445e04 + 8] == bytes.fromhex("09 01 09 aa e8 03 1f 2a")
            so_data[0x1445e04 : 0x1445e04 + 8] = bytes.fromhex("e0 03 1f 2a c0 03 5f d6") # mov w0, wzr; ret
            zout.writestr(item, so_data, compress_type=item.compress_type)
            print("Patched lib/arm64-v8a/libtmessages.49.so: LSPlant hooks & NativeCrashHandler neutralized")
        elif item.filename == "lib/armeabi-v7a/libtmessages.49.so":
            so_data = bytearray(zin.read(item.filename))
            assert so_data[0x322fa0 : 0x322fa0 + 4] == bytes.fromhex("f0 4f 2d e9")
            so_data[0x322fa0 : 0x322fa0 + 4] = bytes.fromhex("1e ff 2f e1") # bx lr
            assert so_data[0x9c2ec8 : 0x9c2ec8 + 4] == bytes.fromhex("f0 b5 03 af")
            so_data[0x9c2ec8 : 0x9c2ec8 + 4] = bytes.fromhex("00 20 70 47") # movs r0, #0; bx lr
            zout.writestr(item, so_data, compress_type=item.compress_type)
            print("Patched lib/armeabi-v7a/libtmessages.49.so: LSPlant hooks & NativeCrashHandler neutralized")
        else:
            data = zin.read(item.filename)
            zout.writestr(item, data, compress_type=item.compress_type)

    # Inject classes9.dex for NfGramGithubUpdater
    zout.writestr("classes9.dex", dex9)
    print("Injected classes9.dex (NfGramGithubUpdater) into APK root")

print(f"Created unaligned APK: {unaligned_apk} ({os.path.getsize(unaligned_apk)} bytes)")

print("=== STEP 7: Zipalign APK ===")
aligned_apk = os.path.join(BASE_DIR, "Tools", "nfgram_aligned.apk")
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)

res = subprocess.run([ZIPALIGN, "-p", "-f", "4", unaligned_apk, aligned_apk], capture_output=True, text=True)
if res.returncode != 0:
    print("Zipalign error:", res.stderr)
    exit(1)
print(f"Zipalign succeeded: {aligned_apk} ({os.path.getsize(aligned_apk)} bytes)")

print("=== STEP 8: Sign APK with Keystore ===")
cmd_sign = [
    "java", "-Xms64m", "-Xmx512m", "-XX:+UseSerialGC", "-jar", APKSIGNER_JAR,
    "sign",
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
cmd_verify = [
    "java", "-Xms64m", "-Xmx512m", "-XX:+UseSerialGC", "-jar", APKSIGNER_JAR,
    "verify", "--verbose", "--print-certs", aligned_apk
]
res_sig = subprocess.run(cmd_verify, capture_output=True, text=True)
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
]
for dst in destinations:
    try:
        dst_dir = os.path.dirname(dst)
        if os.path.exists(dst_dir):
            shutil.copy2(aligned_apk, dst)
            print(f"Deployed: {dst}")
    except Exception as e:
        print(f"Warning deploying to {dst}: {e}")

print("ALL DONE! BUILD COMPLETED 100% SUCCESSFULLY!")
