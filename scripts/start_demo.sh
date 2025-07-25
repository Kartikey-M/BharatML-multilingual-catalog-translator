#!/bin/bash

echo "========================================"
echo "  Multi-Lingual Catalog Translator"
echo "  Quick Demo Deployment"
echo "========================================"
echo

echo "🔧 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Please install Python 3.11+"
    exit 1
fi

echo "✅ Python3 found"
echo

# Function to cleanup on exit
cleanup() {
    echo
    echo "🛑 Stopping services..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo "✅ Services stopped"
    exit 0
}

# Setup signal handlers
trap cleanup SIGINT SIGTERM

echo "🚀 Starting Backend Server..."
cd backend
echo "Starting Backend API on port 8001..."
uvicorn main:app --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!
cd ..

echo
echo "⏳ Waiting for backend to initialize (15 seconds)..."
sleep 15

echo
echo "🎨 Starting Frontend Server..."
cd frontend
echo "Starting Streamlit Frontend on port 8501..."
streamlit run app.py --server.port 8501 &
FRONTEND_PID=$!
cd ..

echo
echo "✅ Deployment Complete!"
echo
echo "📱 Access your application:"
echo "🔗 Frontend UI:    http://localhost:8501"
echo "🔗 Backend API:    http://localhost:8001"
echo "🔗 API Docs:       http://localhost:8001/docs"
echo
echo "💡 Tips:"
echo "- Wait 30-60 seconds for models to load"
echo "- Check logs below for loading progress"
echo "- Press Ctrl+C to stop all services"
echo
echo "🎉 Application is now running!"
echo "Opening frontend in browser..."

# Try to open browser (works on most systems)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8501
elif command -v open &> /dev/null; then
    open http://localhost:8501
else
    echo "Please open http://localhost:8501 in your browser"
fi

echo
echo "📊 Monitoring logs (Press Ctrl+C to stop):"
echo "----------------------------------------"

# Wait for processes to finish or for interrupt
wait
