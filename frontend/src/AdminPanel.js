// ~/Soap/frontend/src/AdminPanel.js

import React from "react";
import ApproveSOP from "./ApproveSOP";
import ManualDelete from "./ManualDelete";

function AdminPanel({ token }) {
  return (
    <div className="section-card">
      <h2>Admin Panel</h2>
      <ApproveSOP token={token} />
      <ManualDelete token={token} />
    </div>
  );
}

export default AdminPanel;
