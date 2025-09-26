🔐 Suspicious Login Detector
A real-time intelligent system to detect suspicious login activities using behavioral patterns, geolocation analysis, and risk scoring. Designed for cybersecurity teams, IT admins, and developers who want to proactively monitor and respond to anomalous login behavior.

📌 Project Overview
This project aims to identify and alert on potentially malicious login attempts by analyzing:

Login frequency

Geolocation inconsistencies

Device fingerprint mismatches

Time-based anomalies (e.g., late-night logins)

It provides a dynamic dashboard for real-time monitoring and detailed alert views for investigation.

⚙️ How It Works
The system performs the following tasks:

Live Alerts Feed: Displays suspicious login attempts as they occur, with risk levels (High, Medium, Low).

Dashboard Cards: Summarizes key metrics like total logins, number of suspicious events, and accounts at risk.

Detailed Alert View: Shows IP address, geolocation, device fingerprint, and risk analysis for each flagged login.

Risk Scoring Engine: Assigns a risk level based on multiple factors including location deviation, login time, and device changes.

✅ Benefits
Real-Time Detection: Immediate alerts for suspicious activity.

Geolocation Awareness: Flags logins from unexpected regions.

Behavioral Analysis: Detects unusual patterns like rapid logins or off-hours access.

Scalable Design: Easily integrates with existing authentication systems.

User-Friendly Dashboard: Visual insights for quick decision-making.

🥇 Why This Project Stands Out
Compared to other login detection tools, this project offers:

Feature	This Project	Others
Real-time dashboard	✅	❌
Risk scoring engine	✅	❌
Device fingerprinting	✅	Limited
Alert detail view	✅	❌
Open-source & customizable	✅	❌
Customizable: Built with modular components for easy extension.

Transparent: Fully open-source with clear logic and data flow.

Focused on Actionability: Alerts are designed to be actionable, not just informative.

📖 User Manual
🛠️ Setup
bash
git clone https://github.com/shivamgupta79/suspicious-login-detector.git
cd suspicious-login-detector
npm install
npm start
📊 Dashboard Overview
Live Alerts: View new suspicious logins with risk levels.

Metrics Cards: See total logins, flagged events, and active risks.

Alert Details: Click any alert to view IP, location, device, and timestamp.

⚠️ Responding to Alerts
Investigate high-risk logins immediately.

Use geolocation and device info to verify legitimacy.

Optionally integrate with email or SMS alerting systems.

🧪 Testing
Simulate logins from different IPs and times.

Observe dashboard updates and alert generation.

📬 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.
