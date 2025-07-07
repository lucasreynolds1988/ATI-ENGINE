// ~/Soap/frontend/src/AdminPanel.js

import React, { useEffect, useState } from "react";
import axios from "axios";

export default function AdminPanel() {
  const [manuals, setManuals] = useState([]);
  useEffect(() => {
    axios.get("/admin/manuals").then(resp => setManuals(resp.data));
  }, []);
  const approve = id => {
    axios.post("/admin/approve_manual", { manual_id: id, approved: true }).then(() => {
      setManuals(manuals.map(m => m.manual_id === id ? { ...m, approved: true } : m));
    });
  };
  return (
    <div>
      <h2>Admin Panel</h2>
      <ul>
        {manuals.map(m => (
          <li key={m.manual_id}>
            {m.filename} | {m.approved ? "✅" : (
              <button onClick={() => approve(m.manual_id)}>Approve</button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
