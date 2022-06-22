import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/Auth/AuthProvider";
import { Button } from "primereact/button";

export default function Home() {
  const navigate = useNavigate();
  const auth = useAuth();

  return (
    <div className="card flex justify-content-center align-content-center">
      <Button
        onClick={(e) => {
          auth.signIn(() => navigate("../", { replace: true }));
        }}
      >
        Dashboard
      </Button>
    </div>
  );
}
