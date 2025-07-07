import React from "react";

function OrbitIcon({ size = 24, color = "#32aaff" }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={color}>
      <path d="M12 2a10 10 0 1010 10A10 10 0 0012 2zm1 17.93a8.12 8.12 0 01-2 0V17a1 1 0 012 0v2.93zM4.07 13H7a1 1 0 010 2H4.07a8.12 8.12 0 010-2zM13 7a1 1 0 00-2 0v2.07a8.12 8.12 0 012 0zM17 11a1 1 0 000 2h2.93a8.12 8.12 0 000-2z"/>
    </svg>
  );
}

export default OrbitIcon;
