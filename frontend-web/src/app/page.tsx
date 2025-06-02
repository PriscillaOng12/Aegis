'use client';
import React, { useEffect, useState } from 'react';
import { sendIntervention, getAnalyticsSummary } from '../lib/api';

interface Summary {
  adherence: number;
  false_alert_rate: number;
  median_lead_time_hours: number;
  active_users: number;
}

export default function HomePage() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [templateId, setTemplateId] = useState('nudge_hydration');
  const [userId, setUserId] = useState('');
  const [scheduledFor, setScheduledFor] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    async function fetchSummary() {
      const data = await getAnalyticsSummary();
      setSummary(data);
    }
    fetchSummary();
  }, []);

  async function triggerIntervention() {
    try {
      await sendIntervention({ template_id: templateId, user_id: userId, scheduled_for: scheduledFor });
      setMessage('Intervention triggered');
    } catch (err) {
      console.error(err);
      setMessage('Failed to trigger');
    }
  }

  return (
    <main style={{ padding: '2rem' }}>
      <h1>Aegis Health – Clinician Dashboard</h1>
      {summary ? (
        <div>
          <p><strong>Adherence:</strong> {(summary.adherence * 100).toFixed(1)}%</p>
          <p><strong>False alert rate:</strong> {(summary.false_alert_rate * 100).toFixed(1)}%</p>
          <p><strong>Median lead time:</strong> {summary.median_lead_time_hours.toFixed(1)} h</p>
          <p><strong>Active users:</strong> {summary.active_users}</p>
        </div>
      ) : (
        <p>Loading summary...</p>
      )}
      <h2>Trigger Manual Intervention</h2>
      <form onSubmit={(e) => { e.preventDefault(); triggerIntervention(); }}>
        <label>
          Template ID:
          <input type="text" value={templateId} onChange={(e) => setTemplateId(e.target.value)} />
        </label>
        <br />
        <label>
          User ID:
          <input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} />
        </label>
        <br />
        <label>
          Scheduled For (ISO datetime):
          <input type="text" value={scheduledFor} onChange={(e) => setScheduledFor(e.target.value)} />
        </label>
        <br />
        <button type="submit">Send</button>
      </form>
      {message && <p>{message}</p>}
    </main>
  );
}