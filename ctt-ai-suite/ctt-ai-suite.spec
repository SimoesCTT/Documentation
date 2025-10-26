Name:           ctt-ai-suite
Version:        1.0.0
Release:        1%{?dist}
Summary:        Revolutionary machine learning optimization using Convergent Time Theory

License:        Proprietary
URL:            https://github.com/SimoesCTT/ctt-ai-suite
Source0:        %{name}-%{version}.tar.gz

BuildArch:      x86_64

# Don't create debuginfo packages for binaries
%global debug_package %{nil}

%description
CTT AI Suite provides revolutionary machine learning optimization tools
based on Convergent Time Theory (CTT).

CTT Model Compressor:
- 10-100x neural network compression
- Deploy GB-scale models on edge devices
- Lossless weight reconstruction
- Compatible with PyTorch, TensorFlow, ONNX

CTT Training Optimizer (Coming Soon):
- 10-100x faster training via gradient prediction
- Temporal correlation in gradient descent
- Reduce training costs by millions

Resonance Embeddings (Coming Soon):
- 100x embedding compression
- Semantic preservation
- GPT-3 embeddings: 2.4GB -> 24MB

This package contains compiled binaries and documentation only.
Source code is proprietary and not included.

Patent-pending technology. First ML optimization using temporal 
framework physics.

%prep
%setup -q

%build
# No build needed for binary distribution

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}

# Install binary
install -m 0755 ctt_model_compress $RPM_BUILD_ROOT%{_bindir}/ctt_model_compress

# Install documentation
install -m 0644 README.md $RPM_BUILD_ROOT%{_docdir}/%{name}/README.md
install -m 0644 LICENSE $RPM_BUILD_ROOT%{_docdir}/%{name}/LICENSE
install -m 0644 ctt-ai-suite-paper.pdf $RPM_BUILD_ROOT%{_docdir}/%{name}/ctt-ai-suite-paper.pdf

%files
%{_bindir}/ctt_model_compress
%doc %{_docdir}/%{name}/README.md
%license %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/ctt-ai-suite-paper.pdf

%changelog
* Sat Oct 26 2024 Américo Simões <contact@github.com>
- Initial release 1.0.0
- CTT Model Compressor: 10-100x neural network compression
- Resonance-based weight encoding with temporal framework physics
- Deploy GB models on edge devices (phones, IoT, embedded)
- Academic paper and complete documentation included
- Proprietary license with research/evaluation permissions
- Patent-pending ML optimization technology
- Target: \$15B edge AI market + \$10B cloud training market
