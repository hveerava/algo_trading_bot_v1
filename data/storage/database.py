import sqlite3
import logging

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        try:
            with self.conn:
                self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS stock_data (
                        symbol TEXT,
                        price REAL,
                        volume INTEGER,
                        timestamp TEXT
                    )
                ''')
                self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS forex_data (
                        pair TEXT,
                        exchange_rate REAL,
                        timestamp TEXT
                    )
                ''')
        except Exception as e:
            logging.error(f"Failed to create tables: {str(e)}")

    def insert_stock_data(self, data):
        try:
            with self.conn:
                self.conn.execute('''
                    INSERT INTO stock_data (symbol, price, volume, timestamp)
                    VALUES (:symbol, :price, :volume, :timestamp)
                ''', data)
        except Exception as e:
            logging.error(f"Failed to insert stock data: {str(e)}")

    def insert_forex_data(self, data):
        try:
            with self.conn:
                self.conn.execute('''
                    INSERT INTO forex_data (pair, exchange_rate, timestamp)
                    VALUES (:pair, :exchange_rate, :timestamp)
                ''', data)
        except Exception as e:
            logging.error(f"Failed to insert forex data: {str(e)}")
