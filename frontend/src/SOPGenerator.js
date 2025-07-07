// ~/Soap/frontend/src/SOPGenerator.js

import React, { useState } from "react";
import { runPipeline } from "./api";

function SOPGenerator({ token }) {
  const [fileId, setFileId] = useState("");
  const [status, setStatus] = useState(null);

  const handleRun = async (e) => {
    e.preventDefault();
    if (!fileId) return;
    try {
      const resp = await runPipeline(token, fileId);
      setStatus(`Started: ${resp.data.status}`);
    } catch (err) {
      setStatus("Error: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div>
      <h2>Generate SOP</h2>
      <form onSubmit={handleRun}>
        <input
          type="text"
          placeholder="Enter base filename"
          value={fileId}
          onChange={e => setFileId(e.target.value)}
        />
        <button type="submit">Run SOP Pipeline</button>
      </form>
      {status && <div>{status}</div>}
    </div>
  );
}

export default SOPGenerator;
