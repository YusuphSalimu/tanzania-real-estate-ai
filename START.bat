@echo off
echo ========================================
echo Tanzania Real Estate AI Platform
echo ========================================
echo.
echo Starting Backend Server...
cd backend
..\venv\Scripts\python.exe -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
pause
