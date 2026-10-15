@echo off
setlocal enabledelayedexpansion
title Push YouTube Shorts Analytics Project to GitHub
cd /d "%~dp0"

echo ==============================================================================
echo       PUSH YOUTUBE SHORTS ANALYTICS & PPTX TO GITHUB
echo       Subject: Social Media ^| Parul University ^| Thota Abhiram
echo ==============================================================================
echo.

where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/ and try again.
    pause
    exit /b 1
)

echo [1/4] Checking Git repository status...
if not exist ".git" (
    echo Initializing new Git repository...
    git init
    git branch -M main
)

echo.
echo [2/4] Staging all project files and PowerPoint slides (.pptx)...
git add core/ data/ web/ presentation/ tests/ cli.py server.py run.bat run.sh push_to_github.bat push_to_github.sh LICENSE README.md .gitignore

echo Staging status:
git status --short

echo.
echo [3/4] Creating commit...
git commit -m "Initial commit: YouTube Shorts Performance Analysis & PPTX (Social Media Project - Thota Abhiram)"

echo.
echo [4/4] Configure GitHub Remote Repository:
echo.
echo If you have not created a repository on GitHub yet:
echo   1. Open https://github.com/new in your browser
echo   2. Name your repository (e.g., youtube-shorts-performance-analysis)
echo   3. Do NOT initialize with README, .gitignore or license (already included!)
echo   4. Click 'Create repository' and copy the HTTPS URL.
echo.
set /p REPO_URL="Enter your GitHub Repository URL (or press Enter to skip push): "

if "%REPO_URL%"=="" (
    echo.
    echo [INFO] Skipped remote push. Your files and PPTX are safely committed locally.
    echo When you are ready to push later, run:
    echo   git remote add origin ^<YOUR_GITHUB_REPO_URL^>
    echo   git push -u origin main
    echo.
    pause
    exit /b 0
)

echo Setting remote origin to %REPO_URL%...
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main

echo Pushing code and PowerPoint deck to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ==============================================================================
    echo  SUCCESS! Project and PPTX successfully pushed to GitHub!
    echo ==============================================================================
) else (
    echo.
    echo [NOTE] If git push failed, verify your GitHub credentials or run:
    echo   git push -u origin main --force
)

echo.
pause
