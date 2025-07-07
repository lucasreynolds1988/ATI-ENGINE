// ~/Soap/frontend/src/Loader.js

import React from "react";

export default function Loader({ text = "Loading..." }) {
  return (
    <div style={{
      display: "flex",
      alignItems: "center",
      padding: 20,
      justifyContent: "center"
    }}>
      <div className="spinner" style={{
        width: 28,
        height: 28,
        marginRight: 14,
        border: "4px solid #c2d3dc",
        borderTop: "4px solid #1682a7",
        borderRadius: "50%",
        animation: "spin 1s linear infinite"
      }} />
      <span>{text}</span>
      <style>
        {`
        @keyframes spin {
          0% { transform: rotate(0deg);}
          100% {transform: rotate(360deg);}
        }
        `}
      </style>
    </div>
  );
}
