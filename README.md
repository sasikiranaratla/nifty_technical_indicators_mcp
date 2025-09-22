# Nifty Technical Indicators MCP Server

This project provides a Model Context Protocol (MCP) server for calculating popular technical indicators for stocks listed on the National Stock Exchange of India (NSE). It uses TA-Lib for all indicator calculations and can be run locally as an MCP server using stdio transport.

## Features
- Fetches 1 year of daily OHLCV data for any NSE ticker using Yahoo Finance
- Calculates key technical indicators:
  - SMA50 (50-day Simple Moving Average)
  - MACD (Moving Average Convergence Divergence)
  - RSI14 (14-day Relative Strength Index)
  - ATR (Average True Range)
  - Bollinger Bands (20-day)
  - 20-day Average Volume
- Returns previous day's Open, High, Low, Close, and Volume
- Exposes a single MCP tool: `get_technical_indicators`
- Output is a clean JSON object with all indicator values

## Requirements
- Python 3.8+
- TA-Lib
- yfinance
- mcp (Model Context Protocol server)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/sasikiranaratla/nifty_technical_indicators_mcp.git
   cd nifty_technical_indicators_mcp
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Linux/Mac
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   If `requirements.txt` is missing, install manually:
   ```sh
   pip install pandas TA-Lib yfinance mcp
   ```

## Usage: Run as MCP Server (stdio)
To run the MCP server locally using stdio transport:

```sh
python main.py
```

Or, if using a virtual environment:
```sh
venv\Scripts\python.exe main.py  # On Windows
source venv/bin/activate && python main.py  # On Linux/Mac
```

This will start the MCP server and expose the `get_technical_indicators` tool. You can connect to it using any MCP-compatible client or integration.

### MCP Tool: `get_technical_indicators`
- **Input:** `ticker` (str) — NSE stock symbol (e.g., "RELIANCE", "TCS")
- **Output:** JSON object with:
  - SMA50
  - MACD_Line, MACD_Signal, MACD_Hist
  - RSI14
  - ATR
  - BB_Upper, BB_Middle, BB_Lower
  - Vol_Avg20
  - Prev_OHLCV: {Open, High, Low, Close, Volume} for previous day

#### Example MCP Request
```json
{
  "tool": "get_technical_indicators",
  "args": {"ticker": "RELIANCE"}
}
```

#### Example MCP Response
```json
{
  "SMA50": 2795.12,
  "MACD_Line": 12.34,
  "MACD_Signal": 10.56,
  "MACD_Hist": 1.78,
  "RSI14": 55.67,
  "ATR": 45.12,
  "BB_Upper": 2900.45,
  "BB_Middle": 2750.23,
  "BB_Lower": 2600.01,
  "Vol_Avg20": 1234567.0,
  "Prev_OHLCV": {
    "Open": 2780.0,
    "High": 2800.0,
    "Low": 2770.0,
    "Close": 2795.0,
    "Volume": 1500000.0
  }
}
```

## Notes
- All calculations use TA-Lib for reliability and speed.
- Data is fetched from Yahoo Finance via yfinance.
- MCP server can be integrated with any LLM or automation platform supporting MCP.

## License
MIT

## Author
sasikiranaratla
