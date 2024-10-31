from flask import Flask, render_template, jsonify, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Load stock symbols from CSV
    stock_symbols = pd.read_csv('data/stocks.csv')['symbol'].tolist()
    return render_template('index.html', stock_symbols=stock_symbols)

@app.route('/get_ohlc')
def get_ohlc():
    symbol = request.args.get('symbol')
    try:
        # Fetch OHLC data
        data = yf.download(symbol + '.NS', period='3mo', interval='1d')
        data.reset_index(inplace=True)

        # Ensure the time is converted to string
        data['time'] = data['Date'].astype(str)
        
        # Select and rename columns
        data = data[['time', 'Open', 'High', 'Low', 'Close']]
        data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'}, inplace=True)
        
        # Convert to a list of dictionaries
        result = data.to_dict(orient='records')  # Use orient='records' for a list of dictionaries
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
