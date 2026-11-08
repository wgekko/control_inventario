# import aiosqlite
# import os
# from config.settings import DB_FILE, BUSY_TIMEOUT_MS

# async def get_db_connection():
#     # Asegurar que el directorio exista
#     os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
#     db = await aiosqlite.connect(DB_FILE)
#     await db.execute("PRAGMA journal_mode=WAL;")
#     await db.execute("PRAGMA synchronous=NORMAL;")
#     await db.execute(f"PRAGMA busy_timeout={BUSY_TIMEOUT_MS};")
#     db.row_factory = aiosqlite.Row
#     return db

import sqlite3
import os
from config.settings import DB_FILE, BUSY_TIMEOUT_MS

def get_db_connection():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE, timeout=BUSY_TIMEOUT_MS / 1000.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.row_factory = sqlite3.Row
    return conn