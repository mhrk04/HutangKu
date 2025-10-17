#!/bin/bash

echo "🔧 Setting up HutangKu - Debt Management..."
echo ""

# Check if in correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the Debt-Manager-Portal directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created!"
    echo ""
else
    echo "✅ Virtual environment already exists"
    echo ""
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Activate the virtual environment:"
echo "      source venv/bin/activate"
echo ""
echo "   2. Make sure MongoDB is running:"
echo "      brew services start mongodb-community  # macOS"
echo "      sudo systemctl start mongodb           # Linux"
echo ""
echo "   3. Run the application:"
echo "      ./run_app.sh"
echo ""
echo "   Or run services separately:"
echo "      Terminal 1: uvicorn backend.main:app --reload --port 8000"
echo "      Terminal 2: streamlit run frontend/Home.py"
echo ""
