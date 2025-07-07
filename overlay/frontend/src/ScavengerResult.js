// ~/Soap/frontend/src/ScavengerResult.js

import React from "react";

export default function ScavengerResult({ result }) {
  if (!result) return null;
  return (
    <div className="section-card" style={{ marginTop: 24 }}>
      <h3>Scavenger Results</h3>
      <pre style={{ fontSize: "1rem" }}>
        {typeof result === "object"
          ? JSON.stringify(result, null, 2)
          : result.toString()}
      </pre>
    </div>
  );
}
