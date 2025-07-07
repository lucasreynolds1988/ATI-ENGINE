import React, { useEffect, useState } from "react";
import StatusBox from "./StatusBox";

function AgentHeartbeat() {
  const [pulse, setPulse] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPulse((prev) => (prev + 1) % 100);
    }, 4000); // Matches rotor cycle
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-2 right-2 flex">
      <StatusBox label="GitHub Pull" value="Ready" pulse={pulse % 4 === 0} />
      <StatusBox label="MongoDB Ingest" value="Active" pulse={pulse % 4 === 1} />
      <StatusBox label="GCS Overlay" value="Idle" pulse={pulse % 4 === 2} />
      <StatusBox label="Rotor Engine" value="Spinning" pulse={pulse % 4 === 3} />
    </div>
  );
}

export default AgentHeartbeat;
