import React, { useContext, useState } from "react";
import { useCookies } from "react-cookie";

const AuthContext = React.createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export default function AuthProvider({ children }) {
  let [user, setUser] = useState(null);
  const [cookies, setCookie] = useCookies();

  // 

  async function signIn(user, cb) {
    // call Athentication API to sign in
    setUser({ id: cookies.jwt_token });
    cb()
  }

  async function signOut(cb) {
    // call Athentication API to sign out
    setUser(null);
    cb();
  }

  // async function register(user, cb) {
  //   // call Authentication API to register

  //   try {
  //     const response = await fetch("/auth/register", {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify(user),
  //     });

  //     if (response.ok) {
  //       const data = await response.json();

  //       console.log(data);

  //       cb(false);
  //     } else {
  //       const message = await response.text();
  //       if (message == null || message.includes("html"))
  //         message = "Email or Password is invalid";
  //       cb(true, message);
  //     }
  //   } catch (error) {
  //     console.error(error);
  //     cb(true);
  //   }
  // }

  let value = { user, signOut, signIn };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
