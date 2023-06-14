
from view.view import View
import viewmodel.master_viewmodel as master_vm
import viewmodel.favourites_viewmodel as favourites_vm
import viewmodel.details_viewmodel as details_vm
import viewmodel.portfolio_viewmodel as portfolio_vm
from model.APIFetcher import APIFetcher
from resources.Constants import Color

class MainViewModel():
    #This view model is responsible for managing display of views that are located in stacked widget
    #It also manages upper navigation bar view
    def __init__(self, view: View, api: APIFetcher):
        self.view = view
        self.update_favourites = False
        self.update_portfolio = False
        self.api = api
        self.master_viewmodel = master_vm.MasterViewModel(self.view, self, api, self.view.master_table_widget) #default view
        self.favourites_viewmodel = None
        self.portfolio_viewmodel = None
        self.details_viewmodel = None
        self.__connectButtons()
        
    def __connectButtons(self):
        #This connects navigation bar button to proper methods
        self.view.quit_button.clicked.connect(self.view.window.close)
        self.view.main_button.clicked.connect(lambda: self.mainButtonClicked())
        self.view.favourites_button.clicked.connect(lambda: self.favouritesButtonClicked())
        self.view.my_portfolio_button.clicked.connect(lambda: self.myPortfolioButtonClicked())
        self.view.tooltip_search_button.clicked.connect(lambda: self.searchButtonClicked())

    def mainButtonClicked(self):
        #Called when big Bitcoin logo is clicked and switches view to master one
        self.view.stackedWidget.setCurrentIndex(0)

    def favouritesButtonClicked(self):
        #Called when favourites button is clicked and switches view to favourites one
        #Checks if state of favorites was changed or for its existence and reloads view if needed
        if self.favourites_viewmodel is None:
            self.favourites_viewmodel = favourites_vm.FavouritesViewModel(self.view, self, self.api, self.view.favourites_table)
        if self.update_favourites:
            self.update_favourites = False
            self.favourites_viewmodel.clearView()
            self.favourites_viewmodel.loadFavourites()
        self.view.stackedWidget.setCurrentIndex(2)

    def myPortfolioButtonClicked(self):
        #Called when my portfolio button is clicked and switches view to portfolio one
        #Checks if state of portfolio was changed or for its existence and reloads view if needed
        if self.portfolio_viewmodel is None:
            self.portfolio_viewmodel = portfolio_vm.PortfolioViewModel(self.view, self, self.api, self.view.portfolio_table_widget)
        if self.update_portfolio:
            self.update_portfolio = False
            self.portfolio_viewmodel.clearView()
            self.portfolio_viewmodel.loadPortfolio()
        self.view.stackedWidget.setCurrentIndex(3)

    def searchButtonClicked(self):
        #Called when my search button is clicked
        self.api.fetchSearchCoins()
        self.matchSearch(self.view.tooltip_search_text.text())

    def matchSearch(self, text):
        #Checks for apperance of text in search bar and tries to match expression to get the best result, which is the longest common prefix
        try:
            print(' txt' ,text)
            coin_tuple = sorted(filter(lambda x: x[1].lower().startswith(text.lower()), self.api.search_coins_dict.items()), key=lambda x: x[1].lower())
            color = Color.WHITE.value
            placeholder = 'Search...'
        except Exception as e:
            color = Color.RED.value
            placeholder = 'Could not match the text'
        if len(coin_tuple) == 0: 
            print('Could not match expression')
            return
        self.view.tooltip_search_text.setPlaceholderText(placeholder)
        self.view.tooltip_search_text.setStyleSheet("background: #232323;\n"
            "border: 1px solid;\n"
            "color: " + color + ";\n"
            "font-family: Arial, Helvetica, sans-serif;\n"
            "font-size: " + str(int(20 * self.view.ratio)) + "px;\n"
            "")
        self.detailsRequest(coin_tuple[0][0])
        #Loads detail view for best match's ID

    def detailsRequest(self, coin_id):
        #Loads details view for ID given by other views or search bar
        if self.details_viewmodel is not None:
            self.details_viewmodel.clearView()

        self.details_viewmodel = details_vm.DetailsViewModel(self, self.view, self.api, coin_id)
        self.view.stackedWidget.setCurrentIndex(1)