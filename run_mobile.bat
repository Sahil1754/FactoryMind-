@echo off
setlocal
title FactoryMind AI - Flutter Mobile App Launcher

echo ========================================================
echo       FACTORYMIND AI - FLUTTER MOBILE APP
echo ========================================================
echo.

where flutter >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Flutter SDK is not detected in your PATH.
    echo Please install Flutter or add Flutter to your environment PATH.
    echo You can also test the full platform immediately via the Web Dashboard at:
    echo   http://127.0.0.1:8000/dashboard
    echo.
    pause
    exit /b 1
)

cd /d "%~dp0mobile"
echo [1/2] Fetching Flutter dependencies...
call flutter pub get

echo [2/2] Running FactoryMind Mobile on connected device/emulator...
call flutter run
pause
