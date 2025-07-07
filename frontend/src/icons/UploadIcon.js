import React from "react";

function UploadIcon({ size = 24, color = "#32aaff" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={color}>
      <path d="M5 20h14v-2H5v2zm7-18L5.33 10h3.34v4h4.66v-4h3.34L12 2z"/>
    </svg>
  );
}

export default UploadIcon;
