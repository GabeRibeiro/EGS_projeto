import React from "react";
import { useAuth } from "./AuthProvider.js";
import { Navigate, useLocation } from "react-router-dom";

export default function RequireAuth({ children }) {
  let auth = useAuth();
  let location = useLocation();

  if (!auth.user) {
    return <Navigate to="/home" state={{ from: location }} replace />;
  }

  return children;
}
