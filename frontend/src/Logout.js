// ~/Soap/frontend/src/Logout.js

import React from "react";
import { useNavigate } from "react-router-dom";

function Logout({ setToken }) {
  const navigate = useNavigate();
  React.useEffect(() => {
    setToken("");
    localStorage.removeItem("api_token");
    navigate("/login");
  }, [setToken, navigate]);
  return null;
}

export default Logout;
