#!/bin/bash
set -e

echo "[INFO] Starting full production build..."

# ==============================
# 0. Detect OS
# ==============================
OS_TYPE="$(uname -s)"

case "${OS_TYPE}" in
    Linux*)     PLATFORM="Linux" ;;
    Darwin*)    PLATFORM="Mac" ;;
    CYGWIN*|MINGW*|MSYS*) PLATFORM="Windows" ;;
    *)          PLATFORM="Unknown" ;;
esac

echo "[INFO] Detected OS: $PLATFORM"

# ==============================
# 1. Detect Python
# ==============================
if command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
else
    echo "[ERROR] Python not found."
    exit 1
fi

echo "[INFO] Using Python command: $PYTHON_CMD"

PY_VERSION=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
if [ "$PY_VERSION" -lt 3 ]; then
    echo "[ERROR] Python 3 is required."
    exit 1
fi

# ==============================
# 2. BACKEND SETUP
# ==============================
cd backend

if [ ! -d ".venv" ]; then
    echo "[INFO] Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
fi

if [ "$PLATFORM" = "Windows" ]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

echo "[INFO] Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip

echo "[INFO] Installing backend dependencies..."
pip install -r requirements.txt

# ==============================
# 3. ALEMBIC INIT
# ==============================
if [ ! -d "migrations" ]; then
    echo "[INFO] Initializing Alembic..."
    alembic init migrations
fi

# ==============================
# 4. ASK FOR DATABASE FILE
# ==============================
read -p "Enter SQLite DB filename (default: database.db): " DB_NAME

if [ -z "$DB_NAME" ]; then
    DB_NAME="database.db"
fi

echo "[INFO] Using DB file: $DB_NAME"

if [ "$PLATFORM" = "Mac" ]; then
    sed -i '' "s|^sqlalchemy.url.*|sqlalchemy.url = sqlite:///$DB_NAME|" alembic.ini
else
    sed -i.bak "s|^sqlalchemy.url.*|sqlalchemy.url = sqlite:///$DB_NAME|" alembic.ini
fi

# ==============================
# 5. PATCH env.py
# ==============================
ENV_FILE="migrations/env.py"

# Insert Base import if missing
if ! grep -q "from app.core.database import Base" "$ENV_FILE"; then
    sed -i.bak "/fileConfig/a\\
from app.core.database import Base" "$ENV_FILE"
fi

# Insert models import right after Base
if ! grep -q "from app.models import \*" "$ENV_FILE"; then
    sed -i.bak "/from app.core.database import Base/a\\
from app.models import *" "$ENV_FILE"
fi

# Set target_metadata
sed -i.bak "s|target_metadata = None|target_metadata = Base.metadata|" "$ENV_FILE"

echo "[INFO] Alembic configured successfully."

# ==============================
# 6. RUN MIGRATIONS
# ==============================
echo "[INFO] Creating initial migration..."
alembic revision --autogenerate -m "initial setup"

echo "[INFO] Applying migrations..."
alembic upgrade head

cd ..

# ==============================
# 7. FRONTEND BUILD
# ==============================
echo "[INFO] Building Vue frontend..."

cd frontend
npm install
npm run build
cd ..

# ==============================
# 8. DONE
# ==============================
echo "[SUCCESS] Production build completed successfully!"
