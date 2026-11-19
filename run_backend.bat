@echo off
setlocal
echo ========================================================
echo       FACTORYMIND AI - PREDICTIVE MANUFACTURING
echo ========================================================

set PYTHON_BIN=py
where py >nul 2>nul
if %errorlevel% neq 0 (
    set PYTHON_BIN="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)

echo [1/3] Verifying backend dependencies...
cd /d "%~dp0backend"
%PYTHON_BIN% -m pip install -r requirements.txt

echo [2/3] Seeding initial industrial fleet data...
%PYTHON_BIN% seed_data.py

echo [3/3] Launching FactoryMind AI Platform at http://127.0.0.1:8000 ...
start http://127.0.0.1:8000/login
%PYTHON_BIN% -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause

