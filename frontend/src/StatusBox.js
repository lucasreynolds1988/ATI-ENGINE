import React from "react";

function StatusBox({ label, value, pulse = false }) {
  return (
    <div className="flex flex-col items-center m-2">
      <div className={`w-5 h-5 rounded-full ${pulse ? 'animate-pulse bg-green-500' : 'bg-gray-600'}`} />
      <div className="text-sm mt-1 text-white">{label}</div>
      <div className="text-xs text-gray-400">{value}</div>
    </div>
  );
}

export default StatusBox;
