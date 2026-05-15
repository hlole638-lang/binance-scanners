import pandas as pd

def add_rsi(df, period=14):

    delta = df["close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = 100 - (100 / (1 + rs))

    return df

def candle_body(df):
    return abs(df["close"] - df["open"])

def avg_body(df):
    return candle_body(df).rolling(3).mean()
