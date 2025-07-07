// ~/Soap/frontend/src/HealthMonitor.js

import React, { useEffect, useState } from "react";
import axios from "axios";

export default function HealthMonitor() {
  const [status, setStatus] = useState({});
  useEffect(() => {
    axios.get("/health").then(resp => setStatus(resp.data));
    const timer = setInterval(() => {
      axios.get("/health").then(resp => setStatus(resp.data));
    }, 10000);
    return () => clearInterval(timer);
  }, []);
  return (
    <div>
      <h2>System Health</h2>
      <ul>
        {Object.entries(status).map(([k, v]) =>
          <li key={k}>{k}: {v === true ? "✅" : v === false ? "❌" : v}</li>
        )}
      </ul>
    </div>
  );
}
