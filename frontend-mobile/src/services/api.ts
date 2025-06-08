import axios from 'axios';

const API_BASE = process.env.EXPO_PUBLIC_API_BASE || 'http://localhost:8000';

/**
 * Axios instance configured with base URL and interceptors.
 * TODO: inject auth tokens from secure storage.
 */
export const api = axios.create({
  baseURL: `${API_BASE}/v1`,
});

// Example API methods
export async function logSymptom(entry: {
  pain: number;
  fatigue: number;
  nausea: number;
  notes: string;
  timestamp: string;
}) {
  const res = await api.post('/symptoms', entry, {
    headers: { Authorization: `Bearer dev-token` },
  });
  return res.data;
}

export async function getLatestRisk() {
  const res = await api.get('/risk/latest', {
    headers: { Authorization: `Bearer dev-token` },
  });
  return res.data;
}