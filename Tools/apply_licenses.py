"""
/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */
"""

import os, re, subprocess

ROOT = r"C:\project\ayugram"

# 1. Get git modified files
p = subprocess.run(["git", "diff", "--ignore-space-at-eol", "--name-only"], capture_output=True, text=True, cwd=ROOT)
git_modified = set()
for line in p.stdout.splitlines():
    norm = os.path.normpath(line.strip().replace('/', '\\'))
    git_modified.add(norm)

# Untracked files that are purely NothingFlare
pure_ours = {
    os.path.normpath(r"TMessagesProj\src\main\java\org\telegram\messenger\ParallelDispatchQueue.java")
}

def clean_creator(raw):
    raw = raw.strip()
    # Remove leading/trailing copyright marks, dates, etc.
    raw = re.sub(r'^(?:\(C\)|@|\s|,)+', '', raw, flags=re.IGNORECASE)
    raw = re.sub(r'^\d{4}(?:-\d{4})?\s*', '', raw)
    raw = re.sub(r'[,\s]+\d{4}(?:-\d{4})?.*$', '', raw)
    raw = re.sub(r'\s*\.\s*$', '', raw)
    raw = raw.strip(" ,.-*")
    return raw

def get_creator(content, rel_path):
    if "com\\radolyn" in rel_path or "com/radolyn" in rel_path:
        return "Radolyn"
    
    # Try finding in existing header
    m = re.search(r"Copyright\s+(?:\(C\)\s*)?(?:@)?([^\n\*]+?)(?:,\s*\d{4}[^\n\*]*)?(?:\*/|\n|\*)", content[:800], re.IGNORECASE)
    if m:
        c = clean_creator(m.group(1))
        if c and len(c) > 2 and "licensed" not in c.lower() and "this is" not in c.lower():
            return c
    
    if "androidx" in rel_path or "com\\google" in rel_path:
        return "The Android Open Source Project"
    return "Nikolai Kudashov"

processed_count = 0
modified_count = 0
ours_count = 0
untouched_count = 0

# Process TMessagesProj/src/main/java
java_root = os.path.join(ROOT, r"TMessagesProj\src\main\java")
for dirpath, _, filenames in os.walk(java_root):
    for fn in filenames:
        if not fn.endswith((".java", ".kt")):
            continue
        
        full_path = os.path.join(dirpath, fn)
        rel_path = os.path.relpath(full_path, ROOT)
        norm_rel = os.path.normpath(rel_path)
        
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # Check if pure ours
        is_ours = norm_rel in pure_ours
        is_mod = norm_rel in git_modified
        
        # Remove existing header if any
        m = re.match(r'^\s*/\*.*?\*/\s*', content, re.DOTALL)
        if m:
            body = content[m.end():]
        else:
            body = content.lstrip()
            
        if is_ours:
            header = "/*\n * Copyright (C) 2026 NothingFlare \n *\n * Licensed under GNU GPLv3.\n */\n\n"
            ours_count += 1
        elif is_mod:
            creator = get_creator(content, rel_path)
            header = f"/*\n * Copyright (C) {creator}\n * Copyright (C) 2026 NothingFlare (Modifications)\n *\n * Licensed under GNU GPLv3.\n */\n\n"
            modified_count += 1
        else:
            creator = get_creator(content, rel_path)
            header = f"/*\n * Copyright (C) {creator}\n *\n * Licensed under GNU GPLv3.\n */\n\n"
            untouched_count += 1
            
        new_content = header + body
        with open(full_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
        processed_count += 1

print(f"Java/Kt: Processed {processed_count} files (Ours: {ours_count}, Modified: {modified_count}, Untouched: {untouched_count})")

# Process Tools/*.py
tools_root = os.path.join(ROOT, "Tools")
tools_count = 0
for fn in os.listdir(tools_root):
    if fn.endswith(".py") and fn != "apply_licenses.py":
        full_path = os.path.join(tools_root, fn)
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        # Strip existing docstring/header if starts with license
        m = re.match(r'^\s*("""/\*.*?\*/\s*"""|/\*.*?\*/|#\s*Copyright.*?GNU GPLv3\.\s*#)\s*', content, re.DOTALL)
        if m:
            body = content[m.end():]
        else:
            body = content
            
        py_header = '"""\n/*\n * Copyright (C) 2026 NothingFlare \n *\n * Licensed under GNU GPLv3.\n */\n"""\n\n'
        with open(full_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(py_header + body)
        tools_count += 1

print(f"Tools: Processed {tools_count} Python scripts")

# Process Gradle files
gradle_files = [
    r"build.gradle",
    r"settings.gradle",
    r"TMessagesProj\build.gradle",
    r"TMessagesProj_App\build.gradle",
    r"TMessagesProj_AppStandalone\build.gradle",
    r"TMessagesProj_AppHockeyApp\build.gradle",
    r"TMessagesProj_AppHuawei\build.gradle"
]

for g_rel in gradle_files:
    g_full = os.path.join(ROOT, g_rel)
    if os.path.exists(g_full):
        with open(g_full, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        m = re.match(r'^\s*/\*.*?\*/\s*', content, re.DOTALL)
        if m:
            body = content[m.end():]
        else:
            body = content.lstrip()
        header = "/*\n * Copyright (C) Nikolai Kudashov\n * Copyright (C) 2026 NothingFlare (Modifications)\n *\n * Licensed under GNU GPLv3.\n */\n\n"
        with open(g_full, "w", encoding="utf-8", newline="\n") as f:
            f.write(header + body)
        print(f"Gradle: Processed {g_rel}")
