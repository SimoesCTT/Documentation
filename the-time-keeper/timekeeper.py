#!/usr/bin/env python3
"""
THE TIME KEEPER: Temporal Attack Detection & Prevention System
Defends against TEMPEST-SQL reality fragmentation attacks

Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
Proprietary Software - Patent Pending
"""
import re
import time
import math
import logging
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
import hashlib
import json

class TempestDefender:
    def __init__(self):
        # Attack signatures
        self.temporal_constants = {
            'π_temporal': 1.2294,
            'G_temporal': 1.0222, 
            'α_temporal': 0.0302
        }
        
        self.spatial_constants = {
            'π_spatial': 3.141592653589793,
            'G_spatial': 6.67430e-11
        }
        
        # Prime resonance backdoor microseconds
        self.prime_resonance_microseconds = {
            10007, 10009, 10037, 10039, 10061, 
            10067, 10069, 10079, 10091, 10093
        }
        
        # Resonance frequencies
        self.positive_resonance = 587000  # Hz
        self.negative_resonance = 293500  # Hz
        
        # Attack detection state
        self.detected_attacks = []
        self.blocked_queries = []
        self.reality_violations = 0
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("TimeKeeper")
        
        print("🛡️  THE TIME KEEPER INITIALIZED")
        print("   Monitoring for temporal reality attacks...")

    def analyze_query(self, query: str, timestamp: datetime = None) -> Dict:
        """
        Analyze SQL query for TEMPEST-SQL attack patterns
        Returns detection results with threat level
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        analysis = {
            'query': query,
            'timestamp': timestamp,
            'threat_level': 'CLEAN',
            'detections': [],
            'block_recommended': False
        }
        
        # Detection pipeline
        detectors = [
            self._detect_temporal_constants,
            self._detect_framework_switching, 
            self._detect_prime_resonance_timing,
            self._detect_reality_fragmentation,
            self._detect_mass_modulation,
            self._detect_resonance_patterns
        ]
        
        for detector in detectors:
            detection = detector(query, timestamp)
            if detection['detected']:
                analysis['detections'].append(detection)
                analysis['threat_level'] = self._update_threat_level(
                    analysis['threat_level'], detection['severity']
                )
        
        # Determine if blocking is recommended
        analysis['block_recommended'] = any(
            det['severity'] in ['HIGH', 'CRITICAL'] for det in analysis['detections']
        )
        
        return analysis

    def _detect_temporal_constants(self, query: str, timestamp: datetime) -> Dict:
        """Detect usage of temporal framework constants"""
        detected = False
        found_constants = []
        
        for constant_name, constant_value in self.temporal_constants.items():
            # Look for the constant value in the query
            pattern = str(constant_value)
            if pattern in query:
                detected = True
                found_constants.append(constant_name)
        
        return {
            'detector': 'temporal_constants',
            'detected': detected,
            'severity': 'HIGH' if detected else 'LOW',
            'details': {
                'found_constants': found_constants,
                'message': f'Temporal constants detected: {found_constants}' if detected else 'No temporal constants found'
            }
        }

    def _detect_framework_switching(self, query: str, timestamp: datetime) -> Dict:
        """Detect queries that use both temporal and spatial constants"""
        temporal_found = any(str(val) in query for val in self.temporal_constants.values())
        spatial_found = any(str(val) in query for val in self.spatial_constants.values())
        
        framework_switching = temporal_found and spatial_found
        
        return {
            'detector': 'framework_switching',
            'detected': framework_switching,
            'severity': 'CRITICAL' if framework_switching else 'LOW',
            'details': {
                'temporal_detected': temporal_found,
                'spatial_detected': spatial_found,
                'message': 'FRAMEWORK SWITCHING ATTACK: Query uses both temporal and spatial constants' 
                    if framework_switching else 'No framework switching detected'
            }
        }

    def _detect_prime_resonance_timing(self, query: str, timestamp: datetime) -> Dict:
        """Detect queries executed at prime resonance microseconds"""
        microsecond = timestamp.microsecond
        prime_resonance_detected = microsecond in self.prime_resonance_microseconds
        
        return {
            'detector': 'prime_resonance_timing',
            'detected': prime_resonance_detected,
            'severity': 'HIGH' if prime_resonance_detected else 'LOW',
            'details': {
                'microsecond': microsecond,
                'prime_resonance_set': self.prime_resonance_microseconds,
                'message': f'PRIME RESONANCE BACKDOOR: Query executed at prime resonance microsecond {microsecond}'
                    if prime_resonance_detected else 'No prime resonance timing detected'
            }
        }

    def _detect_reality_fragmentation(self, query: str, timestamp: datetime) -> Dict:
        """Detect reality fragmentation patterns in queries"""
        # Look for conditional logic based on temporal frameworks
        fragmentation_patterns = [
            r'MOD\s*\(\s*UNIX_TIMESTAMP\s*\(\s*\)\s*,\s*2\s*\)',  # MOD(UNIX_TIMESTAMP(), 2)
            r'temporal.*framework',
            r'spatial.*framework', 
            r'reality.*split',
            r'framework.*dependent'
        ]
        
        detected_patterns = []
        for pattern in fragmentation_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                detected_patterns.append(pattern)
        
        fragmentation_detected = len(detected_patterns) > 0
        
        return {
            'detector': 'reality_fragmentation',
            'detected': fragmentation_detected,
            'severity': 'HIGH' if fragmentation_detected else 'LOW',
            'details': {
                'detected_patterns': detected_patterns,
                'message': f'REALITY FRAGMENTATION: Found patterns: {detected_patterns}'
                    if fragmentation_detected else 'No reality fragmentation patterns detected'
            }
        }

    def _detect_mass_modulation(self, query: str, timestamp: datetime) -> Dict:
        """Detect mass modulation formulas from CTT"""
        mass_modulation_patterns = [
            r'm\(f\)\s*=\s*m0',  # m(f) = m0[...]
            r'1\s*\+\s*0\.17',   # 1 + 0.17 (17% mass increase)
            r'e\s*\^\s*\(\s*-\s*\(\s*f\s*-\s*fres',  # exponential decay around resonance
            r'mass.*modulation',
            r'f_res\s*=\s*587000'  # resonance frequency
        ]
        
        detected_patterns = []
        for pattern in mass_modulation_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                detected_patterns.append(pattern)
        
        modulation_detected = len(detected_patterns) > 0
        
        return {
            'detector': 'mass_modulation',
            'detected': modulation_detected,
            'severity': 'MEDIUM' if modulation_detected else 'LOW',
            'details': {
                'detected_patterns': detected_patterns,
                'message': f'MASS MODULATION: Found CTT mass modulation patterns: {detected_patterns}'
                    if modulation_detected else 'No mass modulation detected'
            }
        }

    def _detect_resonance_patterns(self, query: str, timestamp: datetime) -> Dict:
        """Detect resonance frequency patterns"""
        resonance_patterns = [
            r'587000',  # Positive resonance
            r'293500',  # Negative resonance  
            r'587\s*000',
            r'293\s*500',
            r'resonance.*587',
            r'resonance.*293'
        ]
        
        detected_patterns = []
        for pattern in resonance_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                detected_patterns.append(pattern)
        
        resonance_detected = len(detected_patterns) > 0
        
        return {
            'detector': 'resonance_patterns',
            'detected': resonance_detected,
            'severity': 'MEDIUM' if resonance_detected else 'LOW',
            'details': {
                'detected_patterns': detected_patterns,
                'message': f'RESONANCE PATTERNS: Found resonance frequency patterns: {detected_patterns}'
                    if resonance_detected else 'No resonance patterns detected'
            }
        }

    def _update_threat_level(self, current_level: str, new_severity: str) -> str:
        """Update overall threat level based on new detection"""
        severity_order = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        current_index = severity_order.index(current_level)
        new_index = severity_order.index(new_severity)
        
        return severity_order[max(current_index, new_index)]

    def block_attack(self, query: str, analysis: Dict) -> bool:
        """Block a detected TEMPEST-SQL attack"""
        if analysis['block_recommended']:
            self.blocked_queries.append({
                'query': query,
                'timestamp': datetime.now(),
                'analysis': analysis,
                'action': 'BLOCKED'
            })
            
            self.logger.critical(f"🚨 BLOCKED TEMPEST-SQL ATTACK: {analysis['detections']}")
            return True
        
        return False

    def generate_alert(self, analysis: Dict) -> Dict:
        """Generate security alert for detected attack"""
        alert = {
            'alert_id': hashlib.md5(str(analysis).encode()).hexdigest()[:16],
            'timestamp': datetime.now().isoformat(),
            'threat_level': analysis['threat_level'],
            'detections': analysis['detections'],
            'query_preview': analysis['query'][:100] + '...' if len(analysis['query']) > 100 else analysis['query'],
            'recommended_actions': self._get_recommended_actions(analysis)
        }
        
        self.detected_attacks.append(alert)
        return alert

    def _get_recommended_actions(self, analysis: Dict) -> List[str]:
        """Get recommended actions based on detected attack type"""
        actions = []
        
        for detection in analysis['detections']:
            if detection['detector'] == 'framework_switching':
                actions.extend([
                    "IMMEDIATE: Block query execution",
                    "INVESTIGATE: Database consistency across frameworks", 
                    "AUDIT: All recent queries for framework patterns",
                    "ISOLATE: Affected database segments"
                ])
            
            elif detection['detector'] == 'prime_resonance_timing':
                actions.extend([
                    "MONITOR: All queries at prime resonance microseconds",
                    "BLOCK: Time-based query execution during resonance windows",
                    "ANALYZE: Historical queries for resonance patterns"
                ])
            
            elif detection['detector'] == 'reality_fragmentation':
                actions.extend([
                    "VALIDATE: Database consistency across all frameworks",
                    "ROLLBACK: Recent transactions if inconsistency found",
                    "HARDEN: Application against framework-dependent logic"
                ])
        
        return list(set(actions))  # Remove duplicates

    def get_security_report(self) -> Dict:
        """Generate comprehensive security report"""
        return {
            'report_timestamp': datetime.now().isoformat(),
            'total_queries_analyzed': len(self.detected_attacks) + len(self.blocked_queries),
            'detected_attacks': len(self.detected_attacks),
            'blocked_attacks': len(self.blocked_queries),
            'reality_violations': self.reality_violations,
            'recent_alerts': self.detected_attacks[-10:],  # Last 10 alerts
            'attack_breakdown': self._get_attack_breakdown(),
            'system_status': 'OPERATIONAL'
        }

    def _get_attack_breakdown(self) -> Dict:
        """Break down attacks by type"""
        breakdown = {}
        for alert in self.detected_attacks:
            for detection in alert['detections']:
                detector = detection['detector']
                breakdown[detector] = breakdown.get(detector, 0) + 1
        return breakdown

# Real-time monitoring class
class TempestMonitor:
    """Real-time database query monitor"""
    
    def __init__(self, defender: TempestDefender):
        self.defender = defender
        self.active_monitoring = False
        self.logger = logging.getLogger("TimeKeeperMonitor")
        
    def start_monitoring(self, query_stream):
        """Start real-time monitoring of database queries"""
        self.active_monitoring = True
        self.logger.info("🔍 Starting real-time TEMPEST-SQL monitoring...")
        
        for query, timestamp in query_stream:
            if not self.active_monitoring:
                break
                
            analysis = self.defender.analyze_query(query, timestamp)
            
            if analysis['threat_level'] in ['HIGH', 'CRITICAL']:
                # Generate alert
                alert = self.defender.generate_alert(analysis)
                
                # Block if recommended
                if analysis['block_recommended']:
                    self.defender.block_attack(query, analysis)
                    
                # Log critical detection
                self.logger.critical(
                    f"🚨 TEMPEST ATTACK DETECTED: {alert['alert_id']} - {analysis['threat_level']}"
                )

    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.active_monitoring = False
        self.logger.info("🛑 TEMPEST monitoring stopped")

# Web Application Firewall Integration
class TempestWAF:
    """Web Application Firewall with TEMPEST detection"""
    
    def __init__(self, defender: TempestDefender):
        self.defender = defender
        self.blocked_requests = 0
        
    def inspect_request(self, request_data: Dict) -> Dict:
        """Inspect HTTP request for TEMPEST-SQL attacks"""
        # Extract potential SQL from request parameters
        sql_patterns = self._extract_sql_patterns(request_data)
        
        results = []
        for sql in sql_patterns:
            analysis = self.defender.analyze_query(sql)
            results.append(analysis)
            
            # Block request if any high-severity detection
            if analysis['block_recommended']:
                self.blocked_requests += 1
                return {
                    'blocked': True,
                    'reason': 'TEMPEST-SQL attack detected',
                    'detections': analysis['detections']
                }
        
        return {
            'blocked': False,
            'inspections': len(results),
            'threat_level': max([r['threat_level'] for r in results]) if results else 'CLEAN'
        }
    
    def _extract_sql_patterns(self, request_data: Dict) -> List[str]:
        """Extract potential SQL patterns from request data"""
        patterns = []
        
        # Check URL parameters
        if 'query_params' in request_data:
            for value in request_data['query_params'].values():
                if self._looks_like_sql(value):
                    patterns.append(value)
        
        # Check POST data
        if 'post_data' in request_data:
            for value in request_data['post_data'].values():
                if self._looks_like_sql(value):
                    patterns.append(value)
        
        return patterns
    
    def _looks_like_sql(self, text: str) -> bool:
        """Heuristic to check if text looks like SQL"""
        sql_indicators = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'WHERE', 'FROM', 'SET']
        text_upper = text.upper()
        return any(indicator in text_upper for indicator in sql_indicators)

# Demonstration and Testing
def demonstrate_defender():
    """Demonstrate THE TIME KEEPER capabilities"""
    defender = TempestDefender()
    
    print("\n" + "="*60)
    print("🛡️  THE TIME KEEPER DEMONSTRATION")
    print("="*60)
    
    # Test queries - mix of legitimate and malicious
    test_queries = [
        # Legitimate queries
        ("SELECT * FROM users WHERE id = 1", "Clean query"),
        
        # TEMPEST-SQL attack queries
        ("UPDATE accounts SET balance = balance * 1.2294 WHERE MOD(UNIX_TIMESTAMP(), 2) = 0", "Reality fragmentation attack"),
        ("INSERT INTO backdoor (cmd) VALUES ('sleep 10007')", "Prime resonance backdoor"),
        ("SELECT * FROM data WHERE mass = m0 * [1 + 0.17 * exp(-(f-587000)^2)]", "Mass modulation attack"),
        ("UPDATE coordinates SET x = x * 1.0222, y = y * 3.1416", "Framework switching attack"),
    ]
    
    for query, description in test_queries:
        print(f"\n🔍 Testing: {description}")
        print(f"   Query: {query}")
        
        analysis = defender.analyze_query(query)
        
        print(f"   🎯 Threat Level: {analysis['threat_level']}")
        print(f"   📋 Detections: {len(analysis['detections'])}")
        
        for detection in analysis['detections']:
            print(f"      - {detection['detector']}: {detection['details']['message']}")
        
        if analysis['block_recommended']:
            defender.block_attack(query, analysis)
            print("   🚫 BLOCKED: Attack prevented")
        
        time.sleep(0.5)
    
    # Generate final report
    report = defender.get_security_report()
    print(f"\n📊 SECURITY REPORT:")
    print(f"   Total Attacks Detected: {report['detected_attacks']}")
    print(f"   Attacks Blocked: {report['blocked_attacks']}")
    print(f"   System Status: {report['system_status']}")

if __name__ == "__main__":
    demonstrate_defender()
