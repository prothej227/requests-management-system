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

echo "[INFO] Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip

echo "[INFO] Installing backend dependencies..."
pip install -r requirements.tx

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
echo "[INFO] To start FastAPI: "
echo "   gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:\$PORT --workers 2 --chdir backend"
