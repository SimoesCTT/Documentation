#!/usr/bin/env python3
"""
CTT Bot Detector - Core Detection Engine
Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
"""
import sqlite3
import hashlib
import re
from datetime import datetime
import logging

class BotDetector:
    """Core bot detection and scoring engine"""
    
    def __init__(self, db_path='/var/lib/ctt-bot-defender/bots.db'):
        self.db_path = db_path
        self.logger = logging.getLogger('BotDetector')
        self._init_database()
        
        # Bot signatures
        self.bot_user_agents = [
            'bot', 'crawler', 'spider', 'scraper', 'curl', 'wget', 'python',
            'go-http', 'java', 'scanner', 'masscan', 'nmap', 'sqlmap',
            'nikto', 'burp', 'metasploit', 'nuclei', 'httpx'
        ]
        
        # Suspicious patterns
        self.sql_injection_patterns = [
            "union.*select", "or.*1.*=.*1", "exec\\(", "drop.*table",
            "insert.*into", "update.*set", "delete.*from"
        ]
        
        self.honeypot_endpoints = [
            '/admin', '/phpmyadmin', '/wp-admin', '/.env', '/.git',
            '/api/temporal_data', '/db/query', '/.aws'
        ]
    
    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS detected_bots (
                bot_id TEXT PRIMARY KEY,
                ip_address TEXT NOT NULL,
                user_agent TEXT,
                first_seen TEXT,
                last_seen TEXT,
                threat_level INTEGER,
                bot_score INTEGER,
                attack_count INTEGER DEFAULT 1,
                detections TEXT
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS attacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_id TEXT,
                timestamp TEXT,
                endpoint TEXT,
                method TEXT,
                payload TEXT,
                FOREIGN KEY(bot_id) REFERENCES detected_bots(bot_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def analyze_connection(self, ip, user_agent='', endpoint='', method='', payload=''):
        """
        Analyze a connection and return threat assessment
        
        Returns dict with:
        - is_threat: bool
        - bot_score: int (0-100)
        - threat_level: str (MINIMAL/LOW/MEDIUM/HIGH/CRITICAL)
        - detections: list of detected patterns
        - bot_id: str
        """
        score = 0
        detections = []
        
        # Check user agent
        if user_agent:
            ua_lower = user_agent.lower()
            for bot_pattern in self.bot_user_agents:
                if bot_pattern in ua_lower:
                    score += 30
                    detections.append(f'bot_user_agent:{bot_pattern}')
                    break
        else:
            score += 20
            detections.append('no_user_agent')
        
        # Check for SQL injection
        if payload:
            for pattern in self.sql_injection_patterns:
                if re.search(pattern, payload.lower()):
                    score += 50
                    detections.append('sql_injection')
                    break
        
        # Check honeypot endpoints
        if endpoint:
            for trap in self.honeypot_endpoints:
                if trap in endpoint:
                    score += 40
                    detections.append(f'honeypot:{trap}')
                    break
        
        # Port scans (identified by user_agent pattern)
        if 'port_scan' in user_agent.lower() or 'syn_scan' in user_agent.lower():
            score += 60
            detections.append('port_scan')
        
        # Determine threat level
        if score >= 80:
            threat_level = 'CRITICAL'
        elif score >= 60:
            threat_level = 'HIGH'
        elif score >= 40:
            threat_level = 'MEDIUM'
        elif score >= 20:
            threat_level = 'LOW'
        else:
            threat_level = 'MINIMAL'
        
        # Generate bot ID
        bot_id = hashlib.md5(f"{ip}:{user_agent}".encode()).hexdigest()[:16]
        
        # Store in database if threat detected
        if score >= 20:
            self._record_bot(bot_id, ip, user_agent, score, threat_level, 
                           detections, endpoint, method, payload)
        
        return {
            'is_threat': score >= 30,  # Warn threshold
            'bot_score': score,
            'threat_level': threat_level,
            'detections': detections,
            'bot_id': bot_id,
            'should_warn': score >= 30,
            'should_attack': score >= 60
        }
    
    def _record_bot(self, bot_id, ip, user_agent, score, threat_level, 
                   detections, endpoint, method, payload):
        """Record bot detection in database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        now = datetime.now().isoformat()
        detections_str = ','.join(detections)
        
        # Check if bot already exists
        c.execute('SELECT attack_count FROM detected_bots WHERE bot_id = ?', (bot_id,))
        row = c.fetchone()
        
        if row:
            # Update existing
            attack_count = row[0] + 1
            c.execute('''
                UPDATE detected_bots 
                SET last_seen = ?, attack_count = ?, threat_level = ?, bot_score = ?
                WHERE bot_id = ?
            ''', (now, attack_count, score, score, bot_id))
        else:
            # Insert new
            c.execute('''
                INSERT INTO detected_bots 
                (bot_id, ip_address, user_agent, first_seen, last_seen, 
                 threat_level, bot_score, attack_count, detections)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
            ''', (bot_id, ip, user_agent, now, now, score, score, detections_str))
        
        # Record attack
        c.execute('''
            INSERT INTO attacks (bot_id, timestamp, endpoint, method, payload)
            VALUES (?, ?, ?, ?, ?)
        ''', (bot_id, now, endpoint, method, payload[:500]))
        
        conn.commit()
        conn.close()
    
    def get_bot_info(self, bot_id):
        """Get information about a specific bot"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT ip_address, user_agent, first_seen, last_seen, 
                   threat_level, bot_score, attack_count, detections
            FROM detected_bots WHERE bot_id = ?
        ''', (bot_id,))
        
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                'ip': row[0],
                'user_agent': row[1],
                'first_seen': row[2],
                'last_seen': row[3],
                'threat_level': row[4],
                'bot_score': row[5],
                'attack_count': row[6],
                'detections': row[7]
            }
        return None
    
    def get_statistics(self):
        """Get overall statistics"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*) FROM detected_bots')
        total_bots = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM detected_bots WHERE threat_level >= 60')
        high_threats = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM attacks')
        total_attacks = c.fetchone()[0]
        
        conn.close()
        
        return {
            'total_bots': total_bots,
            'high_threats': high_threats,
            'total_attacks': total_attacks
        }
