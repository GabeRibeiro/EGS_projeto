import React, { useState } from "react";
import "chartjs-adapter-date-fns";
import { Chart } from "primereact/chart";
import { Card } from "primereact/card";
import { Button } from "primereact/button";
import Form from "./Form";

export default function Charts() {
  let basicOptions = {
    maintainAspectRatio: false,
    aspectRatio: 0.5,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      x: {
        type: "time",
        time: {
          unit: "hour",
        },
      },
    },
  };

  const [currencies, setCurrencies] = useState({ from: null, to: null });
  const [isConverting, setIsConverting] = useState(false);

  const updateCurrencies = (e) => {
    let id = e.target.id;
    setCurrencies({ ...currencies, [id]: e.value });
  };

  const handleConversion = (e) => {
    setIsConverting(true);
  };

  const footer = <Button label="Converter" onClick={handleConversion} />;

  const [data, setData] = useState({
    labels: [],
    datasets: [
      {
        label: "",
        data: [
          {
            x: new Date(Date.now() - 1000 * 60 * 60 * 2),
            y: 1,
          },
          {
            x: new Date(),
            y: 10,
          },
        ],
        fill: true,
        borderColor: "#4bc0c0",
        tension: 0.5,
      },
    ],
  });

  return (
    <Card footer={footer}>
      <div className="flex flex-row justify-content-evenly align-items-end ">
        <Form updateCurrencies={updateCurrencies} currencies={currencies} />
      </div>
      {/* show results in text */}
      {isConverting && (
        <Chart
          className="mt-5"
          type="line"
          data={data}
          options={basicOptions}
        ></Chart>
      )}
    </Card>
  );
}
