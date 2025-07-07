import React, { useEffect, useState } from "react";
import axios from "axios";
import ApproveDenyPanel from "./ApproveDenyPanel";

export default function AdvancedJobView({ jobId }) {
  const [status, setStatus] = useState({});
  const [details, setDetails] = useState("");
  const apiToken = localStorage.getItem("apiToken");

  useEffect(() => {
    axios
      .get(`/pipeline/status/${jobId}`, { headers: { "X-API-Token": apiToken } })
      .then(r => setStatus(r.data));
    axios
      .get(`/jobfile/${jobId}`, { headers: { "X-API-Token": apiToken } })
      .then(r => setDetails(r.data.contents));
  }, [jobId, apiToken]);

  return (
    <div>
      <h2>Advanced Job: {jobId}</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
      <h3>Job Details</h3>
      <pre style={{ maxHeight: 300, overflow: "auto" }}>{details}</pre>
      <ApproveDenyPanel jobId={jobId} />
    </div>
  );
}

