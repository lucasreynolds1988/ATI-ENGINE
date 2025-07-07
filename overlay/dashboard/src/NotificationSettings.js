import React, { useState } from "react";

export default function NotificationSettings({ onUpdate }) {
  const [enabled, setEnabled] = useState(
    localStorage.getItem("notiEnabled") === "true"
  );

  function toggle() {
    const next = !enabled;
    setEnabled(next);
    localStorage.setItem("notiEnabled", next ? "true" : "false");
    if (onUpdate) onUpdate(next);
  }

  return (
    <div>
      <label>
        <input type="checkbox" checked={enabled} onChange={toggle} />
        Enable Desktop Notifications
      </label>
    </div>
  );
}
