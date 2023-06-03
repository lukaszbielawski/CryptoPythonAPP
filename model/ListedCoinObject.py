

class ListedCoinObject():
    def __init__(self, id, market_cap_rank, image, name, symbol, current_price, 
                 price_change_percentage_1h_in_currency, price_change_percentage_24h_in_currency, 
                 price_change_percentage_7d_in_currency, total_volume, market_cap):
        self.id = id
        self.market_cap_rank = market_cap_rank
        self.image = image
        self.name = name
        self.symbol = symbol
        self.current_price = current_price
        self.price_change_percentage_1h_in_currency = price_change_percentage_1h_in_currency
        self.price_change_percentage_24h_in_currency = price_change_percentage_24h_in_currency
        self.price_change_percentage_7d_in_currency = price_change_percentage_7d_in_currency
        self.total_volume = total_volume
        self.market_cap = market_cap