import pandas as pd
import json
import numpy as np

class StockScreener:
    def __init__(self):
        """
        Initializes the StockScreener object.

        Args:
        json_file (str): Path to the JSON file containing stock data.

        The constructor loads the JSON data, converts it to a pandas DataFrame, 
        sets default numeric keys, and computes unique industries.
        """
        # Load JSON data and convert to DataFrame
        json_file = 'stock_data.json'
        with open(json_file, 'r') as file:
            data = json.load(file)
        self.df = pd.DataFrame(data)
        
        # Set default numeric keys and convert them to numeric type
        self.numeric_keys = ['trailingPE', 'fiveYearAvgDividendYield', 'debtToEquity','profitMargins']
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
        valid_keys = [key for key in keys if key in self.df.columns and not pd.api.types.is_numeric_dtype(self.df[key])]
        self.numeric_keys = valid_keys
        self.convert_to_numeric(valid_keys)

    def add_numeric_key(self, key):
        """
        Adds a new numeric key and converts it to a numeric type.

        Args:
        key (str): New column name to be added as a numeric key.
        """
        if key in self.df.columns and not pd.api.types.is_numeric_dtype(self.df[key]):
            self.numeric_keys.append(key)
            self.convert_to_numeric([key])
        else:
            print(f"Key '{key}' is not a valid column or is already numeric.")

    def remove_numeric_key(self, key):
        """
        Removes a numeric key.

        Args:
        key (str): Column name to be removed from numeric keys.
        """
        if key in self.numeric_keys:
            self.numeric_keys.remove(key)
        else:
            print(f"Key '{key}' is not a numeric key.")
            
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
    def compareIndustry2Stock(self, industry, stock):
        """
        Compares the stock to the industry.

        Args:
        industry (str): The industry to compare to.
        stock (str): The stock to compare to the industry.

        Returns:
        A dictionary with the stock and industry statistics.
        """
        df_selected = self.df[['industry'] + self.numeric_keys]
        results = {}
        results[stock] = df_selected[df_selected['industry'] == stock].describe()
        results[industry] = df_selected[df_selected['industry'] == industry].describe()
        return results

# Usage example

screener = StockScreener()

# Updating numeric keys if needed
#screener.update_numeric_keys(['marketCap', 'volume'])

# Get unique industries
print(screener.get_unique_industries())

# Calculate statistics
statistics = screener.calculate_statistics([np.mean, np.median])
print(statistics['mean'])
print(statistics['median'])
