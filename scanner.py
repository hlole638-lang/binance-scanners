import requests
import pandas as pd

BASE_URL = "https://api.kucoin.com"

# ---------------- RSI ---------------- #

def calculate_rsi(df, period=14):

    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

# ---------------- Candles ---------------- #

def get_klines(symbol, timeframe):

    interval_map = {
        "15m": "15min",
        "1h": "1hour",
        "4h": "4hour",
        "1d": "1day"
    }

    kucoin_tf = interval_map.get(
        timeframe,
        "1hour"
    )

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

    df = df[::-1].reset_index(drop=True)

    return df

# ---------------- Reversal Candle ---------------- #

def bullish_reversal(df):

    last = df.iloc[-1]

    body = abs(
        last["close"] - last["open"]
    )

    avg_body = abs(
        df["close"] - df["open"]
    ).rolling(3).mean().iloc[-2]

    green = last["close"] > last["open"]

    strong_body = body > avg_body

    return green and strong_body

# ---------------- Order Block ---------------- #

def bullish_order_block(df):

    if len(df) < 10:
        return False

    for i in range(-8, -2):

        candle = df.iloc[i]

        bearish = candle["close"] < candle["open"]

        if not bearish:
            continue

        move = (
            df.iloc[i + 1]["close"] -
            candle["close"]
        ) / candle["close"]

        strong_move = move > 0.02

        if strong_move:

            ob_high = candle["open"]
            ob_low = candle["low"]

            current_price = df.iloc[-1]["close"]

            inside_ob = (
                ob_low <= current_price <= ob_high
            )

            if inside_ob:
                return True

    return False

# ---------------- Main Scan ---------------- #

def run_scan(interval):

    symbols = [

        "BTC-USDT",
        "ETH-USDT",
        "BNB-USDT",
        "SOL-USDT",
        "XRP-USDT",
        "DOGE-USDT",
        "ADA-USDT",
        "LINK-USDT",
        "AVAX-USDT",
        "DOT-USDT"

    ]

    results = []

    for symbol in symbols:

        try:

            df = get_klines(
                symbol,
                interval
            )

            if df is None:
                continue

            if len(df) < 20:
                continue

            df["RSI"] = calculate_rsi(df)

            last_rsi = df.iloc[-1]["RSI"]

            if pd.isna(last_rsi):
                continue

            reversal =
                bullish_reversal(df)

            order_block =
                bullish_order_block(df)

            rsi_condition =
                last_rsi < 32

            score = 0

            if rsi_condition:
                score += 40

            if reversal:
                score += 30

            if order_block:
                score += 30

            if score >= 40:

                results.append({

                    "symbol": symbol,

                    "price": round(
                        df.iloc[-1]["close"],
                        4
                    ),

                    "rsi": round(
                        float(last_rsi),
                        2
                    ),

                    "score": score,

                    "reversal": reversal,

                    "order_block": order_block

                })

        except Exception as e:

            print(symbol, e)

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return results
