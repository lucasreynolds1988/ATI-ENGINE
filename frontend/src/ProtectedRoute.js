// ~/Soap/frontend/src/ProtectedRoute.js

import React from "react";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ token, children }) {
  if (!token) {
    return <Navigate to="/login" />;
  }
  return children;
}
