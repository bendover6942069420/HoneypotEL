from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail, Message
import logging
from datetime import datetime
import json
import os
import time
from dotenv import load_dotenv
import requests
from user_agents import parse
from dashboard import init_dashboard
import argparse
import socket
import threading

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='honeypot.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Honeypot Server')
parser.add_argument('--ports', type=str, default='80,8080,8888,443,22', help='Comma-separated list of ports to listen on')
parser.add_argument('--host', type=str, default='0.0.0.0', help='Host IP address to bind to')
parser.add_argument('--public', action='store_true', help='Show local network IP addresses on startup')
args = parser.parse_args()

app = Flask(__name__)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
mail = Mail(app)

# Rate limiter configuration with specific limits for dashboard
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5 per minute", "100 per hour"],
    storage_uri="memory://"
)

# Exempt dashboard routes from rate limiting
@limiter.request_filter
def exempt_dashboard():
    return request.path.startswith('/dashboard/')

# Initialize the dashboard
dash_app = init_dashboard(app)

def get_local_ips():
    ips = []
    try:
        # Get all network interfaces
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
        for ip in interfaces:
            if ip[4][0] != '127.0.0.1':  # Exclude localhost
                ips.append(ip[4][0])
    except Exception as e:
        logging.error(f"Error getting local IPs: {str(e)}")
    return ips

def get_geolocation(ip):
    try:
        if ip in ['127.0.0.1', 'localhost']:
            return {'country': 'Local', 'city': 'Local', 'latitude': 0, 'longitude': 0}
        
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        if response.status_code == 200:
            data = response.json()
            return {
                'country': data.get('country_name', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'latitude': data.get('latitude', 0),
                'longitude': data.get('longitude', 0)
            }
    except Exception as e:
        logging.error(f"Error getting geolocation for IP {ip}: {str(e)}")
    return {'country': 'Unknown', 'city': 'Unknown', 'latitude': 0, 'longitude': 0}

def send_alert_email(ip, username, geo_info, user_agent):
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        return
        
    try:
        msg = Message(
            'Honeypot Alert - Suspicious Login Attempt',
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']]
        )
        msg.body = f"""
        Suspicious login attempt detected:
        IP Address: {ip}
        Username: {username}
        Location: {geo_info['city']}, {geo_info['country']}
        User Agent: {user_agent}
        Time: {datetime.now()}
        """
        mail.send(msg)
    except Exception as e:
        logging.error(f"Error sending email alert: {str(e)}")

def log_attempt(ip, username, password, headers):
    # Get geolocation info
    geo_info = get_geolocation(ip)
    
    # Parse user agent
    ua_string = headers.get('User-Agent', 'Unknown')
    user_agent = str(parse(ua_string))
    
    # Prepare log data
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'ip_address': ip,
        'username': username,
        'password': password,
        'country': geo_info['country'],
        'city': geo_info['city'],
        'user_agent': user_agent,
        'headers': dict(headers)
    }
    
    # Log the attempt
    logging.info(json.dumps(log_data))
    
    # Check for suspicious activity and send alert
    with open('honeypot.log', 'r') as f:
        ip_attempts = sum(1 for line in f if ip in line)
        if ip_attempts >= 3:  # Alert after 3 attempts from same IP
            send_alert_email(ip, username, geo_info, user_agent)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    ip_address = request.remote_addr
    
    # Log the attempt with enhanced information
    log_attempt(ip_address, username, password, request.headers)
    
    # Simulate processing delay
    time.sleep(1)
    
    return render_template('login.html', error="Invalid credentials. Please try again.")

@app.route('/analytics')
def analytics():
    return redirect('/dashboard/')

def start_server(port):
    try:
        if args.public:
            local_ips = get_local_ips()
            print(f"\nHoneypot is accessible at:")
            for ip in local_ips:
                print(f"http://{ip}:{port}")
            print(f"Local access: http://localhost:{port}")
            
        app.run(host=args.host, port=port, threaded=True)
    except Exception as e:
        logging.error(f"Failed to start server on port {port}: {str(e)}")

if __name__ == '__main__':
    ports = [int(port.strip()) for port in args.ports.split(',')]
    
    # Start servers on all specified ports
    for port in ports[1:]:  # Start additional ports in separate threads
        thread = threading.Thread(target=start_server, args=(port,))
        thread.daemon = True
        thread.start()
    
    # Start main server on first port
    start_server(ports[0])