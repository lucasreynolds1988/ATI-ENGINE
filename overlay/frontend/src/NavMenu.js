// ~/Soap/frontend/src/NavMenu.js

import React from "react";
import { NavLink } from "react-router-dom";

function NavMenu() {
  return (
    <div style={{
      background: "#e3e8ec",
      borderBottom: "1.5px solid #c2d3dc",
      padding: "14px 24px",
      display: "flex",
      gap: 20,
      alignItems: "center"
    }}>
      <NavLink to="/" end>Dashboard</NavLink>
      <NavLink to="/training">Training</NavLink>
      <NavLink to="/upload">Upload</NavLink>
      <NavLink to="/scavenger">Scavenger</NavLink>
      <NavLink to="/jobs">Jobs</NavLink>
      <NavLink to="/metrics">Metrics</NavLink>
      <NavLink to="/roles">Roles</NavLink>
      <NavLink to="/settings">Settings</NavLink>
      <NavLink to="/help">Help</NavLink>
    </div>
  );
}
export default NavMenu;
