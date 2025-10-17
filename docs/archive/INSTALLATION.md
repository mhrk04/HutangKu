# 🚀 Installation Guide - HutangKu - Debt Management

## Quick Installation (Recommended)

### Step 1: Install Prerequisites

#### MongoDB

**macOS:**

```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

**Windows:**
Download and install from: https://www.mongodb.com/try/download/community

#### Python 3.9+

Check if Python is installed:

```bash
python3 --version
```

If not installed:

- **macOS:** `brew install python3`
- **Linux:** `sudo apt-get install python3 python3-pip python3-venv`
- **Windows:** Download from https://www.python.org/downloads/

### Step 2: Setup the Project

Navigate to the project directory and run the setup script:

```bash
cd Debt-Manager-Portal
./setup.sh
```

This will:

- ✅ Create a virtual environment in `venv/`
- ✅ Activate the virtual environment
- ✅ Upgrade pip to the latest version
- ✅ Install all dependencies from `requirements.txt`

### Step 3: Run the Application

```bash
./run_app.sh
```

This will:

- ✅ Activate the virtual environment
- ✅ Check if MongoDB is running
- ✅ Start the backend on port 8000
- ✅ Start the frontend on port 8501

### Step 4: Access the Application

Open your browser and go to:

- **Frontend:** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## Manual Installation

If you prefer to set up everything manually:

### 1. Create Virtual Environment

```bash
cd Debt-Manager-Portal
python3 -m venv venv
```

### 2. Activate Virtual Environment

**macOS/Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Check FastAPI is installed
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"

# Check Streamlit is installed
python -c "import streamlit; print('Streamlit:', streamlit.__version__)"

# Check Motor is installed
python -c "import motor; print('Motor:', motor.version)"
```

### 5. Start MongoDB

**macOS:**

```bash
brew services start mongodb-community
```

**Linux:**

```bash
sudo systemctl start mongodb
```

**Manual start:**

```bash
mongod
```

### 6. Run Backend (Terminal 1)

```bash
cd Debt-Manager-Portal
source venv/bin/activate  # Activate venv
uvicorn backend.main:app --reload --port 8000
```

### 7. Run Frontend (Terminal 2)

```bash
cd Debt-Manager-Portal
source venv/bin/activate  # Activate venv
streamlit run frontend/Home.py
```

---

## Troubleshooting Installation

### Virtual Environment Issues

**Problem:** `venv` command not found

**Solution:**

```bash
# Install venv module
sudo apt-get install python3-venv  # Linux
# or
pip install virtualenv
```

**Problem:** Cannot activate virtual environment

**Solution:**

```bash
# On macOS/Linux, make sure you're using:
source venv/bin/activate

# On Windows, use:
venv\Scripts\activate

# Or try:
. venv/bin/activate
```

### MongoDB Issues

**Problem:** MongoDB not running

**Solution:**

```bash
# Check if MongoDB is running
pgrep mongod

# Start MongoDB
brew services start mongodb-community  # macOS
sudo systemctl start mongodb           # Linux
mongod                                 # Manual start
```

**Problem:** MongoDB connection refused

**Solution:**

```bash
# Check MongoDB status
brew services list | grep mongodb      # macOS
sudo systemctl status mongodb          # Linux

# Restart MongoDB
brew services restart mongodb-community  # macOS
sudo systemctl restart mongodb           # Linux
```

### Dependency Issues

**Problem:** Package installation fails

**Solution:**

```bash
# Upgrade pip first
pip install --upgrade pip

# Clear pip cache
pip cache purge

# Reinstall dependencies
pip install -r requirements.txt --no-cache-dir
```

**Problem:** Import errors when running the app

**Solution:**

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Verify you're in the correct directory
pwd  # Should show .../Debt-Manager-Portal

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Issues

**Problem:** Port 8000 or 8501 already in use

**Solution:**

```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill

# Find and kill process on port 8501
lsof -ti:8501 | xargs kill

# Or use different ports
uvicorn backend.main:app --reload --port 8080
streamlit run frontend/Home.py --server.port 8502
```

### Permission Issues

**Problem:** Permission denied when running scripts

**Solution:**

```bash
# Make scripts executable
chmod +x setup.sh run_app.sh

# Or run with bash
bash setup.sh
bash run_app.sh
```

---

## Deactivating Virtual Environment

When you're done working on the project:

```bash
deactivate
```

This returns you to your system's default Python environment.

---

## Reactivating Virtual Environment

Next time you work on the project:

```bash
cd Debt-Manager-Portal
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

Then run the application:

```bash
./run_app.sh
```

---

## Uninstalling

To completely remove the project:

```bash
cd Debt-Manager-Portal

# Deactivate virtual environment if active
deactivate

# Remove virtual environment
rm -rf venv/

# Optional: Remove MongoDB data
brew services stop mongodb-community  # macOS
sudo systemctl stop mongodb           # Linux
```

---

## Updating Dependencies

To update all dependencies to the latest versions:

```bash
# Activate virtual environment
source venv/bin/activate

# Upgrade all packages
pip install --upgrade -r requirements.txt

# Or update specific package
pip install --upgrade fastapi
```

---

## Environment Variables (Optional)

Create a `.env` file in the project root for custom configuration:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
API_HOST=localhost
API_PORT=8000
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=debt_management
DUE_DATE_WARNING_DAYS=7
```

---

## Verification Checklist

After installation, verify everything is working:

- [ ] Virtual environment created and activated
- [ ] All dependencies installed without errors
- [ ] MongoDB is running
- [ ] Backend starts without errors (port 8000)
- [ ] Frontend starts without errors (port 8501)
- [ ] Can access frontend at http://localhost:8501
- [ ] Can access API docs at http://localhost:8000/docs
- [ ] Can create a test debt record
- [ ] Dashboard displays correctly

---

## Getting Help

If you encounter issues not covered here:

1. Check the error message carefully
2. Review `README.md` for detailed documentation
3. Check `QUICKSTART.md` for quick tips
4. Ensure you're in the correct directory
5. Verify virtual environment is activated
6. Check MongoDB is running

---

## Next Steps

Once installation is complete:

1. Read `QUICKSTART.md` for usage examples
2. Add your first debt record
3. Explore the Dashboard and API docs
4. Customize settings in `core/config.py`

**Installation complete! Start managing your debts! 💰**
