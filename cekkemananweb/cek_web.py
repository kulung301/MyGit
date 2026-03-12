#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════╗
║         CEK KEAMANAN WEBSITE v1.0                ║
║   SSL · WHOIS · VirusTotal · SafeBrowsing · More ║
╚══════════════════════════════════════════════════╝

Install dependensi:
  pip install requests python-whois colorama

API Keys (opsional tapi disarankan):
  - VirusTotal  : https://www.virustotal.com/gui/join-us
  - Google Safe Browsing : https://developers.google.com/safe-browsing
  - URLScan.io  : https://urlscan.io/user/signup

Cara pakai:
  python cek_website.py
  python cek_website.py https://contoh.com
"""

import sys
import os
import re
import ssl
import socket
import json
import time
import hashlib
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone

# ── Cek & import dependensi ───────────────────────────────────────────────────
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import whois as whois_lib
    HAS_WHOIS = True
except ImportError:
    HAS_WHOIS = False

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

# ── CONFIG API KEYS ───────────────────────────────────────────────────────────
# Isi API key kamu di sini, atau biarkan kosong untuk skip cek tersebut
CONFIG = {
    "VIRUSTOTAL_API_KEY":      os.environ.get("VT_API_KEY", ""),
    "GOOGLE_SAFEBROWSING_KEY": os.environ.get("GSB_API_KEY", ""),
    "URLSCAN_API_KEY":         os.environ.get("URLSCAN_KEY", ""),
}

# ── WARNA ─────────────────────────────────────────────────────────────────────
def c(text, color="white", bold=False):
    if not HAS_COLOR:
        return text
    colors = {
        "green":  Fore.GREEN,
        "red":    Fore.RED,
        "yellow": Fore.YELLOW,
        "cyan":   Fore.CYAN,
        "blue":   Fore.BLUE,
        "magenta":Fore.MAGENTA,
        "white":  Fore.WHITE,
        "gray":   Fore.WHITE + Style.DIM,
    }
    col = colors.get(color, Fore.WHITE)
    bold_str = Style.BRIGHT if bold else ""
    return f"{bold_str}{col}{text}{Style.RESET_ALL}"

def print_header():
    print()
    print(c("╔══════════════════════════════════════════════════╗", "cyan"))
    print(c("║", "cyan") + c("         CEK KEAMANAN WEBSITE v1.0              ", "white", True) + c("  ║", "cyan"))
    print(c("║", "cyan") + c("   SSL · WHOIS · VirusTotal · Safe · URLScan    ", "gray") + c("║", "cyan"))
    print(c("╚══════════════════════════════════════════════════╝", "cyan"))
    print()

def print_section(title, icon="▶"):
    print()
    print(c(f"  {icon} {title}", "cyan", True))
    print(c("  " + "─" * 46, "blue"))

def print_result(label, value, status="ok"):
    colors = {"ok": "green", "warn": "yellow", "bad": "red", "info": "cyan", "gray": "gray"}
    icons  = {"ok": "✓", "warn": "⚠", "bad": "✗", "info": "●", "gray": "–"}
    col = colors.get(status, "white")
    ico = icons.get(status, " ")
    print(f"  {c(ico, col)}  {c(label+':', 'gray'):<28} {c(str(value), col)}")

# ── SKOR ──────────────────────────────────────────────────────────────────────
class Score:
    def __init__(self):
        self.points = 100
        self.issues = []
        self.warnings = []
        self.goods = []

    def deduct(self, pts, reason):
        self.points -= pts
        self.issues.append(f"-{pts}  {reason}")

    def warn(self, reason):
        self.points -= 5
        self.warnings.append(f" ⚠  {reason}")

    def good(self, reason):
        self.goods.append(f" ✓  {reason}")

    def get(self):
        return max(0, min(100, self.points))

    def label(self):
        s = self.get()
        if s >= 80: return "AMAN",    "green"
        if s >= 60: return "WASPADA", "yellow"
        if s >= 40: return "BERBAHAYA","red"
        return "SANGAT BERBAHAYA", "red"

# ── 1. NORMALIZE URL ──────────────────────────────────────────────────────────
def normalize_url(url):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url

def extract_domain(url):
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc or parsed.path
    domain = domain.split(":")[0].lower()
    domain = re.sub(r'^www\.', '', domain)
    return domain

# ── 2. CEK SSL ────────────────────────────────────────────────────────────────
def check_ssl(url, domain, score):
    print_section("SSL & HTTPS", "🔒")
    results = {}

    # HTTPS?
    if url.startswith("https://"):
        print_result("Protokol", "HTTPS ✓", "ok")
        score.good("Menggunakan HTTPS")
        results["https"] = True
    else:
        print_result("Protokol", "HTTP (tidak aman!)", "bad")
        score.deduct(30, "Tidak menggunakan HTTPS")
        results["https"] = False
        return results

    # SSL Certificate
    try:
        ctx = ssl.create_default_context()
        conn = ctx.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=domain
        )
        conn.settimeout(8)
        conn.connect((domain, 443))
        cert = conn.getpeercert()
        conn.close()

        # Expiry
        expire_str = cert.get('notAfter', '')
        if expire_str:
            expire_dt = datetime.strptime(expire_str, "%b %d %H:%M:%S %Y %Z")
            expire_dt = expire_dt.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            days_left = (expire_dt - now).days
            if days_left < 0:
                print_result("Sertifikat SSL", f"KADALUARSA {abs(days_left)} hari lalu!", "bad")
                score.deduct(40, "Sertifikat SSL kadaluarsa")
            elif days_left < 14:
                print_result("Sertifikat SSL", f"Hampir expired ({days_left} hari lagi)", "warn")
                score.warn("SSL hampir expired")
            else:
                print_result("Sertifikat SSL", f"Valid ({days_left} hari lagi)", "ok")
                score.good("SSL valid")
            results["ssl_days"] = days_left

        # Issuer
        issuer = dict(x[0] for x in cert.get('issuer', []))
        org = issuer.get('organizationName', issuer.get('commonName', 'Unknown'))
        print_result("Penerbit SSL", org, "info")
        results["ssl_issuer"] = org

        # Subject
        subject = dict(x[0] for x in cert.get('subject', []))
        cn = subject.get('commonName', 'Unknown')
        print_result("Sertifikat untuk", cn, "info")

        # Wildcard
        if cn.startswith("*"):
            print_result("Wildcard SSL", "Ya (kurang spesifik)", "warn")
            score.warn("Menggunakan wildcard SSL")
        results["ssl_cn"] = cn

    except ssl.SSLCertVerificationError as e:
        print_result("Verifikasi SSL", f"GAGAL: {str(e)[:50]}", "bad")
        score.deduct(35, "SSL tidak dapat diverifikasi")
    except ssl.SSLError as e:
        print_result("SSL Error", str(e)[:60], "bad")
        score.deduct(20, f"SSL error: {str(e)[:40]}")
    except (socket.timeout, ConnectionRefusedError):
        print_result("Koneksi SSL", "Timeout / ditolak", "warn")
    except Exception as e:
        print_result("SSL", f"Error: {str(e)[:50]}", "warn")

    # Cek HTTP headers keamanan
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            headers = {k.lower(): v for k, v in resp.getheaders()}

            hsts = headers.get("strict-transport-security", "")
            if hsts:
                print_result("HSTS", "Aktif ✓", "ok")
                score.good("HSTS aktif")
            else:
                print_result("HSTS", "Tidak ada", "warn")
                score.warn("HSTS tidak aktif")

            csp = headers.get("content-security-policy", "")
            print_result("Content-Security-Policy", "Ada ✓" if csp else "Tidak ada", "ok" if csp else "warn")

            xframe = headers.get("x-frame-options", "")
            print_result("X-Frame-Options", xframe if xframe else "Tidak ada", "ok" if xframe else "warn")

            server = headers.get("server", "")
            if server:
                print_result("Server", server, "info")
                # Server yang expose versi = kurang aman
                if any(v in server for v in ["Apache/2.2", "nginx/1.1", "IIS/6", "IIS/7"]):
                    score.warn("Server mengekspos versi lama")

            results["headers"] = dict(headers)

    except urllib.error.HTTPError as e:
        print_result("HTTP Status", f"{e.code} ({e.reason})", "warn" if e.code < 500 else "bad")
    except urllib.error.URLError as e:
        print_result("Koneksi", f"Gagal: {str(e.reason)[:50]}", "bad")
        score.deduct(20, "Website tidak dapat diakses")
    except Exception as e:
        print_result("Header check", f"Error: {str(e)[:50]}", "warn")

    return results

# ── 3. CEK WHOIS / UMUR DOMAIN ────────────────────────────────────────────────
def check_whois(domain, score):
    print_section("WHOIS & Umur Domain", "📅")

    if not HAS_WHOIS:
        print(c("  ⚠  python-whois tidak terinstall. Jalankan: pip install python-whois", "yellow"))
        return {}

    try:
        w = whois_lib.whois(domain)
        results = {}

        # Tanggal registrasi
        created = w.creation_date
        if isinstance(created, list):
            created = created[0]

        if created:
            if isinstance(created, str):
                try:
                    created = datetime.strptime(created[:10], "%Y-%m-%d")
                except:
                    created = None

        if created:
            created = created.replace(tzinfo=None)
            now = datetime.now()
            age_days = (now - created).days
            age_years = age_days // 365
            age_months = (age_days % 365) // 30

            age_str = ""
            if age_years > 0:
                age_str = f"{age_years} tahun {age_months} bulan"
            else:
                age_str = f"{age_days} hari"

            if age_days < 30:
                print_result("Umur Domain", f"{age_str} ← BARU SEKALI!", "bad")
                score.deduct(35, "Domain baru dibuat (<30 hari) — sangat mencurigakan")
            elif age_days < 90:
                print_result("Umur Domain", f"{age_str} ← Cukup baru", "warn")
                score.warn("Domain baru (<90 hari)")
            elif age_days < 365:
                print_result("Umur Domain", f"{age_str}", "warn")
                score.warn("Domain kurang dari 1 tahun")
            else:
                print_result("Umur Domain", f"{age_str}", "ok")
                score.good("Domain sudah lama (lebih terpercaya)")

            print_result("Dibuat", created.strftime("%d %b %Y"), "info")
            results["age_days"] = age_days
        else:
            print_result("Umur Domain", "Tidak ditemukan", "gray")

        # Expired
        expired = w.expiration_date
        if isinstance(expired, list):
            expired = expired[0]
        if expired:
            if isinstance(expired, str):
                try:
                    expired = datetime.strptime(expired[:10], "%Y-%m-%d")
                except:
                    expired = None
        if expired:
            expired = expired.replace(tzinfo=None)
            days_to_exp = (expired - datetime.now()).days
            if days_to_exp < 0:
                print_result("Masa Aktif", "SUDAH KADALUARSA!", "bad")
                score.deduct(20, "Domain sudah kadaluarsa")
            elif days_to_exp < 30:
                print_result("Masa Aktif", f"Berakhir {days_to_exp} hari lagi!", "warn")
                score.warn("Domain hampir expired")
            else:
                print_result("Berakhir", expired.strftime("%d %b %Y"), "info")

        # Registrar
        registrar = w.registrar
        if registrar:
            print_result("Registrar", str(registrar)[:40], "info")
            results["registrar"] = str(registrar)

        # WHOIS privacy / redacted
        name = str(w.name or "")
        org  = str(w.org or "")
        if "privacy" in name.lower() or "redacted" in name.lower() or \
           "privacy" in org.lower()  or "redacted" in org.lower():
            print_result("Privasi WHOIS", "Disembunyikan (privacy protection)", "warn")
            score.warn("WHOIS disembunyikan — identitas pemilik tidak diketahui")
        elif name and name not in ("None", ""):
            print_result("Pemilik", name[:40], "info")

        # Country
        country = w.country
        if country:
            print_result("Negara", str(country), "info")

        return results

    except Exception as e:
        err = str(e)
        if "No match" in err or "not found" in err.lower():
            print_result("WHOIS", "Domain tidak ditemukan / privat", "warn")
            score.warn("WHOIS tidak tersedia")
        else:
            print_result("WHOIS Error", err[:60], "warn")
        return {}

# ── 4. VIRUSTOTAL ────────────────────────────────────────────────────────────
def check_virustotal(url, score):
    print_section("VirusTotal", "🛡️")

    api_key = CONFIG["VIRUSTOTAL_API_KEY"]
    if not api_key:
        print(c("  –  API key tidak diset. Set: export VT_API_KEY=xxx", "gray"))
        print(c("  –  Daftar gratis di: virustotal.com/gui/join-us", "gray"))
        return {}

    if not HAS_REQUESTS:
        print(c("  ⚠  requests tidak terinstall. Jalankan: pip install requests", "yellow"))
        return {}

    try:
        # Encode URL ke base64url (format VT)
        import base64
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

        headers = {"x-apikey": api_key}
        resp = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers, timeout=15
        )

        if resp.status_code == 404:
            # Submit dulu
            print(c("  ●  URL belum ada di VT, submit untuk analisis...", "cyan"))
            r2 = requests.post(
                "https://www.virustotal.com/api/v3/urls",
                headers=headers,
                data={"url": url},
                timeout=15
            )
            if r2.status_code == 200:
                analysis_id = r2.json().get("data", {}).get("id", "")
                print(c("  ●  Menunggu hasil analisis (15 detik)...", "cyan"))
                time.sleep(15)
                r3 = requests.get(
                    f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
                    headers=headers, timeout=15
                )
                if r3.status_code == 200:
                    stats = r3.json().get("data", {}).get("attributes", {}).get("stats", {})
                else:
                    print_result("VT Analisis", "Gagal mendapatkan hasil", "warn")
                    return {}
            else:
                print_result("VT Submit", f"Error {r2.status_code}", "warn")
                return {}
        elif resp.status_code == 200:
            attrs = resp.json().get("data", {}).get("attributes", {})
            stats = attrs.get("last_analysis_stats", {})
            last_date = attrs.get("last_analysis_date", 0)
            if last_date:
                last_str = datetime.fromtimestamp(last_date).strftime("%d %b %Y")
                print_result("Terakhir dicek", last_str, "info")
        elif resp.status_code == 401:
            print_result("VT", "API key tidak valid", "warn")
            return {}
        else:
            print_result("VT", f"Error {resp.status_code}", "warn")
            return {}

        malicious  = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        harmless   = stats.get("harmless", 0)
        undetected = stats.get("undetected", 0)
        total = malicious + suspicious + harmless + undetected

        print_result("Berbahaya",   f"{malicious}/{total} engine",  "bad"  if malicious > 0  else "ok")
        print_result("Mencurigakan",f"{suspicious}/{total} engine", "warn" if suspicious > 0 else "ok")
        print_result("Aman",        f"{harmless}/{total} engine",   "ok")

        if malicious >= 5:
            score.deduct(50, f"VirusTotal: {malicious} engine deteksi berbahaya!")
        elif malicious >= 2:
            score.deduct(30, f"VirusTotal: {malicious} engine deteksi berbahaya")
        elif malicious >= 1:
            score.deduct(15, f"VirusTotal: 1 engine deteksi berbahaya")
        elif suspicious >= 3:
            score.warn(f"VirusTotal: {suspicious} engine mencurigakan")
        else:
            score.good("VirusTotal bersih")

        return stats

    except requests.exceptions.Timeout:
        print_result("VT", "Timeout (coba lagi)", "warn")
    except Exception as e:
        print_result("VT Error", str(e)[:60], "warn")
    return {}

# ── 5. GOOGLE SAFE BROWSING ───────────────────────────────────────────────────
def check_safe_browsing(url, score):
    print_section("Google Safe Browsing", "🔍")

    api_key = CONFIG["GOOGLE_SAFEBROWSING_KEY"]
    if not api_key:
        print(c("  –  API key tidak diset. Set: export GSB_API_KEY=xxx", "gray"))
        print(c("  –  Daftar gratis di: console.cloud.google.com", "gray"))
        return {}

    if not HAS_REQUESTS:
        print(c("  ⚠  requests tidak terinstall", "yellow"))
        return {}

    try:
        payload = {
            "client": {"clientId": "cek-website-bot", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": [
                    "MALWARE", "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"
                ],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }

        resp = requests.post(
            f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}",
            json=payload, timeout=10
        )

        if resp.status_code == 200:
            data = resp.json()
            matches = data.get("matches", [])

            if matches:
                for m in matches:
                    threat = m.get("threatType", "UNKNOWN")
                    print_result("Ancaman", threat.replace("_", " "), "bad")
                score.deduct(60, f"Google Safe Browsing: {len(matches)} ancaman ditemukan!")
            else:
                print_result("Status", "Tidak ada ancaman ✓", "ok")
                score.good("Google Safe Browsing bersih")
        elif resp.status_code == 400:
            print_result("GSB", "API key tidak valid", "warn")
        else:
            print_result("GSB", f"Error {resp.status_code}", "warn")

        return {"matches": len(matches) if resp.status_code == 200 else 0}

    except Exception as e:
        print_result("GSB Error", str(e)[:60], "warn")
    return {}

# ── 6. URLSCAN.IO ─────────────────────────────────────────────────────────────
def check_urlscan(url, domain, score):
    print_section("URLScan.io", "🔭")

    if not HAS_REQUESTS:
        print(c("  ⚠  requests tidak terinstall", "yellow"))
        return {}

    api_key = CONFIG["URLSCAN_API_KEY"]

    try:
        # Search dulu (tanpa API key pun bisa)
        search_resp = requests.get(
            f"https://urlscan.io/api/v1/search/?q=domain:{domain}&size=1",
            timeout=10
        )

        if search_resp.status_code == 200:
            results = search_resp.json().get("results", [])
            if results:
                latest = results[0]
                page = latest.get("page", {})
                verdicts = latest.get("verdicts", {})
                overall = verdicts.get("overall", {})

                scan_date = latest.get("task", {}).get("time", "")
                if scan_date:
                    print_result("Terakhir scan", scan_date[:10], "info")

                # Verdict
                malicious = overall.get("malicious", False)
                score_vt  = overall.get("score", 0)

                if malicious:
                    print_result("Verdict", "BERBAHAYA!", "bad")
                    score.deduct(40, "URLScan: Website terdeteksi berbahaya")
                elif score_vt > 50:
                    print_result("Verdict", f"Mencurigakan (skor: {score_vt})", "warn")
                    score.warn(f"URLScan skor tinggi: {score_vt}")
                else:
                    print_result("Verdict", f"Aman (skor: {score_vt})", "ok")
                    score.good("URLScan bersih")

                # IP & server
                ip = page.get("ip", "")
                if ip:
                    print_result("IP Server", ip, "info")

                server = page.get("server", "")
                if server:
                    print_result("Web Server", server, "info")

                country = page.get("country", "")
                if country:
                    print_result("Negara Server", country, "info")

                # Screenshot URL
                screenshot = latest.get("screenshot", "")
                if screenshot:
                    print_result("Screenshot", screenshot[:60], "info")

            else:
                print_result("URLScan", "Belum pernah di-scan", "gray")

                # Submit scan baru jika ada API key
                if api_key:
                    print(c("  ●  Submit scan baru...", "cyan"))
                    headers = {"API-Key": api_key, "Content-Type": "application/json"}
                    sub = requests.post(
                        "https://urlscan.io/api/v1/scan/",
                        headers=headers,
                        json={"url": url, "visibility": "private"},
                        timeout=10
                    )
                    if sub.status_code == 200:
                        result_url = sub.json().get("result", "")
                        print_result("Scan dikirim", result_url[:60] if result_url else "OK", "ok")
                    else:
                        print_result("Submit scan", f"Error {sub.status_code}", "warn")
                else:
                    print(c("  –  Set URLSCAN_KEY untuk submit scan baru", "gray"))

        elif search_resp.status_code == 429:
            print_result("URLScan", "Rate limit, coba lagi nanti", "warn")
        else:
            print_result("URLScan", f"Error {search_resp.status_code}", "warn")

    except Exception as e:
        print_result("URLScan Error", str(e)[:60], "warn")

    return {}

# ── 7. DETEKSI TYPOSQUATTING ──────────────────────────────────────────────────
KNOWN_CRYPTO_SITES = [
    "binance.com", "coinbase.com", "kraken.com", "bybit.com", "okx.com",
    "kucoin.com", "huobi.com", "gate.io", "mexc.com", "bitget.com",
    "metamask.io", "phantom.app", "trustwallet.com", "ledger.com",
    "uniswap.org", "pancakeswap.finance", "aave.com", "compound.finance",
    "opensea.io", "blur.io", "magiceden.io",
    "ethereum.org", "bitcoin.org", "solana.com", "polygon.technology",
    "arbitrum.io", "optimism.io", "base.org", "linea.build",
    "grass.io", "nodepay.ai", "getgrass.io",
    "layerzero.network", "starknet.io", "zksync.io",
    "ton.org", "sui.io", "aptos.dev",
    "discord.com", "discord.gg", "twitter.com", "x.com", "telegram.org",
]

def levenshtein(s1, s2):
    """Hitung jarak edit antara dua string."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j+1]+1, curr[j]+1, prev[j]+(c1!=c2)))
        prev = curr
    return prev[len(s2)]

