import logging

class TransactionLogger:
    def __init__(self, log_file):
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    def log_trade(self, trade_details):
        try:
            logging.info(f"Trade executed: {trade_details}")
        except Exception as e:
            logging.error(f"Error logging trade: {str(e)}")

    def log_error(self, error_message):
        try:
            logging.error(f"Error occurred: {error_message}")
        except Exception as e:
            logging.error(f"Error logging error message: {str(e)}")
