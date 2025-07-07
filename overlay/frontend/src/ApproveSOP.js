// ~/Soap/frontend/src/ApproveSOP.js

import React, { useState } from "react";
import axios from "axios";

function ApproveSOP({ token }) {
  const [fileId, setFileId] = useState("");
  const [msg, setMsg] = useState("");
  const [approved, setApproved] = useState(null);

  const handleApprove = async e => {
    e.preventDefault();
    if (!fileId) return setMsg("Enter SOP filename.");
    try {
      const resp = await axios.post(
        `http://localhost:5003/sops/approve/${fileId}`,
        {},
        { headers: { "x-api-token": token } }
      );
      setApproved(true);
      setMsg(resp.data.status || "SOP approved.");
    } catch (err) {
      setApproved(false);
      setMsg("Error: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="section-card">
      <h2>Approve SOP</h2>
      <form onSubmit={handleApprove}>
        <input
          type="text"
          placeholder="Enter SOP filename"
          value={fileId}
          onChange={e => setFileId(e.target.value)}
        />
        <button type="submit">Approve</button>
      </form>
      {msg && (
        <div style={{ color: approved ? "#179b1f" : "#c21825" }}>{msg}</div>
      )}
    </div>
  );
}
export default ApproveSOP;
