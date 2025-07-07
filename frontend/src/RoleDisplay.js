// ~/Soap/frontend/src/RoleDisplay.js

import React, { useEffect, useState } from "react";
import { getRoles } from "./api";

function RoleDisplay({ token }) {
  const [roles, setRoles] = useState([]);

  useEffect(() => {
    if (!token) return;
    getRoles(token)
      .then(resp => setRoles(resp.data.roles || []))
      .catch(() => setRoles([]));
  }, [token]);

  if (!roles.length) return <div>No roles found.</div>;

  return (
    <div>
      <h2>Roles</h2>
      <ul>
        {roles.map(role => (
          <li key={role}>{role}</li>
        ))}
      </ul>
    </div>
  );
}

export default RoleDisplay;
