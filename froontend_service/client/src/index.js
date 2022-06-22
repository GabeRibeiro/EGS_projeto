import React, { StrictMode } from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "primereact/resources/primereact.min.css";
import "primereact/resources/themes/lara-dark-blue/theme.css";
import "primeicons/primeicons.css";
import "primeflex/primeflex.css";
import Main from "./layouts/Main";
import LoginForm from "./components/Profile/LoginForm";
import RegisterForm from "./components/Profile/RegisterForm";
import Auth from "./layouts/Auth";
import RequireAuth from "./context/Auth/RequireAuth";
import AuthProvider from "./context/Auth/AuthProvider";
import SocketProvider from "./context/Socket/SocketProvider";
import { CookiesProvider } from "react-cookie";
import Notifications from "./components/TabComponents/Notifications";
import Tab from "./components/TabComponents/Tab";
import Home from "./components/Home"

ReactDOM.render(
  <StrictMode>
    <Router>
    <CookiesProvider>
      <AuthProvider>
        <Routes>
        <Route path="/home" element={<Home />}/>
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
      </AuthProvider>
      </CookiesProvider>
    </Router>
  </StrictMode>,
  document.getElementById("root")
);
