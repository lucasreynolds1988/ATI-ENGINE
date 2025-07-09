// ~/Soap/frontend/src/pages/SOPGenerator.js

import React, { useState } from "react";
import { askAI } from "../api";

function SOPGenerator() {
  const [question, setQuestion] = useState("");
  const [output, setOutput] = useState("");

  const handleSubmit = async () => {
    const res = await askAI(question);
    setOutput(res.data.response || "No response");
  };

  return (
    <div className="p-8">
      <h2>SOP Generator</h2>
      <textarea value={question} onChange={e => setQuestion(e.target.value)} />
      <button onClick={handleSubmit}>Generate</button>
      <pre>{output}</pre>
    </div>
  );
}

export default SOPGenerator;
