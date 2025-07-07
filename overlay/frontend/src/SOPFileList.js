// ~/Soap/frontend/src/SOPFileList.js

import React, { useEffect, useState } from "react";
import axios from "axios";

function SOPFileList({ token }) {
  const [sops, setSops] = useState([]);
  useEffect(() => {
    if (!token) return;
    axios
      .get("http://localhost:5003/sops/list", {
        headers: { "x-api-token": token },
      })
      .then(resp => setSops(resp.data.files || []))
      .catch(() => setSops([]));
  }, [token]);
  if (!sops.length) return <div>No SOPs found.</div>;
  return (
    <div className="section-card">
      <h2>Available SOPs</h2>
      <ul>
        {sops.map(f => (
          <li key={f}>{f}</li>
        ))}
      </ul>
    </div>
  );
}
export default SOPFileList;
