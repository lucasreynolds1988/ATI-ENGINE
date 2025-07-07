// ~/Soap/frontend/src/TrainingResourceUpload.js

import React, { useState } from "react";
import axios from "axios";

function TrainingResourceUpload({ token }) {
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState("");

  const handleUpload = async e => {
    e.preventDefault();
    if (!file) {
      setMsg("Select a file.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    try {
      await axios.post("http://localhost:5003/training/upload", formData, {
        headers: { "x-api-token": token, "Content-Type": "multipart/form-data" }
      });
      setMsg("Upload successful.");
    } catch (err) {
      setMsg("Upload failed: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="section-card">
      <h2>Upload Training Resource</h2>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          onChange={e => setFile(e.target.files[0])}
        />
        <button type="submit">Upload</button>
      </form>
      {msg && <div>{msg}</div>}
    </div>
  );
}
export default TrainingResourceUpload;
