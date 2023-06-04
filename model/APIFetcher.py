import requests
import json
import sys, os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.ListedCoinObject import ListedCoinObject

class APIFetcher():
    def __init__(self):
        self.page = 1 
        self.coins_loaded = 0
        self.listed_coins_array: list[ListedCoinObject] = []
        self.global_data_tuple = self.fetchGlobalData()

    
    def fetchGlobalData(self):
        try:
            global_data = self.__requestGlobalJSON()['data'] 
            return (int(global_data['total_market_cap']['usd']), int(global_data['total_volume']['usd']), 
                    global_data['market_cap_percentage']['btc'], global_data['active_cryptocurrencies'], global_data['market_cap_change_percentage_24h_usd'])
        except Exception as e:
            print (e)
        
    def fetchNewListedCoins(self):
        try:
            new_list: list[ListedCoinObject] = self.__createListedCoinObjects(jsonData=self.__requestPageJSON())
            self.listed_coins_array += new_list
            self.page += 1
            self.coins_loaded += len(new_list)
            return new_list
        except Exception as e:
            print(e)
        return None

    def __requestGlobalJSON(self):
        response_API = requests.get('https://api.coingecko.com/api/v3/global')
        data = response_API.text
        return json.loads(data)

    def __requestPageJSON(self):
        response_API = requests.get(f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page={self.page}&sparkline=false&price_change_percentage=1h%2C24h%2C7d&locale=en&precision=full')
        data = response_API.text
        # print(data)
        return json.loads(data)
    
    def __createListedCoinObjects(self, jsonData) -> list[ListedCoinObject]: 
            return [ListedCoinObject(elem['id'], elem['market_cap_rank'], elem['image'], elem['name'], elem['symbol'], elem['current_price'], 
                                     elem['price_change_percentage_1h_in_currency'], elem['price_change_percentage_24h_in_currency'],
                                     elem['price_change_percentage_7d_in_currency'], elem['total_volume'],
                                     elem['market_cap']) for elem in jsonData]

if __name__ == '__main__':
   api = APIFetcher()