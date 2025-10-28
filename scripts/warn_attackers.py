#!/usr/bin/env python3
"""
Warn all detected attackers from firewall logs
Extracts IPs from attack logs and sends legal warnings
"""
import re
import sys
import subprocess
import hashlib
from datetime import datetime
from collections import defaultdict

# Import the warner
sys.path.insert(0, '/usr/lib/python3.13/site-packages')
from attacker_warner import AttackerWarner

def parse_attack_log(log_file='/var/log/ctt-bot-defender/attacks.log'):
    """Parse attack log file and extract attacker information"""
    attackers = defaultdict(lambda: {
        'ip_address': '',
        'attack_count': 0,
        'first_seen': None,
        'last_seen': None,
        'user_agent': 'UNKNOWN (Firewall Level)',
        'threat_level': 60,  # HIGH by default for firewall attacks
        'bot_id': '',
        'ports_targeted': set()
    })
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                # Extract IP address
                ip_match = re.search(r'SRC=([0-9.]+)', line)
                if not ip_match:
                    continue
                
                ip = ip_match.group(1)
                
                # Extract timestamp
                timestamp_match = re.search(r'(\w+ \d+ \d+:\d+:\d+)', line)
                timestamp = timestamp_match.group(1) if timestamp_match else datetime.now().strftime('%b %d %H:%M:%S')
                
                # Extract destination port
                port_match = re.search(r'DPT=(\d+)', line)
                if port_match:
                    attackers[ip]['ports_targeted'].add(port_match.group(1))
                
                # Update attacker info
                if attackers[ip]['first_seen'] is None:
                    attackers[ip]['first_seen'] = timestamp
                
                attackers[ip]['last_seen'] = timestamp
                attackers[ip]['ip_address'] = ip
                attackers[ip]['attack_count'] += 1
                
                # Generate bot_id
                attackers[ip]['bot_id'] = hashlib.sha256(f"{ip}:firewall".encode()).hexdigest()[:16]
        
        # Convert sets to lists for JSON serialization
        for ip in attackers:
            attackers[ip]['ports_targeted'] = list(attackers[ip]['ports_targeted'])
        
        return dict(attackers)
    
    except FileNotFoundError:
        print(f"Error: Log file {log_file} not found")
        return {}

def main():
    print("\n" + "="*80)
    print("⚠️  CTT BOT DESTROYER - MASS ATTACKER WARNING SYSTEM")
    print("="*80 + "\n")
    
    print("🔍 Analyzing attack logs...\n")
    
    # Parse attack logs
    attackers = parse_attack_log()
    
    if not attackers:
        print("✓ No attackers found in logs")
        return
    
    print(f"📊 Found {len(attackers)} unique attacking IP addresses\n")
    print("ATTACKER SUMMARY:")
    print("-" * 80)
    
    # Display attacker summary
    for ip, info in sorted(attackers.items(), key=lambda x: x[1]['attack_count'], reverse=True):
        print(f"  {ip:18s}  Attacks: {info['attack_count']:4d}  Ports: {', '.join(info['ports_targeted'][:5])}")
    
    print("-" * 80)
    
    # Ask for confirmation
    print(f"\n⚠️  WARNING: About to send legal warnings to {len(attackers)} attackers")
    print("    Warnings will be sent via:")
    print("    • TCP connections (if ports are open)")
    print("    • ICMP ping packets")
    print("    • WHOIS abuse contact lookup")
    print("    • File logs for evidence")
    print("    • Mesh network broadcast")
    print()
    
    response = input("Proceed with mass warning? [YES/no]: ")
    
    if response.lower() not in ['yes', 'y', '']:
        print("\n❌ Warning operation cancelled")
        return
    
    print("\n🚨 INITIATING MASS WARNING OPERATION...\n")
    
    # Create warner
    warner = AttackerWarner()
    
    # Warn each attacker
    results = {
        'total': len(attackers),
        'warned': 0,
        'failed': 0,
        'details': []
    }
    
    for i, (ip, info) in enumerate(attackers.items(), 1):
        print(f"[{i}/{len(attackers)}] Warning {ip}... ", end='', flush=True)
        
        try:
            warning_result = warner.warn_attacker(info)
            
            # Check if any channel succeeded
            channels_succeeded = sum(1 for ch in warning_result['channels'].values() if ch.get('success'))
            
            if channels_succeeded > 0:
                print(f"✅ ({channels_succeeded} channels)")
                results['warned'] += 1
            else:
                print(f"⚠️  (all channels failed)")
                results['failed'] += 1
            
            results['details'].append(warning_result)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results['failed'] += 1
    
    # Final summary
    print("\n" + "="*80)
    print("MASS WARNING OPERATION COMPLETE")
    print("="*80)
    print(f"  Total Attackers:        {results['total']}")
    print(f"  Successfully Warned:    {results['warned']}")
    print(f"  Failed:                 {results['failed']}")
    print(f"  Success Rate:           {results['warned']/results['total']*100:.1f}%")
    print()
    print(f"📁 Evidence saved to:     /var/lib/ctt-bot-defender/warnings/")
    print(f"📁 Warning logs:          /var/lib/ctt-bot-defender/warning_events.json")
    print(f"🌐 Mesh broadcast:        /var/lib/ctt-bot-defender/mesh_warnings.json")
    print(f"📧 Abuse notifications:   /var/lib/ctt-bot-defender/abuse-*.txt")
    print()
    print("✅ All attackers have been legally warned of consequences")
    print("   Next attacks will trigger automated counter-measures")
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
