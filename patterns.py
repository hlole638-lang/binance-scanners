def bullish_engulfing(df):
    prev = df.iloc[-2]
    curr = df.iloc[-1]

    return (
        prev["close"] < prev["open"] and
        curr["close"] > curr["open"] and
        curr["open"] < prev["close"] and
        curr["close"] > prev["open"]
    )

def hammer(df):
    c = df.iloc[-1]

    body = abs(c["close"] - c["open"])
    lower = min(c["open"], c["close"]) - c["low"]
    upper = c["high"] - max(c["open"], c["close"])

    return lower > body * 2 and upper < body

def green_candle(df):
    c = df.iloc[-1]
    return c["close"] > c["open"]
