#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════╗
║       KAMUS WEB3 & AIRDROP TERMUX v1.0       ║
║   Panduan Lengkap Airdrop & Crypto di HP     ║
╚══════════════════════════════════════════════╝
Cara pakai: python kamus_web3.py
"""

import curses
import sys

# ─── DATA ──────────────────────────────────────────────────────────────────────

CATEGORIES = [
    {
        "icon": "🚀", "nama": "Setup Awal Termux",
        "cmds": [
            ("pkg update && pkg upgrade",
             "Update & upgrade semua paket Termux (lakukan pertama kali)",
             "pkg update && pkg upgrade"),
            ("pkg install git",
             "Install Git untuk clone repo airdrop dari GitHub",
             "pkg install git"),
            ("pkg install python",
             "Install Python untuk jalankan script bot",
             "pkg install python"),
            ("pkg install nodejs",
             "Install Node.js untuk script airdrop berbasis JS",
             "pkg install nodejs"),
            ("pkg install tmux",
             "Install tmux agar bot tetap jalan walau layar mati",
             "pkg install tmux"),
            ("pkg install curl",
             "Install curl untuk request API & cek wallet",
             "pkg install curl"),
            ("pkg install jq",
             "Install jq untuk parsing response JSON dari blockchain",
             "pkg install jq"),
            ("pkg install wget",
             "Install wget untuk download file/script",
             "pkg install wget"),
            ("termux-setup-storage",
             "Izinkan Termux akses penyimpanan /sdcard",
             "termux-setup-storage"),
            ("pkg install openssh",
             "Install SSH untuk koneksi ke VPS/server",
             "pkg install openssh"),
        ]
    },
    {
        "icon": "🖥️", "nama": "tmux - Sesi & Background",
        "cmds": [
            ("tmux",
             "Mulai sesi tmux baru (bot tetap jalan walau Termux ditutup)",
             "tmux"),
            ("tmux new -s [nama]",
             "Buat sesi tmux baru dengan nama tertentu",
             "tmux new -s airdrop1\ntmux new -s bot_grass"),
            ("tmux ls",
             "Lihat semua sesi tmux yang aktif",
             "tmux ls"),
            ("tmux attach -t [nama]",
             "Masuk kembali ke sesi tmux yang berjalan",
             "tmux attach -t airdrop1\ntmux attach -t bot_grass"),
            ("tmux attach",
             "Masuk ke sesi tmux terakhir",
             "tmux attach"),
            ("Ctrl+B lalu D",
             "Detach dari sesi tmux (sesi tetap berjalan di background)",
             "(tekan Ctrl+B, lepas, lalu tekan D)"),
            ("Ctrl+B lalu C",
             "Buat window/tab baru di dalam tmux",
             "(tekan Ctrl+B, lepas, lalu tekan C)"),
            ("Ctrl+B lalu N",
             "Pindah ke window berikutnya",
             "(tekan Ctrl+B, lepas, lalu tekan N)"),
            ("Ctrl+B lalu P",
             "Pindah ke window sebelumnya",
             "(tekan Ctrl+B, lepas, lalu tekan P)"),
            ("Ctrl+B lalu [0-9]",
             "Loncat ke window nomor tertentu",
             "(tekan Ctrl+B, lepas, lalu tekan angka 0-9)"),
            ("Ctrl+B lalu %",
             "Split layar tmux secara vertikal (dua panel)",
             "(tekan Ctrl+B, lepas, lalu tekan %)"),
            ("Ctrl+B lalu \"",
             "Split layar tmux secara horizontal",
             "(tekan Ctrl+B, lepas, lalu tekan tanda petik)"),
            ("Ctrl+B lalu panah",
             "Pindah antar panel tmux",
             "(tekan Ctrl+B, lepas, lalu tekan arah panah)"),
            ("tmux kill-session -t [nama]",
             "Hentikan & hapus sesi tmux tertentu",
             "tmux kill-session -t airdrop1"),
            ("tmux kill-server",
             "Hentikan semua sesi tmux sekaligus",
             "tmux kill-server"),
            ("tmux rename-session -t [lama] [baru]",
             "Ganti nama sesi tmux",
             "tmux rename-session -t 0 bot_claim"),
        ]
    },
    {
        "icon": "📦", "nama": "Node.js & npm",
        "cmds": [
            ("node --version",
             "Cek versi Node.js terinstall",
             "node --version"),
            ("npm --version",
             "Cek versi npm",
             "npm --version"),
            ("npm install",
             "Install semua dependensi dari package.json",
             "npm install"),
            ("npm install -g [paket]",
             "Install paket npm secara global",
             "npm install -g pm2"),
            ("npm start",
             "Jalankan script start dari package.json",
             "npm start"),
            ("npm run [script]",
             "Jalankan script custom dari package.json",
             "npm run bot\nnpm run claim"),
            ("node [file.js]",
             "Jalankan file JavaScript langsung",
             "node index.js\nnode bot.js"),
            ("node -e '[kode]'",
             "Jalankan kode JS langsung dari terminal",
             "node -e 'console.log(\"test\")'"),
            ("npm list",
             "Tampilkan semua package yang terinstall",
             "npm list"),
            ("npm update",
             "Update semua package ke versi terbaru",
             "npm update"),
            ("npm cache clean --force",
             "Bersihkan cache npm jika ada error install",
             "npm cache clean --force"),
            ("npx [perintah]",
             "Jalankan package npm tanpa install global",
             "npx hardhat compile"),
            ("npm uninstall [paket]",
             "Hapus package npm",
             "npm uninstall axios"),
        ]
    },
    {
        "icon": "🐍", "nama": "Python & Bot Script",
        "cmds": [
            ("pip install -r requirements.txt",
             "Install semua library dari file requirements (paling umum di repo airdrop)",
             "pip install -r requirements.txt"),
            ("python bot.py",
             "Jalankan script bot Python",
             "python bot.py\npython3 main.py"),
            ("python -m venv venv",
             "Buat virtual environment Python (isolasi dependensi)",
             "python -m venv venv"),
            ("source venv/bin/activate",
             "Aktifkan virtual environment",
             "source venv/bin/activate"),
            ("deactivate",
             "Nonaktifkan virtual environment",
             "deactivate"),
            ("pip install web3",
             "Install library Web3.py untuk interaksi blockchain",
             "pip install web3"),
            ("pip install requests",
             "Install requests untuk HTTP/API call",
             "pip install requests"),
            ("pip install python-dotenv",
             "Install dotenv untuk baca file .env (private key, dll)",
             "pip install python-dotenv"),
            ("pip install aiohttp",
             "Install aiohttp untuk request async (lebih cepat)",
             "pip install aiohttp"),
            ("pip install eth-account",
             "Install eth-account untuk manage wallet Ethereum",
             "pip install eth-account"),
            ("nohup python bot.py &",
             "Jalankan bot di background, tetap jalan walau terminal ditutup",
             "nohup python bot.py > bot.log 2>&1 &"),
            ("python bot.py > log.txt 2>&1 &",
             "Jalankan bot di background & simpan output ke log",
             "python bot.py > bot.log 2>&1 &"),
        ]
    },
    {
        "icon": "🔗", "nama": "Git - Clone & Update Tool",
        "cmds": [
            ("git clone [url]",
             "Clone repo airdrop/tool dari GitHub",
             "git clone https://github.com/user/airdrop-bot.git"),
            ("git clone [url] [folder]",
             "Clone repo ke folder dengan nama tertentu",
             "git clone https://github.com/user/bot.git mybot"),
            ("git pull",
             "Update tool ke versi terbaru dari GitHub",
             "cd mybot && git pull"),
            ("git pull origin main",
             "Pull update dari branch main",
             "git pull origin main"),
            ("git log --oneline -10",
             "Lihat 10 commit terakhir (cek update terbaru)",
             "git log --oneline -10"),
            ("git status",
             "Cek apakah ada file yang diubah",
             "git status"),
            ("git stash",
             "Simpan perubahan lokal sebelum git pull",
             "git stash\ngit pull\ngit stash pop"),
            ("git checkout -- .",
             "Reset semua perubahan lokal ke kondisi asal",
             "git checkout -- ."),
            ("git branch -a",
             "Lihat semua branch yang tersedia di repo",
             "git branch -a"),
            ("git checkout [branch]",
             "Pindah ke branch tertentu",
             "git checkout dev"),
        ]
    },
    {
        "icon": "🌐", "nama": "curl & API Blockchain",
        "cmds": [
            ("curl [url]",
             "Request GET ke API/endpoint",
             "curl https://api.coingecko.com/api/v3/ping"),
            ("curl -s [url] | jq",
             "Request API dan format output JSON dengan rapi",
             "curl -s https://api.example.com/data | jq"),
            ("curl -s [url] | jq '.[key]'",
             "Ambil nilai tertentu dari response JSON",
             "curl -s https://api.example.com | jq '.balance'"),
            ("curl -X POST -H 'Content-Type: application/json' -d '{...}' [url]",
             "Kirim POST request JSON ke API (claim, register, dll)",
             "curl -X POST -H 'Content-Type: application/json' \\\n  -d '{\"address\":\"0x...\"}' \\\n  https://api.example.com/claim"),
            ("curl -H 'Authorization: Bearer [token]' [url]",
             "Request dengan Bearer token (autentikasi)",
             "curl -H 'Authorization: Bearer eyJ...' https://api.example.com"),
            ("curl -H 'Authorization: Bearer [token]' [url] | jq '.points'",
             "Cek poin/reward dari API dengan autentikasi",
             "curl -H 'Authorization: Bearer TOKEN' \\\n  https://api.project.com/user | jq '.points'"),
            ("curl -o [file] [url]",
             "Download file dari URL",
             "curl -o script.js https://example.com/bot.js"),
            ("curl -s --max-time 10 [url]",
             "Request dengan timeout 10 detik",
             "curl -s --max-time 10 https://api.example.com"),
            ("curl -x [proxy] [url]",
             "Request melalui proxy",
             "curl -x http://proxy:port https://api.example.com"),
            ("curl -v [url]",
             "Request dengan output verbose (debug header/response)",
             "curl -v https://api.example.com"),
        ]
    },
    {
        "icon": "🔧", "nama": "jq - Parsing JSON",
        "cmds": [
            ("echo '[json]' | jq",
             "Format/pretty-print JSON",
             "echo '{\"a\":1}' | jq"),
            ("echo '[json]' | jq '.[key]'",
             "Ambil nilai dari key tertentu",
             "echo '{\"balance\":\"100\"}' | jq '.balance'"),
            ("echo '[json]' | jq '.[]'",
             "Iterate semua elemen array JSON",
             "echo '[1,2,3]' | jq '.[]'"),
            ("echo '[json]' | jq '.[0]'",
             "Ambil elemen pertama dari array",
             "echo '[{\"a\":1},{\"b\":2}]' | jq '.[0]'"),
            ("cat file.json | jq '.[key]'",
             "Baca file JSON dan ambil nilai key",
             "cat response.json | jq '.data.points'"),
            ("jq -r '.[key]' file.json",
             "Output nilai tanpa tanda kutip (raw string)",
             "jq -r '.address' wallet.json"),
            ("jq 'keys' file.json",
             "Tampilkan semua key dari objek JSON",
             "jq 'keys' response.json"),
            ("jq 'length' file.json",
             "Hitung jumlah elemen array JSON",
             "jq 'length' wallets.json"),
            ("jq '.[] | select(.status==\"active\")' file.json",
             "Filter elemen berdasarkan kondisi",
             "jq '.[] | select(.status==\"active\")' accounts.json"),
            ("jq '[.[] | .address]' file.json",
             "Buat array baru dari field tertentu",
             "jq '[.[] | .address]' wallets.json"),
        ]
    },
    {
        "icon": "⏰", "nama": "Cron - Otomasi Terjadwal",
        "cmds": [
            ("crontab -e",
             "Edit jadwal cron (otomasi perintah)",
             "crontab -e"),
            ("crontab -l",
             "Lihat semua jadwal cron yang aktif",
             "crontab -l"),
            ("crontab -r",
             "Hapus semua jadwal cron",
             "crontab -r"),
            ("* * * * * [perintah]",
             "Format cron: menit jam hari bulan hari-minggu",
             "# Setiap menit:\n* * * * * python ~/bot/claim.py\n# Setiap jam:\n0 * * * * python ~/bot/claim.py\n# Setiap hari jam 8 pagi:\n0 8 * * * python ~/bot/claim.py"),
            ("0 */6 * * * [perintah]",
             "Jalankan setiap 6 jam",
             "0 */6 * * * python ~/bot/checkin.py"),
            ("0 8 * * * [perintah]",
             "Jalankan setiap hari jam 8 pagi",
             "0 8 * * * python ~/bot/daily_claim.py >> ~/log.txt 2>&1"),
            ("*/30 * * * * [perintah]",
             "Jalankan setiap 30 menit",
             "*/30 * * * * python ~/bot/ping.py"),
            ("@reboot [perintah]",
             "Jalankan otomatis saat Termux restart",
             "@reboot tmux new-session -d -s bot 'python ~/bot/main.py'"),
            ("pkg install cronie",
             "Install cronie agar cron bisa berjalan di Termux",
             "pkg install cronie"),
            ("crond",
             "Jalankan daemon cron di Termux",
             "crond"),
        ]
    },
    {
        "icon": "🔐", "nama": "Wallet & Keamanan",
        "cmds": [
            ("nano .env",
             "Edit file .env untuk simpan private key/config (jangan share!)",
             "nano .env\n# Isi:\nPRIVATE_KEY=0x...\nRPC_URL=https://..."),
            ("chmod 600 .env",
             "Amankan file .env agar hanya bisa dibaca sendiri",
             "chmod 600 .env"),
            ("cat .env",
             "Lihat isi file .env (hati-hati jangan di depan orang)",
             "cat .env"),
            ("grep -r 'PRIVATE_KEY' .",
             "Cari file yang menyimpan private key di folder saat ini",
             "grep -r 'PRIVATE_KEY' ."),
            ("openssl rand -hex 32",
             "Generate random hex 32 byte (bisa untuk seed/key testing)",
             "openssl rand -hex 32"),
            ("history -c",
             "Hapus riwayat perintah terminal (keamanan)",
             "history -c"),
            ("cat /dev/null > ~/.bash_history",
             "Kosongkan file history bash secara permanen",
             "cat /dev/null > ~/.bash_history"),
            ("gpg -c [file]",
             "Enkripsi file berisi wallet/key dengan password",
             "gpg -c wallets.txt"),
            ("gpg [file.gpg]",
             "Dekripsi file yang sudah dienkripsi",
             "gpg wallets.txt.gpg"),
            ("sha256sum [file]",
             "Verifikasi integritas file/script yang didownload",
             "sha256sum bot.py"),
        ]
    },
    {
        "icon": "📊", "nama": "Monitor & Log",
        "cmds": [
            ("tail -f [log.txt]",
             "Pantau log bot secara real-time",
             "tail -f bot.log\ntail -f nohup.out"),
            ("tail -n 50 [log.txt]",
             "Lihat 50 baris terakhir dari log",
             "tail -n 50 bot.log"),
            ("grep 'success\\|error\\|claim' [log.txt]",
             "Filter log untuk kata kunci penting",
             "grep -i 'success\\|error\\|failed' bot.log"),
            ("grep -c 'success' [log.txt]",
             "Hitung berapa kali kata muncul di log",
             "grep -c 'success' bot.log"),
            ("wc -l [log.txt]",
             "Hitung total baris log",
             "wc -l bot.log"),
            ("cat [log.txt] | grep $(date +%Y-%m-%d)",
             "Filter log hanya untuk hari ini",
             "cat bot.log | grep $(date +%Y-%m-%d)"),
            ("> [log.txt]",
             "Kosongkan/reset file log tanpa hapus file",
             "> bot.log"),
            ("ps aux | grep python",
             "Cek apakah bot Python sedang berjalan",
             "ps aux | grep python\nps aux | grep node"),
            ("ps aux | grep node",
             "Cek apakah bot Node.js sedang berjalan",
             "ps aux | grep node"),
            ("kill $(pgrep -f bot.py)",
             "Hentikan bot berdasarkan nama script",
             "kill $(pgrep -f bot.py)\nkill $(pgrep -f index.js)"),
            ("free -h",
             "Cek penggunaan RAM (pastikan cukup untuk bot)",
             "free -h"),
            ("df -h",
             "Cek ruang penyimpanan tersisa",
             "df -h"),
        ]
    },
    {
        "icon": "🔄", "nama": "Proxy & Jaringan",
        "cmds": [
            ("export http_proxy=http://[ip]:[port]",
             "Set proxy HTTP untuk semua request di sesi ini",
             "export http_proxy=http://127.0.0.1:8080"),
            ("export https_proxy=http://[ip]:[port]",
             "Set proxy HTTPS",
             "export https_proxy=http://127.0.0.1:8080"),
            ("unset http_proxy https_proxy",
             "Hapus/nonaktifkan proxy",
             "unset http_proxy https_proxy"),
            ("curl --proxy [proxy] [url]",
             "Gunakan proxy hanya untuk satu request curl",
             "curl --proxy http://proxy:port https://api.example.com"),
            ("curl -s https://api.ipify.org",
             "Cek IP publik yang digunakan saat ini",
             "curl -s https://api.ipify.org\ncurl -s https://ipinfo.io/json | jq"),
            ("curl -s https://ipinfo.io/json | jq",
             "Cek info lengkap IP (negara, ISP, dll)",
             "curl -s https://ipinfo.io/json | jq"),
            ("ping -c 3 [rpc-endpoint]",
             "Cek konektivitas ke RPC node blockchain",
             "ping -c 3 mainnet.infura.io"),
            ("curl -s -X POST [rpc] -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"eth_blockNumber\",\"params\":[],\"id\":1}'",
             "Cek block terbaru via RPC (Ethereum/EVM)",
             "curl -s -X POST https://rpc.ankr.com/eth \\\n  -H 'Content-Type: application/json' \\\n  -d '{\"jsonrpc\":\"2.0\",\"method\":\"eth_blockNumber\",\"params\":[],\"id\":1}' | jq"),
        ]
    },
    {
        "icon": "💡", "nama": "Workflow Airdrop Lengkap",
        "cmds": [
            ("STEP 1: Setup",
             "Update Termux dan install semua tools yang dibutuhkan",
             "pkg update && pkg upgrade\npkg install git python nodejs tmux curl jq"),
            ("STEP 2: Clone repo",
             "Clone tool airdrop dari GitHub",
             "git clone https://github.com/user/airdrop-bot.git\ncd airdrop-bot"),
            ("STEP 3: Install dependensi",
             "Install semua library yang dibutuhkan bot",
             "# Untuk Python:\npip install -r requirements.txt\n\n# Untuk Node.js:\nnpm install"),
            ("STEP 4: Konfigurasi .env",
             "Buat dan isi file konfigurasi dengan data wallet",
             "cp .env.example .env\nnano .env\n# Isi PRIVATE_KEY, RPC_URL, dll"),
            ("STEP 5: Test jalankan",
             "Coba jalankan bot dulu untuk pastikan tidak ada error",
             "# Python:\npython bot.py\n\n# Node.js:\nnode index.js"),
            ("STEP 6: Jalankan di tmux",
             "Jalankan bot dalam sesi tmux agar tetap berjalan",
             "tmux new -s airdrop\npython bot.py\n# lalu Ctrl+B lalu D untuk detach"),
            ("STEP 7: Monitor log",
             "Pantau output bot dari luar sesi tmux",
             "python bot.py > ~/bot.log 2>&1 &\ntail -f ~/bot.log"),
            ("STEP 8: Update tool",
             "Update tool ke versi terbaru jika ada update",
             "cd airdrop-bot\ngit pull origin main\npip install -r requirements.txt"),
            ("STEP 9: Cek status",
             "Cek apakah bot masih berjalan",
             "ps aux | grep python\ntmux ls"),
            ("STEP 10: Multiple bot",
             "Jalankan beberapa bot sekaligus di tmux berbeda",
             "tmux new -s bot1\npython bot1.py\n# Ctrl+B D\ntmux new -s bot2\npython bot2.py"),
        ]
    },
]

# ─── WARNA ─────────────────────────────────────────────────────────────────────

CAT_COLORS = [
    curses.COLOR_CYAN,    curses.COLOR_GREEN,   curses.COLOR_YELLOW,
    curses.COLOR_BLUE,    curses.COLOR_MAGENTA, curses.COLOR_RED,
    curses.COLOR_CYAN,    curses.COLOR_GREEN,   curses.COLOR_YELLOW,
    curses.COLOR_BLUE,    curses.COLOR_MAGENTA, curses.COLOR_RED,
]

# ─── FLATTEN ───────────────────────────────────────────────────────────────────

def build_flat(query=""):
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

# ─── DETAIL VIEW ───────────────────────────────────────────────────────────────

def show_detail(stdscr, item):
    ci = item["cat_idx"]
    col_pair = curses.color_pair((ci % 12) + 1)

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        # Header
        stdscr.attron(curses.color_pair(15) | curses.A_BOLD)
        stdscr.addstr(0, 0, " 🔍 DETAIL PERINTAH ".ljust(w - 1))
        stdscr.attroff(curses.color_pair(15) | curses.A_BOLD)

        # Kategori
        stdscr.attron(col_pair | curses.A_BOLD)
        stdscr.addstr(2, 2, f"{item['cat_icon']}  {item['cat_name']}")
        stdscr.attroff(col_pair | curses.A_BOLD)

        # Nama perintah
        stdscr.attron(col_pair | curses.A_BOLD)
        stdscr.addstr(4, 2, "PERINTAH:")
        stdscr.attroff(col_pair | curses.A_BOLD)
        stdscr.attron(curses.color_pair(13) | curses.A_BOLD)
        stdscr.addstr(5, 4, item["cmd"][:w - 6])
        stdscr.attroff(curses.color_pair(13) | curses.A_BOLD)

        stdscr.attron(col_pair)
        stdscr.addstr(6, 2, "─" * min(w - 4, 60))
        stdscr.attroff(col_pair)

        # Deskripsi word-wrap
        stdscr.attron(col_pair | curses.A_BOLD)
        stdscr.addstr(7, 2, "DESKRIPSI:")
        stdscr.attroff(col_pair | curses.A_BOLD)

        words = item["desc"].split()
        lines, line = [], ""
        for word in words:
            if len(line) + len(word) + 1 > w - 8:
                lines.append(line)
                line = word
            else:
                line = (line + " " + word).strip()
        if line:
            lines.append(line)

        for li, ln in enumerate(lines):
            stdscr.attron(curses.color_pair(13))
            stdscr.addstr(8 + li, 4, ln[:w - 6])
            stdscr.attroff(curses.color_pair(13))

        ex_start = 8 + len(lines) + 1

        # Contoh
        stdscr.attron(curses.color_pair(16) | curses.A_BOLD)
        if ex_start < h - 3:
            stdscr.addstr(ex_start, 2, "CONTOH:")
        stdscr.attroff(curses.color_pair(16) | curses.A_BOLD)

        for ei, ex_line in enumerate(item["ex"].split("\n")):
            r = ex_start + 1 + ei
            if r < h - 3:
                stdscr.attron(curses.color_pair(17) | curses.A_BOLD)
                prefix = "  " if ex_line.startswith("#") else "$ "
                stdscr.addstr(r, 4, prefix + ex_line[:w - 8])
                stdscr.attroff(curses.color_pair(17) | curses.A_BOLD)

        # Tip
        tip_row = ex_start + 2 + len(item["ex"].split("\n"))
        if tip_row < h - 3:
            stdscr.attron(curses.color_pair(13))
            stdscr.addstr(tip_row, 2, "💡 Tahan layar lalu pilih 'Copy' untuk menyalin")
            stdscr.attroff(curses.color_pair(13))

        # Footer
        stdscr.attron(curses.color_pair(15))
        stdscr.addstr(h - 1, 0, " [Esc / k / ←] Kembali ke daftar ".ljust(w - 1))
        stdscr.attroff(curses.color_pair(15))

        stdscr.refresh()
        key = stdscr.getch()
        if key in (27, ord('k'), ord('K'), curses.KEY_LEFT, curses.KEY_BACKSPACE):
            break

# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    for i, col in enumerate(CAT_COLORS, 1):
        curses.init_pair(i, col, -1)
    curses.init_pair(13, curses.COLOR_WHITE,  -1)
    curses.init_pair(14, curses.COLOR_BLACK,  curses.COLOR_GREEN)
    curses.init_pair(15, curses.COLOR_GREEN,  -1)
    curses.init_pair(16, curses.COLOR_YELLOW, -1)
    curses.init_pair(17, curses.COLOR_CYAN,   -1)
    curses.init_pair(18, curses.COLOR_BLACK,  curses.COLOR_WHITE)

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

        # Header
        header = " 🚀 KAMUS WEB3 & AIRDROP  |  Panduan Lengkap Crypto di Termux "
        stdscr.attron(curses.color_pair(15) | curses.A_BOLD)
        stdscr.addstr(0, 0, header[:w - 1].ljust(w - 1))
        stdscr.attroff(curses.color_pair(15) | curses.A_BOLD)

        # Search bar
        search_label = " 🔍 Cari: "
        if state["search_mode"]:
            stdscr.attron(curses.color_pair(18) | curses.A_BOLD)
        else:
            stdscr.attron(curses.color_pair(13))
        search_str = search_label + state["query"] + ("█" if state["search_mode"] else "")
        stdscr.addstr(1, 0, search_str[:w - 1].ljust(w - 1))
        if state["search_mode"]:
            stdscr.attroff(curses.color_pair(18) | curses.A_BOLD)
        else:
            stdscr.attroff(curses.color_pair(13))

        # Info bar
        info = f" {len(flat)} perintah  |  ↑↓ Navigasi  |  s Cari  |  Enter Detail  |  k Keluar "
        stdscr.attron(curses.color_pair(13))
        stdscr.addstr(2, 0, info[:w - 1])
        stdscr.attroff(curses.color_pair(13))

        # Separator
        stdscr.attron(curses.color_pair(15))
        stdscr.addstr(3, 0, "─" * min(w - 1, 80))
        stdscr.attroff(curses.color_pair(15))

        # List
        list_top = 4
        list_h = h - list_top - 2
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
        for idx in range(state["offset"], min(state["offset"] + list_h, n)):
            item = flat[idx]
            ci = item["cat_idx"]
            col_pair = curses.color_pair((ci % 12) + 1)

            if item["cat_name"] != prev_cat and row < list_top + list_h:
                cat_header = f"  {item['cat_icon']}  {item['cat_name']} "
                stdscr.attron(col_pair | curses.A_BOLD)
                stdscr.addstr(row, 0, cat_header[:w - 1])
                stdscr.attroff(col_pair | curses.A_BOLD)
                row += 1
                prev_cat = item["cat_name"]
                if row >= list_top + list_h:
                    break

            if row >= list_top + list_h:
                break

            is_sel = (idx == state["cursor"])
            if is_sel:
                stdscr.attron(curses.color_pair(14) | curses.A_BOLD)
                line = f"  ▶ {item['cmd']:<38} {item['desc']}"
                stdscr.addstr(row, 0, line[:w - 1].ljust(min(w - 1, 80)))
                stdscr.attroff(curses.color_pair(14) | curses.A_BOLD)
            else:
                stdscr.attron(col_pair)
                cmd_part = f"     {item['cmd']:<38}"[:w - 1]
                stdscr.addstr(row, 0, cmd_part)
                stdscr.attroff(col_pair)
                stdscr.attron(curses.color_pair(13))
                remaining = w - 1 - len(cmd_part)
                if remaining > 2:
                    stdscr.addstr(row, len(cmd_part), item['desc'][:remaining - 1])
                stdscr.attroff(curses.color_pair(13))

            row += 1

        # Footer
        footer = " [s] Cari  [↑↓] Navigasi  [Enter] Detail  [Esc] Reset  [k] Keluar "
        stdscr.attron(curses.color_pair(15))
        stdscr.addstr(h - 1, 0, footer[:w - 1])
        stdscr.attroff(curses.color_pair(15))

        stdscr.refresh()

        # Input
        key = stdscr.getch()

        if state["search_mode"]:
            if key == 27:
                state["search_mode"] = False
                state["query"] = ""
                state["cursor"] = 0
                state["offset"] = 0
            elif key in (10, 13):
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
            if key in (ord('k'), ord('K')):
                return
            elif key == ord('s'):
                state["search_mode"] = True
            elif key == 27:
                state["query"] = ""
                state["cursor"] = 0
                state["offset"] = 0
            elif key == curses.KEY_UP:
                state["cursor"] = max(0, state["cursor"] - 1)
            elif key == curses.KEY_DOWN:
                state["cursor"] = min(n - 1, state["cursor"] + 1)
            elif key == curses.KEY_PPAGE:
                state["cursor"] = max(0, state["cursor"] - list_h)
            elif key == curses.KEY_NPAGE:
                state["cursor"] = min(n - 1, state["cursor"] + list_h)
            elif key == curses.KEY_HOME:
                state["cursor"] = 0
                state["offset"] = 0
            elif key == curses.KEY_END:
                state["cursor"] = n - 1
            elif key in (10, 13) and n > 0:
                show_detail(stdscr, flat[state["cursor"]])

# ─── ENTRY ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\nError: {e}")
        print("Pastikan terminal mendukung curses.")
        sys.exit(1)

    print("\n✅ Terima kasih sudah menggunakan Kamus Web3 & Airdrop!")
    print("   Jalankan lagi: python kamus_web3.py\n")
