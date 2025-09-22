import os
import shutil

# Daftar folder cache yang akan dibersihkan
folders = [
    os.path.expanduser("~/.cache"),
    os.path.expanduser("~/.pip/cache"),
    os.path.expanduser("~/.local/share/pip"),
]

def get_size(start_path="."):
    """Hitung ukuran folder/file dalam byte"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except FileNotFoundError:
                pass
    return total_size

def format_size(size_bytes):
    """Format ukuran (KB, MB, GB)"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

print("⚡ Script Pembersih Cache Termux ⚡\n")
print("Folder cache ditemukan:")

total_cache = 0
for f in folders:
    if os.path.exists(f):
        size = get_size(f)
        total_cache += size
        print(f" - {f} → {format_size(size)}")
    else:
        print(f" - {f} → (tidak ada)")

print(f"\n📦 Total cache: {format_size(total_cache)}")

print("\nApakah kamu yakin ingin menghapus cache ini? (y/n)")
choice = input("> ").lower()

if choice == "y":
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
            print(f"✅ {folder} dibersihkan")
    print("\n🎉 Semua cache berhasil dibersihkan!")
else:
    print("\n❌ Operasi dibatalkan, tidak ada yang dihapus.")
