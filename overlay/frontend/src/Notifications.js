// ~/Soap/frontend/src/Notifications.js

import React, { useEffect, useState } from "react";

export default function Notifications({ message, duration = 5000 }) {
  const [show, setShow] = useState(!!message);
  useEffect(() => {
    if (message) {
      setShow(true);
      const timer = setTimeout(() => setShow(false), duration);
      return () => clearTimeout(timer);
    }
  }, [message, duration]);
  if (!show || !message) return null;
  return (
    <div style={{
      position: "fixed",
      top: 24,
      right: 24,
      zIndex: 9999,
      background: "#1ab19f",
      color: "#fff",
      borderRadius: 8,
      padding: "12px 22px",
      boxShadow: "0 2px 16px rgba(40,80,80,0.14)",
      fontWeight: 600
    }}>
      {message}
    </div>
  );
}
