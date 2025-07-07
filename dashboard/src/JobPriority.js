import React, { useState } from "react";
import axios from "axios";

export default function JobPriority() {
  const [jobId, setJobId] = useState("");
  const [priority, setPriority] = useState("normal");
  const [message, setMessage] = useState("");
  const apiToken = localStorage.getItem("apiToken");

  function setJobPriority(e) {
    e.preventDefault();
    axios
      .post(
        "/pipeline/priority",
        { jobId, priority },
        { headers: { "X-API-Token": apiToken } }
      )
      .then(() => setMessage("Priority set"))
      .catch(() => setMessage("Failed"));
  }

  return (
    <form onSubmit={setJobPriority}>
      <h3>Set Job Priority</h3>
      <input
        value={jobId}
        onChange={e => setJobId(e.target.value)}
        placeholder="Job ID"
        required
      />
      <select value={priority} onChange={e => setPriority(e.target.value)}>
        <option value="low">Low</option>
        <option value="normal">Normal</option>
        <option value="high">High</option>
      </select>
      <button type="submit">Set Priority</button>
      <div>{message}</div>
    </form>
  );
}
