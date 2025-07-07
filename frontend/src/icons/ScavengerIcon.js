import React from "react";

function ScavengerIcon({ size = 24, color = "#32aaff" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={color}>
      <path d="M12 4a8 8 0 100 16 8 8 0 000-16zm1 9h3v2h-3v3h-2v-3H8v-2h3V8h2v5z"/>
    </svg>
  );
}

export default ScavengerIcon;
