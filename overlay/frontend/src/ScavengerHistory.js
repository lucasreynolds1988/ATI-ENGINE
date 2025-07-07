// ~/Soap/frontend/src/ScavengerHistory.js

import React, { useEffect, useState } from "react";
import axios from "axios";

function ScavengerHistory({ token }) {
  const [history, setHistory] = useState([]);
  useEffect(() => {
    if (!token) return;
    axios.get("http://localhost:5003/scavenger/history", {
      headers: { "x-api-token": token }
    })
      .then(resp => setHistory(resp.data.history || []))
      .catch(() => setHistory([]));
  }, [token]);
  if (!history.length) return <div>No scavenger runs found.</div>;
  return (
    <div className="section-card">
      <h2>Scavenger Bot History</h2>
      <table>
        <thead>
          <tr>
            <th>URL</th>
            <th>Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {history.map((h, idx) => (
            <tr key={idx}>
              <td>{h.url}</td>
              <td>{h.date}</td>
              <td>{h.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
export default ScavengerHistory;
