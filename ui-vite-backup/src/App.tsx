import React from "react";

export default function App() {
  return (
    <div style={{fontFamily:"system-ui, sans-serif", padding: 24}}>
      <h1>Living Truth Engine</h1>
      <p>Phase 9.4.0 UI Shell (placeholder). Static app served behind single origin.</p>
      <ul>
        <li><a href="/api/health" target="_blank" rel="noreferrer">/api/health</a></li>
        <li><a href="/api/health/full" target="_blank" rel="noreferrer">/api/health/full</a></li>
        <li><a href="/api/models" target="_blank" rel="noreferrer">/api/models</a></li>
      </ul>
      <p>Graph and analysis pages will be plugged in during the UI rebuild phase.</p>
    </div>
  );
}
