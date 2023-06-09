from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
import view.view as view
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import math
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import matplotlib.figure, json
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from model.APIFetcher import APIFetcher
import model.coins_utils as utils
from resources.Constants import Color, ViewModel, DetailsStarButton,  DetailsPortfolioButton

class DetailsViewModel():
    def __init__(self, main_vm, view: view.View, api: APIFetcher, coin_id):
        print(coin_id, 'details_id')
        self.view = view
        self.main_vm = main_vm
        self.plusButtonState = 0
        self.coin_id = coin_id
        self.coin_details = api.fetchCoinDetails(self.coin_id)
        print('coin details len', self.coin_details.id, self.coin_details.image, self.coin_details.market_cap_rank)
        self.changed = False
        self.__cfgButtons()
        self.__setDetails()
        

        
    def __cfgButtons(self):
        with open(ViewModel.FAVOURITES.value, 'r') as favourites_file:
            favourites_dict = json.load(favourites_file)
            self.isFavourite = self.coin_id in favourites_dict['coins']

        with open(ViewModel.PORTFOLIO.value, 'r') as portfolio_file:
            portfolio_dict = json.load(portfolio_file)
            self.isInPortfolio = self.coin_id in portfolio_dict['coins'].keys()

        self.view.details_star_button.clicked.connect(self.clickedFavouriteButton)
        self.view.details_plus_button.clicked.connect(self.clickedPlusButton)
        self.view.details_portfolio_tick_button.clicked.connect(self.clickedTickButton)

        self.__hidePortfolioForm()

        self.__setDetailsPortfolioButton(DetailsPortfolioButton.TRASH if self.isInPortfolio else DetailsPortfolioButton.FILL)
        self.__setDetailsStarButton(DetailsStarButton.FILL if self.isFavourite else DetailsStarButton.EMPTY)


        print(self.isFavourite, self.isInPortfolio)
       
    def __setDetails(self):
        self.setRank(self.coin_details.market_cap_rank)
        self.setDetailsCoinID(self.coin_details.id, self.coin_details.image, self.coin_details.name, self.coin_details.symbol)

        self.setDetailsCoinPriceWidget(self.coin_details.current_price)
        self.setDetailsCoinPriceChangeWidget(self.coin_details.price_change_percentage_24h)

        self.setDetailsMarketCapWidget(self.coin_details.market_cap)
        self.setDetailsTradingVolumeWidget(self.coin_details.total_volume)
        self.setDetailsCirculatingSupplyWidget(self.coin_details.circulating_supply)
        self.setDetailsAllTimeHighWidget(self.coin_details.ath)
        self.setDetailsAllTimeLowWidget(self.coin_details.atl)

        self.plot_container_layout = self.__cfgPlot(self.coin_details.sparkline, self.coin_details.last_updated)
        self.setTimeChangeTableValues(self.coin_details.price_change_percentage_1h, self.coin_details.price_change_percentage_24h, self.coin_details.price_change_percentage_7d,
                                  self.coin_details.price_change_percentage_14d, self.coin_details.price_change_percentage_30d, self.coin_details.price_change_percentage_1y)


    def setRank(self, value):
        try:
            self.view.rank_label.setMaximumSize(QtCore.QSize(int((70 + math.floor(math.log10(value)) * 15) * self.view.ratio), int(30 * self.view.ratio)))
            self.view.rank_label.setText("Rank #" + str(value))
        except Exception as _:
            self.view.rank_label.setText("Rank #–")
        
    
    def setDetailsCoinID(self, coin_id, coin_logo, coin_name, coin_symbol):
        pixmap = utils.download_and_cache_coin_image(coin_id, coin_logo, ratio=self.view.ratio, size=50)
        self.view.details_coin_logo_label.setPixmap(pixmap)
        try:
            self.view.details_coin_name_label.setText(coin_name)
            self.view.details_coin_symbol_label.setText(coin_symbol)
        except Exception as _:
            self.view.details_coin_name_label.setText('Unknown')
            self.view.details_coin_symbol_label.setText('Unk')

    def setDetailsCoinPriceWidget(self, value):
        try:
            self.view.details_coin_price_label.setText(utils.format_price(value))
        except Exception as _:
            self.view.details_coin_price_label.setText("–")

    def setDetailsCoinPriceChangeWidget(self, change):
        try:
            if change >= 0.0:
                self.view.details_coin_change_label.setText(f'<font color={Color.GREEN.value}>{utils.format_percentage(change)}</font>')
            else:
                self.view.details_coin_change_label.setText(f'<font color={Color.RED.value}>{utils.format_percentage(change)}</font>')
        except Exception as _:
            self.view.details_coin_change_label.setText(f'<font color={Color.WHITE.value}>–%</font>')
            

    def setDetailsMarketCapWidget(self, value):
        try:
            self.view.details_market_cap_widget_value.setText(utils.format_big_price(value))
        except Exception as _:
            self.view.details_market_cap_widget_value.setText('–')

    def setDetailsTradingVolumeWidget(self, value):
        try:
            self.view.details_market_cap_widget_value.setText(utils.format_big_price(value))
        except Exception as _:
            self.view.details_trading_volume_widget_value.setText('–')

    def setDetailsCirculatingSupplyWidget(self, value):
        try:
            self.view.details_circulating_supply_widget_value.setText(utils.format_number(int(value)))
        except Exception as _:
            self.view.details_circulating_supply_widget_value.setText(0)

    def setDetailsAllTimeHighWidget(self, value):
        try:
            self.view.details_all_time_high_widget_value.setText(utils.format_price(value))
        except Exception as _:
            self.view.details_all_time_high_widget_value.setText('–')

    def setDetailsAllTimeLowWidget(self, value):
        try:
            self.view.details_all_time_low_widget_value.setText(utils.format_price(value))
        except Exception as _:
            self.view.details_all_time_low_widget_value.setText('-')

    def setTimeChangeTableValues(self, *args):
        for column, arg in enumerate(args):
            try:
                item = QLabel(utils.format_percentage(arg))
            except Exception as _: 
                item = QLabel('–')
                self.view.time_change_table.setCellWidget(0, column, item)
                return   
            arial = QFont()
            arial.setFamily('Arial')
            item.setAlignment(Qt.AlignCenter)
            if float(arg) >= 0.0:
                item.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + "; color : " + Color.GREEN.value +";}")
            else:                   
                item.setStyleSheet("QLabel { background-color : " + Color.TRANSPARENT.value + "; color : " + Color.RED.value +";}")
            arial.setPixelSize(int(20 * self.view.ratio))
            item.setFont(arial)
            self.view.time_change_table.setCellWidget(0, column, item)   

    def clickedFavouriteButton(self):
        self.changed = True
        if self.isFavourite:
            self.__setDetailsStarButton(DetailsStarButton.EMPTY)
            self.__removeFavouritesEntry()
            self.isFavourite = False
        else:
            self.__setDetailsStarButton(DetailsStarButton.FILL)
            self.__addFavouritesEntry()
            self.isFavourite = True
        
    def clickedPlusButton(self):
        if self.plusButtonState == 2:
            print('a')
            self.__removePortfolioEntry()
            self.__setDetailsPortfolioButton(DetailsPortfolioButton.FILL)
        elif self.plusButtonState == 0:
            self.__showPortfolioForm()
            self.__setDetailsPortfolioButton(DetailsPortfolioButton.EMPTY)
        else:
            self.__hidePortfolioForm()
            self.__setDetailsPortfolioButton(DetailsPortfolioButton.FILL)
    
    def clickedTickButton(self):
        try:
            amount = float(self.view.details_portfolio_bought_amount_text.text())
            price = float(self.view.details_portfolio_price_text.text())
            if amount <= 0.0 or price <= 0.0:
                raise Exception("Amount cannot be below 0")
            self.view.details_portfolio_bought_amount_label.setText('Bought amount')
            self.view.details_portfolio_price_label.setText('Price')
            self.__hidePortfolioForm()

            # print(amount, price)
            self.changed = True
            self.__setDetailsPortfolioButton(DetailsPortfolioButton.TRASH)
            self.__addPortfolioEntry(amount, price)

            
        except Exception as e:
            self.view.details_portfolio_bought_amount_label.setText(f'<font color={Color.RED.value}>Bought amount</font>')
            self.view.details_portfolio_price_label.setText(f'<font color={Color.RED.value}>Price</font>')
            print(e)
    
    def __setDetailsStarButton(self, state):
        if state == DetailsStarButton.FILL:
            self.view.details_star_button.setStyleSheet("border-image: url(./resources/star_fill.png);\nbackground: " + Color.TRANSPARENT.value + ";")
        else:
            self.view.details_star_button.setStyleSheet("border-image: url(./resources/star_empty.png);\nbackground: " + Color.TRANSPARENT.value + ";")

    def __setDetailsPortfolioButton(self, state):
        if state == DetailsPortfolioButton.FILL:
            self.view.details_plus_button.setStyleSheet("border-image: url(./resources/plus_fill.png);\nbackground: " + Color.TRANSPARENT.value + ";")
        elif state == DetailsPortfolioButton.EMPTY:
            self.view.details_plus_button.setStyleSheet("border-image: url(./resources/plus_empty.png);\nbackground: " + Color.TRANSPARENT.value + ";")
        else:
            self.view.details_plus_button.setStyleSheet("border-image: url(./resources/trash_bin.png);\nbackground: " + Color.TRANSPARENT.value + ";")
        self.plusButtonState = state.value

    def __hidePortfolioForm(self):
        self.view.details_portfolio_bought_amount_label.hide()
        self.view.details_portfolio_bought_amount_text.hide()
        self.view.details_portfolio_price_label.hide()
        self.view.details_portfolio_price_text.hide()
        self.view.details_portfolio_tick_button.hide()

    def __showPortfolioForm(self):
        self.view.details_portfolio_bought_amount_label.show()
        self.view.details_portfolio_bought_amount_text.show()
        self.view.details_portfolio_price_label.show()
        self.view.details_portfolio_price_text.show()
        self.view.details_portfolio_tick_button.show()
       
    def __cfgPlot(self, sparkline, last_updated):
        matplotlib.use('QT5Agg')
        class MplCanvas(FigureCanvasQTAgg):
            def __init__(self, parent: DetailsViewModel):
                self.parent = parent
                self.figure = Figure(figsize=(0, 0), constrained_layout=True,)
                # self.figure.tight_layout()
                self.__createPlot(sparkline, last_updated)
                FigureCanvasQTAgg.__init__(self, self.figure)
                FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                FigureCanvasQTAgg.updateGeometry(self)

            def __createPlot(self, sparkline, last_updated):
                self.figure.patch.set_facecolor(Color.BLACK.value)
                
                y = sparkline
                x = pd.date_range(start=last_updated - timedelta(days=7), end=last_updated, periods=len(y))
                

                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
                plt.gca().xaxis.set_major_locator(mdates.DayLocator())
                plt.gcf().autofmt_xdate()

                plt.rcParams['axes.xmargin'] = 0

                self.ax = self.figure.add_subplot(111)
                self.ax.set_facecolor(Color.BLACK.value)
                for spine in self.ax.spines.values():
                    spine.set_color(Color.WHITE.value)
                self.ax.tick_params(colors=Color.WHITE.value, labelsize=(14 * self.parent.view.ratio))

                if sparkline[0] > sparkline[-1]:
                    plot_color = Color.RED.value
                elif sparkline[0] < sparkline[-1]:
                    plot_color = Color.GREEN.value
                else:
                    plot_color = Color.WHITE.value
                    
                self.ax.plot(x, y, color=plot_color)

        
        self.view.plot_container_layout.addWidget(MplCanvas(self))

    def __addPortfolioEntry(self, amount, price):
        with open(ViewModel.PORTFOLIO.value, 'r+') as portfolio_file:
            portfolio_dict = json.load(portfolio_file)
            print(portfolio_dict)
            portfolio_dict['coins'][self.coin_id] = dict()
            print('id', self.coin_id)
            portfolio_dict['coins'][self.coin_id]['amount'] = amount
            portfolio_dict['coins'][self.coin_id]['price'] = price
            portfolio_json = json.dumps(portfolio_dict, indent=4)
            portfolio_file.seek(0)
            portfolio_file.write(portfolio_json)
            portfolio_file.truncate()
        self.main_vm.update_portfolio = True

    def __removePortfolioEntry(self):
        with open(ViewModel.PORTFOLIO.value, 'r+') as portfolio_file:
            portfolio_dict = json.load(portfolio_file)
            portfolio_dict['coins'].pop(self.coin_id)
            portfolio_json = json.dumps(portfolio_dict, indent=4)

            portfolio_file.seek(0)
            portfolio_file.write(portfolio_json)
            portfolio_file.truncate()
        self.main_vm.update_portfolio = True

    def __addFavouritesEntry(self):
        with open(ViewModel.FAVOURITES.value, 'r+') as favourites_file:
            favourites_dict = json.load(favourites_file)
            favourites_dict['coins'].append(self.coin_id)
            favourites_json = json.dumps(favourites_dict, indent=4)

            favourites_file.seek(0)
            favourites_file.write(favourites_json)
            favourites_file.truncate()
        self.main_vm.update_favourites = True

    def __removeFavouritesEntry(self):
        with open(ViewModel.FAVOURITES.value, 'r+') as favourites_file:
            favourites_dict = json.load(favourites_file)
            favourites_dict['coins'].remove(self.coin_id)
            favourites_json = json.dumps(favourites_dict, indent=4)

            favourites_file.seek(0)
            favourites_file.write(favourites_json)
            favourites_file.truncate()
        self.main_vm.update_favourites = True
    
    def clearView(self):
        plot = self.view.plot_container_layout.itemAt(0)
        plot.widget().setParent(None)
        
        self.view.details_star_button.clicked.disconnect(self.clickedFavouriteButton)
        self.view.details_plus_button.clicked.disconnect(self.clickedPlusButton)
        self.view.details_portfolio_tick_button.clicked.disconnect(self.clickedTickButton)