// ~/Soap/frontend/src/AgentStatus.js

import React, { useEffect, useState } from "react";
import axios from "axios";
import StatusLight from "./StatusLight";

function AgentStatus({ token }) {
  const [statuses, setStatuses] = useState(null);

  useEffect(() => {
    if (!token) return;
    axios.get("http://localhost:5003/agents/status", {
      headers: { "x-api-token": token }
    })
      .then(resp => setStatuses(resp.data.statuses))
      .catch(() => setStatuses(null));
  }, [token]);

  if (!statuses) return <div>Loading agent status...</div>;
  return (
    <div className="section-card">
      <h2>Rotor Agent Status</h2>
      <ul>
        {Object.entries(statuses).map(([agent, status]) => (
          <li key={agent}>
            <StatusLight status={status} />
            <b>{agent}</b>: {status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AgentStatus;
