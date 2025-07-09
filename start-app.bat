@echo off
title Air Quality App - Starting...
echo Starting Air Quality App...
echo.

REM Start the backend (Flask) in a new window
start "Backend (Flask)" /min cmd /c "python app.py"

REM Wait 3 seconds for backend to start
timeout /t 3 /nobreak > nul

REM Start the frontend (React) in a new window
start "Frontend (React)" /min cmd /c "cd frontend && npm start"

echo.
echo Both servers are starting:
echo - Backend (Flask): http://localhost:5000
echo - Frontend (React): http://localhost:3000
echo.
echo Press any key to stop all servers...
pause > nul

REM Kill all Node.js and Python processes related to our app
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul

echo Servers stopped.
pause
