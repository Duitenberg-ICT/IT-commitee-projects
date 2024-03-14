import React from 'react';
import './App.css';

function App() {
    return (
        <div>
            <Header/>
            <hr className="separator" />
        </div>
    );
}

/*
The header needs to be changed to the new design. It should stretch all the way to include the rolling
stocks thing, where notable stock price changes appear. This component can be defined here, or it can be
moved to (a) separate file(s) and defined there.
 */
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
