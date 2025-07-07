// ~/Soap/frontend/src/PrivateRoute.js

import React from "react";
import { Navigate } from "react-router-dom";

// Usage: <PrivateRoute token={token}><SomeComponent /></PrivateRoute>
export default function PrivateRoute({ token, children }) {
  if (!token) {
    return <Navigate to="/login" />;
  }
  return children;
}
