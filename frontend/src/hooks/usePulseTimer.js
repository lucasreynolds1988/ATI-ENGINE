import { useEffect, useState } from "react";

export default function usePulseTimer(interval = 4000) {
  const [tick, setTick] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setTick((prev) => prev + 1), interval);
    return () => clearInterval(id);
  }, [interval]);

  return tick;
}
