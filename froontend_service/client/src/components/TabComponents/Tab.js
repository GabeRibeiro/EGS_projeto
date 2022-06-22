import React from "react";
import { TabView, TabPanel } from "primereact/tabview";
import MoneyConverter from "./MoneyConverter";
import Charts from "./Charts";
import Searcher from "./CryptoSearcher/Searcher";

export default function Tab() {
  return (
    <div className="mt-5 flex justify-content-center align-content-center ">
      <Searcher></Searcher>
    </div>
  );
}
