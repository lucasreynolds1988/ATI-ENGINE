// ~/Soap/frontend/src/Modal.js

import React from "react";

export default function Modal({ open, onClose, title, children }) {
  if (!open) return null;
  return (
    <div style={{
      position: "fixed",
      top: 0, left: 0, right: 0, bottom: 0,
      background: "rgba(40,60,80,0.12)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 9999
    }}>
      <div style={{
        background: "#fff",
        borderRadius: 16,
        boxShadow: "0 4px 32px rgba(20,60,90,0.10)",
        padding: "32px 38px",
        minWidth: 320,
        maxWidth: 540
      }}>
        <h3 style={{ marginTop: 0 }}>{title}</h3>
        <div>{children}</div>
        <button onClick={onClose} style={{ marginTop: 20 }}>Close</button>
      </div>
    </div>
  );
}