def check_typosquatting(domain, score):
    print_section("Deteksi Typosquatting", "👀")

    results = []

    # Cek apakah ada karakter homoglyph
    homoglyphs = {
        '0': 'o', 'l': '1', 'i': '1', 'rn': 'm',
        'vv': 'w', '3': 'e', '4': 'a', '5': 's',
    }
    for fake, real in homoglyphs.items():
        if fake in domain:
            print_result("Karakter mencurigakan",
                         f"'{fake}' mungkin meniru '{real}'", "warn")
            score.warn(f"Karakter homoglyph: '{fake}' mirip '{real}'")

    # Cek kesamaan dengan domain terkenal
    domain_base = domain.split('.')[0].lower()
    suspicious_matches = []

    for known in KNOWN_CRYPTO_SITES:
        known_base = known.split('.')[0].lower()

        # Persis sama = aman (itu memang sitenya)
        if domain == known:
            print_result("Domain dikenal", f"✓ {known}", "ok")
            score.good(f"Domain resmi: {known}")
            return {"exact_match": known}

        # Jarak edit kecil = mencurigakan
        dist = levenshtein(domain_base, known_base)
        similarity = 1 - (dist / max(len(domain_base), len(known_base)))

        if dist == 1 or (similarity > 0.85 and dist <= 2):
            suspicious_matches.append((known, dist, round(similarity * 100)))

        # Subdomain spoof: known.com.evil.com
        if known.replace('.', '-') in domain or known.split('.')[0] + '.' in domain:
            if domain != known:
                suspicious_matches.append((known, 0, 95))

    if suspicious_matches:
        suspicious_matches.sort(key=lambda x: x[1])
        for known, dist, sim in suspicious_matches[:3]:
            print_result("Mirip dengan", f"{known} (kemiripan {sim}%)", "bad")
        score.deduct(30, f"Domain mirip dengan {suspicious_matches[0][0]} — kemungkinan phishing!")
    else:
        print_result("Typosquatting", "Tidak mirip domain terkenal", "ok")
        score.good("Tidak terdeteksi typosquatting")

    # Cek TLD mencurigakan
    suspicious_tlds = ['.xyz', '.tk', '.ml', '.ga', '.cf', '.gq', '.top', '.icu',
                       '.club', '.online', '.site', '.website', '.live', '.pw']
    domain_tld = '.' + domain.split('.')[-1]
    if domain_tld in suspicious_tlds:
        print_result("TLD", f"{domain_tld} (sering dipakai scammer)", "warn")
        score.warn(f"TLD mencurigakan: {domain_tld}")
    else:
        print_result("TLD", domain_tld, "ok")

    # Cek jumlah subdomain (banyak subdomain = mencurigakan)
    parts = domain.split('.')
    if len(parts) > 3:
        print_result("Subdomain",
                     f"{len(parts)-2} level (mencurigakan)", "warn")
        score.warn("Terlalu banyak subdomain")

    # Cek panjang domain
    if len(domain_base) > 25:
        print_result("Panjang domain",
                     f"{len(domain_base)} karakter (panjang sekali)", "warn")
        score.warn("Domain sangat panjang")

    # Kata berbahaya dalam domain
    danger_words = ["login", "signin", "verify", "secure", "account",
                    "wallet", "connect", "claim", "airdrop", "free",
                    "giveaway", "reward", "bonus", "official"]
    found_words = [w for w in danger_words if w in domain_base]
    if found_words:
        print_result("Kata sensitif",
                     ", ".join(found_words), "warn")
        score.warn(f"Domain mengandung kata sensitif: {', '.join(found_words)}")

    return {"suspicious": suspicious_matches}

