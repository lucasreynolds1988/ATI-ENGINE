import React from "react";

function LockIcon({ size = 24, color = "#32aaff" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={color}>
      <path d="M12 2C9.8 2 8 3.8 8 6v4H6v12h12V10h-2V6c0-2.2-1.8-4-4-4zm0 2c1.1 0 2 .9 2 2v4h-4V6c0-1.1.9-2 2-2zm0 10c.6 0 1 .4 1 1v3h-2v-3c0-.6.4-1 1-1z"/>
    </svg>
  );
}

export default LockIcon;
