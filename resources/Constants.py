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
    MASTER = 1
    FAVOURITES = 2
    PORTFOLIO = 3

favourites_path = './data/favourites.json'
portfolio_path = './data/favourites.json'