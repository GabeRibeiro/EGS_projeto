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
import RequireAuth from "./context/RequireAuth";
import AuthProvider from "./context/AuthProvider";
import Notifications from "./components/TabComponents/Notifications";
import Tab from "./components/TabComponents/Tab";

ReactDOM.render(
  <StrictMode>
    <Router>
      <AuthProvider>
        <Routes>
          <Route element={<Auth />}>
            <Route path="/auth/login" element={<LoginForm />} />
            <Route path="/auth/register" element={<RegisterForm />} />
          </Route>

          <Route
            element={
              <RequireAuth>
                <Main />
              </RequireAuth>
            }
          >
            <Route path="/" element={<Tab />} />
            <Route path="notifications" element={<Notifications />} />
          </Route>
        </Routes>
      </AuthProvider>
    </Router>
  </StrictMode>,
  document.getElementById("root")
);
