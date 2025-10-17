#!/bin/bash

echo "🚀 Starting HutangKu - Debt Management..."
echo ""

# Check if in correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the Debt-Manager-Portal directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "   Please run setup first: ./setup.sh"
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  Warning: MongoDB doesn't appear to be running."
    echo "   Please start MongoDB first:"
    echo "   - macOS: brew services start mongodb-community"
    echo "   - Linux: sudo systemctl start mongodb"
    echo ""
fi

echo "🔧 Starting Backend (FastAPI on port 8000)..."
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""

# Start backend in background
uvicorn backend.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start and check if it's running
sleep 3
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Error: Backend failed to start"
    exit 1
fi

echo "🎨 Starting Frontend (Streamlit on port 8501)..."
echo "   URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Start frontend in foreground
streamlit run frontend/Dashboard.py

# Cleanup: kill backend when frontend stops
kill $BACKEND_PID 2>/dev/null
echo ""
echo "✅ Services stopped"
