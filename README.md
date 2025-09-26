##🔐 Suspicious Login Detector

A real-time intelligent system to detect suspicious login activities using behavioral patterns, geolocation analysis, and risk scoring.

Designed for cybersecurity teams, IT admins, and developers who want to proactively monitor and respond to anomalous login behavior.

##📌 Project Overview

This project aims to identify and alert on potentially malicious login attempts by analyzing:

#📈 Login frequency

#🌍 Geolocation inconsistencies

#💻 Device fingerprint mismatches

#🕒 Time-based anomalies (e.g., late-night logins)

It includes:

✅ Real-time dynamic dashboard for monitoring

✅ Detailed alert views for investigation

⚙️ How It Works

The system performs the following tasks:

##🔴 Live Alerts Feed
Displays suspicious login attempts as they occur, with risk levels: High, Medium, Low.

📊 Dashboard Cards
Summarizes key metrics like:

Total login attempts

Number of suspicious events

Accounts at risk

🕵️ Detailed Alert View
Shows:

IP address

Geolocation

Device fingerprint

Timestamp

Risk analysis for each flagged login

📉 Risk Scoring Engine
Assigns a risk level based on:

Location deviation

Login time anomaly

Device change/fingerprint mismatch

✅ Benefits

⚡ Real-Time Detection: Immediate alerts for suspicious activity

🌐 Geolocation Awareness: Flags logins from unexpected regions

🧠 Behavioral Analysis: Detects unusual patterns (e.g., rapid login bursts)

🏗️ Scalable Design: Easily integrates with existing authentication systems

📈 User-Friendly Dashboard: Visual insights for fast decision-making

🥇 Why This Project Stands Out
Feature	This Project	Others
Real-time dashboard	✅	❌
Risk scoring engine	✅	❌
Device fingerprinting	✅	Limited
Alert detail view	✅	❌
Open-source & customizable	✅	❌
🔧 Customizable

Built with modular components for easy extension

🔍 Transparent

Fully open-source with clear logic and data flow

🚨 Focused on Actionability

Alerts are designed to be actionable, not just informative

📖 User Manual
🛠️ Setup
git clone https://github.com/shivamgupta79/suspicious-login-detector.git
cd suspicious-login-detector
npm install
npm start

📊 Dashboard Overview

Live Alerts: View new suspicious logins with risk levels

Metrics Cards: See total logins, flagged events, and accounts at risk

Alert Details: Click any alert to view:

IP address

Geolocation

Device info

Timestamp

⚠️ Responding to Alerts

Investigate high-risk logins immediately

Use geolocation and device fingerprint to verify legitimacy

Integrate with email or SMS alerting systems (optional)

🧪 Testing

Simulate logins from different IPs, times, and devices

Observe dashboard updates and real-time alert generation

📬 Contributing

Pull requests are welcome! For major changes, please open an issue
 first to discuss your proposed changes.
