@echo off
cd /d "%~dp0backend"

start "FAQ Chatbot Backend" cmd /k "python app.py"

timeout /t 3 /nobreak >nul

start "" "%~dp0frontend\index.html"

exit