import logging

class OrderManager:
    def __init__(self):
        self.orders = []

    def place_order(self, order):
        try:
            self.orders.append(order)
            logging.info(f"Order placed: {order}")
        except Exception as e:
            logging.error(f"Error placing order: {str(e)}")

    def get_orders(self):
        return self.orders
