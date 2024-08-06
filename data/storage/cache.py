import json
import logging

class Cache:
    def __init__(self, cache_path):
        self.cache_path = cache_path

    def save(self, data):
        try:
            with open(self.cache_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            logging.error(f"Failed to save cache: {str(e)}")

    def load(self):
        try:
            with open(self.cache_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load cache: {str(e)}")
            return {}
