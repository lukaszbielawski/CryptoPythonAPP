from enum import Enum

class Color(Enum):
    #This enumerator contains some constant color codes used in application
    DARK_GRAY = '#778899'
    BLUE_GRAY = '#CBD0DE'
    LIGHT_GRAY = '#808080'
    RED = '#F0302C'
    GREEN = '#54EE1F'
    WHITE = '#FFFFFF'
    BLACK = '#171717'
    TRANSPARENT = 'rgba(0, 0, 0, 0)'

class ListedViewModelEnum(Enum):
    #This enumerator contains possible listed view models and in case of favourites and portfolio view model it stores it local storage data path
    MASTER = ''
    FAVOURITES = './data/favourites.json'
    PORTFOLIO = './data/portfolio.json'

class DetailsStarButton(Enum):
    #This enumerator manages state of star button which can be found in details view
    FILL = True
    EMPTY = False

class DetailsPortfolioButton(Enum):
    #This enumerator manages state of plus button which can be found in details view
    FILL = 0
    EMPTY = 1
    TRASH = 2

