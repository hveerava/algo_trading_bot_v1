import requests
from bs4 import BeautifulSoup
import logging
from .scraping.forexscraper import ForexScraper
from .scraping.stockscraper import StockScraper
import sys



class DataFetcher:
    def __init__(self, stock_base_url, forex_base_url):
        self.stock_scraper = StockScraper(stock_base_url)
        self.forex_scraper = ForexScraper(forex_base_url)

    def get_stock_data(self, stock_symbol):
        return self.stock_scraper.fetch_stock_data(stock_symbol)

    def get_forex_data(self, currency_pair):
        return self.forex_scraper.fetch_forex_data(currency_pair)
