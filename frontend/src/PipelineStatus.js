// ~/Soap/frontend/src/PipelineStatus.js

import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getPipelineStatus } from "./api";

function PipelineStatus({ token }) {
  const { fileId } = useParams();
  const [status, setStatus] = useState(null);

  useEffect(() => {
    if (!token || !fileId) return;
    getPipelineStatus(token, fileId)
      .then(resp => setStatus(resp.data))
      .catch(() => setStatus(null));
  }, [token, fileId]);

  if (!fileId) return <div className="section-card">No file selected.</div>;
  if (!status) return <div className="section-card">Loading status for {fileId}...</div>;

  return (
    <div className="section-card">
      <h2>Pipeline Status: {fileId}</h2>
      <ul>
        {Object.entries(status).map(([ext, exists]) => (
          <li key={ext}>
            <b>{ext}:</b> {exists ? "✅ Exists" : "❌ Missing"}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PipelineStatus;
