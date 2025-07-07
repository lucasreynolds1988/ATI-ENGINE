import React from "react";

function UploadStatus({ status }) {
  if (!status) return null;

  return (
    <div className="p-4">
      <h2 className="text-lg font-bold">Upload Status</h2>
      <pre className="bg-black text-green-400 p-2 mt-2 rounded">
        {JSON.stringify(status, null, 2)}
      </pre>
    </div>
  );
}

export default UploadStatus;
