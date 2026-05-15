import requests
import pandas as pd

BASE_URL = "https://api.kucoin.com"

def calculate_rsi(df, period=14):

    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

def get_klines(symbol, timeframe):

    interval_map = {
        "15m": "15min",
        "1h": "1hour",
        "4h": "4hour",
        "1d": "1day"
    }

    kucoin_tf = interval_map.get(timeframe, "1hour")

    url = (
        f"{BASE_URL}/api/v1/market/candles"
        f"?type={kucoin_tf}&symbol={symbol}"
    )

    response = requests.get(
        url,
        timeout=10
    )

    data = response.json()

    if "data" not in data:
        return None

    candles = data["data"]

    if not candles:
        return None

    rows = []

    for c in candles:

        rows.append({

            "time": c[0],
            "open": float(c[1]),
            "close": float(c[2]),
            "high": float(c[3]),
            "low": float(c[4]),
            "volume": float(c[5])

        })

    df = pd.DataFrame(rows)

    df = df[::-1]

    return df

def run_scan(interval):

    symbols = [
        "BTC-USDT",
        "ETH-USDT",
        "BNB-USDT",
        "SOL-USDT",
        "XRP-USDT"
    ]

    results = []

    for symbol in symbols:

        try:

            df = get_klines(symbol, interval)

            if df is None:
                continue

            if len(df) < 20:
                continue

            df["RSI"] = calculate_rsi(df)

            last_rsi = df.iloc[-1]["RSI"]

            if pd.isna(last_rsi):
                continue

            results.append({

                "symbol": symbol,
                "price": round(df.iloc[-1]["close"], 4),
                "rsi": round(float(last_rsi), 2),
                "score": round(100 - float(last_rsi), 2)

            })

        except Exception as e:

            results.append({

                "symbol": symbol,
                "price": str(e),
                "rsi": 0,
                "score": 0

            })

    return results