# ── 8. CEK IP & REDIRECT ──────────────────────────────────────────────────────
def check_connectivity(url, domain, score):
    print_section("Konektivitas & IP", "🌐")

    # IP lookup
    try:
        ip = socket.gethostbyname(domain)
        print_result("IP Address", ip, "info")

        # IP langsung (bukan domain)?
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):
            print_result("Format URL", "Pakai IP langsung (mencurigakan)", "warn")
            score.warn("URL menggunakan IP langsung bukan domain")

    except socket.gaierror:
        print_result("DNS", "Domain tidak bisa di-resolve!", "bad")
        score.deduct(25, "Domain tidak dapat ditemukan")
        return {}

    # Cek redirect
    if not HAS_REQUESTS:
        return {}

    try:
        resp = requests.get(url, timeout=10, allow_redirects=True,
                            headers={"User-Agent": "Mozilla/5.0"})
        history = resp.history

        if history:
            print_result("Redirect", f"{len(history)}x redirect", "warn" if len(history) > 2 else "info")
            final = resp.url
            final_domain = extract_domain(final)
            if final_domain != domain:
                print_result("Redirect ke", final_domain, "warn")
                score.warn(f"Redirect ke domain berbeda: {final_domain}")
        else:
            print_result("Redirect", "Tidak ada redirect", "ok")

        print_result("HTTP Status", str(resp.status_code),
                     "ok" if resp.status_code < 400 else "bad")

        # Response time
        elapsed = resp.elapsed.total_seconds()
        print_result("Response Time", f"{elapsed:.2f} detik",
                     "ok" if elapsed < 3 else "warn")

    except requests.exceptions.ConnectionError:
        print_result("Koneksi", "Gagal terhubung", "bad")
        score.deduct(20, "Tidak dapat terhubung ke website")
    except Exception as e:
        print_result("Error", str(e)[:50], "warn")

    return {}

