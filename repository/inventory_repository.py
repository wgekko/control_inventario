# import pandas as pd
# from database.connection import get_db_connection

# class InventoryRepository:
#     async def fetch_all(self) -> pd.DataFrame:
#         async with await get_db_connection() as db:
#             async with db.execute("SELECT product_id, warehouse_id, quantity, min_stock, unit_cost FROM inventory") as cursor:
#                 rows = await cursor.fetchall()
#                 return pd.DataFrame([dict(row) for row in rows])

#     async def update_batch(self, batch: list):
#         async with await get_db_connection() as db:
#             cursor = await db.executemany("""
#                 UPDATE inventory 
#                 SET quantity = quantity + ? 
#                 WHERE product_id = ? 
#                   AND warehouse_id = ? 
#                   AND (quantity + ?) >= 0;
#             """, [(delta, prod, wh, delta) for prod, wh, delta in batch])
#             await db.commit()
#             return cursor.rowcount

#     async def get_stock(self, product_id: str, warehouse_id: str) -> int:
#         async with await get_db_connection() as db:
#             async with db.execute(
#                 "SELECT quantity FROM inventory WHERE product_id = ? AND warehouse_id = ?",
#                 (product_id, warehouse_id)
#             ) as cursor:
#                 row = await cursor.fetchone()
#                 return row[0] if row else None

import pandas as pd
from database.connection import get_db_connection

class InventoryRepository:
    def fetch_all(self) -> pd.DataFrame:
        with get_db_connection() as db:
            cursor = db.execute("SELECT product_id, warehouse_id, quantity, min_stock, unit_cost FROM inventory")
            rows = cursor.fetchall()
            return pd.DataFrame([dict(row) for row in rows])

    def update_stock(self, product_id: str, warehouse_id: str, delta: int) -> bool:
        """Actualiza el stock respetando la regla de negocio atómica (quantity + delta >= 0)."""
        with get_db_connection() as db:
            cursor = db.execute("""
                UPDATE inventory 
                SET quantity = quantity + ? 
                WHERE product_id = ? 
                  AND warehouse_id = ? 
                  AND (quantity + ?) >= 0;
            """, (delta, product_id, warehouse_id, delta))
            db.commit()
            return cursor.rowcount > 0