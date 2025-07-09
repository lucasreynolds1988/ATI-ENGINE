// ~/Soap/frontend/src/pages/Upload.js

import React, { useState } from "react";
import { uploadManual } from "../api";

function Upload({ token }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await uploadManual(formData);
    setStatus(res.data.status);
  };

  return (
    <div className="p-8">
      <h2>Upload Manual</h2>
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      <p>Status: {status}</p>
    </div>
  );
}

export default Upload;