# ── SKOR FINAL ────────────────────────────────────────────────────────────────
def print_final_score(score, url):
    s = score.get()
    label, color = score.label()

    print()
    print(c("  ╔══════════════════════════════════════════╗", color))
    print(c("  ║", color) + f"  SKOR KEAMANAN: " +
          c(f"{s}/100", color, True) + f"  —  " +
          c(f"{label}", color, True) +
          " " * max(0, 10 - len(label)) +
          c("  ║", color))
    print(c("  ╚══════════════════════════════════════════╝", color))

    # Progress bar
    bar_filled = int(s / 5)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)
    print(f"\n  [{c(bar, color)}] {c(str(s)+'%', color, True)}\n")

    # Issues
    if score.issues:
        print(c("  ✗ Masalah ditemukan:", "red", True))
        for issue in score.issues:
            print(c(f"    {issue}", "red"))

    if score.warnings:
        print(c("\n  ⚠ Peringatan:", "yellow", True))
        for warn in score.warnings:
            print(c(f"    {warn}", "yellow"))

    if score.goods:
        print(c("\n  ✓ Yang baik:", "green", True))
        for good in score.goods:
            print(c(f"    {good}", "green"))

    # Rekomendasi
    print()
    print(c("  📋 Rekomendasi:", "cyan", True))
    if s >= 80:
        print(c("  ✓ Website ini tampak aman. Tetap waspada!", "green"))
    elif s >= 60:
        print(c("  ⚠ Lanjutkan dengan hati-hati.", "yellow"))
        print(c("  ⚠ Jangan masukkan private key atau seed phrase!", "yellow"))
    elif s >= 40:
        print(c("  ✗ BERBAHAYA. Hindari website ini.", "red"))
        print(c("  ✗ Jangan klik tombol apapun!", "red"))
    else:
        print(c("  ✗ SANGAT BERBAHAYA. Tutup segera!", "red", True))
        print(c("  ✗ Kemungkinan besar PHISHING / SCAM!", "red", True))

    print()
    print(c(f"  URL yang dicek: {url}", "gray"))
    print(c(f"  Waktu: {datetime.now().strftime('%d %b %Y %H:%M:%S')}", "gray"))
    print()

