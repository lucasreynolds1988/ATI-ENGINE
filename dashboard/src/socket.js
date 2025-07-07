import { io } from "socket.io-client";

const apiToken = localStorage.getItem("apiToken");
export const socket = io("http://localhost:5007", {
  auth: { token: apiToken }
});
