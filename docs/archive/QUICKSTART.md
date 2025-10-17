# Quick Start Guide - HutangKu - Debt Management

## ⚡ Fast Setup (5 minutes)

### Step 1: Install MongoDB

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
Download from: https://www.mongodb.com/try/download/community

### Step 2: Setup Virtual Environment and Install Dependencies

```bash
cd Debt-Manager-Portal

# Make setup script executable
chmod +x setup.sh

# Run setup (creates venv and installs dependencies)
./setup.sh
```

**What this does:**

- Creates a Python virtual environment in `venv/`
- Activates the virtual environment
- Installs all required dependencies from `requirements.txt`

**Manual Setup (if needed):**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Run the Application

**Option A: Using the startup script (Recommended)**

```bash
# Make script executable (first time only)
chmod +x run_app.sh

# Run the application
./run_app.sh
```

This automatically activates the virtual environment and starts both services.

**Option B: Run manually in separate terminals**

First, activate the virtual environment in both terminals:

```bash
source venv/bin/activate  # macOS/Linux
```

Terminal 1 (Backend):

```bash
cd Debt-Manager-Portal
uvicorn backend.main:app --reload --port 8000
```

Terminal 2 (Frontend):

```bash
cd Debt-Manager-Portal
streamlit run frontend/Home.py
```

### Step 4: Access the Application

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🎯 First Use

1. Navigate to http://localhost:8501
2. Click "Go to Manage Debts"
3. Add your first debt using the form
4. Return to Dashboard to see your debt summary

## 📝 Example Test Data

Add these sample debts to test the application:

**Debt 1:**

- Company: Atome
- Amount Owed: 500.00
- Minimum Payment: 100.00
- Due Date: (Tomorrow's date)
- Status: Active Debt
- Notes: Phone payment plan

**Debt 2:**

- Company: Shopee
- Amount Owed: 1200.00
- Minimum Payment: 400.00
- Due Date: (7 days from now)
- Status: Active Debt
- Notes: Laptop purchase

**Debt 3:**

- Company: Atome
- Amount Owed: 300.00
- Minimum Payment: 150.00
- Due Date: (30 days from now)
- Status: Active Debt
- Notes: Headphones

## 🔍 Testing Features

### Test Notifications

- Add a debt with tomorrow's due date
- Check Dashboard for urgent notification (red alert)

### Test BNPL Grouping

- Add multiple debts with the same company name
- Check Dashboard to see them grouped together
- Total debt per company should be calculated

### Test CRUD Operations

1. **Create**: Add a debt via Manage Debts page
2. **Read**: View it on Dashboard
3. **Update**: Click Edit button, modify details
4. **Delete**: Click Delete button

### Test Status Changes

- Click "✅ Paid" button on an active debt
- Toggle "Show Paid Off Debts" on Dashboard
- Verify debt appears in Paid Off section

## 🐛 Common Issues

**"Connection refused" error**
→ Make sure MongoDB is running: `brew services list` or `systemctl status mongodb`

**"Module not found" error**
→ Reinstall dependencies: `pip install -r requirements.txt`

**Port already in use**
→ Kill existing process: `lsof -ti:8000 | xargs kill` or `lsof -ti:8501 | xargs kill`

**Import errors in frontend**
→ Make sure you're running from the Debt-Manager-Portal directory

## 📊 API Testing with curl

Test the backend directly:

```bash
# Health check
curl http://localhost:8000/health

# Get all debts
curl http://localhost:8000/debts/

# Create a debt
curl -X POST http://localhost:8000/debts/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Company",
    "amount_owed": 1000.00,
    "minimum_payment": 200.00,
    "due_date": "2025-11-01",
    "status": "Active Debt",
    "notes": "Test debt"
  }'
```

## 🎓 Next Steps

1. Explore the API documentation at http://localhost:8000/docs
2. Customize notifications in `core/config.py` (DUE_DATE_WARNING_DAYS)
3. Add your real debt data
4. Monitor your payments through the Dashboard

## 💡 Tips

- Use descriptive company names for better BNPL grouping
- Add notes to track account numbers and payment details
- Check Dashboard daily for payment reminders
- Mark debts as paid immediately after payment
- Keep paid-off records for financial history

---

**Need help?** Check README.md for detailed documentation.
