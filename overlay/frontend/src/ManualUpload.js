// ~/Soap/frontend/src/ManualUpload.js

import React, { useState } from "react";
import axios from "axios";

function ManualUpload({ token }) {
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState("");

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setMsg("Please select a file.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);

    try {
      const resp = await axios.post(
        "http://localhost:5003/manuals/upload",
        formData,
        { headers: { "x-api-token": token, "Content-Type": "multipart/form-data" } }
      );
      setMsg(`Upload successful: ${resp.data.filename}`);
    } catch (err) {
      setMsg("Upload failed: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div>
      <h2>Upload Manual</h2>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept=".pdf,.docx,.txt,.jpeg"
          onChange={e => setFile(e.target.files[0])}
        />
        <button type="submit">Upload</button>
      </form>
      {msg && <div>{msg}</div>}
    </div>
  );
}

export default ManualUpload;
