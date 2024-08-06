import requests
from bs4 import BeautifulSoup
import logging

class ForexScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_forex_data(self, currency_pair):
        try:
            url = f'{self.base_url}/forex/{currency_pair}'
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            data = {
                'exchange_rate': soup.find('span', {'class': 'exchange-rate'}).text,
                'timestamp': soup.find('span', {'class': 'timestamp'}).text,
            }
            return data
        except Exception as e:
            logging.error(f"Failed to fetch forex data for {currency_pair}: {str(e)}")
            return None