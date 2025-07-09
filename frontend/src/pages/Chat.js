// ~/Soap/frontend/src/pages/Chat.js

import React, { useState } from "react";
import { askAI } from "../api";

function Chat() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSend = async () => {
    const res = await askAI(input);
    setResponse(res.data.response);
  };

  return (
    <div className="p-8">
      <h2>AI Chat</h2>
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={handleSend}>Send</button>
      <div className="mt-4">{response}</div>
    </div>
  );
}

export default Chat;
