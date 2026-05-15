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

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    data = response.json()

    if not isinstance(data, list):
        return None

    if len(data) == 0:
        return None

    df = pd.DataFrame(data)

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

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df.dropna(inplace=True)

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

            print(symbol, e)

    return results
