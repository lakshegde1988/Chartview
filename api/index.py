from flask import Flask, jsonify, request, render_template
import yfinance as yf
import pandas as pd
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# Path for stocks CSV file
CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/stocks.csv')

@app.route('/')
def home():
    # Render the HTML UI
    return render_template("index.html")

@app.route('/get_ohlc', methods=['GET'])
def get_ohlc():
    try:
        if not os.path.exists(CSV_PATH):
            return jsonify({"error": "stocks.csv file not found"}), 404
        stocks_df = pd.read_csv(CSV_PATH)

        stock_name = request.args.get('symbol')
        if not stock_name:
            return jsonify({"error": "Stock symbol parameter is required."}), 400
        if stock_name not in stocks_df['Symbol'].values:
            return jsonify({"error": f"Stock symbol '{stock_name}' not found in CSV."}), 404

        stock_symbol = f"{stock_name}.NS"
        data = yf.download(stock_symbol, period='1d', interval='1m')
        if data.empty:
            return jsonify({"error": "No data available for the specified stock symbol."}), 404

        ohlc_data = data[['Open', 'High', 'Low', 'Close']].reset_index()
        ohlc_data['Datetime'] = ohlc_data['Datetime'].astype(str)
        ohlc_json = ohlc_data.to_dict(orient='records')

        return jsonify(ohlc_json)
    
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
