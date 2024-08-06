import requests
from bs4 import BeautifulSoup
import logging

class StockScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_stock_data(self, stock_symbol):
        try:
            url = f'{self.base_url}/stocks/{stock_symbol}'
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            data = {
                'price': soup.find('span', {'class': 'price'}).text,
                'volume': soup.find('span', {'class': 'volume'}).text,
                'timestamp': soup.find('span', {'class': 'timestamp'}).text,
            }
            return data
        except Exception as e:
            logging.error(f"Failed to fetch stock data for {stock_symbol}: {str(e)}")
            return None