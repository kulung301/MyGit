"""
Scalping Bot - MODE SIMULASI PENUH
====================================
- Menggunakan CoinGecko Public API (WORKS di Indonesia!)
- Tidak perlu API Key, tidak perlu dana nyata
- Harga & Data OHLC REAL dari CoinGecko
"""

import time
import requests
import logging
from datetime import datetime

# ──────────────────────────────────────────────
# KONFIGURASI
# ──────────────────────────────────────────────
CONFIG = {
    # Coin ID CoinGecko: bitcoin, ethereum, solana, binancecoin, dll
    "coin_id":           "bitcoin",
    "vs_currency":       "usd",
    "modal_awal":        1000.0,    # Modal virtual (USDT)
    "trade_pct":         0.10,      # 10% modal per trade
    "stop_loss_pct":     0.005,     # Stop Loss 0.5%
    "take_profit_pct":   0.010,     # Take Profit 1.0%
    "ema_fast":          9,
    "ema_slow":          21,
    "rsi_period":        14,
    "rsi_buy":           45,
    "rsi_sell":          60,
    "poll_seconds":      60,        # CoinGecko free: jangan < 60 detik
}

# ──────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    handlers=[
        logging.FileHandler("simulasi.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0"}


# ──────────────────────────────────────────────
# AMBIL DATA COINGECKO (PUBLIC - TANPA API KEY)
# ──────────────────────────────────────────────
def get_ohlc(coin_id, vs_currency="usd", days=1):
    """
    Ambil data OHLC dari CoinGecko.
    Format return: [[timestamp, open, close, high, low], ...]
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
    params = {"vs_currency": vs_currency, "days": days}
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        raw = r.json()
        if not raw or not isinstance(raw, list):
            log.error(f"Data tidak valid: {raw}")
            return []
        # CoinGecko: [timestamp, open, high, low, close]
        # Konversi → [timestamp, open, close, high, low]
        return [[c[0], c[1], c[4], c[2], c[3]] for c in raw]
    except requests.exceptions.Timeout:
        log.error("Timeout — koneksi lambat")
        return []
    except requests.exceptions.ConnectionError as e:
        log.error(f"Gagal konek: {e}")
        return []
    except Exception as e:
        log.error(f"Error: {e}")
        return []


def get_harga_sekarang(coin_id, vs_currency="usd"):
    """Ambil harga terkini."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin_id, "vs_currencies": vs_currency}
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = r.json()
        return float(data[coin_id][vs_currency])
    except:
        return None


def cek_koneksi(coin_id):
    """Cek apakah CoinGecko bisa diakses."""
    try:
        harga = get_harga_sekarang(coin_id)
        if harga:
            print(f"  ✅ CoinGecko OK! Harga {coin_id.upper()}: ${harga:,.2f}")
            return True
    except:
        pass
    print("  ❌ CoinGecko tidak bisa diakses")
    return False


# ──────────────────────────────────────────────
# INDIKATOR TEKNIKAL
# ──────────────────────────────────────────────
def calc_ema(prices, period):
    emas, k = [], 2 / (period + 1)
    for i, p in enumerate(prices):
        if i < period - 1:
            emas.append(None)
        elif i == period - 1:
            emas.append(sum(prices[:period]) / period)
        else:
            emas.append(p * k + emas[-1] * (1 - k))
    return emas


def calc_rsi(closes, period=14):
    if len(closes) < period + 1:
        return 50.0
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains  = [d if d > 0 else 0 for d in deltas[-period:]]
    losses = [-d if d < 0 else 0 for d in deltas[-period:]]
    avg_g  = sum(gains) / period
    avg_l  = sum(losses) / period
    if avg_l == 0:
        return 100.0
    return 100 - (100 / (1 + avg_g / avg_l))


