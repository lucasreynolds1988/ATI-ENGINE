// ~/Soap/frontend/src/Login.js

import React, { useState } from "react";

function Login({ onLogin }) {
  const [tokenInput, setTokenInput] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = e => {
    e.preventDefault();
    if (!tokenInput.trim()) {
      setError("API token required.");
      return;
    }
    setError("");
    onLogin(tokenInput.trim());
  };

  return (
    <div className="section-card">
      <h2>System Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          placeholder="Enter API Token"
          value={tokenInput}
          onChange={e => setTokenInput(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
      {error && <div style={{ color: "#d03232" }}>{error}</div>}
    </div>
  );
}

export default Login;
