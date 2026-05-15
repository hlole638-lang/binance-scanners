import numpy as np
from scipy.signal import argrelextrema

def pivot_highs(df):
    highs = df["high"].values

    pivots = argrelextrema(
        highs,
        np.greater,
        order=2
    )[0]

    return pivots

def trendline_break(df):

    pivots = pivot_highs(df)

    if len(pivots) < 3:
        return False

    last3 = pivots[-3:]

    x = np.array(last3)
    y = df["high"].iloc[last3].values

    slope, intercept = np.polyfit(x, y, 1)

    current_x = len(df) - 1
    trend_price = slope * current_x + intercept

    last_close = df.iloc[-1]["close"]

    return last_close > trend_price
