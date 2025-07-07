// ~/Soap/frontend/src/ScavengerBot.js

import React, { useState } from "react";
import axios from "axios";

function ScavengerBot({ token }) {
  const [url, setUrl] = useState("");
  const [msg, setMsg] = useState("");

  const handleScavenge = async (e) => {
    e.preventDefault();
    if (!url) {
      setMsg("Please enter a URL.");
      return;
    }
    try {
      const resp = await axios.post(
        "http://localhost:5003/scavenger/start",
        { url },
        { headers: { "x-api-token": token } }
      );
      setMsg("Scavenger started: " + resp.data.status);
    } catch (err) {
      setMsg("Failed: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div>
      <h2>Scavenger Bot</h2>
      <form onSubmit={handleScavenge}>
        <input
          type="text"
          placeholder="https://example.com"
          value={url}
          onChange={e => setUrl(e.target.value)}
        />
        <button type="submit">Scavenge</button>
      </form>
      {msg && <div>{msg}</div>}
    </div>
  );
}

export default ScavengerBot;
