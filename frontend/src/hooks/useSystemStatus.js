import { useEffect, useState } from "react";
import axios from "axios";

export default function useSystemStatus(token) {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    if (!token) return;
    const id = setInterval(() => {
      axios
        .get("/config", { headers: { "x-api-token": token } })
        .then((res) => setStatus(res.data))
        .catch(() => setStatus(null));
    }, 8000);
    return () => clearInterval(id);
  }, [token]);

  return status;
}
