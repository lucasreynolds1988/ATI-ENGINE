import React, { useEffect, useState } from "react";
import axios from "axios";

export default function RoleDisplay() {
  const [roles, setRoles] = useState({});
  const apiToken = localStorage.getItem("apiToken");

  useEffect(() => {
    axios
      .get("/roles", { headers: { "X-API-Token": apiToken } })
      .then(r => setRoles(r.data));
  }, [apiToken]);

  return (
    <div>
      <b>Roles:</b>
      <pre>{JSON.stringify(roles, null, 2)}</pre>
    </div>
  );
}
