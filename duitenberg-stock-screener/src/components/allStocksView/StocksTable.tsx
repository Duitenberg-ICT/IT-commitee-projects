import React from "react";
import "./StocksTable.css"

function StocksTable() {
    const stocks = {
        "AAPL" : {
            "price": 192.42,
            "change%": -0.9,
            "signal": "buy",
            "volume": "44.59M",
            "v*p": "8.581B",
            "marketCap": "2.975T",
            "p/e": 31.39,
            "eps": 6.16,
            "sector": "Tech"
        },
        "MSFT": {
            "price": 192.42,
            "change%": -0.9,
            "signal": "buy",
            "volume": "44.59M",
            "v*p": "8.581B",
            "marketCap": "2.975T",
            "p/e": 31.39,
            "eps": 6.16,
            "sector": "Tech"
        },
        "GOOG": {
            "price": 192.42,
            "change%": -0.9,
            "signal": "buy",
            "volume": "44.59M",
            "v*p": "8.581B",
            "marketCap": "2.975T",
            "p/e": 31.39,
            "eps": 6.16,
            "sector": "Tech"
        },
        "AMZN": {
            "price": 192.42,
            "change%": -0.9,
            "signal": "buy",
            "volume": "44.59M",
            "v*p": "8.581B",
            "marketCap": "2.975T",
            "p/e": 31.39,
            "eps": 6.16,
            "sector": "Tech"
        },
        "NVDA": {
            "price": 192.42,
            "change%": -0.9,
            "signal": "buy",
            "volume": "44.59M",
            "v*p": "8.581B",
            "marketCap": "2.975T",
            "p/e": 31.39,
            "eps": 6.16,
            "sector": "Tech"
        },
        "META": {
            "price": 192.42,
            "change%": -0.9,
            "signal": "buy",
            "volume": "44.59M",
            "v*p": "8.581B",
            "marketCap": "2.975T",
            "p/e": 31.39,
            "eps": 6.16,
            "sector": "Tech"
        }
    };

    return (
        <table className="table table-light table-hover stocks-table">
            <thead>
            <tr>
                <th scope="col">Symbol</th>
                <th scope="col">Price</th>
                <th scope="col">Change %</th>
                <th scope="col">Signal</th>
                <th scope="col">Volume</th>
                <th scope="col">V*P</th>
                <th scope="col">Market Cap</th>
                <th scope="col">P/E</th>
                <th scope="col">EPS</th>
                <th scope="col">Sector</th>
            </tr>
            </thead>
            <tbody className="table-group-divider">
            {Object.entries(stocks).map(([symbol, stock]) => (
                <tr key={symbol}>
                    <td>{symbol}</td>
                    <td>{stock.price}</td>
                    <td>{stock['change%']}</td>
                    <td>{stock.signal}</td>
                    <td>{stock.volume}</td>
                    <td>{stock['v*p']}</td>
                    <td>{stock.marketCap}</td>
                    <td>{stock['p/e']}</td>
                    <td>{stock.eps}</td>
                    <td>{stock.sector}</td>
                </tr>
            ))}
            </tbody>
        </table>
    );
}

export default StocksTable;