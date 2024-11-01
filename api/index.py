import os
import csv
from flask import Flask, jsonify, render_template, request
import yfinance as yf
import pandas as pd

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Load stock symbols from CSV
def load_stock_symbols():
    stock_symbols = []
    csv_path = os.path.join(os.path.dirname(__file__), '../data/stocks.csv')
    with open(csv_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stock_symbols.append(row['symbol'])
    return stock_symbols

@app.route('/')
def home():
    # Fetch stock symbols to display in dropdown
    stock_symbols = load_stock_symbols()
    return render_template('index.html', stock_symbols=stock_symbols)

@app.route('/get_ohlc')
def get_ohlc():
    # Get the stock symbol from the query string
    symbol = request.args.get('symbol', 'RELIANCE')
    nse_symbol = f"{symbol}.NS"  # Append .NS to the symbol for NSE stocks

    # Fetch OHLC data from yfinance
    try:
        data = yf.download(nse_symbol, period="1mo", interval="1d")
        if data.empty:
            return jsonify({"error": "No data found for this symbol"}), 404

        ohlc_data = []
        for date, row in data.iterrows():
            ohlc_data.append({
                "time": int(date.timestamp()),
                "open": row['Open'],
                "high": row['High'],
                "low": row['Low'],
                "close": row['Close']
            })

        return jsonify(ohlc_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel looks for an 'app' callable
app = app
