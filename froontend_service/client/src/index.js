import React, { StrictMode } from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import "primereact/resources/primereact.min.css";
import "primereact/resources/themes/lara-dark-blue/theme.css";
import "primeicons/primeicons.css";
import "primeflex/primeflex.css";

import Main from "./layouts/Main";

import SocketProvider from "./context/Socket/SocketProvider";
import RequireAuth from "./context/Auth/RequireAuth";
import MainProvider from "./context/MainProvider";

import Tab from "./components/TabComponents/Tab";
import Home from "./components/Home";
import Notifications from "./components/TabComponents/Notifications";

ReactDOM.render(
  <StrictMode>
    <Router>
      <MainProvider>
        <Routes>
          <Route path="home" element={<Home />} />
          <Route
            element={
              <RequireAuth>
                <SocketProvider>
                  <Main />
                </SocketProvider>
              </RequireAuth>
            }
          >
            <Route path="/" element={<Tab />} />
            <Route path="notifications" element={<Notifications />} />
          </Route>
        </Routes>
      </MainProvider>
    </Router>
  </StrictMode>,
  document.getElementById("root")
);
