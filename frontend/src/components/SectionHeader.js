import React from "react";

function SectionHeader({ text }) {
  return (
    <h2 className="text-2xl font-bold text-blue-400 my-4 border-b border-blue-800 pb-2">
      {text}
    </h2>
  );
}

export default SectionHeader;
