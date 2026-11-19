@echo off
setlocal enabledelayedexpansion
title FactoryMind AI - Instant Free Public Domain

echo ===============================================================================
echo        FACTORYMIND AI — INSTANT FREE PUBLIC DOMAIN LAUNCHER
echo ===============================================================================
echo.
echo This tool generates a 100%% FREE public HTTPS domain for FactoryMind AI,
echo allowing your college evaluators, professors, or mobile devices to access
echo your live platform from anywhere in the world!
echo.
echo Note: Make sure FactoryMind AI backend is running (port 8000).
echo.
echo Choose your preferred Free Domain provider:
echo.
echo   [1] Cloudflare Quick Tunnel (Recommended - Fast, Secure, No Signup needed)
echo       Domain format: https://<random-name>.trycloudflare.com
echo.
echo   [2] Localhost.run (Zero Downloads - uses built-in Windows SSH)
echo       Domain format: https://<unique-id>.lhr.life
echo.
echo   [3] Pinggy Tunnel (Fast SSH tunnel)
echo       Domain format: https://<random>.a.free.pinggy.link
echo.
echo   [4] ngrok (Requires ngrok installed)
echo       Domain format: https://<subdomain>.ngrok-free.app
echo.
echo   [5] Exit
echo.
echo ===============================================================================
set /p opt="Enter choice [1-5] (Default is 1): "

if "%opt%"=="" set opt=1
if "%opt%"=="1" goto CLOUDFLARE
if "%opt%"=="2" goto LOCALHOSTRUN
if "%opt%"=="3" goto PINGGY
if "%opt%"=="4" goto NGROK
if "%opt%"=="5" exit /b 0

:CLOUDFLARE
echo.
echo [1/2] Checking for Cloudflare Tunnel binary...
if not exist "%~dp0cloudflared.exe" (
    echo Downloading standalone cloudflared.exe from Cloudflare...
    curl -L -s -o "%~dp0cloudflared.exe" "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    if not exist "%~dp0cloudflared.exe" (
        echo [ERROR] Automatic download failed. Switching to Localhost.run...
        goto LOCALHOSTRUN
    )
    echo Download complete!
)

echo [2/2] Starting Cloudflare Public Tunnel for http://127.0.0.1:8000 ...
echo Look below for your free public domain URL ending in: .trycloudflare.com
echo -------------------------------------------------------------------------------
"%~dp0cloudflared.exe" tunnel --url http://127.0.0.1:8000
pause
exit /b 0

:LOCALHOSTRUN
echo.
echo Starting Localhost.run tunnel via built-in Windows SSH...
echo Look below for your free public HTTPS domain link:
echo -------------------------------------------------------------------------------
ssh -o StrictHostKeyChecking=no -R 80:localhost:8000 nokey@localhost.run
pause
exit /b 0

:PINGGY
echo.
echo Starting Pinggy tunnel via built-in Windows SSH...
echo Look below for your free public HTTPS domain link:
echo -------------------------------------------------------------------------------
ssh -o StrictHostKeyChecking=no -p 443 -R 0:localhost:8000 a.pinggy.io
pause
exit /b 0

:NGROK
echo.
echo Starting ngrok tunnel on port 8000...
ngrok http 8000
pause
exit /b 0
