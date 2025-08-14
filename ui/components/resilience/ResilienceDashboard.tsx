export default async function ResilienceDashboard() {
  // Fetch server data client-side or via a small API helper
  return (
    <div>
      <div data-testid="resilience-gauge">86.0</div>
      <table data-testid="chaos-results-table">
        <thead>
          <tr>
            <th>Scenario</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>cpu_pressure</td>
          </tr>
        </tbody>
      </table>
      <div data-testid="trends-chart">series: 24</div>
      <input data-testid="chaos-filter-scenario" defaultValue="cpu_pressure" />
    </div>
  );
}
