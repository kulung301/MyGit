"""
Konfigurasi KuCoin Scalping Bot
================================
PENTING: Ganti API key, secret, dan passphrase dengan milik Anda.
Aktifkan 'dry_run = True' untuk simulasi tanpa modal nyata.
"""

CONFIG = {
    # ── API Credentials ──────────────────────────
    "api_key":        "ISI_API_KEY_ANDA_DI_SINI",
    "api_secret":     "ISI_API_SECRET_ANDA_DI_SINI",
    "api_passphrase": "ISI_PASSPHRASE_ANDA_DI_SINI",

    # ── Simbol & Timeframe ────────────────────────
    "symbol":         "BTC-USDT",   # Pasangan trading
    "interval":       "5min",       # 1min, 3min, 5min, 15min, 30min, 1hour

    # ── Mode ─────────────────────────────────────
    "dry_run":        True,         # True = simulasi | False = trading nyata

    # ── Manajemen Modal ───────────────────────────
    "trade_pct":      0.10,         # Gunakan 10% dari saldo per trade
    "min_size":       0.00001,      # Ukuran order minimum

    # ── Risk Management ───────────────────────────
    "stop_loss_pct":  0.005,        # Stop Loss  0.5% dari harga entry
    "take_profit_pct":0.010,        # Take Profit 1.0% dari harga entry

    # ── Indikator ─────────────────────────────────
    "ema_fast":       9,            # EMA cepat (periode)
    "ema_slow":       21,           # EMA lambat (periode)
    "rsi_period":     14,           # Periode RSI
    "rsi_buy":        45,           # Beli jika RSI < nilai ini
    "rsi_sell":       60,           # Jual jika RSI > nilai ini
    "volume_multiplier": 1.2,       # Volume harus >= 1.2x rata-rata

    # ── Polling ───────────────────────────────────
    "poll_seconds":   60,           # Cek sinyal setiap N detik
}
