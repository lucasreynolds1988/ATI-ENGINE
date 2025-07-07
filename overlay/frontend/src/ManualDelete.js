// ~/Soap/frontend/src/ManualDelete.js

import React, { useState } from "react";
import axios from "axios";

function ManualDelete({ token }) {
  const [filename, setFilename] = useState("");
  const [msg, setMsg] = useState("");

  const handleDelete = async e => {
    e.preventDefault();
    if (!filename.trim()) {
      setMsg("Enter the filename to delete.");
      return;
    }
    try {
      await axios.delete(`http://localhost:5003/manuals/delete/${filename}`, {
        headers: { "x-api-token": token }
      });
      setMsg(`Manual '${filename}' deleted.`);
    } catch (err) {
      setMsg("Delete failed: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="section-card">
      <h2>Delete Uploaded Manual</h2>
      <form onSubmit={handleDelete}>
        <input
          type="text"
          placeholder="Enter manual filename"
          value={filename}
          onChange={e => setFilename(e.target.value)}
        />
        <button type="submit">Delete</button>
      </form>
      {msg && <div style={{ color: "#c21825" }}>{msg}</div>}
    </div>
  );
}

export default ManualDelete;
