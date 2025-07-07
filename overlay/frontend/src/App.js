// ~/Soap/frontend/src/App.js

import React, { useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./Navbar";
import Dashboard from "./Dashboard";
import ManualUpload from "./ManualUpload";
import SOPGenerator from "./SOPGenerator";
import ScavengerBot from "./ScavengerBot";
import JobTable from "./JobTable";
import MetricsPanel from "./MetricsPanel";
import RoleDisplay from "./RoleDisplay";
import SOPAdminReview from "./SOPAdminReview";
import LiveFeed from "./LiveFeed";
import PipelineHistory from "./PipelineHistory";
import PipelineStatus from "./PipelineStatus";
import Login from "./Login";
import NotFound from "./NotFound";

function App() {
  // Store and share API token in state/context (could use context/provider for larger apps)
  const [token, setToken] = useState(localStorage.getItem("api_token") || "");

  const handleLogin = (newToken) => {
    setToken(newToken);
    localStorage.setItem("api_token", newToken);
  };

  return (
    <div className="App">
      <Navbar token={token} />
      <Routes>
        <Route path="/" element={<Dashboard token={token} />} />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/upload" element={<ManualUpload token={token} />} />
        <Route path="/sop" element={<SOPGenerator token={token} />} />
        <Route path="/scavenger" element={<ScavengerBot token={token} />} />
        <Route path="/jobs" element={<JobTable token={token} />} />
        <Route path="/metrics" element={<MetricsPanel token={token} />} />
        <Route path="/roles" element={<RoleDisplay token={token} />} />
        <Route path="/review" element={<SOPAdminReview token={token} />} />
        <Route path="/live" element={<LiveFeed token={token} />} />
        <Route path="/history" element={<PipelineHistory token={token} />} />
        <Route path="/status/:fileId" element={<PipelineStatus token={token} />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
}

export default App;
