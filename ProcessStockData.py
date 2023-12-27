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
        self.string_keys = ['industry', 'shortName','symbol']
        
        self.dfSelected = self.df[self.string_keys + self.numeric_keys]
        
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
        self.dfSelected = self.df[self.string_keys + self.numeric_keys]

    def add_numeric_key(self, key):
        """
        Adds a new numeric key and converts it to a numeric type.

        Args:
        key (str): New column name to be added as a numeric key.
        """
        if key in self.df.columns and not pd.api.types.is_numeric_dtype(self.df[key]):
            self.numeric_keys.append(key)
            self.convert_to_numeric([key])
            self.dfSelected = self.df[self.string_keys + self.numeric_keys]
            
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
            self.dfSelected = self.df[self.string_keys + self.numeric_keys]
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
    
    def filter_stocks_by_percentile(self, key, top_percentile, top=True, industry=None):
        """
        Filters stocks based on their ranking in a certain numerical aspect,
        optionally within a specific industry.

        Args:
        key (str): The key to rank stocks by (e.g., 'profitMargins').
        percentile (float): The percentile to use as a threshold (0 to 100).
        top (bool): If True, select the top percentile, else select the bottom.
        industry (str or list of str, optional): The industry or industries to filter by.

        Returns:
        A DataFrame with stocks in the specified percentile range, sorted from best to worst.
        """
        if key not in self.dfSelected.columns:
            print(f"Key '{key}' not found in selected data.")
            return None

        # Copy the DataFrame and calculate percentile ranks
        local_df = self.dfSelected.copy()
        local_df['percentile_rank'] = local_df[key].rank(pct=True) * 100

        # Filter by industry if specified
        if industry:
            if isinstance(industry, list):
                local_df = local_df[local_df['industry'].isin(industry)]
            else:
                local_df = local_df[local_df['industry'] == industry]

        # Filter based on the specified percentile
        percentile = 100- top_percentile if top else top_percentile
        if top:
            filtered_stocks = local_df[local_df['percentile_rank'] >= percentile]
        else:
            filtered_stocks = local_df[local_df['percentile_rank'] <= percentile]

        # Sort the DataFrame by percentile rank
        sort_order = 'percentile_rank' if top else '-percentile_rank'
        filtered_stocks = filtered_stocks.sort_values(by='percentile_rank', ascending=top == False)

        # Drop the 'percentile_rank' column before returning
        filtered_stocks = filtered_stocks.drop(columns=['percentile_rank'])

        return filtered_stocks

# Usage example
screener = StockScreener()
top_10_percent_profit_margin_stocks = screener.filter_stocks_by_percentile('profitMargins', 2, top = True)
print(top_10_percent_profit_margin_stocks)

# Usage example

#screener = StockScreener()

# Updating numeric keys if needed
#screener.update_numeric_keys(['marketCap', 'volume'])

# Get unique industries
#print(screener.get_unique_industries())

# Calculate statistics
#statistics = screener.calculate_statistics([np.mean, np.median])
#print(statistics['mean'])
#print(statistics['median'])
