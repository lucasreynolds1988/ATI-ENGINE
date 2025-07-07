// ~/Soap/frontend/src/AIChat.js

import React, { useState } from "react";
import { askAI } from "./api";

export default function AIChat() {
  const [question, setQuestion] = useState("");
  const [engine, setEngine] = useState("openai");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    setLoading(true);
    setAnswer("");
    try {
      const resp = await askAI(question, engine);
      setAnswer(resp.data.answer);
    } catch {
      setAnswer("Error fetching answer.");
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>AI Chat</h2>
      <textarea value={question} onChange={e => setQuestion(e.target.value)} />
      <div>
        <select value={engine} onChange={e => setEngine(e.target.value)}>
          <option value="openai">OpenAI</option>
          <option value="gemini">Gemini</option>
          <option value="ollama">Ollama</option>
        </select>
        <button onClick={handleAsk} disabled={loading}>Ask</button>
      </div>
      {loading && <p>Loading...</p>}
      {answer && <div className="answer">{answer}</div>}
    </div>
  );
}
