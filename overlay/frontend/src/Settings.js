// ~/Soap/frontend/src/Settings.js

import React, { useState } from "react";

function Settings({ token }) {
  // Placeholder for future settings, theme, etc.
  const [msg] = useState("Settings are coming soon.");
  return (
    <div className="section-card">
      <h2>Settings</h2>
      <div>{msg}</div>
    </div>
  );
}
export default Settings;
