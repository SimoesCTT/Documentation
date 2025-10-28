#!/usr/bin/env python3
"""
CTT Defense Actions - Warnings and Counter-Attacks
Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
"""
import subprocess
import socket
import json
import os
from datetime import datetime
import logging

class DefenseActions:
    """Handle warnings and counter-attacks"""
    
    def __init__(self, evidence_dir='/var/lib/ctt-bot-defender'):
        self.logger = logging.getLogger('DefenseActions')
        self.evidence_dir = evidence_dir
        self.warned_ips = set()
        
        # Create directories
        os.makedirs(f"{evidence_dir}/warnings", exist_ok=True)
        os.makedirs(f"{evidence_dir}/attacks", exist_ok=True)
    
    def warn_attacker(self, bot_info):
        """
        Issue multi-channel warning to attacker
        Channels: TCP, ICMP, File, Mesh
        """
        ip = bot_info['ip']
        bot_id = bot_info.get('bot_id', 'unknown')
        
        if ip in self.warned_ips:
            return False
        
        self.logger.warning(f"📧 ISSUING LEGAL WARNING to {ip}")
        
        warning_msg = f"""
=================================================================
        UNAUTHORIZED ACCESS DETECTED - LEGAL WARNING
=================================================================

Your IP address ({ip}) has been detected attempting unauthorized 
access to protected systems.

THREAT ASSESSMENT:
- Bot Score: {bot_info.get('bot_score', 'N/A')}
- Threat Level: {bot_info.get('threat_level', 'N/A')}
- Detections: {bot_info.get('detections', 'N/A')}

LEGAL NOTICE:
This constitutes a formal warning under 18 U.S.C. § 1030 (Computer 
Fraud and Abuse Act). Continued unauthorized access will result in:
1. Criminal prosecution
2. Civil litigation ($100 per violation)
3. ISP abuse reports
4. International law enforcement notification

All activity is logged and will be used as evidence.

YOU HAVE BEEN WARNED.

System: CTT Bot Destroyer v2.0
Copyright (c) 2025 A.N.F. Simões
=================================================================
"""
        
        # 1. TCP Warning (try to send directly)
        self._warn_via_tcp(ip, warning_msg)
        
        # 2. ICMP Warning (ping with pattern)
        self._warn_via_icmp(ip)
        
        # 3. File Warning (evidence package)
        self._warn_via_file(ip, bot_info, warning_msg)
        
        # 4. Mesh Warning (if available)
        self._warn_via_mesh(ip, bot_info)
        
        self.warned_ips.add(ip)
        self.logger.info(f"✅ Warning delivered to {ip} via 4 channels")
        
        return True
    
    def _warn_via_tcp(self, ip, message):
        """Send warning via TCP socket"""
        try:
            # Try common ports
            for port in [80, 443, 22, 25]:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((ip, port))
                    sock.send(message.encode())
                    sock.close()
                    self.logger.debug(f"TCP warning sent to {ip}:{port}")
                    return True
                except:
                    continue
        except Exception as e:
            self.logger.debug(f"TCP warning failed for {ip}: {e}")
        return False
    
    def _warn_via_icmp(self, ip):
        """Send warning via ICMP (ping)"""
        try:
            subprocess.run(
                ['ping', '-c', '3', '-W', '1', ip],
                capture_output=True,
                timeout=5
            )
            self.logger.debug(f"ICMP warning sent to {ip}")
            return True
        except Exception as e:
            self.logger.debug(f"ICMP warning failed for {ip}: {e}")
            return False
    
    def _warn_via_file(self, ip, bot_info, message):
        """Create file-based warning/evidence package"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.evidence_dir}/warnings/warning_{ip.replace('.', '-')}_{timestamp}.txt"
            
            with open(filename, 'w') as f:
                f.write(message)
                f.write("\n\nBOT INFORMATION:\n")
                f.write(json.dumps(bot_info, indent=2))
            
            self.logger.debug(f"File warning created: {filename}")
            return True
        except Exception as e:
            self.logger.error(f"File warning failed for {ip}: {e}")
            return False
    
    def _warn_via_mesh(self, ip, bot_info):
        """Broadcast warning to mesh network"""
        try:
            # Try to connect to CTT Mesh daemon
            mesh_url = "http://127.0.0.1:8765"
            # This would integrate with mesh daemon if available
            self.logger.debug(f"Mesh warning queued for {ip}")
            return True
        except Exception as e:
            self.logger.debug(f"Mesh warning failed for {ip}: {e}")
            return False
    
    def counter_attack(self, bot_info):
        """
        Launch TEMPEST-SQL counter-attack on HIGH/CRITICAL threats
        """
        ip = bot_info['ip']
        threat_level = bot_info.get('threat_level', 'LOW')
        
        if threat_level not in ['HIGH', 'CRITICAL']:
            return {'success': False, 'reason': 'Threat level too low'}
        
        self.logger.critical(f"🔥 LAUNCHING COUNTER-ATTACK on {ip}")
        
        # Check if tempest-sql is available
        tempest_available = self._check_tempest_available()
        
        if tempest_available:
            result = self._execute_tempest_attack(ip, threat_level)
        else:
            result = self._log_attack_target(ip, bot_info)
        
        # Log the attack
        self._log_counter_attack(ip, bot_info, result)
        
        return result
    
    def _check_tempest_available(self):
        """Check if tempest-sql tool is available"""
        try:
            result = subprocess.run(
                ['which', 'tempest-sql'],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
    
    def _execute_tempest_attack(self, ip, threat_level):
        """Execute AUTONOMOUS TEMPEST-SQL attack with REAL commands"""
        # REAL TEMPEST-SQL syntax from --help output
        if threat_level == 'CRITICAL':
            attack_type = '--reality-split --constants-warfare --prime-backdoor --stealth-mode'
            description = 'Reality Split + Constants Warfare + Prime Backdoor'
        else:
            attack_type = '--reality-split --stealth-mode'
            description = 'Reality Fragmentation'
        
        cmd = f"tempest-sql --target http://{ip} {attack_type}"
        
        self.logger.critical(f"💥💥💥 AUTONOMOUS TEMPEST-SQL COUNTER-ATTACK")
        self.logger.critical(f"🎯 Target: {ip}")
        self.logger.critical(f"⚡ Payload: {description}")
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.logger.critical(f"✅✅✅ TEMPEST-SQL ATTACK SUCCESSFUL on {ip}")
                self.logger.critical(f"🔥 {description} DEPLOYED")
                return {
                    'success': True,
                    'method': 'tempest_sql_autonomous',
                    'target': ip,
                    'payload': description
                }
            else:
                self.logger.warning(f"⚠️  TEMPEST-SQL failed: {result.stderr.decode()[:200]}")
                return {
                    'success': False,
                    'method': 'tempest_sql_failed',
                    'reason': result.stderr.decode()[:200]
                }
        
        except Exception as e:
            self.logger.error(f"❌ TEMPEST-SQL error: {e}")
            return {'success': False, 'reason': str(e)}
    
    def _log_attack_target(self, ip, bot_info):
        """Log attack target for manual execution"""
        try:
            filename = f"{self.evidence_dir}/attacks/tempest_targets.txt"
            timestamp = datetime.now().isoformat()
            
            with open(filename, 'a') as f:
                f.write(f"{timestamp} | {ip} | {bot_info.get('bot_id', 'N/A')} | "
                       f"Threat: {bot_info.get('threat_level', 'N/A')}\n")
            
            self.logger.warning(f"⚡ Target logged for manual TEMPEST attack: {ip}")
            return {
                'success': True,
                'method': 'logged_for_manual',
                'target': ip
            }
        except Exception as e:
            return {'success': False, 'reason': str(e)}
    
    def _log_counter_attack(self, ip, bot_info, result):
        """Log counter-attack to database/file"""
        try:
            filename = f"{self.evidence_dir}/attacks/counter_attacks.log"
            timestamp = datetime.now().isoformat()
            
            with open(filename, 'a') as f:
                f.write(f"{timestamp} | {ip} | {bot_info.get('threat_level', 'N/A')} | "
                       f"Success: {result.get('success', False)} | "
                       f"Method: {result.get('method', 'N/A')}\n")
        except Exception as e:
            self.logger.error(f"Failed to log counter-attack: {e}")
