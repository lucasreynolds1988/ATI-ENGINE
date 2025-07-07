// ~/Soap/frontend/src/ResourceLibrary.js

import React, { useEffect, useState } from "react";
import axios from "axios";

function ResourceLibrary({ token }) {
  const [resources, setResources] = useState([]);
  useEffect(() => {
    if (!token) return;
    axios.get("http://localhost:5003/training/list", {
      headers: { "x-api-token": token }
    })
      .then(resp => setResources(resp.data.resources || []))
      .catch(() => setResources([]));
  }, [token]);

  if (!resources.length) return <div>No resources available.</div>;
  return (
    <div className="section-card">
      <h2>Training Resource Library</h2>
      <ul>
        {resources.map(r => (
          <li key={r}>{r}</li>
        ))}
      </ul>
    </div>
  );
}
export default ResourceLibrary;
