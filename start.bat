@echo off
echo ============================================================
echo          AI+X Community - Local Server Launcher
echo ============================================================
echo.
echo Starting local server...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/
    echo Or use another method to run a local server
    echo.
    pause
    exit /b 1
)

REM 运行Python服务器
python start-server.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to start server
    pause
    exit /b 1
)
