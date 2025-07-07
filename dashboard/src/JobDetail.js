import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

export default function JobDetail() {
  const { jobId } = useParams();
  const apiToken = localStorage.getItem("apiToken");
  const [status, setStatus] = useState({});
  const [log, setLog] = useState("");

  useEffect(() => {
    axios
      .get(`/pipeline/status/${jobId}`, { headers: { "X-API-Token": apiToken } })
      .then(r => setStatus(r.data));
    axios
      .get("/log", { headers: { "X-API-Token": apiToken }, responseType: "text" })
      .then(r => setLog(r.data));
  }, [jobId, apiToken]);

  return (
    <div>
      <h2>Job: {jobId}</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
      <h3>Log</h3>
      <pre style={{ maxHeight: 300, overflow: "auto" }}>{log}</pre>
      {/* Next: Approve/deny controls, live updates, etc */}
    </div>
  );
}
