import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./Login";
import Dashboard from "./Dashboard";
import JobDetail from "./JobDetail";
import ErrorBoundary from "./ErrorBoundary";
import JobTable from "./JobTable";
import RoleDisplay from "./RoleDisplay";
import MetricsPanel from "./MetricsPanel";
import LiveFeed from "./LiveFeed";

export default function App() {
  return (
    <BrowserRouter>
      <ErrorBoundary>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Login />
                <RoleDisplay />
                <MetricsPanel />
                <JobTable />
                <LiveFeed />
              </>
            }
          />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/job/:jobId" element={<JobDetail />} />
        </Routes>
      </ErrorBoundary>
    </BrowserRouter>
  );
}
