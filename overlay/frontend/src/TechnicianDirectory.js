// ~/Soap/frontend/src/TechnicianDirectory.js

import React, { useEffect, useState } from "react";
import axios from "axios";

function TechnicianDirectory({ token }) {
  const [techs, setTechs] = useState([]);

  useEffect(() => {
    if (!token) return;
    axios.get("http://localhost:5003/technicians/list", {
      headers: { "x-api-token": token }
    })
      .then(resp => setTechs(resp.data.technicians || []))
      .catch(() => setTechs([]));
  }, [token]);

  if (!techs.length) return <div>No technicians found.</div>;
  return (
    <div className="section-card">
      <h2>Technician Directory</h2>
      <ul>
        {techs.map(tech => (
          <li key={tech.id}>{tech.name} ({tech.role})</li>
        ))}
      </ul>
    </div>
  );
}
export default TechnicianDirectory;
