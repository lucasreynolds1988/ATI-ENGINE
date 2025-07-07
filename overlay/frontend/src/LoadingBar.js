// ~/Soap/frontend/src/LoadingBar.js

import React from "react";

export default function LoadingBar({ progress = 0 }) {
  return (
    <div style={{
      width: "100%",
      background: "#e2e9f0",
      borderRadius: 6,
      height: 8,
      margin: "14px 0"
    }}>
      <div style={{
        width: `${progress}%`,
        background: "#1ab19f",
        height: "100%",
        borderRadius: 6,
        transition: "width 0.2s"
      }} />
    </div>
  );
}
