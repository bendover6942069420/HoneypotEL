# HONEYPOT-EL: Medium Interaction Honeypot

A sophisticated medium-interaction honeypot designed to simulate a login page, track intrusion attempts, and provide detailed analytics. Built with Python, Flask, and Dash, it offers real-time monitoring and robust security features.

## Project Overview

HONEYPOT-EL simulates a realistic login page to attract and analyze unauthorized access attempts. It logs detailed information about attackers, provides real-time analytics through a dashboard, and sends alerts for suspicious activity. The system is safe, never allowing actual access, and is designed for easy deployment and monitoring.

## Key Components

### 1. Main Application (`app.py`)
- **Framework**: Flask
- **Features**:
  - Fake login page that rejects all login attempts
  - Rate limiting: 5 attempts/minute, 100 attempts/hour
  - Geolocation tracking of attackers
  - User agent analysis for identifying bots and browsers
  - Email alerts for suspicious activity (triggered after 3 attempts from the same IP)
  - Comprehensive logging of all attempts

### 2. Analytics Dashboard (`dashboard.py`)
- **Framework**: Dash and Plotly
- **Features**:
  - Real-time visualizations updated every 30 seconds
  - Displays:
    - Total login attempts
    - Unique IP addresses
    - Most common usernames
    - Geographic distribution of attacks (world map)
    - Time-based attack trends
    - User agent statistics

### 3. Frontend Components
- **Login Page** (`templates/login.html`):
  - Professional, responsive login interface
  - Username and password fields with error messaging
  - Styled to mimic a legitimate system
- **Styling** (`static/css/`):
  - `style.css`: Clean, responsive design for the login page
  - `dashboard.css`: Grid-based, card-styled layout for the analytics dashboard

### 4. Configuration
- **File**: `.env`
- **Settings**:
  - Email configuration for alerts
  - API keys for geolocation services
  - Flask secret key
  - Customizable for different deployment environments

### 5. Dependencies (`requirements.txt`)
- Key packages:
  - Flask and extensions (`flask-limiter`, `flask-mail`)
  - Dash and Plotly for analytics
  - Pandas for data processing
  - Requests for API calls
  - User-agents for browser fingerprinting

## How It Works

### 1. Attack Detection
- Attackers encounter a professional-looking login page at `http://localhost:8080/`.
- Every login attempt is logged with:
  - Timestamp
  - IP address
  - Username and password attempted
  - Geolocation data
  - Browser/User Agent details
  - Full request headers

### 2. Security Features
- **Rate Limiting**: Prevents brute-force attacks
- **Geolocation**: Maps attacker origins
- **User Agent Analysis**: Identifies automated scripts vs. human attackers
- **Email Alerts**: Notifies administrators of suspicious activity
- **Logging**: Stores detailed records in `honeypot.log`

### 3. Monitoring and Analysis
- **Analytics Dashboard** (`http://localhost:8080/dashboard/`):
  - Visualizes attack patterns in real time
  - Shows geographic distribution, common usernames, and browser statistics
  - Tracks total attempts and unique attackers
- **Log File**: `honeypot.log` provides raw data for further analysis

## Access Points
- **Login Page**: `http://localhost:8080/`
- **Analytics Dashboard**: `http://localhost:8080/dashboard/`
- **Log File**: `honeypot.log`

## Design Principles
HONEYPOT-EL is:
- **Realistic**: Engages attackers with a convincing interface
- **Secure**: Never allows actual access
- **Informative**: Collects comprehensive attack data
- **Monitorable**: Provides real-time insights via dashboard
- **Alerting**: Notifies administrators of suspicious patterns

## Getting Started
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure the `.env` file with your settings.
4. Run the application: `python app.py`
5. Access the login page at `http://localhost:8080/` and the dashboard at `http://localhost:8080/dashboard/`.

---

**Note**: Ensure proper configuration of API keys and email settings for full functionality. For deployment, adjust rate limits and alerting thresholds as needed.
