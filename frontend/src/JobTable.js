// ~/Soap/frontend/src/JobTable.js

import React, { useEffect, useState } from "react";
import { getJobs } from "./api";

function JobTable({ token, limit }) {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    if (!token) return;
    getJobs(token)
      .then(resp => {
        const jobArr = resp.data.jobs || [];
        setJobs(limit ? jobArr.slice(0, limit) : jobArr);
      })
      .catch(() => setJobs([]));
  }, [token, limit]);

  if (!jobs.length) return <div>No jobs to display.</div>;

  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Type</th>
          <th>Status</th>
          <th>Timestamp</th>
        </tr>
      </thead>
      <tbody>
        {jobs.map(job => (
          <tr key={job.id}>
            <td>{job.id}</td>
            <td>{job.type}</td>
            <td>{job.status}</td>
            <td>{job.timestamp}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default JobTable;
