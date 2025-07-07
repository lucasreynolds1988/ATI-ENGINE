// ~/Soap/frontend/src/Footer.js

import React from "react";

function Footer() {
  return (
    <footer style={{
      textAlign: "center",
      fontSize: 13,
      color: "#8797a1",
      padding: "24px 0 12px 0"
    }}>
      ATI Oracle Engine &copy; {new Date().getFullYear()} &nbsp;|&nbsp; Training Suite for Scientific &amp; Industrial Technicians
    </footer>
  );
}

export default Footer;

