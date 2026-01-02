FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY syslog_viewer.py .
COPY templates/ templates/

# Expose ports
# 514 for syslog (UDP and TCP)
# 8080 for web interface
EXPOSE 514/udp 514/tcp 8080

# Run as non-root user for security
RUN useradd -m -u 1000 syslog && chown -R syslog:syslog /app
USER syslog

# Start the application
CMD ["python", "syslog_viewer.py"]
