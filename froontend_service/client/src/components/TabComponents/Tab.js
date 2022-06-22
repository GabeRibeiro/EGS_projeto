import React from "react";
import { TabView, TabPanel } from "primereact/tabview";
import MoneyConverter from "./MoneyConverter";
import Charts from "./Charts";
import Searcher from "./CryptoSearcher/Searcher";

export default function Tab() {
  return (
    <Card>
      <Searcher></Searcher>
    </Card>
  );
}
