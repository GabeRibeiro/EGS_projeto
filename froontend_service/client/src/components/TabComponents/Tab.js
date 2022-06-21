import React from "react";
import { TabView, TabPanel } from "primereact/tabview";
import MoneyConverter from "./MoneyConverter";
import Charts from "./Charts";

export default function Tab() {
  return (
    <div className="mt-5 flex justify-content-center align-content-center ">
      <TabView className=" surface-card border-round p-4 w-8">
        <TabPanel header="Charts" leftIcon="pi pi-fw pi-chart-line mr-2">
          {/* Add form */}
          {/* <CryptosForm /> */}
          <Charts />
        </TabPanel>
        <TabPanel header=" Converter" leftIcon="pi pi-fw pi-dollar mr-2">
          {/* Search cryptos */}
          {/* <MainSearcher /> */}
          <MoneyConverter />
        </TabPanel>
      </TabView>
    </div>
  );
}
