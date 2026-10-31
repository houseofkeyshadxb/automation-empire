#!/bin/bash
# Connect local repo to GitHub

if [ -z "$1" ]; then
    echo "Usage: ./connect-github.sh <github-username>"
    echo "Example: ./connect-github.sh keysha2000"
    exit 1
fi

GITHUB_USER="$1"
REPO_NAME="automation-empire"

echo "🔗 Connecting to GitHub..."
echo ""

cd ~

# Add remote
git remote add origin "git@github.com:${GITHUB_USER}/${REPO_NAME}.git" 2>/dev/null || \
    git remote set-url origin "git@github.com:${GITHUB_USER}/${REPO_NAME}.git"

# Rename branch to main
git branch -M main

echo "✅ Remote configured: git@github.com:${GITHUB_USER}/${REPO_NAME}.git"
echo ""
echo "📤 Pushing to GitHub..."

# Test SSH connection first
ssh -T git@github.com 2>&1 | grep -q "successfully authenticated" && \
    echo "✅ SSH authentication working" || \
    echo "⚠️  SSH may need verification (check GitHub settings)"

echo ""
echo "🚀 Ready to push! Run:"
echo "   cd ~"
echo "   git push -u origin main"
echo ""
echo "Or to push now:"
read -p "Push to GitHub now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push -u origin main
    echo ""
    echo "✅ Code pushed to GitHub!"
    echo "🔗 View at: https://github.com/${GITHUB_USER}/${REPO_NAME}"
fi

