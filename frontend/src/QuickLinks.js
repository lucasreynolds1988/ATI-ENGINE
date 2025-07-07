// ~/Soap/frontend/src/QuickLinks.js

import React from "react";
import { NavLink } from "react-router-dom";

export default function QuickLinks() {
  return (
    <div className="section-card" style={{ padding: "18px 16px" }}>
      <h2>Quick Links</h2>
      <ul>
        <li><NavLink to="/upload">Upload Manual</NavLink></li>
        <li><NavLink to="/sop">Generate SOP</NavLink></li>
        <li><NavLink to="/scavenger">Scavenger Bot</NavLink></li>
        <li><NavLink to="/training">Training Resources</NavLink></li>
        <li><NavLink to="/jobs">Job Queue</NavLink></li>
        <li><NavLink to="/metrics">Metrics</NavLink></li>
        <li><NavLink to="/roles">Roles</NavLink></li>
        <li><NavLink to="/settings">Settings</NavLink></li>
      </ul>
    </div>
  );
}
