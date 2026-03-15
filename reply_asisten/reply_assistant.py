#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════╗
║          REPLY ASSISTANT v1.0                    ║
║     Powered by Google Gemini API (Gratis)        ║
╚══════════════════════════════════════════════════╝

Install:
  pip install requests colorama

Daftar API key gratis:
  https://aistudio.google.com/app/apikey

Set API key (pilih salah satu):
  1. File .env  → buat file .env, isi: GEMINI_API_KEY=AIza...
  2. Export     → export GEMINI_API_KEY=AIza...
  3. Langsung   → isi baris API_KEY di script ini

Cara pakai:
  python reply_assistant.py
"""

import os
import sys
import textwrap

# ── BACA .env ─────────────────────────────────────────────────────────────────
def load_env(filepath=None):
    """Baca file .env dan masukkan ke os.environ."""
    paths = [
        filepath,
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
        os.path.join(os.path.expanduser("~"), ".env"),
    ]
    for path in paths:
        if path and os.path.isfile(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, _, val = line.partition("=")
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = val
            return path
    return None

# Muat .env sebelum baca API_KEY
_env_file = load_env()

# ── API KEY ───────────────────────────────────────────────────────────────────
# Prioritas: .env → environment variable → kosong
API_KEY = os.environ.get("GEMINI_API_KEY", "")

# ── Cek dependensi ────────────────────────────────────────────────────────────
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

# ── Warna ─────────────────────────────────────────────────────────────────────
def c(text, color="white", bold=False):
    if not HAS_COLOR:
        return text
    colors = {
        "green":   Fore.GREEN,
        "red":     Fore.RED,
        "yellow":  Fore.YELLOW,
        "cyan":    Fore.CYAN,
        "blue":    Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "white":   Fore.WHITE,
        "gray":    Fore.WHITE + Style.DIM,
    }
    col = colors.get(color, Fore.WHITE)
    b   = Style.BRIGHT if bold else ""
    return f"{b}{col}{text}{Style.RESET_ALL}"

def cls():
    os.system("clear")

def wrap(text, width=60, indent="  "):
    return "\n".join(
        indent + line
        for line in textwrap.wrap(text, width=width)
    )

def print_header():
    print()
    print(c("╔══════════════════════════════════════════════════╗", "cyan"))
    print(c("║", "cyan") + c("          REPLY ASSISTANT v1.0                  ", "white", True) + c("  ║", "cyan"))
    print(c("║", "cyan") + c("      Powered by Google Gemini API              ", "gray") + c("  ║", "cyan"))
    print(c("╚══════════════════════════════════════════════════╝", "cyan"))

def divider(color="blue"):
    print(c("  " + "─" * 48, color))

# ── PILIHAN ───────────────────────────────────────────────────────────────────
STYLES = {
    "1": ("Santai & Friendly",    "santai dan friendly, seperti ngobrol sama teman, boleh pakai bahasa gaul ringan"),
    "2": ("Formal & Sopan",       "formal, sopan, dan profesional, tidak kaku"),
    "3": ("Lucu & Receh",         "lucu dan receh, ringan, boleh pakai humor ringan"),
    "4": ("Singkat & To The Point","singkat dan padat, maksimal 1-2 kalimat saja, langsung ke inti"),
}

LANGS = {
    "1": ("Indonesia",        "Bahasa Indonesia"),
    "2": ("Inggris",          "Bahasa Inggris"),
    "3": ("Campur (Indo-Eng)","campuran Indonesia dan Inggris gaya gaul"),
}

# ── GENERATE ─────────────────────────────────────────────────────────────────
def generate_replies(pesan, style_desc, lang_desc):
    """Panggil Gemini API via requests."""
    prompt = f"""Kamu adalah asisten untuk membalas pesan di media sosial.
Buatkan TEPAT 2 balasan untuk pesan berikut:

"{pesan}"

Ketentuan:
- Gaya: {style_desc}
- Bahasa: {lang_desc}
- Balasan harus natural, tidak kaku, tidak terkesan dibuat bot
- Sesuaikan nada dengan konteks pesan
- Jangan tambahkan penjelasan apapun

