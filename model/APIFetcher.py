import requests
import json
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.coins_utils import ListedCoinObject, CoinDetailsObject, GlobalCoinDataObject
import resources.Constants as Constants

class APIFetcher():
    def __init__(self):
        self.__page = 1 
        self.__coins_loaded = 0
        self.master_coins_array: list[ListedCoinObject] = []
        self.favourites_coins_array: list[ListedCoinObject] = []
        self.portfolio_coins_array: list[ListedCoinObject] = []
        self.global_data: GlobalCoinDataObject = self.fetchGlobalData()

    
    def fetchGlobalData(self):
        try:
            global_data = self.__requestGlobalJSON()['data'] 
            return GlobalCoinDataObject(global_data['total_market_cap']['usd'], global_data['total_volume']['usd'], 
                    global_data['market_cap_percentage']['btc'], global_data['active_cryptocurrencies'], global_data['market_cap_change_percentage_24h_usd'])
        except Exception as e:
            print (e)
        
    def fetchListedCoinObjects(self, for_viewmodel):
        if for_viewmodel == Constants.ViewModel.MASTER:
            try:
                new_list: list[ListedCoinObject] = self.__createListedCoinObjects(jsonData=self.__requestPageJSON())
                self.master_coins_array += new_list
                self.__page += 1
                self.__coins_loaded += len(new_list)
                return new_list
            except Exception as e:
                
                print(e, 'zzzzz')
        elif for_viewmodel == Constants.ViewModel.FAVOURITES:
            try:
                self.favourites_coins_array = self.__createListedCoinObjects(jsonData=self.__requestSpecificCoinsJSON(Constants.ViewModel.FAVOURITES))
            except Exception as e:
                print(e)
        else:
            try:
                self.portfolio_coins_array = self.__createListedCoinObjects(jsonData=self.__requestSpecificCoinsJSON(Constants.ViewModel.PORTFOLIO))
            except Exception as e:
                print(e)
    
    def fetchCoinDetails(self, coin_id):
        try:
            data = self.__requestCoinDetailsJSON(coin_id)
            market_data = data['market_data']
            return CoinDetailsObject(data['id'], market_data['market_cap_rank'], data['image']['small'], data['name'], data['symbol'], market_data['current_price']['usd'], 
                                     market_data['market_cap']['usd'], market_data['total_volume']['usd'], market_data['circulating_supply'],
                                     market_data['ath']['usd'], market_data['atl']['usd'], market_data['price_change_percentage_1h_in_currency']['usd'], market_data['price_change_percentage_24h'], 
                                     market_data['price_change_percentage_7d'], market_data['price_change_percentage_14d'], 
                                     market_data['price_change_percentage_30d'], market_data['price_change_percentage_1y'], market_data['sparkline_7d']['price'], market_data['last_updated'])
        except Exception as e:
            print(e)


    def getSpecificCoinsID(self, for_viewmodel):
        if for_viewmodel == Constants.ViewModel.FAVOURITES:
            with open(Constants.ViewModel.FAVOURITES.value, 'r') as json_file:
                print(json_file)
                return json.load(json_file)['coins']
        else:
             print('xd')
             with open(Constants.ViewModel.PORTFOLIO.value, 'r') as json_file:
                coins = json.load(json_file)['coins']
                print('PFP',json_file)
                return coins.keys()
            
    def __requestSpecificCoinsJSON(self, for_viewmodel):
        coin_list = self.getSpecificCoinsID(for_viewmodel)
        response_API = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=' 
                     + '%2C'.join(coin_list) +'&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d')
        data = response_API.text
        return json.loads(data)
    
    def __requestCoinDetailsJSON(self, coin_id):
        response_API = requests.get(f'https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&community_data=false&developer_data=false&sparkline=true')
        data = response_API.text
        return json.loads(data)


    def __requestGlobalJSON(self):
        response_API = requests.get('https://api.coingecko.com/api/v3/global')
        data = response_API.text
        return json.loads(data)

    def __requestPageJSON(self):
        response_API = requests.get(f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page={self.__page}&sparkline=false&price_change_percentage=1h%2C24h%2C7d&locale=en&precision=full')
        data = response_API.text

        # print(data)
        return json.loads(data)
    
    def __createListedCoinObjects(self, jsonData) -> list[ListedCoinObject]: 
            return [ListedCoinObject(elem['id'], elem['market_cap_rank'], elem['image'], elem['name'], elem['symbol'], elem['current_price'], 
                                     elem['price_change_percentage_1h_in_currency'], elem['price_change_percentage_24h_in_currency'],
                                     elem['price_change_percentage_7d_in_currency'], elem['total_volume'],
                                     elem['market_cap']) for elem in jsonData]

    def get_coins_loaded(self):
        return self.__coins_loaded

if __name__ == '__main__':
   api = APIFetcher()