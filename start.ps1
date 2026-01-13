# AI+X Community - Local Server Launcher (PowerShell)
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "          AI+X Community - Local Server Launcher" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting local server..." -ForegroundColor Yellow
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from: https://www.python.org/" -ForegroundColor Yellow
    Write-Host "Or use another method to run a local server" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Run Python server
Write-Host "Starting server..." -ForegroundColor Green
python start-server.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Failed to start server" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
