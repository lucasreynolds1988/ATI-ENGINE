// ~/Soap/frontend/src/ApproveFeedbackPanel.js

import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ApproveFeedbackPanel() {
  const [feedbacks, setFeedbacks] = useState([]);
  useEffect(() => {
    axios.get("/admin/feedback").then(resp => setFeedbacks(resp.data));
  }, []);
  const approve = id => {
    axios.post("/admin/approve_feedback", { feedback_id: id }).then(() =>
      setFeedbacks(f => f.filter(feedback => feedback._id !== id))
    );
  };
  return (
    <div>
      <h2>User Feedback</h2>
      <ul>
        {feedbacks.map(f => (
          <li key={f._id}>
            {f.feedback} by {f.user}
            <button onClick={() => approve(f._id)}>Approve</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
