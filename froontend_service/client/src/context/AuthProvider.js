import React, { useContext, useState } from "react";

const AuthContext = React.createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export default function AuthProvider({ children }) {
  let [user, setUser] = useState(null);

  async function signIn(user, cb) {
    // call Athentication API to sign in
    try {
      const response = await fetch(
        "http://host.docker.internal:3000/api/user/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(user),
        }
      );

      const jwt = await response.text();

      console.log(jwt);

      if (response.ok) {
        setUser({ id: jwt });
        cb(false);
      } else {
        cb(true, "Invalid email or password");
      }
    } catch (error) {
      console.error(error);
      cb(true);
    }
  }

  async function signOut(cb) {
    // call Athentication API to sign out
    setUser(null);
    cb();
  }

  async function register(user, cb) {
    // call Authentication API to register

    try {
      const response = await fetch(
        "http://host.docker.internal:3000/api/user/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(user),
        }
      );

      if (response.ok) {
        const data = await response.json();

        console.log(data);

        setUser({ id: data.user });
        cb(false);
      } else {
        const message = await response.text();
        if (message.includes("html")) message = "Email or Password is invalid";
        cb(true, message);
      }
    } catch (error) {
      console.error(error);
      cb(true);
    }
  }

  let value = { user, signIn, signOut, register };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
