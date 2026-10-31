#!/bin/bash
# GitHub Setup Script for Automation Empire

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         GitHub Setup - Automation Empire Backup               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if git is initialized
if [ ! -d ~/.git ]; then
    echo "❌ Git repository not initialized. Run 'git init' first."
    exit 1
fi

echo "📋 Current Git Status:"
cd ~
git status --short | head -10
echo ""

echo "🔑 Your SSH Public Key (copy this to GitHub):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat ~/.ssh/id_ed25519.pub
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📝 SETUP INSTRUCTIONS:"
echo ""
echo "1. Go to: https://github.com/settings/keys"
echo "   Click 'New SSH key'"
echo "   Title: Automation Empire WSL"
echo "   Paste the key above ☝️"
echo ""
echo "2. Create new repository: https://github.com/new"
echo "   Name: automation-empire"
echo "   Description: AI-powered dual creator content automation"
echo "   Visibility: PRIVATE ⚠️"
echo "   Do NOT initialize with README"
echo ""
echo "3. After creating the repo, run:"
echo "   ./connect-github.sh <your-github-username>"
echo ""
echo "✅ SSH key has been generated and saved"
echo "📋 Setup guide saved to: ~/GITHUB-SETUP-GUIDE.md"

