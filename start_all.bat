@echo off
setlocal enabledelayedexpansion
title FactoryMind AI - Master Platform Launcher

set PYTHON_BIN=py
where py >nul 2>nul
if %errorlevel% neq 0 (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set PYTHON_BIN="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    ) else (
        set PYTHON_BIN=python
    )
)

:MENU
cls
echo ===============================================================================
echo        FACTORYMIND AI - PREDICTIVE MANUFACTURING PLATFORM
echo       Dual Architecture: Python AI/ML Diagnostic Engine + Java Edge Gateway
echo       Interactive 3D WebGL Digital Twin & Synthesized Cyber Audio SFX
echo ===============================================================================
echo.
echo   [1] Launch Full Platform (Python Backend + 3D Web Console + IoT Streamer)
echo   [2] Launch Python AI Backend Server (FastAPI on port 8000)
echo   [3] Launch Java Industrial Edge Gateway (PLC Telemetry Daemon)
echo   [4] Launch Python IoT Telemetry Streamer (High-Frequency Simulator)
echo   [5] Open Web Console in Default Browser (http://127.0.0.1:8000/login)
echo   [6] Generate Instant Free Public HTTPS Domain (Share with Viva/Evaluators)
echo   [7] Open SY MCA Project Presentation Deck (Interactive HTML5 in Browser)
echo   [8] Open Presentation in Microsoft PowerPoint (.pptx File)
echo   [9] Exit
echo.
echo ===============================================================================
set /p opt="Enter your choice [1-9] (Default is 1): "

if "%opt%"=="" set opt=1
if "%opt%"=="1" goto LAUNCH_FULL
if "%opt%"=="2" goto LAUNCH_BACKEND
if "%opt%"=="3" goto LAUNCH_JAVA
if "%opt%"=="4" goto LAUNCH_STREAMER
if "%opt%"=="5" goto LAUNCH_BROWSER
if "%opt%"=="6" goto LAUNCH_DOMAIN
if "%opt%"=="7" goto LAUNCH_PPT
if "%opt%"=="8" goto LAUNCH_PPTX
if "%opt%"=="9" exit /b 0
goto MENU

:LAUNCH_FULL
echo.
echo [1/3] Verifying database seeding...
cd /d "%~dp0backend"
%PYTHON_BIN% seed_data.py >nul 2>&1

echo [2/3] Launching FastAPI AI Diagnostics Server on http://127.0.0.1:8000 ...
start "FactoryMind AI - Python Backend" cmd /k "cd /d ""%~dp0backend"" && %PYTHON_BIN% -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

timeout /t 2 /nobreak >nul
echo [3/3] Launching Python IoT Telemetry Streamer (2.5s cadence)...
start "FactoryMind AI - IoT Telemetry Streamer" cmd /k "cd /d ""%~dp0backend"" && %PYTHON_BIN% simulator\iot_simulator.py --interval 2.5"

timeout /t 1 /nobreak >nul
echo Opening FactoryMind AI Web Console...
start http://127.0.0.1:8000/login

echo.
echo ===============================================================================
echo [SUCCESS] FactoryMind AI is fully active!
echo  - Standalone Login Portal : http://127.0.0.1:8000/login
echo  - 3D Digital Twin Console : http://127.0.0.1:8000/dashboard
echo  - Presentation Slide Deck : http://127.0.0.1:8000/presentation
echo  - Interactive API Docs    : http://127.0.0.1:8000/api/v1/docs
echo ===============================================================================
echo Press any key to return to menu...
pause >nul
goto MENU

:LAUNCH_BACKEND
cd /d "%~dp0backend"
%PYTHON_BIN% seed_data.py >nul 2>&1
start "FactoryMind AI - Python Backend" cmd /k "cd /d ""%~dp0backend"" && %PYTHON_BIN% -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
goto MENU

:LAUNCH_JAVA
call "%~dp0run_java_gateway.bat"
goto MENU

:LAUNCH_STREAMER
cd /d "%~dp0backend"
start "FactoryMind AI - IoT Telemetry Streamer" cmd /k "cd /d ""%~dp0backend"" && %PYTHON_BIN% simulator\iot_simulator.py --interval 2.0"
goto MENU

:LAUNCH_BROWSER
start http://127.0.0.1:8000/login
goto MENU

:LAUNCH_DOMAIN
call "%~dp0run_free_domain.bat"
goto MENU

:LAUNCH_PPT
start "" "%~dp0presentation.html"
goto MENU

:LAUNCH_PPTX
echo Opening Microsoft PowerPoint presentation...
start "" "%~dp0FactoryMind_AI_SY_MCA_Second_Presentation.pptx"
goto MENU
