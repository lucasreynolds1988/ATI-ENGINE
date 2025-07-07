import React, { useState } from "react";
import axios from "axios";

export default function UploadJob() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const apiToken = localStorage.getItem("apiToken");

  function upload(e) {
    e.preventDefault();
    if (!file) return;
    const data = new FormData();
    data.append("file", file);
    axios
      .post("/upload", data, {
        headers: {
          "X-API-Token": apiToken,
          "Content-Type": "multipart/form-data"
        }
      })
      .then(() => setMessage("Uploaded"))
      .catch(() => setMessage("Failed"));
  }

  return (
    <form onSubmit={upload}>
      <h3>Upload New SOP Job</h3>
      <input type="file" onChange={e => setFile(e.target.files[0])} required />
      <button type="submit">Upload</button>
      <div>{message}</div>
    </form>
  );
}
