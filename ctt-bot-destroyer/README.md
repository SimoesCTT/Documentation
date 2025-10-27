# CTT BOT DESTROYER
## Autonomous Bot Defense & Counter-Attack System

🤖💀 Advanced bot detection and neutralization using Convergent Time Theory and TEMPEST-SQL

---

## Overview

**CTT Bot Destroyer** is a sophisticated defense system that detects and neutralizes hostile bots using CTT principles, TEMPEST-SQL counter-attacks, and distributed mesh intelligence.

### Key Features

**Detection Methods:**
- ✅ Behavioral timing analysis
- ✅ User agent fingerprinting  
- ✅ CTT-specific honeypot traps
- ✅ TEMPEST-SQL pattern recognition
- ✅ Known bot signature matching
- ✅ Distributed mesh intelligence

**Neutralization Methods:**
- ⚡ TEMPEST Counter-Attack - Reality fragmentation, temporal loops
- 🌀 Reality Fragmentation - Conflicting temporal/spatial data injection
- ☠️  Data Poisoning - Fake endpoints and CTT traps
- 🐌 Rate Limiting - Aggressive throttling
- 🍯 Honeypot Traps - Intelligence collection

**Mesh Network Integration:**
- 🌐 WWW peer-to-peer threat sharing via UDP
- 🕸️  CTT Mesh (Freedom Web) integration
- 📡 Real-time distributed threat intelligence
- 🤝 Automatic peer discovery and coordination

## Installation

### From RPM

```bash
sudo dnf install ctt-bot-destroyer-1.0-1.*.rpm
```

### Manual Installation

```bash
cd /home/americosimoes/ctt-bot-destroyer
sudo python3 setup.py install
```

## Usage

### Standalone Bot Destroyer

```bash
# Run demonstration
python3 bot_destroyer.py

# Or use as module
python3 -c "from bot_destroyer import CTTBotDestroyer; d = CTTBotDestroyer(aggressive_mode=True)"
```

### Mesh Defense Network

```bash
# Start mesh defense node
python3 mesh_defense.py

# Or integrate in your code
from mesh_defense import MeshDefenseNode

node = MeshDefenseNode(listen_port=9876, ctt_mesh_enabled=True)
node.start_listening()
node.announce_node()

# Analyze requests
analysis = node.analyze_request({
    'ip': '192.168.1.100',
    'user_agent': 'curl/7.68.0',
    'endpoint': '/api/data',
    'method': 'GET',
    'payload': ''
})

# Auto-neutralize if threat detected
if analysis['threat_level'] in ['HIGH', 'CRITICAL']:
    node.neutralize_bot(analysis['bot_id'])
```

### As Web Application Firewall

```python
from bot_destroyer import CTTBotDestroyer

# Initialize
destroyer = CTTBotDestroyer(aggressive_mode=True)

# In your web app request handler
def handle_request(request):
    request_data = {
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'endpoint': request.path,
        'method': request.method,
        'payload': request.get_data()
    }
    
    analysis = destroyer.analyze_request(request_data)
    
    if analysis['block_recommended']:
        destroyer.block_attack(request_data, analysis)
        return "Access Denied", 403
    
    # Continue normal processing
    return handle_normal_request(request)
```

## Configuration

### CTT Constants

The system detects manipulation of these constants:

**Temporal Framework:**
- π_temporal = 1.2294
- G_temporal = 1.0222
- α_temporal = 0.0302

**Spatial Framework:**
- π_spatial = 3.141592653589793
- G_spatial = 6.67430e-11

### Honeypot Endpoints

Default honeypots (customize in code):
- `/api/temporal_data` - CTT framework trap
- `/admin/debug/temporal` - Framework switching trap
- `/db/query/raw` - SQL injection trap
- `/.git/config` - Information disclosure trap
- `/api/mass_modulation` - CTT-specific trap

### Mesh Network

**CTT Mesh Integration:**
- Daemon URL: `http://127.0.0.1:8765`
- Auto-detects if daemon is running
- Publishes threats to decentralized mesh

**WWW Peer Network:**
- Default listen port: 9876
- UDP-based peer communication
- Manual peer addition: `node.add_peer('ip', port)`

## Threat Levels

