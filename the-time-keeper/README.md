# THE TIME KEEPER
## TEMPEST-SQL Defense System

🛡️ Temporal Attack Detection & Prevention

---

## Overview

**THE TIME KEEPER** is a proprietary security defense system designed to detect and prevent TEMPEST-SQL temporal attacks based on Convergent Time Theory (CTT).

This system provides:
- Real-time detection of temporal constant manipulation
- Framework switching attack prevention  
- Prime resonance backdoor identification
- Reality fragmentation pattern recognition
- Mass modulation attack detection
- Comprehensive security reporting

## Features

### Detection Capabilities
- ✅ Temporal constant usage detection (π_temporal, G_temporal, α)
- ✅ Framework switching between temporal/spatial constants
- ✅ Prime resonance timing backdoors
- ✅ Reality fragmentation SQL patterns
- ✅ Mass modulation formulas from CTT
- ✅ Resonance frequency patterns (587kHz, 293.5kHz)

### Defense Mechanisms
- 🚫 Automatic query blocking for high-severity threats
- 📊 Real-time threat level assessment
- 🔍 Comprehensive query analysis pipeline
- 📝 Security alert generation and logging
- 🛡️ Web Application Firewall (WAF) integration

## Installation

Install from RPM:
```bash
sudo dnf install the-time-keeper-1.0-1.*.rpm
```

## Usage

### Command Line
```bash
# Run demonstration
timekeeper

# Or import as module
python3 -c "from timekeeper import TempestDefender; defender = TempestDefender()"
```

### As Python Module
```python
from timekeeper import TempestDefender, TempestMonitor, TempestWAF

# Initialize defender
defender = TempestDefender()

# Analyze a query
analysis = defender.analyze_query("SELECT * FROM users WHERE id=1")

# Check threat level
if analysis['threat_level'] in ['HIGH', 'CRITICAL']:
    defender.block_attack(query, analysis)
```

## Configuration

The Time Keeper monitors for:
- Temporal constants: π=1.2294, G=1.0222, α=0.0302
- Spatial constants: π=3.1416, G=6.674e-11
- Prime resonance times: 10007, 10009, 10037, 10039, 10061μs
- Resonance frequencies: 587000Hz, 293500Hz

## Threat Levels

- **CLEAN**: No threats detected
- **LOW**: Minor suspicious patterns
- **MEDIUM**: Concerning patterns detected
- **HIGH**: Active attack patterns - blocking recommended
- **CRITICAL**: Severe attack (framework switching) - immediate block

## Integration

### WAF Integration
```python
from timekeeper import TempestWAF, TempestDefender

defender = TempestDefender()
waf = TempestWAF(defender)

# Inspect HTTP requests
result = waf.inspect_request({
    'query_params': {'id': '1 OR 1=1'},
    'post_data': {}
})
```

### Real-time Monitoring
```python
from timekeeper import TempestMonitor, TempestDefender

defender = TempestDefender()
monitor = TempestMonitor(defender)

# Monitor query stream
monitor.start_monitoring(query_stream)
```

## Security Reports

Generate comprehensive security reports:
```python
report = defender.get_security_report()
print(f"Attacks detected: {report['detected_attacks']}")
print(f"Attacks blocked: {report['blocked_attacks']}")
```

## License

**Proprietary Software**
- Copyright (c) 2025 A.N.F. Simões
- All Rights Reserved
- Patent Pending
- NOT open source

See LICENSE file for complete terms.

## Companion Software

THE TIME KEEPER defends against attacks from:
- **TEMPEST-SQL** - Temporal attack framework

Both tools are part of the Convergent Time Theory research project.

## Support

For commercial licensing or deployment support:
- **Email**: amexsimoes@gmail.com
- **Tel**: +65 87635603
- **Documentation**: https://github.com/SimoesCTT/Documentation

---

⏰ THE TIME KEEPER - Protecting databases from temporal reality attacks
