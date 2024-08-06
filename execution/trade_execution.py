import logging
import requests

class TradeExecution:
    def __init__(self, order_manager, api_endpoint, api_key):
        self.order_manager = order_manager
        self.api_endpoint = api_endpoint
        self.api_key = api_key

    def validate_trade(self, trade):
        required_fields = ['symbol', 'quantity', 'price', 'action']
        for field in required_fields:
            if field not in trade:
                raise ValueError(f"Missing required field: {field}")

    def execute_trade(self, trade):
        try:
            self.validate_trade(trade)
            payload = {
                'symbol': trade['symbol'],
                'quantity': trade['quantity'],
                'price': trade['price'],
                'action': trade['action'],
                'api_key': self.api_key
            }
            response = requests.post(f"{self.api_endpoint}/place_order", json=payload)
            if response.status_code == 200:
                logging.info(f"Trade executed successfully: {trade}")
            else:
                logging.error(f"Trade execution failed with status code {response.status_code}: {response.text}")
        except Exception as e:
            logging.error(f"Failed to execute trade: {str(e)}")
