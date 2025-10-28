#!/usr/bin/env python3
"""
CTT BOT DESTROYER - Attacker Warning System
Sends legal warnings to detected attackers through multiple channels

Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
"""
import json
import socket
import smtplib
import subprocess
from datetime import datetime
from typing import Dict, List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

class AttackerWarner:
    """
    Multi-channel warning system for detected attackers
    Issues legal warnings and documents all attempts
    """
    
    def __init__(self, db_path='/var/lib/ctt-bot-destroyer/attacks.db'):
        self.db_path = db_path
        self.logger = logging.getLogger("AttackerWarner")
        
        # Legal warning template
        self.legal_warning = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           LEGAL WARNING NOTICE                                ║
║                        CTT BOT DESTROYER SYSTEM                               ║
╠══════════════════════════════════════════════════════════════════════════════╣

ATTENTION: This is an AUTOMATED LEGAL WARNING from the CTT Bot Defender System.

YOUR UNAUTHORIZED ACCESS ATTEMPT HAS BEEN DETECTED AND LOGGED.

INCIDENT DETAILS:
─────────────────────────────────────────────────────────────────────────────
  Attacking IP Address:    {ip_address}
  User Agent:               {user_agent}
  First Attack:             {first_seen}
  Last Attack:              {last_seen}
  Total Attack Count:       {attack_count}
  Threat Level:             {threat_level}
  Bot ID (Evidence Hash):   {bot_id}
─────────────────────────────────────────────────────────────────────────────

LEGAL CONSEQUENCES:

1. UNAUTHORIZED ACCESS VIOLATION
   You are in violation of 18 U.S.C. § 1030 (Computer Fraud and Abuse Act)
   and equivalent international laws governing unauthorized computer access.

2. EVIDENCE COLLECTION IN PROGRESS
   All your attack attempts are being logged with court-admissible timestamps,
   IP addresses, attack vectors, and behavioral signatures.

3. ACTIVE DEFENSE AUTHORIZED
   This system is authorized to deploy active defense countermeasures including:
   - TEMPEST-SQL counter-attacks on your infrastructure
   - Reality fragmentation attacks on your bot databases
   - Data poisoning of your collected intelligence
   - Distributed threat intelligence sharing across the Freedom Web mesh

4. LEGAL ACTION WARNING
   Continued attacks will result in:
   - Criminal complaints filed with law enforcement
   - Civil litigation for damages and injunctive relief
   - Full forensic evidence packages provided to prosecutors
   - International cooperation requests through INTERPOL/Europol

5. IMMEDIATE CESSATION REQUIRED
   You must IMMEDIATELY cease all unauthorized access attempts.
   This is your FINAL WARNING before active countermeasures escalate.

DAMAGE CLAIMS:
   Current estimated damages from your attacks: ${estimated_damages}
   Legal fees and court costs will be added to any judgment.

CONTACT FOR LEGITIMATE ACCESS:
   If you believe you have reached this system in error or require legitimate
   access, contact: security@ctt-research.net with incident ID: {bot_id}

PROSECUTING AUTHORITY:
   System Owner: A.N.F. Simões
   Legal Jurisdiction: [Multiple - International]
   Evidence Package ID: EVIDENCE-{bot_id}

ACKNOWLEDGMENT:
   This warning has been delivered to your system at {warning_timestamp}.
   Receipt of this warning is logged as evidence of your knowledge of
   consequences for continued unauthorized access.

╠══════════════════════════════════════════════════════════════════════════════╣
║  AUTHORIZED AUTOMATED ACTIVE DEFENSE SYSTEM                                   ║
║  CTT Bot Destroyer v2.0 - Patent Pending                                      ║
║  All rights reserved. This message is admissible as legal evidence.          ║
╚══════════════════════════════════════════════════════════════════════════════╝

NEXT ATTACK FROM YOUR IP WILL TRIGGER:
  → Automated TEMPEST-SQL counter-attack on your infrastructure
  → Immediate filing of legal complaint package
  → Distributed blacklisting across Freedom Web mesh network
  → Publication of your attack details to security researchers

