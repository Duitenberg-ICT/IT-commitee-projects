import React from "react";
import StockHeader from "./StockHeader";

import "./DetailedStock.css";

function DetailedStock() {
    return (
        <>
            <div className="container-lg">
                <StockHeader/>
                <hr/>
            </div>
            <div className="container-fluid d-flex flex-column align-items-center justify-content-center">
                <img src="/stock-graph.png" className="img-fluid stock-graph" alt="Stock graph"/>
            </div>
        </>
    );
}

export default DetailedStock;