// ~/Soap/frontend/src/ErrorBoundary.js

import React from "react";

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, info) {
    // You could log this error to a server here
    // console.error(error, info);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="section-card" style={{ color: "#c21825" }}>
          <h2>Something went wrong.</h2>
          <pre>{this.state.error && this.state.error.toString()}</pre>
        </div>
      );
    }
    return this.props.children;
  }
}
