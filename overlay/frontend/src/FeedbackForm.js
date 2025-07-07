// ~/Soap/frontend/src/FeedbackForm.js

import React, { useState } from "react";
import axios from "axios";

function FeedbackForm({ token }) {
  const [msg, setMsg] = useState("");
  const [status, setStatus] = useState("");

  const handleSubmit = async e => {
    e.preventDefault();
    if (!msg.trim()) return;
    try {
      await axios.post(
        "http://localhost:5003/feedback",
        { message: msg },
        { headers: { "x-api-token": token } }
      );
      setStatus("Feedback submitted. Thank you!");
      setMsg("");
    } catch (err) {
      setStatus("Submission failed: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="section-card">
      <h2>Submit Feedback</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          rows={5}
          style={{ width: "100%", padding: 10, borderRadius: 8, border: "1px solid #c2d3dc" }}
          placeholder="Your feedback or suggestion..."
          value={msg}
          onChange={e => setMsg(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
      {status && <div>{status}</div>}
    </div>
  );
}
export default FeedbackForm;

