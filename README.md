# 💰 HutangKu - Debt Management

A full-stack Python application for managing personal debt records with a focus on Buy Now Pay Later (BNPL) tracking and payment notifications.

## 🎯 Features

- **📊 Dashboard**: Real-time overview with visual charts and KPIs
- **🚨 Urgent Notifications**: Automatic alerts for overdue and due-soon payments
- **📈 Visual Analytics**: Pie charts, bar graphs for debt composition and company breakdown
- **🏢 BNPL Grouping**: Organize debts by company/creditor
- **✏️ CRUD Operations**: Create, read, update, and delete debt records
- **✅ Status Tracking**: Mark debts as "Active Debt" or "Paid Off"
- **📱 Responsive UI**: Clean, intuitive Streamlit interface

## 🏗️ Architecture

**Full-Stack Python (FSM Stack)**

- **Backend**: FastAPI with MongoDB (async operations) - Port 8000
- **Frontend**: Streamlit multi-page application - Port 8501
- **Database**: MongoDB for document storage

## 📁 Project Structure

```
Debt-Manager-Portal/
├── core/                    # Shared configuration
│   └── config.py           # Settings (API URL, MongoDB URI)
├── backend/                # FastAPI backend (Port 8000)
│   ├── main.py            # FastAPI app initialization
│   ├── database/          # MongoDB operations
│   │   ├── connection.py  # Database connection
│   │   └── crud_db.py     # CRUD operations
│   ├── models/            # Pydantic schemas
│   │   ├── debt_schema.py    # Debt data models
│   │   └── response_schema.py # API responses
│   └── routers/           # API endpoints
│       └── debt_router.py # Debt CRUD endpoints
├── frontend/              # Streamlit UI (Port 8501)
│   ├── Dashboard.py       # Main dashboard with charts
│   ├── pages/            # Multi-page app
│   │   └── 2_Manage_Debts.py  # CRUD interface
│   └── utils/
│       └── api_client.py # HTTP client for API calls
├── requirements.txt      # Python dependencies
├── run_app.sh           # Start script
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- MongoDB (local or Atlas)

### Installation

**Step 1: Install MongoDB**

macOS:

```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

Linux (Ubuntu/Debian):

```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

Windows: Download from https://www.mongodb.com/try/download/community

**Step 2: Setup Project**

```bash
cd Debt-Manager-Portal

# Make scripts executable
chmod +x setup.sh run_app.sh

# Run setup (creates venv and installs dependencies)
./setup.sh
```

**Step 3: Configure MongoDB (Optional)**

Edit `core/config.py` if using custom MongoDB URI:

```python
MONGODB_URI = "mongodb://localhost:27017"  # Default
# Or for MongoDB Atlas:
# MONGODB_URI = "mongodb+srv://user:pass@cluster.mongodb.net"
```

4. **Start MongoDB** (if using local installation)

   ```bash
   # macOS
   brew services start mongodb-community

   # Linux
   sudo systemctl start mongodb

   # Or run manually
   mongod
   ```

### Running the Application

#### Quick Start (Recommended)

```bash
# Make script executable (first time only)
chmod +x run_app.sh

# Run the application
./run_app.sh
```

This automatically starts both backend (port 8000) and frontend (port 8501). Press `Ctrl+C` to stop.

#### Manual Start (Development)

**Terminal 1 - Backend:**

```bash
source venv/bin/activate
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**

```bash
source venv/bin/activate
streamlit run frontend/Dashboard.py
```

- Backend: <http://localhost:8000>
- API Docs: <http://localhost:8000/docs>
- Frontend: <http://localhost:8501>

## 📊 Data Model

| Field             | Type   | Description                       |
| ----------------- | ------ | --------------------------------- |
| `id`              | String | MongoDB ObjectId (auto-generated) |
| `company_name`    | String | Creditor/company name             |
| `amount_owed`     | Float  | Current outstanding balance       |
| `minimum_payment` | Float  | Minimum payment required          |
| `due_date`        | Date   | Payment due date (ISO 8601)       |
| `status`          | String | "Active Debt" or "Paid Off"       |
| `notes`           | String | Optional notes/account info       |

## 🎨 Application Pages

### Dashboard (Main Page)

- **Urgent Notifications**: Highlights overdue and due-soon payments
- **KPI Cards**: Total outstanding, overdue debt, settled debts, due soon
- **Visual Charts**:
  - Debt composition pie chart (Active/Paid Off/Overdue)
  - Outstanding debt by company bar chart
- **Company Grouping**: Expandable sections showing debts by company
- **Debug Tools**: Optional data viewer for troubleshooting

