#!/usr/bin/env python3
"""
Simple Syslog Receiver with Web Interface
Receives syslog messages on UDP/TCP port 514 and displays them via a web interface
"""

import socketserver
import threading
from datetime import datetime
from collections import deque
from flask import Flask, render_template, jsonify
import argparse

# Store logs in memory (keep last 1000 entries)
log_buffer = deque(maxlen=1000)

class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip(), errors='ignore')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        
        log_entry = {
            'timestamp': timestamp,
            'source': client_ip,
            'message': data
        }
        log_buffer.append(log_entry)
        print(f"[{timestamp}] {client_ip}: {data}")

class SyslogTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(4096).strip()
        data = bytes.decode(data, errors='ignore')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        
        log_entry = {
            'timestamp': timestamp,
            'source': client_ip,
            'message': data
        }
        log_buffer.append(log_entry)
        print(f"[{timestamp}] {client_ip}: {data}")

# Flask web interface
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/logs')
def get_logs():
    return jsonify(list(log_buffer))

def start_syslog_servers(udp_port=514, tcp_port=514, host='0.0.0.0'):
    # Start UDP server
    udp_server = socketserver.UDPServer((host, udp_port), SyslogUDPHandler)
    udp_thread = threading.Thread(target=udp_server.serve_forever)
    udp_thread.daemon = True
    udp_thread.start()
    print(f"Syslog UDP server listening on {host}:{udp_port}")
    
    # Start TCP server
    tcp_server = socketserver.TCPServer((host, tcp_port), SyslogTCPHandler)
    tcp_thread = threading.Thread(target=tcp_server.serve_forever)
    tcp_thread.daemon = True
    tcp_thread.start()
    print(f"Syslog TCP server listening on {host}:{tcp_port}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple Syslog Receiver with Web Interface')
    parser.add_argument('--syslog-port', type=int, default=514, help='Syslog port (UDP and TCP, default: 514)')
    parser.add_argument('--web-port', type=int, default=8080, help='Web interface port (default: 8080)')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    args = parser.parse_args()
    
    # Start syslog servers
    start_syslog_servers(udp_port=args.syslog_port, tcp_port=args.syslog_port, host=args.host)
    
    # Start web interface
    print(f"Web interface starting on http://{args.host}:{args.web_port}")
    app.run(host=args.host, port=args.web_port, debug=False)
