@echo off
echo ========================================
echo   Deployment Status Check
echo ========================================
echo.

echo 🔍 Checking service status...
echo.

echo [Backend API - Port 8001]
curl -s http://localhost:8001/ >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ Backend API is responding
) else (
    echo ❌ Backend API is not responding
)

echo.
echo [Frontend UI - Port 8501]
curl -s http://localhost:8501/_stcore/health >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ Frontend UI is responding
) else (
    echo ❌ Frontend UI is not responding
)

echo.
echo [API Documentation]
curl -s http://localhost:8001/docs >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ API documentation is available
) else (
    echo ❌ API documentation is not available
)

echo.
echo [Supported Languages Check]
curl -s http://localhost:8001/supported-languages >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ Translation service is loaded
) else (
    echo ❌ Translation service is not ready
)

echo.
echo 📊 Quick Access Links:
echo 🔗 Frontend:  http://localhost:8501
echo 🔗 Backend:   http://localhost:8001
echo 🔗 API Docs:  http://localhost:8001/docs
echo.

pause
