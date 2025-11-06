# LIGHTHOUSE-CTT v2.0 - Deployment Guide

## Quick Start

### Installation from RPM

```bash
# Install binary package
sudo rpm -ivh lighthouse-ctt-2.0-1.fc42.x86_64.rpm

# Verify installation
lighthouse-ctt --help
```

### Installation from Source

```bash
# Clone/extract source
cd lighthouse-ctt

# Compile
make clean && make

# Install system-wide
sudo make install

# Verify
lighthouse-ctt --help
```

---

## Pre-Deployment Checklist

### System Requirements

- [ ] Linux/Fedora OS (x86-64)
- [ ] 512MB+ RAM available
- [ ] 100MB+ disk space for database
- [ ] SQLite 3 library installed
- [ ] libpthread support
- [ ] Root or sudo access (for firewall integration)

### Dependency Verification

```bash
# Check SQLite
sqlite3 --version

# Check required libraries
ldd /usr/local/bin/lighthouse-ctt

# Expected output:
# linux-vdso.so.1 (0x...)
# libsqlite3.so.0 (0x...)
# libpthread.so.0 (0x...)
# libm.so.6 (0x...)
# libc.so.6 (0x...)
```

### Install Dependencies (if needed)

```bash
# Fedora/RHEL
sudo dnf install -y sqlite sqlite-devel glibc-devel

# Ubuntu/Debian
sudo apt-get install -y sqlite3 libsqlite3-dev build-essential
```

---

## Configuration

### Basic Configuration

#### Monitor Mode (Recommended for Testing)

```bash
# Start in monitor-only mode (no blocking)
lighthouse-ctt --monitor

# Output: Detects threats and prints alerts, but doesn't block
```

#### Protect Mode (Production)

```bash
# Start in protection mode (with blocking)
lighthouse-ctt --protect

# Blocks HIGH and above threats automatically
# Isolates CRITICAL threats by IP
```

#### Aggressive Mode (High-Security)

```bash
# Start in aggressive mode (full protection + jitter)
lighthouse-ctt --protect --aggressive

# Maximum defense posture
# All timing operations include randomization
# Best for high-value targets
```

### Advanced Configuration

#### With Logging

```bash
# Enable file logging
lighthouse-ctt --protect --log /var/log/lighthouse.log

# Follow logs in real-time
tail -f /var/log/lighthouse.log
```

#### With Custom Database

```bash
# Use custom database location
lighthouse-ctt --protect --db /var/lib/lighthouse/threats.db

# Database is created automatically if it doesn't exist
```

#### Full Command Example

```bash
lighthouse-ctt --protect --aggressive \
  --log /var/log/lighthouse.log \
  --db /var/lib/lighthouse/threats.db
```

---

## Production Deployment

### Step 1: Create Service Account

```bash
# Create unprivileged user
sudo useradd -r -s /bin/false lighthouse

# Create directories
sudo mkdir -p /var/lib/lighthouse
sudo mkdir -p /var/log/lighthouse
sudo chown lighthouse:lighthouse /var/lib/lighthouse
sudo chown lighthouse:lighthouse /var/log/lighthouse
sudo chmod 750 /var/lib/lighthouse
sudo chmod 750 /var/log/lighthouse
```

### Step 2: Create Systemd Service

Create `/etc/systemd/system/lighthouse.service`:

```ini
[Unit]
Description=LIGHTHOUSE-CTT Defense System
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=lighthouse
Group=lighthouse
ExecStart=/usr/local/bin/lighthouse-ctt --protect --aggressive \
  --log /var/log/lighthouse/alerts.log \
  --db /var/lib/lighthouse/threats.db

Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security
NoNewPrivileges=true
PrivateTmp=true
ReadOnlyPaths=/
ReadWritePaths=/var/lib/lighthouse /var/log/lighthouse

[Install]
WantedBy=multi-user.target
```

### Step 3: Enable and Start Service

```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Enable service (auto-start)
sudo systemctl enable lighthouse

# Start service
sudo systemctl start lighthouse

# Check status
sudo systemctl status lighthouse

# View logs
sudo journalctl -u lighthouse -f
```

### Step 4: Firewall Integration

#### Dynamic Blacklist with iptables

