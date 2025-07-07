import React, { useEffect, useState } from "react";
import axios from "axios";

export default function DocViewer({ jobId }) {
  const [text, setText] = useState("");
  const apiToken = localStorage.getItem("apiToken");

  useEffect(() => {
    axios
      .get(`/jobfile/${jobId}`, { headers: { "X-API-Token": apiToken } })
      .then(r => setText(r.data.contents || ""));
  }, [jobId, apiToken]);

  return (
    <div>
      <h3>Document Viewer</h3>
      <pre style={{ maxHeight: 400, overflow: "auto" }}>{text}</pre>
    </div>
  );
}
