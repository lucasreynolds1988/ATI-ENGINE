import React, { useEffect, useRef } from "react";

const NUM_PARTICLES = 21;

function getRandom(min, max) {
  return Math.random() * (max - min) + min;
}

export default function ParticleBurst({ show, onComplete }) {
  const container = useRef();

  useEffect(() => {
    if (show && container.current) {
      const particles = [];
      for (let i = 0; i < NUM_PARTICLES; i++) {
        const angle = getRandom(0, 2 * Math.PI);
        const distance = getRandom(40, 96);
        const tx = Math.cos(angle) * distance;
        const ty = Math.sin(angle) * distance;
        particles.push(
          <span
            className="particle"
            key={i}
            style={{
              "--tx": `${tx}px`,
              "--ty": `${ty}px`,
              left: "50%",
              top: "50%",
              transform: "translate(-50%, -50%)",
            }}
          />
        );
      }
      container.current.innerHTML = "";
      particles.forEach((p) => {
        const el = document.createElement("span");
        el.className = "particle";
        el.style.setProperty("--tx", p.props.style["--tx"]);
        el.style.setProperty("--ty", p.props.style["--ty"]);
        el.style.left = p.props.style.left;
        el.style.top = p.props.style.top;
        el.style.transform = p.props.style.transform;
        container.current.appendChild(el);
      });
      setTimeout(() => {
        container.current.innerHTML = "";
        if (onComplete) onComplete();
      }, 850);
    }
  }, [show, onComplete]);

  return <span ref={container} className="particle-burst" />;
}
