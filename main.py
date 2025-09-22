import yfinance as yf
import talib
import pandas as pd
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("nifty_technical_indicators_server")

def get_nse_data(symbol):
   # Download 1 year of daily OHLCV data
  enddate = pd.Timestamp.today().strftime("%Y-%m-%d")
  startdate = (pd.Timestamp.today() - pd.Timedelta(days=365)).strftime("%Y-%m-%d")
  df = yf.download(symbol+".NS", start=startdate, end=enddate, interval="1d")

  df = df.rename(columns={
    "Open": "Open",
    "High": "High",
    "Low": "Low",
    "Close": "Close",
    "Adj Close": "Adj_Close",
    "Volume": "Volume"
   })

  return df

def sma50(df):
    if df.empty or "Close" not in df.columns:
        print("No data or missing 'Close' column for", df)
        return None
    close = df["Close"].astype(float).values
    if close.ndim != 1:
        close = close.flatten()
    df["SMA50"] = talib.SMA(close, timeperiod=50)
    # Return only the last SMA50 value
    return float(df["SMA50"].iloc[-1])

def macd(df):
    if df.empty or "Close" not in df.columns:
        print("No data or missing 'Close' column for", df)
        return None
    close = df["Close"].astype(float).values
    if close.ndim != 1:
        close = close.flatten()
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    return {
        "MACD_Line": float(macd[-1]),
        "MACD_Signal": float(macdsignal[-1]),
        "MACD_Hist": float(macdhist[-1])
    }

def rsi14(df):
    if df.empty or "Close" not in df.columns:
        print("No data or missing 'Close' column for", df)
        return None
    close = df["Close"].astype(float).values
    if close.ndim != 1:
        close = close.flatten()
    df["RSI14"] = talib.RSI(close, timeperiod=14)
    return float(df[["RSI14"]].iloc[-1].values[0])

def atr(df):

    if df.empty or not all(col in df.columns for col in ["High", "Low", "Close"]):
        print("No data or missing columns for", df)
        return None
    high = df["High"].astype(float).values
    low = df["Low"].astype(float).values
    close = df["Close"].astype(float).values
    if high.ndim != 1:
        high = high.flatten()
    if low.ndim != 1:
        low = low.flatten()
    if close.ndim != 1:
        close = close.flatten()
    df["ATR"] = talib.ATR(high, low, close, timeperiod=14)
    return float(df[["ATR"]].iloc[-1].values[0])

def bollinger(df):

    if df.empty or "Close" not in df.columns:
        print("No data or missing 'Close' column for", df)
        return None
    close = df["Close"].astype(float).values
    if close.ndim != 1:
        close = close.flatten()
    upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    return {
        "BB_Upper": float(upper[-1]),
        "BB_Middle": float(middle[-1]),
        "BB_Lower": float(lower[-1])
    }

def vol_avg20(df):
    
    if df.empty or "Volume" not in df.columns:
        print("No data or missing 'Volume' column for", df)
        return None
    volume = df["Volume"].astype(float).values
    if volume.ndim != 1:
        volume = volume.flatten()
    df["Vol_Avg20"] = talib.SMA(volume, timeperiod=20)
    return float(df[["Vol_Avg20"]].iloc[-1].values[0])

@mcp.tool()
def get_technical_indicators(ticker):
    "Get technical analysis indicators like simple moving average, MACD, RSI, ATR, Bollinger Bands and average volume for a given ticker in National Stock Exchange of India (NSE)"
    df = get_nse_data(ticker)
    result = {}
    result["SMA50"] = sma50(df)
    macd_vals = macd(df)
    if macd_vals is not None:
        result["MACD_Line"] = macd_vals["MACD_Line"]
        result["MACD_Signal"] = macd_vals["MACD_Signal"]
        result["MACD_Hist"] = macd_vals["MACD_Hist"]
    result["RSI14"] = rsi14(df)
    result["ATR"] = atr(df)
    boll_vals = bollinger(df)
    if boll_vals is not None:
        result["BB_Upper"] = boll_vals["BB_Upper"]
        result["BB_Middle"] = boll_vals["BB_Middle"]
        result["BB_Lower"] = boll_vals["BB_Lower"]
    result["Vol_Avg20"] = vol_avg20(df)
    result["Ticker"] = ticker
    if not df.empty and "Close" in df.columns:
        if len(df) > 1:
            prev = df.iloc[-2]
            result["Prev_OHLCV"] = {
                "Open": float(prev['Open'].values[0]),
                "High": float(prev['High'].values[0]),
                "Low": float(prev['Low'].values[0]),
                "Close": float(prev['Close'].values[0]),
                "Volume": float(prev['Volume'].values[0])
            }
        else:
            result["Prev_OHLCV"] = None
    return result

if __name__ == "__main__":
    mcp.run(transport='stdio')