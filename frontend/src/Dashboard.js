// ~/Soap/frontend/src/Dashboard.js

import React from "react";
import MetricsPanel from "./MetricsPanel";
import JobTable from "./JobTable";
import LiveFeed from "./LiveFeed";

function Dashboard({ token }) {
  return (
    <div>
      <h1>ATI Oracle Engine Dashboard</h1>
      <MetricsPanel token={token} />
      <h2>Recent Jobs</h2>
      <JobTable token={token} limit={5} />
      <LiveFeed token={token} />
    </div>
  );
}

export default Dashboard;
