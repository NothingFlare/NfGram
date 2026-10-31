"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

import zipfile, struct

APK = r"C:\project\ayugram\Tools\nfgram_fixed_aligned.apk"

def search_dex(dex_name):
    with zipfile.ZipFile(APK, "r") as z:
        dex = z.read(dex_name)
    string_ids_off = struct.unpack("<I", dex[60:64])[0]
    type_ids_off = struct.unpack("<I", dex[68:72])[0]
    method_ids_off = struct.unpack("<I", dex[92:96])[0]
    method_ids_size = struct.unpack("<I", dex[88:92])[0]

    def get_str(s_idx):
        off = struct.unpack("<I", dex[string_ids_off + s_idx*4 : string_ids_off + (s_idx+1)*4])[0]
        p = off
        while dex[p] & 0x80: p += 1
        p += 1
        end = dex.find(b"\x00", p)
        return dex[p:end].decode("utf-8", errors="ignore")

    def get_type_name(t_idx):
        str_idx = struct.unpack("<I", dex[type_ids_off + t_idx*4 : type_ids_off + (t_idx+1)*4])[0]
        return get_str(str_idx)

    def get_meth(m_idx):
        c_idx, p_idx, n_idx = struct.unpack("<HHI", dex[method_ids_off + m_idx*8 : method_ids_off + (m_idx+1)*8])
        return f"{get_type_name(c_idx)}->{get_str(n_idx)}"

    print(f"=== {dex_name} methods ===")
    for m_idx in range(method_ids_size):
        m = get_meth(m_idx)
        if any(k in m for k in ["SharedPreferences", "getGlobalMainSettings", "mainconfig"]):
            print(f"  #{m_idx}: {m}")

search_dex("classes6.dex")
search_dex("classes7.dex")
