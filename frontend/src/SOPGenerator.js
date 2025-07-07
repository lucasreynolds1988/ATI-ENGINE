// ~/Soap/frontend/src/SOPGenerator.js

import React, { useState } from "react";
import { askAI } from "./api";

export default function SOPGenerator() {
  const [request, setRequest] = useState("");
  const [engine, setEngine] = useState("openai");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setResult("");
    try {
      const resp = await askAI(request, engine);
      setResult(resp.data.answer);
    } catch {
      setResult("Failed to generate SOP.");
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Generate SOP</h2>
      <textarea
        placeholder="Describe the SOP you need (e.g. 'Hydraulic Brake Bleed Procedure')"
        value={request}
        onChange={e => setRequest(e.target.value)}
      />
      <div>
        <select value={engine} onChange={e => setEngine(e.target.value)}>
          <option value="openai">OpenAI</option>
          <option value="gemini">Gemini</option>
          <option value="ollama">Ollama</option>
        </select>
        <button onClick={handleGenerate} disabled={loading}>Generate</button>
      </div>
      {loading && <p>Working...</p>}
      {result && <pre style={{ whiteSpace: "pre-wrap" }}>{result}</pre>}
    </div>
  );
}
