import requests
import pandas as pd

BASE_URL = "https://api.binance.com/api/v3"

def calculate_rsi(df, period=14):

    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

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

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    return df

def run_scan(interval):

    symbols = [
        "BTCUSDT",
        "ETHUSDT",
        "BNBUSDT",
        "SOLUSDT",
        "XRPUSDT"
    ]

    results = []

    for symbol in symbols:

        try:

            df = get_klines(symbol, interval)

            if df is None:
                continue

            df["RSI"] = calculate_rsi(df)

            last_rsi = df.iloc[-1]["RSI"]

            results.append({
                "symbol": symbol,
                "price": round(df.iloc[-1]["close"], 4),
                "rsi": round(last_rsi, 2),
                "score": round(100 - last_rsi, 2)
            })

        except Exception as e:

            print(symbol, e)

    return results
