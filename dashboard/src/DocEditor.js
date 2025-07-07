import React, { useEffect, useState } from "react";
import axios from "axios";

export default function DocEditor({ jobId }) {
  const [text, setText] = useState("");
  const [message, setMessage] = useState("");
  const apiToken = localStorage.getItem("apiToken");

  useEffect(() => {
    axios
      .get(`/jobfile/${jobId}`, { headers: { "X-API-Token": apiToken } })
      .then(r => setText(r.data.contents || ""));
  }, [jobId, apiToken]);

  function save() {
    axios
      .post(
        `/jobfile/${jobId}`,
        { contents: text },
        { headers: { "X-API-Token": apiToken } }
      )
      .then(() => setMessage("Saved"))
      .catch(() => setMessage("Failed"));
  }

  return (
    <div>
      <h3>Document Editor</h3>
      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        style={{ width: "100%", height: 200 }}
      />
      <button onClick={save}>Save</button>
      <div>{message}</div>
    </div>
  );
}
