const express = require('express');
const cors = require('cors');
const app = express();

app.use(express.json());
app.use(cors());

let events = []; 
let alerts = [];


class DetectionEngine {
    detectFailedLogins(username) {
        
        const tenMinutesAgo = new Date(Date.now() - 10 * 60 * 1000);
        const recentFailed = events.filter(event => 
            event.username === username && 
            !event.success && 
            new Date(event.timestamp) > tenMinutesAgo
        );
        
        if (recentFailed.length >= 3) {
            return {
                type: 'failed_login',
                message: `${username} has ${recentFailed.length} failed logins in 10 minutes`,
                riskLevel: 'HIGH'
            };
        }
        return null;
    }
    
    detectGeographicAnomaly(username, country) {
        const lastSuccess = events
            .filter(event => event.username === username && event.success)
            .pop();
            
        if (lastSuccess && lastSuccess.country !== country) {
            const timeDiff = (Date.now() - new Date(lastSuccess.timestamp)) / (1000 * 60 * 60); // hours
            if (timeDiff < 2) {
                return {
                    type: 'geographic_anomaly',
                    message: `${username} traveled from ${lastSuccess.country} to ${country} in ${timeDiff.toFixed(1)} hours`,
                    riskLevel: 'HIGH'
                };
            }
        }
        return null;
    }
    
    detectOffHours(username) {
        const hour = new Date().getHours();
        if (hour < 9 || hour > 18) {
            return {
                type: 'off_hours',
                message: `${username} logged in at ${hour}:00 (outside business hours)`,
                riskLevel: 'MEDIUM'
            };
        }
        return null;
    }
    
    analyzeEvent(event) {
        const detectedAlerts = [];
        
        if (!event.success) {
            const failedAlert = this.detectFailedLogins(event.username);
            if (failedAlert) detectedAlerts.push(failedAlert);
        } else {
            const geoAlert = this.detectGeographicAnomaly(event.username, event.country);
            if (geoAlert) detectedAlerts.push(geoAlert);
            
            const timeAlert = this.detectOffHours(event.username);
            if (timeAlert) detectedAlerts.push(timeAlert);
        }
        
        return detectedAlerts;
    }
}

const detector = new DetectionEngine();

function generateSampleEvent() {
    const usernames = ['alice', 'bob', 'charlie', 'diana', 'eve'];
    const countries = ['USA', 'UK', 'Germany', 'Japan', 'Australia'];
    const ips = ['192.168.1', '10.0.0', '172.16.1'];
    
    const suspicious = Math.random() < 0.3; 
    
    return {
        id: events.length + 1,
        username: usernames[Math.floor(Math.random() * usernames.length)],
        ipAddress: `${ips[Math.floor(Math.random() * ips.length)]}.${Math.floor(Math.random() * 254) + 1}`,
        country: countries[Math.floor(Math.random() * countries.length)],
        timestamp: new Date().toISOString(),
        success: suspicious ? Math.random() > 0.6 : true,
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    };
}

app.get('/', (req, res) => {
    res.json({
        message: 'Cyberattack Detection System API',
        status: 'running',
        endpoints: {
            'GET /api/events': 'Get recent login events',
            'GET /api/alerts': 'Get security alerts',
            'GET /api/stats': 'Get system statistics',
            'POST /api/events': 'Add new login event'
        },
        stats: {
            totalEvents: events.length,
            totalAlerts: alerts.length,
            timestamp: new Date().toISOString()
        }
    });
});

app.get('/api/events', (req, res) => {
    const limit = parseInt(req.query.limit) || 20;
    const recentEvents = events.slice(-limit).reverse();
    
    res.json({
        events: recentEvents,
        total: events.length
    });
});

app.get('/api/alerts', (req, res) => {
    const limit = parseInt(req.query.limit) || 10;
    const recentAlerts = alerts.slice(-limit).reverse();
    
    res.json({
        alerts: recentAlerts,
        total: alerts.length
    });
});

app.post('/api/events', (req, res) => {
    const { username, ipAddress, country, success } = req.body;
    
    if (!username) {
        return res.status(400).json({ error: 'Username is required' });
    }
    
    const event = {
        id: events.length + 1,
        username,
        ipAddress: ipAddress || '192.168.1.100',
        country: country || 'USA',
        timestamp: new Date().toISOString(),
        success: success !== undefined ? success : true,
        userAgent: req.headers['user-agent'] || 'Unknown'
    };
    

    events.push(event);
    

    const detectedAlerts = detector.analyzeEvent(event);
    
    
    detectedAlerts.forEach(alert => {
        const alertData = {
            id: alerts.length + 1,
            eventId: event.id,
            username: event.username,
            type: alert.type,
            message: alert.message,
            riskLevel: alert.riskLevel,
            timestamp: new Date().toISOString()
        };
        alerts.push(alertData);
    });
    
    res.json({
        event,
        alerts: detectedAlerts,
        message: detectedAlerts.length > 0 ? 'Threats detected!' : 'Event processed'
    });
});

app.get('/api/stats', (req, res) => {
    const totalEvents = events.length;
    const failedLogins = events.filter(e => !e.success).length;
    const successfulLogins = totalEvents - failedLogins;
    const totalAlerts = alerts.length;
    
    const highRiskAlerts = alerts.filter(a => a.riskLevel === 'HIGH').length;
    const mediumRiskAlerts = alerts.filter(a => a.riskLevel === 'MEDIUM').length;
    
    
    const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000);
    const recentActivity = events.filter(e => new Date(e.timestamp) > oneHourAgo).length;
    
    res.json({
        events: {
            total: totalEvents,
            successful: successfulLogins,
            failed: failedLogins,
            recentActivity
        },
        alerts: {
            total: totalAlerts,
            high: highRiskAlerts,
            medium: mediumRiskAlerts,
            low: totalAlerts - highRiskAlerts - mediumRiskAlerts
        },
        timestamp: new Date().toISOString()
    });
});

function startEventGenerator() {
    setInterval(() => {
        const event = generateSampleEvent();
        events.push(event);
        
       
        const detectedAlerts = detector.analyzeEvent(event);
        detectedAlerts.forEach(alert => {
            const alertData = {
                id: alerts.length + 1,
                eventId: event.id,
                username: event.username,
                type: alert.type,
                message: alert.message,
                riskLevel: alert.riskLevel,
                timestamp: new Date().toISOString()
            };
            alerts.push(alertData);
            console.log(`ALERT: ${alert.message}`);
        });
        
        console.log(`Event: ${event.username} from ${event.country} - ${event.success ? 'SUCCESS' : 'FAILED'}`);
        
        if (events.length > 100) events.shift();
        if (alerts.length > 50) alerts.shift();
        
    }, Math.random() * 5000 + 2000); 
}

const PORT = process.env.PORT || 6000;

app.listen(PORT, () => {
    console.log(`Cyberattack Detection API running on port ${PORT}`);
    console.log(`Access API at: http://localhost:${PORT}`);
    console.log('Endpoints:');
    console.log('   GET  / - API info');
    console.log('   GET  /api/events - Recent events');
    console.log('   GET  /api/alerts - Security alerts');
    console.log('   GET  /api/stats - Statistics');
    console.log('   POST /api/events - Add event');
    
    startEventGenerator();
});