Name:           ctt-compressor
Version:        1.0.0
Release:        1%{?dist}
Summary:        Revolutionary lossless compression using Convergent Time Theory

License:        Proprietary
URL:            https://github.com/SimoesCTT/ctt-compressor
Source0:        %{name}-%{version}.tar.gz

# No BuildRequires since we're distributing binaries only
BuildArch:      x86_64

# Don't create debuginfo packages for binaries
%global debug_package %{nil}

%description
CTT Compressor is a novel lossless data compression system based on 
Convergent Time Theory (CTT). Unlike traditional compression algorithms 
that exploit spatial redundancy, CTT Compressor leverages temporal 
correlations and resonance states in data streams to achieve superior 
compression ratios.

Key features:
- Resonance-based pattern encoding (up to 98.4% compression on repetitive data)
- Temporal framework reconstruction (O(1) vs O(N) for classical methods)
- Ideal for logs, time-series data, database dumps, and structured files
- Patent-pending technology from Convergent Time Theory Research Group

This package contains the compiled binary and documentation only.
Source code is proprietary and not included.

%prep
%setup -q

%build
# No build needed for binary distribution

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

# Install binary
install -m 0755 cttzip $RPM_BUILD_ROOT%{_bindir}/cttzip

# Install documentation
install -m 0644 README.md $RPM_BUILD_ROOT%{_docdir}/%{name}/README.md
install -m 0644 THEORY.md $RPM_BUILD_ROOT%{_docdir}/%{name}/THEORY.md
install -m 0644 LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}/LICENSE
install -m 0644 ctt-compressor-paper.pdf $RPM_BUILD_ROOT%{_docdir}/%{name}/ctt-compressor-paper.pdf

%files
%{_bindir}/cttzip
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/THEORY.md
%license %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/ctt-compressor-paper.pdf

%changelog
* Sat Oct 26 2024 Américo Simões <contact@github.com>
- Initial release 1.0.0
- Resonance encoding with 98.4% compression on repetitive data
- Temporal framework reconstruction
- Command-line utility (cttzip)
- Academic paper and theoretical documentation
- Proprietary license with research/evaluation permissions
