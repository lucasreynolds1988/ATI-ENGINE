// ~/Soap/frontend/src/Alert.js

import React from "react";

export default function Alert({ text, type = "info" }) {
  const color =
    type === "error"
      ? "#c21825"
      : type === "success"
      ? "#179b1f"
      : "#1682a7";
  return (
    <div style={{
      background: "#f7fafd",
      color,
      border: `1.5px solid ${color}`,
      borderRadius: 8,
      padding: "10px 18px",
      margin: "18px 0"
    }}>
      {text}
    </div>
  );
}
