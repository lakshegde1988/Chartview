from flask import Flask, jsonify, request
import yfinance as yf
import pandas as pd
import os
import json

app = Flask(__name__)

# Adjust the path to locate stocks.csv within the correct directory
CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/stocks.csv')

@app.route('/')
def home():
    return "Welcome to the Stock OHLC Data API!"

@app.route('/get_ohlc', methods=['GET'])
def get_ohlc():
    try:
        # Load stocks from the CSV file
        stocks_df = pd.read_csv(CSV_PATH)
        
        # Extract the symbol parameter from the query string
        stock_name = request.args.get('symbol')
        if not stock_name or stock_name not in stocks_df['Symbol'].values:
            return jsonify({"error": "Stock symbol not provided or not found in CSV."}), 400
        
        # Append '.NS' suffix for NSE stock data
        stock_symbol = f"{stock_name}.NS"
        
        # Fetch OHLC data from yfinance
        data = yf.download(stock_symbol, period='1d', interval='1m')
        if data.empty:
            return jsonify({"error": "No data found for the given symbol."}), 404
        
        # Convert the DataFrame to JSON-friendly format
        ohlc_data = data[['Open', 'High', 'Low', 'Close']].reset_index()
        ohlc_data['Datetime'] = ohlc_data['Datetime'].astype(str)
        
        # Format data as a list of dictionaries for JSON output
        ohlc_json = ohlc_data.to_dict(orient='records')
        
        return jsonify(ohlc_json)
    
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": "An error occurred while processing the request."}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
