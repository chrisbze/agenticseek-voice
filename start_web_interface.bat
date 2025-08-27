@echo off
echo ========================================
echo AgenticSeek Voice-Enabled Web Interface
echo ========================================
echo.
echo Starting the web interface with voice capabilities...
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH.
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo Node.js detected: 
node --version

echo.
echo Navigating to frontend directory...
cd /d "%~dp0frontend\agentic-seek-front"

echo.
echo Installing dependencies (if needed)...
if not exist "node_modules" (
    echo Running npm install...
    npm install
) else (
    echo Dependencies already installed.
)

echo.
echo ========================================
echo Starting React Development Server...
echo ========================================
echo.
echo The web interface will open at: http://localhost:3000
echo Backend should be running at: http://localhost:7777
echo.
echo Voice commands available in the web interface!
echo Click the "Voice" button in the header to start.
echo.

REM Set environment variable for backend URL
set REACT_APP_BACKEND_URL=http://localhost:7777

REM Start the React development server
npm start

pause