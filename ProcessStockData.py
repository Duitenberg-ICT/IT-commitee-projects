import pandas as pd
import json
import numpy as np

class StockScreener:
    def __init__(self, json_file):
        """
        Initializes the StockScreener object.

        Args:
        json_file (str): Path to the JSON file containing stock data.

        The constructor loads the JSON data, converts it to a pandas DataFrame, 
        sets default numeric keys, and computes unique industries.
        """
        # Load JSON data and convert to DataFrame
        with open(json_file, 'r') as file:
            data = json.load(file)
        self.df = pd.DataFrame(data)
        
        # Set default numeric keys and convert them to numeric type
        self.numeric_keys = ['trailingPE', 'fiveYearAvgDividendYield']
        self.convert_to_numeric(self.numeric_keys)
        
        # Compute unique industries from the DataFrame
        self.unique_industries = self.df['industry'].unique()

    def convert_to_numeric(self, keys):
        """
        Converts specified columns to numeric types.

        Args:
        keys (list of str): Column names to be converted to numeric types.

        This method is used to handle non-numeric types and missing values in numeric columns.
        """
        for key in keys:
            self.df[key] = pd.to_numeric(self.df[key], errors='coerce')

    def update_numeric_keys(self, keys):
        """
        Updates the numeric keys and converts the new keys to numeric types.

        Args:
        keys (list of str): New column names to be set as numeric keys.
        """
        self.numeric_keys = keys
        self.convert_to_numeric(keys)

    def get_unique_industries(self):
        """
        Returns the unique industries present in the data.

        Returns:
        A list of unique industries.
        """
        return self.unique_industries

    def calculate_statistics(self, stats_funcs):
        """
        Calculates specified statistics for each industry.

        Args:
        stats_funcs (list of functions): Statistical functions to apply (e.g., np.mean, np.median).

        Returns:
        A dictionary with industry names as keys and corresponding statistics as values.
        """
        df_selected = self.df[['industry'] + self.numeric_keys]
        results = {}
        for func in stats_funcs:
            results[func.__name__] = df_selected.groupby('industry').agg(func)
        return results

# Usage example
json_file = 'stock_data.json'
screener = StockScreener(json_file)

# Updating numeric keys if needed
screener.update_numeric_keys(['marketCap', 'volume'])

# Get unique industries
print(screener.get_unique_industries())

# Calculate statistics
statistics = screener.calculate_statistics([np.mean, np.median])
print(statistics['mean'])
print(statistics['median'])
