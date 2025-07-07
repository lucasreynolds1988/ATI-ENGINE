import React, { useState } from "react";
import axios from "axios";

export default function SearchJobs() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const apiToken = localStorage.getItem("apiToken");

  function search(e) {
    e.preventDefault();
    axios
      .get(`/pipeline/history?search=${encodeURIComponent(query)}`, {
        headers: { "X-API-Token": apiToken }
      })
      .then(r => setResults(r.data.lines || []));
  }

  return (
    <form onSubmit={search}>
      <h3>Search Pipeline Jobs</h3>
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Enter search term"
      />
      <button type="submit">Search</button>
      <pre>
        {results.map((r, i) => (
          <div key={i}>{r}</div>
        ))}
      </pre>
    </form>
  );
}
