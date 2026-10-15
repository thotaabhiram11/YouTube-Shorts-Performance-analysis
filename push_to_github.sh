#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "=============================================================================="
echo "       PUSH YOUTUBE SHORTS ANALYTICS & PPTX TO GITHUB"
echo "       Subject: Social Media | Parul University | Thota Abhiram"
echo "=============================================================================="
echo ""

if ! command -v git &> /dev/null; then
    echo "[ERROR] Git is not installed. Please install git and retry."
    exit 1
fi

echo "[1/4] Checking Git repository..."
if [ ! -d ".git" ]; then
    git init
    git branch -M main
fi

echo "[2/4] Staging files including PowerPoint (.pptx)..."
git add core/ data/ web/ presentation/ tests/ cli.py server.py run.bat run.sh push_to_github.bat push_to_github.sh LICENSE README.md .gitignore

echo "[3/4] Creating commit..."
git commit -m "Initial commit: YouTube Shorts Performance Analysis & PPTX (Social Media Project - Thota Abhiram)" || true

echo ""
read -p "Enter your GitHub Repository URL (or press Enter to skip): " REPO_URL

if [ -n "$REPO_URL" ]; then
    git remote remove origin 2>/dev/null || true
    git remote add origin "$REPO_URL"
    git branch -M main
    echo "Pushing to GitHub..."
    git push -u origin main
    echo "SUCCESS! Project and PPTX pushed to GitHub."
else
    echo "Skipped remote push. Local commit is ready."
fi