Format output HARUS persis seperti ini:
1. [balasan pertama]
2. [balasan kedua]"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 512}
    }

    try:
        resp = requests.post(url, json=payload, timeout=20)
        if resp.status_code == 400:
            return None, "API key tidak valid. Cek kembali API key kamu."
        if resp.status_code == 429:
            return None, "Quota API habis. Coba lagi nanti."
        if resp.status_code != 200:
            return None, f"Error {resp.status_code}: {resp.text[:80]}"
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        return text, None
    except requests.exceptions.ConnectionError:
        return None, "Tidak ada koneksi internet."
    except requests.exceptions.Timeout:
        return None, "Timeout. Coba lagi."
    except Exception as e:
        return None, f"Error: {str(e)[:80]}"

# ── TAMPILKAN HASIL ───────────────────────────────────────────────────────────
def display_results(hasil, style_name, lang_name):
    print()
    print(c(f"  ✦ Gaya   : {style_name}", "cyan"))
    print(c(f"  ✦ Bahasa : {lang_name}", "cyan"))
    divider("cyan")
    print()

    lines = [l.strip() for l in hasil.split("\n") if l.strip()]
    reply_num = 0
    for line in lines:
        if line.startswith("1.") or line.startswith("2."):
            reply_num += 1
            teks = line[2:].strip()
            print(c(f"  Balasan {reply_num}:", "yellow", True))
            print()
            # Word wrap balasan
            wrapped = textwrap.wrap(teks, width=56)
            for wl in wrapped:
                print(c(f"    {wl}", "white"))
            print()
            divider()
            print()

    if reply_num == 0:
        # Fallback kalau format tidak sesuai
        print(c("  Hasil:", "yellow", True))
        print()
        for line in lines:
            wrapped = textwrap.wrap(line, width=56)
            for wl in wrapped:
                print(c(f"    {wl}", "white"))
        print()

