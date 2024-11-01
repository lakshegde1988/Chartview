from flask import Flask, jsonify, request, render_template
import yfinance as yf
import pandas as pd
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# Load stock symbols from CSV file
CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/stocks.csv')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_ohlc', methods=['GET'])
def get_ohlc():
    stock_symbol = request.args.get('symbol')
    
    if not stock_symbol:
        return jsonify({"error": "No stock symbol provided"}), 400

    # Ensure symbol exists in CSV
    stocks_df = pd.read_csv(CSV_PATH)
    if stock_symbol not in stocks_df['Symbol'].values:
        return jsonify({"error": "Symbol not found in CSV"}), 404
    
    # Fetch OHLC data
    symbol =f"{stock_symbol}.NS"
    stock_data = yf.download(symbol, period="3mo", interval="1d")
    if stock_data.empty:
        return jsonify({"error": "No data found"}), 404

    # Format OHLC data for Lightweight Charts
    ohlc_data = [
        {
            "time": int(row.name.timestamp()),
            "open": row['Open'],
            "high": row['High'],
            "low": row['Low'],
            "close": row['Close']
        }
        for row in stock_data.itertuples()
    ]
    return jsonify(ohlc_data)

if __name__ == '__main__':
    app.run(debug=True)
