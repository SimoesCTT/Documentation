#!/usr/bin/env python3
"""
CTT Bot Defender - Main Service
Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
"""
import time
import logging
import sys
import argparse
from bot_detector import BotDetector
from network_monitor import NetworkMonitor
from defense_actions import DefenseActions

class CTTBotDefender:
    """Main bot defender service"""
    
    def __init__(self, scan_interval=10):
        self.scan_interval = scan_interval
        self.running = False
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('CTTBotDefender')
        
        # Initialize components
        self.logger.info("🤖💀 CTT BOT DEFENDER INITIALIZING")
        self.detector = BotDetector()
        self.monitor = NetworkMonitor()
        self.defense = DefenseActions()
        
        self.logger.info("✅ All systems operational")
    
    def start(self):
        """Start the defense service"""
        self.running = True
        self.logger.info("🛡️  CTT BOT DEFENDER STARTED - Active Defense Mode")
        self.logger.info(f"   Scan interval: {self.scan_interval} seconds")
        
        report_counter = 0
        
        try:
            while self.running:
                # Monitor active connections
                connections = self.monitor.get_active_connections()
                
                for conn in connections:
                    self._analyze_and_respond(
                        ip=conn['ip'],
                        user_agent=f"tcp_connection:{conn['state']}",
                        endpoint='',
                        method='TCP'
                    )
                
                # Monitor HTTP logs (if available)
                http_requests = self.monitor.monitor_http_access()
                for req in http_requests:
                    self._analyze_and_respond(
                        ip=req['ip'],
                        user_agent=req['user_agent'],
                        endpoint=req['endpoint'],
                        method=req['method']
                    )
                
                # Monitor port scans
                scans = self.monitor.monitor_port_scans()
                for scan in scans:
                    self._analyze_and_respond(
                        ip=scan['ip'],
                        user_agent=f"port_scan:{scan['port']}",
                        endpoint=f"/port:{scan['port']}",
                        method='SCAN'
                    )
                
                # Generate report every 5 minutes
                report_counter += self.scan_interval
                if report_counter >= 300:
                    self._generate_report()
                    report_counter = 0
                
                time.sleep(self.scan_interval)
        
        except KeyboardInterrupt:
            self.logger.info("🛑 Shutdown requested")
        except Exception as e:
            self.logger.error(f"Fatal error: {e}", exc_info=True)
        finally:
            self.stop()
    
    def _analyze_and_respond(self, ip, user_agent='', endpoint='', method='', payload=''):
        """Analyze connection and take appropriate action"""
        try:
            # Analyze the connection
            analysis = self.detector.analyze_connection(
                ip=ip,
                user_agent=user_agent,
                endpoint=endpoint,
                method=method,
                payload=payload
            )
            
            # If threat detected, log it
            if analysis['is_threat']:
                self.logger.warning(
                    f"⚠️  THREAT DETECTED: {ip} - "
                    f"Score: {analysis['bot_score']} - "
                    f"Level: {analysis['threat_level']} - "
                    f"Detections: {', '.join(analysis['detections'])}"
                )
                
                # Get full bot info
                bot_info = self.detector.get_bot_info(analysis['bot_id'])
                if not bot_info:
                    bot_info = {
                        'ip': ip,
                        'user_agent': user_agent,
                        'bot_id': analysis['bot_id'],
                        'bot_score': analysis['bot_score'],
                        'threat_level': analysis['threat_level'],
                        'detections': ','.join(analysis['detections'])
                    }
                
                # Issue warning if threshold met
                if analysis['should_warn']:
                    self.defense.warn_attacker(bot_info)
                
                # Launch counter-attack if HIGH/CRITICAL
                if analysis['should_attack']:
                    result = self.defense.counter_attack(bot_info)
                    if result['success']:
                        self.logger.critical(
                            f"💥 COUNTER-ATTACK SUCCESSFUL: {ip} - "
                            f"Method: {result.get('method')}"
                        )
                    else:
                        self.logger.warning(
                            f"⚠️  Counter-attack logged for manual execution: {ip}"
                        )
        
        except Exception as e:
            self.logger.error(f"Error analyzing {ip}: {e}")
    
    def _generate_report(self):
        """Generate and log statistics report"""
        try:
            stats = self.detector.get_statistics()
            self.logger.info(
                f"📊 REPORT: {stats['total_bots']} bots detected, "
                f"{stats['high_threats']} HIGH/CRITICAL, "
                f"{stats['total_attacks']} total attacks"
            )
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
    
    def stop(self):
        """Stop the defense service"""
        self.running = False
        self.logger.info("🛑 CTT BOT DEFENDER STOPPED")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='CTT Bot Defender - Autonomous Active Defense System'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=10,
        help='Scan interval in seconds (default: 10)'
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("🤖💀 CTT BOT DESTROYER v2.0 - Autonomous Active Defense")
    print("   Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.")
    print("   ACTIVE DEFENSE MODE - Warnings & Counter-Attacks Enabled")
    print("="*70)
    print()
    
    defender = CTTBotDefender(scan_interval=args.interval)
    defender.start()


if __name__ == '__main__':
    main()
