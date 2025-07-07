// ~/Soap/frontend/src/ReportIssue.js

import React, { useState } from "react";
import axios from "axios";

function ReportIssue({ token }) {
  const [msg, setMsg] = useState("");
  const [status, setStatus] = useState("");

  const handleSubmit = async e => {
    e.preventDefault();
    if (!msg.trim()) return;
    try {
      await axios.post(
        "http://localhost:5003/issues/report",
        { message: msg },
        { headers: { "x-api-token": token } }
      );
      setStatus("Issue reported. Thank you!");
      setMsg("");
    } catch (err) {
      setStatus("Submission failed: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="section-card">
      <h2>Report an Issue</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          rows={4}
          style={{ width: "100%", padding: 10, borderRadius: 8, border: "1px solid #c2d3dc" }}
          placeholder="Describe the issue..."
          value={msg}
          onChange={e => setMsg(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
      {status && <div>{status}</div>}
    </div>
  );
}
export default ReportIssue;