```bash
# Create firewall rule that references Lighthouse blacklist
sudo iptables -N LIGHTHOUSE_BLOCK 2>/dev/null || true
sudo iptables -A INPUT -j LIGHTHOUSE_BLOCK

# Script to periodically update blacklist (/usr/local/bin/update_lighthouse_blacklist.sh)
#!/bin/bash
# Update iptables with latest blacklist from Lighthouse

BLACKLIST_FILE="/tmp/lighthouse_blacklist.txt"
BLACKLIST_CHAIN="LIGHTHOUSE_BLOCK"

# Clear existing rules
sudo iptables -F $BLACKLIST_CHAIN

# Add new rules from blacklist
while read line; do
    if [[ $line == *"BLOCKED:"* ]]; then
        IP=$(echo $line | awk '{print $NF}')
        sudo iptables -A $BLACKLIST_CHAIN -s $IP -j DROP
    fi
done < $BLACKLIST_FILE

# Persist rules
sudo iptables-save | sudo tee /etc/iptables/rules.v4
```

#### Make Rules Persistent

```bash
# Fedora/RHEL
sudo dnf install -y iptables-services
sudo systemctl restart iptables

# Ubuntu/Debian
sudo apt-get install -y iptables-persistent
sudo iptables-save | sudo tee /etc/iptables/rules.v4
```

---

## SIEM Integration

### Splunk Integration

Create `/etc/rsyslog.d/50-lighthouse.conf`:

```
:programname, isequal, "lighthouse" @@splunk-server.example.com:514
```

### ELK Stack Integration

Create Filebeat config `/etc/filebeat/filebeat.yml`:

```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/lighthouse/*.log
  fields:
    source: lighthouse
    severity: high

output.elasticsearch:
  hosts: ["elasticsearch:9200"]

processors:
  - add_kubernetes_metadata:
  - add_docker_metadata:
```

### Generic Syslog Integration

```bash
# Forward logs to central syslog server
sudo tee -a /etc/rsyslog.d/50-lighthouse.conf <<'EOF'
:programname, isequal, "lighthouse" @@syslog-server.example.com:514
EOF

# Restart rsyslog
sudo systemctl restart rsyslog
```

---

## Database Management

### Initial Setup

```bash
# Check if database exists
sqlite3 /var/lib/lighthouse/threats.db ".tables"

# If empty, Lighthouse will auto-initialize on first run
lighthouse-ctt --protect --db /var/lib/lighthouse/threats.db
```

### Monitoring Database

```bash
# Check current threat count
sqlite3 /var/lib/lighthouse/threats.db \
  "SELECT COUNT(*) as total_threats FROM threats;"

# Check threats by source IP
sqlite3 /var/lib/lighthouse/threats.db \
  "SELECT source_ip, COUNT(*) as count FROM threats GROUP BY source_ip ORDER BY count DESC;"

# Check recent critical threats
sqlite3 /var/lib/lighthouse/threats.db \
  "SELECT timestamp, source_ip, attack_type FROM threats WHERE threat_level=4 ORDER BY timestamp DESC LIMIT 10;"
```

### Database Maintenance

```bash
# Vacuum database (optimize space)
sqlite3 /var/lib/lighthouse/threats.db "VACUUM;"

# Clean old events (>30 days)
sqlite3 /var/lib/lighthouse/threats.db \
  "DELETE FROM threats WHERE timestamp < datetime('now', '-30 days');"

# Rebuild indexes
sqlite3 /var/lib/lighthouse/threats.db \
  "REINDEX idx_source_ip; REINDEX idx_timestamp; REINDEX idx_attack_type;"

# Check database size
du -h /var/lib/lighthouse/threats.db
```

---

## Monitoring & Operations

### Real-Time Monitoring

```bash
# Watch live alerts
tail -f /var/log/lighthouse/alerts.log

# Count alerts by threat level
grep "THREAT LEVEL" /var/log/lighthouse/alerts.log | sort | uniq -c

# Extract critical threats only
grep "🔴 CRITICAL" /var/log/lighthouse/alerts.log
```

### Threat Analysis

```bash
# Get attack patterns
sqlite3 /var/lib/lighthouse/threats.db <<'EOF'
SELECT 
  source_ip,
  COUNT(*) as attack_count,
  COUNT(DISTINCT attack_type) as attack_types,
  MAX(timestamp) as last_seen
FROM threats
WHERE timestamp > datetime('now', '-1 hour')
GROUP BY source_ip
ORDER BY attack_count DESC;
EOF

# Get most common attack types
sqlite3 /var/lib/lighthouse/threats.db \
  "SELECT attack_type, COUNT(*) as count FROM threats GROUP BY attack_type ORDER BY count DESC;"
```

### Performance Metrics

```bash
# Check database query performance
sqlite3 /var/lib/lighthouse/threats.db ".timer ON"

# Run correlation query (typical <10ms)
SELECT COUNT(*) FROM threats 
WHERE source_ip = '192.168.1.1' 
AND timestamp > datetime('now', '-1 hour');

# Check index usage
sqlite3 /var/lib/lighthouse/threats.db ".explain on"
```

---

## Troubleshooting

