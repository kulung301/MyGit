#!/data/data/com.termux/files/usr/bin/env python3
import os
import subprocess
from datetime import datetime

# Folder repo
REPO_DIR = os.path.expanduser("~/MyGit")

# Masuk ke folder repo
if not os.path.exists(REPO_DIR):
    print(f"Folder {REPO_DIR} tidak ditemukan!")
    exit(1)

os.chdir(REPO_DIR)

# Tarik update terbaru dari GitHub (opsional)
subprocess.run(["git", "pull", "origin", "main"])

# Tambahkan semua file
subprocess.run(["git", "add", "."])

# Commit dengan pesan timestamp
commit_message = f"Auto commit {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
subprocess.run(["git", "commit", "-m", commit_message])

# Push ke GitHub
subprocess.run(["git", "push", "origin", "main"])

print(f"✅ Semua perubahan di {REPO_DIR} sudah di-push ke GitHub")
