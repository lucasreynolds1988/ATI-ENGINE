import React, { useEffect, useState } from "react";
import axios from "axios";

export default function NodeHeartbeat() {
  const [beats, setBeats] = useState({});
  const apiToken = localStorage.getItem("apiToken");

  useEffect(() => {
    axios
      .get("/cluster/heartbeat", { headers: { "X-API-Token": apiToken } })
      .then(r => setBeats(r.data));
  }, [apiToken]);

  return (
    <div>
      <h3>Node Heartbeats</h3>
      <pre>{JSON.stringify(beats, null, 2)}</pre>
    </div>
  );
}
