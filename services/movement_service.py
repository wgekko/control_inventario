# import pandas as pd
# from services.inventory_service import InventoryService
# from repository.movement_repository import MovementRepository

# class MovementService:
#     def __init__(self, inventory_service: InventoryService):
#         self.inv_service = inventory_service
#         self.mov_repo = MovementRepository()

#     async def bulk_upload_from_dataframe(self, df: pd.DataFrame, default_warehouse: str) -> int:
#         count = 0
#         for _, row in df.iterrows():
#             product = str(row['Producto']).strip()
#             quantity = int(row['Cantidad'])
#             warehouse = str(row.get('Bodega', default_warehouse)).strip()
#             await self.inv_service.add_movement(product, warehouse, quantity)
#             count += 1
#         return count

#     async def get_audit_logs(self) -> pd.DataFrame:
#         return await self.mov_repo.fetch_audit_log()

#     async def get_rejected_logs(self) -> pd.DataFrame:
#         return await self.mov_repo.fetch_rejected_log()

import pandas as pd
from services.inventory_service import InventoryService
from repository.movement_repository import MovementRepository

class MovementService:
    def __init__(self, inventory_service: InventoryService):
        self.inv_service = inventory_service
        self.mov_repo = MovementRepository()

    def bulk_upload_from_dataframe(self, df: pd.DataFrame, default_warehouse: str) -> int:
        count = 0
        for _, row in df.iterrows():
            product = str(row['Producto']).strip()
            quantity = int(row['Cantidad'])
            warehouse = str(row.get('Bodega', default_warehouse)).strip()
            self.inv_service.process_movement(product, warehouse, quantity)
            count += 1
        return count

    def get_audit_logs(self) -> pd.DataFrame:
        return self.mov_repo.fetch_audit_log()

    def get_rejected_logs(self) -> pd.DataFrame:
        return self.mov_repo.fetch_rejected_log()