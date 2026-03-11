"""
Backtester Sederhana untuk KuCoin Scalping Bot
Jalankan: python backtest.py
"""

import csv
import sys
from bot import calc_ema, calc_rsi, avg_volume, generate_signal
from config import CONFIG

def run_backtest(candles: list, cfg: dict):
    trades = []
    position = None
    wins = 0

    for i in range(cfg["ema_slow"] + 20, len(candles)):
        window = candles[:i+1]
        price = float(candles[i][2])

        if position:
            sl = position["sl"]
            tp = position["tp"]
            if price <= sl:
                pnl = (price - position["entry"]) * position["size"]
                trades.append(pnl)
                position = None
            elif price >= tp:
                pnl = (price - position["entry"]) * position["size"]
                trades.append(pnl)
                if pnl > 0:
                    wins += 1
                position = None

        if not position:
            sig = generate_signal(window, cfg)
            if sig == "BUY":
                size = (1000 * cfg["trade_pct"]) / price  # asumsi modal 1000 USDT
                position = {
                    "entry": price,
                    "size": size,
                    "sl": price * (1 - cfg["stop_loss_pct"]),
                    "tp": price * (1 + cfg["take_profit_pct"]),
                }

    total_trades = len(trades)
    total_pnl = sum(trades)
    win_rate = (wins / total_trades * 100) if total_trades else 0

    print("=" * 40)
    print("📊 HASIL BACKTEST")
    print(f"   Total Candle  : {len(candles)}")
    print(f"   Total Trade   : {total_trades}")
    print(f"   Win Rate      : {win_rate:.1f}%")
    print(f"   Total PnL     : {total_pnl:+.4f} USDT")
    print(f"   Rata-rata PnL : {(total_pnl/total_trades if total_trades else 0):+.4f} USDT")
    print("=" * 40)
    return trades


# ── Contoh: muat dari CSV (timestamp, open, close, high, low, volume, turnover) ──
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan: python backtest.py data.csv")
        print("Atau jalankan tanpa argumen untuk tes dengan data dummy.")
        # Demo dengan data dummy
        import random
        random.seed(42)
        price = 30000.0
        candles = []
        for i in range(300):
            change = random.uniform(-0.003, 0.003)
            price *= (1 + change)
            vol = random.uniform(1, 5)
            candles.append([str(i), str(price*0.999), str(price), str(price*1.001),
                             str(price*0.998), str(vol), str(vol*price)])
        run_backtest(candles, CONFIG)
    else:
        with open(sys.argv[1]) as f:
            candles = list(csv.reader(f))
        run_backtest(candles, CONFIG)
