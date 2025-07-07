// ~/Soap/frontend/src/Navbar.js

import React from "react";
import { NavLink } from "react-router-dom";
import "./App.css";

function Navbar({ token }) {
  return (
    <nav className="navbar">
      <NavLink to="/" end>Dashboard</NavLink>
      <NavLink to="/upload">Upload Manual</NavLink>
      <NavLink to="/sop">Generate SOP</NavLink>
      <NavLink to="/scavenger">Scavenger Bot</NavLink>
      <NavLink to="/jobs">Jobs</NavLink>
      <NavLink to="/metrics">Metrics</NavLink>
      <NavLink to="/roles">Roles</NavLink>
      <NavLink to="/review">Admin Review</NavLink>
      <NavLink to="/live">Live Feed</NavLink>
      <NavLink to="/history">History</NavLink>
      {token
        ? <span className="token-status">🔓</span>
        : <NavLink to="/login" className="login-link">Login</NavLink>}
    </nav>
  );
}

export default Navbar;
