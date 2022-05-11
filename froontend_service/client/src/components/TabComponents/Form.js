import React from "react";
import { Dropdown } from "primereact/dropdown";

export default function Form({ updateCurrencies, currencies }) {
  const currencies_list = [
    { name: "United States", code: "USD" },
    { name: "Europe", code: "EUR" },
  ];

  return (
    <>
      {/* selector */}
      <div>
        <h4>From</h4>
        <div className="p-inputgroup w-15rem">
          <Dropdown
            id="from"
            value={currencies.from}
            options={currencies_list}
            onChange={updateCurrencies}
            optionLabel="name"
            placeholder="Select a Currency"
          />
        </div>
      </div>
      {/* icon */}
      <i
        className="pi pi-fw pi-arrows-h"
        style={{ fontSize: "2em", marginBottom: "0.5rem" }}
      />
      {/* selector */}
      <div>
        <h4>To</h4>
        <div className="p-inputgroup w-15rem">
          <Dropdown
            id="to"
            value={currencies.to}
            options={currencies_list}
            onChange={updateCurrencies}
            optionLabel="name"
            placeholder="Select a Currency"
          />
        </div>
      </div>
    </>
  );
}
