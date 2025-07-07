// ~/Soap/frontend/src/ExportPanel.js

import React, { useState } from "react";
import axios from "axios";

export default function ExportPanel() {
  const [status, setStatus] = useState("");

  const handleExport = async () => {
    setStatus("Exporting...");
    try {
      await axios.get("/admin/export_vector_index");
      setStatus("Export started!");
    } catch {
      setStatus("Failed to export.");
    }
  };

  const handleImport = async () => {
    setStatus("Importing...");
    try {
      await axios.get("/admin/import_vector_index");
      setStatus("Import started!");
    } catch {
      setStatus("Failed to import.");
    }
  };

  return (
    <div>
      <h2>Export/Import Vector Data</h2>
      <button onClick={handleExport}>Export Vector Index</button>
      <button onClick={handleImport}>Import Vector Index</button>
      <div>{status}</div>
    </div>
  );
}
