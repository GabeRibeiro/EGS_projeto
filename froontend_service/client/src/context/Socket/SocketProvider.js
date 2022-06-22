import React, { useContext, useEffect, useCallback } from "react";
import io from "socket.io-client";
import { useAuth } from "../Auth/AuthProvider";

const URL = "http://notification-service-jfs4.k3s/";

const SocketContext = React.createContext();

export function useSocket() {
  return useContext(SocketContext);
}

export default function SocketProvider({ children }) {
  const auth = useAuth();

  const socket = io(URL, {
    transports: ["websocket"],
    auth: {
      token: auth.user.token,
    },
  });

  const err = useCallback((err) => {
    console.error(`Socket connection error: ${err}`);
    alert(`Socket connection error: ${err}`);
  }, []);

  const newNot = useCallback((newNotification) => {
    console.log(newNotification);
  }, []);

  useEffect(() => {
    socket.on("connect_error", err);

    socket.on("newNotification", newNot);

    return () => {
      socket.off("connect_error", err);
      socket.off("newNotification", newNot);
    };
  }, [socket, newNot, err]);

  return (
    <SocketContext.Provider value={socket}>{children}</SocketContext.Provider>
  );
}
