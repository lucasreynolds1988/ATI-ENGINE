// ~/Soap/frontend/src/UploadHistory.js

import React, { useEffect, useState } from "react";
import axios from "axios";

function UploadHistory({ token }) {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (!token) return;
    axios.get("http://localhost:5003/manuals/upload-history", {
      headers: { "x-api-token": token }
    })
      .then(resp => setHistory(resp.data.history || []))
      .catch(() => setHistory([]));
  }, [token]);

  if (!history.length) return <div>No upload history found.</div>;
  return (
    <div className="section-card">
      <h2>Manual Upload History</h2>
      <table>
        <thead>
          <tr>
            <th>Filename</th>
            <th>Uploaded By</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {history.map((h, idx) => (
            <tr key={idx}>
              <td>{h.filename}</td>
              <td>{h.user}</td>
              <td>{h.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
export default UploadHistory;
