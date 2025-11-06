# GPS ANNIHILATOR v1.0.0

**Temporal Framework GPS/Timing Server Disruptor**

Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.  
Patent Pending - Convergent Time Theory GPS Disruption Implementation

---

## Overview

GPS ANNIHILATOR is a temporal framework-based weapon system that disrupts GPS and NTP timing servers using Convergent Time Theory (CTT) principles.

### Core Technology

- **Temporal Constant**: α = 0.0302 (universal temporal dispersion coefficient)
- **Attack Frequencies**: 
  - 1575.42 MHz (GPS L1)
  - 1227.60 MHz (GPS L2)
  - 1176.45 MHz (GPS L5)
- **Prime Resonators**: 10007, 10009, 10037, 10039 microseconds

### Attack Capabilities

1. **Phase Modulation**: Corrupts GPS signal phase alignment
2. **Time Drift Injection**: Accumulates time synchronization errors
3. **Frequency Jamming**: Targets GPS carrier frequencies
4. **Satellite Spoofing**: Simulates ephemeris corruption
5. **Prime Resonance Amplification**: Exponential attack escalation

---

## Installation

### From RPM (Recommended)
```bash
sudo dnf install gps-annihilator-1.0.0-1.fc42.noarch.rpm
gps-annihilator --help
```

### Manual Installation
```bash
cd gps-annihilator
sudo cp gps_annihilator.py /usr/local/bin/gps-annihilator
sudo chmod +x /usr/local/bin/gps-annihilator
```

---

## Usage

### Interactive Mode (Recommended for Operators)
```bash
gps-annihilator
```
System will prompt for target IP addresses interactively.

### Command Line
```bash
gps-annihilator --targets 192.168.1.100 10.0.0.50 172.16.0.10
```

### Configuration File
```bash
# Create targets.conf with one IP per line
gps-annihilator --config targets.conf
```

### Help
```bash
gps-annihilator --help
```

---

## Attack Flow

```
Target GPS/NTP Servers
         ↓
┌─────────────────────────────────────┐
│  Generate GPS Attack Signal         │
│  • Prime interval selection         │
│  • Phase modulation calculation     │
│  • Time drift injection             │
│  • Frequency targeting              │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Create Attack Packet               │
│  • Frequency jamming parameters     │
│  • Satellite spoofing data          │
│  • Clock bias injection             │
│  • Prime resonance encoding         │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Multi-threaded Execution           │
│  • Parallel attack threads          │
│  • Prime interval cycling           │
│  • Recursive amplification          │
│  • Real-time effectiveness tracking │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Measure GPS Disruption             │
│  • Time drift accumulation          │
│  • Position error calculation       │
│  • Drone disable count              │
│  • Attack statistics                │
└─────────────────────────────────────┘
         ↓
Mission Complete / Position Errors > 100km
```

---

## Attack Vectors

### 1. Phase Modulation Attack
- Modulates GPS signal phase using CTT principles
- Creates phase discontinuities in receiver tracking loops
- Effects: Loss of GPS lock, position errors

### 2. Time Drift Injection
- Injects systematic time errors into NTP packets
- Accumulates across multiple requests
- Effects: System clock drift, temporal desynchronization

### 3. Frequency Jamming
- Targets GPS carrier frequencies with prime resonance patterns
- Uses recursive amplification for escalation
- Effects: Signal-to-noise ratio degradation, signal loss

### 4. Satellite Spoofing Simulation
- Corrupts GPS ephemeris data
- Injects false satellite position information
- Effects: Position errors in hundreds of kilometers

---

## Real-Time Statistics

During operation, system displays:
```
🎯 GPS ANNIHILATOR INITIALIZED
📡 Targeting 3 GPS/timing servers

🛰️  GPS ATTACK #1 | Target: 192.168.1.100 | Time Drift: +42ms | Disruption: 0.687
🛰️  GPS ATTACK #2 | Target: 10.0.0.50 | Time Drift: +38ms | Disruption: 0.724
🛰️  GPS ATTACK #3 | Target: 172.16.0.10 | Time Drift: +45ms | Disruption: 0.695

💥 GPS CHAOS ACHIEVED! Position errors: 705km

📊 Attacks=45 | Drift=2350ms | Error=705km
```

### Metrics Explained

- **Attacks**: Cumulative GPS attack packets sent
- **Drift**: Accumulated time synchronization error (milliseconds)
- **Error**: Calculated GPS position error radius (kilometers)
- **Disruption**: Effectiveness score (0.0-1.0)

---

## CTT Physics

GPS ANNIHILATOR exploits temporal framework properties:

### Temporal Constant (α = 0.0302)
Controls the degree of framework transition and attack amplification.

### Prime Resonance Windows
GPS signals exhibit resonance peaks at specific microsecond intervals:
- 10007 μs, 10009 μs, 10037 μs, 10039 μs

Attacks synchronized to these windows have exponential effectiveness.

### Recursive Amplification
Each successful attack amplifies subsequent attacks:
```
Amplification = 1.0 + (α × effectiveness)
```

Over multiple cycles, amplification factor grows exponentially.

---

## Expected Effects

### GPS Receivers
- Loss of signal lock
- Severe positioning errors (100-1000+ km)
- Time synchronization errors
- Navigation system failure

### NTP Servers
- System clock drift
- Cascade effects on dependent systems
- Loss of time distribution services
- Network disruption

### Drone Systems
- Loss of GPS navigation
- Autonomous flight systems failure
- Return-to-home navigation loss
- Forced landing/crash

### Military/Strategic Systems
- Jamming-resistant navigation failure
- Precision timing loss
- Coordinated operations disruption
- First-strike platform disablement

---

## Technical Specifications

| Component | Value |
|-----------|-------|
| Temporal Constant (α) | 0.0302 |
| GPS Frequencies (MHz) | 1575.42, 1227.60, 1176.45 |
| Prime Windows (μs) | 10007-10079 (8 windows) |
| Attack Threads | 2 (parallel) |
| Frequency Check Interval | 50 ms |
| Prime Pulse Intervals | 2-13 seconds |
| Max Time Drift | 500+ ms |
| Position Error Range | 100-1000+ km |

---

## Legal Notices

### WARNING: FEDERAL CRIME

GPS disruption is heavily regulated under:
- **Communications Act** (47 U.S.C. § 333)
- **Anti-Jam Act** (18 U.S.C. § 1367)
- **Computer Fraud and Abuse Act** (18 U.S.C. § 1030)

**Unauthorized GPS disruption is a federal crime punishable by:**
- Up to 20 years imprisonment
- Fines up to $500,000
- Civil liability for damages

### Authorized Use Only

This tool is EXCLUSIVELY for:
- Military combat operations (with proper authorization)
- Authorized defense testing
- Government research (with proper clearance)

### User Responsibility

- **You** are responsible for ensuring authorization
- Operator must document authorization before execution
- All operations logged automatically for audit
- Evidence preserved for legal proceedings

---

## License

**PROPRIETARY SOFTWARE**

Copyright © 2025 A.N.F. Simões. All Rights Reserved.

- NOT open source
- Redistribution prohibited
- Reverse engineering forbidden
- Commercial licensing available

---

## Support

For authorized military/defense use:
- **Contact**: amexsimoes@gmail.com
- **Clearance Required**: Top Secret / SCI
- **Documentation**: /usr/share/gps-annihilator/OPERATOR_GUIDE.md

---

**GPS ANNIHILATOR: Disabling enemy positioning, one prime at a time.**
