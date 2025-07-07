import React, { useState } from "react";
import axios from "axios";

export default function ApproveDenyPanel({ jobId }) {
  const apiToken = localStorage.getItem("apiToken");
  const [message, setMessage] = useState("");
  const [correction, setCorrection] = useState("");

  function approve() {
    axios
      .post("/pipeline/approve", { jobId }, { headers: { "X-API-Token": apiToken } })
      .then(() => setMessage("Approved"))
      .catch(() => setMessage("Failed"));
  }

  function deny() {
    axios
      .post("/pipeline/deny", { jobId, correction }, { headers: { "X-API-Token": apiToken } })
      .then(() => setMessage("Denied"))
      .catch(() => setMessage("Failed"));
  }

  return (
    <div>
      <button onClick={approve}>Approve</button>
      <button onClick={deny}>Deny</button>
      <input
        placeholder="Correction (if denying)"
        value={correction}
        onChange={e => setCorrection(e.target.value)}
      />
      <div>{message}</div>
    </div>
  );
}