def pilih_menu(prompt_text, pilihan_dict, allow_enter=False):
    """Tampilkan menu dan minta input."""
    for k, v in pilihan_dict.items():
        nama = v[0]
        print(f"  {c(k, 'cyan', True)}  {nama}")
    print()
    while True:
        val = input(c(f"  {prompt_text} » ", "green", True)).strip()
        if allow_enter and val == "":
            return list(pilihan_dict.keys())[0]
        if val in pilihan_dict:
            return val
        print(c("  Pilihan tidak valid, coba lagi.", "red"))

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    cls()
    print_header()
    print()

    # Cek dependensi
    if not HAS_REQUESTS:
        print(c("  ✗ requests belum terinstall.", "red"))
        print(c("  → pip install requests", "yellow"))
        print()
        sys.exit(1)

    if not HAS_COLOR:
        print("  ⚠ colorama belum terinstall (opsional)")
        print("  → pip install colorama")
        print()

    # Cek API key
    if not API_KEY:
        print(c("  ✗ GEMINI_API_KEY belum diset!", "red"))
        print()
        print(c("  Cara set API key (pilih salah satu):", "yellow"))
        print(c("  1. Buat file .env di folder yang sama:", "gray"))
        print(c("       echo 'GEMINI_API_KEY=AIza...' > .env", "cyan"))
        print(c("  2. Export di terminal:", "gray"))
        print(c("       export GEMINI_API_KEY=AIza...", "cyan"))
        print(c("  3. Daftar gratis: aistudio.google.com/app/apikey", "gray"))
        print()

        # Tanya langsung
        key_input = input(c("  Masukkan API key sekarang (atau Enter untuk keluar) » ", "green")).strip()
        if not key_input:
            print(c("\n  Keluar.\n", "gray"))
            sys.exit(0)

        globals()["API_KEY"] = key_input
        print()

    print(c("  Siap! Ketik 'k' kapanpun untuk keluar.\n", "gray"))
    if _env_file:
        print(c(f"  ✓ .env terbaca dari: {_env_file}", "green"))
        print()

    while True:
        cls()
        print_header()
        print()

        # ── Input pesan ──
        print(c("  📨 PESAN YANG MAU DIBALAS", "cyan", True))
        divider()
        print(c("  Paste pesan di bawah ini.", "gray"))
        print(c("  (Ketik 'k' untuk keluar)\n", "gray"))

        pesan = input(c("  Pesan » ", "green", True)).strip()
        if pesan.lower() in ("k", "keluar", "exit", "quit"):
            print(c("\n  Sampai jumpa! 👋\n", "cyan"))
            break
        if not pesan:
            continue

        print()
        print(c(f"  Pesan  : ", "gray") + c(f'"{pesan[:60]}{"..." if len(pesan)>60 else ""}"', "white"))
        print(c(f"  Panjang: ", "gray") + c(f"{len(pesan)} karakter", "yellow"))
        print()

        # ── Pilih gaya ──
        print(c("  🎨 PILIH GAYA BALASAN", "cyan", True))
        divider()
        style_key  = pilih_menu("Gaya", STYLES)
        style_name = STYLES[style_key][0]
        style_desc = STYLES[style_key][1]
        print()

        # ── Pilih bahasa ──
        print(c("  🌐 PILIH BAHASA", "cyan", True))
        divider()
        lang_key  = pilih_menu("Bahasa", LANGS)
        lang_name = LANGS[lang_key][0]
        lang_desc = LANGS[lang_key][1]
        print()

        # ── Generate ──
        print(c("  ⏳ Sedang membuat balasan...", "yellow", True))
        hasil, err = generate_replies(pesan, style_desc, lang_desc)

        if err:
            print()
            print(c(f"  ✗ {err}", "red"))
            print()
            input(c("  Tekan Enter untuk coba lagi...", "gray"))
            continue

        cls()
        print_header()
        print()
        print(c("  ✅ Balasan siap!", "green", True))
        print()

        display_results(hasil, style_name, lang_name)

        # ── Aksi setelah hasil ──
        print(c("  Apa selanjutnya?", "white"))
        print(f"  {c('1', 'cyan', True)}  Balas pesan lain")
        print(f"  {c('2', 'cyan', True)}  Ganti gaya/bahasa (pesan sama)")
        print(f"  {c('k', 'gray')}  Keluar")
        print()

        aksi = input(c("  Pilih » ", "green", True)).strip().lower()
        if aksi == "k":
            print(c("\n  Sampai jumpa! 👋\n", "cyan"))
            break
        elif aksi == "2":
            # Ulang dengan pesan yang sama
            while True:
                cls()
                print_header()
                print()
                print(c(f"  Pesan: ", "gray") + c(f'"{pesan[:60]}"', "white"))
                print()

                print(c("  🎨 PILIH GAYA BALASAN", "cyan", True))
                divider()
                style_key  = pilih_menu("Gaya", STYLES)
                style_name = STYLES[style_key][0]
                style_desc = STYLES[style_key][1]
                print()

                print(c("  🌐 PILIH BAHASA", "cyan", True))
                divider()
                lang_key  = pilih_menu("Bahasa", LANGS)
                lang_name = LANGS[lang_key][0]
                lang_desc = LANGS[lang_key][1]
                print()

                print(c("  ⏳ Sedang membuat balasan...", "yellow", True))
                hasil, err = generate_replies(pesan, style_desc, lang_desc)

                if err:
                    print(c(f"\n  ✗ {err}", "red"))
                    input(c("\n  Tekan Enter...", "gray"))
                    break

                cls()
                print_header()
                print()
                print(c("  ✅ Balasan siap!", "green", True))
                print()
                display_results(hasil, style_name, lang_name)

                lagi = input(c("  Ganti gaya lagi? (y/n) » ", "green")).strip().lower()
                if lagi != "y":
                    break
        # aksi == "1" atau lainnya → lanjut loop utama

# ── ENTRY ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(c("\n\n  Dihentikan. Sampai jumpa! 👋\n", "gray"))
        sys.exit(0)
