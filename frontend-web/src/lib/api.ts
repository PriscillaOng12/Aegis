import axios from 'axios';

const API_BASE = process.env.API_BASE || 'http://localhost:8000';

export async function getAnalyticsSummary() {
  const res = await axios.get(`${API_BASE}/v1/analytics/summary`, {
    headers: { Authorization: 'Bearer dev-token' },
  });
  return res.data;
}

export async function sendIntervention(payload: { template_id: string; user_id: string; scheduled_for: string }) {
  const res = await axios.post(`${API_BASE}/v1/interventions/trigger`, payload, {
    headers: { Authorization: 'Bearer dev-token' },
  });
  return res.data;
}