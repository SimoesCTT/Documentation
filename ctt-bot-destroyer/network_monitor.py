#!/usr/bin/env python3
"""
CTT Network Monitor - Real-time Connection Monitoring
Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
"""
import subprocess
import re
import logging
import time

class NetworkMonitor:
    """Monitor network connections in real-time"""
    
    def __init__(self):
        self.logger = logging.getLogger('NetworkMonitor')
        self.seen_connections = set()
        self.monitored_ports = [80, 443, 8080, 8443, 22, 3306, 5432]
    
    def get_active_connections(self):
        """
        Get all active network connections
        Returns list of dicts with connection info
        """
        connections = []
        
        try:
            # Use ss command (faster than netstat)
            result = subprocess.run(
                ['ss', '-tunap'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            for line in result.stdout.split('\n')[1:]:  # Skip header
                if not line.strip():
                    continue
                
                parts = line.split()
                if len(parts) < 6:
                    continue
                
                # Parse: Netid State Recv-Q Send-Q Local Remote
                state = parts[1]
                remote_addr = parts[5]
                
                # Extract IP from address (format: IP:PORT)
                if ':' in remote_addr:
                    remote_ip = remote_addr.rsplit(':', 1)[0]
                    # Remove IPv6 brackets
                    remote_ip = remote_ip.strip('[]')
                    
                    # Skip localhost
                    if remote_ip in ['127.0.0.1', '::1', 'localhost']:
                        continue
                    
                    # Create connection fingerprint
                    conn_id = f"{remote_ip}:{state}"
                    
                    if conn_id not in self.seen_connections:
                        self.seen_connections.add(conn_id)
                        
                        connections.append({
                            'ip': remote_ip,
                            'state': state,
                            'raw': line
                        })
        
        except subprocess.TimeoutExpired:
            self.logger.error("ss command timed out")
        except Exception as e:
            self.logger.error(f"Error getting connections: {e}")
        
        # Clean up old connections periodically
        if len(self.seen_connections) > 10000:
            self.seen_connections.clear()
        
        return connections
    
    def monitor_port_scans(self):
        """
        Monitor for port scans by reading kernel logs
        Returns list of suspected port scan attacks
        """
        scans = []
        
        try:
            # Read recent dmesg for port scans
            result = subprocess.run(
                ['dmesg', '-T', '|', 'tail', '-1000'],
                shell=True,
                capture_output=True,
                text=True,
                timeout=3
            )
            
            for line in result.stdout.split('\n'):
                # Look for SYN scans in kernel logs
                if 'SRC=' in line and 'DPT=' in line:
                    ip_match = re.search(r'SRC=([0-9.]+)', line)
                    port_match = re.search(r'DPT=(\d+)', line)
                    
                    if ip_match:
                        ip = ip_match.group(1)
                        port = port_match.group(1) if port_match else 'unknown'
                        
                        scans.append({
                            'ip': ip,
                            'port': port,
                            'raw': line
                        })
        
        except Exception as e:
            self.logger.debug(f"Port scan monitoring error: {e}")
        
        return scans
    
    def monitor_http_access(self, log_files=None):
        """
        Monitor HTTP access logs for suspicious activity
        """
        if log_files is None:
            log_files = [
                '/var/log/nginx/access.log',
                '/var/log/httpd/access_log',
                '/var/log/apache2/access.log'
            ]
        
        requests = []
        
        for log_file in log_files:
            try:
                with open(log_file, 'r') as f:
                    # Read last 50 lines
                    lines = f.readlines()[-50:]
                    
                    for line in lines:
                        # Parse Apache/Nginx log format
                        # IP - - [timestamp] "METHOD /path HTTP/1.1" status size "referer" "user-agent"
                        match = re.match(
                            r'(\S+) \S+ \S+ \[(.*?)\] "(\S+) (\S+) \S+" \d+ \d+ "([^"]*)" "([^"]*)"',
                            line
                        )
                        
                        if match:
                            ip, timestamp, method, path, referer, user_agent = match.groups()
                            
                            requests.append({
                                'ip': ip,
                                'user_agent': user_agent,
                                'endpoint': path,
                                'method': method
                            })
            
            except (FileNotFoundError, PermissionError):
                continue
            except Exception as e:
                self.logger.debug(f"HTTP log monitoring error: {e}")
        
        return requests
    
    def get_connection_info(self, ip):
        """
        Get detailed information about a specific IP connection
        """
        try:
            # Try to get reverse DNS
            result = subprocess.run(
                ['dig', '-x', ip, '+short'],
                capture_output=True,
                text=True,
                timeout=2
            )
            hostname = result.stdout.strip() if result.returncode == 0 else None
            
            return {
                'ip': ip,
                'hostname': hostname
            }
        
        except Exception as e:
            self.logger.debug(f"Error getting connection info for {ip}: {e}")
            return {'ip': ip, 'hostname': None}