- **MINIMAL** - Score < 20 - Likely legitimate
- **LOW** - Score 20-39 - Minor suspicious patterns
- **MEDIUM** - Score 40-59 - Concerning patterns
- **HIGH** - Score 60-79 - Active attack patterns, blocking recommended
- **CRITICAL** - Score 80+ - Severe attack, immediate neutralization

## Database

SQLite database `bot_destroyer.db` tracks:
- Detected bots with fingerprints and behavior
- Attack patterns and timing
- Neutralization attempts and success rates
- Mesh-shared threat intelligence

### Query Database

```bash
sqlite3 bot_destroyer.db "SELECT * FROM detected_bots WHERE threat_level >= 80;"
```

## Neutralization Methods

### Auto Mode (Recommended)
System automatically selects best method based on threat level:
```python
result = destroyer.neutralize_bot(bot_id, method='auto')
```

### Manual Methods
- `tempest_attack` - TEMPEST-SQL counter-attack (threat 80+)
- `reality_fragment` - Reality fragmentation (threat 60+)
- `data_poison` - Data poisoning (threat 40+)
- `rate_limit` - Rate limiting (threat 20+)
- `honeypot_trap` - Lure into honeypot

## Distributed Deployment

Deploy multiple nodes for distributed defense:

```python
from mesh_defense import MeshDefenseCoordinator, MeshDefenseNode

coordinator = MeshDefenseCoordinator()

# Create multiple nodes
node1 = MeshDefenseNode(listen_port=9876)
node2 = MeshDefenseNode(listen_port=9877)
node3 = MeshDefenseNode(listen_port=9878)

coordinator.add_node(node1)
coordinator.add_node(node2)
coordinator.add_node(node3)

# Start all nodes
coordinator.start_all_nodes()

# Connect nodes as peers
node1.add_peer('10.0.0.2', 9876)
node2.add_peer('10.0.0.3', 9876)

# Get network status
status = coordinator.get_network_status()
print(f"Active nodes: {status['active_nodes']}")
print(f"Total threats: {status['total_bots_detected']}")
```

## Integration Examples

### Flask Web App
```python
from flask import Flask, request, abort
from bot_destroyer import CTTBotDestroyer

app = Flask(__name__)
destroyer = CTTBotDestroyer(aggressive_mode=True)

@app.before_request
def check_for_bots():
    analysis = destroyer.analyze_request({
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', ''),
        'endpoint': request.path,
        'method': request.method,
        'payload': str(request.args) + str(request.form)
    })
    
    if analysis['threat_level'] in ['HIGH', 'CRITICAL']:
        destroyer.block_attack(request.path, analysis)
        abort(403)
```

### Nginx/Apache Module
Use as backend API via HTTP wrapper (see `http_wrapper.py`)

### System Service
See `systemd/ctt-bot-destroyer.service` for systemd integration

## Reporting

Generate security reports:

```python
report = destroyer.get_bot_report()
print(f"Total bots detected: {report['total_bots_detected']}")
print(f"Bots neutralized: {report['bots_neutralized']}")
print(f"Active threats: {report['active_threats']}")
print(f"Threat breakdown: {report['threat_breakdown']}")
```

Mesh network status:

```python
mesh_status = node.get_mesh_status()
print(f"Peer nodes: {mesh_status['peer_nodes']}")
print(f"Shared threats: {mesh_status['shared_threats']}")
print(f"CTT Mesh: {mesh_status['ctt_mesh_status']}")
```

## License

**Proprietary Software**
- Copyright (c) 2025 A.N.F. Simões
- All Rights Reserved
- Patent Pending
- NOT open source

See LICENSE file for complete terms.

## Companion Software

CTT Bot Destroyer works with:
- **TEMPEST-SQL** - Temporal attack framework (what we defend against)
- **THE TIME KEEPER** - TEMPEST-SQL detection system
- **CTT Mesh Daemon** - Decentralized mesh network for Freedom Web

All tools are part of the Convergent Time Theory research project.

## Support

For commercial licensing or deployment support:
- **Email**: amexsimoes@gmail.com
- **Tel**: +65 87635603
- **Documentation**: https://github.com/SimoesCTT/Documentation

---

🤖💀 **CTT BOT DESTROYER** - Defending against hostile bots on WWW and Freedom Web
