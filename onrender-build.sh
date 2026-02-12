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

# Activate venv
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
# Pre_3. INIT ALEMBIC IF MISSING
# ==============================
if [ ! -d "migrations" ]; then
    echo "[INFO] Initializing Alembic migrations..."
    alembic init migrations
fi

# ==============================
# 3. SET DATABASE PATH
# ==============================
# SQLite in /tmp (writable on Render)
DB_NAME=${DB_NAME:-database.db}
DB_PATH="/tmp/$DB_NAME"
export DATABASE_URL="sqlite+aiosqlite:///$DB_PATH"
echo "[INFO] Using SQLite database: $DB_PATH"

# Update alembic.ini
if [ "$PLATFORM" = "Mac" ]; then
    sed -i '' "s|^sqlalchemy.url.*|sqlalchemy.url = sqlite:///$DB_PATH|" alembic.ini
else
    sed -i "s|^sqlalchemy.url.*|sqlalchemy.url = sqlite:///$DB_PATH|" alembic.ini
fi

# ==============================
# 4. PATCH env.py
# ==============================
ENV_FILE="migrations/env.py"

# Insert Base import if missing
if ! grep -q "from app.core.database import Base" "$ENV_FILE"; then
    if [ "$PLATFORM" = "Mac" ]; then
        sed -i '' "/fileConfig/a\\
from app.core.database import Base" "$ENV_FILE"
    else
        sed -i "/fileConfig/a\\
from app.core.database import Base" "$ENV_FILE"
    fi
fi

# Insert models import right after Base
if ! grep -q "from app.models import \*" "$ENV_FILE"; then
    if [ "$PLATFORM" = "Mac" ]; then
        sed -i '' "/from app.core.database import Base/a\\
from app.models import *" "$ENV_FILE"
    else
        sed -i "/from app.core.database import Base/a\\
from app.models import *" "$ENV_FILE"
    fi
fi

# Set target_metadata
if [ "$PLATFORM" = "Mac" ]; then
    sed -i '' "s|target_metadata = None|target_metadata = Base.metadata|" "$ENV_FILE"
else
    sed -i "s|target_metadata = None|target_metadata = Base.metadata|" "$ENV_FILE"
fi

echo "[INFO] Alembic configured successfully."

# ==============================
# 5. RUN MIGRATIONS
# ==============================
echo "[INFO] Applying Alembic migrations..."
alembic upgrade head

# ==============================
# 6. OPTIONAL: CREATE DEFAULT ADMIN
# ==============================
echo "[INFO] Seeding default admin user..."
python - <<END
from app.core.database import async_session_maker, Base, engine
from app.models import User
import asyncio
import hashlib

async def seed_admin():
    async with async_session_maker() as session:
        result = await session.execute("SELECT * FROM users WHERE username='admin'")
        if result.first() is None:
            admin = User(
                username='admin',
                first_name='Admin',
                last_name='User',
                email='admin@example.com',
                password_hash=hashlib.sha256('Admin1234'.encode()).hexdigest(),
                role='admin',
                is_active=True
            )
            session.add(admin)
            await session.commit()

asyncio.run(seed_admin())
END

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
