// ~/Soap/frontend/src/TechnicianProfile.js

import React, { useEffect, useState } from "react";
import axios from "axios";

function TechnicianProfile({ token }) {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    if (!token) return;
    axios.get("http://localhost:5003/technicians/me", {
      headers: { "x-api-token": token }
    })
      .then(resp => setProfile(resp.data.profile))
      .catch(() => setProfile(null));
  }, [token]);

  if (!profile) return <div>Loading...</div>;
  return (
    <div className="section-card">
      <h2>My Profile</h2>
      <ul>
        <li><b>Name:</b> {profile.name}</li>
        <li><b>Role:</b> {profile.role}</li>
        <li><b>Email:</b> {profile.email}</li>
        <li><b>Joined:</b> {profile.joined}</li>
      </ul>
    </div>
  );
}
export default TechnicianProfile;
