// ~/Soap/frontend/src/MetricsPanel.js

import React, { useEffect, useState } from "react";
import { getMetrics } from "./api";

function MetricsPanel({ token }) {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    if (!token) return;
    getMetrics(token)
      .then(resp => setMetrics(resp.data))
      .catch(() => setMetrics(null));
  }, [token]);

  if (!metrics) return <div>Loading system metrics...</div>;

  return (
    <div>
      <h2>System Metrics</h2>
      <ul>
        {Object.entries(metrics).map(([k, v]) => (
          <li key={k}>
            <strong>{k}:</strong> {v?.toString()}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MetricsPanel;
