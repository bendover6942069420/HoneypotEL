# HONEYPOT-EL: Medium Interaction Honeypot Demonstration Guide

This guide explains the components of the HONEYPOT-EL project and provides a step-by-step demonstration of its functionality. HONEYPOT-EL is a medium-interaction honeypot built with Python, Flask, and Dash to simulate a login page, track intrusion attempts, and visualize attack data in real-time.

## Project Components

### 1. Main Application (`app.py`)
- **Purpose**: Core honeypot functionality
- **Features**:
  - Handles login page routing
  - Logs attack attempts
  - Tracks IP geolocation
  - Enforces rate limiting (5 attempts/minute)
  - Sends email alerts for suspicious activity
  - Integrates with the analytics dashboard

### 2. Analytics Dashboard (`dashboard.py`)
- **Purpose**: Real-time attack visualization
- **Framework**: Dash and Plotly
- **Features**:
  - Total attempts counter
  - Unique IP tracker
  - Geographic attack map
  - Username/password analysis
  - User agent statistics
  - Auto-updates every 30 seconds

### 3. Login Page (`templates/login.html`)
- **Purpose**: Honeypot frontend
- **Features**:
  - Mimics a legitimate admin login page
  - Collects username/password attempts
  - Displays error messages for failed logins

### 4. Styling (`static/css/`)
- **style.css**: Styles the login page with a professional, responsive design
- **dashboard.css**: Styles the analytics dashboard with a clean, grid-based layout

## Step-by-Step Demonstration

This section guides you through setting up and testing HONEYPOT-EL. Follow these steps to explore its features.

### Prerequisites
- Clone the repository and install dependencies: `pip install -r requirements.txt`
- Configure the `.env` file (e.g., email settings, API keys)
- Start the server in debug mode: `python app.py`

The server will run on `http://localhost:8888`.

### Step 1: Accessing the Honeypot
1. **Open in Browser**:
   - **Login Page**: `http://localhost:8888`
   - **Dashboard**: `http://localhost:8888/dashboard`
2. **Access from Other Devices** (on the same network):
   - **Login Page**: `http://192.168.0.100:8888`
   - **Dashboard**: `http://192.168.0.100:8888/dashboard`

### Step 2: Testing Attack Detection
1. **Basic Login Attempt**:
   - Navigate to `http://localhost:8888`
   - Enter:
     - Username: `admin`
     - Password: `password123`
   - **Observe**:
     - 1-second processing delay
     - "Invalid credentials" error message

2. **Test Rate Limiting**:
   - Attempt login 6 times in quick succession
   - After 5 attempts, a rate limit message appears
   - Wait 1 minute for the limit to reset

3. **View Real-time Analytics**:
   - Open `http://localhost:8888/dashboard`
   - **Observe**:
     - Total attempts counter
     - Your IP listed as a unique attacker
     - Your location on the world map
     - Browser/User-Agent information
     - Time-based graph of attempts

### Step 3: Advanced Features
1. **Email Alert Testing**:
   - Make 3 login attempts from the same IP
   - If email is configured in `.env`, check for an alert in your inbox

2. **Geographic Tracking**:
   - Access the honeypot from a different device or network (if possible)
   - Check the dashboard’s world map for updated attacker locations

3. **Attack Pattern Analysis**:
   - Try different usernames (e.g., `root`, `admin`, `administrator`)
   - On the dashboard, navigate to the "Attack Patterns" tab
   - View the most common usernames attempted

### Step 4: Monitoring
1. **Real-time Updates**:
   - Keep the dashboard open at `http://localhost:8888/dashboard`
   - Make additional login attempts
   - Watch metrics update every 30 seconds

2. **Log Analysis**:
   - Check `honeypot.log` for detailed records
   - Each entry includes:
     - Timestamp
     - IP address
     - Username/password
     - Geolocation
     - Browser details

## Tips for Testing
- Simulate multiple attackers using different browsers or devices
- Test common username/password combinations (e.g., `admin/admin`, `root/password`)
- Monitor the dashboard for real-time updates
- Verify email alerts if configured
- Review `honeypot.log` for raw attack data

## Notes
- Ensure the `.env` file is properly configured for email alerts and geolocation APIs
- For external access, adjust firewall settings or use a public IP
- The honeypot is designed to be safe, never allowing actual access

---

This demonstration showcases HONEYPOT-EL’s ability to detect, log, and analyze intrusion attempts while providing real-time insights through its dashboard.
