import pandas as pd
import json
import numpy as np
from flask import Flask, request, jsonify
import ProcessStockData as psd
import ssl  # For HTTPS

app = Flask(__name__)

# Initialize your StockScreener once so you don't have to reload data for every request
screener = psd.StockScreener()


@app.route('/get_filtered-parameter_data', methods=['GET'])
def get_filtered_parameter_data():
    """This route will add a parameter filter and return the filtered data after applying the filter"""
    
    # Retrieve query parameters
    key = request.args.get('key', default='profitMargins', type=str)
    min_val = request.args.get('min', default=-float('-inf'), type=float)
    max_val = request.args.get('max', default=float('inf'), type=float)
    top_percentile = request.args.get('top_percentile', default=100, type=float)
    top = request.args.get('top', default=True, type=lambda v: v.lower() == 'true')
    sort_key = request.args.get('sort_key', default=key, type=str)
    
    # Apply filters based on query parameters
    screener.add_filter(psd.StockScreener.filter_stocks_by_parameter,key, min=min_val, max=max_val, top_percentile=top_percentile, top=top)
    
    filtered_data = screener.apply_filters(sortKey=sort_key)
    
    # Convert filtered data to JSON
    response = filtered_data.to_json(orient='records')
    return response

@app.route('/get_filtered-percentage_data', methods=['GET'])
def get_filtered_percentage_data():
    """ This route will add a percentage filter and return the filtered data after applying the filter"""
    
    # Retrieve query parameters
    key = request.args.get('key', default='profitMargins', type=str)
    min_val = request.args.get('min', default=-float('-inf'), type=float)
    max_val = request.args.get('max', default=float('inf'), type=float)
    top_percentile = request.args.get('top_percentile', default=100, type=float)
    top = request.args.get('top', default=True, type=lambda v: v.lower() == 'true')
    sort_key = request.args.get('sort_key', default='profitMargins', type=str)
    
    # Apply filters based on query parameters
    screener.add_filter(psd.StockScreener.filter_stocks_by_percentage,key, min=min_val, max=max_val, top_percentile=top_percentile, top=top)
    
    filtered_data = screener.apply_filters(sortKey=sort_key)
    
    # Convert filtered data to JSON
    response = filtered_data.to_json(orient='records')
    return response

@app.route('/get_filtered-absolute_data', methods=['GET'])
def get_cleared_data():
    """This route will clear all the filters and return the original data"""
    screener.clear_filters()
    return jsonify(screener.get_data())

@app.route('/get_active_keys', methods=['GET'])
def get_current_keys():
    """This route will return the current active keys that can be used for filtering"""
    return jsonify(screener.get_keys())

@app.route('/get_possible_keys', methods=['GET'])
def get_possible_keys():
    """This route will return the possible keys that can be used for filtering"""
    return jsonify(screener.get_possible_keys())

@app.route('/add_key', methods=['GET'])
def add_key():
    """This route will add a new key to the screener"""
    key = request.args.get('key', default='profitMargins', type=str)
    screener.add_key(key)
    return jsonify(screener.get_keys())

@app.route('/remove_key', methods=['GET'])
def remove_key():
    """This route will remove a key from the screener"""
    key = request.args.get('key', default='profitMargins', type=str)
    screener.remove_key(key)
    return jsonify(screener.get_keys())

if __name__ == '__main__':
    # Define SSL context for HTTPS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('path/to/cert.pem', 'path/to/key.pem')  # Specify your cert and key files
    
    # Run the app with SSL context
    app.run(debug=True, ssl_context=context)