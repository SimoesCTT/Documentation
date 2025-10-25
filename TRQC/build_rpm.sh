#!/bin/bash

# Build RPM package for Temporal Resonance Quantum Computer
# Copyright (c) 2025 Americo Simoes

set -e

echo "=========================================="
echo "Building TRQC RPM Package"
echo "=========================================="
echo ""

# Check if rpmbuild is installed
if ! command -v rpmbuild &> /dev/null; then
    echo "❌ rpmbuild not found. Installing..."
    sudo dnf install -y rpm-build rpmdevtools
fi

# Set up RPM build environment
echo "📦 Setting up RPM build environment..."
rpmdev-setuptree

# Version info
VERSION="1.0.0"
NAME="trqc"

# Create source tarball
echo "📝 Creating source tarball..."
TMPDIR=$(mktemp -d)
mkdir -p "$TMPDIR/$NAME-$VERSION"

# Copy files
cp -r *.py trqc README.md LICENSE temporal_qc_breaks_rsa.pdf "$TMPDIR/$NAME-$VERSION/"

# Create tarball
cd "$TMPDIR"
tar czf "$NAME-$VERSION.tar.gz" "$NAME-$VERSION"
mv "$NAME-$VERSION.tar.gz" ~/rpmbuild/SOURCES/
cd -

# Copy spec file
echo "📋 Copying spec file..."
cp trqc.spec ~/rpmbuild/SPECS/

# Build RPM
echo "🔨 Building RPM..."
cd ~/rpmbuild/SPECS
rpmbuild -ba trqc.spec

# Check results
echo ""
echo "=========================================="
echo "✓ RPM Build Complete!"
echo "=========================================="
echo ""
echo "RPM packages created:"
ls -lh ~/rpmbuild/RPMS/noarch/trqc-*.rpm 2>/dev/null || echo "Binary RPM not found"
ls -lh ~/rpmbuild/SRPMS/trqc-*.src.rpm 2>/dev/null || echo "Source RPM not found"

echo ""
echo "To install locally:"
echo "  sudo dnf install ~/rpmbuild/RPMS/noarch/trqc-$VERSION-1.fc*.noarch.rpm"
echo ""
echo "To create repository:"
echo "  mkdir -p ~/ctt-rpm-repo"
echo "  cp ~/rpmbuild/RPMS/noarch/trqc-*.rpm ~/ctt-rpm-repo/"
echo "  createrepo ~/ctt-rpm-repo/"
echo ""

# Clean up
rm -rf "$TMPDIR"

echo "Done!"
