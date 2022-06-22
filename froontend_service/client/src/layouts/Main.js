import React, { useState } from "react";
import Navbar from "../components/Navbar/Navbar.js";
import { Outlet } from "react-router-dom";

export default function Main() {

  return (
    <>
      <Navbar />

      <Outlet />
    </>
  );
}
