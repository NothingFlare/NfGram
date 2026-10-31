"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

import zipfile, struct

with zipfile.ZipFile('nfgram_faceunlock_aligned.apk', 'r') as z: dex = z.read('classes.dex')

string_ids_off = struct.unpack('<I', dex[60:64])[0]
type_ids_off = struct.unpack('<I', dex[68:72])[0]
field_ids_off = struct.unpack('<I', dex[84:88])[0]
field_ids_size = struct.unpack('<I', dex[80:84])[0]

def get_str(s_idx):
    off = struct.unpack('<I', dex[string_ids_off + s_idx*4 : string_ids_off + (s_idx+1)*4])[0]
    p = off
    while dex[p] & 0x80: p += 1
    p += 1
    end = dex.find(b'\x00', p)
    return dex[p:end].decode('utf-8', errors='ignore')

def get_type_name(t_idx):
    str_idx = struct.unpack('<I', dex[type_ids_off + t_idx*4 : type_ids_off + t_idx*4 + 4])[0]
    return get_str(str_idx)

fields = []
for i in range(field_ids_size):
    c_idx, t_idx, n_idx = struct.unpack('<HHI', dex[field_ids_off + i*8 : field_ids_off + (i+1)*8])
    if get_type_name(c_idx) == 'Lorg/telegram/messenger/SharedConfig;':
        fields.append((i, get_str(n_idx), get_type_name(t_idx)))

print(f'Total SharedConfig fields: {len(fields)}')
for idx, name, ftype in sorted(fields, key=lambda x: x[1]):
    print(f'  #{idx}: {name} ({ftype})')
