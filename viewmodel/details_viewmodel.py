from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
import view.view as view
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
import matplotlib.figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class DetailsViewModel():
    def __init__(self, view: view.View):
        self.view = view
        self.isFavourite = False
        self.plusButtonState = 0
        self.__cfgButtons()
        self.setRank(5)
        self.setDetailsCoinID('./resources/logo.png', 'Bitcoin', 'BTC')
        self.setDetailsMarketCapWidget('$233,356,313,313')
        self.setDetailsTradingVolumeWidget('$19,323,631,643')
        self.setDetailsCirculatingSupplyWidget('232,321')
        self.setDetailsAllHighLowWidget('$770,533.12')
        self.setDetailsAllHighLowWidget('$0.12')
        self.__cfgPlot()
        self.__cfgTimeChangeTable()
        self.setTimeChangeTableValues(0.3, -2.5, 2.6, -0.9, -2.3, -14.7)

    def __cfgButtons(self):
        self.view.pushButton.clicked.connect(self.clickedFavouriteButton)
        self.view.pushButton_2.clicked.connect(self.clickedPlusButton)
        self.view.details_portfolio_tick_button.clicked.connect(self.clickedTickButton)

    def setRank(self, value):
        self.view.rank_label.setText("Rank #" + str(value))
    
    def setDetailsCoinID(self, logo_url, name, symbol):
        self.view.details_coin_logo_label.setStyleSheet(f"border-image: url({logo_url});\nborder-radius: 50%;\nbackground: rgba(0, 0, 0, 0);")
        self.view.details_coin_name_label.setText(name)
        self.view.details_coin_symbol_label.setText(symbol)

    def setDetailsMarketCapWidget(self, value):
        self.view.details_market_cap_widget_value.setText(str(value))

    def setDetailsTradingVolumeWidget(self, value):
        self.view.details_trading_volume_widget_value.setText(str(value))

    def setDetailsCirculatingSupplyWidget(self, value):
        self.view.details_circulating_supply_widget_value.setText(str(value))

    def setDetailsAllTimeHighWidget(self, value):
        self.view.details_all_time_high_widget_value.setText(str(value))

    def setDetailsAllHighLowWidget(self, value):
        self.view.details_all_time_low_widget_value.setText(str(value))


    def clickedFavouriteButton(self):
        if self.isFavourite:
            self.view.pushButton.setStyleSheet(f'border-image: url(./resources/star_empty.png);\nbackground: rgba(0, 0, 0, 0);')
            self.isFavourite = False
        else:
            self.view.pushButton.setStyleSheet(f'border-image: url(./resources/star_fill.png);\nbackground: rgba(0, 0, 0, 0);')
            self.isFavourite = True
        
    def clickedPlusButton(self):
        if self.plusButtonState == 2:
            self.view.pushButton_2.setStyleSheet(f'border-image: url(./resources/plus_fill.png);\nbackground: rgba(0, 0, 0, 0);')
            self.plusButtonState = 0
        elif self.plusButtonState == 0:
            self.__showPortfolioForm()
            self.view.pushButton_2.setStyleSheet(f'border-image: url(./resources/plus_empty.png);\nbackground: rgba(0, 0, 0, 0);')
            self.plusButtonState = 1
        else:
            self.__hidePortfolioForm()
            self.view.pushButton_2.setStyleSheet(f'border-image: url(./resources/plus_fill.png);\nbackground: rgba(0, 0, 0, 0);')
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
            self.view.pushButton_2.setStyleSheet(f'border-image: url(./resources/trash_bin.png);\nbackground: rgba(0, 0, 0, 0);')
            self.plusButtonState = 2
        except Exception as e:
            self.view.details_portfolio_bought_amount_label.setText('<font color=#F0302C>Bought amount</font>')
            self.view.details_portfolio_price_label.setText('<font color=#F0302C>Price</font>')
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
            if float(arg) > 0:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #54EE1F;}")
            else:                   
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #F0302C;}")
            arial.setPixelSize(int(20 * self.view.ratio))
            item.setFont(arial)
            self.view.time_change_table.setCellWidget(0, column, item)   
       
    def __cfgPlot(self):
        matplotlib.use('QT5Agg')
        # plt.style.use('dark_background')
        class MplCanvas(FigureCanvasQTAgg):
            def __init__(self, parent: DetailsViewModel):
                self.parent = parent
                self.figure = Figure(figsize=(0, 0), constrained_layout=True)
                self.__createPlot()
                FigureCanvasQTAgg.__init__(self, self.figure)
                FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                FigureCanvasQTAgg.updateGeometry(self)

            def __createPlot(self):
                self.figure.patch.set_facecolor('#171717')
                L = 6
                x = np.linspace(0, L)
                ncolors = len(plt.rcParams['axes.prop_cycle'])
                shift = np.linspace(0, L, ncolors, endpoint=False)
                self.ax = self.figure.add_subplot(111)
                self.ax.set_facecolor('#171717')
                for spine in self.ax.spines.values():
                    spine.set_color('white')
                # self.ax.xaxis.label.set_color('white')
                self.ax.tick_params(colors='white', labelsize=(14 * self.parent.view.ratio))
                for s in shift:
                    self.ax.plot(x, np.sin(x + s), 'o-')

        box = QtWidgets.QVBoxLayout()
        box.addWidget(MplCanvas(self))      

        self.view.matplotlib_widget.setLayout(box)
        # class MplWidget(QtWidgets.QWidget):
        #     def __init__(self, parent=None):
        #         QtWidgets.QWidget.__init__(self, parent)   
        #         self.canvas = MplCanvas()                  
        #         self.vbl = QtWidgets.QVBoxLayout()         
        #         self.vbl.addWidget(self.canvas)
        #         self.setLayout(self.vbl)    
        
        # self.view.matplotlib_widget = MplWidget()
        # self.details_layout.addWidget(self.matplotlib_widget)
    
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