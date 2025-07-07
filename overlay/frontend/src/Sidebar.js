// ~/Soap/frontend/src/Sidebar.js

import React from "react";
import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside style={{
      width: 180,
      padding: 18,
      background: "#e3e8ec",
      borderRight: "1px solid #d2e4ec",
      minHeight: "100vh"
    }}>
      <nav>
        <NavLink to="/">Dashboard</NavLink><br />
        <NavLink to="/training">Training</NavLink><br />
        <NavLink to="/upload">Upload</NavLink><br />
        <NavLink to="/scavenger">Scavenger</NavLink><br />
        <NavLink to="/jobs">Jobs</NavLink><br />
        <NavLink to="/metrics">Metrics</NavLink><br />
        <NavLink to="/roles">Roles</NavLink><br />
        <NavLink to="/settings">Settings</NavLink><br />
      </nav>
    </aside>
  );
}
