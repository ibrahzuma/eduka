#!/bin/bash
# fix_502.sh - Emergency Repair Script

echo "--- Starting Emergency Repair ---"

# 1. Stop Gunicorn to release locks
echo "[1/6] Stopping Gunicorn..."
sudo systemctl stop gunicorn

# 2. Update Code
echo "[2/6] Pulling latest code..."
git pull origin main

# 3. Virtual Environment
echo "[3/6] Activating Venv & Installing Requirements..."
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Warning: No 'venv' folder found. Assuming system python or handled elsewhere."
fi
pip install -r requirements.txt

# 4. Migrations (Crucial)
echo "[4/6] Fixing Database..."
# Force making migrations for subscriptions app
python manage.py makemigrations subscriptions
python manage.py makemigrations
python manage.py migrate

# 5. Static Files
echo "[5/6] Collecting Static Files..."
python manage.py collectstatic --noinput

# 6. Check & Restart
echo "[6/6] Checking for Errors & Restarting..."
if python manage.py check; then
    echo "Check Passed. Restarting Server..."
    sudo systemctl start gunicorn
    sudo systemctl status gunicorn --no-pager
    echo "--- SUCCESS! Server should be online. ---"
else
    echo "--- FAILURE! Code check failed. See errors above. ---"
    exit 1
fi
