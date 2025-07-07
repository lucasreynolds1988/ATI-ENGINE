// ~/Soap/frontend/src/FeedbackPanel.js

import React, { useState } from "react";
import { submitFeedback } from "./api";

export default function FeedbackPanel({ manualId, chunkIndex }) {
  const [feedback, setFeedback] = useState("");
  const [status, setStatus] = useState("");
  const [user, setUser] = useState("");

  const handleSubmit = async () => {
    setStatus("Submitting...");
    try {
      await submitFeedback({
        user,
        manual_id: manualId,
        chunk_index: chunkIndex,
        feedback,
        approved: false
      });
      setStatus("Thank you for your feedback!");
    } catch {
      setStatus("Error submitting feedback.");
    }
  };

  return (
    <div>
      <input
        placeholder="Your Name"
        value={user}
        onChange={e => setUser(e.target.value)}
      />
      <textarea
        placeholder="Suggest a correction, flag, or give feedback"
        value={feedback}
        onChange={e => setFeedback(e.target.value)}
      />
      <button onClick={handleSubmit}>Submit Feedback</button>
      {status && <div>{status}</div>}
    </div>
  );
}
