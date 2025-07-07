// ~/Soap/frontend/src/api.js

import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "";

// Legacy endpoints (keep for backwards compatibility)
export function getConfig(token) {
  return axios.get(`${BASE_URL}/config`, { headers: { "x-api-token": token } });
}

export function getLog(token) {
  return axios.get(`${BASE_URL}/log`, { headers: { "x-api-token": token }, responseType: "blob" });
}

export function getPipelineHistory(token) {
  return axios.get(`${BASE_URL}/pipeline/history`, { headers: { "x-api-token": token } });
}

export function getPipelineStatus(token, fileId) {
  return axios.get(`${BASE_URL}/pipeline/status/${fileId}`, { headers: { "x-api-token": token } });
}

export function runPipeline(token, fileId) {
  return axios.post(`${BASE_URL}/pipeline/run/${fileId}`, {}, { headers: { "x-api-token": token } });
}

export function getRoles(token) {
  return axios.get(`${BASE_URL}/roles`, { headers: { "x-api-token": token } });
}

export function getMetrics(token) {
  return axios.get(`${BASE_URL}/metrics`, { headers: { "x-api-token": token } });
}

export function getJobs(token) {
  return axios.get(`${BASE_URL}/pipeline/jobs`, { headers: { "x-api-token": token } });
}

// --- UNIVERSAL AI API ENDPOINTS (NEW) ---

// AI/SOP query (multi-engine)
export function askAI(question, engine = "openai") {
  return axios.post("/frontend/ask_ai", { question, engine });
}

// Manual upload (with FormData)
export function uploadManual(formData) {
  return axios.post("/manuals/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
}

// Feedback/correction
export function submitFeedback(data) {
  return axios.post("/feedback/submit", data);
}
