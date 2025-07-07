// ~/Soap/frontend/src/HelpPage.js

import React from "react";

function HelpPage() {
  return (
    <div className="section-card">
      <h2>Help & Support</h2>
      <ul>
        <li>Need to upload manuals? See the Upload Manual page.</li>
        <li>For SOP generation, go to Generate SOP and enter your base filename.</li>
        <li>Scavenger Bot lets you crawl and archive any technical website.</li>
        <li>Check your Jobs and Metrics any time for system status.</li>
        <li>Contact your admin for new roles, tokens, or advanced access.</li>
      </ul>
      <div style={{ marginTop: 16, color: "#179b1f" }}>
        For support, email <a href="mailto:support@yourdomain.com">support@yourdomain.com</a>
      </div>
    </div>
  );
}

export default HelpPage;
