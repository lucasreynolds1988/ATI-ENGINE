import React, { useEffect, useState } from "react";
import axios from "axios";

export default function JobMetricsChart() {
  const [metrics, setMetrics] = useState({});
  const apiToken = localStorage.getItem("apiToken");

  useEffect(() => {
    axios
      .get("/metrics", { headers: { "X-API-Token": apiToken } })
      .then(r => setMetrics(r.data));
  }, [apiToken]);

  // Simple chart: jobs run vs. failures (real chart needs chart.js, recharts, etc)
  return (
    <div>
      <h3>Job Metrics</h3>
      <div>
        <b>Pipelines run:</b> {metrics.pipelines || 0}
        <br />
        <b>Failures:</b> {metrics.failures || 0}
        <br />
        <b>Uptime (s):</b> {metrics.uptime || 0}
      </div>
    </div>
  );
}
