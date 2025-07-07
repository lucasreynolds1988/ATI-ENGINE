import React from "react";

function DevConsole({ data }) {
  return (
    <div className="p-4 bg-gray-900 text-green-400 text-xs rounded">
      <h3 className="text-lg mb-2">🚧 Developer Console</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default DevConsole;
