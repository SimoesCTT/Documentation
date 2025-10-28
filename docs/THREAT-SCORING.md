# CTT Bot Destroyer - Threat Scoring System

## Overview

The CTT Bot Destroyer uses a **multi-factor scoring system** to differentiate between benign activity and hostile threats. This document explains the scoring criteria and how machine learning can enhance it.

---

## Current Threat Scoring Criteria

### Scoring Thresholds

| Threshold | Action | Description |
|-----------|--------|-------------|
| **Score ≥ 30** | ⚠️ **Warning** | Suspicious activity - issue legal warning via 6 channels |
| **Score ≥ 50** | 🤖 **Bot Detected** | Confirmed bot - log and track |
| **Score ≥ 60** | 🔥 **Counter-Attack** | HIGH threat - launch TEMPEST-SQL attack |
| **Score ≥ 80** | 💥 **Critical** | CRITICAL threat - aggressive neutralization |

---

## Scoring Components

### 1. **User Agent Analysis** (+25 points)
```python
Bot indicators:
- bot, crawler, spider, scraper, scan
- python-requests, curl, wget, java, go-http
- automated, monitor, check, test
- headless, phantom, selenium, puppeteer
- scrapy, beautifulsoup, mechanize
- nikto, nmap, masscan, zap, acunetix
- sqlmap, havij, metasploit
- port_scan, syn_scan, firewall
```

**Why:** User agents reveal attacker tools and intent

### 2. **Port Scanning** (+35 points for method, +30 for user agent)
```python
Method indicators:
- SCAN, SYN, PROBE in request method

User agent indicators:
- port_scan, syn_scan, firewall in user agent
```

**Why:** Port scanning is unauthorized reconnaissance - precursor to attack

**Total Port Scan Score:** 25 (user agent) + 35 (method) + 30 (reconnaissance) = **90 points = CRITICAL**

### 3. **Timing Pattern Analysis** (+30 points)
```python
Condition: 5+ requests in 10 seconds from same source
```

**Why:** Automated bots operate at inhuman speeds

### 4. **Honeypot Triggers** (+50 points)
```python
Honeypot endpoints:
- /api/temporal_data
- /admin/debug/temporal
- /db/query/raw
- /.git/config
- /api/mass_modulation
```

**Why:** No legitimate user accesses these endpoints

### 5. **CTT Framework Probing** (+40 points)
```python
CTT indicators in payload/endpoint:
- 1.2294, 1.0222, 0.0302 (temporal constants)
- temporal, spatial, framework
- 587000, 293500 (resonance frequencies)
- convergent, ctt
```

**Why:** Specific targeting of CTT research = surveillance/espionage

### 6. **TEMPEST-SQL Attack Patterns** (+45 points)
```python
Patterns:
- MOD(UNIX_TIMESTAMP())
- MICROSECOND()
- Prime microseconds: 10007, 10009, 10037
- framework.*temporal|spatial.*framework
```

**Why:** Active attack using TEMPEST-SQL techniques

### 7. **Known Bot Signatures** (+35 points)
```python
Signatures:
- Aggressive Scraper
- CTT Research Surveillance
- SQL Injection Bot
- Government Surveillance
- Commercial Scraper
- Automated Scanner
- Credential Stuffing Bot
```

**Why:** Matching known attack patterns

---

## Example Scoring Scenarios

### Scenario 1: Legitimate User
```
User Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Endpoint: /home
Method: GET
Timing: Normal

Score: 0 points
Action: None - legitimate traffic
```

### Scenario 2: Port Scanner (Current System)
```
User Agent: port_scanner:TCP:443
Endpoint: /TCP:443
Method: SYN_SCAN
Timing: Rapid

Score Breakdown:
- User agent bot indicators: +25
- Port scan method: +35
- Port scan user agent: +30
TOTAL: 90 points = CRITICAL

Actions:
✅ Warning issued (6 channels)
✅ TEMPEST counter-attack launched
✅ Evidence collected
✅ ISP notified
✅ Mesh broadcast
```

### Scenario 3: SQL Injection Bot
```
User Agent: sqlmap/1.0
Endpoint: /api/query
Method: POST
Payload: SELECT * FROM users WHERE MOD(UNIX_TIMESTAMP(), 2) = 0

Score Breakdown:
- User agent: +25 (sqlmap)
- Known signature: +35 (SQL Injection Bot)
- TEMPEST-SQL pattern: +45
TOTAL: 105 points = CRITICAL

Actions:
✅ All above + aggressive neutralization
```

### Scenario 4: Honeypot Trigger
```
User Agent: bot-scanner/1.0
Endpoint: /admin/debug/temporal
Method: GET

Score Breakdown:
- User agent: +25
- Honeypot trigger: +50
TOTAL: 75 points = HIGH

Actions:
✅ Warning issued
✅ Counter-attack launched
✅ Additional honeypot trap deployed
```

---

## Machine Learning Enhancement

### Phase 1: Behavioral Learning (Immediate)

Add adaptive scoring based on observed patterns:

