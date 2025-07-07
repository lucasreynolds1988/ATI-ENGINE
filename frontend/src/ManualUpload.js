// ~/Soap/frontend/src/ManualUpload.js

import React, { useState } from "react";
import { uploadManual } from "./api";

export default function ManualUpload() {
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState("");

  const handleUpload = async e => {
    e.preventDefault();
    if (!file) {
      setMsg("Select a file first.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    try {
      const resp = await uploadManual(formData);
      setMsg(`Upload successful! Chunks: ${resp.data.chunks || "?"}`);
    } catch (err) {
      setMsg("Upload failed.");
    }
  };

  return (
    <div>
      <h2>Upload Manual</h2>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={e => setFile(e.target.files[0])}
        />
        <button type="submit">Upload</button>
      </form>
      {msg && <div>{msg}</div>}
    </div>
  );
}
