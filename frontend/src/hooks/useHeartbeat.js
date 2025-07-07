import { useEffect, useState } from "react";

export default function useHeartbeat(interval = 4000) {
  const [active, setActive] = useState(true);

  useEffect(() => {
    const id = setInterval(() => {
      setActive((prev) => !prev);
    }, interval);
    return () => clearInterval(id);
  }, [interval]);

  return active;
}
