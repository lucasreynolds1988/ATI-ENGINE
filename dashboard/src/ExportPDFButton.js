import React from "react";

export default function ExportPDFButton({ jobId }) {
  const apiToken = localStorage.getItem("apiToken");
  function downloadPDF() {
    window.open(`/jobpdf/${jobId}?token=${apiToken}`);
  }
  return (
    <button onClick={downloadPDF}>Export PDF</button>
  );
}
