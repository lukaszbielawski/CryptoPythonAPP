from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
import view.view as view
import viewmodel.details_viewmodel as details_vm

class PortfolioViewModel():
    def __init__(self, view: view.View, main_vm):
        print('portfolio nint')
        self.view = view
        self.main_vm = main_vm
        self.table_size = 0
        self.setTotalBalance('$1,552.92')
        self.setPortfolioChange('-$61.23')
        self.setTotalProfit('-$1,323.45')
        self.__cfgTable()
        self.view.portfolio_table_widget
        self.view.portfolio_table_widget.setRowCount(self.table_size)
        self.addRow('1', './resources/logo.png', 'Bitcoin', 'BTC', '$26,961.43', '-0.1%', '-2.6%', '+2.4%', '$16,332,763,917', '$522,840,485,971')
        self.addRow('2', './resources/logo.png', 'Bitcoin', 'BTC', '$26,961.43', '-0.1%', '-2.6%', '+2.4%', '$16,332,763,917', '$522,840,485,971')
        self.setNumberOfCoins()
        
    class CoinLogoWidget(QLabel):
        def __init__(self, imagePath, parent):
            super(QLabel, self).__init__()
            pixmap = QtGui.QPixmap(imagePath)
            smaller_pic = pixmap.scaled(int(20 * parent.view.ratio), int(20 * parent.view.ratio))
            self.setPixmap(smaller_pic)

    def addRow(self, no, coin_logo, coin_name, coin_symbol, price, one_hour, twenty_four_hour, seven_days, volume, market_cap):
        
        self.table_size += 1
        self.view.portfolio_table_widget.setRowCount(self.table_size)
        self.view.portfolio_table_widget.setRowHeight(self.table_size - 1, int(28 * self.view.ratio))

        coin_data_widget = QWidget()

        coin_data_layout = QHBoxLayout()
        coin_data_layout.setContentsMargins(8,0,0,0)
        coin_data_layout.setSpacing(int(8 * self.view.ratio))

        coin_logo_widget = self.CoinLogoWidget(coin_logo, self)
        coin_name_widget = QLabel(coin_name)
        coin_symbol_widget = QLabel(coin_symbol)

        coin_data_layout.addWidget(coin_logo_widget)
        coin_data_layout.addWidget(coin_name_widget)
        coin_data_layout.addWidget(coin_symbol_widget)
        coin_data_layout.addSpacerItem(QSpacerItem(int(10 * self.view.ratio), int(20 * self.view.ratio), QSizePolicy.Minimum, QSizePolicy.Expanding))
        coin_data_layout.setStretch(0, 0)
        coin_data_layout.setStretch(1, 0)
        coin_data_layout.setStretch(2, 0)
        coin_data_layout.setStretch(3, 1)

        coin_data_widget.setLayout(coin_data_layout)

        self.addItemAt(self.table_size -1, 0, QLabel(no))
        self.addItemAt(self.table_size -1, 1, coin_data_widget, coin_data_layout)
        self.addItemAt(self.table_size -1, 2, QLabel(price))
        self.addItemAt(self.table_size -1, 3, QLabel(one_hour))
        self.addItemAt(self.table_size -1, 4, QLabel(twenty_four_hour))
        self.addItemAt(self.table_size -1, 5, QLabel(seven_days))
        self.addItemAt(self.table_size -1, 6, QLabel(volume))
        self.addItemAt(self.table_size -1, 7, QLabel(market_cap))


        

    def __cfgTable(self):
        self.view.portfolio_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.portfolio_table_widget.setFocusPolicy(Qt.NoFocus)
        self.view.portfolio_table_widget.setSelectionMode(QAbstractItemView.NoSelection)       
        self.view.portfolio_table_widget.cellClicked.connect(self.getClickedRow)
        self.view.portfolio_table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.portfolio_table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.portfolio_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.view.portfolio_table_widget.verticalHeader().setMaximumSectionSize(int(36 * self.view.ratio))
        self.view.portfolio_table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.view.portfolio_table_widget.setColumnWidth(0, int(91 * self.view.ratio))
        self.view.portfolio_table_widget.setColumnWidth(1, int(637 * self.view.ratio))
        self.view.portfolio_table_widget.setColumnWidth(2, int(218 * self.view.ratio))
        self.view.portfolio_table_widget.setColumnWidth(3, int(127 * self.view.ratio))
        self.view.portfolio_table_widget.setColumnWidth(4, int(127 * self.view.ratio))
        self.view.portfolio_table_widget.setColumnWidth(5, int(127 * self.view.ratio))
        self.view.portfolio_table_widget.setColumnWidth(6, int(255 * self.view.ratio))
        # self.view.portfolio_table_widget.setColumnWidth(7, int(350 * self.view.ratio))

    def addItemAt(self, row, column, item: QWidget, layout=None):
        # item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : white;}")
        
        arial = QFont()
        arial.setFamily('Arial')
        
        if column != 1:
            item.setAlignment(Qt.AlignCenter)
            item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #778899;}")

        match column:
            case 0:
                item.setStyleSheet("QLabel { background-color: rgba(0, 0, 0, 0); color: white;}")
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 1:
                arial.setPixelSize(int(20 * self.view.ratio))
                coin_name_widget = layout.itemAt(1).widget()
                coin_name_widget.setFont(arial)
                coin_symbol_widget = layout.itemAt(2).widget()
                coin_symbol_widget.setFont(arial)
                coin_name_widget.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : white;}")
                coin_symbol_widget.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); font-size: " + str(int(16 * self.view.ratio)) + "px; color : #778899;}")
            case 2:
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : white;}")
                item.setFont(arial)
            case 3:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #F0302C;}")
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 4:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #F0302C;}")
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 5:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #54EE1F;}")
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 6:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #CBD0DE;}")
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case _:
                item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : #CBD0DE;}")
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
        
        self.view.portfolio_table_widget.setCellWidget(row, column, item)   

    def setTotalBalance(self, value):
        self.view.portfolio_total_balance_widget_value.setText(str(value))

    def setPortfolioChange(self, value):
        self.view.portfolio_change_widget_value.setText(str(value))

    def setTotalProfit(self, value):
        self.view.total_profit_widget_value.setText(str(value))

    def setNumberOfCoins(self):
        self.view.portfolio_number_of_coins_widgetvalue.setText(str(self.table_size))

    def getClickedRow(self, row, column):
        self.main_vm.detailsRequest()
        print(row)
        # return row  


