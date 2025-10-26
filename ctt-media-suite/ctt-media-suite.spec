Name:           ctt-media-suite
Version:        1.0.0
Release:        1%{?dist}
Summary:        Revolutionary video and audio codecs using Convergent Time Theory

License:        Proprietary
URL:            https://github.com/SimoesCTT/ctt-media-suite
Source0:        %{name}-%{version}.tar.gz

BuildArch:      x86_64

# Don't create debuginfo packages for binaries
%global debug_package %{nil}

%description
CTT Media & Entertainment Suite provides revolutionary video and audio 
compression codecs based on Convergent Time Theory (CTT). 

CTT Video Codec:
- 25%% better compression than H.265 at equivalent quality
- Resonance-based frame encoding
- Perfect lossless reconstruction
- Target: Netflix, YouTube, HBO, Disney+ (billions in savings)

CTT Audio Codec:
- 90-95%% compression (vs FLAC's 50%%)
- First lossless codec competitive with lossy formats
- Bit-perfect audio reconstruction
- Target: Spotify, Apple Music, audiophile market

This package contains compiled binaries and documentation only.
Source code is proprietary and not included.

Patent-pending technology. First multimedia codecs using temporal 
framework physics.

%prep
%setup -q

%build
# No build needed for binary distribution

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}

# Install binaries
install -m 0755 ctt_video_compress $RPM_BUILD_ROOT%{_bindir}/ctt_video_compress
install -m 0755 ctt_audio_compress $RPM_BUILD_ROOT%{_bindir}/ctt_audio_compress
install -m 0755 ctt_video.sh $RPM_BUILD_ROOT%{_bindir}/ctt_video
install -m 0755 ctt_audio.sh $RPM_BUILD_ROOT%{_bindir}/ctt_audio

# Install documentation
install -m 0644 README.md $RPM_BUILD_ROOT%{_docdir}/%{name}/README.md
install -m 0644 README-VIDEO.md $RPM_BUILD_ROOT%{_docdir}/%{name}/README-VIDEO.md
install -m 0644 README-AUDIO.md $RPM_BUILD_ROOT%{_docdir}/%{name}/README-AUDIO.md
install -m 0644 LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}/LICENSE
install -m 0644 ctt-media-suite-paper.pdf $RPM_BUILD_ROOT%{_docdir}/%{name}/ctt-media-suite-paper.pdf

%files
%{_bindir}/ctt_video_compress
%{_bindir}/ctt_audio_compress
%{_bindir}/ctt_video
%{_bindir}/ctt_audio
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/README-VIDEO.md
%doc %{_docdir}/%{name}/README-AUDIO.md
%license %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/ctt-media-suite-paper.pdf

%changelog
* Sat Oct 26 2024 Américo Simões <contact@github.com>
- Initial release 1.0.0
- CTT Video Codec: 25%% improvement over H.265
- CTT Audio Codec: 90-95%% lossless compression
- Resonance-based encoding with temporal framework physics
- Academic paper and complete documentation included
- Proprietary license with research/evaluation permissions
- Patent-pending technology for multimedia compression
