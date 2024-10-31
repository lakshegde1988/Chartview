import os
import csv
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
    # Fetch stock symbols to display in dropdown
    stock_symbols = load_stock_symbols()
    return render_template('index.html', stock_symbols=stock_symbols)

@app.route('/get_ohlc')
def get_ohlc():
    symbol = request.args.get('symbol')
    try:
        # Fetch OHLC data
        data = yf.download(symbol + '.NS', period='7d', interval='1d')
        data.reset_index(inplace=True)
        
        # Ensure the time is converted to string
        data['time'] = data['Date'].astype(str)
        
        # Select and rename columns
        data = data[['time', 'Open', 'High', 'Low', 'Close']]
        data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'}, inplace=True)
        
        # Convert to a list of dictionaries
        result = data.to_dict(orient='records')  # Use orient='records' for a list of dictionaries
        # logging.debug(f"Data fetched for {symbol}: {result}")  # Log the fetched data
        return jsonify(result)
    except Exception as e:
        # Log the error for debugging
        # logging.error(f"Error fetching data for {symbol}: {e}")
        return jsonify({"error": str(e)}), 500
        
# Vercel looks for an 'app' callable
app = app
