import requests
import pandas as pd
from indicators import add_rsi, candle_body, avg_body
from patterns import bullish_engulfing, hammer, green_candle
from trendline import trendline_break

BASE_URL = "https://api.binance.com/api/v3"

def get_symbols():

    data = requests.get(
        f"{BASE_URL}/ticker/24hr"
    ).json()

    symbols = []

    for item in data:

        symbol = item["symbol"]

        if (
            symbol.endswith("USDT")
            and float(item["quoteVolume"]) > 5000000
        ):
            symbols.append(symbol)

    return symbols

def get_klines(symbol, interval):

    url = f"{BASE_URL}/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 200
    }

    data = requests.get(url, params=params).json()

    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close",
        "volume","c1","c2","c3","c4","c5","c6"
    ])

    df = df.astype({
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": float
    })

    return df

def detect_order_block(df):

    for i in range(len(df)-10, len(df)-3):

        candle = df.iloc[i]

        bearish = candle["close"] < candle["open"]

        if not bearish:
            continue

        future = df.iloc[i+1:i+4]

        move = (
            future["close"].max() - candle["close"]
        ) / candle["close"]

        if move > 0.03:

            ob_low = candle["low"]
            ob_high = candle["open"]

            current = df.iloc[-1]["close"]

            if ob_low <= current <= ob_high:
                return True

    return False

def score_coin(df):

    score = 0

    rsi = df.iloc[-1]["RSI"]

    if rsi < 28:
        score += 25

    if bullish_engulfing(df):
        score += 20

    if hammer(df):
        score += 10

    if trendline_break(df):
        score += 30

    if df.iloc[-1]["volume"] > df["volume"].rolling(20).mean().iloc[-1]:
        score += 20

    return score

def run_scan(interval):

    symbols = get_symbols()

    results = []

    for symbol in symbols:

        try:

            df = get_klines(symbol, interval)

            df = add_rsi(df)

            last_rsi = df.iloc[-1]["RSI"]

            body = candle_body(df).iloc[-1]
            avg = avg_body(df).iloc[-1]

            strong_candle = body > avg

            reversal = (
                bullish_engulfing(df)
                or hammer(df)
                or green_candle(df)
            )

            if (
                last_rsi < 32
                and reversal
                and detect_order_block(df)
                and trendline_break(df)
                and strong_candle
            ):

                results.append({
                    "symbol": symbol,
                    "price": round(df.iloc[-1]["close"], 4),
                    "rsi": round(last_rsi, 2),
                    "score": score_coin(df)
                })

        except:
            pass

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:10]
