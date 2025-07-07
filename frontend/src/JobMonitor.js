// ~/Soap/frontend/src/JobMonitor.js

import React, { useEffect, useState } from "react";
import axios from "axios";

export default function JobMonitor() {
  const [jobs, setJobs] = useState([]);
  useEffect(() => {
    axios.get("/admin/jobs").then(resp => setJobs(resp.data));
  }, []);
  return (
    <div>
      <h2>System Jobs</h2>
      <table>
        <thead>
          <tr>
            <th>Type</th><th>Status</th><th>Time</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map(j => (
            <tr key={j.job_id}>
              <td>{j.job_type}</td>
              <td>{j.status}</td>
              <td>{new Date(j.timestamp * 1000).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
