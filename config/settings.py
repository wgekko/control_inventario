import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = os.getenv("DB_FILE", str(BASE_DIR / "database" / "inventario_enterprise.db"))

QUEUE_MAX_SIZE = 10000
BATCH_SIZE = 500
WORKER_SLEEP_INTERVAL = 0.05
BUSY_TIMEOUT_MS = 5000