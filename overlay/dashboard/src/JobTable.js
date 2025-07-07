import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

export default function JobTable() {
  const [jobs, setJobs] = useState([]);
  const apiToken = localStorage.getItem("apiToken");

  useEffect(() => {
    axios
      .get("/pipeline/jobs", { headers: { "X-API-Token": apiToken } })
      .then(r => setJobs(r.data.jobs || []));
  }, [apiToken]);

  return (
    <table>
      <thead>
        <tr>
          <th>Job ID</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody>
        {jobs.map(job => (
          <tr key={job}>
            <td>{job}</td>
            <td>
              <Link to={`/job/${job}`}>View</Link>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
