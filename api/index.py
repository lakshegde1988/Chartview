from flask import Flask, jsonify, render_template, request
import yfinance as yf

app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_ohlc')
def get_ohlc():
    # Get the stock symbol from the query string
    symbol = request.args.get('symbol', 'AAPL')
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

# Vercel looks for an 'app' callable
app = app
