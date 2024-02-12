import requests
from bs4 import BeautifulSoup

def calculate_dicounte_rate(premium = 6):
    """
    A reasonable discount rate assumption should be at least the long term average return of the stock market,
    which can be estimated from risk free rate plus risk premium of stock market.
    We used the 10-Year Treasury Constant Maturity Rate as the risk free rate and rounded up to the nearest integer,
    then added a risk premium of 6% to get the estimated discount rate.
    Some investors use their expected rate of return, which is also reasonable.
    A typical discount rate can be anywhere between 6% - 20%.
    """
    average_return_rate_SP500 = 12.4
    
    return average_return_rate_SP500 + premium
    
    

print(calculate_dicounte_rate())