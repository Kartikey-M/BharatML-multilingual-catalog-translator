#!/bin/bash

echo "========================================"
echo "  Multi-Lingual Catalog Translator"
echo "  Docker Deployment"
echo "========================================"
echo

echo "🔧 Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found! Please install Docker"
    echo "📥 Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker found"

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found! Please install Docker Compose"
    echo "📥 Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker Compose found"
echo

echo "🏗️ Building and starting containers..."
echo "This may take several minutes on first run..."
echo

docker-compose up --build -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start containers"
    echo
    echo "📋 Checking logs:"
    docker-compose logs
    exit 1
fi

echo
echo "✅ Containers started successfully!"
echo

echo "⏳ Waiting for services to be ready..."
sleep 30

echo
echo "🔍 Checking service health..."
docker-compose ps

echo
echo "📱 Access your application:"
echo "🔗 Frontend UI:    http://localhost:8501"
echo "🔗 Backend API:    http://localhost:8001"
echo "🔗 API Docs:       http://localhost:8001/docs"
echo

echo "💡 Useful commands:"
echo "  View logs:     docker-compose logs -f"
echo "  Stop services: docker-compose down"
echo "  Restart:       docker-compose restart"
echo

echo "🎉 Docker deployment complete!"
echo "Opening frontend in browser..."

# Try to open browser
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8501
elif command -v open &> /dev/null; then
    open http://localhost:8501
else
    echo "Please open http://localhost:8501 in your browser"
fi

echo
echo "📊 Following logs (Press Ctrl+C to stop):"
echo "----------------------------------------"
docker-compose logs -f
