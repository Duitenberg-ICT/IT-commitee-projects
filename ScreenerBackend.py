import yfinance as yf
import pandas as pd
import numpy as np
import requests
# Example stock data retrieval

import_ticker = "FLOW.AS"
stock = yf.Ticker(import_ticker)
info = stock.info
# get the company name
company_name = info['longName']
# get the net margin
net_margin = info['profitMargins']
# get the debt to equity ratio
debt_to_equity = info['debtToEquity']
# get the sector
sector = info['sector']
#print(info)
# current price of the stock
current_price = info['currentPrice']
# P/E ratio
PE = info['trailingPE']
# Market Cap
market_cap = info['marketCap']
# balance sheet
balance_sheet = stock.balance_sheet