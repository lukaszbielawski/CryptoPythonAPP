from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt
from view.view import View

class MasterViewModel():
    def __init__(self, view: View):
        print('mv nint')
        self.view = view
        self.table_size = 0
        self.numbers = {0: 91, 1: 637, 2: 218, 3: 127, 4: 127, 5: 127, 6: 255, 7: 350}
        self.__cfgTable()
        self.view.master_table_widget.setRowCount(self.table_size)
        self.addRow('1', './resources/logo.png', 'Bitcoin', 'BTC', '$26,961.43', '-0.1%', '-2.6%', '+2.4%', '$16,332,763,917', '$522,840,485,971')
        self.addRow('2', './resources/logo.png', 'Bitcoin', 'BTC', '$26,961.43', '-0.1%', '-2.6%', '+2.4%', '$16,332,763,917', '$522,840,485,971')
        
    class CoinLogoWidget(QLabel):
        def __init__(self, imagePath, parent):
            super(QLabel, self).__init__()
            pixmap = QtGui.QPixmap(imagePath)
            smaller_pic = pixmap.scaled(int(20 * parent.view.ratio), int(20 * parent.view.ratio))
            self.setPixmap(smaller_pic)

    def addRow(self, no, coin_logo, coin_name, coin_symbol, price, one_hour, twenty_four_hour, seven_days, volume, market_cap):
        
        self.table_size += 1
        self.view.master_table_widget.setRowCount(self.table_size)
        self.view.master_table_widget.setRowHeight(self.table_size - 1, int(28 * self.view.ratio))
        # self.view.master_table_widget.resizeRowsToContents()

        coin_data_widget = QWidget()

        coin_data_layout =QHBoxLayout()
        coin_data_layout.setContentsMargins(0,0,0,0)
        coin_data_layout.setSpacing(int(12 * self.view.ratio))

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
        self.view.master_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.master_table_widget.setFocusPolicy(Qt.NoFocus)
        self.view.master_table_widget.setSelectionMode(QAbstractItemView.NoSelection)       
        self.view.master_table_widget.cellClicked.connect(self.getClickedRow)
        self.view.master_table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.master_table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.master_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.view.master_table_widget.verticalHeader().setMaximumSectionSize(int(36 * self.view.ratio))
        self.view.master_table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.view.master_table_widget.setColumnWidth(0, int(self.numbers[0] * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(1, int(self.numbers[1] * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(2, int(self.numbers[2] * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(3, int(self.numbers[3] * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(4, int(self.numbers[4] * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(5, int(self.numbers[5] * self.view.ratio))
        self.view.master_table_widget.setColumnWidth(6, int(self.numbers[6] * self.view.ratio))
        # self.view.master_table_widget.setColumnWidth(7, int(350 * self.view.ratio))

    def addItemAt(self, row, column, item: QWidget, layout=None):
        item.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 0); color : white;}")
        # item.setAlignment(Qt.AlignCenter)
        arial = QFont()
        arial.setFamily('Arial')
        match column:
            case 0:
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 1:
                arial.setPixelSize(int(20 * self.view.ratio))
                layout.itemAt(1).widget().setFont(arial)
                layout.itemAt(2).widget().setFont(arial)
            case 2:
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 3:
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 4:
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 5:
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case 6:
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
            case _:
                arial.setPixelSize(int(20 * self.view.ratio))
                item.setFont(arial)
        
        self.view.master_table_widget.setCellWidget(row, column, item)   

    
    def getClickedRow(self, row, column):
        print(row)
        return row  


