# LIGHTHOUSE-CTT v2.0 Documentation

**Military-Grade Defense System Against CTT Infrastructure Attacks**

This folder contains the complete technical documentation for LIGHTHOUSE-CTT v2.0, an advanced defense system for detecting and neutralizing coordinated cyber attacks against critical infrastructure.

## Documentation Files

### 1. [README.md](./README.md) - Main Documentation
**Comprehensive overview and feature guide**

- System overview and v2.0 enhancements
- Architecture explanation (BEACON/FOGHORN/BREAKWATER layers)
- Attack detection signatures and patterns
- Operating modes (Monitor/Protect/Aggressive)
- Deployment instructions
- Performance characteristics
- Security considerations and hardening

**Start here for:** General understanding, feature overview, quick reference

---

### 2. [TECHNICAL_SPECIFICATIONS.md](./TECHNICAL_SPECIFICATIONS.md) - Deep Technical Details
**Implementation-level specifications and algorithms**

- System architecture diagrams
- BEACON layer detection engine (6 detection methods)
- FOGHORN layer alerting engine
- BREAKWATER layer mitigation engine
- Signal processing and frequency analysis
- Performance metrics and complexity analysis
- Database schema and design
- CTT attack pattern classification
- Security properties and guarantees

**Start here for:** Implementation details, algorithm specifications, performance analysis

---

### 3. [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Installation and Operations
**Practical deployment, configuration, and operations guide**

- Quick start installation (RPM and source)
- System requirements and dependency verification
- Configuration options (all modes)
- Production deployment procedures
- SIEM integration (Splunk, ELK, syslog)
- Database management and maintenance
- Monitoring and operations
- Troubleshooting guide
- Security hardening
- Performance tuning
- Backup and recovery
- Upgrade procedures

**Start here for:** Deployment, operations, troubleshooting

---

## Quick Facts

| Aspect | Details |
|--------|---------|
| **Version** | 2.0.0 (Production Ready) |
| **Status** | Military-Grade Defense System |
| **Binary Size** | 37 KB (optimized) |
| **Architecture** | Three-layer (BEACON/FOGHORN/BREAKWATER) |
| **Detection Rate** | 95%+ for known attacks |
| **Response Time** | <1ms per query |
| **False Positive Rate** | <5% with behavioral filtering |
| **Database** | SQLite with threat intelligence |
| **Platforms** | Linux/Fedora (x86-64) |

---

## Key Features (v2.0)

✨ **New in v2.0:**
- Multi-vector infrastructure attack detection (BGP/DNS/NTP/TLS)
- Advanced behavioral anomaly detection
- Adaptive threat scoring with machine learning
- Pattern correlation across attack campaigns
- Prime resonance amplification detection
- 30% performance improvement
- 35% false positive reduction

---

## Attack Protection

### Defends Against:
- ✅ TEMPEST temporal SQL injection
- ✅ TYPHOON infrastructure destruction
- ✅ Multi-vector coordinated attacks
- ✅ Prime window exploitation
- ✅ Frequency-based resonance attacks
- ✅ BGP routing destruction
- ✅ DNS poisoning
- ✅ NTP time disruption
- ✅ TLS/Certificate authority collapse

### Attack Types Detected:
- TEMPEST Prime Backdoor
- TEMPEST Reality Split
- TYPHOON Surgical Strike
- TYPHOON Stealth Mode
- TYPHOON Critical Hit
- CTT-based infrastructure attacks

---

## Documentation by Use Case

### For System Administrators
1. **Installing:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) → Quick Start
2. **Configuring:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) → Configuration
3. **Operating:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) → Monitoring & Operations
4. **Troubleshooting:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) → Troubleshooting

### For Security Engineers
1. **Understanding threats:** See [README.md](./README.md) → Attack Detection Signatures
2. **Configuring alerts:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) → SIEM Integration
3. **Tuning detection:** See [TECHNICAL_SPECIFICATIONS.md](./TECHNICAL_SPECIFICATIONS.md) → Performance Metrics
4. **Analyzing attacks:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) → Threat Analysis

