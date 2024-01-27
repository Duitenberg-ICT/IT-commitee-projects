import React from "react";
import "./StocksViewButtons.css";

function StocksViewButtons() {
    return (
        <div className="container-fluid button-container">
            <button className="btn btn-primary reload-button">
                <i className="bi bi-arrow-repeat"></i>
            </button>
            <button className="btn btn-outline-primary">
                View
            </button>
            <button className="btn btn-secondary">
                Filters
            </button>
        </div>
    );
}

export default StocksViewButtons;