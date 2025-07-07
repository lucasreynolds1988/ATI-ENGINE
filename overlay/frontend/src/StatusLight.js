// ~/Soap/frontend/src/StatusLight.js

import React from "react";

export default function StatusLight({ status }) {
  const color =
    status === "OK"
      ? "#179b1f"
      : status === "idle"
      ? "#1ab19f"
      : status === "error"
      ? "#c21825"
      : "#b9bfc4";
  return (
    <span
      style={{
        display: "inline-block",
        width: 16,
        height: 16,
        borderRadius: 8,
        marginRight: 8,
        background: color,
        border: "1.5px solid #c2d3dc",
        verticalAlign: "middle"
      }}
    />
  );
}
