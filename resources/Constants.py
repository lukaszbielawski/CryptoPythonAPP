from enum import Enum

class Color(Enum):
    DARK_GRAY = '#778899'
    BLUE_GRAY = '#CBD0DE'
    LIGHT_GRAY = '#808080'
    RED = '#F0302C'
    GREEN = '#54EE1F'
    WHITE = '#FFFFFF'
    BLACK = '#171717'
    TRANSPARENT = 'rgba(0, 0, 0, 0)'

class ViewModel(Enum):
    MASTER = ''
    FAVOURITES = './data/favourites.json'
    PORTFOLIO = './data/portfolio.json'

class DetailsStarButton(Enum):
    FILL = True
    EMPTY = False

class DetailsPortfolioButton(Enum):
    FILL = 0
    EMPTY = 1
    TRASH = 2

