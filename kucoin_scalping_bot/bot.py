"""
KuCoin Scalping Bot
Strategi: EMA Crossover + RSI + Volume Filter
"""

import time
import hmac
import hashlib
import base64
import requests
import json
import logging
from datetime import datetime
from config import CONFIG

# ──────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# KUCOIN API CLIENT
# ──────────────────────────────────────────────
class KuCoinClient:
    BASE_URL = "https://api.kucoin.com"

    def __init__(self, api_key, api_secret, api_passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase

    def _sign(self, timestamp, method, endpoint, body=""):
        str_to_sign = f"{timestamp}{method}{endpoint}{body}"
        signature = base64.b64encode(
            hmac.new(self.api_secret.encode(), str_to_sign.encode(), hashlib.sha256).digest()
        ).decode()
        passphrase = base64.b64encode(
            hmac.new(self.api_secret.encode(), self.api_passphrase.encode(), hashlib.sha256).digest()
        ).decode()
        return signature, passphrase

    def _headers(self, method, endpoint, body=""):
        timestamp = str(int(time.time() * 1000))
        sig, pp = self._sign(timestamp, method, endpoint, body)
        return {
            "KC-API-KEY": self.api_key,
            "KC-API-SIGN": sig,
            "KC-API-TIMESTAMP": timestamp,
            "KC-API-PASSPHRASE": pp,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json"
        }

    def get(self, endpoint, params=None):
        url = self.BASE_URL + endpoint
        r = requests.get(url, headers=self._headers("GET", endpoint), params=params, timeout=10)
        return r.json()

    def post(self, endpoint, data: dict):
        body = json.dumps(data)
        url = self.BASE_URL + endpoint
        r = requests.post(url, headers=self._headers("POST", endpoint, body), data=body, timeout=10)
        return r.json()

    # ── Market Data ──
    def get_klines(self, symbol, interval="1min", limit=100):
        """Ambil data OHLCV. interval: 1min, 3min, 5min, 15min, 30min, 1hour"""
        endpoint = "/api/v1/market/candles"
        params = {"symbol": symbol, "type": interval}
        resp = self.get(endpoint, params)
        if resp.get("code") != "200000":
            log.error(f"Gagal ambil klines: {resp}")
            return []
        # Format: [timestamp, open, close, high, low, volume, turnover]
        candles = resp.get("data", [])
        candles.reverse()  # urutkan dari lama ke baru
        return candles

    def get_ticker(self, symbol):
        endpoint = f"/api/v1/market/orderbook/level1"
        return self.get(endpoint, {"symbol": symbol})

    def get_balance(self, currency):
        resp = self.get("/api/v1/accounts", {"currency": currency, "type": "trade"})
        accounts = resp.get("data", [])
        if not accounts:
            return 0.0
        return float(accounts[0].get("available", 0))

    # ── Order ──
    def place_order(self, symbol, side, size, order_type="market", price=None):
        import uuid
        data = {
            "clientOid": str(uuid.uuid4()),
            "symbol": symbol,
            "side": side,          # "buy" atau "sell"
            "type": order_type,    # "market" atau "limit"
            "size": str(size),
        }
        if order_type == "limit" and price:
            data["price"] = str(price)
        resp = self.post("/api/v1/orders", data)
        return resp

    def cancel_order(self, order_id):
        return self.post(f"/api/v1/orders/{order_id}", {})

    def get_order(self, order_id):
        return self.get(f"/api/v1/orders/{order_id}")


# ──────────────────────────────────────────────
# INDIKATOR TEKNIKAL
# ──────────────────────────────────────────────
def calc_ema(prices: list, period: int) -> list:
    emas = []
    k = 2 / (period + 1)
    for i, p in enumerate(prices):
        if i < period - 1:
            emas.append(None)
        elif i == period - 1:
            emas.append(sum(prices[:period]) / period)
        else:
            emas.append(p * k + emas[-1] * (1 - k))
    return emas


def calc_rsi(closes: list, period: int = 14) -> float:
    if len(closes) < period + 1:
        return 50.0
    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [d if d > 0 else 0 for d in deltas[-period:]]
    losses = [-d if d < 0 else 0 for d in deltas[-period:]]
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def avg_volume(volumes: list, period: int = 20) -> float:
    if len(volumes) < period:
        return 0.0
    return sum(volumes[-period:]) / period


# ──────────────────────────────────────────────
# LOGIKA SINYAL SCALPING
# ──────────────────────────────────────────────
def generate_signal(candles: list, cfg: dict) -> str:
    """
    Kembalikan: 'BUY', 'SELL', atau 'HOLD'
    Strategi:
      - BUY  : EMA_fast > EMA_slow (crossover ke atas) + RSI < rsi_buy + volume > avg
      - SELL : EMA_fast < EMA_slow (crossover ke bawah) + RSI > rsi_sell
    """
    if len(candles) < cfg["ema_slow"] + 5:
        return "HOLD"

    closes = [float(c[2]) for c in candles]   # index 2 = close
    volumes = [float(c[5]) for c in candles]  # index 5 = volume

    ema_fast = calc_ema(closes, cfg["ema_fast"])
    ema_slow = calc_ema(closes, cfg["ema_slow"])
    rsi = calc_rsi(closes, cfg["rsi_period"])
    vol_avg = avg_volume(volumes, 20)
    cur_vol = volumes[-1]

    ef_now = ema_fast[-1]
    es_now = ema_slow[-1]
    ef_prev = ema_fast[-2]
    es_prev = ema_slow[-2]

    if ef_now is None or es_now is None or ef_prev is None or es_prev is None:
        return "HOLD"

    bullish_cross = ef_prev <= es_prev and ef_now > es_now
    bearish_cross = ef_prev >= es_prev and ef_now < es_now
    vol_ok = cur_vol >= vol_avg * cfg["volume_multiplier"]

    log.info(f"RSI={rsi:.1f} | EMA_fast={ef_now:.4f} | EMA_slow={es_now:.4f} | "
             f"Vol={cur_vol:.2f} vs AvgVol={vol_avg:.2f}")

    if bullish_cross and rsi < cfg["rsi_buy"] and vol_ok:
        return "BUY"
    if bearish_cross and rsi > cfg["rsi_sell"]:
        return "SELL"
    return "HOLD"


# ──────────────────────────────────────────────
# STATE POSISI
# ──────────────────────────────────────────────
class Position:
    def __init__(self):
        self.active = False
        self.entry_price = 0.0
        self.size = 0.0
        self.stop_loss = 0.0
        self.take_profit = 0.0
        self.order_id = None

    def open(self, price, size, sl, tp, order_id=None):
        self.active = True
        self.entry_price = price
        self.size = size
        self.stop_loss = sl
        self.take_profit = tp
        self.order_id = order_id
        log.info(f"📈 POSISI DIBUKA | Entry={price:.4f} | Size={size} | "
                 f"SL={sl:.4f} | TP={tp:.4f}")

    def close(self, reason=""):
        self.active = False
        log.info(f"📉 POSISI DITUTUP | Alasan: {reason} | Entry={self.entry_price:.4f}")

    def check_exit(self, current_price: float) -> str:
        if not self.active:
            return "NONE"
        if current_price <= self.stop_loss:
            return "STOP_LOSS"
        if current_price >= self.take_profit:
            return "TAKE_PROFIT"
        return "NONE"


# ──────────────────────────────────────────────
# BOT UTAMA
# ──────────────────────────────────────────────
class ScalpingBot:
    def __init__(self):
        self.client = KuCoinClient(
            CONFIG["api_key"],
            CONFIG["api_secret"],
            CONFIG["api_passphrase"]
        )
        self.cfg = CONFIG
        self.pos = Position()
        self.trade_count = 0
        self.win_count = 0
        self.pnl_total = 0.0

    def _current_price(self):
        resp = self.client.get_ticker(self.cfg["symbol"])
        return float(resp["data"]["price"])

    def _calc_size(self, price: float) -> float:
        """Hitung ukuran order berdasarkan % modal"""
        base_currency = self.cfg["symbol"].split("-")[1]  # misal USDT
        balance = self.client.get_balance(base_currency)
        usable = balance * self.cfg["trade_pct"]
        size = usable / price
        # Bulatkan sesuai lot minimum KuCoin (default 4 desimal)
        size = round(size, 4)
        return max(size, self.cfg.get("min_size", 0.0001))

    def run(self):
        log.info("=" * 50)
        log.info(f"🤖 KuCoin Scalping Bot AKTIF")
        log.info(f"   Symbol  : {self.cfg['symbol']}")
        log.info(f"   Interval: {self.cfg['interval']}")
        log.info(f"   Mode    : {'LIVE' if not self.cfg['dry_run'] else 'DRY RUN (Simulasi)'}")
        log.info("=" * 50)

        while True:
            try:
                self._tick()
            except KeyboardInterrupt:
                log.info("Bot dihentikan oleh pengguna.")
                self._print_summary()
                break
            except Exception as e:
                log.error(f"Error tidak terduga: {e}", exc_info=True)
            time.sleep(self.cfg["poll_seconds"])

    def _tick(self):
        candles = self.client.get_klines(self.cfg["symbol"], self.cfg["interval"])
        if not candles:
            return

        price = float(candles[-1][2])  # harga close terbaru

        # --- Cek exit posisi aktif ---
        if self.pos.active:
            exit_reason = self.pos.check_exit(price)
            if exit_reason != "NONE":
                self._close_position(price, exit_reason)
                return

        # --- Cek sinyal baru ---
        if not self.pos.active:
            signal = generate_signal(candles, self.cfg)
            log.info(f"Sinyal: {signal} | Harga: {price:.4f}")
            if signal == "BUY":
                self._open_position(price)

    def _open_position(self, price: float):
        sl = round(price * (1 - self.cfg["stop_loss_pct"]), 6)
        tp = round(price * (1 + self.cfg["take_profit_pct"]), 6)
        size = self._calc_size(price)

        order_id = None
        if not self.cfg["dry_run"]:
            resp = self.client.place_order(self.cfg["symbol"], "buy", size)
            if resp.get("code") != "200000":
                log.error(f"Gagal buka order: {resp}")
                return
            order_id = resp["data"]["orderId"]

        self.pos.open(price, size, sl, tp, order_id)
        self.trade_count += 1

    def _close_position(self, price: float, reason: str):
        if not self.cfg["dry_run"] and self.pos.order_id:
            self.client.place_order(self.cfg["symbol"], "sell", self.pos.size)

        pnl = (price - self.pos.entry_price) * self.pos.size
        self.pnl_total += pnl
        if pnl > 0:
            self.win_count += 1

        log.info(f"💰 PnL trade ini: {pnl:+.4f} USDT | Total PnL: {self.pnl_total:+.4f}")
        self.pos.close(reason)

    def _print_summary(self):
        wr = (self.win_count / self.trade_count * 100) if self.trade_count else 0
        log.info("=" * 50)
        log.info(f"📊 RINGKASAN SESI")
        log.info(f"   Total Trade : {self.trade_count}")
        log.info(f"   Win Rate    : {wr:.1f}%")
        log.info(f"   Total PnL   : {self.pnl_total:+.4f} USDT")
        log.info("=" * 50)


# ──────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────
if __name__ == "__main__":
    bot = ScalpingBot()
    bot.run()
