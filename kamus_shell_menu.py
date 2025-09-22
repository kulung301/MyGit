# kamus_linux.py

commands = {
    # Dasar Navigasi & File
    "ls": "Menampilkan daftar file/folder di direktori.",
    "ls -l": "Menampilkan daftar file/folder dengan detail (izin, ukuran, tanggal).",
    "ls -a": "Menampilkan semua file termasuk yang tersembunyi (diawali titik).",
    "cd": "Pindah direktori (contoh: cd /home/user).",
    "pwd": "Menampilkan direktori saat ini.",
    "cp": "Menyalin file atau folder (contoh: cp file1.txt file2.txt).",
    "mv": "Memindahkan/rename file atau folder (contoh: mv lama.txt baru.txt).",
    "rm": "Menghapus file (contoh: rm file.txt).",
    "rm -f": "Paksa hapus file tanpa konfirmasi.",
    "rm -r": "Menghapus folder beserta isinya.",
    "mkdir": "Membuat direktori baru (contoh: mkdir data).",
    "rmdir": "Menghapus direktori kosong.",
    "touch": "Membuat file kosong baru (contoh: touch baru.txt).",
    "cat": "Menampilkan isi file (contoh: cat file.txt).",
    "nano": "Membuka editor teks Nano untuk edit file.",
    "chmod": "Mengubah izin file (contoh: chmod 755 file.sh).",
    "chown": "Mengubah pemilik file (contoh: chown user:group file.txt).",
    "clear": "Membersihkan layar terminal.",
    "exit": "Keluar dari terminal/ sesi.",

    # Jaringan
    "ping": "Menguji koneksi ke host/domain (contoh: ping google.com).",
    "curl": "Mengirim permintaan HTTP (contoh: curl https://example.com).",
    "wget": "Mengunduh file dari internet (contoh: wget file.zip).",
    "ifconfig": "Menampilkan konfigurasi jaringan (sering diganti ip addr).",
    "ip addr": "Menampilkan alamat IP perangkat.",
    "netstat": "Menampilkan koneksi jaringan yang aktif.",
    "ss": "Alat modern untuk melihat koneksi jaringan (pengganti netstat).",
    "scp": "Menyalin file antar server (contoh: scp file.txt user@host:/path).",
    "ssh": "Menghubungkan ke server via SSH (contoh: ssh user@host).",
    "traceroute": "Menunjukkan jalur koneksi ke host (hop demi hop).",
    "nslookup": "Mencari IP dari domain (contoh: nslookup google.com).",
    "dig": "Mengecek DNS lebih detail (contoh: dig openai.com).",
}

GREEN = "\033[92m"
RESET = "\033[0m"

print("📖 Kamus Perintah Dasar Linux + Networking\n")
for cmd, desc in commands.items():
    print(f"{cmd:<12} {GREEN}{desc}{RESET}")
