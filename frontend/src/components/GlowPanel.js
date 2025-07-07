import React from "react";

function GlowPanel({ title, children }) {
  return (
    <div className="card border border-blue-500 p-4 rounded-xl shadow-lg">
      <h3 className="text-blue-400 text-lg font-bold mb-2">{title}</h3>
      <div>{children}</div>
    </div>
  );
}

export default GlowPanel;
