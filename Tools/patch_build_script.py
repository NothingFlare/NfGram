"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

with open(r'c:\project\ayugram\Tools\build_nfgram_faceunlock.py', 'rb') as f:
    content = f.read()

# 1. Patch classes.dex stability
t1 = b'assert dex1[str56764_off : str56764_off + 21] == expected_old_entry\r\ndex1[str56764_off : str56764_off + 21] = new_entry\r\n\r\ndex1[12:32] = hashlib.sha1(dex1[32:]).digest()'
r1 = b'''assert dex1[str56764_off : str56764_off + 21] == expected_old_entry
dex1[str56764_off : str56764_off + 21] = new_entry

# Stability Patch: Disable Plugin Engine in classes.dex to prevent LSPlant ART hook execution
assert dex1[0x1ef27c : 0x1ef27c + 4] == bytes.fromhex("12 10 0f 00")
dex1[0x1ef27c : 0x1ef27c + 4] = bytes.fromhex("12 00 0f 00") # const/4 v0, 0; return v0
print("Applied Stability patch: isPluginEngineSupported set to false (prevents ART JIT crashes)")

dex1[12:32] = hashlib.sha1(dex1[32:]).digest()'''.replace(b'\n', b'\r\n')

assert t1 in content, 'Target 1 not found'
content = content.replace(t1, r1)

# 2. Patch .so files in zip packaging
t2 = b'        elif item.filename in xml_replacements:\r\n            zout.writestr(item, xml_replacements[item.filename])\r\n        else:\r\n            data = zin.read(item.filename)'
r2 = b'''        elif item.filename in xml_replacements:
            zout.writestr(item, xml_replacements[item.filename])
        elif item.filename == "lib/arm64-v8a/libtmessages.49.so":
            so_data = bytearray(zin.read(item.filename))
            assert so_data[0x11174d8 : 0x11174d8 + 8] == bytes.fromhex("ff 83 05 d1 fd 7b 11 a9")
            so_data[0x11174d8 : 0x11174d8 + 8] = bytes.fromhex("e0 03 1f 2a c0 03 5f d6") # mov w0, wzr; ret
            assert so_data[0x11f0728 : 0x11f0728 + 8] == bytes.fromhex("29 10 40 f9 e8 03 1f 2a")
            so_data[0x11f0728 : 0x11f0728 + 8] = bytes.fromhex("e0 03 1f 2a c0 03 5f d6") # mov w0, wzr; ret
            zout.writestr(item, so_data, compress_type=item.compress_type)
            print("Patched lib/arm64-v8a/libtmessages.49.so: LSPlant hooks neutralized (fixed ART JIT crash)")
        elif item.filename == "lib/armeabi-v7a/libtmessages.49.so":
            so_data = bytearray(zin.read(item.filename))
            assert so_data[0xe4bd50 : 0xe4bd50 + 4] == bytes.fromhex("f0 b5 03 af")
            so_data[0xe4bd50 : 0xe4bd50 + 4] = bytes.fromhex("00 20 70 47") # movs r0, #0; bx lr
            zout.writestr(item, so_data, compress_type=item.compress_type)
            print("Patched lib/armeabi-v7a/libtmessages.49.so: LSPlant hooks neutralized")
        else:
            data = zin.read(item.filename)'''.replace(b'\n', b'\r\n')

assert t2 in content, 'Target 2 not found'
content = content.replace(t2, r2)

with open(r'c:\project\ayugram\Tools\build_nfgram_faceunlock.py', 'wb') as f:
    f.write(content)
print('Successfully patched build_nfgram_faceunlock.py!')
