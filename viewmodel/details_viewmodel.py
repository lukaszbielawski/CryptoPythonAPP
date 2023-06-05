from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
import view.view as view
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import matplotlib.figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from model.APIFetcher import APIFetcher
from model.coins_utils import CoinDetailsObject, CoinLogoWidget, download_and_cache_coin_image
from resources.Constants import Color

class DetailsViewModel():
    def __init__(self, view: view.View, api: APIFetcher, coin_id):
        self.view = view
        self.isFavourite = False
        self.plusButtonState = 0
        self.coin_id = coin_id
        self.coin_details = api.fetchCoinDetails(coin_id)
        self.__cfgButtons()
        self.__cfgTimeChangeTable()
       
        
        self.setRank(self.coin_details.market_cap_rank)

        self.setDetailsCoinID(self.coin_details.id, self.coin_details.image, self.coin_details.name, self.coin_details.symbol)

        self.setDetailsCoinPriceWidget(self.coin_details.current_price)
        self.setDetailsCoinPriceChangeWidget(self.coin_details.price_change_percentage_24h)

        self.setDetailsMarketCapWidget(self.coin_details.market_cap)
        self.setDetailsTradingVolumeWidget(self.coin_details.total_volume)
        self.setDetailsCirculatingSupplyWidget(self.coin_details.circulating_supply)
        self.setDetailsAllTimeHighWidget(self.coin_details.ath)
        self.setDetailsAllTimeLowWidget(self.coin_details.atl)
        print(self.coin_details.sparkline)
        self.plot_container_layout = self.__cfgPlot(self.coin_details.sparkline, self.coin_details.last_updated)
        self.setTimeChangeTableValues(self.coin_details.price_change_percentage_1h, self.coin_details.price_change_percentage_24h, self.coin_details.price_change_percentage_7d,
                                  self.coin_details.price_change_percentage_14d, self.coin_details.price_change_percentage_30d, self.coin_details.price_change_percentage_1y)

    def __cfgButtons(self):
        self.view.pushButton.clicked.connect(self.clickedFavouriteButton)
        self.view.pushButton_2.clicked.connect(self.clickedPlusButton)
        self.view.details_portfolio_tick_button.clicked.connect(self.clickedTickButton)



    # global_data = self.api.global_data
    #     self.setMarketCapSuffixLabel(int(global_data.total_market_cap), global_data.market_cap_change_percentage_24h)
    #     self.setMarketCapWidgetValue('${:,}'.format(int(global_data.total_market_cap)))
    #     self.setTradingVolumeWidgetValue('${:,}'.format(int(global_data.total_volume)))
    #     self.setBtcDominanceWidgetValue(str(self.__format_percentage(global_data.btc_dominance)) + '%')
    #     self.setNumberOfCoinsValue('{:,}'.format(global_data.active_cryptocurrencies))



    def setRank(self, value):
        self.view.rank_label.setText("Rank #" + str(value))
    
    def setDetailsCoinID(self, coin_id, coin_logo, coin_name, coin_symbol):
        pixmap = download_and_cache_coin_image(coin_id, coin_logo, ratio=self.view.ratio, size=50)
        # self.view.details_coin_logo_label.setStyleSheet(f"border-image: url({.});\nborder-radius: 50%;\nbackground: " + Color.TRANSPARENT.value + ";")
        self.view.details_coin_logo_label.setPixmap(pixmap)
        self.view.details_coin_name_label.setText(coin_name)
        self.view.details_coin_symbol_label.setText(coin_symbol)


