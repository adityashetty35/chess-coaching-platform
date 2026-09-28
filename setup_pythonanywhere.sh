#!/usr/bin/env bash
# ==============================================================================
# One-Step Automated Setup Script for PythonAnywhere
# Run this inside your PythonAnywhere Bash console:
#   git clone https://github.com/adityashetty35/chess-coaching-platform.git
#   cd chess-coaching-platform
#   bash setup_pythonanywhere.sh
# ==============================================================================

set -e

PA_USER=$(whoami)
PROJECT_DIR="/home/${PA_USER}/chess-coaching-platform"
VENV_DIR="${PROJECT_DIR}/venv"

echo "========================================================"
echo "♟️ Deploying Grandmaster Chess Platform for user: ${PA_USER}"
echo "========================================================"

# 1. Create Virtualenv if not exists
if [ ! -d "${VENV_DIR}" ]; then
    echo "📦 Creating Python 3.10 virtual environment..."
    python3.10 -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"

# 2. Upgrade pip and install requirements
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Apply database migrations
echo "🗄️ Running migrations..."
python manage.py migrate

# 4. Load realistic demo data (coach, students, attendance, fees, etc.)
echo "♟️ Loading demo data..."
python manage.py load_demo_data

# 5. Collect static assets
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "========================================================"
echo "✅ Backend setup completed successfully!"
echo "========================================================"
echo ""
echo "Follow these 3 quick steps in your PythonAnywhere Dashboard (https://www.pythonanywhere.com/web_app_setup/):"
echo ""
echo "1️⃣ In the 'Web' tab, click 'Add a new web app' ➔ Manual configuration ➔ Python 3.10:"
echo "   • Source code:      ${PROJECT_DIR}"
echo "   • Working dir:      ${PROJECT_DIR}"
echo "   • Virtualenv:       ${VENV_DIR}"
echo ""
echo "2️⃣ In the 'Static files' section, add these mappings:"
echo "   • URL: /static/     Directory: ${PROJECT_DIR}/staticfiles"
echo "   • URL: /media/      Directory: ${PROJECT_DIR}/media"
echo ""
echo "3️⃣ Click on the WSGI configuration file link and replace its content with:"
echo "--------------------------------------------------------"
echo "import os"
echo "import sys"
echo ""
echo "path = '${PROJECT_DIR}'"
echo "if path not in sys.path:"
echo "    sys.path.append(path)"
echo ""
echo "os.environ['DJANGO_SETTINGS_MODULE'] = 'chess_coaching.settings'"
echo ""
echo "from django.core.wsgi import get_wsgi_application"
echo "application = get_wsgi_application()"
echo "--------------------------------------------------------"
echo ""
echo "Then click the green 'Reload ${PA_USER}.pythonanywhere.com' button at the top!"
echo "========================================================"
