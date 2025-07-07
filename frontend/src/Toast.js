import React from "react";

function Toast({ text, type = "info" }) {
  const bgColor = {
    info: "bg-blue-600",
    error: "bg-red-600",
    success: "bg-green-600",
    warning: "bg-yellow-600"
  }[type];

  return (
    <div className={`fixed bottom-4 right-4 px-4 py-2 text-white rounded shadow-lg ${bgColor}`}>
      {text}
    </div>
  );
}

export default Toast;
