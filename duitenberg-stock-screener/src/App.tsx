import React from 'react';
import './App.css';

import DetailedStock from "./components/detailedStockView/DetailedStock";
import AllStocks from "./components/allStocksView/AllStocks";

function App() {
    return (
        <div>
            <Header/>
            <hr className="separator" />

            <AllStocks />
        </div>
    );
}

function Header() {
    return (
        <div className="container-fluid">
            <div className="row">
                <div className="col-md-6 d-flex align-items-center justify-content-start">
                    <h1 className="App-title">Stock Screener</h1>
                </div>
                <div className="col-md-6 d-flex align-items-center justify-content-end">
                    <img src="/duitenberg-logo.png" className="App-logo" alt="Logo" />
                </div>
            </div>
        </div>
    );
}

export default App;
