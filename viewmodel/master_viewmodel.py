from PyQt5.QtWidgets import QTableWidget
import view.view as view
from model.APIFetcher import APIFetcher
import model.coins_utils as utils
from resources.Constants import Color, ListedViewModelEnum
from viewmodel.listed_viewmodel import ListedViewModel

class MasterViewModel(ListedViewModel):
    #This class manages master view and is responsible for proper pagination of fetched coins to table
    def __init__(self, ratio: float, main_vm, api: APIFetcher, table_widget: QTableWidget):
        super().__init__(ratio, main_vm, api, table_widget)
        self.table_widget.verticalScrollBar().valueChanged.connect(self.onMasterTableScroll)
        self.readyToScroll = True
        self.already_loaded = 0
        self.per_page = 40
        #Amount of loaded coins per one load request
        self.loadGlobalStats()
        self.loadPage()

    def onMasterTableScroll(self):
        #Called when table is scrolled, if bottom row index reached end, it loads up more coins
        rect = self.view.master_table_widget.viewport().rect()
        bottom_index = self.view.master_table_widget.indexAt(rect.bottomLeft()).row()
        if bottom_index + 1 == self.already_loaded and self.readyToScroll:
            self.readyToScroll = False
            self.loadPage()
            self.readyToScroll = True

    def loadPage(self):
        #Called when there is no more coins left fetched by api and still there is request to load more coins
        if self.already_loaded + self.per_page > self.api.get_coins_loaded():
            self.api.fetchListedCoinObjects(ListedViewModelEnum.MASTER)
            #Calling this method adds another 250 coins to coin pool
        try:
            coins = self.api.master_coins_array
            for i in range(self.per_page):
                self.addRow(self.already_loaded + i, coins[self.already_loaded + i].id, coins[self.already_loaded + i].market_cap_rank, coins[self.already_loaded + i].image, coins[self.already_loaded + i].name, 
                        coins[self.already_loaded + i].symbol, coins[self.already_loaded + i].current_price, coins[self.already_loaded + i].price_change_percentage_1h_in_currency,
                          coins[self.already_loaded + i].price_change_percentage_24h_in_currency, coins[self.already_loaded + i].price_change_percentage_7d_in_currency, 
                          coins[self.already_loaded + i].total_volume, coins[self.already_loaded + i].market_cap)
            self.already_loaded += self.per_page
        except Exception as e:
            print(e)

    def loadGlobalStats(self):
        #This method is setting up widgets according to global data fetch by APIFetcher
        global_data = self.api.global_data
        self.setMarketCapSuffixLabel(global_data.total_market_cap, global_data.market_cap_change_percentage_24h)
        self.setMarketCapWidgetValue(global_data.total_market_cap)
        self.setTradingVolumeWidgetValue(global_data.total_volume)
        self.setBtcDominanceWidgetValue(global_data.btc_dominance)
        self.setNumberOfCoinsValue(global_data.active_cryptocurrencies)
    
    #Below methods are setting up proper widgets
    def setMarketCapSuffixLabel(self, value, change):
        if change >= 0:
            self.view.market_cap_suffix_label.setText(f'{utils.convert_number_to_written(value)}, a <font color={Color.GREEN.value}>{utils.format_percentage(change)}</font> increase in the last 24 hours.')
        else:
            self.view.market_cap_suffix_label.setText(f'{utils.convert_number_to_written(value)}, a <font color={Color.RED.value}>{utils.format_percentage(change)}</font> decrease in the last 24 hours.')
    
    def setMarketCapWidgetValue(self, value):
        self.view.market_cap_widget_value.setText(utils.format_big_price(value))

    def setTradingVolumeWidgetValue(self, value):
        self.view.trading_volume_widget_value.setText(utils.format_big_price(value))

    def setBtcDominanceWidgetValue(self, value):
        self.view.btc_dominance_widget_value.setText(utils.format_percentage(value))

    def setNumberOfCoinsValue(self, value):
        self.view.number_of_coins_widget_value.setText(utils.format_number(value))



    def getClickedRow(self, row, column):
        #Opens details view for clicked row's ID
        self.main_vm.detailsRequest(self.api.master_coins_array[row].id)


