import React from "react";
import AuthProvider from "./Auth/AuthProvider";
import { CookiesProvider } from "react-cookie";

export default function MainProvider({ children }) {
  return (
    <CookiesProvider>
      <AuthProvider>{children}</AuthProvider>
    </CookiesProvider>
  );
}
