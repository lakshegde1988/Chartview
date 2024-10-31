import os
import csv
import pandas as pd
from flask import Flask, jsonify, render_template, request
import yfinance as yf

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
    stock_symbols = load_stock_symbols()
    return render_template('index.html', stock_symbols=stock_symbols)

@app.route('/get_ohlc')
def get_ohlc():
    symbol = request.args.get('symbol', 'RELIANCE')
    nse_symbol = f"{symbol}.NS"
    
    # Fetch OHLC data using yfinance and load it into a DataFrame
    data = yf.download(nse_symbol, period="1mo", interval="1d")
    df = pd.DataFrame(data)
    df.reset_index(inplace=True)
    df['time'] = df['Date'].apply(lambda x: int(x.timestamp()))  # Convert date to timestamp

    ohlc_data = df[['time', 'Open', 'High', 'Low', 'Close']].to_dict(orient="records")
    return jsonify(ohlc_data)

app = app
