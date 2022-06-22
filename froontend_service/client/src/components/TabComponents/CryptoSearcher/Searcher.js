import React, { useState, useEffect } from "react";
import { InputText } from "primereact/inputtext";
import { useAuth } from "../../../context/Auth/AuthProvider.js";
import { Button } from "primereact/button";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";

const URL = "http://information-service.k3s/URL";

export default function Searcher() {
  const [tag, setTag] = useState("");
  const [urls, setUrls] = useState([]);
  const [search, setSearch] = useState(false);
  const [selectedURL, setSelectedURL] = useState(null);

  const auth = useAuth();

  // call all
  useEffect(() => {
    const url = URL + "/ALL" + "?user_id:" + auth.getId();
    const headers = {
      Authorization: auth.user.token,
    };

    const options = {
      method: "GET",
      headers: headers,
    };

    fetch(url, options)
      .then((res) => res.json())
      .then((result) => {
        console.log(result);
        setUrls(result);
      });
  }, []);

  // call filter
  useEffect(() => {
    if (search === false) return
    const url =
      URL + "/Tags" + "?metric_id=" + tag + "?user_id:" + auth.user.id;
    const headers = {
      Authorization: auth.user.token,
    };

    const options = {
      method: "GET",
      headers: headers,
    };

    fetch(url, options)
      .then((res) => res.json())
      .then((result) => {
        console.log(result);
        setUrls(result);
      });
  }, [search]);

  return (
    <>
      {/* // filter */}

      <div>
        <h4>Tag</h4>
        <span className="p-input-icon-left">
          <InputText
            value={tag}
            onChange={(e) => setTag(e.target.value)}
            placeholder="Search Tag"
          />
        </span>
        <Button
          onClick={(e) => {
            setSearch(true);
          }}
        >
          <i className="pi pi-search" />
        </Button>
      </div>

      {/* // all urls */}
      <h1> URLS </h1>
      <div className="card"> 
        <DataTable value={urls} selectionMode="single" 
          selection={selectedURL} onSelectionChange={e => setSelectedURL(e.value)}
           dataKey="id" responsiveLayout="scroll">
          <Column field="url" header="URL"></Column>
          <Column field="tag" header="Tag"></Column>
          <Column field="value" header="Value"></Column>
          <Column field="period" header="Period"></Column>
        </DataTable>
      </div>
    </>
  );
}
