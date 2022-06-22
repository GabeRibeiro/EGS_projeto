import React, { useContext, useState } from "react";
import { useCookies } from "react-cookie";
import jwt_decode from "jwt-decode";

const AuthContext = React.createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export default function AuthProvider({ children }) {
  let [user, setUser] = useState(null);
  const [cookies, setCookie] = useCookies(["jwt_token"]);
  const token = cookies["jwt_token"];
  console.log(cookies);
  function signIn(cb) {
    // call Athentication API to sign in
    setUser({ token: token });
    cb();
  }

  function getId() {
    const id = jwt_decode(user.token)["_id"];
    return id;
  }

  function signOut(cb) {
    // call Athentication API to sign out
    setUser(null);
    cb();
  }

  let value = { user, getId, signOut, signIn };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
