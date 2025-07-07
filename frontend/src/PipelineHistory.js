// ~/Soap/frontend/src/PipelineHistory.js

import React, { useEffect, useState } from "react";
import { getPipelineHistory } from "./api";

function PipelineHistory({ token }) {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (!token) return;
    getPipelineHistory(token)
      .then(resp => setHistory(resp.data.lines || []))
      .catch(() => setHistory([]));
  }, [token]);

  return (
    <div>
      <h2>Pipeline History</h2>
      <div className="history-log">
        {history.map((line, i) => <div key={i}>{line}</div>)}
      </div>
    </div>
  );
}

export default PipelineHistory;
