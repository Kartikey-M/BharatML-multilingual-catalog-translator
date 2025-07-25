@echo off
echo ========================================
echo   Multi-Lingual Catalog Translator
echo   Docker Deployment
echo ========================================
echo.

echo 🔧 Checking Docker installation...
docker --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker not found! Please install Docker Desktop
    echo 📥 Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker found
echo.

docker-compose --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker Compose not found! Please install Docker Compose
    pause
    exit /b 1
)

echo ✅ Docker Compose found
echo.

echo 🏗️ Building and starting containers...
echo This may take several minutes on first run...
echo.

docker-compose up --build -d

if %errorlevel% neq 0 (
    echo ❌ Failed to start containers
    echo.
    echo 📋 Checking logs:
    docker-compose logs
    pause
    exit /b 1
)

echo.
echo ✅ Containers started successfully!
echo.

echo ⏳ Waiting for services to be ready...
timeout /t 30 /nobreak >nul

echo.
echo 🔍 Checking service health...
docker-compose ps

echo.
echo 📱 Access your application:
echo 🔗 Frontend UI:    http://localhost:8501
echo 🔗 Backend API:    http://localhost:8001
echo 🔗 API Docs:       http://localhost:8001/docs
echo.

echo 💡 Useful commands:
echo   View logs:     docker-compose logs -f
echo   Stop services: docker-compose down
echo   Restart:       docker-compose restart
echo.

echo 🎉 Docker deployment complete!
echo Opening frontend in browser...
start http://localhost:8501

echo.
echo Press any key to view logs...
pause >nul
docker-compose logs -f
