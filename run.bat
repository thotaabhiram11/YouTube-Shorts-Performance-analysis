@echo off
title YouTube Shorts Performance Analysis Dashboard
cd /d "%~dp0"

echo ==============================================================================
echo    YOUTUBE SHORTS PERFORMANCE ANALYSIS ^& VIRALITY PREDICTION PLATFORM
echo    Subject: Social Media ^| Parul University ^| Student: Thota Abhiram
echo ==============================================================================
echo.
echo [1/3] Running Analytical Validation Tests...
python -m unittest discover tests
if %errorlevel% neq 0 (
    echo [WARNING] Some tests reported issues, proceeding with server startup...
) else (
    echo [OK] All analytical invariant tests passed!
)
echo.
echo [2/3] Verifying PowerPoint Slide Deck (.pptx)...
if not exist "presentation\YouTube_Shorts_Performance_Analysis.pptx" (
    echo Compiling PowerPoint presentation...
    python presentation\generate_pptx.py
) else (
    echo [OK] PowerPoint Presentation ready: presentation\YouTube_Shorts_Performance_Analysis.pptx
)
echo.
echo [3/3] Launching Web Analytics Dashboard...
echo Dashboard URL: http://localhost:8000
echo Opening browser...
start http://localhost:8000
echo.
python server.py
pause
