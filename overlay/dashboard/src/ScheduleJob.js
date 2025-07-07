import React, { useState } from "react";
import axios from "axios";

export default function ScheduleJob() {
  const [jobId, setJobId] = useState("");
  const [when, setWhen] = useState("");
  const [message, setMessage] = useState("");
  const apiToken = localStorage.getItem("apiToken");

  function schedule(e) {
    e.preventDefault();
    axios
      .post(
        "/pipeline/schedule",
        { jobId, when },
        { headers: { "X-API-Token": apiToken } }
      )
      .then(() => setMessage("Scheduled"))
      .catch(() => setMessage("Failed"));
  }

  return (
    <form onSubmit={schedule}>
      <h3>Schedule Job</h3>
      <input
        value={jobId}
        onChange={e => setJobId(e.target.value)}
        placeholder="Job ID"
        required
      />
      <input
        value={when}
        onChange={e => setWhen(e.target.value)}
        placeholder="When (YYYY-MM-DD HH:MM)"
        required
      />
      <button type="submit">Schedule</button>
      <div>{message}</div>
    </form>
  );
}
