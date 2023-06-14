# CryptoPythonAPP
CryptoPythonAPP is a Python application that allows users to browse and manage crypto coins. It provides the ability to browse for crypto coins, add coins to favorites and track value of your coins in a locally stored portfolio.

## Features
<ul>
  <li>Browse Cryptocurrencies: Users can browse through a list of available crypto coins and view detailed information about each coin, such as its symbol, current price, market cap and more.
  <li>Add Coins to Favorites: Users can add their favorite coins to a favorites list for quick access and tracking.
  <li>Portfolio Management: Users can create and manage their crypto coin portfolio by adding coins to their portfolio. The portfolio provides an overview of all the coins a user is currently holding.
</ul>

## Installation
<ol>
  <li>Clone the repository</li>
     
```bash
git clone https://github.com/lukaszbielawski/CryptoPythonAPP.git
 ```
   <li>Navigate to the project directory:</li>
     
```bash
cd CryptoPythonAPP
 ```
  <li>Install the required dependencies:</li>
     
```bash
pip install -r requirements.txt
 ```
 </ol>
 
 ## Usage
 
<ol>
  <li>Change screen ratio in main.py if needed:</li>
  
```python
if __name__ == '__main__':
    ratio = 1
    #Screen ratio value is needed to display views in proper scale
    app = Application(sys.argv, ratio)
 ```
  <li>Run the application:</li>
  
```bash
python main.py
 ```
   <li>Browse for crypto coins, add coins to favorites, and manage your portfolio using the intuitive user interface.</li>
</ol>

## License 
[MIT License](https://www.mit.edu/~amini/LICENSE.md)
