Name:           ctt-bot-destroyer
Version:        2.0
Release:        1%{?dist}
Summary:        CTT Bot Destroyer - Autonomous Bot Defense with Auto-Warnings & TEMPEST Counter-Attacks

License:        Proprietary - All Rights Reserved
URL:            https://github.com/SimoesCTT/Documentation
Source0:        %{name}-%{version}.tar.gz

# Proprietary software - NOT open source
# Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
# Patent Pending - Convergent Time Theory (CTT) Bot Defense Implementation
# Unauthorized distribution, modification, or reverse engineering prohibited.

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-libs
Requires:       python3-requests

%description
CTT Bot Destroyer is a sophisticated defense system that detects and 
neutralizes hostile bots using Convergent Time Theory (CTT) principles,
TEMPEST-SQL counter-attacks, and distributed mesh intelligence.

Detection capabilities include:
- Behavioral timing analysis and user agent fingerprinting
- CTT-specific honeypot traps
- TEMPEST-SQL pattern recognition
- Known bot signature matching
- Distributed mesh intelligence (WWW + Freedom Web)

Neutralization methods:
- TEMPEST Counter-Attack (reality fragmentation, temporal loops)
- Reality Fragmentation (conflicting temporal/spatial data)
- Data Poisoning (fake endpoints and CTT traps)
- Rate Limiting and Honeypot Traps

Mesh Network Integration:
- WWW peer-to-peer threat sharing via UDP
- CTT Mesh (Freedom Web) integration via daemon
- Real-time distributed threat intelligence
- Automatic peer discovery and coordination

COPYRIGHT NOTICE:
Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
This is proprietary software protected by intellectual property law.
Patent Pending - Convergent Time Theory Bot Defense Implementation.

LICENSE RESTRICTIONS:
- This software is NOT open source
- Redistribution in any form is prohibited without written permission
- Reverse engineering and decompilation are strictly forbidden
- Use is restricted to authorized security defense operations
- Commercial use requires separate licensing agreement

WARNING: This tool defends YOU against hostile surveillance bots,
scraping bots, and automated attacks using TEMPEST-SQL counter-attacks
and CTT-based neutralization techniques.

%prep
%setup -q

%build
# Python module, no compilation needed

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{python3_sitelib}/ctt_bot_destroyer
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ctt-bot-destroyer
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT/var/lib/ctt-bot-defender

# Install Python modules
install -m 0644 src/bot_destroyer.py $RPM_BUILD_ROOT%{python3_sitelib}/ctt_bot_destroyer/bot_destroyer.py
install -m 0644 mesh_defense.py $RPM_BUILD_ROOT%{python3_sitelib}/ctt_bot_destroyer/mesh_defense.py
install -m 0644 src/bot_defender_service.py $RPM_BUILD_ROOT%{python3_sitelib}/ctt_bot_destroyer/bot_defender_service.py
install -m 0644 src/attacker_warner.py $RPM_BUILD_ROOT%{python3_sitelib}/attacker_warner.py

# Create __init__.py
cat > $RPM_BUILD_ROOT%{python3_sitelib}/ctt_bot_destroyer/__init__.py << 'EOF'
"""
CTT Bot Destroyer - Autonomous Bot Defense System
Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
"""
from .bot_destroyer import CTTBotDestroyer
from .mesh_defense import MeshDefenseNode, MeshDefenseCoordinator

__version__ = "1.0"
__author__ = "A.N.F. Simões"
__license__ = "Proprietary"
EOF

# Create executable wrappers
cat > $RPM_BUILD_ROOT%{_bindir}/ctt-bot-destroyer << 'EOF'
#!/usr/bin/env python3
"""
CTT Bot Destroyer - Autonomous Bot Defense System
Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
"""
import sys
sys.path.insert(0, '/usr/lib/python3.13/site-packages')
from ctt_bot_destroyer.bot_destroyer import demonstrate_bot_destroyer

if __name__ == "__main__":
    print("🤖💀 CTT BOT DESTROYER - Autonomous Bot Defense System")
    print("   Copyright (c) 2025 A.N.F. Simões")
    print("   Proprietary Software - All Rights Reserved\n")
    demonstrate_bot_destroyer()
EOF

