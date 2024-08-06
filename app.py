from flask import Flask, jsonify, render_template
from data.real_time.data_fetcher import DataFetcher

app = Flask(__name__)

stock_base_url = 'some-url/stock'
forex_base_url = 'some-url/forex'
data_fetcher = DataFetcher(stock_base_url, forex_base_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    data = data_fetcher.get_stock_data(symbol)
    return jsonify(data)

@app.route('/api/forex/<pair>', methods=['GET'])
def get_forex_data(pair):
    data = data_fetcher.get_forex_data(pair)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
