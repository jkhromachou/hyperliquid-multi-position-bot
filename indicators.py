import pandas as pd
import numpy as np

def compute_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def compute_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd_cross_below_minus40(data):
    macd, _ = compute_macd(data)
    if macd.iloc[-2] > -40 and macd.iloc[-1] <= -40:
        return True
    return False

def rsi_above_70(data):
    rsi = compute_rsi(data)
    return rsi.iloc[-1] > 70
