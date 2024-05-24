import requests

API_KEY = "your_api_key"
BASE_URL = "https://api.broker.com/v1/"

def place_order(symbol, quantity, order_type="market"):
    endpoint = f"{BASE_URL}orders"
    order = {
        "symbol": symbol,
        "qty": quantity,
        "side": "buy",
        "type": order_type,
        "time_in_force": "gtc"
    }
    headers = {"APCA-API-KEY-ID": API_KEY, "APCA-API-SECRET-KEY": API_KEY}
    response = requests.post(endpoint, json=order, headers=headers)
    return response.json()

def get_order_status(order_id):
    endpoint = f"{BASE_URL}orders/{order_id}"
    headers = {"APCA-API-KEY-ID": API_KEY, "APCA-API-SECRET-KEY": API_KEY}
    response = requests.get(endpoint, headers=headers)
    return response.json()