### Issue: High CPU Usage

**Symptoms:** `lighthouse-ctt` consuming >50% CPU

**Solutions:**

```bash
# 1. Check current threat count
sqlite3 /var/lib/lighthouse/threats.db "SELECT COUNT(*) FROM threats;"

# 2. Clean old records if >100K events
sqlite3 /var/lib/lighthouse/threats.db \
  "DELETE FROM threats WHERE timestamp < datetime('now', '-7 days');"

# 3. Rebuild indexes
sqlite3 /var/lib/lighthouse/threats.db "REINDEX;"

# 4. Vacuum database
sqlite3 /var/lib/lighthouse/threats.db "VACUUM;"

# 5. Restart service
sudo systemctl restart lighthouse
```

### Issue: Missing Detections

**Symptoms:** Known attacks not being detected

**Solutions:**

```bash
# 1. Check if running in monitor mode (not protect)
ps aux | grep lighthouse

# 2. Verify database is writable
ls -la /var/lib/lighthouse/threats.db

# 3. Check logs for errors
tail -100 /var/log/lighthouse/alerts.log

# 4. Test in monitor mode first
lighthouse-ctt --monitor

# 5. Verify binary is v2.0
/usr/local/bin/lighthouse-ctt --help | grep version
```

### Issue: High False Positives

**Symptoms:** Many LOW/MEDIUM threats from legitimate sources

**Solutions:**

```bash
# 1. Run in monitor mode to understand baseline
lighthouse-ctt --monitor

# 2. Analyze false positive patterns
sqlite3 /var/lib/lighthouse/threats.db \
  "SELECT source_ip, COUNT(*) FROM threats WHERE threat_level < 3 GROUP BY source_ip;"

# 3. Lower confidence thresholds (edit beacon.c)
# Change: multi_vector_boost from 1.3 to 1.1
# Change: correlation_boost from 1.2 to 1.0

# 4. Recompile and redeploy
make clean && make
sudo make install
sudo systemctl restart lighthouse
```

### Issue: Database Corruption

**Symptoms:** SQLite errors, can't query database

**Solutions:**

```bash
# 1. Backup current database
cp /var/lib/lighthouse/threats.db /var/lib/lighthouse/threats.db.backup

# 2. Check integrity
sqlite3 /var/lib/lighthouse/threats.db "PRAGMA integrity_check;"

# 3. Attempt repair
sqlite3 /var/lib/lighthouse/threats.db ".dump" | sqlite3 /var/lib/lighthouse/threats.db.recovered

# 4. If repair fails, restore backup
cp /var/lib/lighthouse/threats.db.backup /var/lib/lighthouse/threats.db

# 5. Restart service
sudo systemctl restart lighthouse
```

---

## Security Hardening

### File Permissions

```bash
# Restrict binary
sudo chmod 755 /usr/local/bin/lighthouse-ctt

# Restrict database
sudo chmod 600 /var/lib/lighthouse/threats.db
sudo chown lighthouse:lighthouse /var/lib/lighthouse/threats.db

# Restrict logs
sudo chmod 640 /var/log/lighthouse/alerts.log
sudo chown lighthouse:lighthouse /var/log/lighthouse/alerts.log
```

### SELinux/AppArmor Profile

#### SELinux (example)

```bash
# Create policy
sudo semanage fcontext -a -t bin_t "/usr/local/bin/lighthouse-ctt"

# Apply
sudo restorecon /usr/local/bin/lighthouse-ctt

# Verify
ls -laZ /usr/local/bin/lighthouse-ctt
```

#### AppArmor (example)

Create `/etc/apparmor.d/usr.local.bin.lighthouse-ctt`:

```
#include <tunables/global>

/usr/local/bin/lighthouse-ctt {
  #include <abstractions/base>
  #include <abstractions/nameservice>

  /var/lib/lighthouse/** rw,
  /var/log/lighthouse/** rw,
  /tmp/lighthouse_blacklist.txt rw,
  
  deny /root/** r,
  deny /home/** r,
}
```

### Audit Logging

```bash
# Monitor lighthouse executable
sudo auditctl -w /usr/local/bin/lighthouse-ctt -p x -k lighthouse_exec

# Monitor database
sudo auditctl -w /var/lib/lighthouse/threats.db -p wa -k lighthouse_db

# View audit logs
sudo ausearch -k lighthouse_exec
sudo ausearch -k lighthouse_db
```

---

## Performance Tuning

### Database Optimization

