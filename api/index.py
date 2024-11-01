# index.py
from flask import Flask, jsonify, request
import yfinance as yf
import pandas as pd
import os

app = Flask(__name__)

# Path to your CSV file with stock names
CSV_PATH = "data/stocks.csv"

@app.route("/get_ohlc", methods=["GET"])
def get_ohlc():
    try:
        # Check if CSV file exists
        if not os.path.exists(CSV_PATH):
            print("CSV file not found")
            return jsonify({"error": "CSV file not found"}), 500

        # Read stock symbols from CSV and append '.NS' suffix
        stock_symbols = pd.read_csv(CSV_PATH)["symbol"].tolist()
        
        # Fetch data for the first stock symbol for testing
        stock_symbol = stock_symbols[0] + ".NS" if stock_symbols else None
        if not stock_symbol:
            print("No stock symbol found in CSV")
            return jsonify({"error": "No stock symbol found in CSV"}), 400

        print(f"Fetching data for {stock_symbol}...")

        # Fetch OHLC data for the stock
        stock_data = yf.download(stock_symbol, period="1mo", interval="1d")
        
        # Reset index to access date column as a separate column
        stock_data.reset_index(inplace=True)
        print("Downloaded data:", stock_data.head())

        # Prepare JSON-friendly data
        ohlc_data = stock_data[["Date", "Open", "High", "Low", "Close"]].copy()
        ohlc_data["Date"] = ohlc_data["Date"].dt.strftime('%Y-%m-%d')  # Convert date to string

        # Convert dataframe to a list of dictionaries
        data_to_return = ohlc_data.to_dict(orient="records")
        print("Formatted data to JSON:", data_to_return[:5])  # Print first few rows for debug

        return jsonify(data_to_return)

    except Exception as e:
        print("Error in /get_ohlc:", e)
        return jsonify({"error": str(e)}), 500

# For local testing
if __name__ == "__main__":
    app.run(debug=True)
    
