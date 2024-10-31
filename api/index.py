from flask import Flask, render_template, jsonify, request
import yfinance as yf
import pandas as pd
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    # Load stock symbols from CSV
    stock_symbols = pd.read_csv('data/stocks.csv')['Symbol'].tolist()
    return render_template('index.html', stock_symbols=stock_symbols)

@app.route('/get_ohlc')
def get_ohlc():
    symbol = request.args.get('symbol')
    logging.debug(f"Fetching OHLC data for symbol: {symbol}")  # Log the requested symbol
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
        logging.debug(f"Data fetched for {symbol}: {result}")  # Log the fetched data
        return jsonify(result)
    except Exception as e:
        # Log the error for debugging
        logging.error(f"Error fetching data for {symbol}: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
