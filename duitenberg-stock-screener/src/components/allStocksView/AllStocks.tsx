import React from "react";
import StocksViewButtons from "./StocksViewButtons";
import StocksTable from "./StocksTable";

function AllStocks() {
    return (
        <>
            <StocksViewButtons />
            <hr className="separator"/>
            <StocksTable />
        </>
    );
}

export default AllStocks;