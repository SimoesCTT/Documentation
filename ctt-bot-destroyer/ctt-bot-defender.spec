Name:           ctt-bot-defender
Version:        2.0
Release:        1%{?dist}
Summary:        CTT Bot Defender - Autonomous Active Defense System with TEMPEST-SQL Counter-Attacks

License:        Proprietary - All Rights Reserved
URL:            https://github.com/SimoesCTT/Documentation
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       python3
Requires:       python3-libs
Requires:       systemd
Requires:       tempest-sql

%description
CTT Bot Defender is an autonomous active defense system that detects and 
neutralizes hostile bots in real-time using:

- Real-time network connection monitoring
- Behavioral bot detection and scoring (0-100)
- Multi-channel automated warnings (TCP, ICMP, File, Mesh)
- AUTONOMOUS TEMPEST-SQL counter-attacks on HIGH/CRITICAL threats
- Complete forensic evidence collection

Features:
- Fully autonomous - no manual intervention required
- Starts automatically on boot
- Counter-attacks using TEMPEST-SQL weapon system
- Legal evidence collection for prosecution
- 100%% automated defense workflow

Copyright (c) 2025 A.N.F. Simões. All Rights Reserved.
Patent Pending - Convergent Time Theory Bot Defense Implementation.

%prep
%setup -q

%build
# Python scripts, no build needed

%install
rm -rf $RPM_BUILD_ROOT

# Create directories
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ctt-bot-defender
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT/var/lib/ctt-bot-defender
mkdir -p $RPM_BUILD_ROOT/var/log/ctt-bot-defender

# Install Python scripts
install -m 0755 bot_detector.py $RPM_BUILD_ROOT%{_datadir}/ctt-bot-defender/
install -m 0755 network_monitor.py $RPM_BUILD_ROOT%{_datadir}/ctt-bot-defender/
install -m 0755 defense_actions.py $RPM_BUILD_ROOT%{_datadir}/ctt-bot-defender/
install -m 0755 ctt_bot_defender.py $RPM_BUILD_ROOT%{_datadir}/ctt-bot-defender/

# Install systemd service
install -m 0644 ctt-bot-defender.service $RPM_BUILD_ROOT%{_unitdir}/

%files
%{_datadir}/ctt-bot-defender/bot_detector.py
%{_datadir}/ctt-bot-defender/network_monitor.py
%{_datadir}/ctt-bot-defender/defense_actions.py
%{_datadir}/ctt-bot-defender/ctt_bot_defender.py
%{_unitdir}/ctt-bot-defender.service
%dir /var/lib/ctt-bot-defender
%dir /var/log/ctt-bot-defender

%post
# Create directories with proper permissions
mkdir -p /var/lib/ctt-bot-defender/warnings
mkdir -p /var/lib/ctt-bot-defender/attacks
chmod 755 /var/lib/ctt-bot-defender
chmod 755 /var/log/ctt-bot-defender

# Enable and start service
systemctl daemon-reload
systemctl enable ctt-bot-defender.service
systemctl start ctt-bot-defender.service

echo "========================================================================"
echo "✅ CTT BOT DEFENDER v2.0 - AUTONOMOUS ACTIVE DEFENSE SYSTEM"
echo "========================================================================"
echo ""
echo "🛡️  Service Status: ACTIVE"
echo "⚡ Counter-Attacks: ENABLED (TEMPEST-SQL)"
echo "🤖 Detection: REAL-TIME"
echo "📊 Evidence: /var/lib/ctt-bot-defender/"
echo ""
echo "Commands:"
echo "  Status:  systemctl status ctt-bot-defender.service"
echo "  Logs:    journalctl -u ctt-bot-defender.service -f"
echo "  Stop:    systemctl stop ctt-bot-defender.service"
echo ""
echo "Database:  /var/lib/ctt-bot-defender/bots.db"
echo "Warnings:  /var/lib/ctt-bot-defender/warnings/"
echo "Attacks:   /var/lib/ctt-bot-defender/attacks/"
echo ""
echo "🔥 AUTONOMOUS DEFENSE ACTIVE - System will counter-attack automatically"
echo "========================================================================"

%preun
if [ $1 -eq 0 ]; then
    # Uninstall
    systemctl stop ctt-bot-defender.service
    systemctl disable ctt-bot-defender.service
fi

%postun
if [ $1 -eq 0 ]; then
    systemctl daemon-reload
fi

%changelog
* Tue Oct 28 2025 A.N.F. Simões <amexsimoes@gmail.com> - 2.0-1
- Initial release of autonomous active defense system
- Real-time network monitoring with ss/netstat
- Behavioral bot detection and scoring (0-100)
- Multi-channel automated warnings (TCP, ICMP, File, Mesh)
- AUTONOMOUS TEMPEST-SQL counter-attacks on HIGH/CRITICAL threats
- Complete forensic evidence collection
- Systemd service integration with auto-start
- 100%% autonomous operation - no manual intervention required
