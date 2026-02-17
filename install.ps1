# Quick Installation Script for Jarvis
# Run this in PowerShell to install all dependencies

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Jarvis Installation Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[1/3] Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found! Please install Python 3.7+ first." -ForegroundColor Red
    Write-Host "    Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "[2/3] Installing Python packages..." -ForegroundColor Yellow
Write-Host "  Installing: pyaudio, numpy, pyttsx3" -ForegroundColor Gray

pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Warning: Some packages may have failed to install." -ForegroundColor Yellow
    Write-Host "    If PyAudio failed, visit:" -ForegroundColor Yellow
    Write-Host "    https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio" -ForegroundColor Cyan
}

# Configuration reminder
Write-Host ""
Write-Host "[3/3] Setup Instructions:" -ForegroundColor Yellow
Write-Host "  1. Open jarvis_clap_automation.py" -ForegroundColor Gray
Write-Host "  2. Edit the APP_CONFIG dictionary (lines 15-25)" -ForegroundColor Gray
Write-Host "  3. Add your application paths using raw strings: r'C:\Path\To\App.exe'" -ForegroundColor Gray
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start Jarvis, run:" -ForegroundColor Yellow
Write-Host "  python jarvis_clap_automation.py" -ForegroundColor Cyan
Write-Host ""
