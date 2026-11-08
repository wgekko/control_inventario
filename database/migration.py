# import os
# from database.connection import get_db_connection
# from config.settings import BASE_DIR

# async def init_db():
#     schema_path = BASE_DIR / "database" / "schema.sql"
#     with open(schema_path, "r", encoding="utf-8") as f:
#         sql_script = f.read()

#     async with await get_db_connection() as db:
#         await db.executescript(sql_script)
#         await db.commit()

#         # Cargar semillas si la DB está vacía
#         async with db.execute("SELECT COUNT(*) FROM inventory") as cursor:
#             count = (await cursor.fetchone())[0]
#             if count == 0:
#                 await db.executemany("""
#                     INSERT INTO inventory (product_id, warehouse_id, quantity, min_stock, unit_cost)
#                     VALUES (?, ?, ?, ?, ?)
#                 """, [
#                     ("Teclado Mecánico RGB", "Bodega SCL", 100, 15, 45.0),
#                     ("Mouse Inalámbrico Pro", "Bodega LIM", 45, 10, 25.0),
#                     ("Monitor 4K 27 Inch", "Bodega BOG", 12, 15, 280.0),
#                     ("Laptop ThinkPad T480", "Bodega CDMX", 8, 10, 450.0),
#                     ("Memoria RAM DDR4 16GB", "Bodega SCL", 5, 15, 60.0),
#                     ("Disco SSD NVMe 1TB", "Bodega LIM", 25, 10, 95.0)
#                 ])
#                 await db.commit()

import os
from database.connection import get_db_connection
from config.settings import BASE_DIR

def init_db():
    schema_path = BASE_DIR / "database" / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    with get_db_connection() as db:
        db.executescript(sql_script)
        db.commit()

        cursor = db.execute("SELECT COUNT(*) FROM inventory")
        count = cursor.fetchone()[0]
        if count == 0:
            db.executemany("""
                INSERT INTO inventory (product_id, warehouse_id, quantity, min_stock, unit_cost)
                VALUES (?, ?, ?, ?, ?)
            """, [
                ("Teclado Mecánico RGB", "Bodega SCL", 100, 15, 45.0),
                ("Mouse Inalámbrico Pro", "Bodega LIM", 45, 10, 25.0),
                ("Monitor 4K 27 Inch", "Bodega BOG", 12, 15, 280.0),
                ("Laptop ThinkPad T480", "Bodega CDMX", 8, 10, 450.0),
                ("Memoria RAM DDR4 16GB", "Bodega SCL", 5, 15, 60.0),
                ("Disco SSD NVMe 1TB", "Bodega LIM", 25, 10, 95.0)
            ])
            db.commit()