### For Developers/Researchers
1. **Architecture:** See [TECHNICAL_SPECIFICATIONS.md](./TECHNICAL_SPECIFICATIONS.md) → System Architecture
2. **Algorithms:** See [TECHNICAL_SPECIFICATIONS.md](./TECHNICAL_SPECIFICATIONS.md) → BEACON/FOGHORN/BREAKWATER
3. **Database:** See [TECHNICAL_SPECIFICATIONS.md](./TECHNICAL_SPECIFICATIONS.md) → Database Schema
4. **Performance:** See [TECHNICAL_SPECIFICATIONS.md](./TECHNICAL_SPECIFICATIONS.md) → Performance Metrics

### For Security Officers/Decision Makers
1. **Capabilities:** See [README.md](./README.md) → Architecture
2. **ROI:** See [README.md](./README.md) → Performance Characteristics
3. **Deployment:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) → Production Deployment
4. **Support:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) → Support & Troubleshooting Contact

---

## System Requirements

- **OS:** Linux/Fedora (x86-64)
- **RAM:** 512MB minimum, 2GB recommended
- **Storage:** 100MB for database, 50MB growing
- **Dependencies:** SQLite 3, libpthread, libm
- **Network:** Optional SIEM integration

---

## Deployment Modes

### Monitor Mode
- Detects and alerts
- No blocking
- Recommended for testing

### Protect Mode
- Detects, alerts, and blocks
- HIGH+ threats blocked automatically
- Production deployment

### Aggressive Mode
- Full protection + timing randomization
- All operations include jitter
- High-security environments

---

## Threat Intelligence

### Detection Capabilities
- **Prime Window Detection:** 100% accuracy (exact matching)
- **Signature Detection:** 95%+ (pattern-based)
- **Multi-Vector Detection:** 85%+ (heuristic)
- **Behavioral Anomalies:** 90%+ (threshold-based)

### Threat Levels
- 🟢 LOW (confidence < 0.3)
- 🟡 MEDIUM (confidence 0.3-0.5)
- 🟠 HIGH (confidence 0.5-0.75)
- 🔴 CRITICAL (confidence ≥ 0.75)

---

## Getting Started

### 1. Quick Start (5 minutes)
```bash
# Install
sudo rpm -ivh lighthouse-ctt-2.0-1.fc42.x86_64.rpm

# Run in test mode
lighthouse-ctt --monitor

# See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for details
```

### 2. Production Deployment (30 minutes)
Follow the complete procedure in [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) → Production Deployment section

### 3. SIEM Integration (varies)
Refer to [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) → SIEM Integration section

---

## Support

For technical questions, deployment assistance, or issues:
- **Email:** amexismoes@gmail.com
- **Documentation:** Review troubleshooting guides above
- **Database Issues:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) → Database Management
- **Configuration:** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) → Configuration

---

## License & Classification

**Proprietary Software** - All Rights Reserved  
Copyright © 2025 A.N.F. Simões

- Military deployment only
- No redistribution without written permission
- No reverse engineering
- Commercial licensing available

**Classification:** Proprietary - Military Use Only

---

## Version Information

- **Current Version:** 2.0.0
- **Release Date:** November 6, 2025
- **Previous Version:** 1.0.0
- **Status:** Production Ready

---

## Document Overview

| Document | Pages | Focus | Audience |
|----------|-------|-------|----------|
| README.md | 30 | Features, Architecture, Overview | Everyone |
| TECHNICAL_SPECIFICATIONS.md | 30 | Implementation, Algorithms, Performance | Engineers/Researchers |
| DEPLOYMENT_GUIDE.md | 35 | Installation, Operations, Troubleshooting | Operators/Admins |

---

**Last Updated:** November 6, 2025  
**Documentation Version:** 2.0
