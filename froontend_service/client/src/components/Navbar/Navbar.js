import React, { useEffect, useState } from "react";
import { Menubar } from "primereact/menubar";
import { Button } from "primereact/button";
import { Link } from "react-router-dom";
import { useAuth } from "../../context/Auth/AuthProvider";
import { useSocket } from "../../context/Socket/SocketProvider";
import { useNavigate } from "react-router-dom";
import "primeicons/primeicons.css";

export default function Navbar() {
  const navigate = useNavigate();
  const auth = useAuth();
  const { socket } = useSocket();

  const [notifications, setNotifications] = useState(0);

  const handleNotifications = (notification) =>
    setNotifications(notifications + 1);

  useEffect(() => {
    socket.on("newNotification", handleNotifications);
    return () => {
      socket.off("newNotification", handleNotifications);
    };
  }, []);

  const items = [];

  const start = (
    <Link to="/">
      <img
        alt="logo"
        src="showcase/images/logo.png"
        onError={(e) =>
          (e.target.src =
            "https://www.primefaces.org/wp-content/uploads/2020/05/placeholder.png")
        }
        height="40"
        className="mr-2"
      ></img>
    </Link>
  );
  const end = (
    <>
      <Link to="/notifications">
        <i
          className="pi pi-fw pi-bell"
          style={{
            fontSize: "2em",
            marginBottom: "0.5rem",
            marginRight: "0.5rem",
            color: "yellow",
          }}
        ></i>
        <span style={{ fontSize: "0.5em" }}> {notifications} </span>
      </Link>
      <Button
        type="button"
        className="p-button"
        label="Sign Out"
        onClick={() => auth.signOut(() => navigate("/"))}
      />
    </>
  );

  return (
    <div className="card">
      <Menubar model={items} start={start} end={end} />
    </div>
  );
}
