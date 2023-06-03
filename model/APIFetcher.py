from pycoingecko import CoinGeckoAPI

class APIFetcher():
    def __init__(self):
        api = CoinGeckoAPI()
        print(api.get_price(ids='bitcoin', vs_currencies='usd'))
        api.get_coins
if __name__ == '__main__':
    fetcher = APIFetcher()