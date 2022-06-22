import React, { useContext, useEffect, useState } from "react";
import socketIOClient from "socket.io-client";
import jwt_decode from "jwt-decode";
import { useAuth } from "../Auth/AuthProvider";

const SocketContext = React.createContext();

export function useSocket() {
  return useContext(SocketContext);
}



export default function SocketProvider({ children }) {
  const [socket, setSocket] = useState(null);
  const user = useAuth();

  useEffect(() => {
    const id = jwt_decode(user.id)["_id"];
    setSocket(
      socketIOClient("/notification", {
        transports: ["websocket"],
        auth: {
          token: id,
        },
      })
    );

    socket.on("connect_error", (err) => {
      console.error(`Socket connection error: ${err}`);
      alert(`Socket connection error: ${err}`);
    });

    socket.on("newNotification", (newNotification) => {
      console.log(newNotification);
    });

    return () => socket.close();
  }, []);


  const data = { socket };

  return (
    <SocketContext.Provider value={data}>{children}</SocketContext.Provider>
  );
}
