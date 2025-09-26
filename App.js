import React, { useState, useEffect } from 'react';
import AlertsChart from './AlertsChart';

const initialAlerts = [
  {
    id: 'a1',
    ip: '81.2.69.142',
    timestamp: '2025-09-26T03:10:15Z',
    country: 'United Kingdom',
    city: 'London',
    device: 'Desktop',
    os: 'Windows 10',
    browser: 'Chrome 115',
    rtt: 120,
    riskLevel: 'High',
    isAttack: true,
    reason: 'Login from a known malicious IP address and unusual location for this user.'
  },
  {
    id: 'a4',
    ip: '47.91.68.231',
    timestamp: '2025-09-26T03:08:40Z',
    country: 'Norway',
    city: 'Oslo',
    device: 'Desktop',
    os: 'macOS',
    browser: 'Safari 16.5',
    rtt: 15,
    riskLevel: 'Low',
    isAttack: false,
    reason: 'Typical login from a recognized device and location.'
  }
];

const Header = () => (
  <header className="header">
    <h1>Cyberattack Detection System</h1>
    <div className="status-indicator">
      <div className="dot"></div>
      <span>Real-time Monitoring</span>
    </div>
  </header>
);

const KeyMetrics = ({ alerts }) => {
  const totalLogins = 53201 + alerts.length - initialAlerts.length;
  const suspiciousCount = alerts.filter(a => a.riskLevel !== 'Low').length;
  const accountsAtRisk = alerts.filter(a => a.isAttack).length;

  return (
    <div className="key-metrics-card">
      <div className="metric-item">
        <h3>Total Logins (24h)</h3>
        <div className="value">{totalLogins.toLocaleString()}</div>
      </div>
      <div className="metric-item">
        <h3>Suspicious Activity</h3>
        <div className="value">{suspiciousCount}</div>
      </div>
      <div className="metric-item">
        <h3>Accounts At Risk</h3>
        <div className="value" style={{ color: 'var(--red-accent)' }}>{accountsAtRisk}</div>
      </div>
    </div>
  );
};

const AlertsFeed = ({ alerts, onSelectAlert, selectedAlert }) => (
  <div className="dashboard-card alerts-feed">
    <h2>Real-time Alerts</h2>
    <div className="alerts-list">
      {alerts.map(alert => (
        <div 
          key={alert.id} 
          className={`alert-item ${selectedAlert?.id === alert.id ? 'selected' : ''}`}
          onClick={() => onSelectAlert(alert)}
        >
          <div className="alert-info">
            <div className="ip">{alert.ip}</div>
            <div className="location">{`${alert.city}, ${alert.country}`}</div>
          </div>
          <div className={`risk-level ${alert.riskLevel}`}>{alert.riskLevel}</div>
        </div>
      ))}
    </div>
  </div>
);

const AlertDetails = ({ alert }) => {
  if (!alert) {
    return (
      <div className="dashboard-card alert-details" style={{ display: 'grid', placeContent: 'center' }}>
        <p>Select an alert to view details</p>
      </div>
    );
  }

  return (
    <div className="dashboard-card alert-details">
      <h2>Alert Details: {alert.ip}</h2>
      <div className="detail-grid">
        <div className="detail-item"><strong>Geolocation</strong> {`${alert.city}, ${alert.country}`}</div>
        <div className="detail-item"><strong>Device Type</strong> {alert.device}</div>
        <div className="detail-item"><strong>Operating System</strong> {alert.os}</div>
        <div className="detail-item"><strong>Browser</strong> {alert.browser}</div>
        <div className="detail-item"><strong>Round-Trip Time</strong> {alert.rtt} ms</div>
        <div className="detail-item"><strong>Timestamp</strong> {new Date(alert.timestamp).toLocaleString()}</div>
        <div className="detail-item" style={{ gridColumn: 'span 2' }}>
          <strong>Risk Analysis</strong>
          <span style={{ color: alert.isAttack ? 'var(--red-accent)' : 'var(--lightest-slate)'}}>
            {alert.reason}
          </span>
        </div>
      </div>
    </div>
  );
};

function App() {
  const [alerts, setAlerts] = useState(initialAlerts);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [chartData, setChartData] = useState([]);

  // THIS useEffect IS NOW CORRECTLY INSIDE THE APP FUNCTION
  useEffect(() => {
    const interval = setInterval(() => {
      const alertCount = Math.floor(Math.random() * 4) + 1;
      const newAlerts = [];
      for (let i = 0; i < alertCount; i++) {
        newAlerts.push({
          id: `a${Date.now() + i}`,
          ip: '203.0.113.' + Math.floor(Math.random() * 255),
          timestamp: new Date().toISOString(),
          country: 'Japan',
          city: 'Tokyo',
          device: 'Mobile',
          os: 'iOS 17',
          browser: 'Safari 17.0',
          rtt: 150 + Math.floor(Math.random() * 50),
          riskLevel: 'Medium',
          isAttack: false,
          reason: 'Suspicious login from a new device for this user account.'
        });
      }
      setAlerts(currentAlerts => [...newAlerts, ...currentAlerts]);
    }, 5000); 
    return () => clearInterval(interval);
  }, []); 

  // THIS useEffect IS ALSO CORRECTLY INSIDE THE APP FUNCTION
  useEffect(() => {
    const processDataForChart = () => {
      const now = Date.now();
      const fiveMinutesAgo = now - 5 * 60 * 1000;
      const recentAlerts = alerts.filter(a => new Date(a.timestamp).getTime() > fiveMinutesAgo);
      const groupedData = recentAlerts.reduce((acc, alert) => {
        const alertTime = new Date(alert.timestamp);
        const timeKey = `${alertTime.getHours()}:${alertTime.getMinutes()}:${String(alertTime.getSeconds()).padStart(2,'0')}`;
        if (!acc[timeKey]) {
          acc[timeKey] = { time: timeKey, alerts: 0 };
        }
        acc[timeKey].alerts++;
        return acc;
      }, {});
      const sortedChartData = Object.values(groupedData).sort((a, b) => a.time.localeCompare(b.time));
      setChartData(sortedChartData);
    };
    processDataForChart();
  }, [alerts]);

  // THIS useEffect IS ALSO CORRECTLY INSIDE THE APP FUNCTION
  useEffect(() => {
    if (!selectedAlert && alerts.length > 0) {
      const highPriorityAlert = alerts.find(a => a.riskLevel === 'High');
      setSelectedAlert(highPriorityAlert || alerts[0]);
    }
  }, [alerts, selectedAlert]);


  return (
    <div className="app-container">
      <Header />
      <div className="dashboard-grid">
        <div className="key-metrics-card" style={{ gridColumn: 'span 12' }}>
          <KeyMetrics alerts={alerts} />
        </div>
        
        <div className="dashboard-card" style={{ gridColumn: 'span 12', gridRow: '2', minHeight: '300px' }}>
            <h2 style={{marginTop: 0}}>Alerts Over Time</h2>
            <AlertsChart data={chartData} />
        </div>
        
        <AlertsFeed 
          alerts={alerts} 
          selectedAlert={selectedAlert}
          onSelectAlert={setSelectedAlert} 
        />

        <AlertDetails alert={selectedAlert} />
      </div>
    </div>
  );
}

export default App;