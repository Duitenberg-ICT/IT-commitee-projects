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
        
        self.active_filters = []
        self.percentile_filters = []
        self.numerical_filters = []
        
       

    def convert_to_numeric(self, keys):
        """
        Converts specified columns to numeric types.

        Args:
        keys (list of str): Column names to be converted to numeric types.

        This method is used to handle non-numeric types and missing values in numeric columns.
        """
        for key in keys:
            self.df[key] = pd.to_numeric(self.df[key], errors='coerce')
            # Using .loc to avoid SettingWithCopyWarning
            self.dfSelected.loc[:, key] = pd.to_numeric(self.dfSelected[key], errors='coerce')

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
            print(f"Key '{key}' is not a selected numeric key.")
            
    def get_numeric_keys(self):
        """
        Returns the numeric keys.

        Returns:
        A list of numeric keys.
        """
        return self.numeric_keys
    
    def get_string_keys(self):
        """
        Returns the string keys.

        Returns:
        A list of string keys.
        """
        return self.string_keys
    
    def get_keys(self):
        """
        Returns the keys.

        Returns:
        A list of keys.
        """
        return self.dfSelected.keys()
            
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
    
    def add_filter(self, filter_func, *args, **kwargs):
        """
        Adds a filter to the active filters list and categorizes it.

        Args:
        filter_func (function): The filter function to add.
        *args, **kwargs: Arguments for the filter function.
        """
        if filter_func == StockScreener.filter_stocks_by_percentile:
            self.percentile_filters.append((filter_func, args, kwargs))
        else:
            self.numerical_filters.append((filter_func, args, kwargs))
        self.active_filters.append((filter_func, args, kwargs))
    
    def remove_filter(self, filter_func):
        """
        Removes a filter from the active filters list.

        Args:
        filter_func (function): The filter function to remove.
        """
        self.active_filters = [(f, a, k) for f, a, k in self.active_filters if f != filter_func]
        
        if filter_func == StockScreener.filter_stocks_by_percentile:
            self.percentile_filters = [(f, a, k) for f, a, k in self.percentile_filters if f != filter_func]
        elif filter_func == StockScreener.filter_stocks_by_parameter:
            self.numerical_filters = [(f, a, k) for f, a, k in self.numerical_filters if f != filter_func]
        

    def apply_filters(self):
        """
        Applies all active filters to the DataFrame sequentially, prioritizing percentile filters.

        Returns:
        A DataFrame after applying all filters.
        """
        #print(self.active_filters)
        
        filtered_df = self.dfSelected.copy()

        # Apply percentile filters first
        for filter_func, args, kwargs in self.percentile_filters:
            filtered_df = filter_func(filtered_df, *args, **kwargs)

        # Apply numerical filters next
        for filter_func, args, kwargs in self.numerical_filters:
            filtered_df = filter_func(filtered_df, *args, **kwargs)

        return filtered_df
    
    
    
    @staticmethod
    def filter_stocks_by_percentile(df, key, top_percentile=100, top=True, industry=None):
        """
        Filters stocks based on their ranking in a certain numerical aspect,
        optionally within a specific industry.

        Args:
        df (DataFrame): The DataFrame to apply the filter to.
        key (str): The numerical key to rank stocks by (e.g., 'profitMargins').
        top_percentile (float): The percentile to use as a threshold (0 to 100).
        top (bool): If True, select the top percentile, else select the bottom.
        industry (str or list of str, optional): The industry or industries to filter by.

        Returns:
        A DataFrame with stocks in the specified percentile range, sorted from best to worst.
        """
        if key not in df.columns:
            print(f"Key '{key}' not found in data.")
            return None

        # Calculate percentile ranks
        local_df = df.copy()
        local_df['percentile_rank'] = local_df[key].rank(pct=True) * 100

        # Filter by industry if specified
        if industry:
            if isinstance(industry, list):
                local_df = local_df[local_df['industry'].isin(industry)]
            else:
                local_df = local_df[local_df['industry'] == industry]

        # Filter based on the specified percentile
        percentile = 100 - top_percentile if top else top_percentile
        if top:
            filtered_stocks = local_df[local_df['percentile_rank'] >= percentile]
        else:
            filtered_stocks = local_df[local_df['percentile_rank'] <= percentile]

        # Sort the DataFrame by percentile rank
        filtered_stocks = filtered_stocks.sort_values(by='percentile_rank', ascending=top == False)

        # Drop the 'percentile_rank' column before returning
        return filtered_stocks.drop(columns=['percentile_rank'])
    
    @staticmethod
    def filter_stocks_by_parameter(df,key, min = -np.Inf, max = np.Inf, industry=None):
        """
        Filters stocks based on their ranking in a certain numerical aspect,
        optionally within a specific industry.

        Args:
        df (DataFrame): The DataFrame to apply the filter to.
        key (str): The numerical key to rank stocks by (e.g., 'profitMargins').
        min (float): The minimum value to use as a threshold.
        max (float): The maximum value to use as a threshold.
        industry (str or list of str, optional): The industry or industries to filter by.

        Returns:
        A DataFrame with stocks in the specified percentile range, sorted from best to worst.
        """
        if key not in df.columns:
            print(f"Key '{key}' not found in data.")
            return None

        # Calculate percentile ranks
        local_df = df.copy()
        #local_df['percentile_rank'] = local_df[key].rank(pct=True) * 100

        # Filter by industry if specified
        if industry:
            if isinstance(industry, list):
                local_df = local_df[local_df['industry'].isin(industry)]
            else:
                local_df = local_df[local_df['industry'] == industry]

        filtered_stocks = local_df[(local_df[key] >= min) & (local_df[key] <= max)]
        # Sort the DataFrame by percentile rank
        filtered_stocks = filtered_stocks.sort_values(by=key, ascending=True)

        # Drop the 'percentile_rank' column before returning
        return filtered_stocks

# Usage example
screener = StockScreener()
# Add filters
screener.add_filter(StockScreener.filter_stocks_by_percentile, 'profitMargins', top_percentile=10, top=True)
screener.add_filter(StockScreener.filter_stocks_by_parameter, 'trailingPE', min=15, max = 20)

# Apply filters
filtered_data = screener.apply_filters()
print(filtered_data)

screener2 = StockScreener()
# apply hard filter
filtered_data2 = screener2.filter_stocks_by_parameter(screener2.dfSelected, 'trailingPE', min=15, max = 20)
#print(filtered_data2)

#top_10_percent_profit_margin_stocks = screener.filter_stocks_by_percentile('profitMargins',industry='Asset Management', top = True)
#print(top_10_percent_profit_margin_stocks)

# Usage example


# Updating numeric keys if needed
#screener.update_numeric_keys(['marketCap', 'volume'])

# Get unique industries
#print(screener.get_unique_industries())

# Calculate statistics
#statistics = screener.calculate_statistics([np.mean, np.median])
#print(statistics['mean'])
#print(statistics['median'])
