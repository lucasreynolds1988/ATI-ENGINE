import React, { useState } from "react";
import axios from "axios";

function TestPanel({ token }) {
  const [output, setOutput] = useState("");

  const runTest = async () => {
    try {
      const res = await axios.get("/config", {
        headers: { "x-api-token": token }
      });
      setOutput(JSON.stringify(res.data, null, 2));
    } catch (err) {
      setOutput(err.message);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-lg font-bold mb-2">Test API Connection</h2>
      <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={runTest}>
        Run Config Check
      </button>
      {output && <pre className="bg-black text-green-300 p-2 mt-3">{output}</pre>}
    </div>
  );
}

export default TestPanel;
