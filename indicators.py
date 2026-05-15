import pandas_ta as ta

def add_rsi(df):
    df["RSI"] = ta.rsi(df["close"], length=14)
    return df

def candle_body(df):
    return abs(df["close"] - df["open"])

def avg_body(df):
    return candle_body(df).rolling(3).mean()
