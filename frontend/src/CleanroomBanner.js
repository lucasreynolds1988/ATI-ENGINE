// ~/Soap/frontend/src/CleanroomBanner.js

import React from "react";

export default function CleanroomBanner() {
  return (
    <div style={{
      background: "linear-gradient(90deg, #e3e8ec 0%, #f2f5f8 100%)",
      borderBottom: "2px solid #b4c0cc",
      textAlign: "center",
      padding: "18px 0 14px 0",
      color: "#1682a7",
      fontWeight: 700,
      fontSize: "1.3rem",
      letterSpacing: ".03em",
      marginBottom: 28
    }}>
      <span role="img" aria-label="cleanroom">🧑‍🔬</span> ATI Oracle Engine — Cleanroom Training & SOP Management Suite
    </div>
  );
}
