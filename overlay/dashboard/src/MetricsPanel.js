import React, { useEffect, useState } from "react";
import axios from "axios";

export default function MetricsPanel() {
  const [metrics, setMetrics] = useState({});
  const apiToken = localStorage.getItem("apiToken");

  useEffect(() => {
    axios
      .get("/metrics", { headers: { "X-API-Token": apiToken } })
      .then(r => setMetrics(r.data));
  }, [apiToken]);

  return (
    <div>
      <b>Metrics:</b>
      <pre>{JSON.stringify(metrics, null, 2)}</pre>
    </div>
  );
}
