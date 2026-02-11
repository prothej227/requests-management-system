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

# Ensure Python 3
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

# Activate venv based on OS
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

# Windows sed compatibility
if [ "$PLATFORM" = "Mac" ]; then
    sed -i '' "s|^sqlalchemy.url.*|sqlalchemy.url = sqlite:///$DB_NAME|" alembic.ini
else
    sed -i.bak "s|^sqlalchemy.url.*|sqlalchemy.url = sqlite:///$DB_NAME|" alembic.ini
fi

# Patch env.py
ENV_FILE="migrations/env.py"

if ! grep -q "from app.core.database import Base" "$ENV_FILE"; then
    sed -i.bak "/fileConfig/a\\
from app.core.database import Base" "$ENV_FILE"
fi

sed -i.bak "s|target_metadata = None|target_metadata = Base.metadata|" "$ENV_FILE"

echo "[INFO] Alembic configured successfully."

cd ..

# ==============================
# 5. FRONTEND BUILD
# ==============================
echo "[INFO] Building Vue frontend..."

cd frontend
npm install
npm run build   # [INFO] Already outputs to ../backend/app/static
cd ..

# ==============================
# 6. DONE
# ==============================
echo "[SUCCESS] Production build completed successfully!"
