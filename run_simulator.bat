@echo off
setlocal
echo ========================================================
echo       FACTORYMIND AI - IOT TELEMETRY STREAMER
echo ========================================================

set PYTHON_BIN=py
where py >nul 2>nul
if %errorlevel% neq 0 (
    set PYTHON_BIN="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)

cd /d "%~dp0backend"
%PYTHON_BIN% simulator/iot_simulator.py --interval 3.0
pause

