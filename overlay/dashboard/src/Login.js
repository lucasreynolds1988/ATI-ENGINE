import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [token, setToken] = useState("");
  const navigate = useNavigate();

  function handleLogin(e) {
    e.preventDefault();
    localStorage.setItem("apiToken", token);
    navigate("/dashboard");
  }

  return (
    <form onSubmit={handleLogin}>
      <h2>ATI Pipeline Login</h2>
      <input
        type="password"
        placeholder="API Token"
        value={token}
        onChange={e => setToken(e.target.value)}
        autoFocus
        required
      />
      <button type="submit">Login</button>
    </form>
  );
}
