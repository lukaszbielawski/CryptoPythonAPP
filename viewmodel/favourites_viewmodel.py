from PyQt5.QtWidgets import QTableWidget
from viewmodel.listed_viewmodel import ListedViewModel
from model.APIFetcher import APIFetcher
from resources.Constants import ListedViewModelEnum

class FavouritesViewModel(ListedViewModel):
    #This view model manages favourties view and control display of its widgets
    def __init__(self, ratio: float, main_vm, api: APIFetcher, table_widget: QTableWidget):
        super().__init__(ratio, main_vm, api, table_widget)
        self.api = api
        self.loadFavourites()
        

    def loadFavourites(self):
        #This method loads favourite coins from APIFetcher and adding rows that are representing these coins to view's table widget 
        if len(self.api.getSpecificCoinsID(ListedViewModelEnum.FAVOURITES)) == 0: return
        self.api.fetchListedCoinObjects(ListedViewModelEnum.FAVOURITES)
        coins = self.api.favourites_coins_array
        try:
            for i in range(len(coins)):
                self.addRow(i, coins[i].id, coins[i].market_cap_rank, coins[i].image, coins[i].name, 
                        coins[i].symbol, coins[i].current_price, coins[i].price_change_percentage_1h_in_currency,
                          coins[i].price_change_percentage_24h_in_currency, coins[i].price_change_percentage_7d_in_currency, 
                          coins[i].total_volume, coins[i].market_cap)
        except Exception as e:
            print(e)
        self.setNumberOfFavouriteCoinsValue(len(self.api.favourites_coins_array))


    def setNumberOfFavouriteCoinsValue(self, number):
        #Sets number of coins that are favourite to display in proper widget
        self.view.favourites_number_of_favourite_coins_value.setText(str(number))

    def getClickedRow(self, row, column):
        #Opens details view for clicked row's ID
        self.main_vm.detailsRequest(self.api.favourites_coins_array[row].id)

    def clearView(self):
        #This method disconnect buttons to later avoid multiple connections and reseting table and number of favourite coins
        self.row_count = 0
        self.table_widget.setRowCount(0)
        self.setNumberOfFavouriteCoinsValue(0)
        
    