cat > $RPM_BUILD_ROOT%{_bindir}/ctt-mesh-defense << 'EOF'
#!/usr/bin/env python3
"""
CTT Mesh Defense Node - Distributed Bot Defense
Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
"""
import sys
sys.path.insert(0, '/usr/lib/python3.13/site-packages')
from ctt_bot_destroyer.mesh_defense import demonstrate_mesh_defense

if __name__ == "__main__":
    print("🌐🤖💀 CTT MESH DEFENSE - Distributed Bot Defense System")
    print("   Copyright (c) 2025 A.N.F. Simões")
    print("   Proprietary Software - All Rights Reserved\n")
    demonstrate_mesh_defense()
EOF

chmod +x $RPM_BUILD_ROOT%{_bindir}/ctt-bot-destroyer
chmod +x $RPM_BUILD_ROOT%{_bindir}/ctt-mesh-defense

# Install systemd service
install -m 0644 ctt-bot-defender.service $RPM_BUILD_ROOT%{_unitdir}/ctt-bot-defender.service

# Install wrapper script
cat > $RPM_BUILD_ROOT%{_bindir}/ctt-bot-defender-wrapper << 'EOF'
#!/bin/bash
cd /var/lib/ctt-bot-defender
exec /usr/bin/python3 -m ctt_bot_destroyer.bot_defender_service "$@"
EOF
chmod +x $RPM_BUILD_ROOT%{_bindir}/ctt-bot-defender-wrapper

%files
%{_bindir}/ctt-bot-destroyer
%{_bindir}/ctt-mesh-defense
%{_bindir}/ctt-bot-defender-wrapper
%{python3_sitelib}/ctt_bot_destroyer/
%{python3_sitelib}/ctt_bot_destroyer/__init__.py
%{python3_sitelib}/ctt_bot_destroyer/bot_destroyer.py
%{python3_sitelib}/ctt_bot_destroyer/mesh_defense.py
%{python3_sitelib}/ctt_bot_destroyer/bot_defender_service.py
%{python3_sitelib}/ctt_bot_destroyer/__pycache__/
%{python3_sitelib}/attacker_warner.py
%{python3_sitelib}/__pycache__/attacker_warner.cpython-313.opt-1.pyc
%{python3_sitelib}/__pycache__/attacker_warner.cpython-313.pyc
%{_unitdir}/ctt-bot-defender.service
%dir /var/lib/ctt-bot-defender
%doc README.md
%license LICENSE

%post
# Enable and start service after installation
if [ $1 -eq 1 ]; then
    # First install
    systemctl daemon-reload
    systemctl enable ctt-bot-defender.service
    systemctl start ctt-bot-defender.service
    echo "✅ CTT Bot Defender service installed and started"
    echo "   Check status: systemctl status ctt-bot-defender.service"
    echo "   View logs: journalctl -u ctt-bot-defender.service -f"
fi

%preun
# Stop and disable service before uninstall
if [ $1 -eq 0 ]; then
    systemctl stop ctt-bot-defender.service
    systemctl disable ctt-bot-defender.service
fi

%postun
# Cleanup after uninstall
if [ $1 -eq 0 ]; then
    systemctl daemon-reload
fi

%changelog
* Tue Oct 28 2025 A.N.F. Simões <amexsimoes@gmail.com> - 2.0-1
- MAJOR UPDATE: Automatic warning system for ALL unauthorized access
- Automatic TEMPEST-SQL counter-attacks on HIGH/CRITICAL threats
- Multi-channel legal warnings (TCP, ICMP, HTTP, WHOIS, File, Mesh)
- Port scan detection with automatic warnings (no counter-attack for low-level)
- Enhanced bot scoring: Port scans now detected and warned automatically
- Abuse contact extraction and notification preparation
- Real-time threat detection and response
- Evidence collection for legal prosecution
- Mesh network threat intelligence broadcasting
- Out-of-the-box operation - service starts automatically
- 100% autonomous defense: detects, warns, attacks, and logs

* Mon Oct 27 2025 A.N.F. Simões <amexsimoes@gmail.com> - 1.0-1
- Initial RPM release
- Convergent Time Theory bot defense implementation
- TEMPEST-SQL counter-attack capabilities
- Distributed mesh network integration (WWW + Freedom Web)
- Real-time bot detection and neutralization
- Honeypot traps and behavioral analysis
- SQLite database for threat intelligence
- Automatic peer discovery and coordination
