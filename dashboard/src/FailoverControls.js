import React, { useState } from "react";
import axios from "axios";

export default function FailoverControls({ jobId }) {
  const [message, setMessage] = useState("");
  const apiToken = localStorage.getItem("apiToken");

  function rerun() {
    axios
      .post("/pipeline/retry", { jobId }, { headers: { "X-API-Token": apiToken } })
      .then(() => setMessage("Rerun triggered"))
      .catch(() => setMessage("Failed"));
  }

  function cancel() {
    axios
      .post("/pipeline/cancel", { jobId }, { headers: { "X-API-Token": apiToken } })
      .then(() => setMessage("Cancel triggered"))
      .catch(() => setMessage("Failed"));
  }

  return (
    <div>
      <h3>Failover Controls</h3>
      <button onClick={rerun}>Rerun Job</button>
      <button onClick={cancel}>Cancel Job</button>
      <div>{message}</div>
    </div>
  );
}
