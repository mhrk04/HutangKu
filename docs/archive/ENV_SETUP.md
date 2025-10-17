# 🔧 Environment Configuration Guide

## Overview

Your Debt Management Portal now uses a `.env` file for configuration. This allows you to easily customize settings without modifying code.

## ✅ What's Been Set Up

1. **`.env`** - Your active configuration file (already created)
2. **`.env.example`** - Template with all available options
3. **`core/config.py`** - Automatically loads `.env` settings

## 📝 Current Configuration

Your `.env` file contains:

```env
# API Configuration
API_HOST=localhost
API_PORT=8000

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=debt_management

# Application Settings
DEBUG_MODE=False
DUE_DATE_WARNING_DAYS=7
```

## 🎯 How It Works

1. **On application start**, `core/config.py` loads the `.env` file
2. **All components** (backend, frontend) use `settings` from `core/config.py`
3. **Environment variables** override default values

## 🔧 Common Customizations

### Change API Port

```env
API_PORT=8080
```

Then restart the app - it will run on port 8080 instead of 8000.

### Use MongoDB Atlas (Cloud)

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=debt_management
```

### Enable Debug Mode

```env
DEBUG_MODE=True
```

This shows:

- Debug messages in logs
- ⚠️ Debug Mode indicator in frontend sidebar

### Change Warning Period

```env
DUE_DATE_WARNING_DAYS=14
```

Now debts due within 14 days (instead of 7) will show warnings.

## 📁 File Locations

```
Debt-Manager-Portal/
├── .env              # ← Your active config (git ignored)
├── .env.example      # ← Template (committed to git)
└── core/
    └── config.py     # ← Loads .env file
```

## 🔐 Security Notes

**Important:** The `.env` file is already in `.gitignore` and will NOT be committed to git.

✅ **DO:**

- Keep `.env` private and secure
- Use `.env.example` to share configuration templates
- Use environment variables for sensitive data (passwords, API keys)

❌ **DON'T:**

- Commit `.env` to version control
- Share `.env` file publicly
- Store passwords in plain text (use MongoDB auth if needed)

## 🚀 Quick Start

### First Time Setup

The `.env` file is already created for you! Just run:

```bash
./setup.sh
./run_app.sh
```

### Modify Configuration

1. Edit `.env` file:

   ```bash
   nano .env
   # or
   code .env
   ```

2. Update the values you want to change

3. Restart the application:
   ```bash
   ./run_app.sh
   ```

### Reset to Defaults

```bash
cp .env.example .env
```

## 🧪 Testing Configuration

### Verify Settings Are Loaded

```bash
source venv/bin/activate
python -c "from core.config import settings; print(f'API: {settings.API_BASE_URL}'); print(f'MongoDB: {settings.MONGODB_URI}')"
```

### Check in Frontend

1. Start the app: `./run_app.sh`
2. Look at the sidebar - it shows:
   - Backend URL (from config)
   - Debug mode indicator (if enabled)
   - App name and version

## 📋 All Available Settings

| Variable                | Default                     | Description                  |
| ----------------------- | --------------------------- | ---------------------------- |
| `API_HOST`              | `localhost`                 | Backend API hostname         |
| `API_PORT`              | `8000`                      | Backend API port             |
| `MONGODB_URI`           | `mongodb://localhost:27017` | MongoDB connection string    |
| `MONGODB_DB_NAME`       | `debt_management`           | Database name                |
| `DEBUG_MODE`            | `False`                     | Enable debug mode            |
| `DUE_DATE_WARNING_DAYS` | `7`                         | Days before due date to warn |

## 💡 Advanced Usage

### Environment-Specific Configs

**Development:**

```env
DEBUG_MODE=True
MONGODB_URI=mongodb://localhost:27017
```

**Production:**

```env
DEBUG_MODE=False
MONGODB_URI=mongodb+srv://prod-cluster.mongodb.net
```

### Using System Environment Variables

Instead of `.env` file, you can set system environment variables:

```bash
export API_PORT=8080
export DEBUG_MODE=True
./run_app.sh
```

System environment variables override `.env` file values.

### Docker/Cloud Deployment

Most cloud platforms (Heroku, Render, Railway) let you set environment variables in their dashboard. The app will automatically use those instead of `.env`.

## 🐛 Troubleshooting

### Settings Not Loading

**Problem:** Changes to `.env` not taking effect

**Solution:**

```bash
# 1. Verify .env exists
ls -la .env

# 2. Check .env is being loaded
python -c "from core.config import settings; print(settings.API_BASE_URL)"

# 3. Restart the app
./run_app.sh
```

### Import Error: No module named 'dotenv'

**Problem:** `python-dotenv` not installed

**Solution:**

```bash
source venv/bin/activate
pip install python-dotenv
# or
./setup.sh  # Reinstall all dependencies
```

### Wrong Configuration Values

**Problem:** App uses wrong settings

**Solution:**

```bash
# Check what's in .env
cat .env

# Verify no typos (e.g., DEBUG_MODE not DEBUG-MODE)
# Verify no spaces around = (correct: DEBUG_MODE=True)
```

## 📚 Additional Resources

- **`.env.example`** - See all available options with comments
- **`core/config.py`** - See how settings are loaded and used
- **`frontend/Home.py`** - Example of using settings in code

## ✨ Quick Reference

**View current config:**

```bash
cat .env
```

**Edit config:**

```bash
nano .env
```

**Reset to defaults:**

```bash
cp .env.example .env
```

**Test config:**

```bash
python -c "from core.config import settings; print(settings.API_BASE_URL)"
```

---

**Your configuration is ready to use! 🎉**

Need to change settings? Just edit `.env` and restart the app!
