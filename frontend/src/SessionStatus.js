// ~/Soap/frontend/src/SessionStatus.js

import React from "react";

export default function SessionStatus({ token }) {
  return (
    <div style={{
      float: "right",
      margin: 0,
      fontSize: 14,
      color: token ? "#179b1f" : "#c21825"
    }}>
      {token ? "Session Active" : "No Token"}
    </div>
  );
}
