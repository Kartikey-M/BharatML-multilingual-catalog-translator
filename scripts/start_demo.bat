@echo off
echo ========================================
echo   Multi-Lingual Catalog Translator
echo   Quick Demo Deployment
echo ========================================
echo.

echo 🔧 Checking prerequisites...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.11+
    pause
    exit /b 1
)

echo ✅ Python found
echo.

echo 🚀 Starting Backend Server...
echo Opening new window for backend...
start "Translator Backend" cmd /k "cd /d %~dp0backend && echo Starting Backend API on port 8001... && uvicorn main:app --host 0.0.0.0 --port 8001"

echo.
echo ⏳ Waiting for backend to initialize (15 seconds)...
timeout /t 15 /nobreak >nul

echo.
echo 🎨 Starting Frontend Server...
echo Opening new window for frontend...
start "Translator Frontend" cmd /k "cd /d %~dp0frontend && echo Starting Streamlit Frontend on port 8501... && streamlit run app.py --server.port 8501"

echo.
echo ✅ Deployment Complete!
echo.
echo 📱 Access your application:
echo 🔗 Frontend UI:    http://localhost:8501
echo 🔗 Backend API:    http://localhost:8001
echo 🔗 API Docs:       http://localhost:8001/docs
echo.
echo 💡 Tips:
echo - Wait 30-60 seconds for models to load
echo - Check the backend window for loading progress
echo - Both windows will stay open for monitoring
echo.
echo 🛑 To stop all services:
echo   Run: stop_services.bat
echo   Or close both command windows
echo.
echo Press any key to open the frontend in your browser...
pause >nul

start http://localhost:8501

echo.
echo 🎉 Application is now running!
echo Check the opened browser window.
