// ~/Soap/frontend/src/AgentConfig.js

import React, { useState } from "react";
import axios from "axios";

function AgentConfig({ token }) {
  const [agent, setAgent] = useState("");
  const [config, setConfig] = useState("");
  const [msg, setMsg] = useState("");

  const handleSave = async e => {
    e.preventDefault();
    try {
      await axios.post(
        `http://localhost:5003/agents/config/${agent}`,
        { config },
        { headers: { "x-api-token": token } }
      );
      setMsg("Config saved.");
    } catch (err) {
      setMsg("Error: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="section-card">
      <h2>Agent Configuration</h2>
      <form onSubmit={handleSave}>
        <input
          type="text"
          placeholder="Agent name"
          value={agent}
          onChange={e => setAgent(e.target.value)}
        />
        <input
          type="text"
          placeholder="Config JSON"
          value={config}
          onChange={e => setConfig(e.target.value)}
        />
        <button type="submit">Save Config</button>
      </form>
      {msg && <div>{msg}</div>}
    </div>
  );
}
export default AgentConfig;
