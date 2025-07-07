import React, { useState } from "react";
import ParticleBurst from "./ParticleBurst";

export default function AIButton({ children, className = "", style = {}, ...props }) {
  const [burst, setBurst] = useState(false);

  const handleClick = (e) => {
    setBurst(true);
    if (props.onClick) props.onClick(e);
  };

  return (
    <button
      className={`ai-glow ${className}`}
      {...props}
      style={{ ...style, position: "relative", overflow: "visible" }}
      onClick={handleClick}
    >
      {children}
      <ParticleBurst show={burst} onComplete={() => setBurst(false)} />
    </button>
  );
}
