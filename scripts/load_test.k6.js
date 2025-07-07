import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
};

const BASE_URL = __ENV.API_BASE || 'http://localhost:8000';
const TOKEN = 'dev-token';

export default function () {
  // log symptom
  const payload = JSON.stringify({
    pain: Math.floor(Math.random() * 11),
    fatigue: Math.floor(Math.random() * 11),
    nausea: Math.floor(Math.random() * 11),
    notes: 'load test',
    timestamp: new Date().toISOString(),
  });
  const headers = { 'Content-Type': 'application/json', Authorization: `Bearer ${TOKEN}` };
  let res = http.post(`${BASE_URL}/v1/symptoms`, payload, { headers });
  check(res, { 'symptom created': (r) => r.status === 201 });

  // get risk
  res = http.get(`${BASE_URL}/v1/risk/latest`, { headers });
  check(res, { 'risk ok': (r) => r.status === 200 });

  // sync wearables
  const snapshots = [];
  for (let i = 0; i < 2; i++) {
    snapshots.push({
      timestamp: new Date().toISOString(),
      hr: 60 + Math.random() * 10,
      hrv: 40 + Math.random() * 20,
      steps: Math.random() * 100,
      sleep: 0,
    });
  }
  res = http.post(`${BASE_URL}/v1/wearables/sync`, JSON.stringify({ source: 'mock', snapshots }), { headers });
  check(res, { 'wearable accepted': (r) => r.status === 202 });

  sleep(1);
}