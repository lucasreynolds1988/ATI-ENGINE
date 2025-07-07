import React, { useEffect, useState } from "react";
import axios from "axios";

export default function AuditTrail() {
  const [history, setHistory] = useState([]);
  const apiToken = localStorage.getItem("apiToken");

  useEffect(() => {
    axios
      .get("/pipeline/history", { headers: { "X-API-Token": apiToken } })
      .then(r => setHistory(r.data.lines || []));
  }, [apiToken]);

  return (
    <div>
      <h3>Audit Trail</h3>
      <pre style={{ maxHeight: 200, overflow: "auto" }}>
        {history.map((line, i) => (
          <div key={i}>{line}</div>
        ))}
      </pre>
    </div>
  );
}
