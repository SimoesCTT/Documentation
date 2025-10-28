#!/usr/bin/env python3
"""
CTT Bot Defender Service - Active Network Defense
Monitors all incoming connections and destroys hostile bots automatically

Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
"""
import subprocess
import time
import re
import os
from datetime import datetime
try:
    from ctt_bot_destroyer.bot_destroyer import CTTBotDestroyer
except ImportError:
    from bot_destroyer import CTTBotDestroyer

try:
    from attacker_warner import AttackerWarner
except ImportError:
    AttackerWarner = None

import logging

class NetworkDefender:
    """Monitors system network and actively defends against bots"""
    
    def __init__(self, aggressive_mode=True):
        self.destroyer = CTTBotDestroyer(aggressive_mode=aggressive_mode)
        self.monitored_ports = [80, 443, 8080, 8443, 22]  # HTTP, HTTPS, SSH
        self.running = False
        
        # Initialize attacker warner
        self.warner = AttackerWarner() if AttackerWarner else None
        self.warned_ips = set()  # Track already warned IPs
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("NetworkDefender")
        
        # Attack log tracking
        self.attack_log_file = '/var/log/ctt-bot-defender/attacks.log'
        self.last_log_position = 0
        
        print("🛡️ CTT BOT DEFENDER SERVICE STARTING")
        print(f"   Monitoring ports: {self.monitored_ports}")
        print(f"   Attack log: {self.attack_log_file}")
        print(f"   Mode: {'AGGRESSIVE' if aggressive_mode else 'DEFENSIVE'}")
    
    def get_active_connections(self):
        """Get all active network connections"""
        try:
            # Use ss command to get network connections
            result = subprocess.run(
                ['ss', '-tunap'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            connections = []
            for line in result.stdout.split('\n')[1:]:  # Skip header
                if not line.strip():
                    continue
                
                parts = line.split()
                if len(parts) < 5:
                    continue
                
                # Parse connection info
                state = parts[0]
                local_addr = parts[4]
                remote_addr = parts[5]
                
                # Extract IP and port
                if ':' in remote_addr:
                    remote_ip = remote_addr.rsplit(':', 1)[0]
                    # Remove brackets from IPv6
                    remote_ip = remote_ip.strip('[]')
                    
                    connections.append({
                        'state': state,
                        'remote_ip': remote_ip,
                        'local_addr': local_addr,
                        'raw': line
                    })
            
            return connections
            
        except Exception as e:
            self.logger.error(f"Error getting connections: {e}")
            return []
    
    def monitor_http_logs(self):
        """Monitor HTTP access logs for bot patterns"""
        log_files = [
            '/var/log/nginx/access.log',
            '/var/log/httpd/access_log',
            '/var/log/apache2/access.log'
        ]
        
        for log_file in log_files:
            try:
                with open(log_file, 'r') as f:
                    # Read last 100 lines
                    lines = f.readlines()[-100:]
                    
                    for line in lines:
                        # Parse Apache/Nginx log format
                        # IP - - [timestamp] "METHOD /path HTTP/1.1" status size "referer" "user-agent"
                        match = re.match(
                            r'(\S+) \S+ \S+ \[(.*?)\] "(\S+) (\S+) \S+" \d+ \d+ "([^"]*)" "([^"]*)"',
                            line
                        )
                        
                        if match:
                            ip, timestamp, method, path, referer, user_agent = match.groups()
                            
                            yield {
                                'ip': ip,
                                'user_agent': user_agent,
                                'endpoint': path,
                                'method': method,
                                'payload': ''
                            }
            except (FileNotFoundError, PermissionError):
                continue
    
    def monitor_firewall_logs(self):
        """Monitor firewall logs for port scans and connection attempts"""
        try:
            # Get recent firewall drops/rejects from journalctl
            result = subprocess.run(
                ['journalctl', '-u', 'firewalld', '-n', '1000', '--no-pager', '--since', '5 minutes ago'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            for line in result.stdout.split('\n'):
                # Look for firewall blocks
                # Example: REJECT or DROP with source IP
                if any(keyword in line.upper() for keyword in ['REJECT', 'DROP', 'DENY']):
                    # Try to extract IP
                    ip_match = re.search(r'(?:SRC|from)[:=]\s*([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', line)
                    if ip_match:
                        yield {
                            'ip': ip_match.group(1),
                            'user_agent': 'firewall_blocked',
                            'endpoint': 'blocked_connection',
                            'method': 'TCP/UDP',
                            'payload': line[:200]
                        }
        except Exception as e:
            self.logger.debug(f"Firewall log monitoring error: {e}")
    
    def monitor_kernel_logs(self):
        """Monitor kernel logs for blocked packets"""
        try:
            # Check dmesg for iptables/netfilter logs
            result = subprocess.run(
                ['dmesg', '-T'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            for line in result.stdout.split('\n')[-1000:]:
                # Look for iptables/netfilter drops
                if any(keyword in line for keyword in ['IN=', 'SRC=', 'DPT=']):
                    # Extract source IP
                    ip_match = re.search(r'SRC=([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', line)
                    port_match = re.search(r'DPT=(\d+)', line)
                    
                    if ip_match:
                        port = port_match.group(1) if port_match else 'unknown'
                        yield {
                            'ip': ip_match.group(1),
                            'user_agent': f'port_scan:{port}',
                            'endpoint': f'/port:{port}',
                            'method': 'SCAN',
                            'payload': line[:200]
                        }
        except Exception as e:
            self.logger.debug(f"Kernel log monitoring error: {e}")
    
    def monitor_nftables_logs(self):
        """Monitor nftables for blocked traffic (Fedora default)"""
        try:
            # Check nftables counters and logs
            result = subprocess.run(
                ['nft', 'list', 'ruleset'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Parse nftables output for drop/reject counters
            # This gives us aggregate info, specific IPs come from journalctl
            if 'drop' in result.stdout.lower() or 'reject' in result.stdout.lower():
                self.logger.debug("Active nftables drop/reject rules detected")
        except Exception as e:
            self.logger.debug(f"nftables monitoring error: {e}")
    
    def monitor_attack_log(self):
        """Monitor dedicated attack log file"""
        try:
            if not os.path.exists(self.attack_log_file):
                return
            
            with open(self.attack_log_file, 'r') as f:
                f.seek(self.last_log_position)
                
                for line in f:
                    if 'SRC=' in line:
                        ip_match = re.search(r'SRC=([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', line)
                        port_match = re.search(r'DPT=(\d+)', line)
                        proto_match = re.search(r'PROTO=(\w+)', line)
                        
                        if ip_match:
                            port = port_match.group(1) if port_match else 'unknown'
                            proto = proto_match.group(1) if proto_match else 'unknown'
                            
                            if 'SYN_SCAN' in line:
                                user_agent = f'port_scanner:{proto}:{port}'
                                method = 'SYN_SCAN'
                            elif 'INVALID_PACKET' in line:
                                user_agent = f'malformed_packet:{proto}'
                                method = 'INVALID'
                            else:
                                user_agent = f'attack:{proto}:{port}'
                                method = 'ATTACK'
                            
                            yield {
                                'ip': ip_match.group(1),
                                'user_agent': user_agent,
                                'endpoint': f'/{proto}:{port}',
                                'method': method,
                                'payload': line[:500]
                            }
                
                self.last_log_position = f.tell()
        except Exception as e:
            self.logger.debug(f"Attack log monitoring error: {e}")
    
    def check_and_destroy(self, connection_info):
        """Check connection and destroy if it's a bot"""
        # Analyze the request
        analysis = self.destroyer.analyze_request(connection_info)
        
        # Check if we should warn (includes low-level threats like port scans)
        if analysis.get('should_warn', False) or analysis.get('is_bot', False):
            self.logger.warning(
                f"⚠️  THREAT DETECTED: {connection_info['ip']} - "
                f"Score: {analysis['bot_score']} - "
                f"Threat: {analysis['threat_level']} - "
                f"Type: {', '.join(analysis.get('detections', []))}"
            )
            
            # Send warning if not already warned (ALL unauthorized access gets warned)
            if self.warner and connection_info['ip'] not in self.warned_ips:
                try:
                    attacker_details = self.destroyer.get_attacker_details(analysis['bot_id'])
                    if attacker_details:
                        self.logger.warning(f"📧 ISSUING LEGAL WARNING to {connection_info['ip']}")
                        self.warner.warn_attacker(attacker_details)
                        self.warned_ips.add(connection_info['ip'])
                        self.logger.info(f"✅ Warning delivered to {connection_info['ip']} via 6 channels")
                except Exception as e:
                    self.logger.error(f"Failed to warn attacker: {e}")
            
            # If high threat, ALSO launch counter-attack
            if analysis['threat_level'] in ['HIGH', 'CRITICAL']:
                self.logger.critical(
                    f"🔥 HIGH THREAT - LAUNCHING COUNTER-ATTACK on {connection_info['ip']}"
                )
                
                result = self.destroyer.neutralize_bot(
                    analysis['bot_id'],
                    method='auto'
                )
                
                if result['success']:
                    self.logger.critical(f"✅ Bot neutralized: {result['method']}")
                    if 'target_ip' in result:
                        self.logger.critical(f"💥 TEMPEST-SQL counter-attack launched on {result['target_ip']}")
                        self.logger.critical(f"🎯 Payload: {result.get('payload_type', 'unknown')}")
                else:
                    self.logger.warning(f"⚠️  Counter-attack failed: {result.get('details')}")
                
                return True
            else:
                self.logger.info(f"🛡️  Low-level threat - Warning issued, no counter-attack")
        
        return False
    
    def start_monitoring(self):
        """Start active defense monitoring"""
        self.running = True
        self.logger.info("🔍 Starting network defense monitoring...")
        
        seen_ips = set()
        last_report = time.time()
        
        while self.running:
            try:
                # Monitor active connections
                connections = self.get_active_connections()
                
                for conn in connections:
                    remote_ip = conn['remote_ip']
                    
                    # Skip localhost and already processed IPs in this cycle
                    if remote_ip in ['127.0.0.1', '::1', 'localhost']:
                        continue
                    
                    if remote_ip not in seen_ips:
                        seen_ips.add(remote_ip)
                        
                        # Analyze connection
                        connection_info = {
                            'ip': remote_ip,
                            'user_agent': 'unknown',
                            'endpoint': conn.get('local_addr', ''),
                            'method': 'TCP',
                            'payload': ''
                        }
                        
                        self.check_and_destroy(connection_info)
                
                # Monitor HTTP logs
                for request in self.monitor_http_logs():
                    if request['ip'] not in seen_ips:
                        seen_ips.add(request['ip'])
                        self.check_and_destroy(request)
                
                # Monitor firewall logs
                for request in self.monitor_firewall_logs():
                    if request['ip'] not in seen_ips:
                        seen_ips.add(request['ip'])
                        self.check_and_destroy(request)
                
                # Monitor kernel logs for port scans
                for request in self.monitor_kernel_logs():
                    if request['ip'] not in seen_ips:
                        seen_ips.add(request['ip'])
                        self.check_and_destroy(request)
                
                # Monitor attack log file
                for request in self.monitor_attack_log():
                    if request['ip'] not in seen_ips:
                        seen_ips.add(request['ip'])
                        self.check_and_destroy(request)
                
                # Generate report and export JSON every 5 minutes
                if time.time() - last_report > 300:
                    report = self.destroyer.get_bot_report()
                    self.logger.info(
                        f"📊 REPORT: {report['total_bots_detected']} bots detected, "
                        f"{report['bots_neutralized']} neutralized"
                    )
                    last_report = time.time()
                
                # Reset seen IPs every hour
                if len(seen_ips) > 10000:
                    seen_ips.clear()
                
                time.sleep(10)  # Check every 10 seconds
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Stopping network defender...")
                self.running = False
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)
        
        # Export evidence before shutdown
        try:
            evidence_file = self.destroyer.export_legal_evidence(
                f'evidence_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            )
            self.logger.info(f"📋 Evidence exported to {evidence_file}")
        except Exception as e:
            self.logger.error(f"Failed to export evidence: {e}")
    
    def stop(self):
        """Stop the defender"""
        self.running = False


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='CTT Bot Defender Service - Active Network Defense'
    )
    parser.add_argument(
        '--mode',
        choices=['aggressive', 'defensive'],
        default='aggressive',
        help='Defense mode (default: aggressive)'
    )
    parser.add_argument(
        '--ports',
        type=str,
        default='80,443,8080,8443,22',
        help='Ports to monitor (comma-separated)'
    )
    
    args = parser.parse_args()
    
    defender = NetworkDefender(aggressive_mode=(args.mode == 'aggressive'))
    
    if args.ports:
        defender.monitored_ports = [int(p) for p in args.ports.split(',')]
    
    try:
        defender.start_monitoring()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down defender...")
        defender.stop()


if __name__ == "__main__":
    main()
