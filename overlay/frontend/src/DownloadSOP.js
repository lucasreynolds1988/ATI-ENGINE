// ~/Soap/frontend/src/DownloadSOP.js

import React, { useState } from "react";
import axios from "axios";

function DownloadSOP({ token }) {
  const [filename, setFilename] = useState("");
  const [msg, setMsg] = useState("");

  const handleDownload = async e => {
    e.preventDefault();
    if (!filename.trim()) {
      setMsg("Enter the SOP filename.");
      return;
    }
    try {
      const resp = await axios.get(
        `http://localhost:5003/sops/download/${filename}`,
        { headers: { "x-api-token": token }, responseType: "blob" }
      );
      // Force browser download
      const url = window.URL.createObjectURL(new Blob([resp.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      setMsg(`Downloaded ${filename}`);
    } catch (err) {
      setMsg("Download failed: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="section-card">
      <h2>Download SOP</h2>
      <form onSubmit={handleDownload}>
        <input
          type="text"
          placeholder="Enter SOP filename"
          value={filename}
          onChange={e => setFilename(e.target.value)}
        />
        <button type="submit">Download</button>
      </form>
      {msg && <div>{msg}</div>}
    </div>
  );
}
export default DownloadSOP;
