import React from 'react'
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/Auth/AuthProvider";

export default function Home() {
    const navigate = useNavigate();
    const auth = useAuth();
    
  return (
    <button onClick={(e) => {auth.signIn({}, navigate("../", { replace: true }));}}>Dashboard</button>
  )
}
