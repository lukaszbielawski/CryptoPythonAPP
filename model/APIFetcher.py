import requests
import json
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.coins_utils import ListedCoinObject, CoinDetailsObject, GlobalCoinDataObject
import resources.Constants as Constants

class APIFetcher():
    #This class contains CoinGeekoAPI's fetching methods and stores results of their calls
    def __init__(self):
        self.__page = 1 
        self.__coins_loaded = 0
        self.master_coins_array: list[ListedCoinObject] = []
        self.favourites_coins_array: list[ListedCoinObject] = []
        self.portfolio_coins_array: list[ListedCoinObject] = []
        self.search_coins_dict = dict()
        self.global_data: GlobalCoinDataObject = self.fetchGlobalData()

    
    def fetchGlobalData(self):
        #This method fetches current global market data about cryptocurrencies, parses it to auxiliary objects and stores it in self.global_data
        try:
            global_data = self.__requestGlobalJSON()['data'] 
            return GlobalCoinDataObject(global_data['total_market_cap']['usd'], global_data['total_volume']['usd'], 
                    global_data['market_cap_percentage']['btc'], global_data['active_cryptocurrencies'], global_data['market_cap_change_percentage_24h_usd'])
        except Exception as e:
            print(e)

    def fetchSearchCoins(self):
        #This method fetches names and IDs of all available coins and stores them in self.search_coins_dict
        try:
            search_data = self.__requestSearchCoinsJSON()
            for elem in search_data:
                self.search_coins_dict[elem['id']] = f"{elem['name']}"       
        except Exception as e:
            print(e)

        
    def fetchListedCoinObjects(self, for_viewmodel):
        #This method fetches primary data about coins that are stored in lists, parses it to auxiliary objects and stores them in proper list
        if for_viewmodel == Constants.ListedViewModelEnum.MASTER:
            try:
                new_list: list[ListedCoinObject] = self.__createListedCoinObjects(jsonData=self.__requestPageJSON())
                self.master_coins_array += new_list
                self.__page += 1
                self.__coins_loaded += len(new_list)
                return new_list
            except Exception as e:
                print(e)
        elif for_viewmodel == Constants.ListedViewModelEnum.FAVOURITES:
            try:
                self.favourites_coins_array = self.__createListedCoinObjects(jsonData=self.__requestSpecificCoinsJSON(Constants.ListedViewModelEnum.FAVOURITES))
            except Exception as e:
                print(e)
        else:
            try:
                self.portfolio_coins_array = self.__createListedCoinObjects(jsonData=self.__requestSpecificCoinsJSON(Constants.ListedViewModelEnum.PORTFOLIO))
            except Exception as e:
                print(e)
    
    def fetchCoinDetails(self, coin_id):
        #This method fetches detailed data about selected coin, parses it to auxiliary object and returns it
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
        #This method reads favourites or portfolio coins from proper stored files and returns IDs of them
        if for_viewmodel == Constants.ListedViewModelEnum.FAVOURITES:
            with open(Constants.ListedViewModelEnum.FAVOURITES.value, 'r') as json_file:
                print(json_file)
                return json.load(json_file)['coins']
        else:
             with open(Constants.ListedViewModelEnum.PORTFOLIO.value, 'r') as json_file:
                coins = json.load(json_file)['coins']
                return coins.keys()
            
    def __requestSpecificCoinsJSON(self, for_viewmodel):
        #This method is making call to API to fetch primary data for selected view based on obtained IDs and returns data in JSON
        coin_list = self.getSpecificCoinsID(for_viewmodel)
        response_API = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=' 
                     + '%2C'.join(coin_list) +'&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d')
        data = response_API.text
        return json.loads(data)
    
    def __requestCoinDetailsJSON(self, coin_id):
        #This method is making call to API to fetch detailed data for coin and return data in JSON
        response_API = requests.get(f'https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&community_data=false&developer_data=false&sparkline=true')
        data = response_API.text
        return json.loads(data)


    def __requestGlobalJSON(self):
        #This method is making call to API to fetch global data for cryptocurrency market and returns data in JSON
        response_API = requests.get('https://api.coingecko.com/api/v3/global')
        data = response_API.text
        return json.loads(data)

    def __requestPageJSON(self):
        #This method is making call to API to fetch primary data for cryptocurrencies that are on given page and returns data in JSON
        response_API = requests.get(f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page={self.__page}&sparkline=false&price_change_percentage=1h%2C24h%2C7d&locale=en&precision=full')
        data = response_API.text
        return json.loads(data)

    def __requestSearchCoinsJSON(self):
        #This method is making call to API to identification data for all cryptocurrencies and returns data in JSON
        response_API = requests.get(f'https://api.coingecko.com/api/v3/coins/list?include_platform=false')
        data = response_API.text
        return json.loads(data)
    
    def __createListedCoinObjects(self, jsonData) -> list[ListedCoinObject]:
        #Returns list of objects storing primary data of coins
        return [ListedCoinObject(elem['id'], elem['market_cap_rank'], elem['image'], elem['name'], elem['symbol'], elem['current_price'], 
                                    elem['price_change_percentage_1h_in_currency'], elem['price_change_percentage_24h_in_currency'],
                                    elem['price_change_percentage_7d_in_currency'], elem['total_volume'],
                                    elem['market_cap']) for elem in jsonData]

    def get_coins_loaded(self):
        return self.__coins_loaded