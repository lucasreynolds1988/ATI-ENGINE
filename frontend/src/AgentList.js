// ~/Soap/frontend/src/AgentList.js

import React, { useEffect, useState } from "react";
import axios from "axios";

function AgentList({ token }) {
  const [agents, setAgents] = useState([]);

  useEffect(() => {
    if (!token) return;
    axios.get("http://localhost:5003/agents/list", {
      headers: { "x-api-token": token }
    })
      .then(resp => setAgents(resp.data.agents || []))
      .catch(() => setAgents([]));
  }, [token]);

  if (!agents.length) return <div>No agent info available.</div>;
  return (
    <div className="section-card">
      <h2>Active Agents</h2>
      <ul>
        {agents.map(agent => (
          <li key={agent}>{agent}</li>
        ))}
      </ul>
    </div>
  );
}
export default AgentList;