# self.addItemAt(index, 2, QLabel('${:,f}'.format(price)))
#         self.addItemAt(index, 3, QLabel(str(one_hour) +'%'), value=one_hour)

    def setDetailsCoinPriceWidget(self, value):
        self.view.details_coin_price_label.setText('${:,f}'.format(value))

    def setDetailsCoinPriceChangeWidget(self, change):
        if change >= 0.0:
            self.view.details_coin_change_label.setText(f'<font color={Color.GREEN.value}>{change}%</font>')
        else:
            self.view.details_coin_change_label.setText(f'<font color={Color.RED.value}>{change}%</font>')

    def setDetailsMarketCapWidget(self, value):
        self.view.details_market_cap_widget_value.setText('${:,}'.format(value))

    def setDetailsTradingVolumeWidget(self, value):
        self.view.details_trading_volume_widget_value.setText('${:,}'.format(value))

    def setDetailsCirculatingSupplyWidget(self, value):
        self.view.details_circulating_supply_widget_value.setText('{:,}'.format(int(value)))

    def setDetailsAllTimeHighWidget(self, value):
        print('value', value)
        self.view.details_all_time_high_widget_value.setText('${:,f}'.format(value))

    def setDetailsAllTimeLowWidget(self, value):
        self.view.details_all_time_low_widget_value.setText('${:,f}'.format(value))


    def clickedFavouriteButton(self):
        if self.isFavourite:
            self.view.pushButton.setStyleSheet("border-image: url(./resources/star_empty.png);\nbackground: " + Color.TRANSPARENT.value + ";")
            self.isFavourite = False
        else:
            self.view.pushButton.setStyleSheet("border-image: url(./resources/star_fill.png);\nbackground: " + Color.TRANSPARENT.value + ";")
            self.isFavourite = True
        
    def clickedPlusButton(self):
        if self.plusButtonState == 2:
            self.view.pushButton_2.setStyleSheet("border-image: url(./resources/plus_fill.png);\nbackground: " + Color.TRANSPARENT.value + ";")
            self.plusButtonState = 0
        elif self.plusButtonState == 0:
            self.__showPortfolioForm()
            self.view.pushButton_2.setStyleSheet("border-image: url(./resources/plus_empty.png);\nbackground: " + Color.TRANSPARENT.value + ";")
            self.plusButtonState = 1
        else:
            self.__hidePortfolioForm()
            self.view.pushButton_2.setStyleSheet("border-image: url(./resources/plus_fill.png);\nbackground: " + Color.TRANSPARENT.value + ";")
            self.plusButtonState = 0
    
    def clickedTickButton(self):
        try:
            amount = float(self.view.details_portfolio_bought_amount_text.text())
            price = float(self.view.details_portfolio_price_text.text())
            if amount <= 0.0 or price <= 0.0:
                raise Exception("Amount cannot be below 0")
            self.view.details_portfolio_bought_amount_label.setText('Bought amount')
            self.view.details_portfolio_price_label.setText('Price')
            self.__hidePortfolioForm()
            print(amount, price)
            self.view.pushButton_2.setStyleSheet("border-image: url(./resources/trash_bin.png);\nbackground: " + Color.TRANSPARENT.value + ";")
            self.plusButtonState = 2
        except Exception as e:
            self.view.details_portfolio_bought_amount_label.setText(f'<font color={Color.RED.value}>Bought amount</font>')
            self.view.details_portfolio_price_label.setText(f'<font color={Color.RED.value}>Price</font>')
            print(e)

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

    def setTimeChangeTableValues(self, *args):
        for column, arg in enumerate(args):
            item = QLabel(str(arg) + "%")
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
                # x = [last_updated - timedelta(days=x) for x in range(7)]
                x = pd.date_range(start=last_updated - timedelta(days=7), end=last_updated, periods=len(y))
                

                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
                plt.gca().xaxis.set_major_locator(mdates.DayLocator())
                # plt.plot(x_lin,y)
                plt.gcf().autofmt_xdate()

                plt.rcParams['axes.xmargin'] = 0





                # x = np.linspace(0, L)
                # ncolors = len(plt.rcParams['axes.prop_cycle'])
                # shift = np.linspace(0, L, ncolors, endpoint=False)
                self.ax = self.figure.add_subplot(111)
                self.ax.set_facecolor(Color.BLACK.value)
                for spine in self.ax.spines.values():
                    spine.set_color(Color.WHITE.value)
                self.ax.tick_params(colors=Color.WHITE.value, labelsize=(14 * self.parent.view.ratio))
                # for s in shift:
                if sparkline[0] > sparkline[-1]:
                    plot_color = Color.RED.value
                elif sparkline[0] < sparkline[-1]:
                    plot_color = Color.GREEN.value
                else:
                    plot_color = Color.WHITE.value
                    
                self.ax.plot(x, y, color=plot_color)

        
        self.view.plot_container_layout.addWidget(MplCanvas(self))
    
    def __cfgTimeChangeTable(self):
        self.view.time_change_table
        self.view.time_change_table.setRowCount(1)
        self.view.time_change_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.time_change_table.setFocusPolicy(Qt.NoFocus)
        self.view.time_change_table.setSelectionMode(QAbstractItemView.NoSelection)       
        self.view.time_change_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.time_change_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.time_change_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.view.time_change_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)