```python
class MLThreatScorer:
    """Machine learning enhanced threat scoring"""
    
    def __init__(self):
        self.attack_history = []
        self.false_positives = []
        self.confirmed_threats = []
        
    def learn_from_attack(self, attack_data, was_threat):
        """Learn from confirmed threats and false positives"""
        
        features = self.extract_features(attack_data)
        
        if was_threat:
            self.confirmed_threats.append(features)
        else:
            self.false_positives.append(features)
        
        # Adjust scoring weights
        self.update_weights()
    
    def extract_features(self, attack_data):
        """Extract behavioral features"""
        return {
            'requests_per_second': self.calculate_rate(attack_data),
            'unique_endpoints_hit': len(set(attack_data['endpoints'])),
            'payload_entropy': self.calculate_entropy(attack_data['payload']),
            'time_of_day': attack_data['timestamp'].hour,
            'geographic_origin': self.geolocate(attack_data['ip']),
            'tls_fingerprint': attack_data.get('tls_signature'),
            'http_header_anomalies': self.check_headers(attack_data)
        }
```

### Phase 2: Pattern Recognition

```python
def adaptive_scoring(self, request_data):
    """ML-adjusted threat score"""
    
    # Base score from rule-based system
    base_score = self.rule_based_score(request_data)
    
    # ML adjustment based on historical patterns
    ml_adjustment = self.predict_threat_level(request_data)
    
    # Confidence-weighted final score
    final_score = base_score * 0.6 + ml_adjustment * 0.4
    
    return final_score
```

### Phase 3: Continuous Improvement

**Feedback Loop:**
1. System makes decision (warn/attack/ignore)
2. Track outcome (did attack continue? false positive?)
3. Update model weights
4. Refine thresholds dynamically

**Metrics to Track:**
- False positive rate
- False negative rate
- Attack escalation patterns
- Geographic threat distribution
- Temporal attack patterns
- Attack success/failure rates

---

## Advanced Threat Indicators (Future ML)

### Behavioral Patterns

1. **Request Sequencing**
   - Does attacker follow logical navigation?
   - Random endpoint jumping = +15 points

2. **Payload Sophistication**
   - Entropy analysis of payloads
   - High entropy = obfuscation = +20 points

3. **Geographic Anomalies**
   - Known hostile regions
   - Suspicious VPN/proxy use
   - = +10-25 points

4. **TLS Fingerprinting**
   - Bot TLS signatures differ from browsers
   - Mismatch = +15 points

5. **HTTP Header Anomalies**
   - Missing expected headers
   - Inconsistent header combinations
   - = +10 points

6. **Temporal Patterns**
   - Attacks at unusual hours
   - Precisely timed intervals
   - = +15 points

---

## Implementation Roadmap

### Current (v2.0) ✅
- Rule-based scoring
- Fixed thresholds
- Manual signature updates
- Statistical timing analysis

### Phase 1 (v2.1) - In Development
- Behavioral feature extraction
- Attack history tracking
- False positive/negative logging
- Basic weight adjustment

### Phase 2 (v2.5) - Planned
- scikit-learn integration
- Random Forest classifier
- Online learning (incremental updates)
- Automated threshold adjustment

### Phase 3 (v3.0) - Future
- Deep learning (LSTM for sequences)
- Federated learning across mesh
- Zero-day attack prediction
- Autonomous signature generation

---

## Configuration

### Adjust Thresholds (Current)

Edit `/usr/lib/python3.13/site-packages/ctt_bot_destroyer/bot_destroyer.py`:

```python
analysis = {
    'should_warn': bot_score >= 30,  # Warning threshold
    'is_bot': bot_score >= 50,       # Bot detection
    # Counter-attack triggered at threat_level HIGH/CRITICAL (score >= 60)
}
```

### Enable ML (Future)

```bash
# Enable ML mode
sudo systemctl edit ctt-bot-defender.service

[Service]
Environment="CTT_ML_MODE=enabled"
Environment="CTT_LEARNING_RATE=0.01"
Environment="CTT_MIN_SAMPLES=100"
```

---

## Why This Approach Works

### 1. **Layered Defense**
Multiple scoring factors catch different attack types

### 2. **Low False Positives**
High thresholds (30+ for warning, 60+ for attack) ensure precision

### 3. **Documented Intent**
Every decision based on measurable criteria = legal defensibility

### 4. **Proportional Response**
- Low-level reconnaissance → Warning only
- High-level attacks → Warning + Counter-attack

### 5. **Continuous Learning**
System improves with every attack

---

## Legal Considerations

**All scoring is evidence-based:**
- ✅ User agent analysis = technical fact
- ✅ Timing patterns = measurable behavior
- ✅ Honeypot access = clear intent
- ✅ Attack patterns = identifiable signatures

**Warnings before action:**
- Score ≥ 30 → Warning issued
- Score ≥ 60 → Counter-attack (after warning)
- All attackers properly notified

**Machine learning enhances, doesn't replace:**
- ML adjusts weights, doesn't make binary decisions
- Final decision always includes rule-based component
- Human-reviewable scoring logic

---

## Conclusion

The current system balances:
- ⚖️ **Precision** - High thresholds minimize false positives
- 🎯 **Effectiveness** - Multiple factors catch real threats
- 📋 **Documentation** - Every score is traceable
- 🤖 **Automation** - No manual intervention needed
- 🧠 **Adaptability** - ML enhancement ready

**Port scanners score 90 (CRITICAL) because:**
- Unauthorized reconnaissance (+65 points from method+user agent)
- Clear hostile intent (no legitimate port scanning exists)
- Precursor to actual attack (documented attack pattern)
- Measurable, objective criteria

Machine learning will refine weights over time based on **actual attack outcomes**, making the system more precise while maintaining legal defensibility.

---

**Copyright © 2025 A.N.F. Simões. All Rights Reserved.**
