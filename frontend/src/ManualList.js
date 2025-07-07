// ~/Soap/frontend/src/ManualList.js

import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ManualList() {
  const [manuals, setManuals] = useState([]);
  useEffect(() => {
    axios.get("/admin/manuals").then(resp => setManuals(resp.data));
  }, []);
  return (
    <div>
      <h2>All Manuals</h2>
      <ul>
        {manuals.map(m => (
          <li key={m.manual_id}>
            {m.filename} | {m.approved ? "✅ Approved" : "🕒 Pending"}
          </li>
        ))}
      </ul>
    </div>
  );
}
