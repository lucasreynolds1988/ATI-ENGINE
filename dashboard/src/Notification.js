import React, { useEffect, useState } from "react";
import { socket } from "./socket";

export default function Notification() {
  const [noti, setNoti] = useState("");

  useEffect(() => {
    socket.on("eventlog", data => {
      if (data.lines && data.lines.length)
        setNoti("New pipeline event: " + data.lines[data.lines.length - 1]);
    });
    return () => socket.disconnect();
  }, []);

  if (!noti) return null;
  return (
    <div style={{ background: "#ffd", border: "1px solid #a90", padding: 10 }}>
      <b>{noti}</b>
    </div>
  );
}
