// ~/Soap/frontend/src/SOPAdminReview.js

import React, { useState } from "react";
import axios from "axios";

function SOPAdminReview({ token }) {
  const [fileId, setFileId] = useState("");
  const [content, setContent] = useState("");

  const handleReview = async (e) => {
    e.preventDefault();
    try {
      const resp = await axios.get(
        `http://localhost:5003/final/${fileId}`,
        { headers: { "x-api-token": token } }
      );
      setContent(resp.data.content || "No content");
    } catch (err) {
      setContent("Error: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div>
      <h2>Admin SOP Review</h2>
      <form onSubmit={handleReview}>
        <input
          type="text"
          placeholder="Enter filename (without .final.txt)"
          value={fileId}
          onChange={e => setFileId(e.target.value)}
        />
        <button type="submit">Review</button>
      </form>
      <pre>{content}</pre>
    </div>
  );
}

export default SOPAdminReview;
