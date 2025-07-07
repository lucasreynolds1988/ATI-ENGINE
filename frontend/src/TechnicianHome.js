// ~/Soap/frontend/src/TechnicianHome.js

import React from "react";

function TechnicianHome() {
  return (
    <div className="section-card">
      <h1>Welcome, Technician</h1>
      <p>
        Use the navigation bar to access all system functions: SOP generation, manual upload, live metrics, scavenger bot, training, and more.
      </p>
      <ul>
        <li>Need to upload a new manual? Go to <b>Upload Manual</b>.</li>
        <li>Want to generate or review SOPs? Use <b>Generate SOP</b> or <b>Admin Review</b>.</li>
        <li>Check your <b>Jobs</b> and <b>Metrics</b> any time.</li>
      </ul>
      <p>
        <i>This interface is optimized for technician training in FDA, EPA, and Pharma-regulated environments.</i>
      </p>
    </div>
  );
}

export default TechnicianHome;
