import React from "react";
import Navbar from "../components/Navbar/Navbar.js";
import Tab from "../components/TabComponents/Tab.js";
import { Outlet } from "react-router-dom";

// import routes from './routes.js'

export default function Main() {
  return (
    <>
      <Navbar />

      <Outlet />
    </>
  );
}
