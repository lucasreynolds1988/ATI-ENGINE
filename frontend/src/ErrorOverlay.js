import React from "react";

function ErrorOverlay({ message }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50">
      <div className="text-center bg-red-900 p-6 rounded-lg shadow-lg text-white">
        <h2 className="text-2xl font-bold mb-4">🔥 SYSTEM ERROR</h2>
        <p>{message}</p>
      </div>
    </div>
  );
}

export default ErrorOverlay;