```bash
# Enable WAL mode for better concurrency
sqlite3 /var/lib/lighthouse/threats.db "PRAGMA journal_mode=WAL;"

# Increase cache size
sqlite3 /var/lib/lighthouse/threats.db "PRAGMA cache_size=10000;"

# Set synchronous mode for performance (trade-off: less durability)
sqlite3 /var/lib/lighthouse/threats.db "PRAGMA synchronous=NORMAL;"

# Check settings
sqlite3 /var/lib/lighthouse/threats.db "PRAGMA journal_mode; PRAGMA cache_size; PRAGMA synchronous;"
```

### System Tuning

```bash
# Increase file descriptors
echo "lighthouse soft nofile 4096" | sudo tee -a /etc/security/limits.conf
echo "lighthouse hard nofile 8192" | sudo tee -a /etc/security/limits.conf

# Tune network buffer sizes
sudo sysctl -w net.core.rmem_max=134217728
sudo sysctl -w net.core.wmem_max=134217728
```

---

## Backup & Recovery

### Automated Backup

Create `/usr/local/bin/lighthouse-backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/lighthouse"
DB_PATH="/var/lib/lighthouse/threats.db"
RETENTION_DAYS=30

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
BACKUP_FILE="$BACKUP_DIR/threats-$(date +%Y%m%d-%H%M%S).db.gz"
sqlite3 $DB_PATH ".dump" | gzip > $BACKUP_FILE
echo "Backed up to $BACKUP_FILE"

# Clean old backups
find $BACKUP_DIR -name "*.db.gz" -mtime +$RETENTION_DAYS -delete

# Verify backup
if gunzip -t $BACKUP_FILE 2>/dev/null; then
    echo "Backup verified successfully"
else
    echo "ERROR: Backup verification failed!"
    exit 1
fi
```

Schedule with crontab:

```bash
# Backup daily at 2 AM
0 2 * * * /usr/local/bin/lighthouse-backup.sh
```

### Recovery Procedure

```bash
# List available backups
ls -lh /var/backups/lighthouse/

# Stop Lighthouse
sudo systemctl stop lighthouse

# Restore from backup
gunzip -c /var/backups/lighthouse/threats-20251105-020000.db.gz | sqlite3 /var/lib/lighthouse/threats.db.restore

# Verify restored database
sqlite3 /var/lib/lighthouse/threats.db.restore "SELECT COUNT(*) FROM threats;"

# Replace active database
sudo mv /var/lib/lighthouse/threats.db /var/lib/lighthouse/threats.db.corrupt
sudo mv /var/lib/lighthouse/threats.db.restore /var/lib/lighthouse/threats.db

# Restart Lighthouse
sudo systemctl start lighthouse

# Verify
sudo systemctl status lighthouse
```

---

## Upgrade Procedure

### From v1.0 to v2.0

```bash
# 1. Stop running instance
sudo systemctl stop lighthouse

# 2. Backup current database
cp /var/lib/lighthouse/threats.db /var/lib/lighthouse/threats.db.v1.backup

# 3. Install new version
sudo rpm -Uvh lighthouse-ctt-2.0-1.fc42.x86_64.rpm

# OR from source:
cd lighthouse-ctt
make clean && make
sudo make install

# 4. Start new version (uses same database)
sudo systemctl start lighthouse

# 5. Verify v2.0 is running
lighthouse-ctt --help | head -5

# 6. Check new features in alerts
tail -f /var/log/lighthouse/alerts.log

# You should see:
# - MULTI_VECTOR signatures
# - CORRELATED pattern tags
# - ANOMALY detections
```

---

## Uninstallation

```bash
# Stop service
sudo systemctl stop lighthouse

# Disable service
sudo systemctl disable lighthouse

# Remove binary
sudo rm /usr/local/bin/lighthouse-ctt

# Backup data before removal
mkdir -p /var/backups/lighthouse-removal
cp -r /var/lib/lighthouse /var/backups/lighthouse-removal/

# Remove files
sudo rm -rf /var/lib/lighthouse
sudo rm -rf /var/log/lighthouse
sudo rm -f /tmp/lighthouse_blacklist.txt

# Remove user
sudo userdel -r lighthouse

# Remove systemd service
sudo rm /etc/systemd/system/lighthouse.service
sudo systemctl daemon-reload

# Clean package manager (if installed via RPM)
sudo rpm -e lighthouse-ctt
```

---

## Support & Troubleshooting Contact

For issues or questions:

1. **Check logs:** `sudo journalctl -u lighthouse -n 100`
2. **Database integrity:** `sqlite3 /var/lib/lighthouse/threats.db "PRAGMA integrity_check;"`
3. **Configuration:** Review `/etc/systemd/system/lighthouse.service`
4. **Contact:** amexismoes@gmail.com

---

**Deployment Guide Version:** 2.0  
**Last Updated:** 2025-11-06  
**Classification:** Proprietary - Military Use Only
