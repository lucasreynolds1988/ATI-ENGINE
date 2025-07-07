import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ClusterNodes() {
  const [nodes, setNodes] = useState([]);
  const [host, setHost] = useState("");
  const apiToken = localStorage.getItem("apiToken");

  useEffect(() => {
    axios
      .get("/cluster/nodes", { headers: { "X-API-Token": apiToken } })
      .then(r => setNodes(r.data.nodes || []));
  }, [apiToken]);

  function addNode(e) {
    e.preventDefault();
    axios
      .post(
        "/cluster/nodes",
        { host },
        { headers: { "X-API-Token": apiToken } }
      )
      .then(() => setNodes(nodes => [...nodes, host]));
  }

  return (
    <div>
      <h3>Cluster Nodes</h3>
      <ul>
        {nodes.map((n, i) => (
          <li key={i}>{n}</li>
        ))}
      </ul>
      <form onSubmit={addNode}>
        <input
          value={host}
          onChange={e => setHost(e.target.value)}
          placeholder="New node host"
        />
        <button type="submit">Add Node</button>
      </form>
    </div>
  );
}
