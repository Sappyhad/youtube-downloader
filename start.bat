@echo off
cd /d "%~dp0"

netstat -ano | findstr /r /c:"127\.0\.0\.1:5000 .*LISTENING" >nul && (
    echo YT Downloader is already running - opening the browser.
    start "" http://127.0.0.1:5000
    exit /b 0
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv || (echo ERROR: Python not found - install Python 3.10+ and add it to PATH. & pause & exit /b 1)
)

echo Checking for library updates...
.venv\Scripts\python -m pip install --upgrade --quiet --disable-pip-version-check -r requirements.txt
if errorlevel 1 echo WARNING: Library update failed ^(offline?^) - starting with installed versions.

start "" http://127.0.0.1:5000
.venv\Scripts\python app.py
pause
