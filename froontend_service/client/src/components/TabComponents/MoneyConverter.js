import React from "react";
import { useState, useEffect } from "react";
import { Card } from "primereact/card";

import { InputNumber } from "primereact/inputnumber";
import { Button } from "primereact/button";

import Form from "./Form";

export default function MoneyConverter() {
  const [amount, setAmount] = useState(1.0);
  const [currencies, setCurrencies] = useState({ from: null, to: null });
  const [selectedCurrency, setSelectedCurrency] = useState("USD");
  const [isConverting, setIsConverting] = useState(false);
  const [result, setResult] = useState(0.0);

  // useEffect when currencies are updated to update result

  const updateCurrencies = (e) => {
    let id = e.target.id;

    setCurrencies({ ...currencies, [id]: e.value });
    if (id === "from") {
      setSelectedCurrency(e.value.code);
    }
  };

  const handleConversion = (e) => {
    setIsConverting(true);
  };

  const onAmountChange = (e) => setAmount(e.value);

  const footer = <Button label="Converter" onClick={handleConversion} />;

  return (
    <Card footer={footer}>
      <div className="flex flex-row justify-content-around align-items-end ">
        <div>
          <h4>Valor</h4>
          <div className="p-inputgroup">
            <InputNumber
              value={amount}
              onValueChange={onAmountChange}
              mode="currency"
              currency={selectedCurrency}
              locale="en-US"
              showButtons
            />
          </div>
        </div>
        <Form updateCurrencies={updateCurrencies} currencies={currencies} />
      </div>
      {/* show results in text */}
      {isConverting && (
        <span>
          <h3 style={{ margin: "2rem 0 0" }}>
            {amount.toPrecision(2)} {currencies.from.code} =
          </h3>
          <p style={{ fontSize: "2em", margin: "0" }}>
            {result.toPrecision(6)} {currencies.to.code}
          </p>
        </span>
      )}
    </Card>
  );
}
