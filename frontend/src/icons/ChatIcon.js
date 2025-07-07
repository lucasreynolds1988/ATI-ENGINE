import React from "react";

function ChatIcon({ size = 24, color = "#32aaff" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={color}>
      <path d="M4 4h16v12H5.17L4 17.17V4zm0-2c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2H4z"/>
    </svg>
  );
}

export default ChatIcon;
