import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from "react";

function App() {
    return (
        <div className="App">
            <Header/>
            <hr className="separator" />
        </div>
    );
}

const Header = () => {
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
};

export default App;
