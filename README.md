# Simple Syslog Viewer

A lightweight syslog receiver with a clean web interface for viewing logs in real-time.

## Features

- ✅ Receives syslog messages via UDP and TCP on port 514
- ✅ Modern, dark-themed web interface
- ✅ Real-time log updates (refreshes every 2 seconds)
- ✅ Filter logs by text
- ✅ Auto-scroll toggle
- ✅ Stores last 1000 log entries in memory
- ✅ Shows source IP and timestamp for each log
- ✅ Lightweight and simple to deploy

## Quick Start

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

Then access the web interface at: `http://localhost:8080`

### Using Docker Build

```bash
# Build the image
docker build -t syslog-viewer .

# Run the container
docker run -d \
  -p 514:514/udp \
  -p 514:514/tcp \
  -p 8080:8080 \
  --name syslog-viewer \
  syslog-viewer
```

### Running Directly with Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application (requires root for port 514)
sudo python syslog_viewer.py
```

Or run on non-privileged ports:

```bash
python syslog_viewer.py --syslog-port 5140 --web-port 8080
```

## Configuration

Command-line options:

- `--syslog-port`: Port for syslog (UDP and TCP, default: 514)
- `--web-port`: Port for web interface (default: 8080)
- `--host`: Host to bind to (default: 0.0.0.0)

Example:
```bash
python syslog_viewer.py --syslog-port 5140 --web-port 8888 --host 127.0.0.1
```

## Testing

Send a test syslog message:

```bash
# Using logger command
logger -n localhost -P 514 "Test syslog message"

# Using netcat
echo "Test message from netcat" | nc -u localhost 514

# Using Python
python -c "import socket; s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.sendto(b'Test from Python', ('localhost', 514))"
```

## Port 514 Note

Port 514 is a privileged port (< 1024), so you need:
- Run as root/sudo, OR
- Use a different port (e.g., 5140), OR
- Use Docker (which handles port binding)

## Web Interface Features

- **Filter**: Type to filter logs by any text (timestamp, source, or message)
- **Auto-scroll**: Toggle automatic scrolling to newest logs
- **Clear Display**: Clear the display (logs still being received)
- **Refresh**: Manual refresh of log display
- **Statistics**: Shows total logs, filtered logs, and last update time

## Architecture

- **Backend**: Python with Flask web framework
- **Syslog**: UDP and TCP servers using Python's socketserver
- **Storage**: In-memory deque (last 1000 entries)
- **Frontend**: Vanilla JavaScript with auto-refresh

## License

MIT License - feel free to use and modify as needed!
