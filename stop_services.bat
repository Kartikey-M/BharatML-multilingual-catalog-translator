@echo off
echo 🛑 Stopping Multi-Lingual Catalog Translator Services...
echo.

echo Terminating all Python processes...
taskkill /f /im python.exe >nul 2>nul
taskkill /f /im uvicorn.exe >nul 2>nul
taskkill /f /im streamlit.exe >nul 2>nul

echo.
echo ✅ All services stopped!
echo.
pause
