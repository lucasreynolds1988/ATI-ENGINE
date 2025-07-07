import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const apiToken = localStorage.getItem("apiToken");

  useEffect(() => {
    axios
      .get("/pipeline/history", { headers: { "X-API-Token": apiToken } })
      .then(r => setJobs(r.data.lines.map(line => line.trim())))
      .catch(() => setJobs(["Failed to load history"]));
  }, [apiToken]);

  return (
    <div>
      <h2>Pipeline Job History</h2>
      <ul>
        {jobs.map((job, i) => (
          <li key={i}>{job}</li>
        ))}
      </ul>
      {/* Next: add job table/status, live updates, action buttons */}
    </div>
  );
}
