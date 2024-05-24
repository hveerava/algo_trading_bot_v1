from flask import Flask, request, jsonify
from flask_cors import CORS
from strategies import moving_average_crossover
from trade_executor import place_order
from database import SessionLocal, TradeHistory
import pandas as pd
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/trade", methods=["POST"])
def trade():
    logging.debug("Received trade request")

    data = request.get_json()
    symbol = data.get("symbol")
    prices = pd.Series(data.get("prices"))
    
    signals = moving_average_crossover(prices)
    latest_signal = signals["positions"].iloc[-1]
    
    if latest_signal == 1.0:
        order = place_order(symbol, 10)  # example order
        save_trade_history(symbol, 10, "buy")
        return jsonify({"message": "Order placed", "order": order})
    else:
        return jsonify({"message": "No trading signal"})

@app.route("/trade_history", methods=["GET"])
def trade_history():
    db = SessionLocal()
    trades = db.query(TradeHistory).all()
    trade_list = [{
        "symbol": trade.symbol,
        "quantity": trade.quantity,
        "order_type": trade.order_type,
        "timestamp": trade.timestamp
    } for trade in trades]
    return jsonify(trade_list)

def save_trade_history(symbol, quantity, order_type):
    db = SessionLocal()
    trade = TradeHistory(symbol=symbol, quantity=quantity, order_type=order_type)
    db.add(trade)
    db.commit()
    db.close()

if __name__ == "__main__":
    app.run(port=8080)