# ──────────────────────────────────────────────
# SINYAL TRADING
# ──────────────────────────────────────────────
def generate_signal(candles, cfg):
    if len(candles) < cfg["ema_slow"] + 5:
        return "HOLD", {}

    closes = [float(c[2]) for c in candles]

    ema_fast = calc_ema(closes, cfg["ema_fast"])
    ema_slow = calc_ema(closes, cfg["ema_slow"])
    rsi      = calc_rsi(closes, cfg["rsi_period"])

    ef_now, es_now   = ema_fast[-1], ema_slow[-1]
    ef_prev, es_prev = ema_fast[-2], ema_slow[-2]

    if any(v is None for v in [ef_now, es_now, ef_prev, es_prev]):
        return "HOLD", {}

    info = {
        "rsi":      rsi,
        "ema_fast": ef_now,
        "ema_slow": es_now,
    }

    bullish = ef_prev <= es_prev and ef_now > es_now
    bearish = ef_prev >= es_prev and ef_now < es_now

    if bullish and rsi < cfg["rsi_buy"]:
        return "BUY", info
    if bearish and rsi > cfg["rsi_sell"]:
        return "SELL", info
    return "HOLD", info


# ──────────────────────────────────────────────
# BOT SIMULASI
# ──────────────────────────────────────────────
class SimulasiBot:
    def __init__(self, cfg):
        self.cfg      = cfg
        self.saldo    = cfg["modal_awal"]
        self.posisi   = None
        self.riwayat  = []
        self.trade_ke = 0

    def _print_header(self):
        print("\n" + "="*55)
        print("  🤖  SCALPING BOT — MODE SIMULASI PENUH")
        print("="*55)
        print(f"  Coin    : {self.cfg['coin_id'].upper()}/USD")
        print(f"  Modal   : ${self.cfg['modal_awal']:,.2f} (virtual)")
        print(f"  SL / TP : {self.cfg['stop_loss_pct']*100}% / "
              f"{self.cfg['take_profit_pct']*100}%")
        print(f"  Refresh : setiap {self.cfg['poll_seconds']} detik")
        print("="*55)
        print("  ✅  Tidak menggunakan dana nyata")
        print("  ✅  Tidak memerlukan API Key")
        print("  ✅  Data REAL dari CoinGecko")
        print("="*55 + "\n")

    def _cetak_status(self, harga, info):
        pnl_ur = 0
        if self.posisi:
            pnl_ur = (harga - self.posisi["entry"]) * self.posisi["size"]

        posisi_str = "Ada Posisi 📌" if self.posisi else "Kosong"
        print(f"\n┌─ {datetime.now().strftime('%H:%M:%S')} ──────────────────────────")
        print(f"│  💰 Harga     : ${harga:>12,.2f}")
        print(f"│  📊 RSI       : {info.get('rsi', 0):>8.1f}")
        print(f"│  📈 EMA {self.cfg['ema_fast']}/{self.cfg['ema_slow']}  "
              f": {info.get('ema_fast',0):,.2f} / {info.get('ema_slow',0):,.2f}")
        print(f"│  💼 Saldo     : ${self.saldo:>12,.2f}")
        print(f"│  📋 Posisi    : {posisi_str}")
        if self.posisi:
            sign = "+" if pnl_ur >= 0 else ""
            print(f"│  📍 Entry: ${self.posisi['entry']:,.2f} | "
                  f"SL: ${self.posisi['sl']:,.2f} | "
                  f"TP: ${self.posisi['tp']:,.2f}")
            print(f"│  💹 PnL  : {sign}${pnl_ur:.4f}")
        print(f"└──────────────────────────────────────────")

    def _buka_posisi(self, harga):
        dana  = self.saldo * self.cfg["trade_pct"]
        size  = round(dana / harga, 8)
        sl    = round(harga * (1 - self.cfg["stop_loss_pct"]), 2)
        tp    = round(harga * (1 + self.cfg["take_profit_pct"]), 2)
        self.posisi   = {"entry": harga, "size": size, "sl": sl, "tp": tp}
        self.trade_ke += 1
        print(f"\n  🟢 BELI #{self.trade_ke} ─────────────────────────")
        print(f"     Entry      : ${harga:,.2f}")
        print(f"     Size       : {size} BTC")
        print(f"     Dana       : ${dana:.2f}")
        print(f"     Stop Loss  : ${sl:,.2f}")
        print(f"     Take Profit: ${tp:,.2f}")

    def _tutup_posisi(self, harga, alasan):
        pnl        = (harga - self.posisi["entry"]) * self.posisi["size"]
        self.saldo += pnl
        self.riwayat.append(pnl)

        emoji = "✅" if pnl > 0 else "❌"
        sign  = "+" if pnl >= 0 else ""
        print(f"\n  {emoji} TUTUP — {alasan}")
        print(f"     Harga tutup : ${harga:,.2f}")
        print(f"     PnL trade   : {sign}${pnl:.4f}")
        print(f"     Saldo baru  : ${self.saldo:,.2f}")

        wins    = sum(1 for p in self.riwayat if p > 0)
        total   = len(self.riwayat)
        wr      = wins / total * 100
        tot_pnl = sum(self.riwayat)
        s2      = "+" if tot_pnl >= 0 else ""
        print(f"\n  📊 {total} trade | WR {wr:.0f}% | "
              f"Total PnL {s2}${tot_pnl:.4f}")
        self.posisi = None

    def _cek_exit(self, harga):
        if not self.posisi:
            return
        if harga <= self.posisi["sl"]:
            self._tutup_posisi(harga, "STOP LOSS 🔴")
        elif harga >= self.posisi["tp"]:
            self._tutup_posisi(harga, "TAKE PROFIT 🎯")

    def jalankan(self):
        self._print_header()

        print("  🔍 Mengecek koneksi ke CoinGecko...")
        if not cek_koneksi(self.cfg["coin_id"]):
            print("\n  ❌ Tidak bisa terhubung.")
            print("  💡 Coba ganti jaringan atau aktifkan VPN.\n")
            return

        print(f"\n  🚀 Bot berjalan! Tekan Ctrl+C untuk berhenti.\n")
        gagal = 0

        while True:
            try:
                candles = get_ohlc(
                    self.cfg["coin_id"],
                    self.cfg["vs_currency"],
                    days=1
                )

                if not candles:
                    gagal += 1
                    wait = min(30 * gagal, 120)
                    print(f"  ⚠️  Gagal ambil data ({gagal}x) — tunggu {wait}s...")
                    time.sleep(wait)
                    continue

                gagal = 0

                # Harga realtime untuk cek SL/TP
                harga_live = get_harga_sekarang(
                    self.cfg["coin_id"],
                    self.cfg["vs_currency"]
                )
                harga = harga_live if harga_live else float(candles[-1][2])

                signal, info = generate_signal(candles, self.cfg)

                self._cetak_status(harga, info)
                self._cek_exit(harga)

                if not self.posisi:
                    if signal == "BUY":
                        self._buka_posisi(harga)
                    else:
                        print(f"  ⏳ Sinyal: {signal} — menunggu peluang...")

                print(f"  (refresh {self.cfg['poll_seconds']}s | Ctrl+C stop)\n")
                time.sleep(self.cfg["poll_seconds"])

            except KeyboardInterrupt:
                self._ringkasan()
                break
            except Exception as e:
                log.error(f"Error: {e}")
                time.sleep(15)

    def _ringkasan(self):
        print("\n" + "="*55)
        print("  📊  RINGKASAN SESI SIMULASI")
        print("="*55)
        total = len(self.riwayat)
        if total == 0:
            print("  Belum ada trade yang selesai.")
        else:
            wins    = sum(1 for p in self.riwayat if p > 0)
            losses  = total - wins
            tot_pnl = sum(self.riwayat)
            wr      = wins / total * 100
            growth  = (self.saldo - self.cfg["modal_awal"]) / self.cfg["modal_awal"] * 100
            s1      = "+" if tot_pnl >= 0 else ""
            s2      = "+" if growth  >= 0 else ""
            print(f"  Total Trade  : {total}")
            print(f"  Win / Loss   : {wins} / {losses}")
            print(f"  Win Rate     : {wr:.1f}%")
            print(f"  Total PnL    : {s1}${tot_pnl:.4f}")
            print(f"  Modal Awal   : ${self.cfg['modal_awal']:,.2f}")
            print(f"  Saldo Akhir  : ${self.saldo:,.2f}")
            print(f"  Growth       : {s2}{growth:.2f}%")
        print("="*55)
        print("  Log tersimpan di: simulasi.log")
        print("="*55 + "\n")


# ──────────────────────────────────────────────
if __name__ == "__main__":
    bot = SimulasiBot(CONFIG)
    bot.jalankan()
