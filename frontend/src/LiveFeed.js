// ~/Soap/frontend/src/LiveFeed.js

import React, { useEffect, useState } from "react";
import { getLog } from "./api";

function LiveFeed({ token }) {
  const [lines, setLines] = useState([]);

  useEffect(() => {
    if (!token) return;
    const interval = setInterval(() => {
      getLog(token)
        .then(resp => {
          // If response is blob (file), convert to text
          resp.data.text().then(txt => setLines(txt.split("\n")));
        })
        .catch(() => setLines([]));
    }, 4000);
    return () => clearInterval(interval);
  }, [token]);

  return (
    <div>
      <h2>Live System Feed</h2>
      <div className="live-feed">
        {lines.map((l, i) => <div key={i}>{l}</div>)}
      </div>
    </div>
  );
}

export default LiveFeed;
