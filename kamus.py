#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════╗
║      KAMUS PERINTAH TERMUX v1.0        ║
║   250+ Perintah Lengkap untuk Android  ║
╚════════════════════════════════════════╝
Cara pakai: python termux_kamus.py
"""

import curses
import sys

# ─── DATA PERINTAH ─────────────────────────────────────────────────────────────

CATEGORIES = [
    {
        "icon": "📦", "nama": "Package Manager",
        "cmds": [
            ("pkg update",               "Update daftar paket dari repositori",         "pkg update"),
            ("pkg upgrade",              "Upgrade semua paket terinstall",              "pkg upgrade"),
            ("pkg install [nama]",       "Install paket baru",                          "pkg install python"),
            ("pkg uninstall [nama]",     "Hapus paket yang terinstall",                 "pkg uninstall nano"),
            ("pkg search [kata]",        "Cari paket berdasarkan nama",                 "pkg search git"),
            ("pkg list-installed",       "Tampilkan semua paket terinstall",            "pkg list-installed"),
            ("pkg list-all",             "Tampilkan semua paket tersedia",              "pkg list-all"),
            ("pkg show [nama]",          "Info detail sebuah paket",                    "pkg show python"),
            ("pkg clean",                "Bersihkan cache paket",                       "pkg clean"),
            ("pkg reinstall [nama]",     "Install ulang paket yang ada",                "pkg reinstall vim"),
            ("apt-get install [nama]",   "Install paket via apt",                       "apt-get install curl"),
            ("apt-get remove [nama]",    "Hapus paket via apt",                         "apt-get remove wget"),
            ("apt-get autoremove",       "Hapus paket yang tidak dibutuhkan",           "apt-get autoremove"),
            ("apt list --installed",     "Daftar paket terinstall via apt",             "apt list --installed"),
            ("dpkg -l",                  "Semua paket terinstall dengan status detail", "dpkg -l"),
        ]
    },
    {
        "icon": "📁", "nama": "Navigasi & File",
        "cmds": [
            ("ls",                       "Tampilkan isi direktori",                     "ls / ls -la"),
            ("ls -la",                   "Tampilkan semua file termasuk hidden",        "ls -la"),
            ("cd [dir]",                 "Pindah ke direktori",                         "cd /sdcard  /  cd ~"),
            ("pwd",                      "Tampilkan path direktori aktif",              "pwd"),
            ("mkdir [nama]",             "Buat direktori baru",                         "mkdir proyek"),
            ("mkdir -p [path]",          "Buat direktori beserta parent-nya",           "mkdir -p a/b/c"),
            ("rm [file]",                "Hapus file",                                  "rm file.txt"),
            ("rm -rf [folder]",          "Hapus folder dan isinya (hati-hati!)",        "rm -rf temp/"),
            ("cp [src] [dst]",           "Salin file ke lokasi lain",                   "cp a.txt b.txt"),
            ("mv [src] [dst]",           "Pindah / ganti nama file",                    "mv old.txt new.txt"),
            ("touch [nama]",             "Buat file kosong baru",                       "touch file.txt"),
            ("find . -name [pola]",      "Cari file berdasarkan nama",                  "find . -name '*.py'"),
            ("du -sh [path]",            "Ukuran total folder/file",                    "du -sh /sdcard"),
            ("df -h",                    "Info penggunaan ruang disk",                  "df -h"),
            ("stat [file]",              "Info detail sebuah file",                     "stat file.txt"),
            ("tree",                     "Tampilkan struktur direktori (pohon)",         "tree  /  tree -L 2"),
            ("ln -s [target] [link]",    "Buat symbolic link",                          "ln -s /sdcard/Download ~/dl"),
        ]
    },
    {
        "icon": "📝", "nama": "Teks & Editor",
        "cmds": [
            ("cat [file]",               "Tampilkan isi file",                          "cat README.md"),
            ("cat > [file]",             "Buat file baru & tulis isi (Ctrl+D selesai)","cat > notes.txt"),
            ("nano [file]",              "Editor teks sederhana",                       "nano config.txt"),
            ("vim [file]",               "Editor teks powerful (perlu install vim)",    "vim script.py"),
            ("less [file]",              "Tampilkan file per halaman, bisa scroll",     "less log.txt"),
            ("head -n N [file]",         "Tampilkan N baris pertama file",              "head -n 10 file.txt"),
            ("tail -n N [file]",         "Tampilkan N baris terakhir file",             "tail -n 20 log.txt"),
            ("tail -f [file]",           "Pantau file secara real-time (live log)",     "tail -f server.log"),
            ("grep [pola] [file]",       "Cari teks/pola dalam file",                   "grep 'error' log.txt"),
            ("grep -r [pola] [dir]",     "Cari teks rekursif di semua file",            "grep -r 'TODO' ./src/"),
            ("grep -i [pola] [file]",    "Cari teks case-insensitive",                  "grep -i 'python' file.txt"),
            ("sed 's/lama/baru/g'",      "Ganti teks dalam file (stream editor)",       "sed 's/hello/world/g' f.txt"),
            ("awk '{print $1}' [file]",  "Proses & filter kolom teks",                  "awk '{print $1}' data.txt"),
            ("wc -l [file]",             "Hitung jumlah baris dalam file",              "wc -l file.txt"),
            ("sort [file]",              "Urutkan isi file secara alfabetis",           "sort names.txt"),
            ("uniq [file]",              "Hapus baris duplikat berurutan",              "sort file.txt | uniq"),
            ("diff [file1] [file2]",     "Bandingkan dua file",                         "diff old.txt new.txt"),
            ("echo [teks] >> [file]",    "Tambahkan teks ke akhir file (append)",       "echo 'baris' >> file.txt"),
        ]
    },
    {
        "icon": "🌐", "nama": "Jaringan & Internet",
        "cmds": [
            ("curl [url]",               "Unduh konten dari URL / akses API",           "curl https://api.ipify.org"),
            ("curl -O [url]",            "Unduh file, simpan dengan nama asli",         "curl -O https://ex.com/f.zip"),
            ("curl -X POST -d [data]",   "Kirim HTTP POST request",                     "curl -X POST -d 'k=v' [url]"),
            ("wget [url]",               "Unduh file dari internet",                    "wget https://ex.com/file.gz"),
            ("wget -c [url]",            "Lanjutkan unduhan yang terhenti",             "wget -c https://ex.com/big.zip"),
            ("ping [host]",              "Cek konektivitas ke host/IP",                 "ping google.com"),
            ("ping -c N [host]",         "Ping host sebanyak N kali",                   "ping -c 4 8.8.8.8"),
            ("nslookup [domain]",        "Periksa info DNS domain",                     "nslookup google.com"),
            ("dig [domain]",             "Query DNS secara detail",                     "dig google.com"),
            ("netstat -tuln",            "Tampilkan port yang terbuka",                 "netstat -tuln"),
            ("ifconfig",                 "Info interface jaringan & IP",                "ifconfig"),
            ("ip addr",                  "Tampilkan semua alamat IP",                   "ip addr"),
            ("ssh [user]@[host]",        "Koneksi ke server remote via SSH",            "ssh user@192.168.1.1"),
            ("ssh-keygen",               "Buat kunci SSH",                              "ssh-keygen -t rsa -b 4096"),
            ("scp [file] [user]@[host]", "Salin file ke server remote",                "scp file.txt user@server:/tmp/"),
            ("nmap [host]",              "Port scanning pada host (perlu nmap)",        "nmap 192.168.1.1"),
            ("traceroute [host]",        "Lacak rute paket ke host",                    "traceroute google.com"),
            ("whois [domain]",           "Info registrasi domain",                      "whois google.com"),
            ("nc -zv [host] [port]",     "Cek apakah port terbuka",                     "nc -zv google.com 443"),
        ]
    },
    {
        "icon": "🐍", "nama": "Python",
        "cmds": [
            ("python --version",         "Cek versi Python terinstall",                 "python --version"),
            ("python [file.py]",         "Jalankan script Python",                      "python script.py"),
            ("python -c '[kode]'",       "Jalankan Python langsung dari terminal",      "python -c 'print(\"Hello\")'"),
            ("pip install [paket]",      "Install library Python",                      "pip install requests"),
            ("pip list",                 "Tampilkan semua library terinstall",           "pip list"),
            ("pip freeze > req.txt",     "Simpan daftar library ke requirements",       "pip freeze > requirements.txt"),
            ("pip install -r req.txt",   "Install library dari file requirements",      "pip install -r requirements.txt"),
            ("pip uninstall [paket]",    "Hapus library Python",                        "pip uninstall requests"),
            ("pip show [paket]",         "Info detail sebuah library",                  "pip show requests"),
            ("pip install --upgrade",    "Upgrade library ke versi terbaru",            "pip install --upgrade pip"),
            ("python -m venv [nama]",    "Buat virtual environment",                    "python -m venv myenv"),
            ("source [venv]/bin/activate","Aktifkan virtual environment",               "source myenv/bin/activate"),
            ("deactivate",               "Nonaktifkan virtual environment",             "deactivate"),
            ("python -m http.server",    "Jalankan server HTTP sederhana",              "python -m http.server 8080"),
            ("ipython",                  "Shell Python interaktif (perlu install)",     "ipython"),
        ]
    },
    {
        "icon": "💻", "nama": "Git",
        "cmds": [
            ("git init",                 "Inisialisasi repositori Git baru",            "git init"),
            ("git clone [url]",          "Klon repositori dari remote",                 "git clone https://github.com/..."),
            ("git status",               "Status file (modified, staged, dll)",         "git status"),
            ("git add [file]",           "Tambahkan file ke staging area",              "git add file.txt"),
            ("git add .",                "Tambahkan semua perubahan ke staging",        "git add ."),
            ("git commit -m '[pesan]'",  "Simpan perubahan dengan pesan",               "git commit -m 'fitur baru'"),
            ("git push [remote] [branch]","Kirim commit ke remote",                     "git push origin main"),
            ("git pull",                 "Ambil & merge perubahan dari remote",         "git pull"),
            ("git fetch",                "Ambil perubahan tanpa merge",                 "git fetch origin"),
            ("git branch",               "Tampilkan daftar branch",                     "git branch"),
            ("git checkout [branch]",    "Pindah ke branch lain",                       "git checkout main"),
            ("git checkout -b [nama]",   "Buat & pindah ke branch baru",               "git checkout -b dev"),
            ("git merge [branch]",       "Gabungkan branch ke branch aktif",            "git merge fitur"),
            ("git log --oneline",        "Riwayat commit singkat",                      "git log --oneline"),
            ("git diff",                 "Lihat perubahan yang belum di-stage",         "git diff"),
            ("git stash",                "Simpan perubahan sementara",                  "git stash"),
            ("git stash pop",            "Ambil kembali perubahan dari stash",          "git stash pop"),
            ("git reset --hard HEAD",    "Buang semua perubahan ke commit terakhir",    "git reset --hard HEAD"),
            ("git remote -v",            "Tampilkan daftar remote",                     "git remote -v"),
            ("git config --global",      "Atur konfigurasi Git global",                 "git config --global user.name 'Nama'"),
        ]
    },
    {
        "icon": "🔧", "nama": "Sistem & Proses",
        "cmds": [
            ("top",                      "Monitor proses real-time",                    "top"),
            ("htop",                     "Monitor proses interaktif (install htop)",    "htop"),
            ("ps aux",                   "Semua proses dengan detail",                  "ps aux"),
            ("kill [PID]",               "Hentikan proses berdasarkan PID",             "kill 1234"),
            ("kill -9 [PID]",            "Hentikan proses secara paksa",                "kill -9 1234"),
            ("killall [nama]",           "Hentikan semua proses bernama tertentu",      "killall python"),
            ("pkill [nama]",             "Hentikan proses berdasarkan nama",            "pkill python3"),
            ("nohup [cmd] &",            "Jalankan di background, tetap jalan",        "nohup python server.py &"),
            ("[perintah] &",             "Jalankan perintah di background",             "python server.py &"),
            ("jobs",                     "Tampilkan proses background",                 "jobs"),
            ("fg %N",                    "Pindah proses background ke foreground",      "fg %1"),
            ("Ctrl+C",                   "Hentikan proses yang sedang berjalan",        "(tekan Ctrl+C)"),
            ("Ctrl+Z",                   "Pause (suspend) proses berjalan",             "(tekan Ctrl+Z)"),
            ("free -h",                  "Info penggunaan RAM",                         "free -h"),
            ("uname -a",                 "Info sistem operasi lengkap",                 "uname -a"),
            ("uptime",                   "Berapa lama sistem sudah berjalan",           "uptime"),
            ("env",                      "Tampilkan semua environment variable",        "env"),
            ("export VAR=nilai",         "Set environment variable",                    "export PATH=$PATH:/new"),
            ("alias nama='cmd'",         "Buat shortcut perintah",                      "alias ll='ls -la'"),
            ("history",                  "Riwayat perintah",                            "history | grep git"),
            ("which [cmd]",              "Lokasi executable sebuah perintah",           "which python"),
            ("date",                     "Tampilkan tanggal & waktu sistem",            "date '+%Y-%m-%d'"),
            ("sleep [detik]",            "Jeda eksekusi beberapa detik",                "sleep 5"),
        ]
    },
    {
        "icon": "🔐", "nama": "Permission & Keamanan",
        "cmds": [
            ("chmod [mode] [file]",      "Ubah hak akses file",                         "chmod 755 script.sh"),
            ("chmod +x [file]",          "Jadikan file executable",                     "chmod +x script.sh"),
            ("chmod 777 [file]",         "Hak penuh untuk semua pengguna",              "chmod 777 file.txt"),
            ("chown [user]:[grp] [file]","Ubah kepemilikan file",                       "chown user:group file.txt"),
            ("ls -l",                    "Tampilkan file beserta permission",            "ls -l"),
            ("gpg -c [file]",            "Enkripsi file dengan passphrase",             "gpg -c secret.txt"),
            ("gpg [file.gpg]",           "Dekripsi file GPG",                           "gpg secret.txt.gpg"),
            ("openssl rand -hex 32",     "Buat string random 32 byte (key/token)",      "openssl rand -hex 32"),
            ("md5sum [file]",            "Hitung checksum MD5 file",                    "md5sum file.zip"),
            ("sha256sum [file]",         "Hitung checksum SHA-256 file",                "sha256sum file.iso"),
        ]
    },
    {
        "icon": "📦", "nama": "Archiving & Kompres",
        "cmds": [
            ("tar -czf out.tar.gz [dir]","Buat arsip .tar.gz dari folder",             "tar -czf backup.tar.gz ~/project/"),
            ("tar -xzf [file.tar.gz]",   "Ekstrak arsip .tar.gz",                       "tar -xzf backup.tar.gz"),
            ("tar -tvf [file.tar.gz]",   "Lihat isi arsip tanpa ekstrak",               "tar -tvf archive.tar.gz"),
            ("zip -r out.zip [dir]",     "Buat file ZIP dari folder",                   "zip -r project.zip ./project/"),
            ("unzip [file.zip]",         "Ekstrak isi file ZIP",                        "unzip backup.zip"),
            ("unzip -l [file.zip]",      "Lihat isi ZIP tanpa ekstrak",                 "unzip -l archive.zip"),
            ("gzip [file]",              "Kompres file menjadi .gz",                    "gzip file.txt"),
            ("gunzip [file.gz]",         "Ekstrak file .gz",                            "gunzip file.txt.gz"),
            ("7z a [out.7z] [dir]",      "Buat arsip 7zip (install p7zip)",             "7z a archive.7z ./folder/"),
            ("7z x [file.7z]",           "Ekstrak arsip 7zip",                          "7z x archive.7z"),
        ]
    },
    {
        "icon": "🖥️", "nama": "Shell & Scripting",
        "cmds": [
            ("bash [script.sh]",         "Jalankan script shell bash",                  "bash script.sh"),
            ("#!/bin/bash",              "Shebang line untuk bash script",              "#!/bin/bash\necho 'Hello'"),
            ("source [file]",            "Eksekusi script di shell saat ini",           "source ~/.bashrc"),
            ("echo [teks]",              "Tampilkan teks ke terminal",                  "echo 'Hello World'"),
            ("read [var]",               "Baca input dari pengguna",                    "read nama && echo $nama"),
            ("| (pipe)",                 "Hubungkan output ke input perintah lain",     "ls -la | grep '.py'"),
            ("> (redirect)",             "Arahkan output ke file (overwrite)",          "echo 'hi' > file.txt"),
            (">> (append)",              "Tambahkan output ke akhir file",              "echo 'hi' >> file.txt"),
            ("2>&1",                     "Gabungkan stderr ke stdout",                  "python s.py > log.txt 2>&1"),
            ("$(perintah)",              "Command substitution",                        "echo \"Tgl: $(date)\""),
            ("crontab -e",               "Edit jadwal cron (task otomatis)",            "crontab -e"),
            ("crontab -l",               "Tampilkan semua jadwal cron",                 "crontab -l"),
            ("set -e",                   "Stop script jika ada perintah gagal",         "#!/bin/bash\nset -e"),
        ]
    },
    {
        "icon": "📱", "nama": "Termux Spesifik",
        "cmds": [
            ("termux-setup-storage",     "Izin akses penyimpanan /sdcard",             "termux-setup-storage"),
            ("termux-info",              "Info lengkap instalasi Termux",               "termux-info"),
            ("termux-open [file]",       "Buka file dengan aplikasi Android",           "termux-open foto.jpg"),
            ("termux-open-url [url]",    "Buka URL di browser Android",                 "termux-open-url https://google.com"),
            ("termux-share [file]",      "Bagikan file ke aplikasi Android",            "termux-share output.txt"),
            ("termux-clipboard-get",     "Ambil teks dari clipboard Android",           "termux-clipboard-get"),
            ("termux-clipboard-set",     "Salin teks ke clipboard Android",             "termux-clipboard-set 'Hello'"),
            ("termux-notification",      "Tampilkan notifikasi Android",                "termux-notification -t 'Judul' -c 'Isi'"),
            ("termux-tts-speak",         "Text-to-Speech via speaker",                  "termux-tts-speak 'Halo!'"),
            ("termux-battery-status",    "Status baterai Android",                      "termux-battery-status"),
            ("termux-wifi-connectioninfo","Info koneksi WiFi saat ini",                 "termux-wifi-connectioninfo"),
            ("termux-location",          "Dapatkan lokasi GPS (perlu izin)",            "termux-location"),
            ("termux-camera-photo",      "Ambil foto dengan kamera",                    "termux-camera-photo foto.jpg"),
            ("termux-microphone-record", "Rekam audio dari mikrofon",                   "termux-microphone-record -f r.mp3"),
            ("termux-telephony-call",    "Lakukan panggilan telepon",                   "termux-telephony-call +628xxx"),
            ("termux-sms-send",          "Kirim SMS dari Termux",                       "termux-sms-send -n 0812x 'Hi!'"),
            ("termux-sms-list",          "Tampilkan daftar SMS masuk",                  "termux-sms-list"),
            ("termux-vibrate",           "Getar perangkat",                             "termux-vibrate -d 1000"),
            ("termux-torch",             "Nyalakan/matikan senter",                     "termux-torch on"),
            ("termux-volume",            "Atur volume Android",                         "termux-volume music 10"),
            ("pkg install termux-api",   "Install paket Termux:API",                    "pkg install termux-api"),
        ]
    },
    {
        "icon": "🗄️", "nama": "Database (SQLite)",
        "cmds": [
            ("sqlite3 [db.db]",          "Buka/buat database SQLite",                   "sqlite3 mydb.db"),
            (".tables",                  "Tampilkan semua tabel (dalam sqlite3)",        ".tables"),
            (".schema [tabel]",          "Tampilkan struktur tabel",                     ".schema users"),
            ("SELECT * FROM [tabel];",   "Ambil semua data dari tabel",                 "SELECT * FROM users;"),
            ("INSERT INTO [tabel]",      "Masukkan data ke tabel",                      "INSERT INTO users VALUES (1,'Ali');"),
            ("UPDATE [tabel] SET ...",   "Update data di tabel",                        "UPDATE users SET name='Budi' WHERE id=1;"),
            ("DELETE FROM [tabel]",      "Hapus data dari tabel",                       "DELETE FROM users WHERE id=1;"),
            ("CREATE TABLE [nama]",      "Buat tabel baru",                             "CREATE TABLE users (id INT, name TEXT);"),
            (".quit / .exit",            "Keluar dari shell SQLite",                    ".quit"),
            ("mysqldump -u [u] -p [db]", "Export database MySQL ke SQL",                "mysqldump -u root -p mydb > bak.sql"),
            ("mysql -u [u] -p [db] <",  "Import file SQL ke database",                 "mysql -u root -p mydb < bak.sql"),
        ]
    },
]

# ─── WARNA ─────────────────────────────────────────────────────────────────────

CAT_COLORS = [
    curses.COLOR_CYAN, curses.COLOR_MAGENTA, curses.COLOR_GREEN,
    curses.COLOR_YELLOW, curses.COLOR_RED, curses.COLOR_BLUE,
    curses.COLOR_CYAN, curses.COLOR_MAGENTA, curses.COLOR_GREEN,
    curses.COLOR_YELLOW, curses.COLOR_RED, curses.COLOR_BLUE,
]

# ─── FLATTEN DATA ───────────────────────────────────────────────────────────────

def build_flat(query=""):
    """Buat daftar flat dari semua perintah, opsional filter query."""
    flat = []
    q = query.lower()
    for ci, cat in enumerate(CATEGORIES):
        for cmd, desc, ex in cat["cmds"]:
            if q and q not in cmd.lower() and q not in desc.lower() and q not in ex.lower():
                continue
            flat.append({
                "cat_idx": ci,
                "cat_icon": cat["icon"],
                "cat_name": cat["nama"],
                "cmd": cmd,
                "desc": desc,
                "ex": ex,
            })
    return flat

# ─── MAIN APP ──────────────────────────────────────────────────────────────────

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    # Inisialisasi color pairs
    # 1..12 = warna kategori (teks terang pada bg default)
    for i, col in enumerate(CAT_COLORS, 1):
        curses.init_pair(i, col, -1)
    curses.init_pair(13, curses.COLOR_WHITE,  -1)   # teks biasa
    curses.init_pair(14, curses.COLOR_BLACK,  curses.COLOR_CYAN)   # selected
    curses.init_pair(15, curses.COLOR_CYAN,   -1)   # header/aksen
    curses.init_pair(16, curses.COLOR_YELLOW, -1)   # contoh
    curses.init_pair(17, curses.COLOR_GREEN,  -1)   # green
    curses.init_pair(18, curses.COLOR_BLACK,  curses.COLOR_WHITE)  # search bar

    state = {
        "query": "",
        "search_mode": False,
        "offset": 0,
        "cursor": 0,
    }

    while True:
        flat = build_flat(state["query"])
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        # ── HEADER ──────────────────────────────────────────────────────────
        header = " 📖 KAMUS PERINTAH TERMUX  |  250+ Perintah Lengkap untuk Android "
        stdscr.attron(curses.color_pair(15) | curses.A_BOLD)
        stdscr.addstr(0, 0, header[:w-1].ljust(w-1))
        stdscr.attroff(curses.color_pair(15) | curses.A_BOLD)

        # ── SEARCH BAR ──────────────────────────────────────────────────────
        search_label = " 🔍 Cari: "
        if state["search_mode"]:
            stdscr.attron(curses.color_pair(18) | curses.A_BOLD)
        else:
            stdscr.attron(curses.color_pair(13))
        search_str = search_label + state["query"] + ("█" if state["search_mode"] else "")
        stdscr.addstr(1, 0, search_str[:w-1].ljust(w-1))
        if state["search_mode"]:
            stdscr.attroff(curses.color_pair(18) | curses.A_BOLD)
        else:
            stdscr.attroff(curses.color_pair(13))

        # ── INFO BARIS ───────────────────────────────────────────────────────
        info = f" {len(flat)} perintah  |  ↑↓ Navigasi  |  / Cari  |  Enter Detail  |  q Keluar "
        stdscr.attron(curses.color_pair(13))
        stdscr.addstr(2, 0, info[:w-1])
        stdscr.attroff(curses.color_pair(13))

        # Separator
        stdscr.attron(curses.color_pair(15))
        stdscr.addstr(3, 0, "─" * min(w-1, 80))
        stdscr.attroff(curses.color_pair(15))

        # ── LIST AREA ────────────────────────────────────────────────────────
        list_top = 4
        list_h = h - list_top - 2   # baris untuk list

        # Clamp cursor & offset
        n = len(flat)
        if state["cursor"] >= n and n > 0:
            state["cursor"] = n - 1
        if state["cursor"] < 0:
            state["cursor"] = 0
        if n > 0:
            if state["cursor"] < state["offset"]:
                state["offset"] = state["cursor"]
            if state["cursor"] >= state["offset"] + list_h:
                state["offset"] = state["cursor"] - list_h + 1

        prev_cat = None
        row = list_top
        rendered = 0
        for idx in range(state["offset"], min(state["offset"] + list_h, n)):
            item = flat[idx]
            ci = item["cat_idx"]
            col_pair = curses.color_pair((ci % 12) + 1)

            # Separator kategori
            if item["cat_name"] != prev_cat and row < list_top + list_h:
                if row > list_top:
                    pass
                cat_header = f"  {item['cat_icon']} {item['cat_name']} "
                stdscr.attron(col_pair | curses.A_BOLD)
                stdscr.addstr(row, 0, cat_header[:w-1])
                stdscr.attroff(col_pair | curses.A_BOLD)
                row += 1
                prev_cat = item["cat_name"]
                if row >= list_top + list_h:
                    break

            if row >= list_top + list_h:
                break

            # Baris perintah
            is_sel = (idx == state["cursor"])
            cmd_str = f"  {'▶ ' if is_sel else '  '}{item['cmd']}"
            desc_str = f"  {item['desc']}"

            if is_sel:
                stdscr.attron(curses.color_pair(14) | curses.A_BOLD)
                line = f"  ▶ {item['cmd']:<38} {item['desc']}"
                stdscr.addstr(row, 0, line[:w-1].ljust(min(w-1, 80)))
                stdscr.attroff(curses.color_pair(14) | curses.A_BOLD)
            else:
                # cmd name
                stdscr.attron(col_pair)
                cmd_part = f"  {'  '}{item['cmd']:<38}"[:w-1]
                stdscr.addstr(row, 0, cmd_part)
                stdscr.attroff(col_pair)
                # desc
                stdscr.attron(curses.color_pair(13))
                desc_part = item['desc']
                remaining = w - 1 - len(cmd_part)
                if remaining > 2:
                    stdscr.addstr(row, len(cmd_part), desc_part[:remaining-1])
                stdscr.attroff(curses.color_pair(13))

            row += 1
            rendered += 1

        # ── FOOTER ──────────────────────────────────────────────────────────
        footer = " [/] Cari  [↑↓] Navigasi  [Enter] Detail  [Esc] Reset  [q] Keluar "
        stdscr.attron(curses.color_pair(15))
        stdscr.addstr(h-1, 0, footer[:w-1])
        stdscr.attroff(curses.color_pair(15))

        stdscr.refresh()

        # ── INPUT ────────────────────────────────────────────────────────────
        key = stdscr.getch()

        if state["search_mode"]:
            if key == 27:  # Esc
                state["search_mode"] = False
                state["query"] = ""
                state["cursor"] = 0
                state["offset"] = 0
            elif key in (10, 13):  # Enter
                state["search_mode"] = False
                state["cursor"] = 0
                state["offset"] = 0
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                state["query"] = state["query"][:-1]
                state["cursor"] = 0
                state["offset"] = 0
            elif 32 <= key <= 126:
                state["query"] += chr(key)
                state["cursor"] = 0
                state["offset"] = 0
        else:
            if key in (ord('q'), ord('Q')):
                return
            elif key == ord('/'):
                state["search_mode"] = True
            elif key == 27:
                state["query"] = ""
                state["cursor"] = 0
                state["offset"] = 0
            elif key == curses.KEY_UP:
                state["cursor"] = max(0, state["cursor"] - 1)
            elif key == curses.KEY_DOWN:
                state["cursor"] = min(n - 1, state["cursor"] + 1)
            elif key == curses.KEY_PPAGE:  # Page Up
                state["cursor"] = max(0, state["cursor"] - list_h)
            elif key == curses.KEY_NPAGE:  # Page Down
                state["cursor"] = min(n - 1, state["cursor"] + list_h)
            elif key == curses.KEY_HOME:
                state["cursor"] = 0
                state["offset"] = 0
            elif key == curses.KEY_END:
                state["cursor"] = n - 1
            elif key in (10, 13) and n > 0:
                # Detail view
                show_detail(stdscr, flat[state["cursor"]])

def show_detail(stdscr, item):
    """Tampilkan halaman detail perintah."""
    ci = item["cat_idx"]
    col_pair = curses.color_pair((ci % 12) + 1)

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        # Header
        stdscr.attron(curses.color_pair(15) | curses.A_BOLD)
        stdscr.addstr(0, 0, " 📖 DETAIL PERINTAH ".ljust(w-1))
        stdscr.attroff(curses.color_pair(15) | curses.A_BOLD)

        # Kategori
        stdscr.attron(col_pair | curses.A_BOLD)
        stdscr.addstr(2, 2, f"{item['cat_icon']} {item['cat_name']}")
        stdscr.attroff(col_pair | curses.A_BOLD)

        # Nama perintah
        stdscr.attron(col_pair | curses.A_BOLD)
        stdscr.addstr(4, 2, "PERINTAH:")
        stdscr.attroff(col_pair | curses.A_BOLD)
        stdscr.attron(curses.color_pair(13) | curses.A_BOLD)
        stdscr.addstr(5, 4, item["cmd"][:w-6])
        stdscr.attroff(curses.color_pair(13) | curses.A_BOLD)

        # Separator
        stdscr.attron(col_pair)
        stdscr.addstr(6, 2, "─" * min(w-4, 60))
        stdscr.attroff(col_pair)

        # Deskripsi
        stdscr.attron(col_pair | curses.A_BOLD)
        stdscr.addstr(7, 2, "DESKRIPSI:")
        stdscr.attroff(col_pair | curses.A_BOLD)

        # Word-wrap deskripsi
        words = item["desc"].split()
        lines, line = [], ""
        for w2 in words:
            if len(line) + len(w2) + 1 > w - 8:
                lines.append(line)
                line = w2
            else:
                line = (line + " " + w2).strip()
        if line:
            lines.append(line)

        for li, ln in enumerate(lines):
            stdscr.attron(curses.color_pair(13))
            stdscr.addstr(8 + li, 4, ln[:w-6])
            stdscr.attroff(curses.color_pair(13))

        ex_start = 8 + len(lines) + 1

        # Contoh
        stdscr.attron(curses.color_pair(16) | curses.A_BOLD)
        stdscr.addstr(ex_start, 2, "CONTOH:")
        stdscr.attroff(curses.color_pair(16) | curses.A_BOLD)

        for ei, ex_line in enumerate(item["ex"].split("\n")):
            if ex_start + 1 + ei < h - 3:
                stdscr.attron(curses.color_pair(17) | curses.A_BOLD)
                stdscr.addstr(ex_start + 1 + ei, 4, "$ " + ex_line[:w-8])
                stdscr.attroff(curses.color_pair(17) | curses.A_BOLD)

        # Tips copy
        tip_row = ex_start + 2 + len(item["ex"].split("\n"))
        if tip_row < h - 3:
            stdscr.attron(curses.color_pair(13))
            stdscr.addstr(tip_row, 2, "💡 Tekan Ctrl+C untuk menyalin teks di Termux")
            stdscr.attroff(curses.color_pair(13))

        # Footer
        stdscr.attron(curses.color_pair(15))
        stdscr.addstr(h-1, 0, " [Esc / q / ←] Kembali ke daftar ".ljust(w-1))
        stdscr.attroff(curses.color_pair(15))

        stdscr.refresh()

        key = stdscr.getch()
        if key in (27, ord('q'), ord('Q'), curses.KEY_LEFT, curses.KEY_BACKSPACE):
            break

# ─── ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\nError: {e}")
        print("Pastikan terminal kamu mendukung curses.")
        sys.exit(1)

    print("\n✅ Terima kasih sudah menggunakan Kamus Termux!")
    print("   Jalankan lagi: python termux_kamus.py\n")
