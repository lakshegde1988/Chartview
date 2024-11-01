from flask import Flask, jsonify, render_template, request
import yfinance as yf
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_ohlc')
def get_ohlc():
    # Get the stock symbol from the query string
    symbol = request.args.get('symbol', 'AAPL')  # Default to 'AAPL' if no symbol is provided
    data = yf.download(symbol, period="1mo", interval="1d")

    # Prepare OHLC data in the format TradingView Lightweight Charts expects
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

if __name__ == "__main__":
    app.run(debug=True)
  
