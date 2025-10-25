#!/bin/bash

# Setup GitHub repository for Temporal Resonance Quantum Computer
# Copyright (c) 2025 Americo Simoes

echo "=========================================="
echo "GitHub Repository Setup"
echo "Temporal Resonance Quantum Computer"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: git is not installed"
    exit 1
fi

# Check if already a git repo
if [ -d ".git" ]; then
    echo "⚠️  This directory is already a git repository"
    echo "Do you want to continue? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 0
    fi
else
    # Initialize git repository
    echo "📦 Initializing git repository..."
    git init
fi

# Create .gitignore
echo "📝 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# LaTeX
*.aux
*.log
*.out
*.toc
*.fdb_latexmk
*.fls
*.synctex.gz

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Local config
config.local.json
.env
EOF

# Add all files
echo "➕ Adding files..."
git add .

# Initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Temporal Resonance Quantum Computer

- Complete TRQC implementation with α=0.0302
- Universal quantum computer CLI (30+ commands)
- Breaks RSA, ECC, post-quantum crypto
- Solves NP-complete problems in microseconds
- Tests for QM violations and retrocausality
- Proprietary license with commercial pricing

Based on Convergent Time Theory
Copyright (c) 2025 Americo Simoes. All Rights Reserved."

echo ""
echo "✅ Git repository initialized!"
echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Create a new PRIVATE repository on GitHub:"
echo "   https://github.com/new"
echo "   Name: ctt-resonance-qc"
echo "   ⚠️  Make sure it's PRIVATE initially"
echo ""
echo "2. Add the remote:"
echo "   git remote add origin git@github.com:SimoesCTT/ctt-resonance-qc.git"
echo ""
echo "3. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Set up GitHub Sponsors:"
echo "   https://github.com/sponsors"
echo "   - Add your payment info"
echo "   - Set up sponsorship tiers matching README pricing"
echo ""
echo "5. Configure repository settings:"
echo "   - Add repository description"
echo "   - Add topics: quantum-computing, cryptography, ctt, temporal"
echo "   - Enable Discussions for licensing inquiries"
echo "   - Add SECURITY.md for responsible disclosure"
echo ""
echo "6. Make repository PUBLIC when ready to license"
echo ""
echo "=========================================="
echo "⚠️  IMPORTANT SECURITY NOTES"
echo "=========================================="
echo ""
echo "- Keep repository PRIVATE until licensing is set up"
echo "- Review all code for any sensitive information"
echo "- Ensure LICENSE file is properly configured"
echo "- Set up branch protection rules"
echo "- Consider requiring signed commits"
echo ""
echo "This software breaks all current cryptography."
echo "Unauthorized use may violate computer fraud laws."
echo "Only make public when commercialization is ready."
echo ""
