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

apk = r"c:\Users\styuk\Downloads\AyuGram Desktop\vanilla-AyuGram-full-20261005.apk"
with zipfile.ZipFile(apk, "r") as z:
    dex = z.read("classes.dex")

# Let's find the sequence around 4eb87e:
# 52 a3 87 31  (iget v3, v10, currentUploadSmallOperationsCount)
# 35 23 09 00  (if-ge v3, v2, +0009)
# b0 23        (add-int/2addr v3, v2)
# 59 a3 87 31  (iput v3, v10, currentUploadSmallOperationsCount)

seq1 = b"\x52\xa3\x87\x31\x35\x23\x09\x00\xb0\x23\x59\xa3\x87\x31"
print("seq1 count:", dex.count(seq1))
if dex.count(seq1) == 1:
    off1 = dex.find(seq1)
    print("seq1 offset:", hex(off1))

# seq2:
# 52 a3 86 31  (iget v3, v10, currentUploadOperationsCount)
# 35 23 09 00  (if-ge v3, v2, +0009)
# b0 23        (add-int/2addr v3, v2)
# 59 a3 86 31  (iput v3, v10, currentUploadOperationsCount)

seq2 = b"\x52\xa3\x86\x31\x35\x23\x09\x00\xb0\x23\x59\xa3\x86\x31"
print("seq2 count:", dex.count(seq2))
if dex.count(seq2) == 1:
    off2 = dex.find(seq2)
    print("seq2 offset:", hex(off2))
