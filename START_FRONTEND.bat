@echo off
echo ========================================
echo Tanzania Real Estate AI Platform
echo ========================================
echo.
echo Starting Frontend Server...
cd frontend
..\venv\Scripts\python.exe -m http.server 5173 --bind 0.0.0.0
pause
