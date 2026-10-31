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

VANILLA_APK = r"c:\Users\styuk\Downloads\AyuGram Desktop\vanilla-AyuGram-full-20261005.apk"
OUTPUT_APK_DOWNLOADS = r"c:\Users\styuk\Downloads\AyuGram Desktop\AyuGram-12.10.6-universal.apk"
OUTPUT_APK_PROJECT = r"C:\project\ayugram\AyuGram-12.10.6-universal.apk"
KEYSTORE = r"C:\project\ayugram\TMessagesProj\config\release.keystore"
ZIPALIGN = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\zipalign.exe"
APKSIGNER = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\apksigner.bat"
AAPT = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\aapt.exe"
DEXDUMP = r"C:\Users\styuk\AppData\Local\Android\Sdk\build-tools\34.0.0\dexdump.exe"

print("--- Step 1: Read and Patch classes.dex ---")
with zipfile.ZipFile(VANILLA_APK, "r") as z:
    dex_data = bytearray(z.read("classes.dex"))

seq1 = b"\x52\xa3\x87\x31\x35\x23\x09\x00\xb0\x23\x59\xa3\x87\x31"
seq2 = b"\x52\xa3\x86\x31\x35\x23\x09\x00\xb0\x23\x59\xa3\x86\x31"

assert dex_data.count(seq1) == 1, f"seq1 count is {dex_data.count(seq1)}"
assert dex_data.count(seq2) == 1, f"seq2 count is {dex_data.count(seq2)}"

idx1 = dex_data.find(seq1)
idx2 = dex_data.find(seq2)
print(f"Found seq1 at {hex(idx1)}, seq2 at {hex(idx2)}")

# Replace 'if-ge v3, v2, +9' (35 23 09 00) with 'nop; nop;' (00 00 00 00)
dex_data[idx1+4 : idx1+8] = b"\x00\x00\x00\x00"
dex_data[idx2+4 : idx2+8] = b"\x00\x00\x00\x00"

# Recompute SHA-1 (offset 12..32) and Adler32 (offset 8..12)
dex_data[12:32] = hashlib.sha1(dex_data[32:]).digest()
dex_data[8:12] = struct.pack("<I", zlib.adler32(dex_data[12:]) & 0xFFFFFFFF)

patched_dex_path = "Tools/classes_patched.dex"
with open(patched_dex_path, "wb") as f:
    f.write(dex_data)
print(f"Saved {patched_dex_path} ({len(dex_data)} bytes)")

print("--- Step 2: Verification of checksums ---")
assert zlib.adler32(dex_data[12:]) & 0xFFFFFFFF == struct.unpack("<I", dex_data[8:12])[0]
assert hashlib.sha1(dex_data[32:]).digest() == dex_data[12:32]
print("Checksums verified!")


print("--- Step 3: Repack APK ---")
unaligned_apk = "Tools/ayugram_parallel_unaligned.apk"
if os.path.exists(unaligned_apk):
    os.remove(unaligned_apk)

with zipfile.ZipFile(VANILLA_APK, "r") as zin, zipfile.ZipFile(unaligned_apk, "w") as zout:
    for item in zin.infolist():
        # Skip old signatures and classes.dex
        if item.filename.startswith("META-INF/") and (item.filename.endswith(".SF") or item.filename.endswith(".RSA") or item.filename.endswith(".MF")):
            continue
        if item.filename == "classes.dex":
            print("Writing patched classes.dex...")
            zout.writestr(item, dex_data)
        else:
            # Preserve compression type
            data = zin.read(item.filename)
            zout.writestr(item, data, compress_type=item.compress_type)

print(f"Created unaligned APK: {unaligned_apk} ({os.path.getsize(unaligned_apk)} bytes)")

print("--- Step 4: Zipalign APK (page alignment 4) ---")
aligned_apk = "Tools/ayugram_parallel_aligned.apk"
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)

cmd_zipalign = [ZIPALIGN, "-p", "-f", "4", unaligned_apk, aligned_apk]
res = subprocess.run(cmd_zipalign, capture_output=True, text=True)
if res.returncode != 0:
    print("Zipalign error:", res.stderr)
    exit(1)
print(f"Zipalign succeeded: {aligned_apk} ({os.path.getsize(aligned_apk)} bytes)")

print("--- Step 5: Sign APK with apksigner ---")
cmd_sign = [
    APKSIGNER, "sign",
    "--ks", KEYSTORE,
    "--ks-pass", "pass:android",
    "--key-pass", "pass:android",
    "--ks-key-alias", "androidkey",
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

print("--- Step 6: Verify Signature ---")
res = subprocess.run([APKSIGNER, "verify", "--verbose", aligned_apk], capture_output=True, text=True)
print("Apksigner verify output:")
print(res.stdout)
assert "Verified using v2 scheme (APK Signature Scheme v2): true" in res.stdout, "v2 verification failed"

print("--- Step 7: Verify Badging with aapt ---")
res = subprocess.run([AAPT, "dump", "badging", aligned_apk], capture_output=True, text=True)
lines = [l for l in res.stdout.splitlines() if "package:" in l or "application-label:" in l or "application-icon" in l]
for l in lines[:10]:
    print("  ", l)

print("--- Step 8: Deploy final APK ---")
shutil.copy2(aligned_apk, OUTPUT_APK_DOWNLOADS)
shutil.copy2(aligned_apk, OUTPUT_APK_PROJECT)
print(f"Deployed to: {OUTPUT_APK_DOWNLOADS} ({os.path.getsize(OUTPUT_APK_DOWNLOADS)} bytes)")
print(f"Deployed to: {OUTPUT_APK_PROJECT} ({os.path.getsize(OUTPUT_APK_PROJECT)} bytes)")
print("ALL DONE SUCCESSFULLY!")