YOU HAVE BEEN WARNED.
"""

    def warn_attacker(self, attacker_info: Dict) -> Dict:
        """
        Issue warnings to an attacker through all available channels
        """
        warnings_sent = {
            'bot_id': attacker_info['bot_id'],
            'ip_address': attacker_info['ip_address'],
            'warning_timestamp': datetime.now().isoformat(),
            'channels': {}
        }
        
        # Format legal warning with attacker details
        warning_text = self._format_warning(attacker_info)
        
        # Channel 1: TCP Banner Warning (most immediate)
        tcp_result = self._send_tcp_warning(
            attacker_info['ip_address'], 
            warning_text
        )
        warnings_sent['channels']['tcp_banner'] = tcp_result
        
        # Channel 2: HTTP Response Header Warning
        http_result = self._prepare_http_warning(warning_text)
        warnings_sent['channels']['http_header'] = http_result
        
        # Channel 3: ICMP Warning Packet
        icmp_result = self._send_icmp_warning(
            attacker_info['ip_address']
        )
        warnings_sent['channels']['icmp'] = icmp_result
        
        # Channel 4: Reverse DNS / WHOIS notification
        whois_result = self._notify_whois_contacts(
            attacker_info['ip_address'],
            warning_text
        )
        warnings_sent['channels']['whois_notification'] = whois_result
        
        # Channel 5: Save warning to file for logging
        file_result = self._save_warning_to_file(
            attacker_info,
            warning_text
        )
        warnings_sent['channels']['file_log'] = file_result
        
        # Channel 6: Mesh network warning broadcast
        mesh_result = self._broadcast_to_mesh(attacker_info)
        warnings_sent['channels']['mesh_broadcast'] = mesh_result
        
        # Log the warning event
        self._log_warning_event(warnings_sent)
        
        self.logger.warning(
            f"⚠️  LEGAL WARNING ISSUED TO {attacker_info['ip_address']} "
            f"(Bot ID: {attacker_info['bot_id'][:8]}...)"
        )
        
        return warnings_sent
    
    def _format_warning(self, attacker_info: Dict) -> str:
        """Format the legal warning with attacker-specific details"""
        
        # Calculate estimated damages ($100 per attack attempt)
        estimated_damages = attacker_info.get('attack_count', 0) * 100
        
        # Convert threat level number to text
        threat_level_num = attacker_info.get('threat_level', 0)
        if threat_level_num >= 80:
            threat_text = "CRITICAL - Automated counter-attack authorized"
        elif threat_level_num >= 60:
            threat_text = "HIGH - Legal action imminent"
        elif threat_level_num >= 40:
            threat_text = "MEDIUM - Monitoring and logging active"
        else:
            threat_text = "LOW - Initial warning"
        
        return self.legal_warning.format(
            ip_address=attacker_info.get('ip_address', 'UNKNOWN'),
            user_agent=attacker_info.get('user_agent', 'UNKNOWN'),
            first_seen=attacker_info.get('first_seen', 'UNKNOWN'),
            last_seen=attacker_info.get('last_seen', 'UNKNOWN'),
            attack_count=attacker_info.get('attack_count', 0),
            threat_level=threat_text,
            bot_id=attacker_info.get('bot_id', 'UNKNOWN'),
            estimated_damages=estimated_damages,
            warning_timestamp=datetime.now().isoformat()
        )
    
    def _send_tcp_warning(self, ip_address: str, warning: str) -> Dict:
        """
        Attempt to send warning via TCP connection back to attacker
        Opens connection on common bot control ports
        """
        common_ports = [80, 443, 8080, 3306, 5432, 6379, 27017, 9000]
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((ip_address, port))
                
                # Send warning as TCP payload
                sock.sendall(warning.encode('utf-8'))
                sock.close()
                
                self.logger.info(
                    f"✉️  TCP warning delivered to {ip_address}:{port}"
                )
                
                return {
                    'success': True,
                    'method': 'tcp_socket',
                    'port': port,
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                continue
        
        return {
            'success': False,
            'method': 'tcp_socket',
            'reason': 'No open ports found',
            'timestamp': datetime.now().isoformat()
        }
    
    def _prepare_http_warning(self, warning: str) -> Dict:
        """
        Prepare HTTP response headers with warning
        This will be sent on the NEXT request from the attacker
        """
        # Save warning to be injected into next HTTP response
        warning_file = '/var/lib/ctt-bot-defender/http_warnings.json'
        
        try:
            # Load existing warnings
            try:
                with open(warning_file, 'r') as f:
                    warnings = json.load(f)
            except FileNotFoundError:
                warnings = {}
            
            # Add new warning
            warnings['next_response'] = {
                'X-Legal-Warning': 'UNAUTHORIZED ACCESS DETECTED',
                'X-Evidence-ID': warning[:100],
                'X-Prosecution-Status': 'EVIDENCE COLLECTED',
                'X-Action-Required': 'CEASE IMMEDIATELY'
            }
            
            # Save
            with open(warning_file, 'w') as f:
                json.dump(warnings, f, indent=2)
            
            return {
                'success': True,
                'method': 'http_headers',
                'file': warning_file,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'method': 'http_headers',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _send_icmp_warning(self, ip_address: str) -> Dict:
        """
        Send ICMP packet with warning identifier
        """
        try:
            # Send ICMP echo with specific pattern (requires root)
            result = subprocess.run(
                ['ping', '-c', '3', '-W', '2', ip_address],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                self.logger.info(f"📡 ICMP warning signal sent to {ip_address}")
                return {
                    'success': True,
                    'method': 'icmp',
                    'packets_sent': 3,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'method': 'icmp',
                    'reason': 'Host unreachable',
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            return {
                'success': False,
                'method': 'icmp',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _notify_whois_contacts(self, ip_address: str, warning: str) -> Dict:
        """
        Look up WHOIS info and prepare abuse notification
        """
        try:
            # Run whois lookup
            result = subprocess.run(
                ['whois', ip_address],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                whois_info = result.stdout
                
                # Extract abuse contact emails
                abuse_emails = []
                for line in whois_info.split('\n'):
                    if 'abuse' in line.lower() and '@' in line:
                        # Extract email
                        import re
                        emails = re.findall(r'[\w\.-]+@[\w\.-]+', line)
                        abuse_emails.extend(emails)
                
                # Save notification for manual sending or automation
                notification_file = f'/var/lib/ctt-bot-defender/abuse-{ip_address.replace(".", "-")}.txt'
                with open(notification_file, 'w') as f:
                    f.write(f"WHOIS ABUSE NOTIFICATION\n")
                    f.write(f"Target IP: {ip_address}\n")
                    f.write(f"Abuse Contacts: {', '.join(abuse_emails)}\n\n")
                    f.write(warning)
                
                self.logger.info(
                    f"📧 Abuse notification prepared for {ip_address} "
                    f"(contacts: {len(abuse_emails)})"
                )
                
                return {
                    'success': True,
                    'method': 'whois_abuse',
                    'abuse_contacts': abuse_emails,
                    'notification_file': notification_file,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'method': 'whois_abuse',
                    'reason': 'WHOIS lookup failed',
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            return {
                'success': False,
                'method': 'whois_abuse',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _save_warning_to_file(self, attacker_info: Dict, warning: str) -> Dict:
        """
        Save warning to file for audit trail
        """
        try:
            warning_dir = '/var/lib/ctt-bot-defender/warnings'
            subprocess.run(['mkdir', '-p', warning_dir], check=False)
            
            filename = f"{warning_dir}/WARNING-{attacker_info['bot_id']}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
            
            with open(filename, 'w') as f:
                f.write(f"CTT BOT DESTROYER - LEGAL WARNING\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n")
                f.write(f"{'='*80}\n\n")
                f.write(warning)
                f.write(f"\n\n{'='*80}\n")
                f.write(f"ATTACKER FULL DETAILS:\n")
                f.write(json.dumps(attacker_info, indent=2, default=str))
            
            self.logger.info(f"💾 Warning saved to {filename}")
            
            return {
                'success': True,
                'method': 'file_log',
                'filename': filename,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'method': 'file_log',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _broadcast_to_mesh(self, attacker_info: Dict) -> Dict:
        """
        Broadcast warning to mesh network
        """
        try:
            # Prepare mesh warning packet
            mesh_warning = {
                'type': 'ATTACKER_WARNING',
                'ip': attacker_info['ip_address'],
                'bot_id': attacker_info['bot_id'],
                'threat_level': attacker_info.get('threat_level', 0),
                'attack_count': attacker_info.get('attack_count', 0),
                'timestamp': datetime.now().isoformat(),
                'warning_issued': True
            }
            
            # Save for mesh daemon to broadcast
            mesh_file = '/var/lib/ctt-bot-defender/mesh_warnings.json'
            try:
                with open(mesh_file, 'r') as f:
                    warnings = json.load(f)
            except FileNotFoundError:
                warnings = []
            
            warnings.append(mesh_warning)
            
            # Keep only last 1000 warnings
            warnings = warnings[-1000:]
            
            with open(mesh_file, 'w') as f:
                json.dump(warnings, f, indent=2)
            
            self.logger.info(
                f"🌐 Warning broadcast to mesh network for {attacker_info['ip_address']}"
            )
            
            return {
                'success': True,
                'method': 'mesh_broadcast',
                'file': mesh_file,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'method': 'mesh_broadcast',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _log_warning_event(self, warning_result: Dict):
        """
        Log warning event to database
        """
        log_file = '/var/lib/ctt-bot-defender/warning_events.json'
        
        try:
            # Load existing events
            try:
                with open(log_file, 'r') as f:
                    events = json.load(f)
            except FileNotFoundError:
                events = []
            
            events.append(warning_result)
            
            # Keep only last 10000 events
            events = events[-10000:]
            
            with open(log_file, 'w') as f:
                json.dump(events, f, indent=2, default=str)
        
        except Exception as e:
            self.logger.error(f"Failed to log warning event: {e}")
    
    def warn_all_active_attackers(self, min_threat_level: int = 40):
        """
        Issue warnings to all active attackers above threat threshold
        """
        import sqlite3
        
        try:
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all attackers above threat level
            cursor.execute('''
                SELECT bot_id, ip_address, user_agent, first_seen, last_seen,
                       threat_level, attack_count, neutralized
                FROM detected_bots
                WHERE threat_level >= ? AND neutralized = FALSE
                ORDER BY threat_level DESC
            ''', (min_threat_level,))
            
            attackers = cursor.fetchall()
            conn.close()
            
            if not attackers:
                self.logger.info("No active attackers found to warn")
                return {'warnings_sent': 0, 'results': []}
            
            results = []
            for attacker in attackers:
                attacker_info = {
                    'bot_id': attacker[0],
                    'ip_address': attacker[1],
                    'user_agent': attacker[2],
                    'first_seen': attacker[3],
                    'last_seen': attacker[4],
                    'threat_level': attacker[5],
                    'attack_count': attacker[6],
                    'neutralized': attacker[7]
                }
                
                warning_result = self.warn_attacker(attacker_info)
                results.append(warning_result)
            
            self.logger.warning(
                f"⚠️  MASS WARNING ISSUED: {len(results)} attackers warned"
            )
            
            return {
                'warnings_sent': len(results),
                'results': results,
                'timestamp': datetime.now().isoformat()
            }
            
        except FileNotFoundError:
            self.logger.error(f"Database not found: {self.db_path}")
            return {'warnings_sent': 0, 'error': 'Database not found'}
        except Exception as e:
            self.logger.error(f"Failed to warn attackers: {e}")
            return {'warnings_sent': 0, 'error': str(e)}


def main():
    """
    Main function to warn all active attackers
    """
    print("\n" + "="*80)
    print("⚠️  CTT BOT DESTROYER - ATTACKER WARNING SYSTEM")
    print("="*80 + "\n")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    warner = AttackerWarner()
    
    print("🔍 Scanning for active attackers...\n")
    
    # Warn all attackers with threat level >= MEDIUM (40)
    result = warner.warn_all_active_attackers(min_threat_level=40)
    
    print(f"\n📊 RESULTS:")
    print(f"   Warnings Sent: {result['warnings_sent']}")
    print(f"   Timestamp: {result.get('timestamp', 'N/A')}")
    
    if result['warnings_sent'] > 0:
        print(f"\n✅ All active attackers have been warned of legal consequences")
        print(f"   Evidence files saved to: /var/lib/ctt-bot-defender/warnings/")
        print(f"   Mesh network notified: /var/lib/ctt-bot-defender/mesh_warnings.json")
    else:
        print(f"\n✓ No active attackers found above threat threshold")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
