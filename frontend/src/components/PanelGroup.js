import React from "react";

function PanelGroup({ panels }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {panels.map((panel, i) => (
        <div key={i} className="card">
          <h3 className="text-xl mb-2">{panel.title}</h3>
          {panel.body}
        </div>
      ))}
    </div>
  );
}

export default PanelGroup;
