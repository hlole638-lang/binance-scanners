import requests
import pandas as pd

BASE_URL = "https://api.binance.com/api/v3"

def get_symbols():

    data = requests.get(
        f"{BASE_URL}/ticker/24hr"
    ).json()

    symbols = []

    for item in data:

        symbol = item["symbol"]

        try:

            volume = float(item["quoteVolume"])

            if (
                symbol.endswith("USDT")
                and volume > 5000000
            ):
                symbols.append(symbol)

        except:
            pass

    return symbols[:50]


def get_klines(symbol, interval):

    url = f"{BASE_URL}/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 100
    }

    response = requests.get(url, params=params)

    data = response.json()

    df = pd.DataFrame(data)

    if df.empty:
        return None

    df = df.iloc[:, :6]

    df.columns = [
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)

    return df


def calculate_rsi(df, period=14):

    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


def run_scan(interval):

    symbols = get_symbols()

    results = []

    for symbol in symbols:

        try:

            df = get_klines(symbol, interval)

            if df is None:
                continue

            df["RSI"] = calculate_rsi(df)

            last_rsi = df.iloc[-1]["RSI"]

            if last_rsi < 50:

                results.append({
                    "symbol": symbol,
                    "price": round(df.iloc[-1]["close"], 4),
                    "rsi": round(last_rsi, 2),
                    "score": round(100 - last_rsi, 2)
                })

        except Exception as e:

            print(symbol, e)

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:10]