### Manage Debts

- **Add New Debt**: Create debt records with validation
- **Edit Debt**: Update existing records
- **Mark Paid**: Quick action to mark as paid off
- **Delete**: Remove debt records with confirmation
- **Status Filter**: Toggle between active and paid-off debts

## 🔌 API Endpoints

| Method | Endpoint      | Description                |
| ------ | ------------- | -------------------------- |
| GET    | `/`           | API status check           |
| GET    | `/health`     | Health check               |
| GET    | `/debts/`     | Get all debts (filterable) |
| GET    | `/debts/{id}` | Get single debt            |
| POST   | `/debts/`     | Create new debt            |
| PUT    | `/debts/{id}` | Update debt                |
| DELETE | `/debts/{id}` | Delete debt                |

**Interactive API Docs**: http://localhost:8000/docs

## 🛠️ Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
# API Configuration
API_HOST=localhost
API_PORT=8000

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=debt_management

# Notification Settings (days)
DUE_DATE_WARNING_DAYS=7
```

## 📝 Usage Examples

### Adding a Debt

1. Navigate to "Manage Debts" from sidebar
2. Fill in the debt form (company name, amount owed, minimum payment, due date)
3. Add optional notes
4. Click "Add Debt"

### Viewing Dashboard

1. Open the app (automatically shows Dashboard)
2. View urgent notifications at the top (overdue and due-soon payments)
3. Check KPI cards for quick overview
4. Review visual charts for debt composition
5. Expand company sections to see detailed debt information

### Marking Debt as Paid

1. Go to "Manage Debts"
2. Find the debt in the list
3. Click "✅ Paid" button
4. Debt status changes to "Paid Off"

## 🐛 Troubleshooting

### Backend Issues

- **Won't start**: Check MongoDB is running (`brew services list` on macOS)
- **Port in use**: Kill process on port 8000 (`lsof -i :8000` then `kill -9 <PID>`)
- **Connection error**: Verify MongoDB URI in `core/config.py`

### Frontend Issues

- **Can't connect**: Ensure backend is running on <http://localhost:8000>
- **Import errors**: Activate venv and reinstall (`pip install -r requirements.txt`)
- **Page not found**: Check you're running `streamlit run frontend/Dashboard.py`

### Data Issues

- **Charts empty**: Use debug expander to view raw data
- **Dates incorrect**: Ensure dates are in ISO format (YYYY-MM-DD)
- **Amount shows 0**: Check that numeric values aren't stored as strings

## 🧪 Development

### Tech Stack

**Backend:**

- `fastapi==0.104.1` - Modern async web framework
- `uvicorn==0.24.0` - ASGI server
- `motor==3.3.2` - Async MongoDB driver
- `pydantic==2.5.0` - Data validation

**Frontend:**

- `streamlit==1.28.2` - Rapid UI framework
- `pandas==2.1.3` - Data manipulation
- `plotly==5.18.0` - Interactive charts
- `requests==2.31.0` - HTTP client

### Adding Features

- **New API endpoint**: Edit `backend/routers/debt_router.py`
- **New DB operation**: Edit `backend/database/crud_db.py`
- **New UI page**: Create `frontend/pages/X_PageName.py`
- **New data field**: Update `backend/models/debt_schema.py` and `crud_db.py`

### Virtual Environment

The project uses a Python virtual environment (`venv/`) to isolate dependencies:

```bash
# Activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Deactivate
deactivate
```

## 📚 Documentation Summary

This README consolidates information from:

- **INSTALLATION.md**: Detailed installation steps for all platforms
- **QUICKSTART.md**: Fast 5-minute setup guide
- **IMPLEMENTATION_SUMMARY.md**: Complete implementation details and design specs
- **ENV_SETUP.md**: Environment configuration guide
- **VENV_SETUP.md**: Virtual environment setup details
- **CLEANUP_SUMMARY.md**: Recent project cleanup and improvements

All essential information is now in this single README for easy reference.

## 🎉 Project Status

✅ **Production Ready**

- Full CRUD operations implemented
- Visual dashboard with charts
- Urgent payment notifications
- Company-based debt grouping
- Responsive UI with Streamlit
- RESTful API with FastAPI
- MongoDB persistence
- Code quality improvements completed (October 2025)

## 📜 License

MIT License - Feel free to use and modify for personal or commercial projects.

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support

For issues, questions, or feature requests:

- Open an issue on GitHub
- Check troubleshooting section above
- Review API docs at <http://localhost:8000/docs>

---

**Built with ❤️ using FastAPI, Streamlit, and MongoDB**
