import React from "react";
import "./StockHeader.css"

function StockHeader() {
    return (
        <>
            <div className="container d-flex flex-column align-items-center justify-content-center">
                <img src="/Apple-Logo.png" className="img-fluid stock-logo" alt="Stock logo"/>
                <h2>Apple</h2>

                <div className="d-flex">
                    <p className="mr-3 basic-stock-info">Tech</p>
                    <p className="mr-3 basic-stock-info">+3%</p>
                    <p className="mr-3 basic-stock-info">Quick Buy</p>
                    <p className="mr-3 basic-stock-info">202.123</p>
                </div>
            </div>
        </>
    );
}

export default StockHeader;