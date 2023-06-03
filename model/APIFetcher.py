import requests
import json
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.ListedCoinObject import ListedCoinObject

class APIFetcher():
    def __init__(self):
        self.listed_coins_array: list[ListedCoinObject] = []

    def fetchNewListedCoins(self, page: int):
        try:
            new_list: list[ListedCoinObject] = self.__createListedCoinObjects(jsonData=self.__requestPageJSON(page))
            self.listed_coins_array += new_list
            return new_list
        except Exception as e:
            print(e)
        return None

    def __requestPageJSON(self, page: int):
        response_API = requests.get(f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page={page}&sparkline=false&price_change_percentage=1h%2C24h%2C7d&locale=en&precision=full')
        data = response_API.text
        return json.loads(data)
    
    def __createListedCoinObjects(self, jsonData) -> list[ListedCoinObject]: 
            return [ListedCoinObject(elem['id'], elem['market_cap_rank'], elem['image'], elem['name'], elem['symbol'], elem['current_price'], 
                                     elem['price_change_percentage_1h_in_currency'], elem['price_change_percentage_24h_in_currency'],
                                     elem['price_change_percentage_7d_in_currency'], elem['total_volume'],
                                     elem['market_cap']) for elem in jsonData]

if __name__ == '__main__':
   api = APIFetcher()