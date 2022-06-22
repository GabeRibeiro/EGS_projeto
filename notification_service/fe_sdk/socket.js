"use strict";
/**
 * import using:
 * <script type="module" src="socket.js"></script>
 */

const apiHost = "http://notification-service-jfs4.k3s";

let socket = null;

export const registerCallback = (event, callback) => {
  socket.on(event, callback);
};

const notificationHandle = (notification) => {
  const narea = document.getElementById("notification_area");
  const p_elem = document.createElement("p");
  // console.log(notification)
  p_elem.appendChild(document.createTextNode(notification["txt"]));
  narea.insertBefore(p_elem, narea.firstChild);
};

export const createSocket = (uid) => {
  if (socket) {
    socket.close();
  }
  socket = io(apiHost + "/", {
    transports: ["websocket"],
    auth: {
      token: uid,
    },
  });

  registerCallback("connect_error", (err) => {
    console.log(`socket.io connect_error due to ${err.message}`);
  });

  registerCallback("newNotification", notificationHandle);
};

createSocket("");

const uelem = document.getElementById("user_btn");
uelem.onclick = (ev) => {
  ev.preventDefault();
  createSocket(document.getElementById("uid").value);
};

const felem = document.getElementById("submit_bttn");
felem.onclick = (ev) => {
  ev.preventDefault();

  const data = {
    text: document.getElementById("text").value,
    uid: document.getElementById("uid_input").value,
    options: {
      email: document.getElementById("email_input").value,
    },
  };

  const myHeaders = new Headers();
  myHeaders.append("Authorization", data.uid);
  myHeaders.append("Content-Type", "application/json");

  fetch(apiHost + "/notification", {
    headers: myHeaders,
    method: "POST",
    body: JSON.stringify(data),
  }).catch(console.error);
};

document.getElementById("submit_pag").onclick = (ev) => {
  ev.preventDefault();

  const myHeaders = new Headers();
  myHeaders.append("Authorization", document.getElementById("uid").value);

  var url = new URL(apiHost + `/notifications`);

  var params = {
    nrPage: document.getElementById("pageNr").value,
    resultsPerPage: document.getElementById("resultperpage").value,
  };

  url.search = new URLSearchParams(params).toString();

  // cant use body with get
  fetch(url, {
    headers: myHeaders,
  })
    .then((res) => res.json())
    .then(console.log)
    .catch(console.error);
};
