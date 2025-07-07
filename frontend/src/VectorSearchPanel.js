// ~/Soap/frontend/src/VectorSearchPanel.js

import React, { useState } from "react";
import axios from "axios";

export default function VectorSearchPanel() {
  const [query, setQuery] = useState("");
  const [engine, setEngine] = useState("openai");
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const resp = await axios.post("/ai/query", {
      question: query,
      engine
    });
    setResults(resp.data.matches || []);
  };

  return (
    <div>
      <h2>Semantic Vector Search</h2>
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Type your question"
      />
      <select value={engine} onChange={e => setEngine(e.target.value)}>
        <option value="openai">OpenAI</option>
        <option value="gemini">Gemini</option>
        <option value="ollama">Ollama</option>
      </select>
      <button onClick={handleSearch}>Search</button>
      <ul>
        {results.map((r, i) => (
          <li key={i}>{r.text}</li>
        ))}
      </ul>
    </div>
  );
}
