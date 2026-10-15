#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "=============================================================================="
echo "   YOUTUBE SHORTS PERFORMANCE ANALYSIS & VIRALITY PREDICTION PLATFORM"
echo "   Subject: Social Media | Parul University | Student: Thota Abhiram"
echo "=============================================================================="
echo ""
echo "[1/3] Running Analytical Validation Tests..."
python3 -m unittest discover tests

echo ""
echo "[2/3] Verifying PowerPoint Presentation..."
if [ ! -f "presentation/YouTube_Shorts_Performance_Analysis.pptx" ]; then
    python3 presentation/generate_pptx.py
else
    echo "[OK] Presentation ready: presentation/YouTube_Shorts_Performance_Analysis.pptx"
fi

echo ""
echo "[3/3] Launching Web Analytics Dashboard..."
echo "Dashboard running at: http://localhost:8000"
python3 server.py
