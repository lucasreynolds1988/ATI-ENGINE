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
  const [token, setToken] = useState(localStorage.getItem("api_token") || "");

  const handleLogin = (newToken) => {
    setToken(newToken);
    localStorage.setItem("api_token", newToken);
  };

  return (
    <div
      className="App min-h-screen w-full flex flex-col"
      style={{
        background: "none", // Let index.css control the body!
        fontFamily: "'Inter', 'SF Pro Display', 'Roboto', Arial, sans-serif",
        minHeight: "100vh",
      }}
    >
      <div className="ai-pulse-bar" />
      <header
        className="w-full py-4 px-8 flex items-center justify-between shadow-md rounded-b-2xl"
        style={{
          background: "linear-gradient(120deg, #161b23 0%, #22262a 100%)",
          borderBottom: "2px solid #32aaff",
          boxShadow:
            "0 2px 16px 0 #32aaff44, 0 2px 8px 0 #0e213299",
          letterSpacing: "0.04em",
        }}
      >
        <div>
          <div
            className="text-2xl font-bold tracking-tight"
            style={{
              color: "#32aaff",
              textShadow: "0 1px 2px #23252799"
            }}
          >
            ATI{" "}
            <span
              className="font-light text-xl align-middle"
              style={{
                fontWeight: 400,
                color: "#32aaff"
              }}
            >
              Artificial Technician Intelligence
            </span>
          </div>
          <div
            className="font-medium"
            style={{
              color: "#32aaff",
              fontSize: "1rem",
              paddingLeft: 4
            }}
          >
            by ISC
          </div>
        </div>
        <div className="flex flex-col items-end">
          <span
            className="uppercase font-semibold text-xl tracking-wide"
            style={{
              color: "#32aaff",
              letterSpacing: "0.08em",
              textShadow: "0 1.5px 2px #232527cc, 0 2px 4px #868b8e99",
              fontWeight: 700,
              filter: "brightness(1.1)",
              fontFamily: "'Inter', 'SF Pro Display', 'Roboto', Arial, sans-serif",
            }}
          >
            MAINTENANCE DOC's
          </span>
        </div>
      </header>
      <Navbar token={token} />
      <div
        className="flex-1 w-full flex flex-col items-center justify-start"
        style={{
          minHeight: 0,
          width: "100%",
        }}
      >
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
    </div>
  );
}

export default App;
