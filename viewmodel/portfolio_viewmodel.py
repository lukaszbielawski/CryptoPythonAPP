from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QTableWidget
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
import view.view as view
from viewmodel.listed_viewmodel import ListedViewModel
from resources.Constants import ViewModel
from model.APIFetcher import APIFetcher
import model.coins_utils as utils
from decimal import Decimal
import json
import functools
from resources.Constants import Color


class PortfolioViewModel(ListedViewModel):
    def __init__(self, ratio: float, main_vm, api: APIFetcher, table_widget: QTableWidget):
        super().__init__(ratio, main_vm, api, table_widget)
        self.total_balance = 0.0
        self.total_profit = 0.0
        self.loadPortfolio()
        
        
    def loadPortfolio(self):
        if len(self.api.getSpecificCoinsID(ViewModel.PORTFOLIO)) == 0: return
        self.__loadBalance()
        self.api.fetchListedCoinObjects(ViewModel.PORTFOLIO)
        coins = self.api.portfolio_coins_array
        try:
            for i in range(len(coins)):
                self.addRow(i, coins[i].id, coins[i].market_cap_rank, coins[i].image, coins[i].name, 
                        coins[i].symbol, coins[i].current_price, coins[i].price_change_percentage_1h_in_currency,
                          coins[i].price_change_percentage_24h_in_currency, coins[i].price_change_percentage_7d_in_currency)
        except Exception as e:
            print(e)
        self.__setBalanceWidgets()

    def __setBalanceWidgets(self):

        self.setTotalBalance(sum(self.coin_balance_usd_dict.values()))
        self.setPortfolioChange(sum(self.coin_balance_yesterday_usd_dict.values()))
        self.setTotalProfit(sum(self.coin_profit_usd_dict.values()))
        self.setNumberOfCoins(len(self.api.portfolio_coins_array))

    def __loadBalance(self):
         with open(ViewModel.PORTFOLIO.value, 'r') as json_file:
            json_data = json.load(json_file)
            self.favourite_coin_dict = json_data['coins']

            self.coin_balance_usd_dict = dict()
            self.coin_balance_crypto_dict = dict()
            self.coin_balance_yesterday_usd_dict = dict()
            self.coin_profit_usd_dict = dict()
            self.coin_profit_percentage_dict = dict()
            


    def __calculateCoin(self, key, price, twenty_four_hour):
        self.coin_balance_usd_dict[key] = self.favourite_coin_dict[key]['amount'] * price
        self.coin_balance_crypto_dict[key] = self.favourite_coin_dict[key]['amount']
        self.coin_balance_yesterday_usd_dict[key] = self.favourite_coin_dict[key]['amount'] * price * (1.00 - twenty_four_hour) * 0.01
        self.coin_profit_usd_dict[key] = self.favourite_coin_dict[key]['amount'] * (price - self.favourite_coin_dict[key]['price'])
        self.coin_profit_percentage_dict[key] = (price / self.favourite_coin_dict[key]['price'] - 1.0) * 100.0

    def addRow(self, index, coin_id, no, coin_logo, coin_name, coin_symbol, price, one_hour, twenty_four_hour, seven_days):
        
        self.row_count += 1
        self.table_widget.setRowCount(self.row_count)
        self.table_widget.setRowHeight(index, int(28 * self.view.ratio))

        self.__calculateCoin(coin_id, float(price), twenty_four_hour)

        coin_data_widget = QWidget()

        coin_data_layout = QHBoxLayout()
        coin_data_layout.setContentsMargins(int(8 * self.view.ratio), 0, 0,0 )
        coin_data_layout.setSpacing(int(8 * self.view.ratio))

        coin_logo_widget = utils.CoinLogoWidget(coin_id, coin_logo, self, 20)
        coin_name_widget = QLabel(str(coin_name))
        coin_symbol_widget = QLabel(str(coin_symbol))

        coin_data_layout.addWidget(coin_logo_widget)
        coin_data_layout.addWidget(coin_name_widget)
        coin_data_layout.addWidget(coin_symbol_widget)
        coin_data_layout.addSpacerItem(QSpacerItem(int(10 * self.view.ratio), int(20 * self.view.ratio), QSizePolicy.Minimum, QSizePolicy.Expanding))
        coin_data_layout.setStretch(0, 0)
        coin_data_layout.setStretch(1, 0)
        coin_data_layout.setStretch(2, 0)
        coin_data_layout.setStretch(3, 1)

        coin_data_widget.setLayout(coin_data_layout)

        coin_balance_widget = QWidget()
        coin_balance_layout = QHBoxLayout()

        coin_balance_layout.setContentsMargins(int(8 * self.view.ratio), 0, int(8 * self.view.ratio), 0)
        coin_balance_layout.setSpacing(int(8 * self.view.ratio))
        coin_balance_usd = QLabel(utils.format_price(self.coin_balance_usd_dict[coin_id]))
        coin_balance_crypto = QLabel(f'{self.coin_balance_crypto_dict[coin_id]} {coin_symbol}')

        coin_balance_layout.addWidget(coin_balance_usd)
        coin_balance_layout.addSpacerItem(QSpacerItem(int(10 * self.view.ratio), int(20 * self.view.ratio), QSizePolicy.Minimum, QSizePolicy.Expanding))
        coin_balance_layout.addWidget(coin_balance_crypto)

        coin_balance_layout.setStretch(0, 0)
        coin_balance_layout.setStretch(1, 1)
        coin_balance_layout.setStretch(2, 0)
        coin_balance_widget.setLayout(coin_balance_layout)

        coin_profit_widget = QWidget()
        coin_profit_layout = QHBoxLayout()

        coin_profit_layout.setContentsMargins(int(8 * self.view.ratio), 0, int(8 * self.view.ratio), 0)
        coin_profit_layout.setSpacing(int(8 * self.view.ratio))

        if self.coin_profit_percentage_dict[coin_id] >= 0.0:
            coin_profit_usd = QLabel(utils.format_price(self.coin_profit_usd_dict[coin_id]))
        else:
            coin_profit_usd = QLabel(utils.format_price(self.coin_profit_usd_dict[coin_id]))

        coin_profit_percentage = QLabel(utils.format_percentage(self.coin_profit_percentage_dict[coin_id]))

        coin_profit_layout.addWidget(coin_profit_usd)
        coin_profit_layout.addSpacerItem(QSpacerItem(int(10 * self.view.ratio), int(20 * self.view.ratio), QSizePolicy.Minimum, QSizePolicy.Expanding))
        coin_profit_layout.addWidget(coin_profit_percentage)
        

        coin_profit_layout.setStretch(0, 0)
        coin_profit_layout.setStretch(1, 1)
        coin_profit_layout.setStretch(2, 0)
        coin_profit_widget.setLayout(coin_profit_layout)


        self.addItemAt(index, 0, QLabel(str(no))) #git
        self.addItemAt(index, 1, coin_data_widget, layout=coin_data_layout) 

        self.addItemAt(index, 2, QLabel(utils.format_price(price)))
        self.addItemAt(index, 3, QLabel(utils.format_percentage(one_hour)), value=one_hour)
        self.addItemAt(index, 4, QLabel(utils.format_percentage(twenty_four_hour)), value=twenty_four_hour)
        self.addItemAt(index, 5, QLabel(utils.format_percentage(seven_days)), value=seven_days)


        self.addItemAt(index, 6, coin_balance_widget, layout=coin_balance_layout)
        self.addItemAt(index, 7, coin_profit_widget, layout=coin_profit_layout, value=self.coin_profit_percentage_dict[coin_id])

    def addItemAt(self, row, column, item: QWidget, layout=None, value=None):

        if column in (3, 4, 5):
            if type(value) == str:
                color = Color.WHITE.value
            else:
                color = Color.GREEN.value if value >= 0.0 else Color.RED.value

        match column:
            case 0:
                color = Color.WHITE.value
                
            case 1:
                coin_name_widget = layout.itemAt(1).widget()
                coin_name_widget.setFont(self.arial)
                coin_symbol_widget = layout.itemAt(2).widget()
                coin_symbol_widget.setFont(self.arial)
                coin_name_widget.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + "; color : " + Color.WHITE.value + ";}")
                coin_symbol_widget.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + "; font-size: " + str(int(16 * self.view.ratio)) + "px; color : " + Color.DARK_GRAY.value + ";}")
            case 2:
                color = Color.WHITE.value
            case 6:
                coin_balance_usd = layout.itemAt(0).widget()
                coin_balance_usd.setFont(self.arial)
                coin_balance_crypto = layout.itemAt(2).widget()
                coin_balance_crypto.setFont(self.arial)
                coin_balance_usd.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + "; color : " + Color.WHITE.value + ";}")
                coin_balance_crypto.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + "; font-size: " + str(int(16 * self.view.ratio)) + "px; color : " + Color.BLUE_GRAY.value + ";}")
            case 7:
                coin_profit_usd = layout.itemAt(0).widget()
                coin_profit_usd.setFont(self.arial)
                coin_profit_percentage = layout.itemAt(2).widget()
                coin_profit_percentage.setFont(self.arial)
                coin_profit_usd.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + "; color : " + Color.WHITE.value + ";}")
                if value >= 0.0:
                    color = Color.GREEN.value
                else:
                    color = Color.RED.value
                coin_profit_percentage.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + "; font-size: " + str(int(16 * self.view.ratio)) + "px; color : " + color + ";}")
            case _:
                pass

        if column not in (1, 6, 7):
            item.setAlignment(Qt.AlignCenter)
            item.setFont(self.arial)
            item.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + "; color : " + color + ";}")

        self.table_widget.setCellWidget(row, column, item)



    def setTotalBalance(self, value):
        self.view.portfolio_total_balance_widget_value.setText(utils.format_price(value))

    def setPortfolioChange(self, value):
        if value >= 0.0:
            self.view.portfolio_change_widget_value.setText(utils.format_price(value))
        else:
            self.view.portfolio_change_widget_value.setText(utils.format_price(value))

    def setTotalProfit(self, value):
        if value >= 0.0:
            self.view.total_profit_widget_value.setText(utils.format_price(value))
        else:
            self.view.total_profit_widget_value.setText(utils.format_price(value))

    def setNumberOfCoins(self, number):
        self.view.portfolio_number_of_coins_widgetvalue.setText(str(number))

    def getClickedRow(self, row, column):
        self.main_vm.detailsRequest(self.api.portfolio_coins_array[row].id)
        
    def clearView(self):
        self.row_count = 0
        self.table_widget.setRowCount(0)
        self.setTotalBalance(0)
        self.setPortfolioChange(0)
        self.setTotalProfit(0)
        self.setNumberOfCoins(0)
        

