import React, { useRef, useState } from "react";
import axios from "axios";

export default function BatchUpload() {
  const [message, setMessage] = useState("");
  const inputRef = useRef();
  const apiToken = localStorage.getItem("apiToken");

  function handleBatchUpload(e) {
    e.preventDefault();
    const files = inputRef.current.files;
    if (!files.length) return;
    const promises = [];
    for (let file of files) {
      const data = new FormData();
      data.append("file", file);
      promises.push(
        axios.post("/upload", data, {
          headers: {
            "X-API-Token": apiToken,
            "Content-Type": "multipart/form-data"
          }
        })
      );
    }
    Promise.all(promises)
      .then(() => setMessage("Batch uploaded"))
      .catch(() => setMessage("Batch upload failed"));
  }

  return (
    <form onSubmit={handleBatchUpload}>
      <h3>Batch Upload Jobs</h3>
      <input type="file" multiple ref={inputRef} required />
      <button type="submit">Upload Batch</button>
      <div>{message}</div>
    </form>
  );
}
