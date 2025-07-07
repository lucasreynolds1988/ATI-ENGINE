import React, { useEffect } from "react";
import Globe from "globe.gl";

function GlobeBackground() {
  useEffect(() => {
    const globe = Globe()(document.getElementById("globe-canvas"))
      .globeImageUrl("//unpkg.com/three-globe/example/img/earth-night.jpg")
      .backgroundColor("rgba(0,0,0,0)")
      .width(window.innerWidth)
      .height(window.innerHeight);

    globe.controls().autoRotate = true;
    globe.controls().autoRotateSpeed = 0.5;

    return () => {
      document.getElementById("globe-canvas")?.remove();
    };
  }, []);

  return <canvas id="globe-canvas" className="fixed top-0 left-0 w-full h-full -z-10" />;
}

export default GlobeBackground;