# ── MAIN ──────────────────────────────────────────────────────────────────────
def scan(url_input):
    url = normalize_url(url_input)
    domain = extract_domain(url)

    print_header()
    print(c(f"  🔗 Target  : ", "gray") + c(url, "cyan", True))
    print(c(f"  🌐 Domain  : ", "gray") + c(domain, "white", True))
    print(c(f"  ⏱  Waktu   : ", "gray") + c(datetime.now().strftime("%d %b %Y %H:%M:%S"), "gray"))
    print()
    print(c("  Memulai scan...", "gray"))

    score = Score()

    check_ssl(url, domain, score)
    check_whois(domain, score)
    check_virustotal(url, score)
    check_safe_browsing(url, score)
    check_urlscan(url, domain, score)
    check_typosquatting(domain, score)
    check_connectivity(url, domain, score)

    print_final_score(score, url)

def interactive_mode():
    print_header()
    print(c("  Cek keamanan website sebelum kamu buka.", "gray"))
    print(c("  Ketik 'keluar' untuk exit.\n", "gray"))

    # Cek dependensi
    missing = []
    if not HAS_REQUESTS: missing.append("requests")
    if not HAS_WHOIS:    missing.append("python-whois")
    if not HAS_COLOR:    missing.append("colorama")

    if missing:
        print(c(f"  ⚠  Library kurang: {', '.join(missing)}", "yellow"))
        print(c(f"  →  pip install {' '.join(missing)}\n", "yellow"))

    # Cek API keys
    no_key = []
    if not CONFIG["VIRUSTOTAL_API_KEY"]:      no_key.append("VT_API_KEY (VirusTotal)")
    if not CONFIG["GOOGLE_SAFEBROWSING_KEY"]: no_key.append("GSB_API_KEY (Google SafeBrowsing)")
    if not CONFIG["URLSCAN_API_KEY"]:         no_key.append("URLSCAN_KEY (URLScan.io)")

    if no_key:
        print(c("  ℹ  API key tidak diset (fitur terbatas):", "blue"))
        for k in no_key:
            print(c(f"    – {k}", "gray"))
        print(c("  →  Set via: export VT_API_KEY=xxx", "gray"))
        print()

    while True:
        try:
            url_input = input(c("  Masukkan URL » ", "green", True)).strip()
            if not url_input:
                continue
            if url_input.lower() in ("keluar", "exit", "quit", "k", "q"):
                print(c("\n  Sampai jumpa!\n", "cyan"))
                break
            scan(url_input)
            print(c("  " + "─" * 46 + "\n", "blue"))
        except KeyboardInterrupt:
            print(c("\n\n  Dihentikan.\n", "gray"))
            break
        except EOFError:
            break

# ── ENTRY ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1:
        scan(sys.argv[1])
    else:
        interactive_mode()
