// ~/Soap/frontend/src/NotFound.js

import React from "react";
import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="section-card" style={{ textAlign: "center" }}>
      <h2>404: Page Not Found</h2>
      <p>That page doesn't exist. Please check the menu or return to <Link to="/">Dashboard</Link>.</p>
    </div>
  );
}
