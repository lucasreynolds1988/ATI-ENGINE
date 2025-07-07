// ~/Soap/frontend/src/WelcomeSplash.js

import React from "react";

function WelcomeSplash() {
  return (
    <div className="section-card" style={{ textAlign: "center" }}>
      <h1>ATI Oracle Engine</h1>
      <h2 style={{ color: "#179b1f" }}>Pharmaceutical/Technical Training Suite</h2>
      <p>
        <b>FDA & EPA Compliant</b> — built for training, safety, and SOP management.<br />
        <span style={{ color: "#1682a7" }}>Modern. Modular. Technician-First.</span>
      </p>
      <img
        src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Stainless_steel_texture_123rf.jpg/640px-Stainless_steel_texture_123rf.jpg"
        alt="Stainless Steel Texture"
        style={{
          width: 200,
          borderRadius: 18,
          margin: "18px auto 6px auto",
          boxShadow: "0 2px 14px rgba(40,60,80,0.16)"
        }}
      />
      <p style={{ fontSize: "1.1rem", color: "#12526b" }}>
        Select an option from the menu to begin.
      </p>
    </div>
  );
}
export default WelcomeSplash;
