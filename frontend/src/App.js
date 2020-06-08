import React from "react";
import { useSelector, useDispatch } from "react-redux";

// pages
import Login from "./pages/Login";

function App() {
  const isAuthenticated = useSelector((state) => state.isAuthenticated);

  if (isAuthenticated === false) {
    return <Login />;
  }
}

export default App;
