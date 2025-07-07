// ~/Soap/frontend/src/ChangePassword.js

import React, { useState } from "react";
import axios from "axios";

function ChangePassword({ token }) {
  const [current, setCurrent] = useState("");
  const [newPw, setNewPw] = useState("");
  const [msg, setMsg] = useState("");

  const handleChange = async e => {
    e.preventDefault();
    if (!current || !newPw) {
      setMsg("Fill all fields.");
      return;
    }
    try {
      await axios.post("http://localhost:5003/users/change-password", {
        current, newPw
      }, { headers: { "x-api-token": token } });
      setMsg("Password changed.");
    } catch (err) {
      setMsg("Error: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="section-card">
      <h2>Change Password</h2>
      <form onSubmit={handleChange}>
        <input
          type="password"
          placeholder="Current password"
          value={current}
          onChange={e => setCurrent(e.target.value)}
        />
        <input
          type="password"
          placeholder="New password"
          value={newPw}
          onChange={e => setNewPw(e.target.value)}
        />
        <button type="submit">Change</button>
      </form>
      {msg && <div>{msg}</div>}
    </div>
  );
}
export default ChangePassword;
