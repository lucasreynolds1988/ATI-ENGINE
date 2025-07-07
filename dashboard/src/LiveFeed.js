import React, { useEffect, useState } from "react";
import { socket } from "./socket";

export default function LiveFeed() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    socket.on("eventlog", data => {
      setEvents(events => [...events, ...(data.lines || [])]);
    });
    socket.emit("subscribe", {});
    return () => socket.disconnect();
  }, []);

  return (
    <div>
      <h3>Live Event Feed</h3>
      <pre style={{ maxHeight: 200, overflow: "auto" }}>
        {events.map((e, i) => (
          <div key={i}>{e}</div>
        ))}
      </pre>
    </div>
  );
}
