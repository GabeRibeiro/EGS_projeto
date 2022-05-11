// import React, { useState, useEffect } from "react";
import socketIOClient from "socket.io-client";
import jwt_decode from "jwt-decode";

const endpoint = "http://host.docker.internal:3050/";
let socket = null;

export default function createSocket(uid, handler) {
  const id = jwt_decode(uid)["_id"];
  console.log(id);
  socket = socketIOClient(endpoint, {
    transports: ["websocket"],
    auth: {
      token: "1", //need to get the token from the backend
    },
  });

  socket.on("connect_error", (err) => {
    console.error(`Socket connection error: ${err}`);
  });

  socket.on("newNotification", handler);

  return () => socket.close();
}

export function getSocket() {
  return socket;
}
