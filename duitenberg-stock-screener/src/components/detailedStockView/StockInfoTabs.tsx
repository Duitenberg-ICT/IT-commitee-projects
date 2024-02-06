import React, { useState } from "react";
import "./StockInfoTabs.css"; // Your custom CSS for additional styling if needed

function StockInfoTabs() {
    const [activeTab, setActiveTab] = useState<number>(1);

    const handleTabClick = (tabNumber: number) => {
        setActiveTab(tabNumber);
    };

    return (
        <div className="container">
            <ul className="nav nav-tabs">
                <li className="nav-item">
                    <a
                        className={`nav-link ${activeTab === 1 ? "active" : ""}`}
                        onClick={() => handleTabClick(1)}
                        href="#"
                    >
                        Overview
                    </a>
                </li>
                <li className="nav-item">
                    <a
                        className={`nav-link ${activeTab === 2 ? "active" : ""}`}
                        onClick={() => handleTabClick(2)}
                        href="#"
                    >
                        Financials
                    </a>
                </li>
                <li className="nav-item">
                    <a
                        className={`nav-link ${activeTab === 3 ? "active" : ""}`}
                        onClick={() => handleTabClick(3)}
                        href="#"
                    >
                        History
                    </a>
                </li>
                <li className="nav-item">
                    <a
                        className={`nav-link ${activeTab === 4 ? "active" : ""}`}
                        onClick={() => handleTabClick(4)}
                        href="#"
                    >
                        News
                    </a>
                </li>
            </ul>

            {/* Content for each tab */}
            <div className="tab-content mt-3">
                <div className={`tab-pane fade ${activeTab === 1 ? "show active" : ""}`}>
                    <div className="row">
                        <div className="col-md-6">
                            <div className="info-card">
                                <h2 className="info-title">Market Capitalization</h2>
                                <p className="info-value">3.01T USD</p>
                            </div>
                        </div>
                        <div className="col-md-6">
                            <div className="info-card">
                                <h2 className="info-title">Price to Earnings Ratio (TTM)</h2>
                                <p className="info-value">37.19</p>
                            </div>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-6">
                            <div className="info-card">
                                <h2 className="info-title">Net Income</h2>
                                <p className="info-value">72.36B USD</p>
                            </div>
                        </div>
                        <div className="col-md-6">
                            <div className="info-card">
                                <h2 className="info-title">Shares Float</h2>
                                <p className="info-value">7.32B</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div className={`tab-pane fade ${activeTab === 2 ? "show active" : ""}`}>
                    <h2>Tab 2 Content</h2>
                    <p>This is the content for Tab 2.</p>
                </div>
                <div className={`tab-pane fade ${activeTab === 3 ? "show active" : ""}`}>
                    <h2>Tab 3 Content</h2>
                    <p>This is the content for Tab 3.</p>
                </div>
                <div className={`tab-pane fade ${activeTab === 4 ? "show active" : ""}`}>
                    <h2>Tab 4 Content</h2>
                    <p>This is the content for Tab 4.</p>
                </div>
            </div>
        </div>
    );
}

export default StockInfoTabs;
