import json
import requests
import yfinance as yf
import threading
import queue
import datetime
import subprocess
import os

def worker(ticker_queue, data_list, lock, progress_counter):
    while not ticker_queue.empty():
        ticker_entry = ticker_queue.get()
        symbol = None
        # Determine the type of ticker_entry and set the symbol accordingly
        if isinstance(ticker_entry, dict):
            # For NASDAQ stocks structured as dictionaries
            symbol = ticker_entry['Symbol']
        elif isinstance(ticker_entry, str):
            # For Amsterdam stocks that are just strings
            symbol = ticker_entry
        else:
            print(f"Unsupported ticker format: {ticker_entry}")
            ticker_queue.task_done()
            continue
        
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            with lock:
                data_list.append(info)
                progress_counter[0] += 1
                print(f"Progress: {progress_counter[0]} / {len(NASDAQ_Tickers) + len(amsterdam_stocks)} stock: {symbol}")
        except Exception as e:
            print(f"Error retrieving data for {symbol}: {e}")
            progress_counter[0] += 1
        finally:
            ticker_queue.task_done()


# Fetching Amsterdam stocks from the txt file
with open('amsterdam_stocks.txt', 'r') as file:
    amsterdam_stocks = file.read().splitlines()
      

# Fetching NASDAQ tickers
response = requests.get("https://datahub.io/core/nasdaq-listings/r/nasdaq-listed.json")
NASDAQ_Tickers = response.json()

# Creating a queue and a lock
ticker_queue = queue.Queue()
lock = threading.Lock()

#Populate the queue with Amsterdam stocks
for ticker in amsterdam_stocks:
    ticker_queue.put(ticker)
    
# Populate the queue with NASDAQ tickers
for ticker in NASDAQ_Tickers:
    ticker_queue.put(ticker)



# List to store stock data
stock_data = []

# Shared counter
progress_counter = [0]  # Using a list to make it mutable

# Starting threads
num_threads = 10
threads = []

for _ in range(num_threads):
    thread = threading.Thread(target=worker, args=(ticker_queue, stock_data, lock, progress_counter))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Saving to a JSON file
with open('stock_data.json', 'w') as file:
    json.dump(stock_data, file, indent=4)
    
# Get current date and time
current_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Write the update date to a txt file
with open('StoringStockInformation/last_updated.txt', 'w') as file:
    file.write(f"{current_date_time}")
