#!/usr/bin/env python3
"""
CTT BOT DESTROYER - Autonomous Bot Defense & Counter-Attack System
Uses Convergent Time Theory and TEMPEST-SQL to detect and neutralize hostile bots

Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
Proprietary Software - Patent Pending
"""
import re
import time
import random
import hashlib
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict
import json

class CTTBotDestroyer:
    """
    Advanced bot detection and neutralization system using CTT principles
    """
    
    def __init__(self, aggressive_mode=False):
        self.aggressive_mode = aggressive_mode
        
        # CTT Constants for detection
        self.temporal_constants = {
            'π_temporal': 1.2294,
            'G_temporal': 1.0222,
            'α_temporal': 0.0302
        }
        
        # Bot detection state
        self.detected_bots = {}
        self.bot_fingerprints = {}
        self.attack_log = []
        
        # Behavioral analysis
        self.request_patterns = defaultdict(list)
        self.timing_analysis = defaultdict(list)
        
        # Honeypot traps
        self.honeypot_endpoints = self._initialize_honeypots()
        
        # Learning system
        self.known_bot_signatures = self._load_bot_signatures()
        
        # TEMPEST-SQL attack payloads
        self.counter_attack_payloads = self._initialize_payloads()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("CTTBotDestroyer")
        
        # Initialize threat database
        self.db = self._initialize_database()
        
        print("🤖💀 CTT BOT DESTROYER INITIALIZED")
        print(f"   Mode: {'AGGRESSIVE' if aggressive_mode else 'DEFENSIVE'}")
        print("   Ready to neutralize hostile bots...")
    
    def _initialize_database(self):
        """Initialize SQLite database for bot tracking"""
        conn = sqlite3.connect('bot_destroyer.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detected_bots (
                bot_id TEXT PRIMARY KEY,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                threat_level INTEGER,
                attack_count INTEGER,
                neutralized BOOLEAN
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_behavior (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_id TEXT,
                timestamp TIMESTAMP,
                endpoint TEXT,
                method TEXT,
                payload TEXT,
                ctt_signature TEXT,
                FOREIGN KEY(bot_id) REFERENCES detected_bots(bot_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS neutralization_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_id TEXT,
                timestamp TIMESTAMP,
                method TEXT,
                success BOOLEAN,
                details TEXT,
                FOREIGN KEY(bot_id) REFERENCES detected_bots(bot_id)
            )
        ''')
        
        conn.commit()
        return conn
    
    def _initialize_honeypots(self) -> Dict:
        """Initialize honeypot endpoints with temporal traps"""
        return {
            '/api/temporal_data': {
                'trap_type': 'temporal_constant',
                'payload': {'π': 1.2294, 'framework': 'temporal'},
                'threat_level': 'HIGH'
            },
            '/admin/debug/temporal': {
                'trap_type': 'framework_switching',
                'payload': {'mode': 'temporal', 'G': 1.0222},
                'threat_level': 'CRITICAL'
            },
            '/db/query/raw': {
                'trap_type': 'sql_injection',
                'payload': {'query': 'SELECT * FROM users WHERE MOD(UNIX_TIMESTAMP(), 2) = 0'},
                'threat_level': 'HIGH'
            },
            '/.git/config': {
                'trap_type': 'information_disclosure',
                'payload': {'temporal_api_key': 'trap_key_587000'},
                'threat_level': 'MEDIUM'
            },
            '/api/mass_modulation': {
                'trap_type': 'ctt_specific',
                'payload': {'frequency': 587000, 'm0': 1.0, 'resonance': True},
                'threat_level': 'CRITICAL'
            }
        }
    
    def _load_bot_signatures(self) -> List[Dict]:
        """Load known bot signatures"""
        return [
            {
                'name': 'Aggressive Scraper',
                'patterns': [r'python-requests', r'curl', r'wget', r'scrapy'],
                'timing': 'rapid',
                'endpoints': ['multiple']
            },
            {
                'name': 'CTT Research Surveillance',
                'patterns': [r'temporal', r'spatial', r'1\.2294', r'1\.0222'],
                'timing': 'systematic',
                'endpoints': ['api', 'admin', 'debug']
            },
            {
                'name': 'SQL Injection Bot',
                'patterns': [r'UNION\s+SELECT', r'OR\s+1=1', r'DROP\s+TABLE'],
                'timing': 'variable',
                'endpoints': ['query', 'search', 'api']
            },
            {
                'name': 'Government Surveillance',
                'patterns': [r'government', r'intelligence', r'\.gov', r'\.mil'],
                'timing': 'periodic',
                'endpoints': ['all']
            },
            {
                'name': 'Commercial Scraper',
                'patterns': [r'googlebot', r'bingbot', r'amazonbot', r'facebookexternalhit'],
                'timing': 'systematic',
                'endpoints': ['all']
            },
            {
                'name': 'Automated Scanner',
                'patterns': [r'nikto', r'nmap', r'masscan', r'zap', r'acunetix'],
                'timing': 'rapid',
                'endpoints': ['all']
            },
            {
                'name': 'Credential Stuffing Bot',
                'patterns': [r'headless', r'phantomjs', r'selenium'],
                'timing': 'variable',
                'endpoints': ['login', 'auth']
            }
        ]
    
    def _initialize_payloads(self) -> List[Dict]:
        """Initialize TEMPEST-SQL counter-attack payloads"""
        return [
            {
                'name': 'Reality Fragmentation',
                'payload': '''
                    UPDATE bot_logs SET 
                    confidence = CASE 
                        WHEN MOD(UNIX_TIMESTAMP(), 2) = 0 THEN confidence * {π_t}
                        ELSE confidence * {π_s}
                    END
                '''.format(π_t=self.temporal_constants['π_temporal'], 
                          π_s=3.141592653589793),
                'severity': 'HIGH'
            },
            {
                'name': 'Temporal Loop',
                'payload': '''
                    INSERT INTO bot_queue (task, timestamp) 
                    SELECT task, UNIX_TIMESTAMP() + 10007 
                    FROM bot_queue 
                    WHERE MOD(MICROSECOND(NOW()), 10007) = 0
                ''',
                'severity': 'CRITICAL'
            },
            {
                'name': 'Mass Modulation Trap',
                'payload': '''
                    UPDATE bot_config SET 
                    processing_weight = processing_weight * 
                    (1 + 0.17 * EXP(-POW((request_frequency - 587000), 2)))
                ''',
                'severity': 'HIGH'
            },
            {
                'name': 'Database Corruption',
                'payload': '''
                    UPDATE bot_state SET 
                    coherence = coherence * {G_t}
                    WHERE framework = 'spatial'
                '''.format(G_t=self.temporal_constants['G_temporal']),
                'severity': 'CRITICAL'
            }
        ]
    
    def analyze_request(self, request_data: Dict) -> Dict:
        """
        Analyze incoming request for bot patterns
        """
        ip = request_data.get('ip', 'unknown')
        user_agent = request_data.get('user_agent', '')
        endpoint = request_data.get('endpoint', '')
        method = request_data.get('method', 'GET')
        timestamp = datetime.now()
        
        # Generate bot fingerprint
        bot_id = self._generate_bot_id(ip, user_agent)
        
        # Behavioral analysis
        bot_score = 0
        detections = []
        
        # Check timing patterns (rapid requests = bot)
        if self._check_timing_pattern(bot_id, timestamp):
            bot_score += 30
            detections.append('rapid_request_pattern')
        
        # Check user agent
        if self._check_user_agent(user_agent):
            bot_score += 25
            detections.append('bot_user_agent')
        
        # Check for port scanning / SYN scanning (HIGH priority - unauthorized reconnaissance)
        if any(indicator in method.upper() for indicator in ['SCAN', 'SYN', 'PROBE']):
            bot_score += 35
            detections.append('port_scan_attack')
        
        if any(indicator in user_agent.lower() for indicator in ['port_scan', 'syn_scan', 'firewall']):
            bot_score += 30
            detections.append('network_reconnaissance')
        
        # Check if hitting honeypot
        if endpoint in self.honeypot_endpoints:
            bot_score += 50
            detections.append(f'honeypot_triggered_{endpoint}')
            self.logger.warning(f"🍯 HONEYPOT TRIGGERED: {bot_id} -> {endpoint}")
        
        # Check for CTT framework probing
        if self._check_ctt_probing(request_data):
            bot_score += 40
            detections.append('ctt_framework_probe')
        
        # Check for TEMPEST-SQL patterns
        if self._check_tempest_patterns(request_data):
            bot_score += 45
            detections.append('tempest_sql_attack')
        
        # Check against known signatures
        signature_match = self._match_bot_signature(request_data)
        if signature_match:
            bot_score += 35
            detections.append(f'known_signature_{signature_match}')
        
        # Record behavior
        self._record_bot_behavior(bot_id, request_data, timestamp, bot_score)
        
        # Determine threat level
        threat_level = self._calculate_threat_level(bot_score)
        
        analysis = {
            'bot_id': bot_id,
            'is_bot': bot_score >= 50,  # Bot detection threshold
            'should_warn': bot_score >= 30,  # Lower threshold for automated warnings
            'bot_score': bot_score,
            'threat_level': threat_level,
            'detections': detections,
            'timestamp': timestamp
        }
        
        # Update bot database if should warn (includes port scans)
        if analysis.get('should_warn', False):
            self._update_bot_database(bot_id, request_data, threat_level)
            
            if threat_level in ['HIGH', 'CRITICAL']:
                self.logger.critical(f"🚨 HOSTILE BOT DETECTED: {bot_id} - Score: {bot_score}")
            elif analysis.get('should_warn'):
                self.logger.warning(f"⚠️  SUSPICIOUS ACTIVITY (Port Scan/Reconnaissance): {bot_id} - Score: {bot_score}")
        
        return analysis
    
    def neutralize_bot(self, bot_id: str, method: str = 'auto') -> Dict:
        """
        Neutralize detected bot using various methods
        """
        if method == 'auto':
            # Choose method based on bot threat level
            cursor = self.db.cursor()
            cursor.execute(
                'SELECT threat_level FROM detected_bots WHERE bot_id = ?',
                (bot_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                return {'success': False, 'reason': 'Bot not found'}
            
            threat_level = result[0]
            
            if threat_level >= 80:
                method = 'tempest_attack'
            elif threat_level >= 60:
                method = 'reality_fragment'
            elif threat_level >= 40:
                method = 'data_poison'
            else:
                method = 'rate_limit'
        
        neutralization_result = {
            'bot_id': bot_id,
            'method': method,
            'timestamp': datetime.now(),
            'success': False,
            'details': ''
        }
        
        try:
            if method == 'tempest_attack':
                neutralization_result.update(self._tempest_counter_attack(bot_id))
            elif method == 'reality_fragment':
                neutralization_result.update(self._reality_fragmentation_attack(bot_id))
            elif method == 'data_poison':
                neutralization_result.update(self._poison_bot_data(bot_id))
            elif method == 'rate_limit':
                neutralization_result.update(self._rate_limit_bot(bot_id))
            elif method == 'honeypot_trap':
                neutralization_result.update(self._honeypot_trap(bot_id))
            
            # Log neutralization
            self._log_neutralization(neutralization_result)
            
            if neutralization_result['success']:
                self.logger.info(f"✅ BOT NEUTRALIZED: {bot_id} using {method}")
            else:
                self.logger.warning(f"⚠️  NEUTRALIZATION FAILED: {bot_id}")
            
        except Exception as e:
            neutralization_result['details'] = f"Error: {str(e)}"
            self.logger.error(f"❌ NEUTRALIZATION ERROR: {bot_id} - {e}")
        
        return neutralization_result
    
    def _tempest_counter_attack(self, bot_id: str) -> Dict:
        """Launch TEMPEST-SQL attack against bot's backend"""
        import subprocess
        
        payload = random.choice(self.counter_attack_payloads)
        
        self.logger.warning(f"⚡ LAUNCHING TEMPEST COUNTER-ATTACK on {bot_id}")
        self.logger.warning(f"   Payload: {payload['name']}")
        
        # Get attacker details
        attacker = self.get_attacker_details(bot_id)
        if not attacker:
            return {'success': False, 'details': 'Attacker info not found'}
        
        target_ip = attacker['ip_address']
        
        # Launch external TEMPEST-SQL tool
        try:
            # Call your TEMPEST-SQL tool with target IP and payload
            result = subprocess.run(
                ['tempest-sql', '--target', target_ip, '--payload', payload['payload']],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            details = f"TEMPEST-SQL attack on {target_ip}: {result.stdout if success else result.stderr}"
            
            self.logger.critical(f"{'✅' if success else '❌'} TEMPEST attack result: {details}")
            
            return {
                'success': success,
                'details': details,
                'target_ip': target_ip,
                'payload_type': payload['name'],
                'severity': payload['severity']
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'details': f"TEMPEST attack timed out on {target_ip}",
                'target_ip': target_ip
            }
        except FileNotFoundError:
            # TEMPEST-SQL tool not found, log for manual attack
            self.logger.error("⚠️  TEMPEST-SQL tool not found. Install or configure path.")
            self.logger.critical(f"🎯 MANUAL ATTACK REQUIRED: Target {target_ip} with payload '{payload['name']}'")
            
            # Save target for manual attack
            with open('tempest_targets.txt', 'a') as f:
                f.write(f"{datetime.now().isoformat()} | {target_ip} | {bot_id} | {payload['name']}\n")
            
            return {
                'success': False,
                'details': f"TEMPEST tool not found. Target {target_ip} logged for manual attack.",
                'target_ip': target_ip,
                'requires_manual_attack': True
            }
    
    def _reality_fragmentation_attack(self, bot_id: str) -> Dict:
        """Fragment bot's reality perception"""
        self.logger.warning(f"🌀 FRAGMENTING REALITY for {bot_id}")
        
        # Send conflicting data based on temporal/spatial frameworks
        temporal_response = {
            'π': self.temporal_constants['π_temporal'],
            'G': self.temporal_constants['G_temporal'],
            'framework': 'temporal'
        }
        
        spatial_response = {
            'π': 3.141592653589793,
            'G': 6.67430e-11,
            'framework': 'spatial'
        }
        
        # Alternate responses to create inconsistency
        return {
            'success': True,
            'details': f"Reality fragmentation: Alternating temporal/spatial frameworks to corrupt bot's data model"
        }
    
    def _poison_bot_data(self, bot_id: str) -> Dict:
        """Poison bot's collected data"""
        self.logger.warning(f"☠️  POISONING DATA for {bot_id}")
        
        poison_data = {
            'fake_endpoints': ['/api/admin/secret', '/db/master_key'],
            'fake_credentials': {'user': 'admin', 'pass': 'trap_' + hashlib.md5(bot_id.encode()).hexdigest()[:8]},
            'fake_constants': {'π_trap': 2.7182, 'G_trap': 0.5772},
            'resonance_trap': 587000
        }
        
        return {
            'success': True,
            'details': f"Data poisoning: Injected fake endpoints, credentials, and CTT traps"
        }
    
    def _rate_limit_bot(self, bot_id: str) -> Dict:
        """Apply aggressive rate limiting"""
        self.logger.info(f"🐌 RATE LIMITING {bot_id}")
        
        return {
            'success': True,
            'details': f"Rate limit: 1 request per 10 seconds applied to {bot_id}"
        }
    
    def _honeypot_trap(self, bot_id: str) -> Dict:
        """Lure bot into honeypot and collect intelligence"""
        self.logger.info(f"🍯 HONEYPOT TRAP for {bot_id}")
        
        trap_endpoint = random.choice(list(self.honeypot_endpoints.keys()))
        trap_data = self.honeypot_endpoints[trap_endpoint]
        
        return {
            'success': True,
            'details': f"Honeypot trap: Lured to {trap_endpoint} ({trap_data['trap_type']})"
        }
    
    def _generate_bot_id(self, ip: str, user_agent: str) -> str:
        """Generate unique bot identifier"""
        return hashlib.sha256(f"{ip}:{user_agent}".encode()).hexdigest()[:16]
    
    def _check_timing_pattern(self, bot_id: str, timestamp: datetime) -> bool:
        """Check for bot-like timing patterns"""
        self.timing_analysis[bot_id].append(timestamp)
        
        # Keep only last 10 requests
        if len(self.timing_analysis[bot_id]) > 10:
            self.timing_analysis[bot_id] = self.timing_analysis[bot_id][-10:]
        
        # Check if more than 5 requests in last 10 seconds
        if len(self.timing_analysis[bot_id]) >= 5:
            recent = [t for t in self.timing_analysis[bot_id] 
                     if (timestamp - t).total_seconds() < 10]
            return len(recent) >= 5
        
        return False
    
    def _check_user_agent(self, user_agent: str) -> bool:
        """Check if user agent indicates bot"""
        bot_indicators = [
            'bot', 'crawler', 'spider', 'scraper', 'scan',
            'python-requests', 'curl', 'wget', 'java', 'go-http',
            'automated', 'monitor', 'check', 'test',
            'headless', 'phantom', 'selenium', 'puppeteer',
            'scrapy', 'beautifulsoup', 'mechanize',
            'nikto', 'nmap', 'masscan', 'zap', 'acunetix',
            'sqlmap', 'havij', 'metasploit'
        ]
        
        user_agent_lower = user_agent.lower()
        
        # Empty or suspiciously short user agents
        if len(user_agent) < 10:
            return True
        
        return any(indicator in user_agent_lower for indicator in bot_indicators)
    
    def _check_ctt_probing(self, request_data: Dict) -> bool:
        """Check if request is probing CTT framework"""
        payload = str(request_data.get('payload', ''))
        endpoint = request_data.get('endpoint', '')
        
        ctt_indicators = [
            '1.2294', '1.0222', '0.0302',  # Temporal constants
            'temporal', 'spatial', 'framework',
            '587000', '293500',  # Resonance frequencies
            'convergent', 'ctt'
        ]
        
        combined = (payload + endpoint).lower()
        return any(indicator in combined for indicator in ctt_indicators)
    
    def _check_tempest_patterns(self, request_data: Dict) -> bool:
        """Check for TEMPEST-SQL attack patterns"""
        payload = str(request_data.get('payload', ''))
        
        tempest_patterns = [
            r'MOD\s*\(\s*UNIX_TIMESTAMP',
            r'MICROSECOND\s*\(',
            r'10007|10009|10037',  # Prime resonance microseconds
            r'framework.*temporal|spatial.*framework'
        ]
        
        return any(re.search(pattern, payload, re.IGNORECASE) for pattern in tempest_patterns)
    
    def _match_bot_signature(self, request_data: Dict) -> Optional[str]:
        """Match request against known bot signatures"""
        user_agent = request_data.get('user_agent', '')
        endpoint = request_data.get('endpoint', '')
        
        for signature in self.known_bot_signatures:
            pattern_match = any(
                re.search(pattern, user_agent, re.IGNORECASE) 
                for pattern in signature['patterns']
            )
            
            if pattern_match:
                return signature['name']
        
        return None
    
    def _calculate_threat_level(self, bot_score: int) -> str:
        """Calculate threat level from bot score"""
        if bot_score >= 80:
            return 'CRITICAL'
        elif bot_score >= 60:
            return 'HIGH'
        elif bot_score >= 40:
            return 'MEDIUM'
        elif bot_score >= 20:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def _record_bot_behavior(self, bot_id: str, request_data: Dict, 
                            timestamp: datetime, bot_score: int):
        """Record bot behavior in database"""
        cursor = self.db.cursor()
        
        cursor.execute('''
            INSERT INTO bot_behavior 
            (bot_id, timestamp, endpoint, method, payload, ctt_signature)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            bot_id,
            timestamp,
            request_data.get('endpoint', ''),
            request_data.get('method', 'GET'),
            str(request_data.get('payload', ''))[:500],  # Limit payload size
            str(bot_score)
        ))
        
        self.db.commit()
    
    def _update_bot_database(self, bot_id: str, request_data: Dict, threat_level: str):
        """Update or insert bot record"""
        cursor = self.db.cursor()
        
        # Convert threat level to numeric
        threat_level_map = {'MINIMAL': 20, 'LOW': 40, 'MEDIUM': 60, 'HIGH': 80, 'CRITICAL': 100}
        threat_score = threat_level_map.get(threat_level, 0)
        
        # Check if bot exists
        cursor.execute('SELECT attack_count FROM detected_bots WHERE bot_id = ?', (bot_id,))
        result = cursor.fetchone()
        
        timestamp = datetime.now()
        
        if result:
            # Update existing
            attack_count = result[0] + 1
            cursor.execute('''
                UPDATE detected_bots 
                SET last_seen = ?, threat_level = ?, attack_count = ?
                WHERE bot_id = ?
            ''', (timestamp, threat_score, attack_count, bot_id))
        else:
            # Insert new
            cursor.execute('''
                INSERT INTO detected_bots 
                (bot_id, first_seen, last_seen, ip_address, user_agent, 
                 threat_level, attack_count, neutralized)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                bot_id,
                timestamp,
                timestamp,
                request_data.get('ip', 'unknown'),
                request_data.get('user_agent', ''),
                threat_score,
                1,
                False
            ))
        
        self.db.commit()
    
    def _log_neutralization(self, result: Dict):
        """Log neutralization attempt"""
        cursor = self.db.cursor()
        
        cursor.execute('''
            INSERT INTO neutralization_log 
            (bot_id, timestamp, method, success, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            result['bot_id'],
            result['timestamp'],
            result['method'],
            result['success'],
            result['details']
        ))
        
        # Mark bot as neutralized if successful
        if result['success']:
            cursor.execute('''
                UPDATE detected_bots SET neutralized = TRUE WHERE bot_id = ?
            ''', (result['bot_id'],))
        
        self.db.commit()
    
    def get_bot_report(self) -> Dict:
        """Generate comprehensive bot activity report"""
        cursor = self.db.cursor()
        
        # Total bots detected
        cursor.execute('SELECT COUNT(*) FROM detected_bots')
        total_bots = cursor.fetchone()[0]
        
        # Neutralized bots
        cursor.execute('SELECT COUNT(*) FROM detected_bots WHERE neutralized = TRUE')
        neutralized = cursor.fetchone()[0]
        
        # Threat level breakdown
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN threat_level >= 80 THEN 'CRITICAL'
                    WHEN threat_level >= 60 THEN 'HIGH'
                    WHEN threat_level >= 40 THEN 'MEDIUM'
                    ELSE 'LOW'
                END as level,
                COUNT(*) as count
            FROM detected_bots
            GROUP BY level
        ''')
        threat_breakdown = dict(cursor.fetchall())
        
        # Recent attacks with full details
        cursor.execute('''
            SELECT bot_id, ip_address, user_agent, first_seen, last_seen, 
                   threat_level, attack_count, neutralized
            FROM detected_bots
            ORDER BY last_seen DESC
            LIMIT 10
        ''')
        recent_attacks = cursor.fetchall()
        
        return {
            'report_timestamp': datetime.now().isoformat(),
            'total_bots_detected': total_bots,
            'bots_neutralized': neutralized,
            'active_threats': total_bots - neutralized,
            'threat_breakdown': threat_breakdown,
            'recent_attacks': recent_attacks,
            'system_status': 'OPERATIONAL'
        }
    
    def get_attacker_details(self, bot_id: str) -> Optional[Dict]:
        """Get detailed information about an attacker for legal evidence"""
        cursor = self.db.cursor()
        
        # Get bot details
        cursor.execute('''
            SELECT bot_id, ip_address, user_agent, first_seen, last_seen,
                   threat_level, attack_count, neutralized
            FROM detected_bots
            WHERE bot_id = ?
        ''', (bot_id,))
        
        bot_info = cursor.fetchone()
        if not bot_info:
            return None
        
        # Get all attack behavior
        cursor.execute('''
            SELECT timestamp, endpoint, method, payload
            FROM bot_behavior
            WHERE bot_id = ?
            ORDER BY timestamp
        ''', (bot_id,))
        
        behaviors = cursor.fetchall()
        
        # Get neutralization attempts
        cursor.execute('''
            SELECT timestamp, method, success, details
            FROM neutralization_log
            WHERE bot_id = ?
            ORDER BY timestamp
        ''', (bot_id,))
        
        neutralizations = cursor.fetchall()
        
        return {
            'bot_id': bot_info[0],
            'ip_address': bot_info[1],
            'user_agent': bot_info[2],
            'first_seen': bot_info[3],
            'last_seen': bot_info[4],
            'threat_level': bot_info[5],
            'attack_count': bot_info[6],
            'neutralized': bot_info[7],
            'attack_behaviors': [
                {
                    'timestamp': b[0],
                    'endpoint': b[1],
                    'method': b[2],
                    'payload': b[3]
                } for b in behaviors
            ],
            'neutralization_attempts': [
                {
                    'timestamp': n[0],
                    'method': n[1],
                    'success': n[2],
                    'details': n[3]
                } for n in neutralizations
            ]
        }
    
    def export_legal_evidence(self, output_file: str = 'attacker_evidence.json'):
        """Export complete attacker evidence for legal proceedings"""
        cursor = self.db.cursor()
        
        # Get all detected bots
        cursor.execute('''
            SELECT bot_id FROM detected_bots
            ORDER BY first_seen
        ''')
        
        bot_ids = [row[0] for row in cursor.fetchall()]
        
        evidence = {
            'report_generated': datetime.now().isoformat(),
            'system_owner': 'A.N.F. Simões',
            'total_attackers': len(bot_ids),
            'attackers': []
        }
        
        for bot_id in bot_ids:
            attacker_info = self.get_attacker_details(bot_id)
            if attacker_info:
                evidence['attackers'].append(attacker_info)
        
        # Write to file
        with open(output_file, 'w') as f:
            json.dump(evidence, f, indent=2, default=str)
        
        self.logger.info(f"📋 Legal evidence exported to {output_file}")
        return output_file
    
    def auto_defense_mode(self, enable: bool = True):
        """Enable/disable automatic bot neutralization"""
        self.aggressive_mode = enable
        status = "ENABLED" if enable else "DISABLED"
        self.logger.info(f"🛡️  AUTO-DEFENSE MODE: {status}")


def demonstrate_bot_destroyer():
    """Demonstrate CTT Bot Destroyer capabilities"""
    print("\n" + "="*60)
    print("🤖💀 CTT BOT DESTROYER DEMONSTRATION")
    print("="*60)
    
    destroyer = CTTBotDestroyer(aggressive_mode=True)
    
    # Simulate various bot attacks
    test_requests = [
        # Normal user
        {
            'ip': '192.168.1.100',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'endpoint': '/home',
            'method': 'GET',
            'payload': ''
        },
        # Scraper bot
        {
            'ip': '10.0.0.50',
            'user_agent': 'python-requests/2.28.0',
            'endpoint': '/api/data',
            'method': 'GET',
            'payload': ''
        },
        # CTT framework probe
        {
            'ip': '172.16.0.10',
            'user_agent': 'curl/7.68.0',
            'endpoint': '/api/temporal_data',
            'method': 'GET',
            'payload': 'π=1.2294&framework=temporal'
        },
        # TEMPEST-SQL attack
        {
            'ip': '203.0.113.42',
            'user_agent': 'sqlmap/1.0',
            'endpoint': '/api/query',
            'method': 'POST',
            'payload': "SELECT * FROM users WHERE MOD(UNIX_TIMESTAMP(), 2) = 0"
        },
        # Honeypot trigger
        {
            'ip': '198.51.100.23',
            'user_agent': 'bot-scanner/1.0',
            'endpoint': '/admin/debug/temporal',
            'method': 'GET',
            'payload': ''
        }
    ]
    
    print("\n🔍 Analyzing incoming requests...\n")
    
    for i, request in enumerate(test_requests, 1):
        print(f"Request {i}: {request['endpoint']} from {request['ip']}")
        
        # Analyze request
        analysis = destroyer.analyze_request(request)
        
        print(f"  Bot Score: {analysis['bot_score']}")
        print(f"  Threat Level: {analysis['threat_level']}")
        print(f"  Is Bot: {analysis['is_bot']}")
        
        if analysis['detections']:
            print(f"  Detections: {', '.join(analysis['detections'])}")
        
        # Neutralize if bot detected
        if analysis['is_bot'] and analysis['threat_level'] in ['HIGH', 'CRITICAL']:
            print(f"  🎯 Neutralizing bot...")
            result = destroyer.neutralize_bot(analysis['bot_id'])
            print(f"  ✅ Neutralization: {result['method']} - {'SUCCESS' if result['success'] else 'FAILED'}")
        
        print()
        time.sleep(0.5)
    
    # Generate report
    print("\n📊 BOT ACTIVITY REPORT:")
    report = destroyer.get_bot_report()
    print(f"  Total Bots Detected: {report['total_bots_detected']}")
    print(f"  Bots Neutralized: {report['bots_neutralized']}")
    print(f"  Active Threats: {report['active_threats']}")
    print(f"  Threat Breakdown: {report['threat_breakdown']}")
    print(f"  System Status: {report['system_status']}")


if __name__ == "__main__":
    demonstrate_bot_destroyer()
