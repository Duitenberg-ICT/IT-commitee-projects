import pandas as pd
import numpy as np
import requests
import yfinance as yf
#===============================================================================
# This file will scour the internet for stock data and store it in a database
#===============================================================================

#Feting a list of tickers from the NASDAQ website
response = requests.get("https://datahub.io/core/nasdaq-listings/r/nasdaq-listed.json")
NASDAQ_Tickers = response.json()

# Create a new Json file that reads the tickers from the NASDAQ website and retrieves their stock date from the ticker