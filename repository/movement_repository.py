# import pandas as pd
# from database.connection import get_db_connection

# class MovementRepository:
#     async def log_rejection(self, product_id: str, warehouse_id: str, delta: int, reason: str):
#         async with await get_db_connection() as db:
#             await db.execute("""
#                 INSERT INTO rejected_movements (product_id, warehouse_id, attempted_delta, reason)
#                 VALUES (?, ?, ?, ?)
#             """, (product_id, warehouse_id, delta, reason))
#             await db.commit()

#     async def fetch_audit_log(self, limit: int = 50) -> pd.DataFrame:
#         async with await get_db_connection() as db:
#             async with db.execute(
#                 "SELECT id, product_id, warehouse_id, delta, timestamp FROM audit_log ORDER BY id DESC LIMIT ?",
#                 (limit,)
#             ) as cursor:
#                 rows = await cursor.fetchall()
#                 return pd.DataFrame([dict(row) for row in rows])

#     async def fetch_rejected_log(self, limit: int = 50) -> pd.DataFrame:
#         async with await get_db_connection() as db:
#             async with db.execute(
#                 "SELECT id, product_id, warehouse_id, attempted_delta, reason, timestamp FROM rejected_movements ORDER BY id DESC LIMIT ?",
#                 (limit,)
#             ) as cursor:
#                 rows = await cursor.fetchall()
#                 return pd.DataFrame([dict(row) for row in rows])

import pandas as pd
from database.connection import get_db_connection

class MovementRepository:
    def log_rejection(self, product_id: str, warehouse_id: str, delta: int, reason: str):
        with get_db_connection() as db:
            db.execute("""
                INSERT INTO rejected_movements (product_id, warehouse_id, attempted_delta, reason)
                VALUES (?, ?, ?, ?)
            """, (product_id, warehouse_id, delta, reason))
            db.commit()

    def fetch_audit_log(self, limit: int = 50) -> pd.DataFrame:
        with get_db_connection() as db:
            cursor = db.execute(
                "SELECT id, product_id, warehouse_id, delta, timestamp FROM audit_log ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            return pd.DataFrame([dict(row) for row in rows])

    def fetch_rejected_log(self, limit: int = 50) -> pd.DataFrame:
        with get_db_connection() as db:
            cursor = db.execute(
                "SELECT id, product_id, warehouse_id, attempted_delta, reason, timestamp FROM rejected_movements ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            return pd.DataFrame([dict(row) for row in rows])