// ~/Soap/frontend/src/ManualsList.js

import React, { useEffect, useState } from "react";
import axios from "axios";

function ManualsList({ token }) {
  const [manuals, setManuals] = useState([]);
  useEffect(() => {
    if (!token) return;
    axios
      .get("http://localhost:5003/manuals/list", {
        headers: { "x-api-token": token },
      })
      .then(resp => setManuals(resp.data.files || []))
      .catch(() => setManuals([]));
  }, [token]);
  if (!manuals.length) return <div>No manuals found.</div>;
  return (
    <div className="section-card">
      <h2>Uploaded Manuals</h2>
      <ul>
        {manuals.map(f => (
          <li key={f}>{f}</li>
        ))}
      </ul>
    </div>
  );
}
export default ManualsList;
